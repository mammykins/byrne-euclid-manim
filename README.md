# byrne-euclid-manim

Animated Euclidean geometry in the style of Oliver Byrne's 1847 *Euclid*.

## What is this?

This project renders short geometry animations with ManimCE using Byrne's four-colour visual language on a warm cream background. The first milestone is a clean end-to-end render of Proposition I, with a repo structure that can scale to the rest of Book I.

## Quickstart

### Prerequisites

- `uv`
- `ffmpeg`
- `cairo`
- `pango`

### Install and render

```bash path=null start=null
uv sync
uv run python scripts/render_one.py PropI
```

The rendered file is copied into `output/mp4/`.

## Status

The repository is under active construction. Phase 0 and Phase 1 lay down the shared style, geometry helpers, tests, and render tooling that the later animation tiers build on.

## Licence

- Code: MIT
- Rendered animations: planned for CC-BY 4.0

## Credits

- Oliver Byrne
- Nicholas Rougeux and c82.net
- Sergey Slyusarev / jemmybutton
- Manim Community Edition
- Oak National Academy