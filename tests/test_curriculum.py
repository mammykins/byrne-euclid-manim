from datetime import UTC, datetime
from pathlib import Path

import pytest

from byrne_euclid.curriculum import (
    build_manifest,
    load_mapping_entries,
    render_curriculum_mapping_markdown,
)


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
                                "Show non-symmetrical examples as well as "
                                "symmetrical ones."
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
                    "Two compass arcs meet and a line through their intersection "
                    "bisects an angle."
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
