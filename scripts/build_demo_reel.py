from __future__ import annotations

import argparse
import logging
import os
import subprocess
from collections.abc import Callable
from pathlib import Path

from byrne_euclid.curriculum import load_mapping_entries

logger = logging.getLogger(__name__)

DEFAULT_DEMO_MAPPING_PATH = Path("curriculum/demo_curriculum_preview.yaml")
DEFAULT_DEMO_MP4_DIR = Path("output/mp4")
DEFAULT_DEMO_OUTPUT_DIR = Path("output/demo")
DEFAULT_DEMO_REEL_OUTPUT = DEFAULT_DEMO_OUTPUT_DIR / "demo_curriculum_preview_reel.mp4"
DEFAULT_DEMO_REEL_CONCAT = DEFAULT_DEMO_OUTPUT_DIR / "demo_curriculum_preview_reel.concat.txt"


def load_demo_reel_scene_names(mapping_path: Path = DEFAULT_DEMO_MAPPING_PATH) -> list[str]:
    return [entry.scene for entry in load_mapping_entries(mapping_path)]


def build_demo_reel_sources(
    scene_names: list[str],
    mp4_dir: Path = DEFAULT_DEMO_MP4_DIR,
) -> list[Path]:
    return [mp4_dir / f"{scene_name}.mp4" for scene_name in scene_names]


def _display_source_path(source: Path, mp4_dir: Path) -> str:
    if mp4_dir.name == "mp4" and mp4_dir.parent.name == "output":
        return str(Path("output/mp4") / source.name)
    return str(source)


def ensure_demo_reel_sources_exist(sources: list[Path], mp4_dir: Path) -> None:
    missing_sources = [source for source in sources if not source.exists()]
    if missing_sources:
        missing = _display_source_path(missing_sources[0], mp4_dir)
        raise FileNotFoundError(f"Missing demo reel source video: {missing}")


def write_concat_manifest(sources: list[Path], concat_path: Path) -> None:
    concat_path.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for source in sources:
        relative_path = os.path.relpath(source, concat_path.parent).replace(os.sep, "/")
        lines.append(f"file '{relative_path}'")
    concat_path.write_text("\n".join(lines) + "\n")


def build_ffmpeg_command(concat_path: Path, output_path: Path) -> list[str]:
    return [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_path),
        "-c",
        "copy",
        str(output_path),
    ]


def run_command(command: list[str]) -> None:
    subprocess.run(command, check=True)


def build_demo_reel(
    scene_names: list[str] | None = None,
    mapping_path: Path = DEFAULT_DEMO_MAPPING_PATH,
    mp4_dir: Path = DEFAULT_DEMO_MP4_DIR,
    output_dir: Path = DEFAULT_DEMO_OUTPUT_DIR,
    run_command: Callable[[list[str]], None] = run_command,
) -> Path:
    ordered_scene_names = scene_names or load_demo_reel_scene_names(mapping_path)
    sources = build_demo_reel_sources(ordered_scene_names, mp4_dir)
    ensure_demo_reel_sources_exist(sources, mp4_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / DEFAULT_DEMO_REEL_OUTPUT.name
    concat_path = output_dir / DEFAULT_DEMO_REEL_CONCAT.name

    write_concat_manifest(sources, concat_path)
    command = build_ffmpeg_command(concat_path, output_path)
    run_command(command)
    logger.info("Wrote stitched demo reel to %s", output_path)
    return output_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Stitch the synthetic curriculum preview scenes into one demo reel"
    )
    parser.add_argument(
        "--mapping",
        default=str(DEFAULT_DEMO_MAPPING_PATH),
        help="Path to the synthetic demo curriculum mapping YAML",
    )
    parser.add_argument(
        "--mp4-dir",
        default=str(DEFAULT_DEMO_MP4_DIR),
        help="Directory containing the source MP4 scene renders",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_DEMO_OUTPUT_DIR),
        help="Directory where the stitched demo reel will be written",
    )
    return parser


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    args = build_parser().parse_args()
    output_path = build_demo_reel(
        mapping_path=Path(args.mapping),
        mp4_dir=Path(args.mp4_dir),
        output_dir=Path(args.output_dir),
    )
    logger.info("Demo reel ready at %s", output_path)


if __name__ == "__main__":
    main()
