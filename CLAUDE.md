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

Everything lives in a single `index.html` — no external dependencies, no framework, no build tool. All CSS is in one `<style>` block in `<head>`; all JS is in one `<script>` block before `</body>`. The PDF resume lives in `assets/`.

**Accent color** — the brand accent is purple `#8c6edc` (RGB `140, 110, 220`), exposed as `--accent`. Many effects (glow shadows, canvas particles, the promo badge) use the raw `rgba(140, 110, 220, …)` triplet inline rather than the variable, so changing the accent means updating both the `--accent` declarations and these literal values.

**Theming** — light/dark mode uses CSS custom properties on `:root`, with a `[data-theme="dark"]` override block. Setting `data-theme="dark"` on `<html>` activates the dark palette; removing it restores light. **The site defaults to dark** — on load the script applies dark unless `localStorage.theme === 'light'` (i.e. the user explicitly chose light). The toggle's checked state uses `label:has(input:checked) .toggle-track`; keyboard focus uses `label:has(input:focus-visible) .toggle-track`.

**Header & nav** — a single sticky bar (`position: sticky; top: 0`) containing the hamburger button, `<nav class="site-nav">`, and the theme toggle. There is no name/brand in the header. The header uses **glassmorphism** (`backdrop-filter: blur(14px)` over a semi-transparent `--header-bg`). Nav links are `href="#section-id"` anchors, but clicks call `e.preventDefault()` + `scrollIntoView({ behavior: 'smooth' })` so no hash is added to the URL. An `IntersectionObserver` (`rootMargin: "-20% 0px -70% 0px"`) adds `active` to the in-view section's link. Sections use `scroll-margin-top: 72px` for the 56px-tall bar.

**Hero (`#home`)** — contains a `<canvas class="home-canvas">` particle network (nodes drift and draw connecting lines within `MAX_DIST`). The rAF loop is gated by an `IntersectionObserver` on the canvas: it pauses when the hero scrolls off-screen and resumes when it returns (saves the main thread / battery). The tagline runs a **typing animation** (JS rewrites it to `.typed-text` + a blinking `.typed-cursor`). The name fades in via the `first-visit` entrance animation.

**Banners** — three `<a class="banner">` cards (LinkedIn, GitHub, CV) in a `div.banners` flex row. Icons are inline SVGs. LinkedIn/GitHub URLs are hardcoded in the `href`. The CV banner is a `banner--soon` placeholder ("Coming soon"): non-interactive via `pointer-events: none`, `tabindex="-1"`, `aria-disabled="true"`. Banners share the purple lift+glow hover with project cards.

**Experience** — a vertical **timeline**: `.experience-list` draws the line (`::before`), each `.exp-entry` draws its dot (`::before`). A `dotObserver` IntersectionObserver toggles `.dot-active` on the in-view entry so only its dot pulses. The promotion line (`.exp-promo`) renders a small purple circular `↑` badge via `::before`.

**Skills** — 2-column grid of `.skill-category` cards, each with a `--bar-width` (set inline) and a `--cat-rgb` triplet (currently unified to purple on the base rule). The animated fill bar fills via a `width` transition triggered when the card gets `is-visible` from the scroll-animation observer. Each card shows a `.skill-level` label; tags are tinted with `rgba(var(--cat-rgb), …)`.

**Projects** — `.project-card` grid; cards are flex columns so the GitHub link (`.project-link`, pinned with `margin-top: auto`) sits at the bottom regardless of text length. The links are "Coming soon" placeholders (`href="#"`, `tabindex="-1"`, `aria-disabled="true"`); swap in the real repo URL and remove those attributes when ready. Hover gives a purple border, lift, glow, and accent title.

**Contact** — a single two-column `.contact-card`: heading + tagline on the left, a purple "Send a message" `mailto:` CTA button plus website/location icon rows on the right.

**Scroll animations** — an inline script in `<head>` adds `first-visit` to `<html>` before CSS loads (prevents FOUC). `.exp-entry`, `.skill-category`, and `.home-name` start hidden (`opacity: 0; translateY`) and get `is-visible` from an `animObserver` IntersectionObserver. Animations play on every load (no sessionStorage gate).

**Sections** — six `<section id="...">` inside `<main>`: `home`, `about`, `experience`, `skills`, `projects`, `contact`. Each has class `section`; adjacent sections separated by `border-top`.

**Mobile collapse** — inside `@media (max-width: 520px)`, a JS IIFE (gated by `matchMedia`) makes long text expandable: the About paragraph collapses to ~80px with a fade-out mask and a "Read more"/"Read less" button; each experience bullet list with >2 items collapses by animating the `<ul>`'s own `height` (single element = one layout recalc per frame), with the hidden `<li>`s fading in via a staggered `opacity`. Buttons are injected by JS only on small screens — no duplicate content.

**Responsive** — the `@media (max-width: 520px)` rule shows the hamburger and turns `.site-nav` into a blurred dropdown, stacks banners, collapses the experience grid and date, and switches the skills grid and contact card to one column.

**Scrollbar** — a thin (4px) purple scrollbar via `::-webkit-scrollbar` (WebKit) and `scrollbar-color` (Firefox), with a transparent track.
