from pathlib import Path

import pytest

from byrne_euclid.rendering import (
    SCENE_REGISTRY,
    build_manim_command,
    collect_rendered_output,
    resolve_scene_source,
)


def test_scene_registry_contains_initial_scene() -> None:
    assert SCENE_REGISTRY["PropI"] == "src/byrne_euclid/propositions.py"


def test_resolve_scene_source_returns_module_path_for_known_scene() -> None:
    assert resolve_scene_source("PropI") == "src/byrne_euclid/propositions.py"


def test_resolve_scene_source_raises_helpful_error_for_unknown_scene() -> None:
    with pytest.raises(ValueError, match="Available scenes"):
        resolve_scene_source("DefinitelyNotAScene")


def test_build_manim_command_uses_uv_run_and_render() -> None:
    assert build_manim_command(
        module_path="src/byrne_euclid/propositions.py",
        scene_name="PropI",
        quality="m",
        output_format="mp4",
    ) == [
        "uv",
        "run",
        "manim",
        "render",
        "-qm",
        "--format=mp4",
        "src/byrne_euclid/propositions.py",
        "PropI",
    ]


def test_collect_rendered_output_copies_mp4_from_media_tree(tmp_path: Path) -> None:
    media_file = tmp_path / "media" / "videos" / "module" / "720p30" / "PropI.mp4"
    media_file.parent.mkdir(parents=True, exist_ok=True)
    media_file.write_bytes(b"video-data")

    destination = collect_rendered_output(
        scene_name="PropI",
        output_format="mp4",
        media_root=tmp_path / "media",
        output_root=tmp_path / "output",
    )

    assert destination == tmp_path / "output" / "mp4" / "PropI.mp4"
    assert destination.read_bytes() == b"video-data"


def test_collect_rendered_output_copies_png_from_media_tree(tmp_path: Path) -> None:
    media_file = tmp_path / "media" / "images" / "module" / "PropI.png"
    media_file.parent.mkdir(parents=True, exist_ok=True)
    media_file.write_bytes(b"png-data")

    destination = collect_rendered_output(
        scene_name="PropI",
        output_format="png",
        media_root=tmp_path / "media",
        output_root=tmp_path / "output",
    )

    assert destination == tmp_path / "output" / "png" / "PropI.png"
    assert destination.read_bytes() == b"png-data"


def test_collect_rendered_output_accepts_version_suffixed_png_names(tmp_path: Path) -> None:
    media_file = tmp_path / "media" / "images" / "module" / "PropI_ManimCE_v0.20.1.png"
    media_file.parent.mkdir(parents=True, exist_ok=True)
    media_file.write_bytes(b"png-data")

    destination = collect_rendered_output(
        scene_name="PropI",
        output_format="png",
        media_root=tmp_path / "media",
        output_root=tmp_path / "output",
    )

    assert destination == tmp_path / "output" / "png" / "PropI.png"
    assert destination.read_bytes() == b"png-data"
