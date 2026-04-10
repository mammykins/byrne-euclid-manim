import json
from pathlib import Path

from scripts.fetch_oak_curriculum import (
    fetch_oak_curriculum_data,
    select_geometry_lessons,
    select_geometry_threads,
)


class FakeOakClient:
    def __init__(self) -> None:
        self.calls: list[str] = []
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
                {
                    "threadSlug": "geometry-properties-of-shapes",
                    "threadTitle": "Geometry: properties of shapes",
                    "subjectSlug": "maths",
                },
                {
                    "threadSlug": "number-place-value",
                    "threadTitle": "Number: place value",
                    "subjectSlug": "maths",
                },
                {
                    "threadSlug": "drawing-and-making",
                    "threadTitle": "Drawing and making",
                    "subjectSlug": "art",
                },
            ],
            "/threads/geometry-properties-of-shapes/units": [
                {
                    "year": 4,
                    "units": [
                        {
                            "unitSlug": "angles-and-shapes",
                            "unitTitle": "Angles and shapes",
                            "threads": [
                                {
                                    "threadSlug": "geometry-properties-of-shapes",
                                    "threadTitle": "Geometry: properties of shapes",
                                }
                            ],
                        }
                    ],
                }
            ],
            "/key-stages/ks2/subject/maths/lessons": [
                {
                    "lessonSlug": "identify-acute-and-obtuse-angles",
                    "lessonTitle": "Identify acute and obtuse angles",
                    "unitSlug": "angles-and-shapes",
                    "unitTitle": "Angles and shapes",
                    "keyStageSlug": "ks2",
                    "threads": [
                        {
                            "threadSlug": "geometry-properties-of-shapes",
                            "threadTitle": "Geometry: properties of shapes",
                        }
                    ],
                },
                {
                    "lessonSlug": "numbers-to-1000",
                    "lessonTitle": "Numbers to 1000",
                    "unitSlug": "place-value",
                    "unitTitle": "Place value",
                    "keyStageSlug": "ks2",
                    "threads": [
                        {
                            "threadSlug": "number-place-value",
                            "threadTitle": "Number: place value",
                        }
                    ],
                },
            ],
            "/key-stages/ks3/subject/maths/lessons": [
                {
                    "lessonSlug": "bisect-a-line-segment",
                    "lessonTitle": "Bisect a line segment",
                    "unitSlug": "constructions-and-loci",
                    "unitTitle": "Constructions and loci",
                    "keyStageSlug": "ks3",
                    "threads": [
                        {
                            "threadSlug": "geometry-properties-of-shapes",
                            "threadTitle": "Geometry: properties of shapes",
                        }
                    ],
                }
            ],
            "/lessons/identify-acute-and-obtuse-angles/summary": {
                "lessonTitle": "Identify acute and obtuse angles",
                "lessonKeywords": [
                    {
                        "keyword": "obtuse angle",
                        "description": "An angle larger than 90°.",
                    }
                ],
                "misconceptionsAndCommonMistakes": [],
            },
            "/lessons/bisect-a-line-segment/summary": {
                "lessonTitle": "Bisect a line segment",
                "lessonKeywords": [
                    {
                        "keyword": "midpoint",
                        "description": "The point halfway along a segment.",
                    }
                ],
                "misconceptionsAndCommonMistakes": [
                    {
                        "misconception": (
                            "Pupils may place the midpoint by eye rather than by "
                            "construction."
                        ),
                        "response": "Use intersecting arcs to justify the midpoint.",
                    }
                ],
            },
        }

    def get_json(self, endpoint: str, params: dict[str, object] | None = None) -> object:
        self.calls.append(endpoint)
        return self.responses[endpoint]


def test_select_geometry_threads_filters_to_geometry_threads_in_maths() -> None:
    threads = [
        {
            "threadSlug": "geometry-properties-of-shapes",
            "threadTitle": "Geometry: properties of shapes",
            "subjectSlug": "maths",
        },
        {
            "threadSlug": "number-place-value",
            "threadTitle": "Number: place value",
            "subjectSlug": "maths",
        },
        {
            "threadSlug": "drawing-and-making",
            "threadTitle": "Drawing and making",
            "subjectSlug": "art",
        },
    ]

    selected = select_geometry_threads(threads)

    assert [thread["threadSlug"] for thread in selected] == ["geometry-properties-of-shapes"]


def test_select_geometry_lessons_filters_by_titles_units_and_threads() -> None:
    lessons = [
        {
            "lessonSlug": "bisect-a-line-segment",
            "lessonTitle": "Bisect a line segment",
            "unitTitle": "Constructions and loci",
            "threads": [{"threadTitle": "Geometry: properties of shapes"}],
        },
        {
            "lessonSlug": "numbers-to-1000",
            "lessonTitle": "Numbers to 1000",
            "unitTitle": "Place value",
            "threads": [{"threadTitle": "Number: place value"}],
        },
    ]

    selected = select_geometry_lessons(lessons)

    assert [lesson["lessonSlug"] for lesson in selected] == ["bisect-a-line-segment"]


def test_fetch_oak_curriculum_data_writes_expected_cache_files(tmp_path: Path) -> None:
    client = FakeOakClient()

    combined = fetch_oak_curriculum_data(client=client, output_dir=tmp_path, summary_limit=4)

    assert combined["subject"]["subjectSlug"] == "maths"
    assert [thread["threadSlug"] for thread in combined["geometry_threads"]] == [
        "geometry-properties-of-shapes"
    ]
    assert [lesson["lessonSlug"] for lesson in combined["ks2_geometry_lessons"]] == [
        "identify-acute-and-obtuse-angles"
    ]
    assert [lesson["lessonSlug"] for lesson in combined["ks3_geometry_lessons"]] == [
        "bisect-a-line-segment"
    ]
    assert set(combined["lesson_summaries"]) == {
        "identify-acute-and-obtuse-angles",
        "bisect-a-line-segment",
    }

    for filename in (
        "oak_subject_maths.json",
        "oak_threads_raw.json",
        "oak_geometry_threads.json",
        "oak_geometry_thread_units.json",
        "oak_ks2_geometry_lessons.json",
        "oak_ks3_geometry_lessons.json",
        "oak_geometry_lesson_summaries.json",
        "oak_geometry_data.json",
    ):
        assert (tmp_path / filename).exists()

    saved = json.loads((tmp_path / "oak_geometry_data.json").read_text())
    assert (
        saved["lesson_summaries"]["bisect-a-line-segment"]["lessonTitle"]
        == "Bisect a line segment"
    )
