use super::palette::Rgb;

#[derive(Clone, Copy, Debug)]
pub enum ColorLevel { None, Ansi256, Truecolor }

#[inline]
pub fn lerp(a: f32, b: f32, t: f32) -> f32 { a + (b - a) * t }

// Generate a piecewise-linear gradient over N stops across `len` samples
pub fn piecewise_gradient(len: usize, stops: &[Rgb]) -> Vec<Rgb> {
    if len == 0 || stops.is_empty() { return vec![]; }
    if stops.len() == 1 { return vec![stops[0]; len]; }
    let segments = stops.len() - 1;
    let mut out = Vec::with_capacity(len);
    for i in 0..len {
        let p = if len > 1 { i as f32 / (len as f32 - 1.0) } else { 0.0 };
        let segf = p * segments as f32;
        let s = segf.floor().clamp(0.0, (segments - 1) as f32) as usize;
        let t = (segf - s as f32).clamp(0.0, 1.0);
        let a = stops[s];
        let b = stops[s + 1];
        let r = lerp(a.r as f32, b.r as f32, t).round() as u8;
        let g = lerp(a.g as f32, b.g as f32, t).round() as u8;
        let bch = lerp(a.b as f32, b.b as f32, t).round() as u8;
        out.push(Rgb { r, g, b: bch });
    }
    out
}

