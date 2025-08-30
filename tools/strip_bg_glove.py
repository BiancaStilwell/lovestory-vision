#!/usr/bin/env python3
"""
Quick-and-simple background stripper for the blue glove PNG.
It converts near-cream/light background pixels to transparent while keeping blue tones.

Usage:
  python3 tools/strip_bg_glove.py assets/icons/home.png

Writes in-place (overwrites the input file). Keep a backup if needed.
"""
from pathlib import Path
from PIL import Image, ImageFilter
import statistics
import sys

def corner_bg_color(img: Image.Image, pad: int = 10) -> tuple[int,int,int]:
    rgb = img.convert('RGB')
    w, h = rgb.size
    samples = []
    for (sx, sy) in [(0,0), (w-pad,0), (0,h-pad), (w-pad,h-pad)]:
        for y in range(sy, min(sy+pad, h)):
            for x in range(sx, min(sx+pad, w)):
                samples.append(rgb.getpixel((x,y)))
    # median per channel is robust to noise
    r = statistics.median(c[0] for c in samples)
    g = statistics.median(c[1] for c in samples)
    b = statistics.median(c[2] for c in samples)
    return int(r), int(g), int(b)

def strip_bg(path: Path) -> None:
    img = Image.open(path).convert('RGBA')
    w, h = img.size
    px = img.load()
    bg_r, bg_g, bg_b = corner_bg_color(img)
    # Build alpha mask by distance to background color; fade edges softly
    mask = Image.new('L', (w, h), 255)
    m = mask.load()
    def dist2(r,g,b):
        dr = r-bg_r; dg = g-bg_g; db = b-bg_b
        return dr*dr + dg*dg + db*db
    # thresholds tuned for cream→transparent while preserving blue
    hard = 55**2   # fully transparent if within this distance
    soft = 95**2   # start of fully opaque region beyond this
    for y in range(h):
        for x in range(w):
            r,g,b,a = px[x,y]
            if a < 12:
                m[x,y] = 0
                continue
            d2 = dist2(r,g,b)
            if d2 <= hard:
                m[x,y] = 0
            elif d2 >= soft:
                m[x,y] = 255
            else:
                # linearly ramp alpha between hard and soft thresholds
                t = (d2 - hard) / (soft - hard)
                m[x,y] = int(255 * t)
    mask = mask.filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    out = Image.new('RGBA', (w,h), (0,0,0,0))
    out.paste(img, (0,0), mask)
    out.save(path)
    print(f"Updated {path} with transparent background")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tools/strip_bg_glove.py assets/icons/home.png")
        sys.exit(1)
    p = Path(sys.argv[1])
    if not p.exists():
        print(f"File not found: {p}")
        sys.exit(2)
    strip_bg(p)

if __name__ == '__main__':
    main()
