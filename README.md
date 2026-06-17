# Mateusz Filipczak — Personal Portfolio

A minimal, single-page personal portfolio — no frameworks, no dependencies, no build step.

## Features

- **Intro reveal** — a full-screen particle animation on first visit (once per session) that converges into the hero, then the page rises in with a staggered reveal
- **Animated hero** — a canvas particle network behind the intro, plus a typing animation on the tagline
- **Glassmorphism header** — frosted, blurred sticky nav with smooth scroll and active link highlighting
- **Timeline experience** — vertical timeline with a pulsing dot on the section currently in view
- **Animated skill bars** — category cards with fill bars that animate into view and proficiency labels
- **Interactive skill popovers** — hover or tap a skill to see how it was used
- **Quick-link banners** — LinkedIn from the home section, with GitHub and CV placeholders
- **Light / dark mode** — toggle in the header; defaults to dark and persists your choice across reloads
- **Installable icon** — a custom `</>` favicon, plus an `apple-touch-icon` so iOS "Add to Home Screen" shows a branded tile instead of a generated letter
- **Purple accent throughout** — unified accent color on nav, toggle, timeline, cards, and scrollbar
- **Mobile-friendly long text** — About and experience bullets collapse with smooth "Read more" toggles
- **Fully responsive** — hamburger nav and single-column layouts on small screens
- **Accessible & considerate** — respects `prefers-reduced-motion` (skips the intro and the scroll-reveal animations), keyboard-navigable
- **Zero dependencies** — pure HTML, CSS, and vanilla JS; works offline

## Getting started

```bash
git clone https://github.com/MateuszFilipczak/professional-portfolio.git
cd professional-portfolio
```

Then open `index.html` directly:

| Platform | Command |
|---|---|
| macOS | `open index.html` |
| Linux | `xdg-open index.html` |
| Windows | `start index.html` |

## Customization

| What | Where |
|---|---|
| Page title & meta description | `<title>`, `<meta>` tags in `index.html` |
| Section content | Each `<section id="...">` in `index.html` |
| Accent color | `--accent` in `:root`, plus the literal `rgba(140, 110, 220, …)` values used for glows and the canvas particles |
| Logo / favicon / home-screen icon | `assets/logo.svg` is the master `<mf/>` mark (with `logo.png` / `logo-square.png` rasters). The browser-tab favicon inlines the same glyph in `<head>`; `assets/apple-touch-icon.png` (180×180, opaque) is the iOS tile. Edit `logo.svg`, then mirror the change into the inline favicon and re-render the PNGs |
| Color palette | CSS custom properties in `:root` and `[data-theme="dark"]` |
| Skill descriptions | The `skillInfo` object in the `<script>` (keyed by skill name) — fills the hover/tap popovers |
| Banner links (GitHub / CV) | Both are "Coming soon" placeholders; restore the real `href` and remove `banner--soon` / `tabindex="-1"` / `aria-disabled="true"` to activate |
| Project GitHub links | Replace each project card's placeholder `href="#"` with the repo URL and remove `tabindex="-1"` / `aria-disabled="true"` |
| Resume / CV | The CV banner is a "Coming soon" placeholder — wire it to a PDF in `assets/` when ready |
| Intro frequency | In the head script: once per session by default (`sessionStorage.introSeen`) — change to every load or disable as needed |

## License

MIT
