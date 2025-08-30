#!/usr/bin/env python3
"""
Make outline-only PNG symbols from arbitrary source images.

Input:  Put 4 images into `icons/_INBOX/` (any names, PNG/JPG/WebP).
        Backgrounds (white/checkerboard) are removed heuristically.

Output: Overwrites the landing icons in `icons/`:
        - about.png
        - portfolio.png
        - contact.png
        - tearsheet.png

Behavior:
  1) Remove light/low-saturation backgrounds (handles screenshots w/ checkerboard).
  2) Compute a clean binary silhouette mask.
  3) Generate an outline from the silhouette (morphological gradient),
     dilated to a sensible stroke weight.
  4) Color the outline using the average subject color from the source image.

Usage:
  python3 tools/make_outline_symbols.py

Notes:
  - Pure-Pillow implementation (no OpenCV install needed).
  - Re-run anytime; it overwrites outputs.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageFilter, ImageStat

INBOX = Path("icons/_INBOX")
OUT = Path("icons")
OUT_FILES = ["about.png", "portfolio.png", "contact.png", "tearsheet.png"]


def ensure_dirs():
    INBOX.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)


def load_candidates() -> List[Path]:
    imgs: List[Path] = []
    for ext in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
        imgs.extend(sorted(INBOX.glob(ext)))
    return imgs


def _clean_background(img: Image.Image) -> Image.Image:
    """Return an RGBA image with transparent background.

    Heuristic: classify very light or very low-saturation light pixels as background.
    """
    rgb = img.convert("RGB")
    w, h = rgb.size
    src = rgb.load()
    mask = Image.new("L", (w, h), 0)
    m = mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b = src[x, y]
            mx, mn = max(r, g, b), min(r, g, b)
            sat = mx - mn
            mean = (r + g + b) / 3
            bg = (mean > 230) or (mean > 200 and sat < 24)
            m[x, y] = 0 if bg else 255
    # soften mask edges a touch
    mask = mask.filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
    rgba = img.convert("RGBA")
    rgba.putalpha(mask)
    return rgba


def _silhouette(alpha: Image.Image, thr: int = 8) -> Image.Image:
    """Binarize the alpha channel into a clean silhouette mask."""
    a = alpha if alpha.mode == "L" else alpha.convert("L")
    # Threshold then close tiny pinholes
    bw = a.point(lambda p: 255 if p > thr else 0, mode="1").convert("L")
    bw = bw.filter(ImageFilter.MaxFilter(3))  # dilate once
    bw = bw.filter(ImageFilter.MinFilter(3))  # erode back
    return bw


def _outline_from_mask(mask: Image.Image, stroke_px: int = 4) -> Image.Image:
    """Return an outline mask (L), 0 transparent, 255 at edges with given stroke."""
    # morphological gradient: dilate - erode
    dil = mask.filter(ImageFilter.MaxFilter(3))
    ero = mask.filter(ImageFilter.MinFilter(3))
    grad = ImageChops.subtract(dil, ero)
    # Binarize to crisp edges
    grad = grad.point(lambda p: 255 if p > 0 else 0, mode="1").convert("L")
    # Thicken stroke
    for _ in range(max(0, stroke_px // 2)):
        grad = grad.filter(ImageFilter.MaxFilter(3))
    return grad


def _average_subject_color(rgba: Image.Image) -> Tuple[int, int, int]:
    # Compute average over non-transparent pixels
    if rgba.mode != "RGBA":
        rgba = rgba.convert("RGBA")
    r, g, b, a = rgba.split()
    # Mask RGB by alpha
    # Avoid pure transparency dominating statistics by using only alpha>8
    mask = a.point(lambda p: 255 if p > 8 else 0, mode="1")
    stat = ImageStat.Stat(Image.merge("RGB", (r, g, b)), mask)
    # Fallback to a warm tan if mask empty
    if not stat.count or stat.count[0] == 0:
        return (191, 155, 101)  # soft leather tan
    mean = tuple(int(x) for x in stat.mean)
    return mean  # type: ignore[return-value]


def _composite_outline(outline_mask: Image.Image, color: Tuple[int, int, int]) -> Image.Image:
    w, h = outline_mask.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    # Paint solid color where outline mask is on
    solid = Image.new("RGBA", (w, h), (*color, 255))
    out.putalpha(outline_mask)
    out = Image.alpha_composite(Image.new("RGBA", (w, h), (0, 0, 0, 0)), out)
    out = Image.composite(solid, out, outline_mask)
    return out


def _resize_max(img: Image.Image, max_px: int = 512) -> Image.Image:
    w, h = img.size
    scale = min(1.0, max_px / max(w, h))
    if scale < 1.0:
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    return img


def _process_one(path: Path, stroke_px: int = 4) -> Image.Image:
    src = Image.open(path)
    rgba = _clean_background(src)
    color = _average_subject_color(rgba)
    mask = _silhouette(rgba.getchannel("A"))
    outline = _outline_from_mask(mask, stroke_px=stroke_px)
    out = _composite_outline(outline, color)
    return _resize_max(out, 512)


def _pick_order(files: List[Path]) -> List[Path]:
    """Return files ordered to map to OUT_FILES, using name hints if present."""
    def pick(key: str) -> Path | None:
        key = key.lower()
        for p in files:
            if key in p.name.lower():
                return p
        return None

    ordered: List[Path] = []
    for key in ("about", "portfolio", "contact", "tearsheet"):
        p = pick(key)
        if p:
            ordered.append(p)
    for p in files:
        if p not in ordered:
            ordered.append(p)
    return ordered


def main():
    ensure_dirs()
    files = load_candidates()
    if not files:
        print("No input images found. Drop your 4 images into icons/_INBOX and rerun.")
        return
    ordered = _pick_order(files)
    for i, out_name in enumerate(OUT_FILES):
        if i >= len(ordered):
            break
        out_img = _process_one(ordered[i], stroke_px=5)
        out_path = OUT / out_name
        out_img.save(out_path, "PNG")
        print(f"Saved {out_path} (outline) from {ordered[i].name}")


if __name__ == "__main__":
    # Lazy import placed here to avoid top-level dependency issue if PIL lacks ImageChops.
    from PIL import ImageChops  # type: ignore
    main()

