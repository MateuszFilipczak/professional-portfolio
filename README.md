# Professional Portfolio

A minimal, fast-loading personal portfolio page — no frameworks, no dependencies, no build step.

## Features

- **Resume & GitHub banners** — direct links to your resume and GitHub profile
- **Light / dark mode** — pill toggle in the header; defaults to light
- **Fully responsive** — banners stack gracefully on small screens
- **Zero dependencies** — pure HTML, CSS, and vanilla JS; works offline

## Getting started

Clone and open in a browser:

```bash
git clone https://github.com/MateuszFilipczak/professional-portfolio.git
cd professional-portfolio
open index.html
```

## Customization

| What | Where in `index.html` |
|---|---|
| Resume link | `href="#"` on `<a id="resume-banner">` |
| GitHub link | `href="#"` on `<a id="github-banner">` |
| Page title | `<title>` tag and `<h1>` in `<header>` |
| Color palette | CSS custom properties in `:root` and `[data-theme="dark"]` |

## License

MIT
