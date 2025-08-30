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
import sys

def strip_bg(path: Path) -> None:
    img = Image.open(path).convert('RGBA')
    w, h = img.size
    px = img.load()
    # Create alpha mask based on lightness and low saturation (cream background)
    mask = Image.new('L', (w, h), 255)
    m = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 10:
                m[x, y] = 0
                continue
            mx = max(r, g, b)
            mn = min(r, g, b)
            sat = mx - mn
            light = (r + g + b) / 3
            # Heuristic: bright, low-saturation pixels → background
            if (light > 235 and sat < 40) or (light > 210 and sat < 26):
                m[x, y] = 0
            else:
                m[x, y] = 255
    mask = mask.filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
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
