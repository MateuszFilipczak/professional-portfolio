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

Everything lives in a single `index.html` — no external dependencies, no framework, no build tool.

**Theming** — light/dark mode uses CSS custom properties on `:root`. Setting `data-theme="dark"` on `<html>` activates the dark palette; removing the attribute restores light. On load, the script restores from `localStorage`, falling back to `prefers-color-scheme`. The checked state uses `label:has(input:checked) .toggle-track` (not an adjacent-sibling selector) so it is robust to DOM reordering. Keyboard focus on the toggle is shown via `label:has(input:focus-visible) .toggle-track`.

**Banners** — three `<a class="banner">` cards (Resume, GitHub, LinkedIn) sit in a `div.banners` flexbox row. Icons are inline SVGs (zero network requests). All `href` values are currently placeholders (`#`); a JS handler calls `e.preventDefault()` so clicks do not scroll to the top.

**Responsive** — a single `@media (max-width: 520px)` rule switches the banner row to `flex-direction: column`.
