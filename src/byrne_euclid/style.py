from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np
from manim import (
    LEFT,
    ORIGIN,
    RIGHT,
    UL,
    Angle,
    Arc,
    Circle,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    Line,
    ManimColor,
    Polygon,
    Scene,
    Square,
    Text,
)

BYRNE_RED = "#E6382D"
BYRNE_YELLOW = "#F0C824"
BYRNE_BLUE = "#1A6FB5"
BYRNE_BLACK = "#2B2B2B"
BYRNE_BG = "#F5F0E1"

BYRNE_THICK = 6.0
BYRNE_THIN = 3.0
BYRNE_DASH_LENGTH = 0.15
BYRNE_DASH_RATIO = 0.5
BYRNE_DOT_RADIUS = 0.07
BYRNE_TITLE_FONT_SIZE = 34
BYRNE_QED_HOLD = 2.0


def _point(value: Sequence[float] | np.ndarray) -> np.ndarray:
    point = np.array(value, dtype=float)
    if point.shape == (2,):
        return np.array([point[0], point[1], 0.0], dtype=float)
    if point.shape != (3,):
        raise ValueError(f"Expected a 2D or 3D point, got shape {point.shape}.")
    return point


def _normalise(vector: Sequence[float] | np.ndarray) -> np.ndarray:
    value = _point(vector)
    length = np.linalg.norm(value)
    if np.isclose(length, 0.0):
        raise ValueError("Cannot normalise a zero-length vector.")
    return value / length


class ByrneScene(Scene):
    aspect_ratio = "16:9"

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = ManimColor(BYRNE_BG)

    def byrne_line(
        self,
        start: Sequence[float] | np.ndarray,
        end: Sequence[float] | np.ndarray,
        color: str = BYRNE_BLACK,
        thick: bool = True,
        opacity: float = 1.0,
    ) -> Line:
        return Line(_point(start), _point(end), color=color).set_stroke(
            color=color,
            width=BYRNE_THICK if thick else BYRNE_THIN,
            opacity=opacity,
        )

    def byrne_dashed_line(
        self,
        start: Sequence[float] | np.ndarray,
        end: Sequence[float] | np.ndarray,
        color: str = BYRNE_BLACK,
        thick: bool = False,
        opacity: float = 1.0,
    ) -> DashedLine:
        return DashedLine(
            _point(start),
            _point(end),
            color=color,
            dash_length=BYRNE_DASH_LENGTH,
            dashed_ratio=BYRNE_DASH_RATIO,
        ).set_stroke(
            color=color,
            width=BYRNE_THICK if thick else BYRNE_THIN,
            opacity=opacity,
        )

    def byrne_circle(
        self,
        center: Sequence[float] | np.ndarray = ORIGIN,
        radius: float = 1.0,
        color: str = BYRNE_BLACK,
        thick: bool = False,
        opacity: float = 1.0,
    ) -> Circle:
        circle = Circle(radius=radius, color=color).move_to(_point(center))
        return circle.set_stroke(
            color=color,
            width=BYRNE_THICK if thick else BYRNE_THIN,
            opacity=opacity,
        )

    def byrne_arc(
        self,
        center: Sequence[float] | np.ndarray,
        radius: float,
        start_angle: float,
        angle: float,
        color: str = BYRNE_BLACK,
        thick: bool = False,
        opacity: float = 1.0,
    ) -> Arc:
        arc = Arc(
            radius=radius,
            start_angle=start_angle,
            angle=angle,
            arc_center=_point(center),
            color=color,
        )
        return arc.set_stroke(
            color=color,
            width=BYRNE_THICK if thick else BYRNE_THIN,
            opacity=opacity,
        )

    def byrne_angle(
        self,
        line1: Line,
        line2: Line,
        color: str = BYRNE_YELLOW,
        radius: float = 0.4,
        fill_opacity: float = 0.35,
    ) -> Angle:
        angle = Angle(line1, line2, radius=radius, color=color)
        angle.set_fill(color=color, opacity=fill_opacity)
        angle.set_stroke(color=color, width=BYRNE_THIN)
        return angle

    def byrne_dot(
        self,
        point: Sequence[float] | np.ndarray,
        color: str = BYRNE_BLACK,
        radius: float = BYRNE_DOT_RADIUS,
    ) -> Dot:
        return Dot(point=_point(point), radius=radius, color=color)

    def byrne_polygon(
        self,
        *vertices: Sequence[float] | np.ndarray,
        color: str = BYRNE_BLACK,
        fill_opacity: float = 0.2,
        stroke_color: str | None = None,
        thick: bool = False,
    ) -> Polygon:
        stroke = stroke_color or color
        polygon = Polygon(*[_point(vertex) for vertex in vertices], color=stroke)
        polygon.set_stroke(stroke, width=BYRNE_THICK if thick else BYRNE_THIN)
        polygon.set_fill(color=color, opacity=fill_opacity)
        return polygon

    def byrne_title(
        self,
        text: str,
        position=UL,
        font_size: int = BYRNE_TITLE_FONT_SIZE,
    ) -> Text:
        return Text(text, color=BYRNE_BLACK, font_size=font_size).to_corner(position)

    def byrne_right_angle_mark(
        self,
        vertex: Sequence[float] | np.ndarray,
        line1_dir: Sequence[float] | np.ndarray = RIGHT,
        line2_dir: Sequence[float] | np.ndarray = LEFT,
        color: str = BYRNE_YELLOW,
        size: float = 0.25,
    ) -> Square:
        u1 = _normalise(line1_dir)
        u2 = _normalise(line2_dir)
        square = Square(side_length=size, color=color)
        square.rotate(math.atan2(u1[1], u1[0]))
        square.move_to(_point(vertex) + ((u1 + u2) * (size / 2)))
        square.set_stroke(color, width=BYRNE_THIN)
        square.set_fill(opacity=0.0)
        return square

    def construct_line(
        self,
        start: Sequence[float] | np.ndarray,
        end: Sequence[float] | np.ndarray,
        color: str = BYRNE_BLACK,
        thick: bool = True,
        run_time: float = 1.0,
    ) -> Line:
        line = self.byrne_line(start, end, color=color, thick=thick)
        self.play(Create(line), run_time=run_time)
        return line

    def sweep_circle(
        self,
        center: Sequence[float] | np.ndarray,
        radius: float,
        color: str = BYRNE_BLUE,
        thick: bool = False,
        run_time: float = 1.5,
    ) -> Circle:
        circle = self.byrne_circle(center, radius, color=color, thick=thick)
        self.play(Create(circle), run_time=run_time)
        return circle

    def mark_angle(
        self,
        line1: Line,
        line2: Line,
        color: str = BYRNE_YELLOW,
        radius: float = 0.4,
        run_time: float = 0.6,
    ) -> Angle:
        angle = self.byrne_angle(line1, line2, color=color, radius=radius)
        self.play(FadeIn(angle), run_time=run_time)
        return angle

    def fade_construction(
        self,
        *mobjects,
        target_opacity: float = 0.2,
        run_time: float = 0.8,
    ) -> None:
        self.play(
            *(mobject.animate.set_opacity(target_opacity) for mobject in mobjects),
            run_time=run_time,
        )

    def qed_hold(self, duration: float = BYRNE_QED_HOLD) -> None:
        self.wait(duration)
