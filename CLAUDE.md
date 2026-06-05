# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the site

No build step. Open directly in a browser:

```
open index.html
```

## Architecture

Everything lives in a single `index.html` — no external dependencies, no framework, no build tool.

**Theming** — light/dark mode is driven by CSS custom properties on `:root`. A `data-theme="dark"` attribute on `<html>` activates the dark palette via `[data-theme="dark"] { ... }`. The inline `<script>` at the bottom of `<body>` toggles this attribute when the checkbox changes. Default is light (no attribute set).

**Banners** — two `<a class="banner">` cards sit in a `div.banners` flexbox row. Icons are inline SVGs (zero network requests). Both `href` values are currently placeholders (`#`).

**Responsive** — a single `@media (max-width: 520px)` rule switches the banner row to `flex-direction: column`.
