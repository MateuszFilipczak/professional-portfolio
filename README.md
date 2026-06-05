# Mateusz Filipczak — Personal Portfolio

A minimal, single-page personal portfolio — no frameworks, no dependencies, no build step.

## Features

- **Sticky navigation** — Home, About, Experience, Skills, Projects, Contact with smooth scroll and active link highlighting
- **Resume download** — links directly to `assets/CV_Mateusz_Filipczak.pdf`
- **GitHub & LinkedIn banners** — quick links from the home section
- **Light / dark mode** — toggle in the header; respects OS preference, persists across reloads
- **Fully responsive** — stacks gracefully on small screens
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
| Resume PDF | Replace `assets/CV_Mateusz_Filipczak.pdf` |
| Color palette | CSS custom properties in `:root` and `[data-theme="dark"]` |

## License

MIT
