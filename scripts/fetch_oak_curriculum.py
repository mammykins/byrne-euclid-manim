from __future__ import annotations

import argparse
import json
import logging
import os
import re
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


def _coalesce(item: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = item.get(key)
        if value is not None:
            return value
    return None


def _normalise_text(*parts: object) -> str:
    combined = " ".join(str(part) for part in parts if part).casefold()
    return re.sub(r"[^a-z0-9]+", " ", combined).strip()


def _contains_geometry_term(*parts: object) -> bool:
    combined = f" {_normalise_text(*parts)} "
    return any(f" {term} " in combined for term in GEOMETRY_TERMS)


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


def _dedupe_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        cleaned = value.strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        deduped.append(cleaned)
    return deduped


def _normalise_thread(thread: dict[str, Any]) -> dict[str, Any] | None:
    slug = _coalesce(thread, "threadSlug", "slug")
    title = _coalesce(thread, "threadTitle", "title")
    if not isinstance(slug, str) or not isinstance(title, str):
        return None

    normalised = {
        "threadSlug": slug,
        "threadTitle": title,
    }
    subject_slug = thread.get("subjectSlug")
    if isinstance(subject_slug, str):
        normalised["subjectSlug"] = subject_slug
    return normalised


def select_geometry_threads(threads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = []
    for thread in threads:
        normalised = _normalise_thread(thread)
        if normalised is None:
            continue
        subject_slug = normalised.get("subjectSlug")
        if subject_slug and subject_slug != "maths":
            continue
        if _contains_geometry_term(
            normalised.get("threadTitle"),
            normalised.get("threadSlug"),
        ):
            selected.append(normalised)
    return _dedupe_by_slug(selected, "threadSlug")


def flatten_unit_groups(unit_groups: object) -> list[dict[str, Any]]:
    if not isinstance(unit_groups, list):
        raise ValueError("Expected unit payload to be a list.")

    flattened: list[dict[str, Any]] = []
    for item in unit_groups:
        if not isinstance(item, dict):
            continue

        nested_units = item.get("units")
        if isinstance(nested_units, list):
            year_order = _coalesce(item, "yearOrder", "year")
            year_slug = item.get("yearSlug")
            year_title = item.get("yearTitle")
            if year_order is not None and not year_slug:
                year_slug = f"year-{year_order}"
            if year_order is not None and not year_title:
                year_title = f"Year {year_order}"

            for unit in nested_units:
                if not isinstance(unit, dict):
                    continue
                row = dict(unit)
                if year_slug and "yearSlug" not in row:
                    row["yearSlug"] = year_slug
                if year_title and "yearTitle" not in row:
                    row["yearTitle"] = year_title
                if year_order is not None and "yearOrder" not in row:
                    row["yearOrder"] = year_order
                flattened.append(row)
            continue

        flattened.append(dict(item))

    return _dedupe_by_slug(flattened, "unitSlug")


def select_geometry_units(units: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = []
    for unit in units:
        if _contains_geometry_term(unit.get("unitTitle"), unit.get("unitSlug")):
            selected.append(unit)
    return _dedupe_by_slug(selected, "unitSlug")


def _extract_thread_slugs(lesson: dict[str, Any]) -> list[str]:
    values = lesson.get("threadSlugs")
    if isinstance(values, list):
        return _dedupe_strings([str(value) for value in values if value])

    extracted: list[str] = []
    for thread in lesson.get("threads", []):
        if not isinstance(thread, dict):
            continue
        slug = _coalesce(thread, "threadSlug", "slug")
        if isinstance(slug, str):
            extracted.append(slug)
    return _dedupe_strings(extracted)


def flatten_lesson_groups(
    lesson_groups: object,
    *,
    key_stage_slug: str,
    unit_slug: str | None = None,
    unit_title: str | None = None,
    year_slug: str | None = None,
    year_title: str | None = None,
    thread_slugs: list[str] | None = None,
) -> list[dict[str, Any]]:
    if not isinstance(lesson_groups, list):
        raise ValueError("Expected lesson payload to be a list.")

    flattened: list[dict[str, Any]] = []
    for item in lesson_groups:
        if not isinstance(item, dict):
            continue

        nested_lessons = item.get("lessons")
        if isinstance(nested_lessons, list):
            wrapper_unit_slug = _coalesce(item, "unitSlug") or unit_slug
            wrapper_unit_title = item.get("unitTitle") or unit_title
            wrapper_year_slug = item.get("yearSlug") or year_slug
            wrapper_year_title = item.get("yearTitle") or year_title

            for lesson in nested_lessons:
                if not isinstance(lesson, dict):
                    continue
                row = dict(lesson)
                if wrapper_unit_slug and "unitSlug" not in row:
                    row["unitSlug"] = wrapper_unit_slug
                if wrapper_unit_title and "unitTitle" not in row:
                    row["unitTitle"] = wrapper_unit_title
                if wrapper_year_slug and "yearSlug" not in row:
                    row["yearSlug"] = wrapper_year_slug
                if wrapper_year_title and "yearTitle" not in row:
                    row["yearTitle"] = wrapper_year_title
                row["keyStageSlug"] = row.get("keyStageSlug") or key_stage_slug
                row["threadSlugs"] = _dedupe_strings(
                    _extract_thread_slugs(row) + list(thread_slugs or [])
                )
                flattened.append(row)
            continue

        row = dict(item)
        if unit_slug and "unitSlug" not in row:
            row["unitSlug"] = unit_slug
        if unit_title and "unitTitle" not in row:
            row["unitTitle"] = unit_title
        if year_slug and "yearSlug" not in row:
            row["yearSlug"] = year_slug
        if year_title and "yearTitle" not in row:
            row["yearTitle"] = year_title
        row["keyStageSlug"] = row.get("keyStageSlug") or key_stage_slug
        row["threadSlugs"] = _dedupe_strings(_extract_thread_slugs(row) + list(thread_slugs or []))
        flattened.append(row)

    return _dedupe_by_slug(flattened, "lessonSlug")


def build_unit_thread_index(
    geometry_thread_units: dict[str, list[dict[str, Any]]],
) -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for thread_slug, units in geometry_thread_units.items():
        for unit in units:
            unit_slug = unit.get("unitSlug")
            if not isinstance(unit_slug, str):
                continue
            index.setdefault(unit_slug, []).append(thread_slug)
    return {unit_slug: _dedupe_strings(thread_slugs) for unit_slug, thread_slugs in index.items()}


def attach_thread_slugs_to_units(
    units: list[dict[str, Any]],
    unit_thread_index: dict[str, list[str]],
) -> list[dict[str, Any]]:
    attached: list[dict[str, Any]] = []
    for unit in units:
        unit_slug = unit.get("unitSlug")
        if not isinstance(unit_slug, str):
            continue
        thread_slugs = unit_thread_index.get(unit_slug)
        if not thread_slugs:
            continue
        row = dict(unit)
        row["threadSlugs"] = list(thread_slugs)
        attached.append(row)
    return _dedupe_by_slug(attached, "unitSlug")


def fetch_lessons_for_units(
    client: OakClientProtocol,
    key_stage_slug: str,
    units: list[dict[str, Any]],
    unit_thread_index: dict[str, list[str]],
) -> list[dict[str, Any]]:
    lessons: list[dict[str, Any]] = []
    for unit in units:
        unit_slug = unit.get("unitSlug")
        if not isinstance(unit_slug, str):
            continue
        lesson_groups = client.get_json(
            f"/key-stages/{key_stage_slug}/subject/maths/lessons",
            params={"unit": unit_slug},
        )
        lessons.extend(
            flatten_lesson_groups(
                lesson_groups,
                key_stage_slug=key_stage_slug,
                unit_slug=unit_slug,
                unit_title=unit.get("unitTitle"),
                year_slug=unit.get("yearSlug"),
                year_title=unit.get("yearTitle"),
                thread_slugs=unit_thread_index.get(unit_slug, []),
            )
        )
    return _dedupe_by_slug(lessons, "lessonSlug")


def select_summary_slugs(
    lessons: list[dict[str, Any]],
    limit: int | None = None,
) -> list[str]:
    slugs = []
    max_items = None if limit is None or limit <= 0 else limit
    for lesson in lessons:
        slug = lesson.get("lessonSlug")
        if slug and slug not in slugs:
            slugs.append(slug)
        if max_items is not None and len(slugs) >= max_items:
            break
    return slugs


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def resolve_api_key() -> str | None:
    return os.environ.get("OAK_OPEN_API_KEY") or os.environ.get("OAK_API_KEY")


def fetch_oak_curriculum_data(
    client: OakClientProtocol,
    output_dir: Path,
    summary_limit: int = 0,
) -> dict[str, Any]:
    subject = client.get_json("/subjects/maths")
    threads_raw = client.get_json("/threads")
    if not isinstance(threads_raw, list):
        raise ValueError("Expected /threads to return a list.")

    candidate_geometry_threads = select_geometry_threads(threads_raw)
    candidate_thread_units = {
        thread["threadSlug"]: flatten_unit_groups(
            client.get_json(f"/threads/{thread['threadSlug']}/units")
        )
        for thread in candidate_geometry_threads
    }
    unit_thread_index = build_unit_thread_index(candidate_thread_units)

    ks2_units_raw = client.get_json("/key-stages/ks2/subject/maths/units")
    ks3_units_raw = client.get_json("/key-stages/ks3/subject/maths/units")
    ks2_geometry_units = attach_thread_slugs_to_units(
        select_geometry_units(flatten_unit_groups(ks2_units_raw)),
        unit_thread_index,
    )
    ks3_geometry_units = attach_thread_slugs_to_units(
        select_geometry_units(flatten_unit_groups(ks3_units_raw)),
        unit_thread_index,
    )

    relevant_thread_slugs = {
        thread_slug
        for unit in ks2_geometry_units + ks3_geometry_units
        for thread_slug in unit.get("threadSlugs", [])
        if isinstance(thread_slug, str)
    }
    geometry_threads = [
        thread
        for thread in candidate_geometry_threads
        if thread["threadSlug"] in relevant_thread_slugs
    ]
    geometry_thread_units = {
        thread_slug: candidate_thread_units[thread_slug] for thread_slug in relevant_thread_slugs
    }

    ks2_geometry_lessons = fetch_lessons_for_units(
        client=client,
        key_stage_slug="ks2",
        units=ks2_geometry_units,
        unit_thread_index=unit_thread_index,
    )
    ks3_geometry_lessons = fetch_lessons_for_units(
        client=client,
        key_stage_slug="ks3",
        units=ks3_geometry_units,
        unit_thread_index=unit_thread_index,
    )

    summary_slugs = select_summary_slugs(
        ks2_geometry_lessons + ks3_geometry_lessons,
        limit=summary_limit,
    )
    lesson_summaries = {slug: client.get_json(f"/lessons/{slug}/summary") for slug in summary_slugs}

    combined = {
        "subject": subject,
        "geometry_threads": geometry_threads,
        "geometry_thread_units": geometry_thread_units,
        "geometry_unit_thread_slugs": unit_thread_index,
        "ks2_geometry_units": ks2_geometry_units,
        "ks3_geometry_units": ks3_geometry_units,
        "ks2_geometry_lessons": ks2_geometry_lessons,
        "ks3_geometry_lessons": ks3_geometry_lessons,
        "lesson_summaries": lesson_summaries,
    }

    write_json(output_dir / "oak_subject_maths.json", subject)
    write_json(output_dir / "oak_threads_raw.json", threads_raw)
    write_json(output_dir / "oak_geometry_threads.json", geometry_threads)
    write_json(output_dir / "oak_geometry_thread_units.json", geometry_thread_units)
    write_json(output_dir / "oak_geometry_unit_thread_slugs.json", unit_thread_index)
    write_json(output_dir / "oak_ks2_geometry_units.json", ks2_geometry_units)
    write_json(output_dir / "oak_ks3_geometry_units.json", ks3_geometry_units)
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
        default=0,
        help="Maximum number of lesson summaries to fetch (0 means all geometry lessons)",
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
        logger.info("Would fetch /key-stages/ks2/subject/maths/units")
        logger.info("Would fetch /key-stages/ks3/subject/maths/units")
        logger.info(
            "Would fetch /key-stages/{keyStage}/subject/maths/lessons?unit={unitSlug} "
            "for each selected geometry unit"
        )
        logger.info(
            "Would fetch /lessons/{lessonSlug}/summary for %s geometry lessons",
            "all" if args.summary_limit <= 0 else args.summary_limit,
        )
        logger.info("Would write Oak cache files into %s", output_dir)
        return

    api_key = resolve_api_key()
    if not api_key:
        raise SystemExit(
            "Missing OAK_OPEN_API_KEY or OAK_API_KEY. Re-run with "
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
