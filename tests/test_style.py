import numpy as np
import pytest
from manim import Circle, DashedLine, Line, Scene

from byrne_euclid.style import (
    BYRNE_BG,
    BYRNE_BLACK,
    BYRNE_BLUE,
    BYRNE_DASH_LENGTH,
    BYRNE_DASH_RATIO,
    BYRNE_RED,
    BYRNE_THICK,
    BYRNE_THIN,
    BYRNE_YELLOW,
    ByrneScene,
)


class DummyScene(ByrneScene):
    def construct(self) -> None:
        return None


def colour_hex(value) -> str:
    return value.to_hex().upper()


def build_scene() -> DummyScene:
    scene = DummyScene(skip_animations=True)
    scene.setup()
    return scene


def test_palette_constants_are_locked() -> None:
    assert BYRNE_RED == "#E6382D"
    assert BYRNE_YELLOW == "#F0C824"
    assert BYRNE_BLUE == "#1A6FB5"
    assert BYRNE_BLACK == "#2B2B2B"
    assert BYRNE_BG == "#F5F0E1"


def test_line_style_constants_are_locked() -> None:
    assert BYRNE_THICK > BYRNE_THIN
    assert BYRNE_DASH_LENGTH > 0
    assert BYRNE_DASH_RATIO == pytest.approx(0.5)


def test_byrne_scene_is_a_scene() -> None:
    assert issubclass(ByrneScene, Scene)


def test_setup_sets_the_background_colour() -> None:
    scene = build_scene()
    assert colour_hex(scene.camera.background_color) == BYRNE_BG


def test_byrne_line_returns_a_styled_line() -> None:
    scene = build_scene()
    line = scene.byrne_line(np.array([-1.0, 0.0, 0.0]), np.array([1.0, 0.0, 0.0]), color=BYRNE_RED)

    assert isinstance(line, Line)
    assert colour_hex(line.get_color()) == BYRNE_RED
    assert line.stroke_width == BYRNE_THICK


def test_byrne_dashed_line_returns_a_styled_dashed_line() -> None:
    scene = build_scene()
    dashed = scene.byrne_dashed_line(
        np.array([-1.0, 0.0, 0.0]),
        np.array([1.0, 0.0, 0.0]),
        color=BYRNE_BLUE,
    )

    assert isinstance(dashed, DashedLine)
    assert colour_hex(dashed.get_color()) == BYRNE_BLUE
    assert dashed.dash_length == pytest.approx(BYRNE_DASH_LENGTH)
    assert dashed.dashed_ratio == pytest.approx(BYRNE_DASH_RATIO)


def test_byrne_circle_returns_a_styled_circle() -> None:
    scene = build_scene()
    circle = scene.byrne_circle(np.array([1.0, 2.0, 0.0]), 2.5, color=BYRNE_YELLOW)

    assert isinstance(circle, Circle)
    assert np.allclose(circle.get_center(), np.array([1.0, 2.0, 0.0]))
    assert circle.radius == pytest.approx(2.5)
    assert colour_hex(circle.get_color()) == BYRNE_YELLOW
