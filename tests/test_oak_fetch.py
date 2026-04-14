import json
from pathlib import Path

import pytest

from scripts.fetch_oak_curriculum import (
    attach_thread_slugs_to_units,
    build_unit_thread_index,
    fetch_oak_curriculum_data,
    flatten_lesson_groups,
    flatten_unit_groups,
    resolve_api_key,
    select_geometry_threads,
    select_geometry_units,
)

PARALLEL_PERP_UNIT = "parallel-and-perpendicular-sides-in-polygons-and-perimeter"
ANGLES_UNIT = "angles-compare-name-estimate-and-measure-angles"
ROTATING_ANGLES_LESSON = (
    "make-different-sized-angles-by-rotating-two-lines-around-a-fixed-point"
)
CONSTRUCT_QUADS_LESSON = (
    "construct-quadrilaterals-with-and-without-parallel-and-perpendicular-sides"
)
ESTIMATE_ANGLES_LESSON = (
    "estimate-acute-and-obtuse-angles-using-the-standard-unit-of-degrees"
)
STRAIGHT_LINE_ANGLES_LESSON = (
    "know-that-the-angles-on-a-straight-line-sum-to-180-degrees-and-use-this-to-solve-problems"
)


class FakeOakClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str | None]] = []
        self.responses = {
            "/subjects/maths": {
                "subjectSlug": "maths",
                "subjectTitle": "Maths",
                "sequenceSlugs": [
                    {
                        "sequenceSlug": "maths-primary",
                        "keyStages": [{"keyStageSlug": "ks2"}],
                    },
                    {
                        "sequenceSlug": "maths-secondary",
                        "keyStages": [{"keyStageSlug": "ks3"}],
                    },
                ],
            },
            "/threads": [
                {"slug": "geometry-and-measure", "title": "Geometry and Measure"},
                {"slug": "geometry-21", "title": "Geometry"},
                {"slug": "number", "title": "Number"},
            ],
            "/threads/geometry-and-measure/units": [
                {
                    "unitOrder": 1,
                    "unitSlug": "right-angles",
                    "unitTitle": "Right angles",
                },
                {
                    "unitOrder": 2,
                    "unitSlug": PARALLEL_PERP_UNIT,
                    "unitTitle": "Parallel and perpendicular sides in polygons",
                },
                {
                    "unitOrder": 3,
                    "unitSlug": ANGLES_UNIT,
                    "unitTitle": "Angles: compare, name, estimate and measure angles",
                },
                {
                    "unitOrder": 4,
                    "unitSlug": "constructions",
                    "unitTitle": "Constructions",
                },
                {
                    "unitOrder": 5,
                    "unitSlug": "geometrical-properties-polygons",
                    "unitTitle": "Geometrical properties: polygons",
                },
            ],
            "/threads/geometry-21/units": [
                {
                    "unitOrder": 1,
                    "unitSlug": "shape-and-pattern",
                    "unitTitle": "Shape and pattern",
                }
            ],
            "/key-stages/ks2/subject/maths/units": [
                {
                    "yearSlug": "year-3",
                    "yearTitle": "Year 3",
                    "units": [
                        {"unitSlug": "right-angles", "unitTitle": "Right angles"},
                        {
                            "unitSlug": PARALLEL_PERP_UNIT,
                            "unitTitle": "Parallel and perpendicular sides in polygons",
                        },
                    ],
                },
                {
                    "yearSlug": "year-5",
                    "yearTitle": "Year 5",
                    "units": [
                        {
                            "unitSlug": ANGLES_UNIT,
                            "unitTitle": (
                                "Angles: compare, name, estimate and measure angles"
                            ),
                        },
                        {
                            "unitSlug": "link-area-of-rectangles-to-multiplication",
                            "unitTitle": "Link area of rectangles to multiplication",
                        },
                    ],
                },
            ],
            "/key-stages/ks3/subject/maths/units": [
                {
                    "yearSlug": "year-8",
                    "yearTitle": "Year 8",
                    "units": [
                        {"unitSlug": "constructions", "unitTitle": "Constructions"},
                        {
                            "unitSlug": "geometrical-properties-polygons",
                            "unitTitle": "Geometrical properties: polygons",
                        },
                    ],
                }
            ],
            ("/key-stages/ks2/subject/maths/lessons", "right-angles"): [
                {
                    "unitSlug": "right-angles",
                    "unitTitle": "Right angles",
                    "lessons": [
                        {
                            "lessonSlug": "identify-and-describe-right-angles",
                            "lessonTitle": "Identify and describe right angles",
                        },
                        {
                            "lessonSlug": ROTATING_ANGLES_LESSON,
                            "lessonTitle": (
                                "Make different sized angles by rotating two lines "
                                "around a fixed point"
                            ),
                        },
                    ],
                }
            ],
            ("/key-stages/ks2/subject/maths/lessons", PARALLEL_PERP_UNIT): [
                {
                    "unitSlug": PARALLEL_PERP_UNIT,
                    "unitTitle": "Parallel and perpendicular sides in polygons",
                    "lessons": [
                        {
                            "lessonSlug": "identifying-parallel-lines",
                            "lessonTitle": "Identifying parallel lines",
                        },
                        {
                            "lessonSlug": CONSTRUCT_QUADS_LESSON,
                            "lessonTitle": (
                                "Construct quadrilaterals with and without parallel "
                                "and perpendicular sides"
                            ),
                        },
                    ],
                }
            ],
            ("/key-stages/ks2/subject/maths/lessons", ANGLES_UNIT): [
                {
                    "unitSlug": ANGLES_UNIT,
                    "unitTitle": "Angles: compare, name, estimate and measure angles",
                    "lessons": [
                        {
                            "lessonSlug": ESTIMATE_ANGLES_LESSON,
                            "lessonTitle": (
                                "Estimate acute and obtuse angles using degrees"
                            ),
                        },
                        {
                            "lessonSlug": STRAIGHT_LINE_ANGLES_LESSON,
                            "lessonTitle": (
                                "Know that the angles on a straight line sum to 180 "
                                "degrees and use this to solve problems"
                            ),
                        },
                    ],
                }
            ],
            ("/key-stages/ks3/subject/maths/lessons", "constructions"): [
                {
                    "unitSlug": "constructions",
                    "unitTitle": "Constructions",
                    "lessons": [
                        {
                            "lessonSlug": "bisecting-an-angle",
                            "lessonTitle": "Bisecting an angle",
                        },
                        {
                            "lessonSlug": "perpendicular-bisector-of-a-line-segment",
                            "lessonTitle": "Perpendicular bisector of a line segment",
                        },
                        {
                            "lessonSlug": (
                                "perpendicular-to-a-given-line-through-a-given-point"
                            ),
                            "lessonTitle": (
                                "Perpendicular to a given line through a given point"
                            ),
                        },
                        {
                            "lessonSlug": "understanding-constructing-a-circle",
                            "lessonTitle": "Understanding constructing a circle",
                        },
                    ],
                }
            ],
            (
                "/key-stages/ks3/subject/maths/lessons",
                "geometrical-properties-polygons",
            ): [
                {
                    "unitSlug": "geometrical-properties-polygons",
                    "unitTitle": "Geometrical properties: polygons",
                    "lessons": [
                        {
                            "lessonSlug": "checking-understanding-of-angles-from-ks2",
                            "lessonTitle": (
                                "Checking understanding of angles from KS2"
                            ),
                        },
                        {
                            "lessonSlug": (
                                "deriving-the-sum-of-interior-angles-in-multiple-ways"
                            ),
                            "lessonTitle": (
                                "Deriving the sum of interior angles in multiple ways"
                            ),
                        },
                        {
                            "lessonSlug": "exterior-angles-of-polygons",
                            "lessonTitle": "Exterior angles of polygons",
                        },
                    ],
                }
            ],
            "/lessons/identify-and-describe-right-angles/summary": {
                "lessonTitle": "Identify and describe right angles",
                "lessonKeywords": [{"keyword": "right angle"}],
                "misconceptionsAndCommonMistakes": [
                    {
                        "misconception": (
                            "Pupils may think there is only ever one right angle in "
                            "a shape."
                        )
                    }
                ],
                "threads": [],
            },
            f"/lessons/{ROTATING_ANGLES_LESSON}/summary": {
                "lessonTitle": (
                    "Make different sized angles by rotating two lines around a "
                    "fixed point"
                ),
                "lessonKeywords": [{"keyword": "angle"}],
                "misconceptionsAndCommonMistakes": [],
                "threads": [],
            },
            "/lessons/identifying-parallel-lines/summary": {
                "lessonTitle": "Identifying parallel lines",
                "lessonKeywords": [{"keyword": "parallel"}],
                "misconceptionsAndCommonMistakes": [],
                "threads": [],
            },
            f"/lessons/{CONSTRUCT_QUADS_LESSON}/summary": {
                "lessonTitle": (
                    "Construct quadrilaterals with and without parallel and "
                    "perpendicular sides"
                ),
                "lessonKeywords": [{"keyword": "quadrilateral"}],
                "misconceptionsAndCommonMistakes": [
                    {
                        "misconception": (
                            "Pupils may find it challenging to identify specific "
                            "quadrilaterals when making them."
                        )
                    }
                ],
                "threads": [],
            },
            f"/lessons/{ESTIMATE_ANGLES_LESSON}/summary": {
                "lessonTitle": "Estimate acute and obtuse angles using degrees",
                "lessonKeywords": [{"keyword": "obtuse angle"}],
                "misconceptionsAndCommonMistakes": [],
                "threads": [],
            },
            f"/lessons/{STRAIGHT_LINE_ANGLES_LESSON}/summary": {
                "lessonTitle": (
                    "Know that the angles on a straight line sum to 180 degrees "
                    "and use this to solve problems"
                ),
                "lessonKeywords": [{"keyword": "straight line"}],
                "misconceptionsAndCommonMistakes": [],
                "threads": [],
            },
            "/lessons/bisecting-an-angle/summary": {
                "lessonTitle": "Bisecting an angle",
                "lessonKeywords": [{"keyword": "angle bisector"}],
                "misconceptionsAndCommonMistakes": [
                    {
                        "misconception": (
                            "I can use a protractor to measure an angle, then half "
                            "that angle to bisect it."
                        )
                    }
                ],
                "threads": [],
            },
            "/lessons/perpendicular-bisector-of-a-line-segment/summary": {
                "lessonTitle": "Perpendicular bisector of a line segment",
                "lessonKeywords": [{"keyword": "midpoint"}],
                "misconceptionsAndCommonMistakes": [
                    {
                        "misconception": (
                            "I can use a ruler to measure the midpoint of a line "
                            "segment, and a protractor to find 90°."
                        )
                    }
                ],
                "threads": [],
            },
            "/lessons/perpendicular-to-a-given-line-through-a-given-point/summary": {
                "lessonTitle": "Perpendicular to a given line through a given point",
                "lessonKeywords": [{"keyword": "perpendicular"}],
                "misconceptionsAndCommonMistakes": [
                    {
                        "misconception": (
                            "You can't accurately draw the perpendicular to a point "
                            "on a line segment close to its endpoint."
                        )
                    }
                ],
                "threads": [],
            },
            "/lessons/understanding-constructing-a-circle/summary": {
                "lessonTitle": "Understanding constructing a circle",
                "lessonKeywords": [{"keyword": "radius"}],
                "misconceptionsAndCommonMistakes": [
                    {
                        "misconception": (
                            "During tasks, pupils may use a ruler to draw or check "
                            "whether points are equidistant from a centre."
                        )
                    }
                ],
                "threads": [],
            },
            "/lessons/checking-understanding-of-angles-from-ks2/summary": {
                "lessonTitle": "Checking understanding of angles from KS2",
                "lessonKeywords": [{"keyword": "angles at a point"}],
                "misconceptionsAndCommonMistakes": [],
                "threads": [],
            },
            "/lessons/deriving-the-sum-of-interior-angles-in-multiple-ways/summary": {
                "lessonTitle": "Deriving the sum of interior angles in multiple ways",
                "lessonKeywords": [{"keyword": "interior angle"}],
                "misconceptionsAndCommonMistakes": [
                    {
                        "misconception": (
                            "Interior angles always sum to 180 times the number of "
                            "component triangles."
                        )
                    }
                ],
                "threads": [],
            },
            "/lessons/exterior-angles-of-polygons/summary": {
                "lessonTitle": "Exterior angles of polygons",
                "lessonKeywords": [{"keyword": "exterior angle"}],
                "misconceptionsAndCommonMistakes": [
                    {
                        "misconception": (
                            "The exterior angle is the entire reflex angle on the "
                            "outside of each vertex."
                        )
                    }
                ],
                "threads": [],
            },
        }

    def get_json(self, endpoint: str, params: dict[str, object] | None = None) -> object:
        unit_slug = None
        if params is not None:
            unit = params.get("unit")
            if isinstance(unit, str):
                unit_slug = unit
        self.calls.append((endpoint, unit_slug))
        key: str | tuple[str, str] = endpoint if unit_slug is None else (endpoint, unit_slug)
        return self.responses[key]


def test_select_geometry_threads_matches_live_thread_shape() -> None:
    threads = [
        {"slug": "geometry-and-measure", "title": "Geometry and Measure"},
        {"slug": "number", "title": "Number"},
        {"slug": "earth-geometry", "title": "Earth geometry"},
    ]

    selected = select_geometry_threads(threads)

    assert [thread["threadSlug"] for thread in selected] == [
        "geometry-and-measure",
        "earth-geometry",
    ]


def test_flatten_key_stage_units_preserves_year_metadata() -> None:
    payload = [
        {
            "yearSlug": "year-5",
            "yearTitle": "Year 5",
            "units": [
                {
                    "unitSlug": ANGLES_UNIT,
                    "unitTitle": "Angles: compare, name, estimate and measure angles",
                }
            ],
        }
    ]

    flattened = flatten_unit_groups(payload)

    assert flattened == [
        {
            "unitSlug": ANGLES_UNIT,
            "unitTitle": "Angles: compare, name, estimate and measure angles",
            "yearSlug": "year-5",
            "yearTitle": "Year 5",
        }
    ]


def test_select_geometry_units_avoids_rectangle_false_positive() -> None:
    units = [
        {
            "unitSlug": ANGLES_UNIT,
            "unitTitle": "Angles: compare, name, estimate and measure angles",
        },
        {
            "unitSlug": "link-area-of-rectangles-to-multiplication",
            "unitTitle": "Link area of rectangles to multiplication",
        },
    ]

    selected = select_geometry_units(units)

    assert [unit["unitSlug"] for unit in selected] == [ANGLES_UNIT]


def test_extract_lessons_from_unit_wrappers_preserves_unit_context() -> None:
    payload = [
        {
            "unitSlug": "constructions",
            "unitTitle": "Constructions",
            "lessons": [
                {
                    "lessonSlug": "bisecting-an-angle",
                    "lessonTitle": "Bisecting an angle",
                }
            ],
        }
    ]

    flattened = flatten_lesson_groups(
        payload,
        key_stage_slug="ks3",
        year_slug="year-8",
        year_title="Year 8",
        thread_slugs=["geometry-and-measure"],
    )

    assert flattened == [
        {
            "lessonSlug": "bisecting-an-angle",
            "lessonTitle": "Bisecting an angle",
            "unitSlug": "constructions",
            "unitTitle": "Constructions",
            "yearSlug": "year-8",
            "yearTitle": "Year 8",
            "keyStageSlug": "ks3",
            "threadSlugs": ["geometry-and-measure"],
        }
    ]


def test_build_unit_thread_index_from_thread_units() -> None:
    geometry_thread_units = {
        "geometry-and-measure": [
            {"unitSlug": "right-angles", "unitTitle": "Right angles"},
            {"unitSlug": "constructions", "unitTitle": "Constructions"},
        ],
        "geometry-21": [
            {"unitSlug": "shape-and-pattern", "unitTitle": "Shape and pattern"}
        ],
    }

    index = build_unit_thread_index(geometry_thread_units)

    assert index == {
        "right-angles": ["geometry-and-measure"],
        "constructions": ["geometry-and-measure"],
        "shape-and-pattern": ["geometry-21"],
    }


def test_attach_thread_slugs_to_units_keeps_only_units_backed_by_geometry_threads() -> None:
    units = [
        {"unitSlug": "right-angles", "unitTitle": "Right angles"},
        {
            "unitSlug": "link-area-of-rectangles-to-multiplication",
            "unitTitle": "Link area of rectangles to multiplication",
        },
    ]

    attached = attach_thread_slugs_to_units(
        units,
        {"right-angles": ["geometry-and-measure"]},
    )

    assert attached == [
        {
            "unitSlug": "right-angles",
            "unitTitle": "Right angles",
            "threadSlugs": ["geometry-and-measure"],
        }
    ]


def test_fetch_oak_curriculum_data_normalises_live_oak_payloads(tmp_path: Path) -> None:
    client = FakeOakClient()

    combined = fetch_oak_curriculum_data(client=client, output_dir=tmp_path, summary_limit=0)

    assert combined["subject"]["subjectSlug"] == "maths"
    assert [thread["threadSlug"] for thread in combined["geometry_threads"]] == [
        "geometry-and-measure"
    ]
    assert [unit["unitSlug"] for unit in combined["ks2_geometry_units"]] == [
        "right-angles",
        PARALLEL_PERP_UNIT,
        ANGLES_UNIT,
    ]
    assert [unit["unitSlug"] for unit in combined["ks3_geometry_units"]] == [
        "constructions",
        "geometrical-properties-polygons",
    ]
    assert "link-area-of-rectangles-to-multiplication" not in {
        unit["unitSlug"] for unit in combined["ks2_geometry_units"]
    }
    assert {lesson["lessonSlug"] for lesson in combined["ks2_geometry_lessons"]} == {
        "identify-and-describe-right-angles",
        ROTATING_ANGLES_LESSON,
        "identifying-parallel-lines",
        CONSTRUCT_QUADS_LESSON,
        ESTIMATE_ANGLES_LESSON,
        STRAIGHT_LINE_ANGLES_LESSON,
    }
    assert {lesson["lessonSlug"] for lesson in combined["ks3_geometry_lessons"]} == {
        "bisecting-an-angle",
        "perpendicular-bisector-of-a-line-segment",
        "perpendicular-to-a-given-line-through-a-given-point",
        "understanding-constructing-a-circle",
        "checking-understanding-of-angles-from-ks2",
        "deriving-the-sum-of-interior-angles-in-multiple-ways",
        "exterior-angles-of-polygons",
    }
    assert set(combined["lesson_summaries"]) == {
        "identify-and-describe-right-angles",
        ROTATING_ANGLES_LESSON,
        "identifying-parallel-lines",
        CONSTRUCT_QUADS_LESSON,
        ESTIMATE_ANGLES_LESSON,
        STRAIGHT_LINE_ANGLES_LESSON,
        "bisecting-an-angle",
        "perpendicular-bisector-of-a-line-segment",
        "perpendicular-to-a-given-line-through-a-given-point",
        "understanding-constructing-a-circle",
        "checking-understanding-of-angles-from-ks2",
        "deriving-the-sum-of-interior-angles-in-multiple-ways",
        "exterior-angles-of-polygons",
    }

    for filename in (
        "oak_subject_maths.json",
        "oak_threads_raw.json",
        "oak_geometry_threads.json",
        "oak_geometry_thread_units.json",
        "oak_geometry_unit_thread_slugs.json",
        "oak_ks2_geometry_units.json",
        "oak_ks3_geometry_units.json",
        "oak_ks2_geometry_lessons.json",
        "oak_ks3_geometry_lessons.json",
        "oak_geometry_lesson_summaries.json",
        "oak_geometry_data.json",
    ):
        assert (tmp_path / filename).exists()

    saved = json.loads((tmp_path / "oak_geometry_data.json").read_text())
    assert saved["geometry_unit_thread_slugs"]["constructions"] == [
        "geometry-and-measure"
    ]


def test_fetch_oak_curriculum_data_derives_thread_links_when_summary_threads_are_empty(
    tmp_path: Path,
) -> None:
    client = FakeOakClient()

    combined = fetch_oak_curriculum_data(client=client, output_dir=tmp_path, summary_limit=0)

    lesson_lookup = {
        lesson["lessonSlug"]: lesson
        for lesson in combined["ks2_geometry_lessons"] + combined["ks3_geometry_lessons"]
    }

    assert lesson_lookup["bisecting-an-angle"]["threadSlugs"] == [
        "geometry-and-measure"
    ]
    assert combined["lesson_summaries"]["bisecting-an-angle"]["threads"] == []


def test_resolve_api_key_prefers_oak_open_api_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OAK_API_KEY", "legacy-key")
    monkeypatch.setenv("OAK_OPEN_API_KEY", "preferred-key")

    assert resolve_api_key() == "preferred-key"
