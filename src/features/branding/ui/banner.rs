use std::io::Write;
use crossterm::{queue, style::{SetForegroundColor, ResetColor, Color}, terminal, cursor};
use supports_color::{on_cached, Stream};

use crate::features::branding::theme::{palette, gradient::{self, ColorLevel}};

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

fn center_pad(cols: u16, width: usize) -> u16 {
    if (cols as usize) > width { ((cols as usize - width) / 2) as u16 } else { 0 }
}

pub fn show_startup<W: Write>(mut w: W) -> crossterm::Result<()> {
    let (cols, _) = terminal::size().unwrap_or((120, 40));
    let level = detect_level();
    let stops = palette::light_blue_stops();

    // Print gradient logo, centered
    for line in LOGO.lines() {
        let width = line.chars().count();
        let colors = gradient::piecewise_gradient(width.max(1), &stops);
        let pad_left = center_pad(cols, width);
        if pad_left > 0 { queue!(w, cursor::MoveRight(pad_left))?; }
        for (ch, rgb) in line.chars().zip(colors.into_iter()) {
            let color = match level {
                ColorLevel::Truecolor => rgb_to_color(rgb),
                ColorLevel::Ansi256 => rgb_to_color(rgb), // TODO: quantize to 256 if desired
                ColorLevel::None => Color::Reset,
            };
            if !matches!(level, ColorLevel::None) { queue!(w, SetForegroundColor(color))?; }
            write!(w, "{}", ch)?;
        }
        queue!(w, ResetColor)?;
        writeln!(w)?;
    }

    writeln!(w)?;
    // Tips block (left-aligned; keep simple and readable across terminals)
    writeln!(w, "Tips:")?;
    writeln!(w, "  • Run geneloop auth login to authenticate")?;
    writeln!(w, "  • Explore commands with geneloop help")?;
    writeln!(w, "  • Configure defaults via geneloop config")?;

    Ok(())
}

