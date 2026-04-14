# Plan: byrne-euclid-manim

Animated geometry for teachers — Euclid's Elements in the visual style of Oliver Byrne's 1847 edition, aligned to the English national curriculum.

> Companion document: [research.md](./research.md)

---

## 1. What we're building

A Python project that produces short (30–90 second) animated GIFs and MP4s of Euclidean geometry constructions, styled with Byrne's four-colour palette on a warm cream background. Each animation maps to a specific point in the English national curriculum for mathematics (KS2–KS3). The animations are designed as drop-in visual aids for teachers — not lectures, not explainers, just clean geometry in motion.

The project is open source from day one. A teacher in Salford or a developer in São Paulo should be able to clone the repo, install dependencies with a single command, and render every animation locally.

### Outputs

| Output | Format | Audience |
|--------|--------|----------|
| Animated constructions | GIF (square, 540px) + MP4 (1080p 16:9) | Teachers, students |
| YouTube playlist | MP4 uploads, curriculum-tagged | Teachers discovering via search |
| Blog post | Markdown / Substack | Developers, educators, AI-in-education community |
| Open-source repo | GitHub | Anyone who wants to extend or adapt |
| Curriculum manifest | JSON | Programmatic consumers (e.g. Oak-adjacent tools) |

---

## 2. Repository structure

```
byrne-euclid-manim/
├── .github/
│   └── workflows/
│       └── render.yml              # CI: render all scenes, upload artefacts
├── src/
│   └── byrne_euclid/
│       ├── __init__.py
│       ├── style.py                # Byrne palette, ByrneScene base class, helpers
│       ├── definitions.py          # Scenes: Def I–XXXV
│       ├── postulates.py           # Scenes: Post I–III
│       ├── propositions.py         # Scenes: Prop I, IX, X, XI, XII, XIII, XV, XXXII, XLVII
│       └── utils.py                # Geometry helpers (intersection points, compass arcs, etc.)
├── scripts/
│   ├── render_all.py               # Render every scene to output/
│   ├── render_one.py               # Render a single named scene (for iteration)
│   ├── fetch_oak_curriculum.py     # Pull geometry threads/lessons from Oak API
│   └── build_manifest.py           # Generate curriculum_manifest.json
├── curriculum/
│   ├── oak_geometry_threads.json   # Cached Oak API response (geometry threads)
│   ├── oak_geometry_lessons.json   # Cached Oak API response (geometry lessons)
│   └── curriculum_manifest.json    # Maps animation → NC reference → Oak lesson slug
├── output/
│   ├── gif/                        # 540×540 GIFs (square, looping)
│   ├── mp4/                        # 1920×1080 MP4s (16:9)
│   └── png/                        # Final-frame stills for thumbnails / blog embeds
├── docs/
│   ├── style_guide.md              # Visual design decisions, palette reference
│   └── curriculum_mapping.md       # Euclid ↔ NC ↔ Oak mapping table
├── references/
│   ├── README.md                   # Attribution notices, OGL text, source links
│   ├── NC_KS1_KS2_Mathematics.pdf  # DfE, Crown copyright 2013, OGL v3.0
│   ├── NC_KS3_Mathematics.pdf      # DfE, Crown copyright 2013, OGL v3.0
│   └── NC_KS4_Mathematics.pdf      # DfE, Crown copyright 2014, OGL v3.0
├── tests/
│   └── test_style.py               # Smoke tests: palette values, ByrneScene renders
├── manim.cfg                       # Project-level Manim defaults
├── pyproject.toml                  # Project metadata, dependencies, scripts
├── README.md                       # Project overview, quickstart, licence
├── CONTRIBUTING.md                 # How to add a new animation
├── LICENSE                         # MIT
└── .gitignore
```

### Key design decisions

**`src/` layout with package**: The scenes live in a proper Python package (`byrne_euclid`) so they can import shared code (`style.py`, `utils.py`) cleanly. Manim is invoked via scripts that point at the package, not by running `manim` directly against loose files.

**`curriculum/` as cached data**: Oak API responses are cached as JSON files checked into the repo. This means the project renders without an API key — the key is only needed to refresh the curriculum data. It also means the mapping is version-controlled and auditable.

**`output/` is gitignored**: Rendered artefacts are large and binary. They're produced locally or in CI, never committed. GitHub Releases or a separate hosting solution (e.g. a GitHub Pages site) serves the final outputs.

**No `requirements.txt`**: Dependencies are declared in `pyproject.toml` and managed by `uv`. No pip, no venv, no conda.

---

## 3. Tooling and dependencies

### 3.1 Python environment

```toml
# pyproject.toml
[project]
name = "byrne-euclid-manim"
version = "0.1.0"
description = "Animated Euclidean geometry in the style of Byrne's Euclid, aligned to the English national curriculum"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
authors = [
    {name = "Mat Gregory"}
]
keywords = ["manim", "euclid", "byrne", "geometry", "education", "animation"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "Topic :: Multimedia :: Video",
    "Topic :: Scientific/Engineering :: Mathematics",
    "License :: OSI Approved :: MIT License",
]

dependencies = [
    "manim>=0.18.0,<0.22",
    "httpx>=0.27",            # For Oak API calls (async-ready, lighter than requests)
    "pydantic>=2.0",          # For curriculum manifest schema
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.4",
]

# No [project.scripts] — render scripts are invoked directly via
# `uv run python scripts/render_one.py` (see README quickstart).

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 3.2 System dependencies

Manim requires system-level libraries. These are documented in the README and handled in CI:

```bash
# Ubuntu / Debian
sudo apt-get update && sudo apt-get install -y \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev
    # texlive-latex-extra texlive-fonts-extra  # Optional — only if using Tex()/MathTex()

# macOS
brew install ffmpeg cairo pango
# brew install --cask mactex-no-gui  # Optional — only if using Tex()/MathTex()
```

### 3.3 Project initialisation (one-time)

```bash
# Create project
uv init byrne-euclid-manim
cd byrne-euclid-manim

# Add dependencies
uv add manim httpx pydantic
uv add --dev pytest ruff

# Verify manim works
uv run manim --version
```

### 3.4 Manim configuration

```ini
# manim.cfg
[CLI]
quality = medium_quality
format = mp4
preview = false
background_color = #F5F0E1
media_dir = ./media
```

This provides sensible defaults. Individual render scripts override for specific output formats.

---

## 4. Implementation plan

### Phase 0: Skeleton (Day 1)

**Goal**: A repo that renders a single scene end-to-end, with CI.

- [ ] Initialise repo with `uv init`, push to GitHub
- [ ] Create `src/byrne_euclid/style.py` with the Byrne palette constants and `ByrneScene` base class
- [ ] Create one scene: `PropositionI` (equilateral triangle construction) in `propositions.py`
- [ ] Write `scripts/render_one.py` — takes a scene class name, renders GIF + MP4 + PNG
- [ ] Write `manim.cfg`
- [ ] Write `README.md` with quickstart instructions
- [ ] Add `.gitignore` (ignore `media/`, `output/`, `__pycache__/`, `.venv/`)
- [ ] Set up GitHub Actions workflow to render `PropositionI` on push and upload as artefact
- [ ] Add MIT `LICENSE`

**Deliverable**: Running `uv run python scripts/render_one.py PropositionI` produces a GIF and MP4.

### Phase 1: Design system (Days 2–3)

**Goal**: Lock down the visual style so all subsequent scenes are consistent.

- [ ] Refine `ByrneScene` base class:
  - Background colour
  - Helper methods: `byrne_line()`, `byrne_dashed_line()`, `byrne_circle()`, `byrne_arc()`, `byrne_angle()`, `byrne_dot()`, `byrne_polygon()`, `byrne_title()`
  - Standard animation methods: `construct_line()`, `sweep_circle()`, `mark_angle()`
  - Configurable output dimensions (square vs 16:9) via class attribute
- [ ] Build `utils.py`:
  - `circle_intersection(c1_centre, c1_radius, c2_centre, c2_radius)` → two intersection points
  - `line_intersection(p1, p2, p3, p4)` → intersection point
  - `perpendicular_foot(point, line_start, line_end)` → foot of perpendicular
  - `midpoint(a, b)` → midpoint
  - `angle_between(line1, line2)` → angle in radians
- [ ] Write `docs/style_guide.md` documenting the palette, stroke widths, fill opacities, animation timings, font choices
- [ ] Render a "palette card" scene that displays all four colours with labels — useful for the blog post and as a visual test
- [ ] Smoke test: `tests/test_style.py` — assert palette hex values, assert `ByrneScene` sets background correctly

**Deliverable**: A locked-down design system that any contributor can use to create consistent scenes.

### Phase 2: Tier 1 animations — Definitions & Postulates (Days 4–7)

**Goal**: 7 definition animations + 3 postulate animations covering foundational geometry vocabulary.

Each definition animation follows the same template:
1. Title card (e.g. "Definition X.") — brief, top-left
2. Construction / demonstration of the concept
3. Hold on final state for 2 seconds
4. Total duration: 15–40 seconds

| # | Scene class | Content | Duration |
|---|------------|---------|----------|
| 1 | `DefPointLineStraightLine` | Point appears, line drawn, straight vs curved contrast | ~20s |
| 2 | `DefAngleTypes` | Right angle drawn, arm rotates to show obtuse then acute | ~30s |
| 3 | `DefCircle` | Centre point, radius line, compass sweep, diameter drawn | ~25s |
| 4 | `DefTrianglesBySide` | Three triangles: equilateral (3 equal), isosceles (2 equal), scalene (0 equal) | ~30s |
| 5 | `DefTrianglesByAngle` | Three triangles: right-angled, obtuse-angled, acute-angled, angles marked | ~30s |
| 6 | `DefQuadrilaterals` | Square → rectangle → rhombus → parallelogram, properties highlighted | ~40s |
| 7 | `DefParallelLines` | Two lines extended, showing they never meet, equal spacing | ~20s |
| 8 | `PostulateI` | Two points appear → straight line drawn between them | ~10s |
| 9 | `PostulateII` | A finite line → extended indefinitely in both directions | ~10s |
| 10 | `PostulateIII` | Centre point → radius line → circle swept out | ~15s |

Implementation pattern for each:
```python
# definitions.py
class DefAngleTypes(ByrneScene):
    """Definition X–XII: Right, obtuse, and acute angles."""
    
    def construct(self):
        title = self.byrne_title("Definitions X–XII.")
        self.play(Write(title))
        # ... construction code ...
```

- [ ] Implement all 7 definition scenes
- [ ] Implement all 3 postulate scenes
- [ ] Render each as MP4 (16:9) + PNG (final frame)
- [ ] Review all 10 for visual consistency — adjust timings, sizes, positions
- [ ] Update `curriculum/euclid_to_oak.yaml` with entries for all 10 scenes

### Phase 3: Tier 2 animations — Constructions (Days 8–13)

**Goal**: 7 animations covering the KS3 statutory ruler-and-compass constructions plus their dependencies.

These are longer and more complex — they follow Euclid's actual construction sequence step-by-step. Each should feel like watching someone carefully draw with compass and straightedge.

| # | Scene class | Euclid | Duration |
|---|------------|--------|----------|
| 11 | `PropI` | Construct equilateral triangle on a line | ~45s |
| 12 | `PropII` | From a given point, draw a line equal to a given line | ~50s |
| 13 | `PropIII` | From the greater of two lines, cut off a part equal to the less | ~35s |
| 14 | `PropIX` | Bisect a given rectilinear angle | ~40s |
| 15 | `PropX` | Bisect a given finite straight line | ~40s |
| 16 | `PropXI` | Perpendicular from a point on a line | ~40s |
| 17 | `PropXII` | Perpendicular from an external point to a line | ~45s |

Implementation notes:
- Construction circles should be drawn with `Create` (compass sweep feel), not `FadeIn`
- Auxiliary/construction elements use dashed lines or reduced opacity
- After the construction is complete, fade the auxiliary elements to emphasise the result
- The "QED moment" — a brief hold with only the final construction visible
- Props II and III are prerequisite sub-procedures used in later constructions — they must be implemented first

- [ ] Implement all 7 scenes (Props I–III first, then IX–XII)
- [ ] Render and review
- [ ] Update `curriculum/euclid_to_oak.yaml` with entries for all 7 scenes

### Phase 4: Tier 3 animations — Angle theorems (Days 14–17)

**Goal**: 3 animations demonstrating key angle theorems.

| # | Scene class | Euclid | Duration |
|---|------------|--------|----------|
| 18 | `PropXIII` | Angles on a straight line sum to 180° | ~35s |
| 19 | `PropXV` | Vertically opposite angles are equal | ~35s |
| 20 | `PropXXXII` | Angle sum of a triangle = 180° | ~45s |

PropXLVII (Pythagorean theorem) is **deferred to v0.2** — it is the most complex animation by an order of magnitude and deserves its own focused iteration. It will be the hero feature of the v0.2 release and a sequel blog post.

- [ ] Implement all 3 scenes
- [ ] Render and review
- [ ] Update `curriculum/euclid_to_oak.yaml` with entries for all 3 scenes

### Phase 5: Curriculum integration (Days 17–19)

**Goal**: Connect the animations to the Oak National Academy curriculum via API.

- [ ] Write `scripts/fetch_oak_curriculum.py`:
  - Fetch `GET /threads` and filter for geometry-related threads
  - Fetch `GET /threads/{slug}/units` for each geometry thread
  - Fetch `GET /key-stages/ks2/subject/maths/lessons` and `ks3` — filter for geometry units
  - For a subset of key lessons: fetch `GET /lessons/{slug}/summary` for misconceptions and keywords
  - Cache all responses to `curriculum/` as JSON
  - Script is idempotent — re-running overwrites with fresh data
  - API key read from `OAK_API_KEY` environment variable (never committed)

- [ ] Write `scripts/build_manifest.py`:
  - Read the cached curriculum JSON
  - Read a hand-maintained mapping file (`curriculum/euclid_to_oak.yaml`) that links each Manim scene class to one or more Oak lesson slugs and NC references
  - Output `curriculum/curriculum_manifest.json` with the full cross-reference

- [ ] Write `curriculum/euclid_to_oak.yaml` (hand-maintained):
  ```yaml
  # Maps Manim scene classes to curriculum references
  - scene: DefAngleTypes
    euclid: [def_x, def_xi, def_xii]
    nc_references:
      - key_stage: KS2
        year: 4
        statement: "Identify acute and obtuse angles"
      - key_stage: KS3
        statement: "Draw and measure angles in geometric figures"
    oak_lessons: []  # populated after API exploration
    oak_threads: []
    misconceptions: []  # populated from lesson summaries
  ```

- [ ] Write `docs/curriculum_mapping.md` — a human-readable table rendering the manifest

**Deliverable**: A JSON manifest that any tool can consume to understand where each animation sits in the curriculum.

### Phase 6: Polish and publish (Days 20–24)

- [ ] Final render of all animations at high quality
- [ ] Generate high-quality GIFs using ffmpeg palettegen pipeline:
  ```bash
  ffmpeg -i input.mp4 \
    -vf "fps=15,scale=540:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
    output.gif
  ```
- [ ] Write `CONTRIBUTING.md`:
  - How to add a new animation (copy template, implement `construct()`, add to manifest)
  - Style guide reference
  - How to render locally
  - How to run tests
- [ ] Complete `README.md`:
  - Project description and motivation
  - Gallery of example outputs (link to GIFs hosted on GitHub Pages or similar)
  - Quickstart: `uv sync && uv run python scripts/render_one.py PropI`
  - Curriculum alignment explanation
  - Credits: Byrne, Rougeux (c82.net), jemmybutton, ManimCE, Oak National Academy
  - Licence: MIT (code), CC-BY 4.0 (animations)
- [ ] Upload MP4s to YouTube, organised into playlists per tier
- [ ] Write the blog post
- [ ] Tag a `v0.1.0` release on GitHub with rendered outputs attached

---

## 5. CI / CD

### GitHub Actions workflow

```yaml
# .github/workflows/render.yml
name: Render animations

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'manim.cfg'
  workflow_dispatch:  # manual trigger

jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install system dependencies
        # No texlive — we use Text() not Tex(), so LaTeX is not needed.
        run: |
          sudo apt-get update
          sudo apt-get install -y ffmpeg libcairo2-dev libpango1.0-dev

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install Python dependencies
        run: uv sync

      - name: Run tests
        run: uv run pytest tests/

      - name: Lint
        run: uv run ruff check src/ scripts/

      - name: Render all scenes
        run: uv run python scripts/render_all.py

      - name: Convert to GIF
        run: bash scripts/gif_convert.sh

      - name: Upload rendered outputs
        uses: actions/upload-artifact@v4
        with:
          name: rendered-animations
          path: output/
          retention-days: 30
```

### Why CI rendering matters

- **Reproducibility proof**: If it renders in CI, it renders for anyone. No "works on my machine."
- **Regression detection**: If a Manim upgrade breaks a scene, CI catches it.
- **Release artefacts**: Tagged releases can automatically attach rendered outputs.
- **Contributor confidence**: New contributors can submit a PR and see the output without installing LaTeX locally.

Note: Full rendering of all 16 scenes will be slow (5–15 minutes). For PRs, consider rendering only changed scenes by parsing the git diff.

---

## 6. Rendering pipeline

### render_one.py

```python
"""Render a single scene by class name.

Uses a registry dict to map scene names to their source modules.
This is explicit and avoids fragile text-search discovery.
When adding a new scene, add it to SCENE_REGISTRY below.
"""
import argparse
import glob
import shutil
import subprocess
import sys
from pathlib import Path

# --- Scene Registry ---
# Maps scene class name -> source file path (relative to project root).
# Update this when adding new scenes. Keep alphabetically sorted.
SCENE_REGISTRY: dict[str, str] = {
    # Definitions (Phase 2)
    "DefAngleTypes": "src/byrne_euclid/definitions.py",
    "DefCircle": "src/byrne_euclid/definitions.py",
    "DefParallelLines": "src/byrne_euclid/definitions.py",
    "DefPointLineStraightLine": "src/byrne_euclid/definitions.py",
    "DefQuadrilaterals": "src/byrne_euclid/definitions.py",
    "DefTrianglesByAngle": "src/byrne_euclid/definitions.py",
    "DefTrianglesBySide": "src/byrne_euclid/definitions.py",
    "PaletteCard": "src/byrne_euclid/definitions.py",
    # Postulates (Phase 2)
    "PostulateI": "src/byrne_euclid/postulates.py",
    "PostulateII": "src/byrne_euclid/postulates.py",
    "PostulateIII": "src/byrne_euclid/postulates.py",
    # Propositions (Phases 3–4)
    "PropI": "src/byrne_euclid/propositions.py",
    "PropII": "src/byrne_euclid/propositions.py",
    "PropIII": "src/byrne_euclid/propositions.py",
    "PropIX": "src/byrne_euclid/propositions.py",
    "PropX": "src/byrne_euclid/propositions.py",
    "PropXI": "src/byrne_euclid/propositions.py",
    "PropXII": "src/byrne_euclid/propositions.py",
    "PropXIII": "src/byrne_euclid/propositions.py",
    "PropXV": "src/byrne_euclid/propositions.py",
    "PropXXXII": "src/byrne_euclid/propositions.py",
}

OUTPUT_DIR = Path("output")

def render(scene_name: str, quality: str = "h", fmt: str = "mp4"):
    """Render a named scene class and collect output to output/."""
    if scene_name not in SCENE_REGISTRY:
        print(f"Scene '{scene_name}' not in SCENE_REGISTRY.")
        print(f"Available scenes: {', '.join(sorted(SCENE_REGISTRY))}")
        sys.exit(1)

    module_path = SCENE_REGISTRY[scene_name]
    output_dir = OUTPUT_DIR / fmt
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "uv", "run", "manim", "render",
        f"-q{quality}",
        f"--format={fmt}",
        module_path,
        scene_name,
    ]
    subprocess.run(cmd, check=True)

    # Collect output file from Manim's media/ tree into output/
    ext = "png" if fmt == "png" else fmt
    search_dir = "media/images" if fmt == "png" else "media/videos"
    rendered = glob.glob(f"{search_dir}/**/{scene_name}.{ext}", recursive=True)
    if rendered:
        dest = output_dir / f"{scene_name}.{ext}"
        shutil.copy2(rendered[0], dest)
        print(f"  → {dest}")
    else:
        print(f"  ⚠ Output file not found in {search_dir}/")

def main():
    parser = argparse.ArgumentParser(description="Render a single Byrne-Euclid scene")
    parser.add_argument("scene", help="Scene class name, e.g. PropI")
    parser.add_argument("--quality", "-q", default="h", choices=["l", "m", "h", "p", "k"])
    parser.add_argument("--format", "-f", default="mp4", choices=["mp4", "gif", "png"])
    args = parser.parse_args()
    render(args.scene, args.quality, args.format)

if __name__ == "__main__":
    main()
```

### render_all.py

```python
"""Render every scene to output/ in MP4 and PNG formats.

Square GIFs are produced separately by scripts/gif_convert.sh,
which crops the 16:9 MP4s to square and converts to GIF.
"""
import glob
import shutil
import subprocess
from pathlib import Path

# Import the registry from render_one — single source of truth
from scripts.render_one import SCENE_REGISTRY

OUTPUT_DIR = Path("output")

def main():
    scenes = sorted(SCENE_REGISTRY.items())
    print(f"Rendering {len(scenes)} scenes.\n")

    # Render MP4s at high quality
    mp4_dir = OUTPUT_DIR / "mp4"
    mp4_dir.mkdir(parents=True, exist_ok=True)
    for scene_name, module_path in scenes:
        print(f"  MP4: {scene_name}...")
        cmd = [
            "uv", "run", "manim", "render",
            "-qh", "--format=mp4",
            module_path, scene_name,
        ]
        subprocess.run(cmd, check=True)
        rendered = glob.glob(f"media/videos/**/{scene_name}.mp4", recursive=True)
        if rendered:
            shutil.copy2(rendered[0], mp4_dir / f"{scene_name}.mp4")

    # Render final-frame PNGs
    png_dir = OUTPUT_DIR / "png"
    png_dir.mkdir(parents=True, exist_ok=True)
    for scene_name, module_path in scenes:
        print(f"  PNG: {scene_name}...")
        cmd = [
            "uv", "run", "manim", "render",
            "-qh", "-s",
            module_path, scene_name,
        ]
        subprocess.run(cmd, check=True)
        rendered = glob.glob(f"media/images/**/{scene_name}.png", recursive=True)
        if rendered:
            shutil.copy2(rendered[0], png_dir / f"{scene_name}.png")

    print(f"\nDone. MP4s in {mp4_dir}/, PNGs in {png_dir}/.")
    print("Run 'bash scripts/gif_convert.sh' to generate square GIFs.")

if __name__ == "__main__":
    main()
```

### Post-render: high-quality GIF conversion

Manim's built-in GIF export is adequate for iteration but poor for final output. A post-processing step uses ffmpeg's two-pass palette generation:

```bash
# scripts/gif_convert.sh
#!/usr/bin/env bash
# Convert 16:9 MP4s to square, looping, high-quality GIFs.
# Crops the centre of the 16:9 frame to a square, then applies
# ffmpeg two-pass palettegen for Byrne's limited-colour palette.
set -euo pipefail

mkdir -p output/gif

for mp4 in output/mp4/*.mp4; do
    base=$(basename "$mp4" .mp4)
    echo "  GIF: ${base}..."
    ffmpeg -y -i "$mp4" \
        -vf "crop=ih:ih:(iw-ih)/2:0,fps=15,scale=540:540:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3" \
        -loop 0 \
        "output/gif/${base}.gif"
done

echo "Done. GIFs in output/gif/."
```

The limited palette (64 colours) works well for Byrne's four-colour system — fewer colours means smaller files and cleaner dithering.

---

## 7. Curriculum manifest schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ByrneEuclidCurriculumManifest",
  "type": "object",
  "properties": {
    "version": { "type": "string" },
    "generated_at": { "type": "string", "format": "date-time" },
    "animations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "scene_class": { "type": "string" },
          "title": { "type": "string" },
          "euclid_book": { "type": "integer" },
          "euclid_type": { "enum": ["definition", "postulate", "proposition"] },
          "euclid_number": { "type": "integer" },
          "euclid_numbers": { "type": "array", "items": { "type": "integer" } },
          "description": { "type": "string" },
          "duration_seconds": { "type": "number" },
          "nc_references": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "key_stage": { "type": "string" },
                "year": { "type": "integer" },
                "domain": { "type": "string" },
                "statement": { "type": "string" }
              }
            }
          },
          "oak_lesson_slugs": { "type": "array", "items": { "type": "string" } },
          "oak_thread_slugs": { "type": "array", "items": { "type": "string" } },
          "keywords": { "type": "array", "items": { "type": "string" } },
          "misconceptions": { "type": "array", "items": { "type": "string" } },
          "alt_text": { "type": "string", "description": "One-sentence text description of the animation for accessibility (alt-text for GIF embeds)" },
          "files": {
            "type": "object",
            "properties": {
              "gif": { "type": "string" },
              "mp4": { "type": "string" },
              "png": { "type": "string" }
            }
          }
        },
        "required": ["scene_class", "euclid_type", "title"]
      }
    }
  }
}
```

This manifest is the connective tissue between the animations and the curriculum. It's what makes the project more than a collection of pretty GIFs.

---

## 8. Working in the open

### 8.1 Licence

**Code**: MIT — the same licence as ManimCE. No friction for anyone wanting to fork, adapt, or extend.

**Animations** (rendered outputs): CC-BY 4.0 — teachers can use, share, and adapt the GIFs/videos with attribution. This aligns with Oak's OGL approach.

**Curriculum data** (cached Oak API responses): Open Government Licence — inherited from Oak. Attribution to Oak National Academy required.

### 8.2 Reproducibility guarantees

| Guarantee | How |
|-----------|-----|
| Exact Python environment | `uv.lock` committed to repo — `uv sync` reproduces identical dependency tree |
| System dependencies documented | README lists apt/brew packages; CI workflow is the executable spec |
| Rendering is deterministic | Manim with fixed `seed` in config; no randomness in scenes |
| CI renders match local renders | Same `manim.cfg`, same quality flags, same ffmpeg version |
| Curriculum data versioned | Cached JSON in `curriculum/` — git tracks changes |
| No secrets required for rendering | API key only needed for `fetch_oak_curriculum.py`; cached data is committed |

### 8.3 Contributor experience

The `CONTRIBUTING.md` should make it trivially easy to add a new animation:

1. Pick an unimplemented Euclid definition/proposition from the tracking table in `docs/curriculum_mapping.md`
2. Copy an existing scene class as a template
3. Implement `construct()`
4. Add an entry to `curriculum/euclid_to_oak.yaml`
5. Render locally: `uv run python scripts/render_one.py YourScene`
6. Open a PR — CI renders it and uploads the output as an artefact

### 8.4 Documentation as code

The repo documentation serves three audiences:

| Audience | Document | Purpose |
|----------|----------|---------|
| Teacher | README (top half) | "What is this? How do I use the animations?" |
| Developer | README (bottom half), CONTRIBUTING | "How do I run / extend this?" |
| Designer | `docs/style_guide.md` | "What are the visual rules?" |
| Curriculum specialist | `docs/curriculum_mapping.md` | "How does this connect to the NC?" |

### 8.5 Release process

1. All scenes pass CI rendering
2. Tag `vX.Y.Z` on main
3. GitHub Actions renders all scenes at maximum quality
4. Release is created with rendered GIFs, MP4s, PNGs, and the curriculum manifest attached as assets
5. YouTube playlist is updated manually (scripted upload is a future nice-to-have)

---

## 9. Sequencing and milestones

| Milestone | Phases | Deliverable | Target |
|-----------|--------|-------------|--------|
| **M0: It renders** | Phase 0 | One scene (Prop I), CI green | Day 1 |
| **M1: It's consistent** | Phase 1 | Design system locked, style guide written | Day 3 |
| **M2: Definitions & postulates done** | Phase 2 | 10 animations (7 defs + 3 postulates) | Day 7 |
| **M3: Constructions done** | Phase 3 | 7 construction animations (Props I–III, IX–XII) | Day 13 |
| **M4: Theorems done** | Phase 4 | 3 theorem animations (Props XIII, XV, XXXII) | Day 17 |
| **M5: Curriculum linked** | Phase 5 | Manifest JSON, Oak data cached | Day 20 |
| **M6: Published** | Phase 6 | Blog post live, YouTube playlist up, repo public | Day 25 |

The plan produces **20 animations** in v0.1. PropXLVII (Pythagorean theorem) is the hero feature of v0.2.

---

## 10. Risk register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Manim's geometry primitives don't support a needed construction | Medium | Write custom VMobjects in `utils.py`; the intersection/perpendicular helpers cover the trickiest cases |
| Rendering is too slow for iteration | Low | Use `-ql` (480p 15fps) during development; only render high-quality for review and release |
| Oak API changes or is unavailable | Low | Cached data in `curriculum/` means the project works offline; API is only for refresh |
| Font rendering differs across platforms | Low | Use system-default serif or bundle a font via fontconfig; keep text minimal per the Byrne philosophy |
| GIF file sizes are too large for embedding | Medium | ffmpeg palettegen with 64-colour limit; Byrne's 4-colour palette compresses beautifully; offer MP4 as alternative |
| Scope creep into Books II–VI | Medium | Strict scope: Book I only for v0.1. The architecture supports extension, but the plan doesn't promise it |
| LaTeX dependency makes contributor setup painful | Medium | Avoid `Tex()`/`MathTex()` entirely — use `Text()` for all labels. LaTeX only needed if someone explicitly wants mathematical notation |

---

## 11. Future extensions (out of scope for v0.1)

These are noted so the architecture can accommodate them, but they're explicitly not in the plan:

- **PropXLVII — Pythagorean theorem (v0.2 hero feature)**: The most complex and visually spectacular animation. Squares on each side of a right triangle, area equivalence via Euclid's altitude construction. Byrne's most iconic page. Deserves its own focused iteration with sub-tasks: coordinate planning, static diagram, construction animation, area demonstration, polish. Target for v0.2 release and a sequel blog post.
- **Interactive web versions**: Render to Manim's WebGL output or convert to Lottie/SVG animations for embedding without video
- **Narration track**: AI-generated or recorded voiceover synced to animation timestamps
- **Books II–VI**: Extend beyond Book I — the `ByrneScene` class and curriculum manifest support this
- **Other curricula**: Map to Scottish, Welsh, IB, or Common Core standards
- **Oak API write-back**: If Oak ever supports third-party resource submissions, auto-submit the animations
- **Classroom worksheet generator**: Use the curriculum manifest to generate printable worksheets that reference specific animations
- **Manim Slides integration**: Convert the scenes to interactive slide decks using `manim-slides` for live classroom use
- **Colour-blind-safe palette**: Alternative palette mode using Wong's colour-blind-safe colours, swappable via `style.py` constants

---

## 12. Detailed TODO

Every task needed to ship v0.1, broken down by phase. Tasks are ordered within each phase — work top-to-bottom. Dependencies between phases are noted where they exist.

### Phase 0: Skeleton → Milestone M0 ("It renders")

> **Goal**: A repo on GitHub that renders one scene end-to-end, with CI passing.
> **Depends on**: Nothing. This is the starting point.

#### 0.1 — Repository initialisation

- [ ] Create project directory: `uv init byrne-euclid-manim`
- [ ] `cd byrne-euclid-manim`
- [ ] Create the `src/byrne_euclid/` package directory
- [ ] Create `src/byrne_euclid/__init__.py` (empty, or with package-level docstring)
- [ ] Write `pyproject.toml` with project metadata, dependencies (`manim`, `httpx`, `pydantic`), dev dependencies (`pytest`, `ruff`), and build system
- [ ] Run `uv add manim httpx pydantic` to populate the lockfile
- [ ] Run `uv add --dev pytest ruff`
- [ ] Verify: `uv run manim --version` outputs a version string without error
- [ ] Verify: `uv run python -c "from manim import *; print('OK')"` succeeds

#### 0.2 — Core style module

- [ ] Create `src/byrne_euclid/style.py`
- [ ] Define palette constants: `BYRNE_RED`, `BYRNE_YELLOW`, `BYRNE_BLUE`, `BYRNE_BLACK`, `BYRNE_BG`
- [ ] Define line style constants: `BYRNE_THICK`, `BYRNE_THIN`
- [ ] Implement `ByrneScene(Scene)` base class with `setup()` method that sets `self.camera.background_color = BYRNE_BG`
- [ ] Add `byrne_line(self, start, end, color, thick)` helper method
- [ ] Add `byrne_circle(self, center, radius, color)` helper method
- [ ] Add `byrne_dot(self, point, color)` helper method
- [ ] Add `byrne_title(self, text, position)` helper method

#### 0.3 — First scene: Proposition I

- [ ] Create `src/byrne_euclid/propositions.py`
- [ ] Implement `PropI(ByrneScene)` — equilateral triangle construction:
  - Title card "Proposition I." in top-left
  - Draw given line AB (black)
  - Sweep circle centred on A, radius AB (blue)
  - Sweep circle centred on B, radius BA (red)
  - Mark intersection point C
  - Draw line CA (yellow) and line CB (red)
  - Fill triangle lightly
  - Fade construction circles
  - Hold on final state
- [ ] Verify: `uv run manim render -pql src/byrne_euclid/propositions.py PropI` plays a preview

#### 0.4 — Render script

- [ ] Create `scripts/` directory
- [ ] Write `scripts/render_one.py` with **scene registry dict**:
  - Maintain `SCENE_REGISTRY: dict[str, str]` mapping scene class names to source file paths
  - Accept scene class name as CLI argument
  - Accept `--quality` flag (`l`, `m`, `h`) defaulting to `m`
  - Accept `--format` flag (`mp4`, `gif`, `png`) defaulting to `mp4`
  - Look up the scene in the registry; exit with helpful error listing available scenes if not found
  - Invoke `uv run manim render` as a subprocess with the correct arguments
  - **Collect output**: find the rendered file in `media/` and copy it to `output/{fmt}/`
  - Document the registry dict in a module docstring: "When adding a new scene, add it to SCENE_REGISTRY"
- [ ] Verify: `uv run python scripts/render_one.py PropI` produces `output/mp4/PropI.mp4`
- [ ] Verify: `uv run python scripts/render_one.py PropI --format gif` produces a GIF in `output/gif/`

#### 0.5 — Project configuration files

- [ ] Write `manim.cfg` — all settings under `[CLI]`:
  ```ini
  [CLI]
  quality = medium_quality
  format = mp4
  preview = false
  background_color = #F5F0E1
  media_dir = ./media
  ```
- [ ] Write `.gitignore`:
  - `media/`
  - `output/`
  - `__pycache__/`
  - `.venv/`
  - `*.pyc`
  - `.ruff_cache/`
  - `.pytest_cache/`
  - `.env`
- [ ] Write `LICENSE` (MIT licence text, copyright Mat Gregory)

#### 0.6 — README (initial version)

- [ ] Write `README.md` with:
  - Project title and one-line description
  - A "What is this?" paragraph (animated Euclid, Byrne style, curriculum-aligned)
  - "Quickstart" section: prerequisites (ffmpeg, cairo, pango), then `uv sync && uv run python scripts/render_one.py PropI`
  - "Status" badge placeholder (CI link)
  - Licence note (MIT code, CC-BY animations)
  - Credits: Byrne, Rougeux, jemmybutton, ManimCE, Oak

#### 0.7 — Continuous integration

- [ ] Create `.github/workflows/render.yml`
- [ ] Define trigger: push to `main` on paths `src/**` and `manim.cfg`, plus `workflow_dispatch`
- [ ] Job steps:
  - `actions/checkout@v4`
  - Install system deps: `sudo apt-get install -y ffmpeg libcairo2-dev libpango1.0-dev`
  - Install uv: `astral-sh/setup-uv@v4`
  - `uv sync`
  - Render PropI at medium quality: `uv run python scripts/render_one.py PropI --quality m`
  - Lint: `uv run ruff check src/ scripts/`
  - Upload output as artefact: `actions/upload-artifact@v4`
- [ ] Push to GitHub
- [ ] Verify: CI workflow runs green
- [ ] Verify: rendered artefact is downloadable from the Actions tab

#### 0.8 — Stub files for future phases

- [ ] Create `src/byrne_euclid/definitions.py` with module docstring only (no scenes yet)
- [ ] Create `src/byrne_euclid/postulates.py` with module docstring only
- [ ] Create `src/byrne_euclid/utils.py` with module docstring only
- [ ] Create `curriculum/` directory with a `.gitkeep`
- [ ] Create `docs/` directory with a `.gitkeep`
- [ ] Create `tests/` directory with `tests/__init__.py`
- [ ] Create `output/` directories: `output/gif/`, `output/mp4/`, `output/png/` (all gitignored)

#### 0.9 — References and attribution

- [ ] Create `references/` directory
- [ ] Download the three NC Mathematics Programme of Study PDFs from GOV.UK:
  - KS1 & KS2: `https://assets.publishing.service.gov.uk/media/5a7da548ed915d2ac884cb07/PRIMARY_national_curriculum_-_Mathematics_220714.pdf`
  - KS3: `https://assets.publishing.service.gov.uk/media/5a7c1408e5274a1f5cc75a68/SECONDARY_national_curriculum_-_Mathematics.pdf`
  - KS4: `https://assets.publishing.service.gov.uk/media/5a7dc9dced915d2ac884d8ef/KS4_maths_PoS_FINAL_170714.pdf`
- [ ] Save as `references/NC_KS1_KS2_Mathematics.pdf`, `references/NC_KS3_Mathematics.pdf`, `references/NC_KS4_Mathematics.pdf`
- [ ] Write `references/README.md` containing:
  - OGL v3.0 attribution statement: *"Contains public sector information licensed under the Open Government Licence v3.0"*
  - Table of all project sources with URL, licence, and how we use each (see research.md §10.1)
  - Statement that Byrne's 1847 text is public domain (CC0, Smithsonian confirmation)
  - Statement that our animations are original works inspired by Byrne's public domain design system, not reproductions of any copyrighted work
  - Links to sources we reference but don't store (Internet Archive scan, c82.net, jemmybutton repo, Tufte)
  - Credit to Nicholas Rougeux (c82.net), Sergey Slyusarev (jemmybutton), ManimCE community, Oak National Academy
  - Credit to Oliver Byrne, William Pickering, Mary Byfield (original 1847 edition)
- [ ] Commit `references/` to the repo

---

### Phase 1: Design system → Milestone M1 ("It's consistent")

> **Goal**: A locked-down visual style that produces consistent output. Any future scene inherits the look automatically.
> **Depends on**: Phase 0 complete (repo exists, ByrneScene renders).

#### 1.0 — Verify Byrne colour palette

- [ ] Open https://www.c82.net/euclid/book1/ in a browser
- [ ] Use browser DevTools or a colour picker to sample the exact red, yellow, blue, and black from a diagram (e.g. Proposition I)
- [ ] Compare sampled values to the research values (`#E6382D`, `#F0C824`, `#1A6FB5`, `#2B2B2B`)
- [ ] Sample the background/page colour — compare to `#F5F0E1`
- [ ] If any value differs significantly, update `BYRNE_RED` etc. in `style.py` and document the verified values in `docs/style_guide.md`
- [ ] This is a 👤 **Mat only** task — visual judgment on whether sampled colours match the "feel" of Byrne

#### 1.1 — Expand ByrneScene helper methods

- [ ] Add `byrne_dashed_line(self, start, end, color, thick)` — returns a `DashedLine` with `dash_length=BYRNE_DASH_LENGTH, dashed_ratio=BYRNE_DASH_RATIO` and Byrne styling
- [ ] Add `byrne_arc(self, center, radius, start_angle, angle, color)` — returns a styled `Arc`
- [ ] Add `byrne_angle(self, line1, line2, color, radius)` — returns a styled `Angle` mobject with fill
- [ ] Add `byrne_polygon(self, *vertices, color, fill_opacity)` — returns a styled `Polygon`
- [ ] Add `byrne_right_angle_mark(self, vertex, line1_dir, line2_dir, color)` — small square at a right angle vertex

#### 1.2 — Animation convenience methods on ByrneScene

- [ ] Add `construct_line(self, start, end, color, thick, run_time)` — plays `Create` and returns the line
- [ ] Add `sweep_circle(self, center, radius, color, run_time)` — plays `Create` on an arc from 0 to TAU, returns circle
- [ ] Add `mark_angle(self, line1, line2, color, radius)` — plays `FadeIn` on angle mark, returns it
- [ ] Add `fade_construction(self, *mobjects, target_opacity, run_time)` — fades auxiliary elements
- [ ] Add `qed_hold(self, duration)` — `self.wait(duration)` with a standardised default (2 seconds)

#### 1.3 — Configurable output dimensions

- [ ] Add class attribute `aspect_ratio` to `ByrneScene` (default `"16:9"`, option `"1:1"`)
- [ ] In `setup()`, set `config.pixel_width` and `config.pixel_height` based on `aspect_ratio`
- [ ] Verify: a scene with `aspect_ratio = "1:1"` renders as a 1080×1080 square
- [ ] Verify: default `"16:9"` renders as 1920×1080

#### 1.4 — Geometry utility functions

- [ ] Create `src/byrne_euclid/utils.py` with the following pure functions:
- [ ] `circle_intersection(c1_centre, c1_radius, c2_centre, c2_radius) -> tuple[np.ndarray, np.ndarray]` — returns both intersection points (upper first), raises `ValueError` if circles don't intersect
- [ ] `line_intersection(p1, p2, p3, p4) -> np.ndarray` — intersection of line through p1-p2 and line through p3-p4, raises `ValueError` if parallel
- [ ] `perpendicular_foot(point, line_start, line_end) -> np.ndarray` — foot of perpendicular from point to line
- [ ] `midpoint(a, b) -> np.ndarray` — midpoint of segment
- [ ] `point_on_circle(centre, radius, angle_radians) -> np.ndarray` — point at given angle on circle
- [ ] `angle_between_lines(p1, p2, p3) -> float` — angle at p2 in radians, measured from p1-p2 to p2-p3

#### 1.5 — Unit tests

- [ ] Create `tests/test_style.py`:
  - Assert `BYRNE_RED == "#E6382D"` (and other palette values) — prevents accidental changes
  - Assert `ByrneScene` is a subclass of `Scene`
  - Test `byrne_line` returns a `Line` with correct colour and stroke width
  - Test `byrne_circle` returns a `Circle` with correct colour, centred at the right point
- [ ] Create `tests/test_utils.py`:
  - Test `circle_intersection` with known geometry (two unit circles at distance 1 → known intersection)
  - Test `circle_intersection` raises `ValueError` for non-intersecting circles
  - Test `midpoint` for trivial cases
  - Test `perpendicular_foot` for a point directly above a horizontal line
  - Test `line_intersection` for perpendicular lines through origin
- [ ] Verify: `uv run pytest tests/` passes

#### 1.6 — Palette card scene

- [ ] Create a `PaletteCard(ByrneScene)` scene (in `definitions.py` or a standalone `showcase.py`):
  - Display four colour swatches (filled squares) labelled with hex values
  - Show line thickness comparison (thick vs thin, solid vs dashed)
  - Show an angle mark example
  - Background is `BYRNE_BG`
- [ ] Render as PNG — this becomes the palette reference image for `docs/style_guide.md` and the blog post

#### 1.7 — Style guide document

- [ ] Write `docs/style_guide.md`:
  - Palette table with hex values and usage rules (which colour for what)
  - Stroke width rules (thick for primary elements, thin for construction/auxiliary)
  - Line style rules (solid for results, dashed for construction)
  - Fill opacity rules (0.3–0.5 for shape fills, 0.5 for angle sectors)
  - Animation timing rules (default `run_time` values, hold durations)
  - Typography rules (font choice, size, positioning, minimal text)
  - Aspect ratio guidance (compose for 16:9; square GIFs are cropped from centre in post-processing)
  - Embed the palette card PNG
  - "Do" and "Don't" examples with screenshots
  - **Accessibility note**: document the palette's colour-blind limitations honestly; note that Byrne's system also uses stroke thickness and dash pattern to differentiate (not colour alone); colour-blind-safe alternative palette is a v0.2 goal

#### 1.8 — Update CI

- [ ] Add `uv run pytest tests/` step to the CI workflow, before the render step
- [ ] Verify: CI passes with tests and render

---

### Phase 2: Tier 1 animations — Definitions & Postulates → Milestone M2 ("Definitions & postulates done")

> **Goal**: 10 polished animations covering foundational geometry vocabulary (KS2–KS3): 7 definitions + 3 postulates.
> **Depends on**: Phase 1 complete (design system locked, helpers available).

#### 2.1 — DefPointLineStraightLine

- [ ] Implement `DefPointLineStraightLine(ByrneScene)` in `definitions.py`
- [ ] Animation sequence:
  - Title "Definitions I, II, IV."
  - A dot appears at centre (Byrne black) — "A point has no parts"
  - A line is drawn from left to right (Byrne black) — "length without breadth"
  - A curved line appears above, then a straight line below — contrast between them
  - The curved line fades; the straight line "lies evenly between its extremities"
  - Hold
- [ ] Render at low quality, review timing and positioning
- [ ] Adjust and re-render at medium quality

#### 2.2 — DefAngleTypes

- [ ] Implement `DefAngleTypes(ByrneScene)` in `definitions.py`
- [ ] Animation sequence:
  - Title "Definitions X–XII."
  - Draw a horizontal base line (black)
  - Draw a vertical line from the same point — forms a right angle
  - Mark the right angle with a small square (Byrne yellow)
  - Label "Right angle" briefly
  - Rotate the vertical arm past 90° — angle sector turns red → "Obtuse angle"
  - Rotate the arm back below 90° — angle sector turns blue → "Acute angle"
  - Show all three side by side in final frame
  - Hold
- [ ] Render, review, adjust

#### 2.3 — DefCircle

- [ ] Implement `DefCircle(ByrneScene)` in `definitions.py`
- [ ] Animation sequence:
  - Title "Definitions XV–XVIII."
  - Centre point appears (black dot)
  - Radius line extends from centre to the right (Byrne red)
  - Circle sweeps out from the radius endpoint (Byrne blue) — compass feel
  - Radius label or emphasis
  - Diameter drawn through centre (Byrne yellow), terminating on circumference both sides
  - Semicircle region fills lightly to show Def XVIII
  - Hold
- [ ] Render, review, adjust

#### 2.4 — DefTrianglesBySide

- [ ] Implement `DefTrianglesBySide(ByrneScene)` in `definitions.py`
- [ ] Animation sequence:
  - Title "Definitions XXIV–XXVI."
  - Draw equilateral triangle (all sides Byrne red, all sides visually equal) — label "Equilateral"
  - Transition or shift; draw isosceles triangle (two sides Byrne blue, one Byrne black) — label "Isosceles"
  - Transition or shift; draw scalene triangle (each side a different colour) — label "Scalene"
  - Final frame: all three side by side
  - Hold
- [ ] Render, review, adjust

#### 2.5 — DefTrianglesByAngle

- [ ] Implement `DefTrianglesByAngle(ByrneScene)` in `definitions.py`
- [ ] Animation sequence:
  - Title "Definitions XXVII–XXIX."
  - Draw right-angled triangle with the right angle marked (yellow square)
  - Transition; draw obtuse-angled triangle with the obtuse angle marked (red sector)
  - Transition; draw acute-angled triangle with all three acute angles marked (blue sectors)
  - Final frame: all three side by side with angle marks
  - Hold
- [ ] Render, review, adjust

#### 2.6 — DefQuadrilaterals

- [ ] Implement `DefQuadrilaterals(ByrneScene)` in `definitions.py`
- [ ] Animation sequence:
  - Title "Definitions XXX–XXXIV."
  - Draw a square (Byrne red fill, all sides equal, all angles right-angle-marked)
  - Transform into a rectangle (stretch horizontally, Byrne blue fill, angles still right)
  - Transform into a rhombus (shear, Byrne yellow fill, sides equal, angles not right)
  - Transform into a parallelogram (Byrne red outline, opposite sides equal, not all sides equal)
  - Optionally show a trapezium as "all other quadrilaterals"
  - Hold
- [ ] Render, review, adjust

#### 2.7 — DefParallelLines

- [ ] Implement `DefParallelLines(ByrneScene)` in `definitions.py`
- [ ] Animation sequence:
  - Title "Definition XXXV."
  - Draw two horizontal lines, close together (Byrne red and Byrne blue)
  - Extend both lines in both directions simultaneously — they grow but never converge
  - Show equal-spacing markers (small perpendicular ticks) at several points
  - Hold
- [ ] Render, review, adjust

#### 2.8 — PostulateI (Draw a straight line)

- [ ] Implement `PostulateI(ByrneScene)` in `postulates.py`
- [ ] Animation sequence:
  - Title "Postulate I."
  - Two points appear (Byrne black dots)
  - A straight line is drawn from one to the other (Byrne black)
  - Hold
- [ ] Render, review, adjust
- [ ] These are simple — ~10 seconds each. They establish the "rules of the game" before constructions.

#### 2.9 — PostulateII (Extend a line)

- [ ] Implement `PostulateII(ByrneScene)` in `postulates.py`
- [ ] Animation sequence:
  - Title "Postulate II."
  - A finite line segment appears (Byrne black)
  - The line extends from one end, growing indefinitely (dashed extension in Byrne blue or same colour)
  - Hold
- [ ] Render, review, adjust

#### 2.10 — PostulateIII (Draw a circle)

- [ ] Implement `PostulateIII(ByrneScene)` in `postulates.py`
- [ ] Animation sequence:
  - Title "Postulate III."
  - A centre point appears (Byrne black dot)
  - A radius line is drawn from centre to a point (Byrne red)
  - A circle sweeps out from the radius endpoint (Byrne blue) — compass feel
  - Hold
- [ ] Render, review, adjust

#### 2.11 — Phase 2 review and consistency pass

- [ ] Render all 10 scenes (7 definitions + 3 postulates) at medium quality as MP4
- [ ] Watch all 10 sequentially — check for:
  - Consistent title positioning and font size
  - Consistent animation timing (not too fast, not too slow)
  - Consistent shape sizes (shapes should be roughly the same scale)
  - Consistent colour usage (same semantic mapping across all scenes)
  - Consistent hold duration at the end
- [ ] Adjust any outliers
- [ ] Final render of all 10 at high quality
- [ ] Generate final-frame PNGs for each

#### 2.12 — Update curriculum mapping

- [ ] Add entries to `curriculum/euclid_to_oak.yaml` for all 10 scenes
- [ ] For each: scene class name, euclid type/numbers, NC references, keywords
- [ ] Oak lesson slugs can be left empty — populated in Phase 5
- [ ] Validate YAML syntax

---

### Phase 3: Tier 2 animations — Constructions → Milestone M3 ("Constructions done")

> **Goal**: 7 animations covering the KS3 statutory ruler-and-compass constructions plus their prerequisite sub-procedures.
> **Depends on**: Phase 1 complete (utils.py geometry helpers needed for intersection calculations).

#### 3.1 — PropI (Equilateral triangle — upgrade from Phase 0)

- [ ] Revisit the Phase 0 `PropI` implementation
- [ ] Refactor to use `ByrneScene` helper methods from Phase 1
- [ ] Refactor to use `circle_intersection()` from `utils.py` instead of hardcoded coordinates
- [ ] Ensure it matches the finalised style guide (stroke widths, fill opacities, timing)
- [ ] Add dashed lines for construction circles if that's the agreed style
- [ ] Re-render and review

#### 3.2 — PropII (Copy a line segment)

- [ ] Implement `PropII(ByrneScene)` in `propositions.py`
- [ ] Animation sequence per Euclid's construction:
  - Title "Proposition II."
  - Given: a point and a separate line segment (Byrne black)
  - Draw a line from the point to one end of the given segment
  - Construct an equilateral triangle on that connecting line (reuse PropI technique)
  - Extend one side of the triangle
  - Draw circle centred on the far end of the given segment, radius = the given segment (Byrne blue)
  - Draw circle centred on the triangle vertex, radius = extended side (Byrne red)
  - The difference gives a line from the original point, equal to the given segment
  - Mark the result; fade construction
  - Hold
- [ ] This is the most complex early proposition — expect iteration on clarity
- [ ] Render, review, adjust

#### 3.3 — PropIII (Cut off a segment equal to a shorter one)

- [ ] Implement `PropIII(ByrneScene)` in `propositions.py`
- [ ] Animation sequence per Euclid's construction:
  - Title "Proposition III."
  - Given: a longer line and a shorter line (Byrne black and Byrne blue)
  - Use PropII technique to copy the shorter line to an endpoint of the longer line (Byrne red)
  - Draw a circle with that copied length as radius (Byrne red circle)
  - The circle cuts the longer line at the desired point
  - Mark the cut-off segment; fade construction
  - Hold
- [ ] Render, review, adjust

#### 3.4 — PropIX (Bisect an angle)

- [ ] Implement `PropIX(ByrneScene)` in `propositions.py`
- [ ] Animation sequence per Euclid's construction:
  - Title "Proposition IX."
  - Draw two lines meeting at a vertex forming an angle (Byrne red and Byrne blue)
  - Take equal segments on each arm from the vertex (mark with dots)
  - Draw connecting line between the two marked points (Byrne yellow)
  - Construct equilateral triangle on that connecting line (using circle sweeps)
  - Draw line from original vertex through the apex of the equilateral triangle (Byrne black)
  - Mark the two half-angles with matching colour sectors — show they're equal
  - Fade construction elements
  - Hold
- [ ] Render, review, adjust

#### 3.5 — PropX (Bisect a line segment)

- [ ] Implement `PropX(ByrneScene)` in `propositions.py`
- [ ] Animation sequence per Euclid's construction:
  - Title "Proposition X."
  - Draw given line segment (Byrne black)
  - Construct equilateral triangle on the line (reusing PropI pattern / calling helper)
  - Bisect the apex angle (reusing PropIX pattern)
  - The bisector meets the base at the midpoint
  - Mark the midpoint; show both halves are equal
  - Fade construction elements
  - Hold
- [ ] Render, review, adjust

#### 3.6 — PropXI (Perpendicular from a point on a line)

- [ ] Implement `PropXI(ByrneScene)` in `propositions.py`
- [ ] Animation sequence per Euclid's construction:
  - Title "Proposition XI."
  - Draw a line with a marked point on it (Byrne black line, red dot)
  - Take equal distances on either side of the point along the line
  - Construct equilateral triangle on the segment between those two points
  - Draw line from the apex to the marked point — this is the perpendicular
  - Mark the right angles with small squares
  - Fade construction elements
  - Hold
- [ ] Render, review, adjust

#### 3.7 — PropXII (Perpendicular from an external point to a line)

- [ ] Implement `PropXII(ByrneScene)` in `propositions.py`
- [ ] Animation sequence per Euclid's construction:
  - Title "Proposition XII."
  - Draw a line (Byrne black) and a point above it (Byrne red dot)
  - From the point, sweep a circle that crosses the line at two points
  - Bisect the segment between those two crossing points (using PropX technique)
  - Draw line from external point to the midpoint — this is the perpendicular
  - Mark the right angle
  - Fade construction elements
  - Hold
- [ ] Render, review, adjust

#### 3.8 — Phase 3 review and consistency pass

- [ ] Render all 7 construction scenes at medium quality
- [ ] Watch all 7 sequentially — check for:
  - Consistent "compass sweep" animation feel across all circle constructions
  - Construction circles consistently styled (same stroke width, same opacity fade)
  - "QED moment" at the end of each (fade aux, hold result) is consistent
  - Timing is deliberate — not rushed
  - Visual consistency with Phase 2 definition scenes
- [ ] Adjust any outliers
- [ ] Final render at high quality
- [ ] Generate final-frame PNGs

#### 3.9 — Update curriculum mapping

- [ ] Add entries to `curriculum/euclid_to_oak.yaml` for all 7 construction scenes
- [ ] For each: scene class name, euclid type/numbers, NC references (KS3 "ruler and compass constructions"), keywords
- [ ] Validate YAML syntax

---

### Phase 4: Tier 3 animations — Angle theorems → Milestone M4 ("Theorems done")

> **Goal**: 3 animations demonstrating key angle theorems.
> **Depends on**: Phase 1 complete. Phase 3 helpful but not strictly required.

#### 4.1 — PropXIII (Angles on a straight line)

- [ ] Implement `PropXIII(ByrneScene)` in `propositions.py`
- [ ] Animation sequence:
  - Title "Proposition XIII."
  - Draw a straight base line (Byrne black)
  - Draw a line standing on it at an arbitrary (non-right) angle
  - Mark the two adjacent angles in different colours (Byrne yellow, Byrne blue)
  - Animate the angle sectors filling
  - Draw a dotted perpendicular from the same point — show the right angles
  - Visually demonstrate that the two coloured angles together make two right angles (180°)
  - Optionally: show a numeric label "= 180°"
  - Hold
- [ ] Render, review, adjust

#### 4.2 — PropXV (Vertically opposite angles)

- [ ] Implement `PropXV(ByrneScene)` in `propositions.py`
- [ ] Animation sequence:
  - Title "Proposition XV."
  - Draw two intersecting straight lines (Byrne red and Byrne blue)
  - Mark all four angles with alternating colours (yellow and black, or red and blue)
  - Highlight one pair of vertically opposite angles — pulse or indicate
  - Visually show they're equal (same colour, same arc radius)
  - Highlight the other pair — show they're also equal
  - Hold
- [ ] Render, review, adjust

#### 4.3 — PropXXXII (Angle sum of a triangle)

- [ ] Implement `PropXXXII(ByrneScene)` in `propositions.py`
- [ ] Animation sequence:
  - Title "Proposition XXXII."
  - Draw a triangle (three sides in different Byrne colours)
  - Mark the three interior angles with three colours
  - Extend one side to form an exterior angle
  - Draw a line through the opposite vertex parallel to the base (construction)
  - Show that the exterior angle equals the sum of the two remote interior angles
  - Alternatively / additionally: animate "tearing off" the three angles and arranging them on a straight line to show they sum to 180°
  - Hold
- [ ] Render, review, adjust

#### 4.4 — Phase 4 review and consistency pass

- [ ] Render all 3 theorem scenes at medium quality
- [ ] Watch sequentially — check visual consistency with Phase 2 and Phase 3 scenes
- [ ] Adjust timing, colours, positions
- [ ] Final render at high quality
- [ ] Generate final-frame PNGs

#### 4.5 — Update curriculum mapping

- [ ] Add entries to `curriculum/euclid_to_oak.yaml` for all 3 theorem scenes
- [ ] For each: scene class name, euclid type/numbers, NC references (KS3 angle theorems), keywords
- [ ] Validate YAML syntax

---

### Phase 5: Curriculum integration → Milestone M5 ("Curriculum linked")

> **Goal**: Animations are connected to the Oak National Academy curriculum via a structured manifest.
> **Depends on**: At least one phase of animation scenes complete (Phase 2 minimum). Oak API key available.

#### 5.1 — Explore Oak API

- [x] Call `GET /subjects/maths` to confirm the subject slug and available sequences/key stages
- [x] Call `GET /threads` and identify the live geometry-related thread slugs
- [x] Call `GET /threads/{slug}/units` for the live geometry threads and confirm the relevant KS2/KS3 material sits under `geometry-and-measure`
- [x] Call `GET /key-stages/ks2/subject/maths/units` and `GET /key-stages/ks3/subject/maths/units` to record the grouped unit payload shape and the relevant geometry unit slugs
- [x] Call `GET /key-stages/{keyStage}/subject/maths/lessons?unit={geometry-unit-slug}` for representative units and confirm the grouped lesson payload shape
- [x] Call `GET /lessons/{lesson-slug}/summary` for representative geometry lessons and confirm keywords and misconceptions are present while `threads` may be empty
- [x] Document the relevant thread, unit, and lesson slugs in the refreshed live cache and hand-maintained mapping

#### 5.2 — Write fetch_oak_curriculum.py

- [x] Refresh `scripts/fetch_oak_curriculum.py` for the current live Oak payloads
- [x] Read `OAK_OPEN_API_KEY` or `OAK_API_KEY` from the environment and exit with a helpful error if neither is present
- [x] Define the base URL as `https://open-api.thenational.academy/api/v0`
- [x] Fetch `GET /threads` and save the full response as `curriculum/oak_threads_raw.json`
- [x] Normalise thread rows to stable `threadSlug` and `threadTitle` fields
- [x] For each candidate geometry thread, fetch `GET /threads/{slug}/units` and derive a unit-to-thread index
- [x] Fetch grouped KS2 and KS3 unit payloads, flatten them, and save the selected geometry units as `curriculum/oak_ks2_geometry_units.json` and `curriculum/oak_ks3_geometry_units.json`
- [x] Fetch `GET /key-stages/{keyStage}/subject/maths/lessons?unit={unitSlug}` for each selected geometry unit and save the normalised lesson rows as `curriculum/oak_ks2_geometry_lessons.json` and `curriculum/oak_ks3_geometry_lessons.json`
- [x] Fetch lesson summaries for the selected geometry lessons and accumulate keywords and misconceptions
- [x] Save the combined geometry thread, unit, lesson, and summary data as `curriculum/oak_geometry_data.json`
- [x] Keep the script idempotent so re-running overwrites the cached files cleanly
- [x] Keep the `--dry-run` flag so the planned Oak requests can be reviewed without making API calls
- [x] Verify: `uv run --env-file .env python scripts/fetch_oak_curriculum.py` populates `curriculum/` with live JSON files

#### 5.3 — Write the hand-maintained mapping file

- [x] Create `curriculum/euclid_to_oak.yaml`
- [x] For each implemented scene class, keep an entry with:
  - `scene`: the Python class name
  - `euclid_type`: `definition`, `postulate`, or `proposition`
  - `euclid_numbers`: list of Euclid numbers covered
  - `title`: human-readable title
  - `description`: one-sentence description of the animation
  - `alt_text`: one-sentence accessible text description for GIF embeds (e.g. "An animated construction showing two intersecting circles forming an equilateral triangle")
  - `nc_references`: list of `{key_stage, year, domain, statement}` objects from the national curriculum
  - `oak_lesson_slugs`: live Oak lesson slugs populated from the 5.1 exploration
  - `oak_thread_slugs`: list of Oak thread slugs
  - `keywords`: geometry vocabulary featured in the animation
  - `misconceptions`: common misconceptions this animation could address (from Oak lesson summaries)
- [x] Validate the YAML syntax
- [x] Verify that every mapped Oak lesson slug resolves against the refreshed live cache

#### 5.4 — Write build_manifest.py

- [x] Create `scripts/build_manifest.py`
- [x] Read `curriculum/euclid_to_oak.yaml`
- [x] Enrich with data from `curriculum/oak_geometry_data.json` when present:
  - Add missing keywords from Oak lesson data
  - Add misconceptions from Oak lesson summaries
- [x] For each entry, add `files` with expected relative output paths: `output/gif/{scene}.gif`, `output/mp4/{scene}.mp4`, `output/png/{scene}.png`
- [x] Add metadata including `version` and `generated_at`
- [x] Write to `curriculum/curriculum_manifest.json`
- [x] Verify: `uv run python scripts/build_manifest.py` produces valid JSON
- [x] Verify: the manifest can be loaded with `json.load()` and iterated

#### 5.5 — Write curriculum_mapping.md

- [x] Create `docs/curriculum_mapping.md`
- [x] Write the introductory paragraph explaining the Euclid → NC → Oak mapping
- [x] Render the manifest as a human-readable grouped view:
  - Columns: Animation title | Euclid ref | Key Stage | Year | NC statement | Oak lesson
  - Sorted by key stage then year
- [x] Link back to `curriculum/euclid_to_oak.yaml` as the source of truth through the generated artefacts
- [x] Verify the regenerated document no longer contains draft Oak placeholders

#### 5.6 — Commit cached curriculum data

- [x] Review all JSON files in `curriculum/` — ensure no API key or sensitive data is present
- [x] Maintain Oak attribution in `curriculum/README.md`
- [ ] Commit and push

---

### Phase 6: Polish and publish → Milestone M6 ("Published")

> **Goal**: Everything is production-quality, documented, and publicly available.
> **Depends on**: Phases 2–4 (animations exist) and Phase 5 (curriculum data exists).

#### 6.1 — Final rendering pipeline

- [ ] Write `scripts/render_all.py`:
  - Discover all `ByrneScene` subclasses across all modules
  - For each scene: render MP4 at high quality (1080p 60fps)
  - For each scene: render last frame as PNG
  - Copy final files to `output/mp4/` and `output/png/`
- [ ] Write `scripts/gif_convert.sh`:
  - For each MP4 in `output/mp4/`: convert to high-quality GIF using ffmpeg two-pass palettegen
  - Output to `output/gif/`
  - Parameters: 15fps, 540px width, 64-colour palette, bayer dithering
- [ ] Run the full pipeline: `uv run python scripts/render_all.py && bash scripts/gif_convert.sh`
- [ ] Spot-check 5 random outputs across all three tiers — verify quality

#### 6.2 — README completion

- [ ] Rewrite `README.md` for a public audience:
  - **Header**: Project name, one-line hook, badge row (CI status, licence, Python version)
  - **Hero image**: Embed the PropI GIF directly in the README
  - **"What is this?"**: 2–3 paragraphs — Byrne's Euclid, the curriculum connection, why animated
  - **Gallery**: Grid of 4–6 GIF thumbnails linking to full animations
  - **"For teachers"**: How to use the animations (download GIFs, embed in slides, link to YouTube)
  - **"For developers"**: Prerequisites, quickstart (`uv sync && uv run python scripts/render_one.py PropI`), project structure overview
  - **"Curriculum alignment"**: Brief explanation + link to `docs/curriculum_mapping.md`
  - **"Contributing"**: Link to `CONTRIBUTING.md`
  - **"Credits"**: Byrne/Pickering (1847), Nicholas Rougeux (c82.net), Sergey Slyusarev (jemmybutton), ManimCE, Oak National Academy
  - **"Licence"**: MIT (code), CC-BY 4.0 (animations), OGL (curriculum data)

#### 6.3 — CONTRIBUTING.md

- [ ] Write `CONTRIBUTING.md` covering:
  - **"Adding a new animation"**: step-by-step walkthrough
    1. Identify the Euclid definition/proposition to animate
    2. Check `docs/curriculum_mapping.md` for its NC alignment
    3. Choose the right module (`definitions.py`, `postulates.py`, or `propositions.py`)
    4. Copy an existing scene class as a template
    5. Implement `construct()` using `ByrneScene` helpers and Byrne palette only
    6. Add an entry to `curriculum/euclid_to_oak.yaml`
    7. Render locally: `uv run python scripts/render_one.py YourScene --quality l`
    8. Iterate until it looks right at `-ql`, then verify at `-qm`
    9. Open a PR with the new scene and YAML entry
  - **"Style rules"**: link to `docs/style_guide.md` and summarise the non-negotiables (four colours only, cream background, minimal text, serif font)
  - **"Running tests"**: `uv run pytest tests/`
  - **"Linting"**: `uv run ruff check src/ scripts/`
  - **"Reporting issues"**: GitHub Issues, include which scene and what's wrong

#### 6.4 — Update CI for full pipeline

- [ ] Update `.github/workflows/render.yml`:
  - Render all scenes (not just PropI)
  - Run tests before rendering
  - Run linting
  - Upload all outputs as artefacts
  - On tagged releases: attach outputs to the GitHub Release
- [ ] Add a separate lint-only workflow that runs on all PRs (faster feedback)
- [ ] Verify: a push to main triggers full render; a PR triggers lint + tests only

#### 6.5 — YouTube upload

- [ ] Create a YouTube channel (or use existing) — decide on channel name
- [ ] Create 4 playlists:
  - "Euclid's Definitions — Geometry for KS2/KS3"
  - "Euclid's Postulates — The Rules of Geometry"
  - "Ruler and Compass Constructions — KS3 Geometry"
  - "Angle Theorems — KS3 Geometry"
- [ ] For each MP4:
  - Title: e.g. "Euclid Def. X–XII: Right, Obtuse & Acute Angles | KS3 Geometry"
  - Description: one-line summary, Euclid reference, NC curriculum reference, link to Oak lesson, link to GitHub repo, CC-BY 4.0 notice
  - Tags: euclid, geometry, KS3, maths, national curriculum, byrne, animation
  - Thumbnail: the final-frame PNG
- [ ] Upload all videos and assign to playlists
- [ ] Add playlist links to the README

#### 6.6 — Blog post

- [ ] Write the blog post (Substack / personal site):
  - Hook: re-learning Euclid with kids → discovering it's in the NC → building animations
  - Section: Byrne's Euclid — history, design, the palette (embed palette card)
  - Section: The NC connection — show the KS3 programme of study, highlight the Euclid propositions
  - Section: ManimCE — what it is, quick code sample, the ByrneScene base class
  - Section: Oak National Academy API — how it connects, the manifest
  - Section: Results — embed 3–4 GIFs inline (PropI, DefAngleTypes, PropXI, PropXXXII)
  - Section: Working in the open — repo link, CC-BY licence, how to contribute
  - Section: What I'd do next — PropXLVII (Pythagorean theorem) as the v0.2 hero, Books II–VI, narration, Manim Slides, other curricula
  - Close: "These 2,300-year-old constructions are still worth learning. They're worth seeing in motion."
- [ ] Proofread
- [ ] Publish
- [ ] Share on LinkedIn (position as AI engineer / education / open source intersection)
- [ ] Share on Twitter/X
- [ ] Post to r/manim on Reddit

#### 6.7 — v0.1.0 release

- [ ] Ensure all tests pass
- [ ] Ensure CI renders all scenes cleanly
- [ ] Ensure `curriculum/curriculum_manifest.json` is up to date
- [ ] Tag `v0.1.0` on main
- [ ] CI creates GitHub Release with:
  - All GIFs, MP4s, PNGs as release assets
  - `curriculum_manifest.json` as release asset
  - Release notes summarising what's included (list of animations, curriculum coverage)
- [ ] Verify: release assets are downloadable

---

### Ongoing: Maintenance tasks (post-v0.1.0)

> Not part of the plan timeline, but documented so they're not forgotten.

- [ ] Monitor ManimCE releases — test with new versions, update lockfile
- [ ] Periodically re-run `fetch_oak_curriculum.py` to refresh cached data if Oak updates their curriculum
- [ ] Respond to GitHub Issues and PRs
- [ ] Consider adding animations for Propositions II, III, IV, V, VIII (next tier of Euclid)
- [ ] Consider KS4 extensions (circle theorems, trigonometry animations)
- [ ] Explore Manim Slides for classroom-interactive versions
- [ ] Explore automated YouTube upload via the YouTube Data API

---

## 13. Human involvement map

Not every task in this plan can or should be done by an AI agent. Some require Mat's judgment, taste, credentials, or physical access to platforms. This section makes that explicit so an AI agent knows when to proceed autonomously and when to pause and ask.

### Classification

Each task falls into one of three categories:

| Label | Meaning | AI agent should... |
|-------|---------|-------------------|
| 🤖 **Agent** | Fully automatable. No human judgment needed. | Execute without asking. |
| 🤝 **Collaborate** | Agent produces a draft or candidate; Mat reviews, adjusts, approves. | Do the work, then present for review before finalising. |
| 👤 **Mat only** | Requires Mat's credentials, accounts, taste, voice, or physical action. | Stop and hand off with clear instructions on what's needed. |

### Phase 0: Skeleton

| Task | Who | Why |
|------|-----|-----|
| 0.1 Repo init, uv setup, dependency installation | 🤖 Agent | Mechanical — follows the plan exactly |
| 0.2 Core style module (palette, ByrneScene) | 🤖 Agent | Defined in research.md — no ambiguity |
| 0.3 PropI scene implementation | 🤝 Collaborate | Agent writes the code; Mat reviews the rendered output for visual quality and "feel". The first scene sets the tone for everything — Mat needs to confirm it looks right. |
| 0.4 Render script | 🤖 Agent | Mechanical CLI wrapper |
| 0.5 Config files (.gitignore, manim.cfg, LICENSE) | 🤖 Agent | Boilerplate |
| 0.6 README (initial) | 🤝 Collaborate | Agent drafts; Mat reviews tone and wording. This is the public face of the project. |
| 0.7 CI workflow | 🤖 Agent | Standard GitHub Actions — no judgment calls |
| 0.7 Push to GitHub | 👤 Mat only | Requires Mat's GitHub credentials and a decision on repo visibility (public from day one, or private until M6). Mat creates the remote repo. |
| 0.8 Stub files | 🤖 Agent | Mechanical |
| 0.9 Download NC PDFs and write references/README.md | 🤖 Agent | The PDFs are publicly available OGL documents. The attribution text is formulaic. Agent downloads and writes the README. |

### Phase 1: Design system

| Task | Who | Why |
|------|-----|-----|
| 1.0 Verify Byrne palette | 👤 Mat only | Visual judgment — sample colours from c82.net, compare to research values, decide if they're right. Mat's eye for the "feel" of Byrne. |
| 1.1 ByrneScene helper methods | 🤖 Agent | API design follows the research spec |
| 1.2 Animation convenience methods | 🤖 Agent | Implementation follows the research spec |
| 1.3 Configurable output dimensions | 🤖 Agent | Mechanical config |
| 1.4 Geometry utility functions | 🤖 Agent | Pure maths — deterministic, testable |
| 1.5 Unit tests | 🤖 Agent | Test cases are specified in the plan |
| 1.6 Palette card scene | 🤝 Collaborate | Agent builds it; Mat reviews the rendered output. This is a visual design artefact — does it look like Byrne? |
| 1.7 Style guide document | 🤝 Collaborate | Agent drafts the document; Mat reviews and may adjust rules based on what he sees in the rendered palette card and PropI. Mat's design instinct matters here — the "Do / Don't" examples especially. |
| 1.8 Update CI | 🤖 Agent | Mechanical |

### Phase 2: Definitions & Postulates

| Task | Who | Why |
|------|-----|-----|
| 2.1–2.7 Implement each definition scene | 🤝 Collaborate | Agent writes the code for each scene. Mat reviews the rendered output of each. These are the visual heart of the project — pacing, composition, and colour assignment are aesthetic judgments. Expect 1–2 rounds of "that angle mark is too big" or "the timing is off on the transition". |
| 2.8–2.10 Implement each postulate scene | 🤝 Collaborate | Same pattern. These are simpler (~10s each) but Mat should confirm the visual approach. |
| 2.11 Consistency review | 👤 Mat only | Mat watches all 10 animations sequentially and flags inconsistencies. This is a holistic judgment that requires seeing them as a set, not individually. Agent can re-render and adjust based on Mat's notes. |
| 2.12 Update curriculum YAML | 🤖 Agent | Mechanical — populate entries from the research mapping tables. |

### Phase 3: Constructions

| Task | Who | Why |
|------|-----|-----|
| 3.1 PropI refactor | 🤖 Agent | Mechanical refactor to use new helpers |
| 3.2–3.3 Implement PropII and PropIII | 🤝 Collaborate | These are the most complex early propositions. PropII especially has many construction steps — Mat should review for clarity. Agent writes, Mat reviews. |
| 3.4–3.7 Implement PropIX–PropXII | 🤝 Collaborate | Same pattern as Phase 2 — agent writes, Mat reviews renders. Construction animations are more complex and have more opportunities for visual awkwardness (overlapping circles, cluttered construction lines). Mat's eye is needed. |
| 3.8 Consistency review | 👤 Mat only | Holistic visual review across the set |
| 3.9 Update curriculum YAML | 🤖 Agent | Mechanical |

### Phase 4: Angle theorems

| Task | Who | Why |
|------|-----|-----|
| 4.1–4.3 Implement theorem scenes | 🤝 Collaborate | Agent writes; Mat reviews |
| 4.4 Consistency review | 👤 Mat only | Holistic visual review |
| 4.5 Update curriculum YAML | 🤖 Agent | Mechanical |

### Phase 5: Curriculum integration

| Task | Who | Why |
|------|-----|-----|
| 5.1 Explore Oak API | 🤝 Collaborate | Agent makes the API calls and presents the results. Mat reviews the thread/unit/lesson slugs and confirms which ones are relevant. Mat has domain expertise from his Oak consultancy work — he knows the data model and can spot wrong mappings faster than an agent guessing from titles. |
| 5.2 Write fetch_oak_curriculum.py | 🤖 Agent | Mechanical script, once 5.1 has identified the target slugs |
| 5.3 Write euclid_to_oak.yaml | 🤝 Collaborate | Agent drafts initial entries based on NC programme of study and Oak API data. Mat reviews and corrects the curriculum mappings — this requires understanding of how the NC statements map to specific Euclid content. A wrong mapping here undermines the project's credibility with teachers. |
| 5.3 Spot-check against NC PDF | 👤 Mat only | Mat verifies 3–4 entries against the actual DfE programme of study. Agent can pull the PDF text, but the judgment "does this animation genuinely support this curriculum statement?" is Mat's. |
| 5.4 Write build_manifest.py | 🤖 Agent | Mechanical script |
| 5.5 Write curriculum_mapping.md | 🤝 Collaborate | Agent generates the table from the YAML; Mat reviews for accuracy and adds the introductory paragraph |
| 5.6 Commit cached data | 🤖 Agent | Mechanical (after Mat has reviewed the data in 5.1) |
| 5.* Provide OAK_API_KEY | 👤 Mat only | Mat supplies the API key via environment variable or `.env` file. Never committed, never shared with the agent's logs. |

### Phase 6: Polish and publish

| Task | Who | Why |
|------|-----|-----|
| 6.1 Rendering pipeline scripts | 🤖 Agent | Mechanical |
| 6.1 Final quality spot-check | 👤 Mat only | Mat watches 5 random outputs and confirms they're production quality |
| 6.2 README completion | 🤝 Collaborate | Agent drafts the full README. Mat reviews tone, wording, and the "What is this?" narrative. The README is a public-facing document that represents Mat — it needs his voice. |
| 6.3 CONTRIBUTING.md | 🤝 Collaborate | Agent drafts; Mat reviews. Less voice-critical than README, but Mat should confirm the contributor workflow is realistic. |
| 6.4 Update CI | 🤖 Agent | Mechanical |
| 6.5 YouTube: create channel / choose name | 👤 Mat only | Mat's Google account. Decision on channel name and branding. |
| 6.5 YouTube: write video titles and descriptions | 🤝 Collaborate | Agent drafts titles/descriptions following the template in the plan. Mat reviews and adjusts — these are SEO-facing and represent his public profile. |
| 6.5 YouTube: upload videos | 👤 Mat only | Requires Mat's YouTube account. Manual upload (or Mat runs a script with his credentials). |
| 6.5 YouTube: add playlist links to README | 🤖 Agent | Mechanical — Mat provides the URLs after uploading |
| 6.6 Blog post: write | 👤 Mat only | **This is Mat's blog post.** His voice, his narrative arc, his professional positioning. An agent can produce an outline or rough draft for Mat to rework, but the published piece must be Mat's writing. Mat's dry, understated style and his specific framing (AI engineer ↔ education ↔ open source) can't be delegated. |
| 6.6 Blog post: embed GIFs and code samples | 🤝 Collaborate | Agent prepares the embed markup and selects which GIFs to feature. Mat places them in the context of his prose. |
| 6.6 Blog post: proofread | 👤 Mat only | Final read-through is Mat's |
| 6.6 Blog post: publish | 👤 Mat only | Mat's Substack / site credentials |
| 6.6 Share on LinkedIn | 👤 Mat only | Mat's account, Mat's professional network. The framing of the LinkedIn post matters — it's about his positioning as a consultant. Agent can draft copy but Mat posts. |
| 6.6 Share on Twitter/X | 👤 Mat only | Mat's account |
| 6.6 Post to r/manim | 👤 Mat only | Mat's Reddit account, and tone matters — the Manim community has its own norms |
| 6.7 Tag release | 👤 Mat only | Requires push access to the repo (Mat's GitHub credentials) |
| 6.7 Write release notes | 🤝 Collaborate | Agent drafts; Mat reviews before the tag is created |

### Summary by category

| Category | Count | % of total |
|----------|-------|------------|
| 🤖 Agent (fully autonomous) | ~70 tasks | ~45% |
| 🤝 Collaborate (agent drafts, Mat reviews) | ~55 tasks | ~35% |
| 👤 Mat only (human required) | ~30 tasks | ~20% |

### Patterns

A few patterns emerge:

1. **All code implementation is 🤖 or 🤝.** The agent can write every line of Python. The 🤝 tasks are where the *rendered output* needs Mat's visual review, not the code itself.

2. **All platform access is 👤.** GitHub push, YouTube upload, Substack publish, LinkedIn post, Reddit post. The agent cannot hold credentials and should never be given them inline.

3. **All visual quality judgments are 🤝 or 👤.** The agent can render, but "does this look right?" is Mat's call. The design system (Phase 1) reduces the surface area of these judgments — once the style guide is locked, most visual decisions are constrained. But the holistic "watch all 10/7/3 as a set" reviews (2.11, 3.8, 4.4) require human eyes.

4. **The blog post is the most human-dependent artefact.** It's the only output where Mat is the primary author rather than a reviewer. Everything else, the agent leads and Mat steers.

5. **Curriculum mapping accuracy is a shared responsibility.** The agent can draft mappings from the NC text and Oak API data, but Mat's Oak consultancy experience and teaching background (qualified science teacher) make him the authority on whether a mapping is correct. A wrong mapping is worse than no mapping.

6. **The palette is the foundation.** Task 1.0 (palette verification) is 👤 Mat only and gates everything else in Phase 1. If the colours are wrong, every subsequent render is wrong. This should be the very first action after Phase 0 is green.

### Handoff protocol

When the agent reaches a 🤝 or 👤 task, it should:

1. **State clearly what it's produced** (e.g. "I've rendered DefAngleTypes — here's the GIF")
2. **State what it needs from Mat** (e.g. "Please review the timing of the obtuse→acute transition and confirm the angle arc radius looks right")
3. **Propose a default** where possible (e.g. "I've used 0.4 for the arc radius — increase to 0.5 if the arcs feel too small")
4. **Not block on other work** — if Mat hasn't reviewed DefAngleTypes yet, the agent can proceed to implement DefCircle and queue both for review together

## 14. Execution status

### Completed tasks

- [x] 0.1 — Repository initialisation
- [x] 0.2 — Core style module
- [x] 0.3 — First scene: Proposition I
- [x] 0.4 — Render script
- [x] 0.5 — Project configuration files
- [x] 0.6 — README (initial version)
- [x] 0.7 — Continuous integration workflow authored locally
- [x] 0.8 — Stub files for future phases
- [x] 0.9 — References and attribution
- [x] Phase 0 local deliverable verified: `uv run python scripts/render_one.py PropI` produces MP4, PNG, and GIF outputs via `scripts/render_one.py`
- [x] 1.1 — Expand `ByrneScene` helper methods
- [x] 1.2 — Animation convenience methods on `ByrneScene`
- [x] 1.5 — Unit tests (`tests/test_style.py`, `tests/test_utils.py`, `tests/test_rendering.py`)
- [x] 1.6 — Palette card scene
- [x] 1.7 — `docs/style_guide.md`
- [x] 1.8 — Update CI
- [x] 2.1–2.10 — Implement definition and postulate scene classes
- [x] 2.12 — Add definition and postulate entries to `curriculum/euclid_to_oak.yaml`
- [x] 3.1–3.7 — Implement construction scene classes
- [x] 3.9 — Add construction entries to `curriculum/euclid_to_oak.yaml`
- [x] 4.1–4.3 — Implement theorem scene classes
- [x] 4.5 — Add theorem entries to `curriculum/euclid_to_oak.yaml`
- [x] Smoke renders verified for `PaletteCard`, `DefAngleTypes`, `DefCircle`, `PostulateIII`, `PropI`, `PropII`, and `PropXXXII`
- [x] 5.1 — Live Oak API exploration completed with a working `OAK_OPEN_API_KEY`, including the current thread, unit, lesson, and summary payload shapes plus the relevant `geometry-and-measure` curriculum slugs
- [x] 5.2 — `scripts/fetch_oak_curriculum.py` refreshed for the live Oak payloads, including grouped unit and lesson normalisation, unit-to-thread derivation, and expanded cache outputs
- [x] 5.3 — `curriculum/euclid_to_oak.yaml` refreshed with live Oak lesson and thread slugs for all implemented scenes
- [x] 5.4 — `scripts/build_manifest.py` rebuilt `curriculum/curriculum_manifest.json` from the refreshed live Oak cache
- [x] 5.5 — `docs/curriculum_mapping.md` regenerated with live Oak lesson and thread links
- [x] Working Oak API key verified locally: authenticated fetch now succeeds against the live curriculum endpoints and refreshes the cached Oak geometry data
- [x] Phase 5 local deliverable verified: authenticated Oak fetch now caches 1 relevant geometry thread, 50 KS2 lessons, and 20 KS3 lessons, and the manifest plus mapping document rebuild cleanly
- [x] Synthetic curriculum preview added so the final Oak-enriched manifest, mapping, and showcase shape can be reviewed without live Oak auth
- [x] Stitched demo reel added for the synthetic preview so visitors can watch a single back-to-back sample without live Oak data
- [x] 6.1 — `scripts/render_all.py` and `scripts/gif_convert.sh` implemented; full low-quality MP4/PNG render pass and local GIF conversion completed successfully
- [x] 6.2 — README completed for public-facing use
- [x] 6.3 — `CONTRIBUTING.md`
- [x] 6.4 — CI expanded for full renders plus PR validation workflow

### Pending Mat-only review or later-phase follow-up

- [ ] 0.7 — Push to GitHub and verify CI green on the remote
- [ ] 1.0 — Verify Byrne palette against c82.net and confirm the visual feel
- [ ] 1.3 — Final square-output approach handled in the render pipeline phase via centre-crop GIF generation rather than scene-level frame resizing
- [ ] 2.11 — Phase 2 consistency review and high-quality render pass
- [ ] 3.8 — Phase 3 consistency review and high-quality render pass
- [ ] 4.4 — Phase 4 consistency review and high-quality render pass
- [ ] 5.6 — Commit the refreshed Oak cache data after review, if and when a VCS checkpoint is requested
- [ ] 6.1 — Mat final quality spot-check across rendered outputs
- [ ] 6.5 — YouTube upload and playlist curation
- [ ] 6.6 — Blog post drafting, review, and publication
- [ ] 6.7 — Tag and publish the `v0.1.0` release
