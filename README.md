# Professional Portfolio

A minimal, fast-loading personal portfolio page — no frameworks, no dependencies, no build step.

## Features

- **Resume & GitHub banners** — direct links to your resume and GitHub profile
- **Light / dark mode** — pill toggle in the header; respects OS preference, persists across reloads
- **Fully responsive** — banners stack gracefully on small screens
- **Zero dependencies** — pure HTML, CSS, and vanilla JS; works offline

## Getting started

Clone and open in a browser:

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

**Adding your URLs (kept private, never committed):**

```bash
cp config.example.js config.js
# Edit config.js and fill in your real URLs
```

`config.js` is listed in `.gitignore` so it will never be pushed to GitHub.

| What | Where |
|---|---|
| Resume / GitHub / LinkedIn URLs | `config.js` (copied from `config.example.js`) |
| Page title | `<title>` tag and `<h1>` in `index.html` |
| Color palette | CSS custom properties in `:root` and `[data-theme="dark"]` in `index.html` |

## License

MIT
