use palette::{Oklch, Srgb, FromColor};

#[derive(Clone, Copy, Debug)]
pub struct Rgb { pub r: u8, pub g: u8, pub b: u8 }

// Light Mode OKLCH (from demo CSS)
// :root[data-theme="light"]
//   --secondary: oklch(0.4820 0.0825 206.0615)
//   --primary:   oklch(0.5855 0.1006 208.0245)
//   --accent:    oklch(0.6697 0.1154 208.9445)
const SEC: Oklch = Oklch::new(0.4820, 0.0825, 206.0615);
const PRI: Oklch = Oklch::new(0.5855, 0.1006, 208.0245);
const ACC: Oklch = Oklch::new(0.6697, 0.1154, 208.9445);

fn to_rgb(ok: Oklch) -> Rgb {
    let srgb: Srgb = Srgb::from_color(ok);
    let (r, g, b) = (srgb.red, srgb.green, srgb.blue);
    Rgb {
        r: (r.clamp(0.0, 1.0) * 255.0).round() as u8,
        g: (g.clamp(0.0, 1.0) * 255.0).round() as u8,
        b: (b.clamp(0.0, 1.0) * 255.0).round() as u8,
    }
}

pub fn light_blue_stops() -> [Rgb; 3] {
    [to_rgb(SEC), to_rgb(PRI), to_rgb(ACC)]
}

pub fn dna_preset() -> (Rgb, Rgb) { (Rgb { r: 0, g: 255, b: 0 }, Rgb { r: 0, g: 0, b: 255 }) }

