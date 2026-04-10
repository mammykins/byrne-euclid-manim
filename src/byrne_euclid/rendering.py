from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

SCENE_REGISTRY: dict[str, str] = {
    "PaletteCard": "src/byrne_euclid/definitions.py",
    "PropI": "src/byrne_euclid/propositions.py",
}

VALID_QUALITIES = {"l", "m", "h", "p", "k"}
VALID_OUTPUT_FORMATS = {"gif", "mp4", "png"}


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_scene_source(scene_name: str) -> str:
    try:
        return SCENE_REGISTRY[scene_name]
    except KeyError as error:
        available = ", ".join(sorted(SCENE_REGISTRY))
        raise ValueError(f"Unknown scene '{scene_name}'. Available scenes: {available}") from error


def build_manim_command(
    module_path: str,
    scene_name: str,
    quality: str = "m",
    output_format: str = "mp4",
) -> list[str]:
    if quality not in VALID_QUALITIES:
        raise ValueError(f"Unsupported quality '{quality}'.")
    if output_format not in VALID_OUTPUT_FORMATS:
        raise ValueError(f"Unsupported output format '{output_format}'.")

    command = ["uv", "run", "manim", "render", f"-q{quality}"]
    if output_format == "png":
        command.append("-s")
    else:
        command.append(f"--format={output_format}")
    command.extend([module_path, scene_name])
    return command


def _find_rendered_matches(search_root: Path, scene_name: str, extension: str) -> list[Path]:
    exact_matches = sorted(search_root.glob(f"**/{scene_name}.{extension}"))
    if exact_matches:
        return exact_matches
    return sorted(search_root.glob(f"**/{scene_name}*.{extension}"))


def collect_rendered_output(
    scene_name: str,
    output_format: str,
    media_root: Path | None = None,
    output_root: Path | None = None,
) -> Path:
    resolved_media_root = media_root or (project_root() / "media")
    resolved_output_root = output_root or (project_root() / "output")

    if output_format == "png":
        search_root = resolved_media_root / "images"
        matches = _find_rendered_matches(search_root, scene_name, "png")
        extension = "png"
    else:
        search_root = resolved_media_root / "videos"
        matches = _find_rendered_matches(search_root, scene_name, output_format)
        extension = output_format

    if not matches:
        raise FileNotFoundError(
            f"No rendered {output_format} file found for {scene_name} under {search_root}."
        )

    destination = resolved_output_root / output_format / f"{scene_name}.{extension}"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(matches[0], destination)
    return destination


def render_scene(scene_name: str, quality: str = "m", output_format: str = "mp4") -> Path:
    root = project_root()
    module_path = resolve_scene_source(scene_name)
    command = build_manim_command(
        module_path,
        scene_name,
        quality=quality,
        output_format=output_format,
    )
    logger.info("Rendering %s as %s at quality %s", scene_name, output_format, quality)
    subprocess.run(command, check=True, cwd=root)
    return collect_rendered_output(scene_name, output_format, root / "media", root / "output")
