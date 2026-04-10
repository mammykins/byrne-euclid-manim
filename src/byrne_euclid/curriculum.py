from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from byrne_euclid.rendering import SCENE_REGISTRY

KEY_STAGE_ORDER = {"KS1": 0, "KS2": 1, "KS3": 2, "KS4": 3}


class NCReference(BaseModel):
    key_stage: str
    year: int | None = None
    domain: str
    statement: str


class MappingEntry(BaseModel):
    scene: str
    euclid_type: str
    euclid_numbers: list[int] = Field(default_factory=list)
    title: str
    description: str
    alt_text: str
    duration_seconds: int | float | None = None
    nc_references: list[NCReference] = Field(default_factory=list)
    oak_lesson_slugs: list[str] = Field(default_factory=list)
    oak_thread_slugs: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    misconceptions: list[str] = Field(default_factory=list)


class ManifestAnimation(BaseModel):
    scene_class: str
    title: str
    euclid_book: int
    euclid_type: str
    euclid_numbers: list[int]
    description: str
    duration_seconds: int | float | None = None
    nc_references: list[NCReference]
    oak_lesson_slugs: list[str]
    oak_thread_slugs: list[str]
    keywords: list[str]
    misconceptions: list[str]
    alt_text: str
    files: dict[str, str]


class CurriculumManifest(BaseModel):
    version: str
    generated_at: str
    animations: list[ManifestAnimation]


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


def _isoformat_z(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_mapping_entries(
    mapping_path: Path,
    scene_registry: dict[str, str] | None = None,
) -> list[MappingEntry]:
    payload = yaml.safe_load(mapping_path.read_text()) or []
    entries = [MappingEntry.model_validate(item) for item in payload]
    registry = scene_registry or SCENE_REGISTRY

    unknown_scenes = sorted({entry.scene for entry in entries if entry.scene not in registry})
    if unknown_scenes:
        unknown = ", ".join(unknown_scenes)
        raise ValueError(f"Unknown scene names in curriculum mapping: {unknown}")

    return entries


def _summary_lookup(oak_data: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    if not oak_data:
        return {}
    summaries = oak_data.get("lesson_summaries", {})
    if isinstance(summaries, dict):
        return summaries
    return {}


def _enrich_keywords(entry: MappingEntry, summaries: dict[str, dict[str, Any]]) -> list[str]:
    values = list(entry.keywords)
    for slug in entry.oak_lesson_slugs:
        summary = summaries.get(slug, {})
        for keyword in summary.get("lessonKeywords", []):
            if isinstance(keyword, dict) and keyword.get("keyword"):
                values.append(keyword["keyword"])
    return _dedupe_strings(values)


def _enrich_misconceptions(
    entry: MappingEntry,
    summaries: dict[str, dict[str, Any]],
) -> list[str]:
    values = list(entry.misconceptions)
    for slug in entry.oak_lesson_slugs:
        summary = summaries.get(slug, {})
        for item in summary.get("misconceptionsAndCommonMistakes", []):
            if isinstance(item, dict) and item.get("misconception"):
                values.append(item["misconception"])
    return _dedupe_strings(values)


def build_manifest(
    entries: list[MappingEntry],
    oak_data: dict[str, Any] | None = None,
    generated_at: datetime | None = None,
    version: str = "0.1.0",
) -> dict[str, Any]:
    summaries = _summary_lookup(oak_data)
    built_entries = []

    for entry in entries:
        built_entries.append(
            ManifestAnimation(
                scene_class=entry.scene,
                title=entry.title,
                euclid_book=1,
                euclid_type=entry.euclid_type,
                euclid_numbers=entry.euclid_numbers,
                description=entry.description,
                duration_seconds=entry.duration_seconds,
                nc_references=entry.nc_references,
                oak_lesson_slugs=_dedupe_strings(entry.oak_lesson_slugs),
                oak_thread_slugs=_dedupe_strings(entry.oak_thread_slugs),
                keywords=_enrich_keywords(entry, summaries),
                misconceptions=_enrich_misconceptions(entry, summaries),
                alt_text=entry.alt_text,
                files={
                    "gif": f"output/gif/{entry.scene}.gif",
                    "mp4": f"output/mp4/{entry.scene}.mp4",
                    "png": f"output/png/{entry.scene}.png",
                },
            )
        )

    timestamp = generated_at or datetime.now(UTC)
    manifest = CurriculumManifest(
        version=version,
        generated_at=_isoformat_z(timestamp),
        animations=built_entries,
    )
    return manifest.model_dump(mode="json")


def _euclid_reference(entry: dict[str, Any]) -> str:
    numbers = entry.get("euclid_numbers", [])
    if not numbers:
        return "Book I"
    formatted_numbers = ", ".join(str(number) for number in numbers)
    return f"Book I {entry['euclid_type']} {formatted_numbers}"


def _key_stage_sort_key(key_stage: str) -> tuple[int, str]:
    return (KEY_STAGE_ORDER.get(key_stage, 99), key_stage)


def _group_manifest_entries(
    manifest: dict[str, Any],
) -> dict[str, dict[int | None, list[tuple[dict[str, Any], dict[str, Any]]]]]:
    grouped: dict[str, dict[int | None, list[tuple[dict[str, Any], dict[str, Any]]]]] = {}

    for animation in manifest.get("animations", []):
        for reference in animation.get("nc_references", []):
            key_stage = reference["key_stage"]
            year = reference.get("year")
            grouped.setdefault(key_stage, {}).setdefault(year, []).append((animation, reference))

    return grouped


def _render_grouped_mapping_sections(
    grouped: dict[str, dict[int | None, list[tuple[dict[str, Any], dict[str, Any]]]]],
    lesson_label: str,
    thread_label: str,
) -> list[str]:
    lines: list[str] = []

    for key_stage in sorted(grouped, key=_key_stage_sort_key):
        lines.append(f"## {key_stage}")
        years = grouped[key_stage]
        for year in sorted(
            years,
            key=lambda value: (value is None, value if value is not None else 999),
        ):
            year_heading = "General" if year is None else f"Year {year}"
            lines.append(f"### {year_heading}")
            for animation, reference in sorted(
                years[year],
                key=lambda item: (item[0]["title"], item[0]["scene_class"]),
            ):
                lines.append(
                    f"- `{animation['scene_class']}` — **{animation['title']}** "
                    f"({_euclid_reference(animation)})"
                )
                lines.append(f"  - NC: {reference['statement']}")
                lines.append(f"  - Domain: {reference['domain']}")
                lesson_slugs = animation.get("oak_lesson_slugs") or []
                thread_slugs = animation.get("oak_thread_slugs") or []
                lines.append(
                    f"  - {lesson_label}: "
                    + (
                        ", ".join(f"`{slug}`" for slug in lesson_slugs)
                        if lesson_slugs
                        else "Draft mapping pending"
                    )
                )
                lines.append(
                    f"  - {thread_label}: "
                    + (
                        ", ".join(f"`{slug}`" for slug in thread_slugs)
                        if thread_slugs
                        else "Draft mapping pending"
                    )
                )
                lines.append(
                    "  - Files: "
                    + ", ".join(
                        f"`{path}`"
                        for path in (
                            animation["files"]["gif"],
                            animation["files"]["mp4"],
                            animation["files"]["png"],
                        )
                    )
                )

    return lines


def render_curriculum_mapping_markdown(manifest: dict[str, Any]) -> str:
    grouped = _group_manifest_entries(manifest)

    lines = [
        "# Curriculum mapping",
        (
            "This document maps each animation to its curriculum position in the "
            "English national curriculum for mathematics."
        ),
        (
            "Contains public sector information licensed under the Open Government "
            "Licence v3.0. Oak National Academy content is used under the Open "
            "Government Licence."
        ),
    ]
    lines.extend(
        _render_grouped_mapping_sections(
            grouped,
            lesson_label="Oak lessons",
            thread_label="Oak threads",
        )
    )

    return "\n".join(lines) + "\n"


def render_curriculum_preview_markdown(manifest: dict[str, Any]) -> str:
    grouped = _group_manifest_entries(manifest)
    lines = [
        "# Demo curriculum mapping",
        (
            "This synthetic preview shows how the curriculum packaging will look once "
            "live Oak-derived metadata is available again."
        ),
        (
            "The lesson and thread slugs below are hand-authored demo values, used "
            "purely to preview the final shape of the enriched outputs."
        ),
    ]
    lines.extend(
        _render_grouped_mapping_sections(
            grouped,
            lesson_label="Preview lesson slugs",
            thread_label="Preview thread slugs",
        )
    )

    return "\n".join(lines) + "\n"


def render_curriculum_showcase_markdown(
    manifest: dict[str, Any],
    title: str = "Curriculum showcase",
) -> str:
    lines = [
        f"# {title}",
        (
            "This synthetic preview shows how enriched curriculum metadata can sit "
            "beside the rendered media files."
        ),
        (
            "Where live Oak data is unavailable, the lesson and thread slugs below "
            "are preview values rather than authoritative curriculum identifiers."
        ),
    ]

    for animation in sorted(
        manifest.get("animations", []),
        key=lambda item: (item["title"], item["scene_class"]),
    ):
        lines.append(f"## {animation['title']}")
        lines.append(f"- Scene: `{animation['scene_class']}`")
        lines.append(f"- Euclid: {_euclid_reference(animation)}")
        lines.append(f"- Description: {animation['description']}")

        nc_references = animation.get("nc_references") or []
        if nc_references:
            lines.append("- Curriculum links:")
            for reference in nc_references:
                year = reference.get("year")
                year_label = "General" if year is None else f"Year {year}"
                lines.append(
                    f"  - {reference['key_stage']} {year_label} — "
                    f"{reference['domain']}: {reference['statement']}"
                )
        else:
            lines.append("- Curriculum links: None recorded")

        lesson_slugs = animation.get("oak_lesson_slugs") or []
        thread_slugs = animation.get("oak_thread_slugs") or []
        keywords = animation.get("keywords") or []
        misconceptions = animation.get("misconceptions") or []

        lines.append(
            "- Lesson slugs: "
            + (
                ", ".join(f"`{slug}`" for slug in lesson_slugs)
                if lesson_slugs
                else "None recorded"
            )
        )
        lines.append(
            "- Thread slugs: "
            + (
                ", ".join(f"`{slug}`" for slug in thread_slugs)
                if thread_slugs
                else "None recorded"
            )
        )
        lines.append(
            "- Keywords: "
            + (
                ", ".join(f"`{keyword}`" for keyword in keywords)
                if keywords
                else "None recorded"
            )
        )
        if misconceptions:
            lines.append("- Misconceptions:")
            for misconception in misconceptions:
                lines.append(f"  - {misconception}")
        else:
            lines.append("- Misconceptions: None recorded")
        lines.append(f"- Alt text: {animation['alt_text']}")
        lines.append(
            "- Files: "
            + ", ".join(
                f"`{animation['files'][format_name]}`"
                for format_name in ("gif", "mp4", "png")
            )
        )

    return "\n".join(lines) + "\n"
