import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from byrne_euclid.curriculum import (
    build_manifest,
    load_mapping_entries,
    render_curriculum_mapping_markdown,
    render_curriculum_preview_markdown,
    render_curriculum_showcase_markdown,
)

DEMO_MAPPING_PATH = Path("curriculum/demo_curriculum_preview.yaml")
DEMO_ENRICHMENT_PATH = Path("curriculum/demo_curriculum_enrichment.json")
DEMO_GENERATED_AT = datetime(2026, 4, 10, 6, 0, tzinfo=UTC)


def _build_demo_preview_manifest() -> dict[str, object]:
    entries = load_mapping_entries(DEMO_MAPPING_PATH)
    oak_data = json.loads(DEMO_ENRICHMENT_PATH.read_text())
    return build_manifest(entries, oak_data=oak_data, generated_at=DEMO_GENERATED_AT)


def test_load_mapping_entries_rejects_unknown_scene_names(tmp_path: Path) -> None:
    mapping_path = tmp_path / "euclid_to_oak.yaml"
    mapping_path.write_text(
        """
- scene: NotAScene
  euclid_type: definition
  euclid_numbers: [1]
  title: Unknown scene
  description: This scene does not exist in the registry.
  alt_text: A missing scene.
  nc_references:
    - key_stage: KS2
      year: 3
      domain: Geometry — properties of shapes
      statement: Identify right angles
  oak_lesson_slugs: []
  oak_thread_slugs: []
  keywords: []
  misconceptions: []
""".strip()
    )

    with pytest.raises(ValueError, match="Unknown scene"):
        load_mapping_entries(mapping_path)


def test_build_manifest_enriches_entries_with_oak_summary_data(tmp_path: Path) -> None:
    mapping_path = tmp_path / "euclid_to_oak.yaml"
    mapping_path.write_text(
        """
- scene: PropXIII
  euclid_type: proposition
  euclid_numbers: [13]
  title: Angles on a straight line
  description: Adjacent angles on a straight line sum to two right angles.
  alt_text: A line stands on another line while two coloured adjacent angles fill in.
  duration_seconds: 35
  nc_references:
    - key_stage: KS2
      year: 5
      domain: Geometry — properties of shapes
      statement: Know angles at a point and angles on a straight line
  oak_lesson_slugs:
    - adjacent-angles-on-a-straight-line
  oak_thread_slugs:
    - geometry-properties-of-shapes
  keywords:
    - angle
    - straight line
  misconceptions: []
""".strip()
    )

    entries = load_mapping_entries(mapping_path)
    manifest = build_manifest(
        entries,
        oak_data={
            "lesson_summaries": {
                "adjacent-angles-on-a-straight-line": {
                    "lessonKeywords": [
                        {
                            "keyword": "supplementary angle",
                            "description": "Two angles that add to 180 degrees.",
                        }
                    ],
                    "misconceptionsAndCommonMistakes": [
                        {
                            "misconception": (
                                "Pupils may think adjacent angles on a straight line "
                                "are always equal."
                            ),
                            "response": (
                                "Show non-symmetrical examples as well as symmetrical ones."
                            ),
                        }
                    ],
                }
            }
        },
        generated_at=datetime(2026, 4, 10, 5, 0, tzinfo=UTC),
    )

    assert manifest["generated_at"] == "2026-04-10T05:00:00Z"
    entry = manifest["animations"][0]
    assert entry["scene_class"] == "PropXIII"
    assert entry["files"] == {
        "gif": "output/gif/PropXIII.gif",
        "mp4": "output/mp4/PropXIII.mp4",
        "png": "output/png/PropXIII.png",
    }
    assert "supplementary angle" in entry["keywords"]
    assert (
        "Pupils may think adjacent angles on a straight line are always equal."
        in entry["misconceptions"]
    )


def test_build_manifest_preserves_verified_oak_slugs_and_dedupes_enrichment(
    tmp_path: Path,
) -> None:
    mapping_path = tmp_path / "euclid_to_oak.yaml"
    mapping_path.write_text(
        """
- scene: PropIX
  euclid_type: proposition
  euclid_numbers: [9]
  title: Bisect an angle
  description: Bisect a rectilinear angle.
  alt_text: Compass arcs meet and a line splits an angle into equal parts.
  duration_seconds: 40
  nc_references:
    - key_stage: KS3
      year: 8
      domain: Geometry and measures
      statement: Derive and use the standard ruler and compass constructions
  oak_lesson_slugs:
    - bisecting-an-angle
  oak_thread_slugs:
    - geometry-and-measure
  keywords:
    - angle bisector
  misconceptions:
    - I can use a protractor to measure an angle, then half that angle to bisect it.
""".strip()
    )

    entries = load_mapping_entries(mapping_path)
    manifest = build_manifest(
        entries,
        oak_data={
            "lesson_summaries": {
                "bisecting-an-angle": {
                    "lessonKeywords": [
                        {"keyword": "angle bisector"},
                        {"keyword": "construction"},
                    ],
                    "misconceptionsAndCommonMistakes": [
                        {
                            "misconception": (
                                "I can use a protractor to measure an angle, then "
                                "half that angle to bisect it."
                            )
                        }
                    ],
                }
            }
        },
        generated_at=datetime(2026, 4, 14, 4, 45, tzinfo=UTC),
    )

    entry = manifest["animations"][0]
    assert entry["oak_lesson_slugs"] == ["bisecting-an-angle"]
    assert entry["oak_thread_slugs"] == ["geometry-and-measure"]
    assert entry["keywords"] == ["angle bisector", "construction"]
    assert entry["misconceptions"] == [
        "I can use a protractor to measure an angle, then half that angle to bisect it."
    ]
    assert entry["files"] == {
        "gif": "output/gif/PropIX.gif",
        "mp4": "output/mp4/PropIX.mp4",
        "png": "output/png/PropIX.png",
    }


def test_render_curriculum_mapping_markdown_groups_entries_by_key_stage_and_year() -> None:
    manifest = {
        "version": "0.1.0",
        "generated_at": "2026-04-10T05:00:00Z",
        "animations": [
            {
                "scene_class": "DefAngleTypes",
                "title": "Angle types",
                "euclid_book": 1,
                "euclid_type": "definition",
                "euclid_numbers": [10, 11, 12],
                "description": "Right, obtuse, and acute angles.",
                "duration_seconds": 30,
                "nc_references": [
                    {
                        "key_stage": "KS2",
                        "year": 4,
                        "domain": "Geometry — properties of shapes",
                        "statement": "Identify acute and obtuse angles",
                    }
                ],
                "oak_lesson_slugs": ["acute-and-obtuse-angles"],
                "oak_thread_slugs": ["geometry-properties-of-shapes"],
                "keywords": ["angle", "acute", "obtuse"],
                "misconceptions": [],
                "alt_text": "An arm rotates to show a right angle becoming obtuse and acute.",
                "files": {
                    "gif": "output/gif/DefAngleTypes.gif",
                    "mp4": "output/mp4/DefAngleTypes.mp4",
                    "png": "output/png/DefAngleTypes.png",
                },
            },
            {
                "scene_class": "PropIX",
                "title": "Bisect an angle",
                "euclid_book": 1,
                "euclid_type": "proposition",
                "euclid_numbers": [9],
                "description": "Bisect a rectilinear angle.",
                "duration_seconds": 40,
                "nc_references": [
                    {
                        "key_stage": "KS3",
                        "year": 7,
                        "domain": "Geometry and measures",
                        "statement": "Derive and use the standard ruler and compass constructions",
                    }
                ],
                "oak_lesson_slugs": ["bisect-a-given-angle"],
                "oak_thread_slugs": ["constructions-and-loci"],
                "keywords": ["angle bisector"],
                "misconceptions": [],
                "alt_text": (
                    "Two compass arcs meet and a line through their intersection bisects an angle."
                ),
                "files": {
                    "gif": "output/gif/PropIX.gif",
                    "mp4": "output/mp4/PropIX.mp4",
                    "png": "output/png/PropIX.png",
                },
            },
        ],
    }

    markdown = render_curriculum_mapping_markdown(manifest)

    assert "# Curriculum mapping" in markdown
    assert "## KS2" in markdown
    assert "### Year 4" in markdown
    assert "`DefAngleTypes`" in markdown
    assert "acute-and-obtuse-angles" in markdown
    assert "## KS3" in markdown
    assert "### Year 7" in markdown
    assert "`PropIX`" in markdown


def test_load_demo_preview_mapping_entries_accepts_only_real_scene_names() -> None:
    entries = load_mapping_entries(DEMO_MAPPING_PATH)

    assert [entry.scene for entry in entries] == [
        "DefAngleTypes",
        "PropXI",
        "PropXXXII",
    ]


def test_build_demo_preview_manifest_enriches_without_live_oak() -> None:
    manifest = _build_demo_preview_manifest()

    assert manifest["generated_at"] == "2026-04-10T06:00:00Z"
    assert [entry["scene_class"] for entry in manifest["animations"]] == [
        "DefAngleTypes",
        "PropXI",
        "PropXXXII",
    ]

    angle_types = manifest["animations"][0]
    assert angle_types["oak_lesson_slugs"] == ["demo-identify-acute-and-obtuse-angles"]
    assert angle_types["oak_thread_slugs"] == ["demo-geometry-properties-of-shapes"]
    assert "angle" in angle_types["keywords"]
    assert "turn" in angle_types["keywords"]
    assert (
        "Pupils may think an obtuse angle is any angle that looks large."
        in angle_types["misconceptions"]
    )
    assert angle_types["files"] == {
        "gif": "output/gif/DefAngleTypes.gif",
        "mp4": "output/mp4/DefAngleTypes.mp4",
        "png": "output/png/DefAngleTypes.png",
    }


def test_render_demo_curriculum_mapping_markdown_has_populated_curriculum_links() -> None:
    manifest = _build_demo_preview_manifest()
    markdown = render_curriculum_preview_markdown(manifest)

    assert "# Demo curriculum mapping" in markdown
    assert "synthetic preview" in markdown
    assert "Preview lesson slugs" in markdown
    assert "Preview thread slugs" in markdown
    assert "demo-identify-acute-and-obtuse-angles" in markdown
    assert "demo-perpendicular-from-a-point-on-a-line" in markdown
    assert "demo-angle-sum-of-a-triangle" in markdown
    assert "Draft mapping pending" not in markdown


def test_render_curriculum_showcase_markdown_includes_media_and_teaching_metadata() -> None:
    manifest = _build_demo_preview_manifest()

    markdown = render_curriculum_showcase_markdown(
        manifest,
        title="Demo curriculum showcase",
    )

    assert "# Demo curriculum showcase" in markdown
    assert "## Definitions X–XII — right, obtuse, and acute angles" in markdown
    assert "## Proposition XI — draw a perpendicular from a point on a line" in markdown
    assert "## Proposition XXXII — angle sum of a triangle" in markdown
    assert "- Keywords:" in markdown
    assert "- Misconceptions:" in markdown
    assert "- Alt text:" in markdown
    assert "`output/gif/PropXXXII.gif`" in markdown
    assert "Pupils may place the perpendicular by eye rather than by construction." in markdown
