#!/usr/bin/env python3
"""
Quick-and-simple cutout for a parchment-background manuscript image to a cursor PNG.

Usage:
  python3 tools/make_snail_cursor.py [input_image] [output_png]

Defaults:
  input_image: assets/icons/snail-source.png (or .jpg/.jpeg/.webp)
  output_png : assets/icons/snail-cursor.png

Notes:
  - This is a heuristic trim tuned for beige/white paper backgrounds.
  - It removes near-paper pixels and keeps saturated/edge details.
  - You can rerun safely; it will overwrite the output.
"""
from __future__ import annotations

import os
import sys
from typing import Tuple

from PIL import Image, ImageFilter, ImageOps


def find_default_input() -> str | None:
    candidates = [
        "assets/icons/snail-source.png",
        "assets/icons/snail-source.jpg",
        "assets/icons/snail-source.jpeg",
        "assets/icons/snail-source.webp",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def compute_mask(img: Image.Image) -> Image.Image:
    # Work in RGB
    rgb = img.convert("RGB")
    w, h = rgb.size
    px = rgb.load()

    # Create mask keeping non-parchment areas
    mask = Image.new("L", (w, h), 0)
    m = mask.load()

    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            # whiteness & low saturation (parchment-ish)
            mx = max(r, g, b)
            mn = min(r, g, b)
            sat = mx - mn
            mean = (r + g + b) / 3

            is_paper = (mean > 190 and sat < 35) or (r > 225 and g > 225 and b > 225)
            m[x, y] = 0 if is_paper else 255

    # Clean mask: blur a bit, then expand and soften edges
    mask = mask.filter(ImageFilter.MedianFilter(size=3))
    mask = mask.filter(ImageFilter.MaxFilter(size=3))
    mask = mask.filter(ImageFilter.GaussianBlur(radius=1.2))
    return mask


def trim_to_content(img: Image.Image, mask: Image.Image) -> Tuple[Image.Image, Image.Image]:
    bbox = mask.getbbox()
    if not bbox:
        return img, mask
    img2 = img.crop(bbox)
    mask2 = mask.crop(bbox)
    return img2, mask2


def make_cursor(input_path: str, output_path: str, out_width: int = 96):
    img = Image.open(input_path)
    mask = compute_mask(img)
    img, mask = trim_to_content(img, mask)

    # Resize to width
    w, h = img.size
    if w > out_width:
        nh = int(h * (out_width / w))
        img = img.resize((out_width, nh), Image.LANCZOS)
        mask = mask.resize((out_width, nh), Image.LANCZOS)

    # Apply alpha and save
    img = img.convert("RGBA")
    img.putalpha(mask)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, format="PNG")
    print(f"Snail cursor saved → {output_path} ({img.size[0]}x{img.size[1]})")


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else (find_default_input() or "")
    if not input_path or not os.path.exists(input_path):
        print("Input image not found. Place your photo at assets/icons/snail-source.png (or .jpg/.webp) or pass a path.")
        sys.exit(1)
    output_path = sys.argv[2] if len(sys.argv) > 2 else "assets/icons/snail-cursor.png"
    make_cursor(input_path, output_path)


if __name__ == "__main__":
    main()

