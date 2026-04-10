from __future__ import annotations

import argparse
import logging
from collections.abc import Callable
from pathlib import Path

from byrne_euclid.rendering import SCENE_REGISTRY, VALID_QUALITIES, render_scene

logger = logging.getLogger(__name__)


def build_render_jobs(
    scene_registry: dict[str, str] | None = None,
    output_formats: tuple[str, ...] = ("mp4", "png"),
) -> list[tuple[str, str]]:
    registry = scene_registry or SCENE_REGISTRY
    return [
        (scene_name, output_format)
        for scene_name in sorted(registry)
        for output_format in output_formats
    ]


def render_all_scenes(
    quality: str = "h",
    scene_registry: dict[str, str] | None = None,
    output_formats: tuple[str, ...] = ("mp4", "png"),
    render_func: Callable[[str, str, str], Path] = render_scene,
) -> list[Path]:
    destinations: list[Path] = []
    for scene_name, output_format in build_render_jobs(scene_registry, output_formats):
        logger.info(
            "Rendering %s as %s at quality %s",
            scene_name,
            output_format,
            quality,
        )
        destinations.append(render_func(scene_name, quality, output_format))
    return destinations


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render every Byrne-Euclid scene")
    parser.add_argument("--quality", "-q", default="h", choices=sorted(VALID_QUALITIES))
    parser.add_argument(
        "--formats",
        default="mp4,png",
        help="Comma-separated output formats to render, e.g. mp4,png",
    )
    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = build_parser().parse_args()
    output_formats = tuple(
        output_format.strip()
        for output_format in args.formats.split(",")
        if output_format.strip()
    )
    destinations = render_all_scenes(quality=args.quality, output_formats=output_formats)
    logger.info("Rendered %s files", len(destinations))


if __name__ == "__main__":
    main()
