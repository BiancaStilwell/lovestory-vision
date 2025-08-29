# AGENTS.md — Static Portfolio Website for **Bianca** (Codex CLI)

> Purpose: empower a completely non‑technical owner (Bianca) to describe what she wants in plain English while the agent does the heavy lifting. Favor the simplest path (plain HTML/CSS + light JS, GitHub Pages). Only escalate tooling when Bianca explicitly asks for features that require it. Keep explanations short and friendly.

**Core principles**

* **Simplicity above all**: prefer the least complex solution that meets the requirement.
* **Agent does the work**: assume Bianca does not know Git, GitHub, or servers. The agent runs all commands (init, commits, pushes, starting/stopping local preview) and reports results in plain English.
* **Minimal questions**: implement what she asks; if underspecified, either choose the simplest sensible default or ask one brief clarifier (especially for style).
* **Bianca overrides**: her explicit instructions trump this file; only push back if something is technically unsound—explain briefly and propose a simpler alternative.

---

## Project Goal

Create and publish a simple, professional **portfolio / work** website with **no build step** by default. Priorities:

* **Simplicity first**: plain HTML + CSS, tiny vanilla JS only as needed.
* **Fast publish**: GitHub Pages, deployed from the repo **root** of `main`.
* **Creative control**: Bianca speaks casually; you interpret and implement, showing previews and small choices.
* **Accessibility & mobile**: readable on phones, good contrast, keyboard friendly.
* **Agent handles Git**: Bianca doesn’t know Git. You run all commands with GitHub CLI where possible.

---

## Instruction Precedence (Bianca First)

* Bianca’s explicit instructions always override this file.
* If a request would be fragile, needlessly complex, or technically unsound, do this:

  1. Explain—briefly and in beginner‑friendly language—why it’s not ideal.
  2. Propose the **simplest** alternative that achieves her goal.
  3. Ask if she wants to proceed anyway; if yes, implement carefully, minimize complexity, and note trade‑offs in the commit message.
* **Never** proceed without explicit confirmation for actions that expose secrets, incur charges, break GitHub Pages limits, or violate platform policies.

---

## Locked Preferences (Do Not Change)

Use this section to record Bianca‑approved choices that must stay exactly as‑is unless she explicitly asks to change them. Treat these as immutable during refactors or redesigns.

- How to use: when Bianca says “add this to the locked list,” append a new bullet with the date and a short note. Only Bianca can approve removals/edits here.

Current locked items:
- 2025‑08‑29 — Font: “Amarante” applied to landing page bubbles, heart badge, and all `.cta` buttons.
- 2025‑08‑29 — Landing layout: full‑bleed splash with circular floating buttons (About, Portfolio, Contact, Download Tearsheet) and a central dark heart CTA.

---

## How to Talk to Bianca

* Let Bianca describe what she wants in plain language. Implement directly.
* If a request lacks specificity, either (a) choose the simplest sensible default and proceed, or (b) ask one brief clarifying question **only when the result would likely be wrong without it**.
* For **stylistic** ambiguity (vibe, spacing, color feel, density), ask a short clarifier like: “When you say ‘cozy,’ should it lean warmer (browns/terracotta) or cooler (greens/blues)?” Otherwise, avoid offering menus of choices.
* Translate casual phrases into concrete actions (e.g., “make it pop” → larger heading, contrast boost, refined spacing) and show the result.

---

## Golden Path (Decision Tree)

1. **Start simple** (default): plain HTML/CSS with tiny vanilla JS only if needed. Files: `index.html`, `styles.css`, `/assets/`, optional `/pages/`.
2. **Add pages only when asked**: create `/pages/*.html` as needed (about, projects, contact) and wire simple nav.
3. **Contact**: default to `mailto:`. If Bianca wants a form that “submits,” explain there’s no backend on Pages and add a minimal static form service **only if she confirms**.
4. **Escalate complexity only when requirements demand it**:

   * **Content templating/blog** → use GitHub Pages with Jekyll (builds on GitHub; Bianca needn’t run anything locally).
   * **App‑like features** (client‑side search, filters, API calls) → keep static where possible; if impossible, introduce a minimal Node/Vite setup and hide complexity (agent runs scripts; Bianca’s workflow unchanged).
5. **Copy & assets discipline**: never ship unknown copy. Keep placeholders obvious, track them in `COPY_TODO.md`, and use the `_INBOX` flow for images before building galleries.
6. Keep diffs small, commits clear, and always prefer the least complex solution that satisfies usability.

---

## Repository Layout (stick to this)

```
/ (repo root)
  index.html
  styles.css
  /assets/
    /img/            (optimized images used on the site)
      /_INBOX/       (Bianca drops new images here; any names are fine)
    /icons/          (SVGs or PNGs)
    /docs/           (optional PDFs)
  /pages/            (optional: about.html, projects.html, contact.html)
  CONTENT_INBOX.md   (plain-English “where to drop files” guide for Bianca)
  COPY_TODO.md       (list of all placeholder copy to replace; agent maintains)
  CNAME              (optional, auto‑managed if custom domain is set in Pages)
```

**Conventions**

* Semantic HTML: `<header> <nav> <main> <section> <footer>`.
* One CSS file (`styles.css`).
* JS only if needed; keep it tiny. No frameworks unless Bianca pushes for them.

---

## What the Agent Does Automatically

* **Scaffold** structure + tasteful, responsive base theme.
* Insert placeholders for: name, tagline, skills/services, projects, contact—**without special styling** (no outlines, no badges). Use normal-looking copy so the design isn’t distorted.
* Generate `<title>`, meta description, basic Open Graph tags.
* Add a favicon (placeholder acceptable) and a skip‑link for accessibility.
* **Optimize images** (downscale large originals; export `.webp` copies); keep originals in `/assets/img/`.
* **Create and maintain helper files**:

  * `CONTENT_INBOX.md` with clear “drop files here” instructions and accepted formats.
  * `COPY_TODO.md` enumerating every placeholder string (ID/key, location, short note). This is the **single source of truth** for temporary copy.
  * Place a short `README.txt` inside `/assets/img/_INBOX/` reminding “drop images here”.
* Mark placeholders **in code only** with HTML comments like `<!-- TODO:COPY hero.tagline -->` and list them in `COPY_TODO.md`. Do **not** add visible CSS effects for placeholders.
* Write plain‑English commit messages and keep diffs small; mention any placeholder keys touched.

---

## Git & GitHub (Agent‑Only Mechanics)

Bianca does **not** use Git directly; you do.

**Initialize & first publish**

* Create repo if needed; set default branch `main`.
* Commit scaffold with message: `chore: scaffold static site (HTML/CSS + light JS)`.
* Push `main` and set remote via GitHub CLI.

**Regular workflow**

* Commit in small steps with clear, friendly messages (e.g., `feat: add projects grid + lightbox`).
* Include a brief **PLACEHOLDER summary** when applicable, e.g., `PLACEHOLDER: hero.tagline, about.bio`.
* Prefer working directly on `main`. If a branch is needed, name it clearly and merge without noise.
* If something breaks, revert the last commit and explain in one sentence.

---

## Local Preview (agent‑run, live reload)

* The agent spins up a **local dev server with live reload** so Bianca can see changes instantly in her browser.
* Bianca does **not** manage ports or commands. The agent selects an available localhost port (prefer `5173`; auto‑fallback if busy) and **opens the browser automatically**.
* Acceptable implementations: a tiny static server with live reload (Python `livereload`, `http.server` + lightweight reload script, or equivalent). Avoid heavy tooling.
* If the server stops (sleep/restart), the agent restarts it and reopens the page. No action needed from Bianca.

---

## Publishing (GitHub Pages — simplest path)

**Primary path:** Deploy from **`main` / root**.

1. Push `main` to GitHub.
2. Enable Pages: **Settings → Pages → Build and deployment → Source: “Deploy from a branch” → Branch: `main` → Folder: `/ (root)` → Save**.
3. Share the URL: `https://<user>.github.io/<repo>/`.

**Custom domain (optional):**

* Add domain in **Settings → Pages → Custom domain** (creates/updates `CNAME`).
* Ask for DNS `CNAME` from `www` → `<user>.github.io`.
* Ensure HTTPS is checked in Pages settings.

> If GitHub CLI can’t toggle Pages directly, guide Bianca through the UI with one short message and a direct link to the repo’s Pages settings.

---

## JavaScript Policy

* Vanilla JS is welcome for small interactions (mobile nav, lightbox, tabs). Use `<script type="module">`.
* A **dev‑only** lightweight live‑reload server is allowed to improve preview speed. Keep it invisible to Bianca.
* Avoid build steps and frameworks unless a requirement truly needs them; if so, add the minimal setup and keep Bianca’s commands unchanged.

---

## Collaboration Style

* Default: implement what she asks. If something is ambiguous **and** would risk missing her intent, ask one short question.
* Don’t present long lists of options. When a stylistic term is vague, propose the sensible interpretation, show it, and offer a tiny tweak: “I went with a warm, cozy palette—want it lighter or darker?”
* Maintain `COPY_TODO.md` and highlight in‑page placeholders so Bianca always knows what text remains temporary.
* For assets (images/docs), direct Bianca to the `_INBOX` folder and `CONTENT_INBOX.md` for exactly where to drop files.

---

## Content & Sections (portfolio‑friendly defaults)

* **Hero**: Name, one‑liner, primary CTA. If Bianca hasn’t supplied copy, use neutral, normal-looking placeholder phrases (e.g., “Short one‑line description goes here”) and track exact keys in `COPY_TODO.md` (no special visual styling on the page).
* **Work / Projects**: grid of cards (title, role, short blurb, link). If assets are missing, add intake instructions to `CONTENT_INBOX.md` and wait for files in `/assets/img/_INBOX/`.
* **About**: short bio and photo; use neutral placeholder text/image only until Bianca provides final content; track items in `COPY_TODO.md`.
* **Contact**: mailto button, phone (if desired), city; placeholders until confirmed—tracked in `COPY_TODO.md`.
* **Footer**: copyright and minimal links; default to a neutral © name/year and track in `COPY_TODO.md`.

---

## Tiny JS Snippets (only if needed)

* **Mobile nav toggle** with ARIA attributes and focus trapping.
* **Lightbox** for gallery images (no deps; graceful fallback to direct links).
* **Tabs/accordion** for FAQs if she asks.

---

## Performance & Accessibility Checklist (agent runs it)

* Images appropriately sized; `.webp` where safe.
* `<meta name="viewport" content="width=device-width, initial-scale=1">`.
* Helpful `<title>` and meta description.
* Color contrast ≳ 4.5:1 for body text.
* Meaningful `alt` text; keyboard‑navigable controls; visible focus states.
* No console errors; internal links work.
* **No placeholder copy** ships unintentionally: before publishing, confirm `COPY_TODO.md` is empty or Bianca explicitly approves any remaining temporary text.

---

## Common Requests → What to Do

* “Add project thumbnails” → create responsive grid; lazy‑load images; open details page or lightbox. If images not provided, instruct Bianca to drop them in `/assets/img/_INBOX/` and list expected counts/sizes in `CONTENT_INBOX.md`.
* “Add a PDF price sheet” → place PDF in `/assets/docs/` and link clearly.
* “Embed a map” → responsive container with an accessible title.
* “Add testimonials” → simple cards with quote/attribution; mark copy as placeholders until Bianca provides final quotes.

---

## Guardrails

* Don’t introduce frameworks, build tools, paid services, or analytics **unless Bianca asks**.
* Keep everything editable in one or two files.
* No secrets or trackers by default.
* Keep changes incremental and explain briefly in plain English.
* **Override rule**: If Bianca asks for something that conflicts with these guardrails and it’s still technically workable, follow her lead after explaining trade‑offs.

---

## Quick Start for Bianca

In the project folder, Bianca can open Terminal and type:

> `codex`

Then say something like:

> “Make me a one‑page portfolio called **Bianca Rivera** with a warm, cozy vibe. I want a hero, a projects section, an about blurb, and a big email button.”

The agent should scaffold, preview locally, then guide publishing to GitHub Pages.
