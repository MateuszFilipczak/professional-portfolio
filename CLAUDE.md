# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the site

No build step. Open `index.html` directly in a browser:

| Platform | Command |
|---|---|
| macOS | `open index.html` |
| Linux | `xdg-open index.html` |
| Windows | `start index.html` |

## Architecture

Everything lives in a single `index.html` — no external dependencies, no framework, no build tool. All CSS is in one `<style>` block in `<head>`; all JS is in one `<script>` block before `</body>`. The PDF resume and the `apple-touch-icon.png` live in `assets/`.

**Icons** — the browser-tab favicon is an inline SVG data URI in `<head>` (the purple `</>` code glyph). iOS Safari ignores SVG favicons for "Add to Home Screen" and would otherwise auto-generate an "M on dark" tile, so a separate `<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">` points at a 180×180 **opaque** PNG (no alpha — iOS rounds the corners itself) drawn from the same glyph on the dark `#1e1e1e` background. To regenerate it after changing the glyph or accent, re-run the rasterizer script (`/tmp/mkicon.py` in the original session) or redraw the PNG at 180×180.

**Accent color** — the brand accent is purple `#8c6edc` (RGB `140, 110, 220`), exposed as `--accent`. Many effects (glow shadows, canvas particles, the promo badge) use the raw `rgba(140, 110, 220, …)` triplet inline rather than the variable, so changing the accent means updating both the `--accent` declarations and these literal values.

**Theming** — light/dark mode uses CSS custom properties on `:root`, with a `[data-theme="dark"]` override block. Setting `data-theme="dark"` on `<html>` activates the dark palette; removing it restores light. **The site defaults to dark** — the inline `<head>` script applies `data-theme="dark"` **before first paint** (unless `localStorage.theme === 'light'`) to avoid a light-background flash on load; the script at the end of `<body>` re-applies it and wires the toggle. `html` also has `background: var(--bg)` so the root surface is themed from frame one. The toggle's checked state uses `label:has(input:checked) .toggle-track`; keyboard focus uses `label:has(input:focus-visible) .toggle-track`.

**Scroll position** — the head script sets `history.scrollRestoration = 'manual'` so reloads always start at the top (otherwise the browser restores the prior scroll position, which breaks the intro/hero reveal).

**Header & nav** — a single sticky bar (`position: sticky; top: 0`) containing the hamburger button, `<nav class="site-nav">`, and the theme toggle. There is no name/brand in the header. **Glassmorphism blur lives on `header::before`, not on `header` itself** — if `<header>` carried `backdrop-filter` it would become a "backdrop root" and the mobile nav dropdown (a descendant) could no longer blur the page behind it. Nav links are `href="#section-id"` anchors, but clicks call `e.preventDefault()` + `scrollIntoView({ behavior: 'smooth' })` so no hash is added to the URL. An `IntersectionObserver` (`rootMargin: "-20% 0px -70% 0px"`) adds `active` to the in-view section's link. Because the last section (Contact) is too short to reach that detection band when the page is scrolled fully down, an `atPageBottom()` check (in both the observer callback and a passive `scroll` listener) forces the **last** nav link active at the bottom — otherwise the highlight sticks on Projects. Sections use `scroll-margin-top: 72px` for the 56px-tall bar. On mobile the dropdown animates open/closed via `opacity` + `transform` + `visibility` (not `display`, so it can transition and so its blur renders).

**Hero (`#home`)** — contains a `<canvas class="home-canvas">` particle network. The particle code is a reusable `createParticleField(canvas, opts)` factory returning `{ start, stop }`, shared by both the hero canvas and the intro overlay. The hero field's rAF loop is gated by an `IntersectionObserver` on the canvas: it pauses when the hero scrolls off-screen and resumes when it returns (saves the main thread / battery). The tagline runs a **typing animation** that waits for the `intro:done` event (so it types out as the page is revealed, not while hidden under the intro). The hero name, tagline, and banners reveal via the intro's staggered `.intro-rise` animation (see **Intro reveal**).

**Intro reveal** — on a genuine first visit per session, the head script adds the `intro` class to `<html>` (gated by `sessionStorage.introSeen`; skipped for `prefers-reduced-motion` and no-JS). A full-viewport `#intro` overlay runs its own particle field. After ~1.3s (or on first click/scroll/key/touch), `finish()` swaps `intro` → `intro-done` on `<html>` (triggering the staggered `@keyframes introRise` on `.intro-rise` elements) and animates the overlay **converging into the hero canvas's bounding box** (translate + scale) while fading, so the field gathers into place rather than being replaced. The overlay keeps an `intro-closing` class so it stays displayed (its base styles aren't gated behind `html.intro`) through the exit animation, then is removed.

**Banners** — three `<a class="banner">` cards (LinkedIn, GitHub, CV) in a `div.banners` flex row. Icons are inline SVGs. The LinkedIn URL is hardcoded in the `href`. **GitHub and CV are both `banner--soon` placeholders** ("Coming soon"): non-interactive via `pointer-events: none`, `tabindex="-1"`, `aria-disabled="true"`, `href="#"`. To activate one, restore its real URL and remove the `banner--soon` class plus those attributes. Banners share the purple lift+glow hover with project cards.

**Experience** — a vertical **timeline**: `.experience-list` draws the line (`::before`), each `.exp-entry` draws its dot (`::before`). A `dotObserver` IntersectionObserver toggles `.dot-active` on the in-view entry so only its dot pulses. The promotion line (`.exp-promo`) renders a small purple circular `↑` badge via `::before`.

**Skills** — 2-column grid of `.skill-category` cards, each with a `--bar-width` (set inline) and a `--cat-rgb` triplet (currently unified to purple on the base rule). The animated fill bar fills via a `width` transition triggered when the card gets `is-visible` from the scroll-animation observer. Each card shows a `.skill-level` label; tags are tinted with `rgba(var(--cat-rgb), …)`.

**Skill popover** — hovering (desktop) / tapping (mobile) a `.skill-tag` shows a shared `.skill-popover` element (one node appended to `<body>`, repositioned per tag, flips above/below based on room) with a fade-and-scale animation. Per-skill copy lives in the editable `skillInfo` object keyed by exact tag text; tags without an entry show a fallback. A `lastShow` timestamp guard prevents the synthesized focus/click on touch from instantly dismissing the popover.

**Projects** — `.project-card` grid; cards are flex columns so the GitHub link (`.project-link`, pinned with `margin-top: auto`) sits at the bottom regardless of text length. The links are "Coming soon" placeholders (`href="#"`, `tabindex="-1"`, `aria-disabled="true"`); swap in the real repo URL and remove those attributes when ready. Hover gives a purple border, lift, glow, and accent title.

**Contact** — a single two-column `.contact-card`: heading + tagline on the left, a purple "Send a message" `mailto:` CTA button plus website/location icon rows on the right.

**Scroll animations** — an inline script in `<head>` adds `first-visit` to `<html>` before CSS loads (prevents FOUC). `.exp-entry` and `.skill-category` start hidden (`opacity: 0; translateY`) and get `is-visible` from an `animObserver` IntersectionObserver. (The hero name is no longer in this set — it's handled by the intro `.intro-rise` reveal.) Animations play on every load (no sessionStorage gate).

**Sections** — six `<section id="...">` inside `<main>`: `home`, `about`, `experience`, `skills`, `projects`, `contact`. Each has class `section`; adjacent sections separated by `border-top`. `#skills`, `#projects`, `#contact`, and `footer` use `content-visibility: auto` (with `contain-intrinsic-size`) so off-screen sections skip layout/paint — this cuts the reflow cost when the experience list expands/collapses on mobile.

**Mobile collapse** — inside the JS, a `matchMedia('(max-width: 520px)')`-driven IIFE makes long text expandable and is **responsive to resize**: `setup()` applies the collapse under 520px, `teardown()` removes the injected buttons and strips the inline styles above 520px (so resizing to desktop restores the full text), driven by the `matchMedia` `change` listener (`data-collapsible` guards prevent double setup). The About paragraph collapses to ~80px with a fade-out mask + "Read more"/"Read less"; each experience bullet list with >2 items collapses by animating the `<ul>`'s own `height` (single element = one layout recalc per frame), with the hidden `<li>`s fading via staggered `opacity`. Buttons are injected by JS only on small screens — no duplicate content.

**Responsive** — the `@media (max-width: 520px)` rule shows the hamburger and turns `.site-nav` into an animated, blurred dropdown, stacks banners, collapses the experience grid and date, and switches the skills grid and contact card to one column.

**Scrollbar** — a thin (4px) purple scrollbar via `::-webkit-scrollbar` (WebKit) and `scrollbar-color` (Firefox), with a transparent track.
