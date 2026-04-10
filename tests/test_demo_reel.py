from pathlib import Path

import pytest

from scripts.build_demo_reel import (
    DEFAULT_DEMO_REEL_OUTPUT,
    build_demo_reel,
    build_demo_reel_sources,
    load_demo_reel_scene_names,
)


def test_build_demo_reel_scene_names_follow_demo_preview_order() -> None:
    assert load_demo_reel_scene_names() == [
        "DefAngleTypes",
        "PropXI",
        "PropXXXII",
    ]


def test_build_demo_reel_inputs_resolve_to_expected_mp4_paths() -> None:
    assert build_demo_reel_sources(
        ["DefAngleTypes", "PropXI", "PropXXXII"],
        mp4_dir=Path("output/mp4"),
    ) == [
        Path("output/mp4/DefAngleTypes.mp4"),
        Path("output/mp4/PropXI.mp4"),
        Path("output/mp4/PropXXXII.mp4"),
    ]


def test_build_demo_reel_writes_concat_manifest_and_invokes_ffmpeg(tmp_path: Path) -> None:
    mp4_dir = tmp_path / "output" / "mp4"
    mp4_dir.mkdir(parents=True)
    for scene_name in ("DefAngleTypes", "PropXI", "PropXXXII"):
        (mp4_dir / f"{scene_name}.mp4").write_bytes(b"fake mp4")

    commands: list[list[str]] = []

    def fake_run(command: list[str]) -> None:
        commands.append(command)

    output_path = build_demo_reel(
        scene_names=["DefAngleTypes", "PropXI", "PropXXXII"],
        mp4_dir=mp4_dir,
        output_dir=tmp_path / "output" / "demo",
        run_command=fake_run,
    )

    concat_path = tmp_path / "output" / "demo" / "demo_curriculum_preview_reel.concat.txt"
    assert output_path == tmp_path / "output" / "demo" / DEFAULT_DEMO_REEL_OUTPUT.name
    assert concat_path.exists()
    assert concat_path.read_text() == (
        "file '../mp4/DefAngleTypes.mp4'\n"
        "file '../mp4/PropXI.mp4'\n"
        "file '../mp4/PropXXXII.mp4'\n"
    )
    assert commands == [
        [
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
            str(tmp_path / "output" / "demo" / "demo_curriculum_preview_reel.mp4"),
        ]
    ]


def test_build_demo_reel_fails_cleanly_when_a_source_video_is_missing(tmp_path: Path) -> None:
    mp4_dir = tmp_path / "output" / "mp4"
    mp4_dir.mkdir(parents=True)
    (mp4_dir / "DefAngleTypes.mp4").write_bytes(b"fake mp4")
    (mp4_dir / "PropXI.mp4").write_bytes(b"fake mp4")

    with pytest.raises(FileNotFoundError, match="output/mp4/PropXXXII.mp4"):
        build_demo_reel(
            scene_names=["DefAngleTypes", "PropXI", "PropXXXII"],
            mp4_dir=mp4_dir,
            output_dir=tmp_path / "output" / "demo",
            run_command=lambda command: None,
        )


def test_readme_documents_how_to_build_and_watch_the_demo_reel() -> None:
    readme = Path("README.md").read_text()

    assert "uv run python scripts/build_demo_curriculum_preview.py" in readme
    assert "uv run python scripts/build_demo_reel.py" in readme
    assert "open output/demo/demo_curriculum_preview_reel.mp4" in readme
    assert "open docs/demo_curriculum_showcase.md" in readme
