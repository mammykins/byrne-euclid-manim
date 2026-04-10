from __future__ import annotations

import numpy as np
from manim import (
    PI,
    ArcBetweenPoints,
    FadeIn,
    FadeOut,
    ReplacementTransform,
    Sector,
    VGroup,
)

from byrne_euclid.style import (
    BYRNE_BLACK,
    BYRNE_BLUE,
    BYRNE_RED,
    BYRNE_YELLOW,
    ByrneScene,
)


def _label(scene: ByrneScene, text: str, point: np.ndarray, font_size: int = 22):
    return scene.byrne_title(text, font_size=font_size).move_to(point)


def _angle_card(
    scene: ByrneScene,
    center: np.ndarray,
    arm_angle: float,
    colour: str,
    label_text: str,
    right_angle: bool = False,
) -> VGroup:
    base = scene.byrne_line(center, center + np.array([1.4, 0.0, 0.0]), thick=False)
    arm = scene.byrne_line(
        center,
        center + np.array([1.2 * np.cos(arm_angle), 1.2 * np.sin(arm_angle), 0.0]),
        color=colour,
        thick=False,
    )
    if right_angle:
        mark = scene.byrne_right_angle_mark(
            center,
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
            color=BYRNE_YELLOW,
            size=0.2,
        )
    else:
        mark = scene.byrne_angle(base, arm, color=colour, radius=0.35)
    label = _label(scene, label_text, center + np.array([0.6, -0.6, 0.0]))
    return VGroup(base, arm, mark, label)


class PaletteCard(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Byrne palette.")

        red = self.byrne_polygon(
            [-5.0, 1.5, 0.0],
            [-3.7, 1.5, 0.0],
            [-3.7, 0.2, 0.0],
            [-5.0, 0.2, 0.0],
            color=BYRNE_RED,
            fill_opacity=1.0,
        )
        yellow = self.byrne_polygon(
            [-1.6, 1.5, 0.0],
            [-0.3, 1.5, 0.0],
            [-0.3, 0.2, 0.0],
            [-1.6, 0.2, 0.0],
            color=BYRNE_YELLOW,
            fill_opacity=1.0,
        )
        blue = self.byrne_polygon(
            [1.8, 1.5, 0.0],
            [3.1, 1.5, 0.0],
            [3.1, 0.2, 0.0],
            [1.8, 0.2, 0.0],
            color=BYRNE_BLUE,
            fill_opacity=1.0,
        )
        black = self.byrne_polygon(
            [5.2, 1.5, 0.0],
            [6.5, 1.5, 0.0],
            [6.5, 0.2, 0.0],
            [5.2, 0.2, 0.0],
            color=BYRNE_BLACK,
            fill_opacity=1.0,
        )

        labels = VGroup(
            self.byrne_title("#E6382D").move_to(red.get_center() + [0.0, -1.0, 0.0]),
            self.byrne_title("#F0C824").move_to(yellow.get_center() + [0.0, -1.0, 0.0]),
            self.byrne_title("#1A6FB5").move_to(blue.get_center() + [0.0, -1.0, 0.0]),
            self.byrne_title("#2B2B2B").move_to(black.get_center() + [0.0, -1.0, 0.0]),
        )

        primary = self.byrne_line(
            [-5.0, -2.3, 0.0],
            [-2.0, -2.3, 0.0],
            color=BYRNE_BLACK,
            thick=True,
        )
        thin = self.byrne_line(
            [-0.5, -2.3, 0.0],
            [2.5, -2.3, 0.0],
            color=BYRNE_BLACK,
            thick=False,
        )
        dashed = self.byrne_dashed_line([4.0, -2.3, 0.0], [6.8, -2.3, 0.0], color=BYRNE_BLUE)

        self.play(FadeIn(title))
        self.play(FadeIn(red), FadeIn(yellow), FadeIn(blue), FadeIn(black))
        self.play(FadeIn(labels))
        self.play(FadeIn(primary), FadeIn(thin), FadeIn(dashed))
        self.qed_hold()


class DefPointLineStraightLine(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Definitions I, II, IV.")
        point = self.byrne_dot(np.array([0.0, 1.5, 0.0]))
        point_label = _label(self, "Point", np.array([0.0, 1.0, 0.0]))
        curved = ArcBetweenPoints(
            np.array([-3.5, 0.6, 0.0]),
            np.array([3.5, 0.6, 0.0]),
            angle=PI / 2,
            color=BYRNE_BLUE,
        ).set_stroke(width=3)
        straight = self.byrne_line(
            np.array([-3.5, -1.0, 0.0]),
            np.array([3.5, -1.0, 0.0]),
            color=BYRNE_RED,
            thick=False,
        )

        self.play(FadeIn(title))
        self.play(FadeIn(point), FadeIn(point_label))
        self.play(FadeIn(curved))
        self.play(FadeIn(straight))
        self.play(FadeOut(curved))
        self.qed_hold()


class DefAngleTypes(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Definitions X–XII.")
        vertex = np.array([-0.5, -0.7, 0.0])
        base = self.byrne_line(vertex, vertex + np.array([3.0, 0.0, 0.0]), thick=False)
        right_arm = self.byrne_line(vertex, vertex + np.array([0.0, 2.8, 0.0]), color=BYRNE_RED)
        obtuse_arm = self.byrne_line(
            vertex,
            vertex + np.array([2.4 * np.cos(2 * PI / 3), 2.4 * np.sin(2 * PI / 3), 0.0]),
            color=BYRNE_RED,
        )
        acute_arm = self.byrne_line(
            vertex,
            vertex + np.array([2.4 * np.cos(PI / 4), 2.4 * np.sin(PI / 4), 0.0]),
            color=BYRNE_BLUE,
        )
        right_mark = self.byrne_right_angle_mark(
            vertex,
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
        )
        right_label = _label(self, "Right", vertex + np.array([1.1, 0.7, 0.0]))
        obtuse_mark = self.byrne_angle(base, obtuse_arm, color=BYRNE_RED, radius=0.55)
        obtuse_label = _label(self, "Obtuse", vertex + np.array([1.3, 0.9, 0.0]))
        acute_mark = self.byrne_angle(base, acute_arm, color=BYRNE_BLUE, radius=0.55)
        acute_label = _label(self, "Acute", vertex + np.array([1.5, 0.8, 0.0]))

        trio = VGroup(
            _angle_card(self, np.array([-4.2, -2.2, 0.0]), PI / 2, BYRNE_YELLOW, "Right", True),
            _angle_card(self, np.array([0.0, -2.2, 0.0]), 2 * PI / 3, BYRNE_RED, "Obtuse"),
            _angle_card(self, np.array([4.2, -2.2, 0.0]), PI / 4, BYRNE_BLUE, "Acute"),
        )

        self.play(FadeIn(title))
        self.play(FadeIn(base), FadeIn(right_arm))
        self.play(FadeIn(right_mark), FadeIn(right_label))
        self.play(
            ReplacementTransform(right_arm, obtuse_arm),
            ReplacementTransform(right_mark, obtuse_mark),
            ReplacementTransform(right_label, obtuse_label),
        )
        self.play(
            ReplacementTransform(obtuse_arm, acute_arm),
            ReplacementTransform(obtuse_mark, acute_mark),
            ReplacementTransform(obtuse_label, acute_label),
        )
        self.play(FadeOut(base), FadeOut(acute_arm), FadeOut(acute_mark), FadeOut(acute_label))
        self.play(FadeIn(trio))
        self.qed_hold()


class DefCircle(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Definitions XV–XVIII.")
        centre = np.array([0.0, -0.2, 0.0])
        radius = 2.2
        radius_end = centre + np.array([radius, 0.0, 0.0])
        diameter_left = centre + np.array([-radius, 0.0, 0.0])
        diameter_right = centre + np.array([radius, 0.0, 0.0])
        semicircle = (
            Sector(
                arc_center=centre,
                radius=radius,
                start_angle=0.0,
                angle=PI,
                color=BYRNE_YELLOW,
            )
            .set_fill(BYRNE_YELLOW, opacity=0.18)
            .set_stroke(BYRNE_YELLOW, width=3)
        )

        centre_dot = self.byrne_dot(centre)
        radius_line = self.byrne_line(centre, radius_end, color=BYRNE_RED)
        circle = self.byrne_circle(centre, radius, color=BYRNE_BLUE)
        diameter = self.byrne_line(diameter_left, diameter_right, color=BYRNE_YELLOW)

        self.play(FadeIn(title))
        self.play(FadeIn(centre_dot))
        self.play(FadeIn(radius_line))
        self.play(FadeIn(circle))
        self.play(FadeIn(diameter))
        self.play(FadeIn(semicircle))
        self.qed_hold()


class DefTrianglesBySide(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Definitions XXIV–XXVI.")

        equilateral = VGroup(
            self.byrne_polygon(
                [-5.0, -1.8, 0.0],
                [-3.6, 0.7, 0.0],
                [-2.2, -1.8, 0.0],
                color=BYRNE_RED,
                fill_opacity=0.14,
            ),
            _label(self, "Equilateral", np.array([-3.6, -2.6, 0.0])),
        )
        isosceles = VGroup(
            self.byrne_line([-1.0, -1.8, 0.0], [0.0, 0.9, 0.0], color=BYRNE_BLUE),
            self.byrne_line([0.0, 0.9, 0.0], [1.0, -1.8, 0.0], color=BYRNE_BLUE),
            self.byrne_line([1.0, -1.8, 0.0], [-1.0, -1.8, 0.0], color=BYRNE_BLACK, thick=False),
            _label(self, "Isosceles", np.array([0.0, -2.6, 0.0])),
        )
        scalene = VGroup(
            self.byrne_line([2.5, -1.8, 0.0], [3.5, 0.7, 0.0], color=BYRNE_RED),
            self.byrne_line([3.5, 0.7, 0.0], [5.4, -1.5, 0.0], color=BYRNE_BLUE),
            self.byrne_line([5.4, -1.5, 0.0], [2.5, -1.8, 0.0], color=BYRNE_BLACK, thick=False),
            _label(self, "Scalene", np.array([4.0, -2.6, 0.0])),
        )

        self.play(FadeIn(title))
        self.play(FadeIn(equilateral))
        self.play(FadeIn(isosceles))
        self.play(FadeIn(scalene))
        self.qed_hold()


class DefTrianglesByAngle(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Definitions XXVII–XXIX.")

        right_base = self.byrne_line([-5.2, -1.7, 0.0], [-3.4, -1.7, 0.0], thick=False)
        right_arm = self.byrne_line([-5.2, -1.7, 0.0], [-5.2, 0.5, 0.0], color=BYRNE_RED)
        right_side = self.byrne_line(
            [-5.2, 0.5, 0.0], [-3.4, -1.7, 0.0], color=BYRNE_BLUE, thick=False
        )
        right_mark = self.byrne_right_angle_mark(
            np.array([-5.2, -1.7, 0.0]),
            np.array([1.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0]),
        )
        right_label = _label(self, "Right-angled", np.array([-4.3, -2.5, 0.0]))

        obtuse_a = np.array([-0.8, -1.7, 0.0])
        obtuse_b = np.array([2.0, -1.7, 0.0])
        obtuse_c = np.array([0.0, 0.6, 0.0])
        obtuse_triangle = VGroup(
            self.byrne_line(obtuse_a, obtuse_c, color=BYRNE_RED),
            self.byrne_line(obtuse_c, obtuse_b, color=BYRNE_BLUE),
            self.byrne_line(obtuse_b, obtuse_a, thick=False),
        )
        obtuse_mark = self.byrne_angle(
            self.byrne_line(obtuse_c, obtuse_a, thick=False),
            self.byrne_line(obtuse_c, obtuse_b, thick=False),
            color=BYRNE_RED,
            radius=0.4,
        )
        obtuse_label = _label(self, "Obtuse-angled", np.array([0.6, -2.5, 0.0]))

        acute_a = np.array([3.0, -1.7, 0.0])
        acute_b = np.array([6.0, -1.7, 0.0])
        acute_c = np.array([4.5, 0.8, 0.0])
        acute_lines = VGroup(
            self.byrne_line(acute_a, acute_c, color=BYRNE_RED),
            self.byrne_line(acute_c, acute_b, color=BYRNE_BLUE),
            self.byrne_line(acute_b, acute_a, thick=False),
        )
        acute_marks = VGroup(
            self.byrne_angle(
                self.byrne_line(acute_c, acute_a, thick=False),
                self.byrne_line(acute_a, acute_b, thick=False),
                color=BYRNE_BLUE,
                radius=0.28,
            ),
            self.byrne_angle(
                self.byrne_line(acute_a, acute_b, thick=False),
                self.byrne_line(acute_b, acute_c, thick=False),
                color=BYRNE_BLUE,
                radius=0.28,
            ),
            self.byrne_angle(
                self.byrne_line(acute_b, acute_c, thick=False),
                self.byrne_line(acute_c, acute_a, thick=False),
                color=BYRNE_BLUE,
                radius=0.28,
            ),
        )
        acute_label = _label(self, "Acute-angled", np.array([4.5, -2.5, 0.0]))

        self.play(FadeIn(title))
        self.play(FadeIn(VGroup(right_base, right_arm, right_side, right_mark, right_label)))
        self.play(FadeIn(VGroup(obtuse_triangle, obtuse_mark, obtuse_label)))
        self.play(FadeIn(VGroup(acute_lines, acute_marks, acute_label)))
        self.qed_hold()


class DefQuadrilaterals(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Definitions XXX–XXXIV.")

        square = self.byrne_polygon(
            [-1.2, -1.2, 0.0],
            [-1.2, 1.2, 0.0],
            [1.2, 1.2, 0.0],
            [1.2, -1.2, 0.0],
            color=BYRNE_RED,
            fill_opacity=0.2,
        )
        rectangle = self.byrne_polygon(
            [-2.0, -1.1, 0.0],
            [-2.0, 1.1, 0.0],
            [2.0, 1.1, 0.0],
            [2.0, -1.1, 0.0],
            color=BYRNE_BLUE,
            fill_opacity=0.2,
        )
        rhombus = self.byrne_polygon(
            [-2.0, -0.8, 0.0],
            [0.0, 1.4, 0.0],
            [2.0, 0.8, 0.0],
            [0.0, -1.4, 0.0],
            color=BYRNE_YELLOW,
            fill_opacity=0.2,
        )
        parallelogram = self.byrne_polygon(
            [-2.3, -0.9, 0.0],
            [-0.6, 1.1, 0.0],
            [2.3, 0.9, 0.0],
            [0.6, -1.1, 0.0],
            color=BYRNE_RED,
            fill_opacity=0.14,
        )

        square_label = _label(self, "Square", np.array([0.0, -2.1, 0.0]))
        rectangle_label = _label(self, "Rectangle", np.array([0.0, -2.1, 0.0]))
        rhombus_label = _label(self, "Rhombus", np.array([0.0, -2.1, 0.0]))
        parallelogram_label = _label(self, "Parallelogram", np.array([0.0, -2.1, 0.0]))

        self.play(FadeIn(title))
        self.play(FadeIn(square), FadeIn(square_label))
        self.play(
            ReplacementTransform(square, rectangle),
            ReplacementTransform(square_label, rectangle_label),
        )
        self.play(
            ReplacementTransform(rectangle, rhombus),
            ReplacementTransform(rectangle_label, rhombus_label),
        )
        self.play(
            ReplacementTransform(rhombus, parallelogram),
            ReplacementTransform(rhombus_label, parallelogram_label),
        )
        self.qed_hold()


class DefParallelLines(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Definition XXXV.")
        top_short = self.byrne_line([-2.0, 0.8, 0.0], [2.0, 0.8, 0.0], color=BYRNE_RED)
        bottom_short = self.byrne_line([-2.0, -0.8, 0.0], [2.0, -0.8, 0.0], color=BYRNE_BLUE)
        top_long = self.byrne_line([-5.8, 0.8, 0.0], [5.8, 0.8, 0.0], color=BYRNE_RED)
        bottom_long = self.byrne_line([-5.8, -0.8, 0.0], [5.8, -0.8, 0.0], color=BYRNE_BLUE)
        spacing_marks = VGroup(
            self.byrne_line([-3.0, -0.4, 0.0], [-3.0, 0.4, 0.0], thick=False),
            self.byrne_line([0.0, -0.4, 0.0], [0.0, 0.4, 0.0], thick=False),
            self.byrne_line([3.0, -0.4, 0.0], [3.0, 0.4, 0.0], thick=False),
        )

        self.play(FadeIn(title))
        self.play(FadeIn(top_short), FadeIn(bottom_short))
        self.play(
            ReplacementTransform(top_short, top_long),
            ReplacementTransform(bottom_short, bottom_long),
        )
        self.play(FadeIn(spacing_marks))
        self.qed_hold()
