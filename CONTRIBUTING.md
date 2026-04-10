# Contributing

This repo values clean geometry, consistent style, and small reviewable changes.

## Adding a new animation

1. Check `docs/curriculum_mapping.md` to see where the scene should sit in the curriculum.
2. Choose the right module:
   - `src/byrne_euclid/definitions.py`
   - `src/byrne_euclid/postulates.py`
   - `src/byrne_euclid/propositions.py`
3. Copy an existing scene with similar structure.
4. Implement `construct()` using `ByrneScene` helpers rather than ad hoc Manim styling.
5. Add or update tests before changing behaviour.
6. Register the scene in `src/byrne_euclid/rendering.py`.
7. Add or update the scene entry in `curriculum/euclid_to_oak.yaml`.
8. Render locally at low quality, then re-check at medium or high quality.

## Style rules

The short version:

- Use only the Byrne palette from `src/byrne_euclid/style.py`
- Keep the cream background
- Use minimal text
- Prefer deliberate, readable motion over flourish
- Fade or soften auxiliary construction geometry once the result is clear

Read `docs/style_guide.md` before opening a scene PR.

## Local workflow

Install dependencies:

```bash path=null start=null
uv sync
```

Render one scene:

```bash path=null start=null
uv run python scripts/render_one.py PropI --quality l
```

Render the full catalogue:

```bash path=null start=null
uv run python scripts/render_all.py --quality l
bash scripts/gif_convert.sh
```

## Tests and lint

Run the full test suite:

```bash path=null start=null
uv run pytest tests/
```

Run lint:

```bash path=null start=null
uv run ruff check src/ scripts/ tests/
```

## Curriculum artefacts

If you change scene titles, scene coverage, curriculum links, or output file expectations, rebuild the generated curriculum artefacts:

```bash path=null start=null
uv run python scripts/build_manifest.py
```

If you are refreshing Oak cache data and have a local key under `OAK_OPEN_API_KEY` or `OAK_API_KEY`:

```bash path=null start=null
uv run --env-file .env python scripts/fetch_oak_curriculum.py
```

## Pull requests

Aim for one coherent change per PR. Good examples:

- one new scene plus its tests and curriculum mapping entry
- one tooling improvement plus the docs that explain it
- one design-system adjustment plus the scene updates it requires

## Reporting issues

When filing a bug, include:

- the scene name
- the command you ran
- whether the issue is visual, geometric, or tooling-related
- a still image or short description of the failure
