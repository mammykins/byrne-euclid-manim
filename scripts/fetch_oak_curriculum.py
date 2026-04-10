from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
from typing import Any, Protocol

import httpx

BASE_URL = "https://open-api.thenational.academy/api/v0"
GEOMETRY_TERMS = (
    "geometry",
    "shape",
    "shapes",
    "angle",
    "angles",
    "triangle",
    "triangles",
    "quadrilateral",
    "quadrilaterals",
    "parallel",
    "perpendicular",
    "construction",
    "constructions",
    "loci",
    "circle",
    "circles",
    "polygon",
    "polygons",
    "radius",
    "diameter",
    "bisect",
    "line segment",
    "straight line",
    "midpoint",
)

logger = logging.getLogger(__name__)


class OakClientProtocol(Protocol):
    def get_json(self, endpoint: str, params: dict[str, object] | None = None) -> object: ...


class OakApiClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = BASE_URL,
        timeout_seconds: float = 30.0,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=timeout_seconds,
        )

    def get_json(self, endpoint: str, params: dict[str, object] | None = None) -> object:
        response = self._client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()


def _normalise_text(*parts: object) -> str:
    return " ".join(str(part) for part in parts if part).casefold()


def _contains_geometry_term(*parts: object) -> bool:
    combined = _normalise_text(*parts)
    return any(term in combined for term in GEOMETRY_TERMS)


def _dedupe_by_slug(items: list[dict[str, Any]], slug_key: str) -> list[dict[str, Any]]:
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for item in items:
        slug = item.get(slug_key)
        if not slug or slug in seen:
            continue
        seen.add(slug)
        deduped.append(item)
    return deduped


def select_geometry_threads(threads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = []
    for thread in threads:
        subject_slug = thread.get("subjectSlug")
        if subject_slug and subject_slug != "maths":
            continue
        if _contains_geometry_term(thread.get("threadTitle"), thread.get("threadSlug")):
            selected.append(thread)
    return _dedupe_by_slug(selected, "threadSlug")


def select_geometry_lessons(lessons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = []
    for lesson in lessons:
        thread_titles = [
            thread.get("threadTitle", "")
            for thread in lesson.get("threads", [])
            if isinstance(thread, dict)
        ]
        if _contains_geometry_term(
            lesson.get("lessonTitle"),
            lesson.get("unitTitle"),
            lesson.get("unitSlug"),
            *thread_titles,
        ):
            selected.append(lesson)
    return _dedupe_by_slug(selected, "lessonSlug")


def select_summary_slugs(lessons: list[dict[str, Any]], limit: int = 12) -> list[str]:
    slugs = []
    for lesson in lessons:
        slug = lesson.get("lessonSlug")
        if slug and slug not in slugs:
            slugs.append(slug)
        if len(slugs) >= limit:
            break
    return slugs


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def fetch_oak_curriculum_data(
    client: OakClientProtocol,
    output_dir: Path,
    summary_limit: int = 12,
) -> dict[str, Any]:
    subject = client.get_json("/subjects/maths")
    threads_raw = client.get_json("/threads")
    if not isinstance(threads_raw, list):
        raise ValueError("Expected /threads to return a list.")

    geometry_threads = select_geometry_threads(threads_raw)
    geometry_thread_units = {
        thread["threadSlug"]: client.get_json(
            f"/threads/{thread['threadSlug']}/units"
        )
        for thread in geometry_threads
    }

    ks2_lessons_raw = client.get_json("/key-stages/ks2/subject/maths/lessons")
    ks3_lessons_raw = client.get_json("/key-stages/ks3/subject/maths/lessons")
    if not isinstance(ks2_lessons_raw, list) or not isinstance(ks3_lessons_raw, list):
        raise ValueError("Expected key-stage lesson endpoints to return lists.")

    ks2_geometry_lessons = select_geometry_lessons(ks2_lessons_raw)
    ks3_geometry_lessons = select_geometry_lessons(ks3_lessons_raw)

    summary_slugs = select_summary_slugs(
        ks2_geometry_lessons + ks3_geometry_lessons,
        limit=summary_limit,
    )
    lesson_summaries = {
        slug: client.get_json(f"/lessons/{slug}/summary")
        for slug in summary_slugs
    }

    combined = {
        "subject": subject,
        "geometry_threads": geometry_threads,
        "geometry_thread_units": geometry_thread_units,
        "ks2_geometry_lessons": ks2_geometry_lessons,
        "ks3_geometry_lessons": ks3_geometry_lessons,
        "lesson_summaries": lesson_summaries,
    }

    write_json(output_dir / "oak_subject_maths.json", subject)
    write_json(output_dir / "oak_threads_raw.json", threads_raw)
    write_json(output_dir / "oak_geometry_threads.json", geometry_threads)
    write_json(output_dir / "oak_geometry_thread_units.json", geometry_thread_units)
    write_json(output_dir / "oak_ks2_geometry_lessons.json", ks2_geometry_lessons)
    write_json(output_dir / "oak_ks3_geometry_lessons.json", ks3_geometry_lessons)
    write_json(output_dir / "oak_geometry_lesson_summaries.json", lesson_summaries)
    write_json(output_dir / "oak_geometry_data.json", combined)

    return combined


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch and cache Oak maths geometry curriculum data"
    )
    parser.add_argument(
        "--output-dir",
        default="curriculum",
        help="Directory where the Oak cache JSON files will be written",
    )
    parser.add_argument(
        "--summary-limit",
        type=int,
        default=12,
        help="Maximum number of lesson summaries to fetch",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Log the planned Oak endpoints without making any API calls",
    )
    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = build_parser().parse_args()
    output_dir = Path(args.output_dir)

    if args.dry_run:
        logger.info("Would fetch /subjects/maths")
        logger.info("Would fetch /threads")
        logger.info("Would fetch /threads/{threadSlug}/units for each geometry thread")
        logger.info("Would fetch /key-stages/ks2/subject/maths/lessons")
        logger.info("Would fetch /key-stages/ks3/subject/maths/lessons")
        logger.info(
            "Would fetch /lessons/{lessonSlug}/summary for up to %s lessons",
            args.summary_limit,
        )
        logger.info("Would write Oak cache files into %s", output_dir)
        return

    api_key = os.environ.get("OAK_API_KEY")
    if not api_key:
        raise SystemExit(
            "Missing OAK_API_KEY. Re-run with "
            "`uv run --env-file .env python scripts/fetch_oak_curriculum.py`."
        )

    client = OakApiClient(api_key)
    combined = fetch_oak_curriculum_data(
        client=client,
        output_dir=output_dir,
        summary_limit=args.summary_limit,
    )
    logger.info(
        "Cached Oak geometry data for %s threads, %s KS2 lessons, and %s KS3 lessons",
        len(combined["geometry_threads"]),
        len(combined["ks2_geometry_lessons"]),
        len(combined["ks3_geometry_lessons"]),
    )


if __name__ == "__main__":
    main()
