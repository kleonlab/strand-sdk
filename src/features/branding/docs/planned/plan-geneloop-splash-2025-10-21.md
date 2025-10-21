# GeneLoop CLI — Startup Splash & Rebrand Plan (2025-10-21)

## 1) Mission & Context
- Goal: Fork OpenAI Codex CLI and rebrand as GeneLoop CLI with a new launch screen that matches the visual style shown (large pixelated ASCII logo, gradient colorway, helpful tips, prompt area), while retaining all core Codex CLI functionality (auth, config, agents).
- Constraints: Keep core behavior intact; banner must degrade gracefully on limited terminals; cross-platform support (macOS/Linux/Windows); minimal new runtime deps; ≤300-line modules; TypeScript + strict types; follow vertical-slice architecture.
- Consumers: Internal engineers, early adopters, and users familiar with Codex CLI who expect stability and clarity.
- Success: Visually distinctive banner using Gene/DNA gradient (#00FF00→#0000FF), frictionless startup on common shells/terminals, no regressions in auth/config/agent flows, docs updated, and a clean release under the new bin `geneloop`.

## 2) Deliverables
- New banner module with ASCII art for "GeneLoop" + DNA gradient.
- Tips section and optional theme selector on first run (opt-in, stored in config).
- Configurable color on/off with robust color detection.
- Updated README and branding strings throughout the CLI.

## 3) Tech Choices (Rust)
- Terminal & colors: `crossterm` for ANSI control + RGB, with `supports-color` (Rust crate) to detect color capability (basic/256/16m).
- Color math: `palette` crate to convert OKLCH (from demo CSS) → sRGB; compute once at startup (negligible cost) or in `build.rs`.
- ASCII art: pre-generated (figlet/artii) and baked as a constant via `include_str!()`.
- Layout: manual box-drawing with Unicode; avoid heavy TUI deps. Keep banner printer ≤200 LOC.

References used (Context7): chalk basic/hex/rgb usage, color levels; figlet.js `textSync`, font listing and custom fonts.

## 4) Architecture Placement (Rust)
- Feature slice: `src/features/branding/`
  - `ui/banner.rs` — banner composition/printing (≤200 lines)
  - `ui/tips.rs` — tips rendering + wrapping helpers (≤120 lines)
  - `theme/palette.rs` — Light Mode OKLCH stops + conversion to sRGB
  - `theme/gradient.rs` — per-char gradient across multi-stop palette
  - `assets/logo_geneloop.txt` — baked ASCII (via `include_str!`)
  - `mod.rs` — `pub fn show_startup<W: Write>(w: &mut W)`
  - `docs/` — plan/summary docs per AGENTS.md

## 5) Step-by-Step Plan
1. Fork & setup
   - Fork Codex CLI → `geneloop-cli`.
   - Node ≥18 LTS; enable ESM if upstream is ESM. Ensure `typescript --strict`.
   - `pnpm`/`npm` install; run existing tests/build.

2. Locate startup entry and splash
   - Search for startup hooks (e.g., `bin/codex`, `src/cli/index.ts`, `src/ui/banner.ts`, usage of `chalk`).
   - Identify the function that prints the initial splash and the first prompt render.

3. Introduce branding slice
   - Create `src/features/branding/` with modules listed in section 4.
   - Wire `showStartup()` into the app’s main entry before the first prompt.

4. Theme + gradient utilities (Rust)
   - Convert Light Mode OKLCH stops → sRGB using `palette`.
   - Implement gradient over N stops (secondary→primary→accent) with piecewise linear interpolation across characters.
   - Detect color capability using `supports_color`; truecolor → RGB; 256-color → quantize; else → monochrome fallback.

5. ASCII art for "GeneLoop"
   - Pre-generate offline (figlet or artii) and bake as a constant file (no runtime figlet dependency).
   - Provide a tiny dev script to regenerate the ASCII on demand; do not ship it in production bundle.

6. Banner composition
   - Gradient-apply per-character across each ASCII line.
   - Add a thin border/padding and title line using Unicode box-drawing.
   - Respect terminal width (center/clamp) via `crossterm::terminal::size`.

7. Tips & prompt area
   - Print 3–5 quick tips (auth, config, help, examples); respect terminal width.
   - Default theme = Light Mode (from demo CSS). Provide `--theme light|dna|mono|none`; persist in config.

8. Cross-platform checks
   - Test on macOS iTerm/Terminal, Ubuntu (xterm-256color), Windows Terminal/PowerShell.
   - Fallback: disable gradients when `chalk.level < 3` (use basic colors or monochrome).

9. Rebrand sweep
   - Rename visible strings from Codex to GeneLoop (banner, help, config headings, telemetry events’ app field).
   - Keep APIs and flags stable; add aliases only where safe.

10. Docs & release
   - Update README, screenshots, and `package.json` (`name: 'geneloop-cli'`, `bin: 'geneloop'`).
   - No publishing yet per scope; prepare docs and screenshots only.

## 6) Code Sketches (TypeScript)

### theme/palette.rs
```rust
// src/features/branding/theme/palette.rs
use palette::{Oklch, Srgb, FromColor, IntoColor};

#[derive(Clone, Copy, Debug)]
pub struct Rgb { pub r: u8, pub g: u8, pub b: u8 }

// Light Mode OKLCH (from demo CSS)
const SEC: Oklch = Oklch::new(0.4820, 0.0825, 206.0615);
const PRI: Oklch = Oklch::new(0.5855, 0.1006, 208.0245);
const ACC: Oklch = Oklch::new(0.6697, 0.1154, 208.9445);

fn to_rgb(ok: Oklch) -> Rgb {
    let srgb: Srgb = Srgb::from_color(ok); // gamma-encoded sRGB in [0,1]
    let (r, g, b) = (srgb.red, srgb.green, srgb.blue);
    Rgb { r: (r.clamp(0.0,1.0)*255.0).round() as u8,
          g: (g.clamp(0.0,1.0)*255.0).round() as u8,
          b: (b.clamp(0.0,1.0)*255.0).round() as u8 }
}

pub fn light_blue_stops() -> [Rgb; 3] { [to_rgb(SEC), to_rgb(PRI), to_rgb(ACC)] }

// Alternate preset
pub fn dna_preset() -> (Rgb, Rgb) { (Rgb{r:0,g:255,b:0}, Rgb{r:0,g:0,b:255}) }
```

### theme/gradient.rs
```rust
// src/features/branding/theme/gradient.rs
use super::palette::Rgb;

#[derive(Clone, Copy, Debug)]
pub enum ColorLevel { None, Ansi256, Truecolor }

pub fn lerp(a: f32, b: f32, t: f32) -> f32 { a + (b - a) * t }

pub fn piecewise_gradient(len: usize, stops: &[Rgb]) -> Vec<Rgb> {
    if len == 0 || stops.is_empty() { return vec![]; }
    if stops.len() == 1 { return vec![stops[0]; len]; }
    let segments = stops.len() - 1;
    let mut out = Vec::with_capacity(len);
    for i in 0..len {
        let p = if len>1 { i as f32 / (len as f32 - 1.0) } else { 0.0 };
        let segf = p * segments as f32;
        let s = segf.floor().clamp(0.0, (segments-1) as f32) as usize;
        let t = (segf - s as f32).clamp(0.0, 1.0);
        let a = stops[s];
        let b = stops[s+1];
        let r = lerp(a.r as f32, b.r as f32, t).round() as u8;
        let g = lerp(a.g as f32, b.g as f32, t).round() as u8;
        let bch = lerp(a.b as f32, b.b as f32, t).round() as u8;
        out.push(Rgb{r, g, b: bch});
    }
    out
}
```

### ui/banner.rs
```rust
// src/features/branding/ui/banner.rs
use std::io::{Write};
use crossterm::{queue, style::{SetForegroundColor, ResetColor, Color}, terminal};
use supports_color::{Stream, on_cached};

use crate::features::branding::theme::{palette, gradient::{piecewise_gradient, ColorLevel}};

const LOGO: &str = include_str!("../assets/logo_geneloop.txt");

fn detect_level() -> ColorLevel {
    match on_cached(Stream::Stdout) {
        Some(lvl) if lvl.has_16m => ColorLevel::Truecolor,
        Some(lvl) if lvl.has_256 => ColorLevel::Ansi256,
        Some(_) => ColorLevel::Ansi256,
        None => ColorLevel::None,
    }
}

fn rgb_to_color(c: palette::Rgb) -> Color { Color::Rgb { r: c.r, g: c.g, b: c.b } }

pub fn show_startup<W: Write>(mut w: W) -> crossterm::Result<()> {
    let (cols, _) = terminal::size().unwrap_or((120, 40));
    let level = detect_level();
    let stops = palette::light_blue_stops();

    for line in LOGO.lines() {
        let width = line.chars().count();
        let colors = piecewise_gradient(width.max(1), &stops);
        let pad_left = if (cols as usize) > width { ((cols as usize - width) / 2) as u16 } else { 0 };
        if pad_left > 0 { queue!(w, crossterm::cursor::MoveRight(pad_left))?; }
        for (ch, rgb) in line.chars().zip(colors.into_iter()) {
            let color = match level { ColorLevel::Truecolor => rgb_to_color(rgb), _ => rgb_to_color(rgb) };
            queue!(w, SetForegroundColor(color))?;
            write!(w, "{}", ch)?;
        }
        queue!(w, ResetColor)?;
        writeln!(w)?;
    }

    // Tips
    writeln!(w)?;
    writeln!(w, "Tips:")?;
    writeln!(w, "  • Run geneloop auth login to authenticate")?;
    writeln!(w, "  • Explore commands with geneloop help")?;
    writeln!(w, "  • Configure defaults via geneloop config")?;
    Ok(())
}
```

### mod.rs (feature entry)
```rust
// src/features/branding/mod.rs
pub mod theme { pub mod palette; pub mod gradient; }
pub mod ui { pub mod banner; }
```

### Wiring in main
```rust
// src/main.rs (or the current entrypoint)
mod features { pub mod branding; }

fn main() -> anyhow::Result<()> {
    features::branding::ui::banner::show_startup(std::io::stdout())?;
    // continue with existing auth/config/agent init…
    Ok(())
}
```

### ui/banner.rs notes
```ts
// src/features/branding/ui/banner.ts
import chalk from 'chalk';
import {gradientLine} from '../theme/colors';

const BORDER = { tl: '╭', tr: '╮', bl: '╰', br: '╯', h: '─', v: '│' } as const;

// Option A: Generate at runtime with figlet (configure font elsewhere)
export function renderAsciiLogo(lines: string[]): string[] { return lines; }

// GeneLoop ASCII (baked, provided by user file)
// Source file: /Users/sethmorton/Downloads/ascii-text-art.txt (16 lines)
// We will paste the final content into src/features/branding/ui/logo.geneloop.ts
// and import it here. Placeholder for now:
// ASCII is embedded via include_str!("../assets/logo_geneloop.txt").
// The file will contain the 16 lines from your provided text.

export function buildBanner(): string {
  const logo = GENELOOP_ASCII.map((line) => gradientLine(line)).join('\n');
  const content = `${logo}\n\n` +
    chalk.dim('Tips:') + '\n' +
    `  • Run ${chalk.bold('geneloop auth login')} to authenticate\n` +
    `  • Explore commands with ${chalk.bold('geneloop help')}\n` +
    `  • Configure defaults via ${chalk.bold('geneloop config')}\n` +
    `  • Start an agent session with ${chalk.bold('geneloop')}\n`;

  const lines = content.split('\n');
  const width = Math.max(...lines.map((l) => l.length));
  const pad = (s: string) => s + ' '.repeat(width - s.length);

  const top = `${BORDER.tl}${BORDER.h.repeat(width + 2)}${BORDER.tr}`;
  const body = lines.map((l) => `${BORDER.v} ${pad(l)} ${BORDER.v}`).join('\n');
  const bottom = `${BORDER.bl}${BORDER.h.repeat(width + 2)}${BORDER.br}`;

  return [top, body, bottom].join('\n');
}

export function showBanner(log = console.log): void {
  log(buildBanner());
}
```

### Offline ASCII generation (dev-only, not shipped)
```ts
// tools/make-ascii.ts (dev script)
// Usage: ts-node tools/make-ascii.ts "GeneLoop" "ANSI Shadow"
import figlet from 'figlet';
const text = process.argv[2] ?? 'GeneLoop';
const font = process.argv[3] ?? 'ANSI Shadow';
const raw = figlet.textSync(text, { font });
console.log(raw);
// Paste the output into src/features/branding/ui/logo.geneloop.ts
```

### Wiring into CLI entry
```ts
// src/cli/index.ts (or equivalent main)
import {showBanner} from '../features/branding';

export async function main() {
  showBanner();
  // existing init: load config → auth check → enter prompt
}
```

## 7) Cross-Platform & Fallbacks
- Use `chalk.level` to detect color support. If `<3`, skip truecolor gradient and use a single accent color.
- Avoid large Unicode blocks that render inconsistently; prefer ASCII/box-drawing characters.
- Respect terminal width (`process.stdout.columns`) and center or clamp banner width when necessary.

## 8) Rebrand Tasks Checklist
- Rename `package.json` → `name: geneloop-cli`; `bin` → `geneloop`.
- Replace user-facing strings: app name, help headers, telemetry app id (if present).
- Keep env vars and config keys backward-compatible or provide aliases.
- Update README badges, examples, and screenshots.

## 9) Test Plan
- Unit: gradient utilities (hex parsing, lerp), banner width calculation, figlet integration (where used).
- Snapshot: banner output under truecolor vs basic color modes.
- Manual: macOS Terminal/iTerm2, Ubuntu xterm-256color, Windows Terminal. Verify monochrome mode with `FORCE_COLOR=0`.

## 10) Open Questions
1) Please share the exact Light Mode gradient from the demo (CSS var names and resolved hex/rgb stops, including angle). We’ll mirror it precisely.
2) Confirm the figlet font you want for the baked logo (e.g., ANSI Shadow, Big). If you already have an ASCII you like, share it and we’ll paste it into constants.
3) Any tagline or subheader you want under “GeneLoop”? E.g., “Terminal-native AI workflows”.
4) Preferred tips list (3–5 bullets) to show in the box? Otherwise I’ll keep the proposed defaults.
