# Content Inbox

Drop files into these folders; I’ll wire them up.

- Images (originals): `assets/img/_INBOX/`
  - Any names are fine; I’ll optimize to WebP and place into `assets/img/`.
  - Ideal sizes: 1600–2400px wide for full‑screen hero, 1200–1600px for portfolio grid, 800–1200px for details.
  - Include a short alt text per image (what’s shown + material/finish).

- Landing hero image (optional now): place a single image at `assets/img/hero.jpg` (landscape, ~2400px wide). The landing will use it full‑bleed behind the circular buttons.

- PDF tear sheet: `assets/docs/tearsheet.pdf`
  - Export as a single PDF; keep file name exactly `tearsheet.pdf` so the “Download Tearsheet” link works.

Hero background image (landing page):
- Put the chosen image at `assets/img/hero.jpg` (JPEG) or `assets/img/hero.webp`.
- If you drop it in `_INBOX`, I’ll move/rename it for you.

Custom snail cursor (landing page):
- Save your snail image as `assets/icons/snail-cursor.png` (PNG) or `snail-cursor.webp`/`snail-cursor.svg`.
- I’ll use it automatically; otherwise a vector fallback snail is shown.

Landing symbols (replace the doodles):
- Drop four PNGs at `assets/img/symbols/` with these exact names:
  - `about.png`
  - `portfolio.png`
  - `contact.png`
  - `tearsheet.png`
- They will appear automatically on the landing page and fade under the hover word animation.

Alternatively, drop the raw images (even with checkerboard background) into `icons/_INBOX/` and run:
`python3 tools/extract_symbols.py`
This will produce cleaned, transparent icons in `icons/about.png`, `icons/portfolio.png`, `icons/contact.png`, `icons/tearsheet.png` and the page will pick them up automatically via `<picture>` fallbacks.

- Bio & contact: send in plain text or paste into a message.

Once files are in place, I’ll optimize and update the pages.
