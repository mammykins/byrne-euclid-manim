# Research: Animating Euclid's Geometry with Manim in the Style of Byrne's Euclid

## 1. Project Vision

Create animated GIFs/videos of Euclid's Book I definitions and early propositions using ManimCE (Community Edition), styled with the visual language of Oliver Byrne's 1847 edition — bold primary colours replacing letter-labels, clean geometry, and a warm vintage background. The output is intended for a blog post exploring this tooling, framed around re-learning basic geometry with kids.

---

## 2. Oliver Byrne's Euclid — Background & Design Language

### 2.1 Historical Context

Oliver Byrne (1810–1880) was an Irish civil engineer and mathematician. In 1847, he published *The First Six Books of the Elements of Euclid in which Coloured Diagrams and Symbols are Used Instead of Letters for the Greater Ease of Learners* through William Pickering. It was one of the earliest multi-colour printed books, and a commercial failure at the time due to the extraordinary cost of chromolithographic printing (each page required multiple press passes, one per colour).

Byrne's innovation was **pedagogical**: instead of labelling angles and lines with letters (A, B, C), he used **colours** as identifiers. A red line in the diagram corresponded to a red line glyph inline in the proof text. This eliminated the constant eye-flicking between labelled diagram and symbolic text. Edward Tufte praised the approach in *Envisioning Information*. The work prefigures De Stijl and Bauhaus design aesthetics — Mondrian before Mondrian.

The book has experienced a major revival:
- **Taschen** published a facsimile edition (2010)
- **Nicholas Rougeux** (c82.net) created a complete, faithful online reproduction with interactive diagrams, clickable cross-references, and custom typography (2018). See: https://www.c82.net/euclid/
- **Sergey Slyusarev** (jemmybutton) created a MetaPost + LaTeX reproduction that can generate the entire book programmatically: https://github.com/jemmybutton/byrne-euclid — with a corresponding LaTeX package on CTAN (`byrne`)
- **Kronecker Wallis** produced a modern redesign extending to all 13 books

### 2.2 The Byrne Colour Palette

Byrne used exactly **four colours** plus two line styles and two line thicknesses:

| Element | Approximate Hex | Notes |
|---------|----------------|-------|
| Red | `#E6382D` | Primary lines/angles under consideration |
| Yellow | `#F0C824` | Secondary/constructed elements, angles |
| Blue | `#1A6FB5` | Tertiary elements, alternative lines |
| Black | `#2B2B2B` | Base lines, text, default strokes |
| Background | `#F5F0E1` | Warm cream/parchment (from c82.net reproduction) |

> **Note on exact values**: The precise hex codes vary across reproductions. The values above are sampled from the c82.net reproduction and the Taschen facsimile. The jemmybutton/byrne-latex package defines its own CMYK values tuned for print. For screen-based Manim output, the hex values above provide an excellent starting point. Tweak to taste — the key constraint is **four and only four** chromatic colours, all saturated primaries against a warm neutral ground.

Byrne's system:
- 4 colours × 2 line styles (solid, dashed) × 2 thicknesses = **16 visual options** for differentiating geometric elements
- Filled shapes use the same colours at full opacity
- Angles are shown as small coloured wedges/arcs

### 2.3 Typography

The original used **Caslon italic** for proposition text, with decorative four-line initials designed by Mary Byfield. Rougeux reproduced these as a custom web font for c82.net.

For Manim animations, the relevant design principle is: **keep text minimal, let the geometry and colour do the talking**. Any labels or titles should use a serif font (e.g., EB Garamond, Libre Caslon) to echo the period feel.

---

## 3. Euclid's Book I — Content to Animate

### 3.1 Definitions (candidates for animation)

The following definitions from Book I are the strongest candidates for visual animation:

| # | Definition | Animation Concept |
|---|-----------|-------------------|
| I | A *point* has no parts | Dot appearing, perhaps shrinking to demonstrate dimensionlessness |
| II | A *line* is length without breadth | Line being drawn, with breadth indicators disappearing |
| IV | A *straight line* lies evenly between its extremities | Contrast: curved vs straight paths between two points |
| VIII–IX | *Plane angle* / *rectilinear angle* | Two lines meeting; angle arc appearing |
| X | *Right angle* / perpendicular | Line standing on another, both angles shown equal |
| XI–XII | *Obtuse* and *acute* angles | Right angle → rotate one arm to show obtuse/acute |
| XV | *Circle* — equidistant from centre | Compass sweeping out a circle |
| XVII | *Diameter* | Line through centre, terminating on circumference |
| XXIV | *Equilateral triangle* | Three equal sides highlighted |
| XXV | *Isosceles triangle* | Two equal sides highlighted |
| XXVII | *Right-angled triangle* | Right angle marked |
| XXX | *Square* | All sides equal, all angles right |
| XXXI | *Rhombus* | All sides equal, angles not right |
| XXXV | *Parallel lines* | Two lines extended indefinitely, never meeting |

### 3.2 Postulates

| # | Postulate | Animation Concept |
|---|-----------|-------------------|
| I | Draw a straight line from any point to any other | Two points appear → line drawn between them |
| II | Produce a finite line to any length | Line extends/grows from endpoint |
| III | Describe a circle with any centre and radius | Point → radius line → circle swept out |

### 3.3 Propositions (early, visual ones)

| # | Proposition | Animation Concept |
|---|-----------|-------------------|
| I | Construct equilateral triangle on a line | **Classic**: two circles, intersection point, triangle drawn. This is Byrne's most iconic page. |
| II | From a given point, draw a line equal to a given line | Construction sequence with auxiliary circles |
| IX | Bisect a rectilinear angle | Construction with equal segments and equilateral triangle |
| X | Bisect a finite straight line | Equilateral triangle + angle bisector |
| XI | Draw a perpendicular from a point on a line | Construction sequence |
| XLVII | Pythagorean theorem | The visual showpiece — squares on each side |

**Recommended starting set**: Definitions I, IV, X–XII, XV; Postulates I–III; Proposition I.

---

## 4. Manim Community Edition (ManimCE) — Technical Reference

### 4.1 Overview

- **Repo**: https://github.com/ManimCommunity/manim/ (36.8k stars)
- **Docs**: https://docs.manim.community/
- **License**: MIT
- **Python**: 3.9+ (project targets 3.10+)
- **Dependencies**: FFmpeg, a LaTeX distribution (optional, for `Tex`/`MathTex`), Cairo
- **Package manager**: Uses `uv` for development; install via `pip install manim` or `uv add manim`

ManimCE is the community fork of 3b1b's personal `manimgl`. It is more stable, better documented, and actively maintained. Grant Sanderson recommends it for beginners.

### 4.2 Installation

```bash
# Using uv (Mat's preference)
uv init byrne-euclid-manim
cd byrne-euclid-manim
uv add manim

# System dependencies (Ubuntu/Debian)
sudo apt install ffmpeg libcairo2-dev libpango1.0-dev

# Optional: LaTeX for Tex/MathTex objects
sudo apt install texlive-full  # or texlive-latex-extra for lighter install
```

### 4.3 Core Concepts

**Scene**: The top-level container. Each animation is a class inheriting from `Scene` with a `construct(self)` method.

**Mobject** (Mathematical Object): Everything on screen — shapes, text, groups. Most geometry is `VMobject` (vectorised).

**Animation**: Transformations applied via `self.play()`. Key animations:
- `Create(mobject)` — draws the object
- `FadeIn(mobject)` / `FadeOut(mobject)`
- `Transform(source, target)` — morphs one shape into another
- `Write(text_mobject)` — handwriting effect for text
- `GrowFromCenter(mobject)`
- `Indicate(mobject)` — brief highlight/pulse
- `DrawBorderThenFill(mobject)` — outline then fill (great for Byrne style)

**Positioning**:
- `.shift(direction)`, `.move_to(point)`, `.next_to(mobject, direction)`
- Constants: `UP`, `DOWN`, `LEFT`, `RIGHT`, `ORIGIN`, `UL`, `UR`, `DL`, `DR`
- Coordinate system: centre of screen is origin, positive y is up

### 4.4 Geometry Primitives

All available in `manim.mobject.geometry`:

```python
from manim import *

# Basic shapes
Point()                          # a dot
Dot(point=ORIGIN, radius=0.08)
Line(start, end)
DashedLine(start, end)
Arrow(start, end)
Circle(radius=1.0)
Arc(radius, start_angle, angle)
Angle(line1, line2, radius=0.5)  # angle arc between two lines
Square(side_length=2.0)
Rectangle(width, height)
Triangle()                       # equilateral by default
Polygon(*vertices)               # arbitrary polygon
RegularPolygon(n=6)

# Styling (VMobject methods)
shape.set_color(color)
shape.set_fill(color, opacity=0.5)
shape.set_stroke(color, width=4)
shape.set_stroke(color, width=2, opacity=0.5)  # for dashed/lighter
```

### 4.5 Custom Colour Configuration

Manim accepts hex strings directly for colours:

```python
# Byrne palette
BYRNE_RED    = "#E6382D"
BYRNE_YELLOW = "#F0C824"
BYRNE_BLUE   = "#1A6FB5"
BYRNE_BLACK  = "#2B2B2B"
BYRNE_BG     = "#F5F0E1"

class ByrneScene(Scene):
    def construct(self):
        self.camera.background_color = BYRNE_BG
        
        line = Line(LEFT * 3, RIGHT * 3, color=BYRNE_BLACK, stroke_width=4)
        circle = Circle(radius=1.5, color=BYRNE_RED, stroke_width=3)
        triangle = Polygon(
            [-1, -1, 0], [1, -1, 0], [0, 0.73, 0],
            color=BYRNE_BLUE,
            fill_color=BYRNE_BLUE,
            fill_opacity=0.3,
            stroke_width=3
        )
```

Manim also ships with named colour modules (BS381, X11, XKCD etc.) but custom hex is simplest here.

### 4.6 Output Formats

```bash
# MP4 (default)
manim -pql scene.py SceneName            # low quality, preview
manim -pqh scene.py SceneName            # high quality (1080p 60fps)

# GIF
manim --format gif -ql scene.py SceneName
# or use -i flag (deprecated but works)

# PNG (last frame only)
manim -s scene.py SceneName

# Transparent background
manim -t --format gif scene.py SceneName  # GIF with alpha

# Quality presets
# -ql: 854×480 @ 15fps  (fast iteration)
# -qm: 1280×720 @ 30fps
# -qh: 1920×1080 @ 60fps
# -qp: 2560×1440 @ 60fps
# -qk: 3840×2160 @ 60fps
```

Programmatic config:
```python
from manim import *
config.background_color = "#F5F0E1"
config.frame_rate = 30
config.format = "gif"  # or "mp4"
config.pixel_width = 1080
config.pixel_height = 1080  # square for social media
```

### 4.7 Useful Techniques for This Project

**Angle marking**:
```python
line1 = Line(ORIGIN, RIGHT * 2)
line2 = Line(ORIGIN, UP * 2)
angle = Angle(line1, line2, radius=0.5, color=BYRNE_YELLOW, fill_opacity=0.5)
```

**Compass sweep (circle construction)**:
```python
arc = Arc(radius=2, start_angle=0, angle=TAU, color=BYRNE_RED)
self.play(Create(arc), run_time=2)
```

**Drawing with `DrawBorderThenFill`** (mimics Byrne's filled shapes):
```python
sq = Square(color=BYRNE_RED, fill_color=BYRNE_RED, fill_opacity=0.4)
self.play(DrawBorderThenFill(sq))
```

**Grouping**:
```python
diagram = VGroup(line1, line2, circle, triangle)
diagram.scale(0.8).move_to(ORIGIN)
```

**Labels** (minimal, Byrne-style):
```python
label = Text("I.", font="EB Garamond", font_size=36, color=BYRNE_BLACK)
label.to_corner(UL)
```

**Updaters** (for interactive-feeling animations):
```python
theta = ValueTracker(0)
line.add_updater(lambda m: m.set_angle(theta.get_value()))
self.play(theta.animate.set_value(PI/2))
```

---

## 5. Existing Prior Art

### 5.1 manim-euclid-elements (osolmaz)

**Repo**: https://github.com/osolmaz/manim-euclid-elements

A video rendering of all of Euclid's Elements using Manim. Animations are auto-generated from machine-readable source data (from Ibrahim Sagiroglu's browser-based interactive rendering). This is the closest existing project to what we're building, but it uses **standard 3b1b-style** colouring (dark background, neon colours) rather than Byrne's palette.

**Key takeaway**: The geometry data and construction sequences are available in machine-readable form. We don't need to manually compute coordinates — we can focus on **styling**.

### 5.2 jemmybutton/byrne-euclid

**Repo**: https://github.com/jemmybutton/byrne-euclid (1.3k stars)

MetaPost + LaTeX reproduction of Byrne's full six books. Not animated, but the **definitive open-source reference** for Byrne's visual style. The associated `byrne` LaTeX package (on CTAN) provides MetaPost macros for Byrne-style diagrams. Key features:
- Procedurally generated initials and vignettes (no two identical)
- Optional letter-label overlay (as suggested by Tufte)
- Both English and Russian editions

### 5.3 c82.net/euclid (Nicholas Rougeux)

**URL**: https://www.c82.net/euclid/

Complete online reproduction with interactive SVG diagrams, clickable shape references in proof text, custom Caslon typography, and decorative initial font. The **gold standard** for visual fidelity to Byrne's original. Rougeux documented the creation process in detail, including the palette development and diagram-tracing workflow.

### 5.4 Math-To-Manim (HarleyCoops)

A multi-pipeline tool for generating Manim animations from natural language descriptions. Uses Claude, Gemini, or Kimi K2.5 as backend. Interesting for automation but not Byrne-styled.

### 5.5 manim-geometry-visualizer (arch571)

A DSL-based geometry visualiser for school curriculum problems. Uses Manim for rendering. Proof of concept — interesting architecture idea (declare geometry in a simple text format, auto-generate animation).

---

## 6. Design Decisions for the Blog Post Project

### 6.1 Visual Style Guide

1. **Background**: Warm cream (`#F5F0E1`) — NOT the default Manim black or white
2. **Palette**: Strict Byrne four-colour (red/yellow/blue/black). No gradients, no other colours
3. **Stroke width**: Thick (4–6px) for primary elements, thin (2px) for construction lines
4. **Dashed lines**: Use `DashedLine` for construction/auxiliary lines
5. **Fill opacity**: 0.3–0.5 for filled regions (triangles, squares, angle sectors)
6. **Angle arcs**: Small coloured wedges, filled with the angle's designated colour
7. **Text**: Minimal. Title/definition number only. Serif font (EB Garamond or similar)
8. **No axes, no grids**: Pure geometry on a blank field
9. **Aspect ratio**: Square (1:1) for social media embeddability, or 16:9 for blog

### 6.2 Animation Style

- **Deliberate pacing**: Slower than typical 3b1b. Each construction step should breathe.
- **Construction order**: Follow Euclid's actual construction sequence (compass, straightedge)
- **Build-up**: `Create` for lines, `DrawBorderThenFill` for filled shapes, `FadeIn` for labels
- **Emphasis**: `Indicate` or brief colour pulse when a key relationship is established
- **Looping**: For GIFs, consider making them loop cleanly (final state = initial state, or natural endpoint)

### 6.3 Project Structure

```
byrne-euclid-manim/
├── pyproject.toml
├── src/
│   ├── byrne_style.py          # Colour palette, base scene class, helper functions
│   ├── definitions.py          # Scenes for Book I definitions
│   ├── postulates.py           # Scenes for postulates
│   ├── propositions.py         # Scenes for propositions (starting with Prop I)
│   └── utils.py                # Geometry construction helpers
├── output/                     # Rendered GIFs and MP4s
├── manim.cfg                   # Project-level Manim config
└── README.md
```

### 6.4 Base Scene Class

```python
"""byrne_style.py — Byrne's Euclid visual style for Manim"""
from manim import *

# Byrne palette
BYRNE_RED    = "#E6382D"
BYRNE_YELLOW = "#F0C824"
BYRNE_BLUE   = "#1A6FB5"
BYRNE_BLACK  = "#2B2B2B"
BYRNE_BG     = "#F5F0E1"

# Line styles
BYRNE_THICK = 5
BYRNE_THIN  = 2.5
BYRNE_DASH_LENGTH = 0.15   # dash segment length for DashedLine
BYRNE_DASH_RATIO  = 0.5    # ratio of dash to gap

class ByrneScene(Scene):
    """Base scene with Byrne's warm background and square aspect."""
    
    def setup(self):
        self.camera.background_color = BYRNE_BG
    
    def byrne_line(self, start, end, color=BYRNE_BLACK, thick=True):
        return Line(
            start, end,
            color=color,
            stroke_width=BYRNE_THICK if thick else BYRNE_THIN
        )
    
    def byrne_circle(self, center, radius, color=BYRNE_RED):
        return Circle(
            radius=radius,
            color=color,
            stroke_width=BYRNE_THIN
        ).move_to(center)
    
    def byrne_angle(self, line1, line2, color=BYRNE_YELLOW, radius=0.4):
        return Angle(
            line1, line2,
            radius=radius,
            color=color,
            fill_opacity=0.5,
            stroke_width=BYRNE_THIN
        )
    
    def byrne_title(self, text, position=UL):
        return Text(
            text,
            font_size=32,
            color=BYRNE_BLACK,
            # font="EB Garamond"  # uncomment if font is installed
        ).to_corner(position, buff=0.5)
```

---

## 7. Starter Animation: Proposition I (Equilateral Triangle)

This is the most iconic construction in Byrne's edition and the ideal first animation.

**Construction**:
1. Given line AB (black)
2. With centre A, radius AB, describe circle (blue)
3. With centre B, radius BA, describe circle (red)
4. From intersection point C, draw CA (yellow) and CB (red)
5. Triangle ABC is equilateral

```python
class PropositionI(ByrneScene):
    """On a given finite straight line, describe an equilateral triangle."""
    
    def construct(self):
        # Title
        title = self.byrne_title("Proposition I.")
        self.play(Write(title))
        self.wait(0.5)
        
        # Given line AB
        A = LEFT * 1.5
        B = RIGHT * 1.5
        line_ab = self.byrne_line(A, B)
        dot_a = Dot(A, color=BYRNE_BLACK, radius=0.06)
        dot_b = Dot(B, color=BYRNE_BLACK, radius=0.06)
        
        self.play(Create(line_ab), FadeIn(dot_a), FadeIn(dot_b))
        self.wait(0.5)
        
        # Circle centred on A with radius AB
        radius = np.linalg.norm(B - A)
        circle_a = self.byrne_circle(A, radius, BYRNE_BLUE)
        self.play(Create(circle_a), run_time=1.5)
        self.wait(0.3)
        
        # Circle centred on B with radius BA
        circle_b = self.byrne_circle(B, radius, BYRNE_RED)
        self.play(Create(circle_b), run_time=1.5)
        self.wait(0.3)
        
        # Intersection point C (upper)
        # For equilateral triangle: C is at midpoint + height up
        mid = (A + B) / 2
        height = np.sqrt(3) / 2 * radius
        C = mid + UP * height
        dot_c = Dot(C, color=BYRNE_BLACK, radius=0.06)
        self.play(FadeIn(dot_c))
        self.wait(0.3)
        
        # Draw CA and CB
        line_ca = self.byrne_line(C, A, BYRNE_YELLOW)
        line_cb = self.byrne_line(C, B, BYRNE_RED)
        self.play(Create(line_ca), Create(line_cb), run_time=1.5)
        self.wait(0.5)
        
        # Fill triangle
        triangle = Polygon(
            A, B, C,
            fill_color=BYRNE_YELLOW,
            fill_opacity=0.15,
            stroke_width=0
        )
        self.play(FadeIn(triangle))
        self.wait(1)
        
        # Fade construction circles
        self.play(
            circle_a.animate.set_opacity(0.2),
            circle_b.animate.set_opacity(0.2),
            run_time=1
        )
        self.wait(2)
```

---

## 8. Technical Gotchas & Tips

### 8.1 Coordinate System
- Manim's default frame is roughly 14.2 units wide × 8 units tall (for 16:9)
- For square output, set `config.pixel_width = config.pixel_height = 1080`
- Frame dimensions change with aspect ratio — use `config.frame_width` and `config.frame_height`

### 8.2 Font Installation
- Manim uses system fonts for `Text()` objects and LaTeX for `Tex()`/`MathTex()`
- Install EB Garamond or Libre Caslon via system font manager or fontconfig
- For the long-s (ſ) used in Byrne's original text, this is Unicode character U+017F — just include it directly in strings

### 8.3 GIF Quality
- `--format gif` uses Pillow by default; quality can be mediocre
- For higher quality: render as MP4 then convert with `ffmpeg -i input.mp4 -vf "fps=15,scale=540:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif`
- For blog posts, consider using MP4 with `<video autoplay loop muted>` instead of GIF

### 8.4 LaTeX for Mathematical Text
- If using `Tex()` or `MathTex()`, need a LaTeX installation
- For simple labels like "I." or "Definition X", `Text()` is lighter weight
- Byrne used minimal text anyway — lean into this

### 8.5 Rendering Performance
- `-ql` (480p 15fps) for rapid iteration
- `-qm` (720p 30fps) for draft review
- `-qh` (1080p 60fps) for final output
- Each `self.play()` call generates a partial movie file; these are concatenated at the end

### 8.6 Caching
- Manim caches rendered animations in `media/` directory
- Use `--flush_cache` or delete `media/` to force re-render
- Useful when tweaking colours or timing

---

## 9. Blog Post Structure

> **Note**: This section was written before the curriculum pivot. See §13.6 for the updated blog post structure that frames the project around the UK national curriculum and teacher utility. The structure below is superseded.

The updated framing (§13.6) positions the project as: *"I've been re-learning Euclid's geometry with my kids — and I realised these 2,300-year-old constructions are still in the English national curriculum. So I built animated versions for teachers."*

---

## 10. Sources, Licences, and What the Repo Should Contain

### 10.1 Source audit

The project draws on several categories of source material. Each has different copyright status and different implications for what we store, link to, or reproduce.

#### Primary source: Byrne's Euclid (1847)

| Item | Status | Evidence |
|------|--------|----------|
| Text of Byrne's 1847 edition | **Public domain (CC0)** | Author died 1880; Smithsonian Digital Library confirms CC0: https://library.si.edu/digital-library/book/firstsixbooksel00byrn |
| Original page scans | **Public domain** | Available on Internet Archive: https://archive.org/details/firstsixbooksofe00byrn and via Getty Research Institute |
| Colour palette (red/yellow/blue/black scheme) | **Not copyrightable** | Colour choices are functional/factual — no copyright attaches to a palette |

The Euclid text reproduced in our Appendix (§11, §12) is taken from Byrne's 1847 edition, which is public domain. No copyright concern.

#### Secondary source: Nicholas Rougeux's c82.net reproduction (2018)

| Item | Status | Source |
|------|--------|-------|
| Diagrams and content | **CC BY-SA 4.0** | https://www.c82.net/euclid/about/ |
| Posters and website design | **© Nicholas Rougeux** | Not freely reusable |
| Byfield initial font | **CC0 (public domain)** | Created by Rougeux as a reproduction of the 1847 originals |

**Implication**: We can reference the c82.net diagrams for visual inspiration and link to them, but we should **not** copy SVG assets or CSS from the site. Our Manim animations are original works inspired by Byrne's (public domain) design system, not reproductions of Rougeux's (CC BY-SA) work. This distinction matters.

#### Secondary source: jemmybutton/byrne-euclid

| Item | Status | Source |
|------|--------|-------|
| byrne-euclid repo (MetaPost + LaTeX book) | **CC BY-SA 4.0** (book), **GPL-3.0** (code) | https://github.com/jemmybutton/byrne-euclid |
| byrne LaTeX package (byrne.sty, byrne.mp) | **GPL-3.0** | https://github.com/jemmybutton/byrne-latex |

**Implication**: We are not using any GPL code. Our Manim scenes are original Python. We reference this project for research only. The GPL-3.0 licence on the MetaPost library would only matter if we copied that code, which we don't.

#### Tool: ManimCE

| Item | Status | Source |
|------|--------|-------|
| ManimCE library | **MIT** | https://github.com/ManimCommunity/manim/ |

**Implication**: No restrictions. MIT is compatible with everything. Attribution required (include in credits).

#### Prior art: manim-euclid-elements

| Item | Status | Source |
|------|--------|-------|
| osolmaz/manim-euclid-elements | **No explicit licence visible** | https://github.com/osolmaz/manim-euclid-elements |

**Implication**: We reference this for research but do not use any of its code. We should note its existence as prior art and credit it.

#### Curriculum sources

| Item | Status | Source |
|------|--------|-------|
| NC Mathematics Programme of Study: KS1 & KS2 (DFE-00180-2013) | **OGL v3.0**, Crown copyright 2013 | https://assets.publishing.service.gov.uk/media/5a7da548ed915d2ac884cb07/PRIMARY_national_curriculum_-_Mathematics_220714.pdf |
| NC Mathematics Programme of Study: KS3 (DFE-00179-2013) | **OGL v3.0**, Crown copyright 2013 | https://assets.publishing.service.gov.uk/media/5a7c1408e5274a1f5cc75a68/SECONDARY_national_curriculum_-_Mathematics.pdf |
| NC Mathematics Programme of Study: KS4 (DFE-00496-2014) | **OGL v3.0**, Crown copyright 2014 | https://assets.publishing.service.gov.uk/media/5a7dc9dced915d2ac884d8ef/KS4_maths_PoS_FINAL_170714.pdf |
| NC Mathematics PoS: HTML version (updated Jan 2021) | **OGL v3.0** | https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study |
| Oak National Academy API data | **OGL** | https://open-api.thenational.academy/ |

**Implication**: OGL permits free reuse with attribution. When we quote curriculum statements in the manifest or documentation, we must include: *"Contains public sector information licensed under the Open Government Licence v3.0"* and *"Oak National Academy content used under the Open Government Licence."*

#### Other references cited in the research

| Reference | Full citation | Used for |
|-----------|--------------|----------|
| Tufte, *Envisioning Information* | Tufte, E.R. (1990). *Envisioning Information*. Graphics Press, Cheshire, CT. | Claim that Tufte praised Byrne's edition |
| Hawes & Kolpas, "The Matisse of Mathematics" | Hawes, S.M. & Kolpas, S.J. (2015). "Oliver Byrne: The Matisse of Mathematics." *Convergence*, 12. MAA. https://old.maa.org/press/periodicals/convergence/oliver-byrne-the-matisse-of-mathematics | Biographical detail on Byrne |
| Public Domain Review entry | "The First Six Books of The Elements of Euclid (1847)." *The Public Domain Review*. https://publicdomainreview.org/collection/the-first-six-books-of-the-elements-of-euclid-1847/ | Historical context |
| UBC Mathematics scan | Casselman, B. "Oliver Byrne's edition of Euclid." UBC Mathematics. https://www.math.ubc.ca/~cass/Euclid/byrne.html | Alternative scan of the original |

### 10.2 What the repo should contain

The question is whether to **store copies** of source materials or **link to them**. Here's the recommendation:

#### Store in the repo (under `references/`)

| File | Why store it | Licence |
|------|-------------|---------|
| `references/NC_KS1_KS2_Mathematics.pdf` | The DfE PDF is the canonical source for our curriculum mapping. It could move or change URL. A local copy ensures the mapping is verifiable. | OGL v3.0 — free to redistribute with attribution |
| `references/NC_KS3_Mathematics.pdf` | Same reasoning. This is the single most important source for the project — the KS3 geometry content is what we're animating. | OGL v3.0 |
| `references/NC_KS4_Mathematics.pdf` | Completeness. Less immediately relevant but useful for KS4 extension scope. | OGL v3.0 |
| `references/README.md` | Attribution notices for all stored files. OGL attribution text. Credit to upstream projects. | — |

#### Link to, do not store

| Resource | Why link only |
|----------|--------------|
| Byrne's 1847 original (Internet Archive PDF, 121MB+) | Too large for a git repo. Public domain and stably hosted on archive.org. Link is sufficient. |
| c82.net reproduction | It's a website, not a file. CC BY-SA 4.0 diagrams — we reference for inspiration, not reproduction. |
| jemmybutton/byrne-euclid repo | It's a git repo. Link to it. |
| ManimCE docs | Website. Link. |
| Oak API responses | We already cache the relevant subset in `curriculum/`. No need to store the full API. |
| Tufte's *Envisioning Information* | Copyrighted book. Cite, don't store. |
| Hawes & Kolpas MAA article | Link to the freely available MAA page. |

#### Do not store or reproduce

| Resource | Why not |
|----------|---------|
| c82.net SVG diagrams or CSS | © Rougeux (website design) or CC BY-SA (diagrams) — we create our own visuals in Manim |
| byrne-euclid MetaPost code | GPL-3.0 — licence incompatible with our MIT repo if we were to include it; and we don't need it |
| Scan pages from the 1847 original | Public domain but large and unnecessary — we recreate the visual style, not reproduce the pages |

### 10.3 Repo structure update

Add a `references/` directory to the repo structure:

```
byrne-euclid-manim/
├── references/
│   ├── README.md                            # Attribution notices, OGL text, links to sources
│   ├── NC_KS1_KS2_Mathematics.pdf           # DfE, Crown copyright 2013, OGL v3.0
│   ├── NC_KS3_Mathematics.pdf               # DfE, Crown copyright 2013, OGL v3.0
│   └── NC_KS4_Mathematics.pdf               # DfE, Crown copyright 2014, OGL v3.0
├── ...
```

The `references/README.md` should contain:

1. Full OGL v3.0 attribution statement
2. A table listing every source the project depends on, with URL, licence, and how we use it
3. Links to the primary sources we don't store (Byrne's 1847 original, c82.net, etc.)
4. A clear statement that our animations are **original works** — they are inspired by Byrne's public domain design system, not reproductions of any copyrighted work

### 10.4 Key resources (URLs only)

| Resource | URL |
|----------|-----|
| **Byrne's Euclid** | |
| Original 1847 edition (Internet Archive) | https://archive.org/details/firstsixbooksofe00byrn |
| Original 1847 edition (Smithsonian, CC0) | https://library.si.edu/digital-library/book/firstsixbooksel00byrn |
| c82.net interactive reproduction | https://www.c82.net/euclid/ |
| c82.net Book I | https://www.c82.net/euclid/book1/ |
| Making of c82 Byrne's Euclid | https://www.c82.net/blog/?id=79 |
| byrne-euclid (MetaPost/LaTeX) | https://github.com/jemmybutton/byrne-euclid |
| byrne LaTeX package (CTAN) | https://ctan.org/pkg/byrne |
| byrne-latex source | https://github.com/jemmybutton/byrne-latex |
| Public Domain Review entry | https://publicdomainreview.org/collection/the-first-six-books-of-the-elements-of-euclid-1847/ |
| UBC Mathematics scan | https://www.math.ubc.ca/~cass/Euclid/byrne.html |
| Wikipedia: Oliver Byrne | https://en.wikipedia.org/wiki/Oliver_Byrne_(mathematician) |
| Kronecker Wallis article | https://www.kroneckerwallis.com/oliver-byrnes-colorful-euclid-when-victorian-design-met-ancient-geometry/ |
| Hawes & Kolpas, "The Matisse of Mathematics" | https://old.maa.org/press/periodicals/convergence/oliver-byrne-the-matisse-of-mathematics |
| **Manim** | |
| ManimCE GitHub | https://github.com/ManimCommunity/manim/ |
| ManimCE Docs | https://docs.manim.community/ |
| ManimCE Example Gallery | https://docs.manim.community/en/stable/examples.html |
| Manim Output Settings | https://docs.manim.community/en/stable/tutorials/output_and_config.html |
| Manim Geometry Module | https://docs.manim.community/en/stable/reference/manim.mobject.geometry.html |
| Manim Color Reference | https://docs.manim.community/en/stable/reference/manim.utils.color.html |
| manim-euclid-elements (prior art) | https://github.com/osolmaz/manim-euclid-elements |
| **UK National Curriculum** | |
| NC Maths PoS: KS1 & KS2 (PDF, OGL v3.0) | https://assets.publishing.service.gov.uk/media/5a7da548ed915d2ac884cb07/PRIMARY_national_curriculum_-_Mathematics_220714.pdf |
| NC Maths PoS: KS3 (PDF, OGL v3.0) | https://assets.publishing.service.gov.uk/media/5a7c1408e5274a1f5cc75a68/SECONDARY_national_curriculum_-_Mathematics.pdf |
| NC Maths PoS: KS4 (PDF, OGL v3.0) | https://assets.publishing.service.gov.uk/media/5a7dc9dced915d2ac884d8ef/KS4_maths_PoS_FINAL_170714.pdf |
| NC Maths PoS: HTML version (GOV.UK) | https://www.gov.uk/government/publications/national-curriculum-in-england-mathematics-programmes-of-study |
| Oak National Academy API | https://open-api.thenational.academy/ |
| Oak API Documentation | https://open-api.thenational.academy/docs |
| **Other references** | |
| Tufte, E.R. (1990). *Envisioning Information* | No URL — physical book. Graphics Press, Cheshire, CT. |

---

## 11. Appendix: Book I Definitions (Full Text from Euclid/Byrne)

For reference when writing animation code:

1. A **point** is that which has no parts.
2. A **line** is length without breadth.
3. The extremities of a line are points.
4. A **straight line** is that which lies evenly between its extremities.
5. A **surface** is that which has length and breadth only.
6. The extremities of a surface are lines.
7. A **plane surface** is that which lies evenly between its extremities.
8. A **plane angle** is the inclination of two lines to one another, in a plane, which meet together, but are not in the same direction.
9. A **plane rectilinear angle** is the inclination of two straight lines to one another, which meet together, but are not in the same straight line.
10. When one straight line standing on another makes the adjacent angles equal, each is called a **right angle**, and each line is said to be **perpendicular** to the other.
11. An **obtuse angle** is an angle greater than a right angle.
12. An **acute angle** is less than a right angle.
13. A **term** or **boundary** is the extremity of any thing.
14. A **figure** is a surface enclosed on all sides by a line or lines.
15. A **circle** is a plane figure bounded by one continued line (circumference), having a point within it from which all straight lines drawn to its circumference are equal.
16. This point is called the **centre** of the circle.
17. A **diameter** is a straight line drawn through the centre, terminated both ways in the circumference.
18. A **semicircle** is the figure contained by the diameter and the part of the circle cut off by the diameter.
19. A **segment** of a circle is a figure contained by a straight line and the part of the circumference which it cuts off.
20. A figure contained by straight lines only is called a **rectilinear figure**.
21. A **triangle** is a rectilinear figure included by three sides.
22. A **quadrilateral** figure is one bounded by four sides.
23. A **polygon** is a rectilinear figure bounded by more than four sides.
24. An **equilateral triangle** has three sides equal.
25. An **isosceles triangle** has only two sides equal.
26. A **scalene triangle** has no two sides equal.
27. A **right-angled triangle** has a right angle.
28. An **obtuse-angled triangle** has an obtuse angle.
29. An **acute-angled triangle** has three acute angles.
30. A **square** has all sides equal and all angles right angles.
31. A **rhombus** has all sides equal but angles not right.
32. An **oblong** (rectangle) has all angles right but not all sides equal.
33. A **rhomboid** has opposite sides equal but sides not all equal nor angles right.
34. All other quadrilateral figures are **trapeziums**.
35. **Parallel** straight lines are in the same plane and, produced continually in both directions, never meet.

---

## 12. Appendix: Postulates and Axioms

### Postulates
1. A straight line may be drawn from any one point to any other point.
2. A finite straight line may be produced to any length.
3. A circle may be described with any centre at any distance from that centre.

### Axioms
1. Things equal to the same thing are equal to each other.
2. If equals be added to equals, the sums are equal.
3. If equals be taken from equals, the remainders are equal.
4. If equals be added to unequals, the sums are unequal.
5. If equals be taken from unequals, the remainders are unequal.
6. Doubles of the same are equal.
7. Halves of the same are equal.
8. Things which coincide with one another are equal.
9. The whole is greater than its part.
10. Two straight lines cannot enclose a space.
11. All right angles are equal.
12. *(Parallel postulate)* If two straight lines meet a third so that the interior angles on one side are less than two right angles, the lines will meet on that side if produced.

---

## 13. UK National Curriculum — Geometry in Maths & Where Animations Fit

### 13.1 Curriculum Structure

The English National Curriculum for Mathematics is organised by Key Stage:

| Key Stage | Years | Ages | Phase |
|-----------|-------|------|-------|
| KS1 | 1–2 | 5–7 | Primary |
| KS2 | 3–6 | 7–11 | Primary |
| KS3 | 7–9 | 11–14 | Secondary |
| KS4 | 10–11 | 14–16 | Secondary (GCSE) |

Geometry appears under **"Geometry — properties of shapes"** (KS1/KS2) and **"Geometry and measures"** (KS3/KS4). The content is cumulative — each key stage builds on the previous one. Euclidean constructions and deductive reasoning peak at KS3, making it the sweet spot for Byrne-style animations.

### 13.2 Geometry Curriculum by Key Stage — Mapped to Euclid

#### KS1 (Years 1–2): Foundations

**Curriculum content**: Recognise and name common 2D shapes (rectangles, circles, triangles); recognise and name common 3D shapes; describe position, direction and movement including quarter, half, three-quarter and full turns.

**Euclid connection**: Very limited — but Def. I (point), Def. II (line), Def. XV (circle) and Postulate III (drawing a circle) could work as gentle introductions. Animations could show "what is a point?", "what is a line?", "what is a circle?" at a very basic level.

| Animation | Euclid Reference | NC Statement |
|-----------|-----------------|--------------|
| What is a point? | Def. I | Recognise basic geometric concepts |
| What is a line? | Def. II, IV | Draw lines using a straight edge |
| What is a circle? | Def. XV, XVI | Recognise and name circles |

#### KS2 (Years 3–6): Properties and Classification

**Year 3**: Recognise angles as a property of shape or a description of a turn; identify right angles; identify horizontal, vertical, perpendicular and parallel lines.

**Year 4**: Compare and classify geometric shapes including quadrilaterals and triangles based on their properties and sizes; identify acute and obtuse angles; identify lines of symmetry.

**Year 5**: Know angles are measured in degrees; identify angles at a point, on a straight line, and vertically opposite angles; use properties of rectangles to deduce related facts; distinguish between regular and irregular polygons.

**Year 6**: Draw 2D shapes using given dimensions and angles; compare and classify geometric shapes based on properties; find unknown angles in triangles, quadrilaterals and regular polygons; illustrate and name parts of circles (radius, diameter, circumference); recognise angles where they meet at a point, on a straight line, or vertically opposite.

| Animation | Euclid Reference | Year | NC Statement |
|-----------|-----------------|------|--------------|
| Right angles | Def. X | Y3 | Identify right angles |
| Acute & obtuse angles | Def. XI, XII | Y4 | Identify acute and obtuse angles |
| Perpendicular lines | Def. X, Prop. XI | Y3 | Identify perpendicular lines |
| Parallel lines | Def. XXXV | Y3 | Identify parallel lines |
| Types of triangle (equilateral, isosceles, scalene) | Def. XXIV–XXVI | Y4 | Classify triangles based on properties |
| Types of triangle (right-angled, obtuse, acute) | Def. XXVII–XXIX | Y4 | Classify triangles based on properties |
| Square vs rectangle vs rhombus vs rhomboid | Def. XXX–XXXIII | Y4 | Compare and classify quadrilaterals |
| Parts of a circle (radius, diameter, circumference) | Def. XV–XVIII | Y6 | Illustrate and name parts of circles |
| Angles at a point / on a straight line | Prop. XIII, XV | Y5–6 | Know angle facts |
| Angles in a triangle sum to 180° | Prop. XXXII | Y6 | Find unknown angles in triangles |
| Constructing an equilateral triangle | Prop. I | Y5–6 | Draw 2D shapes using dimensions |

#### KS3 (Years 7–9): The Sweet Spot — Deductive Geometry

This is where the curriculum explicitly calls for Euclidean reasoning. The statutory programme of study states pupils should be taught to:

1. **"Derive and use the standard ruler and compass constructions"**: perpendicular bisector of a line segment (Prop. X), constructing a perpendicular to a given line from/at a given point (Props. XI, XII), bisecting a given angle (Prop. IX). These are literally Euclid's propositions.

2. **"Describe, sketch and draw using conventional terms and notations"**: points, lines, parallel lines, perpendicular lines, right angles, regular polygons. This maps directly to Euclid's Book I definitions.

3. **"Derive and illustrate properties of triangles, quadrilaterals, circles, and other plane figures"** using appropriate language and technologies. "Technologies" opens the door for animated visualisations.

4. **"Use the standard conventions for labelling the sides and angles of triangle ABC"** and know and use the criteria for congruence of triangles (cf. Props. IV, VIII, XXVI — SAS, SSS, ASA).

5. **"Apply the properties of angles at a point, angles at a point on a straight line, vertically opposite angles"** (Props. XIII, XV).

6. **"Understand and use the relationship between parallel lines and alternate and corresponding angles"** (Props. XXVII–XXIX).

7. **"Derive and use the sum of angles in a triangle"** and use it to deduce the angle sum in any polygon (Prop. XXXII).

8. **"Apply angle facts, triangle congruence, similarity and properties of quadrilaterals to derive results about angles and sides, including Pythagoras' Theorem"** (Prop. XLVII).

9. **"Begin to reason deductively in geometry"** — this is the explicit call for proof-based thinking, which is exactly what Euclid's propositions demonstrate.

| Animation | Euclid Reference | NC Statement (KS3) |
|-----------|-----------------|-------------------|
| Bisect an angle | Prop. IX | Standard ruler and compass constructions |
| Bisect a line segment | Prop. X | Standard ruler and compass constructions |
| Perpendicular from a point on a line | Prop. XI | Standard ruler and compass constructions |
| Perpendicular from a point to a line | Prop. XII | Standard ruler and compass constructions |
| Construct equilateral triangle | Prop. I | Standard ruler and compass constructions |
| Copy a line segment | Prop. II | Standard ruler and compass constructions |
| SAS triangle congruence | Prop. IV | Criteria for congruence of triangles |
| SSS triangle congruence | Prop. VIII | Criteria for congruence of triangles |
| Isosceles triangle base angles equal | Prop. V | Properties of triangles |
| Angles on a straight line | Prop. XIII | Angles at a point on a straight line |
| Vertically opposite angles | Prop. XV | Vertically opposite angles |
| Alternate angles (parallel lines) | Prop. XXIX | Parallel lines and alternate/corresponding angles |
| Angle sum of a triangle | Prop. XXXII | Sum of angles in a triangle |
| Pythagorean theorem | Prop. XLVII | Pythagoras' Theorem |

#### KS4 (Years 10–11, GCSE): Consolidation and Extension

At GCSE level, geometry concepts from KS3 are consolidated and extended to include circle theorems, trigonometry, vectors, and similarity/congruence proofs. The Byrne-style animations from KS3 remain directly relevant as foundational content.

### 13.3 Priority Animation Set — Curriculum-Aligned

Based on the curriculum mapping above, here is a **prioritised set of 15 animations** that maximises coverage of the national curriculum while staying within Book I of Euclid:

**Tier 1 — Definitions (KS2–KS3 foundational vocabulary)**
1. Point, line, straight line (Def. I, II, IV)
2. Angle types: right, obtuse, acute (Def. X–XII)
3. Circle, centre, radius, diameter (Def. XV–XVIII)
4. Triangle types by side: equilateral, isosceles, scalene (Def. XXIV–XXVI)
5. Triangle types by angle: right, obtuse, acute (Def. XXVII–XXIX)
6. Quadrilateral types: square, rectangle, rhombus, parallelogram (Def. XXX–XXXIII)
7. Parallel lines (Def. XXXV)

**Tier 2 — Constructions (KS3 statutory requirement)**
8. Construct equilateral triangle on a line (Prop. I)
9. Bisect an angle (Prop. IX)
10. Bisect a line segment (Prop. X)
11. Perpendicular from a point on a line (Prop. XI)
12. Perpendicular from an external point to a line (Prop. XII)

**Tier 3 — Angle theorems (KS3 deductive reasoning)**
13. Angles on a straight line sum to 180° (Prop. XIII)
14. Vertically opposite angles are equal (Prop. XV)
15. Angle sum of a triangle (Prop. XXXII)

**Stretch goal**:
16. Pythagorean theorem (Prop. XLVII) — the visual showpiece

### 13.4 Oak National Academy API — Integration Opportunity

#### What the API provides

The Oak Curriculum API (https://open-api.thenational.academy/) provides free access (Open Government Licence) to Oak's curriculum data and lesson resources for KS1–KS4 Maths. Key features:

- **Curriculum structure**: Key stages → Subjects → Sequences → Units → Lessons, organised by year group and threaded by topic
- **Threads**: Named topic strands that trace a concept across multiple years (e.g. "Geometry: Properties of shapes" runs from Year 1 through Year 9)
- **Lesson data**: Slide decks (pptx), videos (mp4), transcripts, worksheets (pdf), starter/exit quizzes
- **Misconceptions**: Common misconceptions and suggested teacher responses per lesson
- **Keywords**: Curriculum vocabulary per lesson/unit
- **Quiz questions**: Formative assessment items with answers
- **Search**: Full-text search across all content

#### Key API endpoints for this project

| Endpoint | Use |
|----------|-----|
| `GET /subjects/maths` | Get available sequences, key stages, years for Maths |
| `GET /threads` | List all curriculum threads — filter for geometry-related threads |
| `GET /threads/{threadSlug}/units` | Get all units in a geometry thread, in sequence order |
| `GET /key-stages/ks3/subject/maths/units` | List all KS3 Maths units by year |
| `GET /key-stages/ks3/subject/maths/lessons` | List all KS3 Maths lessons by unit |
| `GET /lessons/{lesson}/summary` | Get misconceptions, keywords, learning objectives for a lesson |
| `GET /key-stages/ks3/subject/maths/questions` | Get quiz questions for KS3 Maths |
| `GET /keywords?subject=maths&keyStage=ks3` | Get all geometry-related keywords |

#### Integration architecture

The connection between Manim animations and Oak's API could work at several levels:

**Level 1 — Metadata alignment (lightweight)**
Use the API to pull the exact lesson titles, keywords, and misconceptions for geometry lessons. Tag each animation with the corresponding Oak lesson slug and curriculum reference. This means a teacher searching Oak for "bisecting an angle" can find the animation as a companion resource.

```python
# Example: pull KS3 geometry lessons
import requests

headers = {"Authorization": "Bearer YOUR_API_KEY"}
resp = requests.get(
    "https://open-api.thenational.academy/api/v0/key-stages/ks3/subject/maths/lessons",
    headers=headers,
    params={"unit": "constructing-triangles-and-quadrilaterals"}
)
lessons = resp.json()
```

**Level 2 — Misconception-informed animation design (medium)**
Use `GET /lessons/{lesson}/summary` to retrieve common misconceptions for each geometry topic. Design animations that specifically address those misconceptions. For example, if a common misconception for "angles in a triangle" is that students think the angle sum depends on the type of triangle, the animation could show multiple triangle types all summing to 180°.

**Level 3 — Automated pipeline (ambitious)**
Build a pipeline that:
1. Queries the Oak API for geometry threads and their unit/lesson structure
2. Maps each lesson to one or more Euclid propositions/definitions
3. Generates Manim scenes parameterised by the lesson metadata
4. Renders GIFs/MP4s tagged with Oak lesson slugs
5. Outputs a manifest file linking each animation to its curriculum position

#### Relevant Oak threads (likely slugs — to be confirmed via API)

Based on Oak's curriculum structure, the geometry-related threads for Maths are likely to include:

- `geometry-properties-of-shapes` (or similar)
- `geometry-position-and-direction`
- `geometry-and-measures`
- `angles-and-lines`
- `constructions-and-loci`

These can be discovered via `GET /threads` and filtering for geometry-related titles.

#### Licensing

Oak's content is published under the **Open Government Licence (OGL)**, which permits free use, adaptation and redistribution with attribution. This is compatible with publishing Manim-generated animations on YouTube and in blog posts, provided attribution to Oak is included where their data informed the animation design.

### 13.5 YouTube Strategy

Animations produced for this project could be organised into YouTube playlists mapped to the curriculum:

1. **"Euclid's Definitions — Geometry Vocabulary for KS2/KS3"** (7 animations covering Defs. I–XXXV)
2. **"Ruler and Compass Constructions — KS3 Geometry"** (5 animations covering Props. I, IX, X, XI, XII)
3. **"Angle Theorems — KS3 Deductive Geometry"** (3–4 animations covering Props. XIII, XV, XXXII, XLVII)

Each video could include:
- The Byrne-style animated construction (the hero content)
- A brief text overlay naming the Euclid proposition and the NC curriculum reference
- A link to the corresponding Oak lesson in the description
- CC-BY or similar open licence for teacher reuse

**Video format considerations**:
- Short form (30–90 seconds each) for maximum teacher utility — these are visual aids, not lectures
- Square (1:1) or vertical (9:16) for social media / embedding in slides
- 16:9 for YouTube primary format
- Render both and upload the 16:9 to YouTube, provide square GIFs for download/embedding
- Consider adding a brief narration track (or keep silent with text overlays for maximum accessibility / use in any language)

### 13.6 The Blog Post Angle — Updated

The pivot from "personal exploration" to "curriculum-aligned teacher resource" strengthens the blog post considerably:

1. **Hook**: "I've been re-learning Euclid's geometry with my kids — and I realised these 2,300-year-old constructions are still in the English national curriculum. So I built animated versions for teachers."

2. **The connection**: Map Euclid → Byrne → UK curriculum → Oak National Academy. Show that Proposition IX (bisect an angle) is literally a statutory requirement at KS3.

3. **The tooling**: ManimCE + Oak API + Byrne palette. This is a technical blog post aimed at the intersection of educators and developers.

4. **The output**: Embeddable GIFs/videos that teachers can use in lessons. Link to YouTube playlist. Open source the Manim code.

5. **The meta-point**: The power of connecting open educational resources (Oak, OGL) with open-source tools (Manim, MIT) and historical design systems (Byrne) to create something genuinely useful.

This positions the project not just as a fun exploration but as a template for how AI engineers can create value in education — relevant to your consultancy positioning.
