# Mateusz Filipczak — Personal Portfolio

A minimal, single-page personal portfolio — no frameworks, no dependencies, no build step.

## Features

- **Animated hero** — a canvas particle network behind the intro, plus a typing animation on the tagline
- **Glassmorphism header** — frosted, blurred sticky nav with smooth scroll and active link highlighting
- **Timeline experience** — vertical timeline with a pulsing dot on the section currently in view
- **Animated skill bars** — category cards with fill bars that animate into view and proficiency labels
- **GitHub & LinkedIn banners** — quick links from the home section, with a CV placeholder
- **Light / dark mode** — toggle in the header; defaults to dark and persists your choice across reloads
- **Purple accent throughout** — unified accent color on nav, toggle, timeline, cards, and scrollbar
- **Mobile-friendly long text** — About and experience bullets collapse with smooth "Read more" toggles
- **Fully responsive** — hamburger nav and single-column layouts on small screens
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
| Color palette | CSS custom properties in `:root` and `[data-theme="dark"]` |
| Project GitHub links | Replace each project card's placeholder `href="#"` with the repo URL and remove `tabindex="-1"` / `aria-disabled="true"` |
| Resume / CV | The CV banner is a "Coming soon" placeholder — wire it to a PDF in `assets/` when ready |

## License

MIT
