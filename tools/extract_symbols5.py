#!/usr/bin/env python3
"""
Extract transparent PNG icons from arbitrary images and write 5 outputs including Press.

Usage:
  mkdir -p icons/_INBOX
  Drop 5 images (png/jpg/webp) into icons/_INBOX
  python3 tools/extract_symbols5.py

Output:
  icons/about.png, icons/portfolio.png, icons/contact.png, icons/tearsheet.png, icons/press.png
"""
from pathlib import Path
from typing import List
from PIL import Image, ImageFilter

INBOX = Path('icons/_INBOX')
OUT = Path('icons')
OUT_FILES = ['about.png', 'portfolio.png', 'contact.png', 'tearsheet.png', 'press.png']


def ensure_dirs():
    INBOX.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)


def load_candidates() -> List[Path]:
    imgs: List[Path] = []
    for ext in ('*.png', '*.jpg', '*.jpeg', '*.webp'):
        imgs.extend(sorted(INBOX.glob(ext)))
    return imgs


def clean_background(img: Image.Image) -> Image.Image:
    rgb = img.convert('RGB')
    w, h = rgb.size
    px = rgb.load()
    mask = Image.new('L', (w, h), 0)
    m = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            mx, mn = max(r, g, b), min(r, g, b)
            sat = mx - mn
            mean = (r + g + b) / 3
            bg = (mean > 230) or (mean > 200 and sat < 24)
            m[x, y] = 0 if bg else 255
    mask = mask.filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    rgba = img.convert('RGBA')
    rgba.putalpha(mask)
    return rgba


def resize_max(img: Image.Image, max_size: int = 512) -> Image.Image:
    w, h = img.size
    scale = min(1.0, max_size / max(w, h))
    if scale < 1.0:
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    return img


def main():
    ensure_dirs()
    imgs = load_candidates()
    if not imgs:
        print('Place up to 5 images into icons/_INBOX and rerun.')
        return
    def pick(name: str):
        name = name.lower()
        for p in imgs:
            if name in p.name.lower():
                return p
        return None
    ordered: List[Path] = []
    for key in ("about", "portfolio", "contact", "tearsheet", "press"):
        p = pick(key)
        if p: ordered.append(p)
    for p in imgs:
        if p not in ordered:
            ordered.append(p)
    for i, out_name in enumerate(OUT_FILES):
        if i >= len(ordered):
            break
        img = Image.open(ordered[i])
        img = clean_background(img)
        img = resize_max(img, 512)
        out_path = OUT / out_name
        img.save(out_path, 'PNG')
        print(f'Saved {out_path} from {ordered[i].name}')

if __name__ == '__main__':
    main()

