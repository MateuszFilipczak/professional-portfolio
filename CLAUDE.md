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

Everything lives in a single `index.html` — no external dependencies, no framework, no build tool. The PDF resume lives in `assets/`.

**Theming** — light/dark mode uses CSS custom properties on `:root`. Setting `data-theme="dark"` on `<html>` activates the dark palette; removing the attribute restores light. On load, the script restores from `localStorage`, falling back to `prefers-color-scheme`. The checked state uses `label:has(input:checked) .toggle-track` (not an adjacent-sibling selector) so it is robust to DOM reordering. Keyboard focus on the toggle is shown via `label:has(input:focus-visible) .toggle-track`.

**Header & nav** — the header is `position: sticky; top: 0` with two rows: the name + theme toggle on top, and a `<nav class="site-nav">` below. Nav links use `href="#section-id"` anchors. An `IntersectionObserver` adds an `active` class to the matching nav link as sections scroll into view (`rootMargin: "-20% 0px -70% 0px"`). Sections use `scroll-margin-top: 100px` to account for the sticky header height. `html { scroll-behavior: smooth }` handles the animation.

**Banners** — three `<a class="banner">` cards (Resume, GitHub, LinkedIn) sit in a `div.banners` flexbox row inside the `#home` section. Icons are inline SVGs (zero network requests). URLs are hardcoded directly in the anchor `href` attributes. The Resume banner uses the `download` attribute to trigger a PDF download from `assets/CV_Mateusz_Filipczak.pdf`.

**Sections** — six `<section id="...">` elements inside `<main>`: `home`, `about`, `experience`, `skills`, `projects`, `contact`. Each has class `section` for consistent padding. Adjacent sections are separated by a `border-top`.

**Responsive** — a single `@media (max-width: 520px)` rule stacks banners vertically, reduces header padding, and collapses the experience date to its own row.
