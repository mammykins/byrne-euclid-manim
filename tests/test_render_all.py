from pathlib import Path

from scripts.render_all import build_render_jobs, render_all_scenes


def test_build_render_jobs_includes_each_scene_for_each_requested_format() -> None:
    jobs = build_render_jobs(
        scene_registry={
            "PropII": "src/byrne_euclid/propositions.py",
            "PropI": "src/byrne_euclid/propositions.py",
        },
        output_formats=("mp4", "png"),
    )

    assert jobs == [
        ("PropI", "mp4"),
        ("PropI", "png"),
        ("PropII", "mp4"),
        ("PropII", "png"),
    ]


def test_render_all_scenes_calls_render_function_for_every_job() -> None:
    calls: list[tuple[str, str, str]] = []

    def fake_render(scene_name: str, quality: str, output_format: str) -> Path:
        calls.append((scene_name, quality, output_format))
        return Path(f"output/{output_format}/{scene_name}.{output_format}")

    destinations = render_all_scenes(
        quality="l",
        scene_registry={
            "PropI": "src/byrne_euclid/propositions.py",
            "PropII": "src/byrne_euclid/propositions.py",
        },
        output_formats=("mp4", "png"),
        render_func=fake_render,
    )

    assert calls == [
        ("PropI", "l", "mp4"),
        ("PropI", "l", "png"),
        ("PropII", "l", "mp4"),
        ("PropII", "l", "png"),
    ]
    assert destinations == [
        Path("output/mp4/PropI.mp4"),
        Path("output/png/PropI.png"),
        Path("output/mp4/PropII.mp4"),
        Path("output/png/PropII.png"),
    ]
