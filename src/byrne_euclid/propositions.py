from __future__ import annotations

import numpy as np
from manim import PI, FadeIn, Sector, VGroup

from byrne_euclid.style import BYRNE_BLACK, BYRNE_BLUE, BYRNE_RED, BYRNE_YELLOW, ByrneScene
from byrne_euclid.utils import circle_intersection, midpoint


def _label(scene: ByrneScene, text: str, point: np.ndarray, font_size: int = 22):
    return scene.byrne_title(text, font_size=font_size).move_to(point)


def _extend(start: np.ndarray, end: np.ndarray, extra: float) -> np.ndarray:
    direction = end - start
    direction = direction / np.linalg.norm(direction)
    return end + (direction * extra)


def _equilateral_apex(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    radius = np.linalg.norm(b - a)
    apex, _ = circle_intersection(a, radius, b, radius)
    return apex


class PropI(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Proposition I.")
        self.play(FadeIn(title))

        point_a = np.array([-2.4, -1.5, 0.0])
        point_b = np.array([2.4, -1.5, 0.0])
        radius = np.linalg.norm(point_b - point_a)
        point_c = _equilateral_apex(point_a, point_b)

        self.play(FadeIn(self.byrne_dot(point_a)), FadeIn(self.byrne_dot(point_b)))
        self.construct_line(point_a, point_b)
        circle_a = self.sweep_circle(point_a, radius, color=BYRNE_BLUE)
        circle_b = self.sweep_circle(point_b, radius, color=BYRNE_RED)
        self.play(FadeIn(self.byrne_dot(point_c)))

        side_ca = self.byrne_line(point_c, point_a, color=BYRNE_YELLOW)
        side_cb = self.byrne_line(point_c, point_b, color=BYRNE_RED)
        triangle = self.byrne_polygon(
            point_a,
            point_b,
            point_c,
            color=BYRNE_BLUE,
            stroke_color=BYRNE_YELLOW,
            fill_opacity=0.18,
        )

        self.play(FadeIn(triangle))
        self.play(FadeIn(side_ca), FadeIn(side_cb))
        self.fade_construction(circle_a, circle_b)
        self.qed_hold()


class PropII(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Proposition II.")
        point_p = np.array([-5.0, -1.2, 0.0])
        segment_a = np.array([1.0, 1.0, 0.0])
        segment_b = np.array([3.4, 1.0, 0.0])
        length = np.linalg.norm(segment_b - segment_a)
        point_q = point_p + np.array([length, 0.0, 0.0])

        given = self.byrne_line(segment_a, segment_b, color=BYRNE_BLUE)
        connector = self.byrne_line(point_p, segment_a, color=BYRNE_BLACK, thick=False)
        helper_circle = self.byrne_circle(point_p, length, color=BYRNE_RED)
        result = self.byrne_line(point_p, point_q, color=BYRNE_YELLOW)

        self.play(FadeIn(title))
        self.play(FadeIn(self.byrne_dot(point_p)), FadeIn(given))
        self.play(FadeIn(connector))
        self.play(FadeIn(helper_circle))
        self.play(FadeIn(self.byrne_dot(point_q)), FadeIn(result))
        self.fade_construction(connector, helper_circle)
        self.qed_hold()


class PropIII(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Proposition III.")
        long_a = np.array([-5.0, -1.2, 0.0])
        long_b = np.array([3.5, -1.2, 0.0])
        short_a = np.array([-2.4, 1.0, 0.0])
        short_b = np.array([0.4, 1.0, 0.0])
        radius = np.linalg.norm(short_b - short_a)
        cut_point = long_a + np.array([radius, 0.0, 0.0])

        long_segment = self.byrne_line(long_a, long_b, color=BYRNE_BLACK)
        short_segment = self.byrne_line(short_a, short_b, color=BYRNE_BLUE)
        helper_circle = self.byrne_circle(long_a, radius, color=BYRNE_RED)
        result = self.byrne_line(long_a, cut_point, color=BYRNE_YELLOW)

        self.play(FadeIn(title))
        self.play(FadeIn(long_segment), FadeIn(short_segment))
        self.play(FadeIn(self.byrne_dot(long_a)))
        self.play(FadeIn(helper_circle))
        self.play(FadeIn(self.byrne_dot(cut_point)), FadeIn(result))
        self.fade_construction(helper_circle, long_segment)
        self.qed_hold()


class PropIX(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Proposition IX.")
        vertex = np.array([-0.8, -1.0, 0.0])
        arm_a = np.array([2.7, -1.0, 0.0])
        arm_b = np.array([1.0, 1.8, 0.0])
        mark_a = vertex + (arm_a - vertex) * 0.55
        mark_b = vertex + (arm_b - vertex) * 0.55
        apex = _equilateral_apex(mark_a, mark_b)

        left_arm = self.byrne_line(vertex, arm_a, color=BYRNE_RED)
        right_arm = self.byrne_line(vertex, arm_b, color=BYRNE_BLUE)
        chord = self.byrne_line(mark_a, mark_b, color=BYRNE_YELLOW, thick=False)
        helper_left = self.byrne_circle(mark_a, np.linalg.norm(mark_b - mark_a), color=BYRNE_BLUE)
        helper_right = self.byrne_circle(mark_b, np.linalg.norm(mark_b - mark_a), color=BYRNE_RED)
        bisector = self.byrne_line(vertex, apex, color=BYRNE_BLACK)
        angle_left = self.byrne_angle(left_arm, bisector, color=BYRNE_YELLOW, radius=0.45)
        angle_right = self.byrne_angle(bisector, right_arm, color=BYRNE_YELLOW, radius=0.55)

        self.play(FadeIn(title))
        self.play(FadeIn(left_arm), FadeIn(right_arm))
        self.play(FadeIn(self.byrne_dot(mark_a)), FadeIn(self.byrne_dot(mark_b)))
        self.play(FadeIn(chord))
        self.play(FadeIn(helper_left), FadeIn(helper_right))
        self.play(FadeIn(self.byrne_dot(apex)), FadeIn(bisector))
        self.play(FadeIn(angle_left), FadeIn(angle_right))
        self.fade_construction(helper_left, helper_right, chord)
        self.qed_hold()


class PropX(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Proposition X.")
        point_a = np.array([-3.5, -1.0, 0.0])
        point_b = np.array([3.5, -1.0, 0.0])
        radius = np.linalg.norm(point_b - point_a) * 0.65
        upper, lower = circle_intersection(point_a, radius, point_b, radius)
        mid = midpoint(point_a, point_b)

        base = self.byrne_line(point_a, point_b, color=BYRNE_BLACK)
        left_circle = self.byrne_circle(point_a, radius, color=BYRNE_BLUE)
        right_circle = self.byrne_circle(point_b, radius, color=BYRNE_RED)
        bisector = self.byrne_line(upper, lower, color=BYRNE_YELLOW)
        half_left = self.byrne_line(point_a, mid, color=BYRNE_YELLOW)
        half_right = self.byrne_line(mid, point_b, color=BYRNE_YELLOW)

        self.play(FadeIn(title))
        self.play(FadeIn(base))
        self.play(FadeIn(left_circle), FadeIn(right_circle))
        self.play(FadeIn(bisector), FadeIn(self.byrne_dot(mid)))
        self.play(FadeIn(half_left), FadeIn(half_right))
        self.fade_construction(left_circle, right_circle, bisector)
        self.qed_hold()


class PropXI(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Proposition XI.")
        left = np.array([-4.0, -1.0, 0.0])
        centre = np.array([0.0, -1.0, 0.0])
        right = np.array([4.0, -1.0, 0.0])
        side_left = np.array([-2.0, -1.0, 0.0])
        side_right = np.array([2.0, -1.0, 0.0])
        apex = _equilateral_apex(side_left, side_right)

        base = self.byrne_line(left, right, color=BYRNE_BLACK)
        helper_left = self.byrne_circle(
            side_left, np.linalg.norm(side_right - side_left), color=BYRNE_BLUE
        )
        helper_right = self.byrne_circle(
            side_right, np.linalg.norm(side_right - side_left), color=BYRNE_RED
        )
        perpendicular = self.byrne_line(centre, apex, color=BYRNE_YELLOW)
        left_mark = self.byrne_right_angle_mark(
            centre, np.array([-1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])
        )
        right_mark = self.byrne_right_angle_mark(
            centre, np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0])
        )

        self.play(FadeIn(title))
        self.play(FadeIn(base), FadeIn(self.byrne_dot(centre, color=BYRNE_RED)))
        self.play(FadeIn(self.byrne_dot(side_left)), FadeIn(self.byrne_dot(side_right)))
        self.play(FadeIn(helper_left), FadeIn(helper_right))
        self.play(FadeIn(perpendicular))
        self.play(FadeIn(left_mark), FadeIn(right_mark))
        self.fade_construction(helper_left, helper_right)
        self.qed_hold()


class PropXII(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Proposition XII.")
        line_a = np.array([-4.5, -1.2, 0.0])
        line_b = np.array([4.5, -1.2, 0.0])
        point_p = np.array([0.0, 2.0, 0.0])
        radius = 3.3
        x_offset = np.sqrt((radius**2) - (3.2**2))
        cross_left = np.array([-x_offset, -1.2, 0.0])
        cross_right = np.array([x_offset, -1.2, 0.0])
        foot = midpoint(cross_left, cross_right)

        base = self.byrne_line(line_a, line_b, color=BYRNE_BLACK)
        helper_circle = self.byrne_circle(point_p, radius, color=BYRNE_BLUE)
        helper_chord = self.byrne_line(cross_left, cross_right, color=BYRNE_RED, thick=False)
        perpendicular = self.byrne_line(point_p, foot, color=BYRNE_YELLOW)
        right_mark = self.byrne_right_angle_mark(
            foot,
            np.array([1.0, 0.0, 0.0]),
            point_p - foot,
        )

        self.play(FadeIn(title))
        self.play(FadeIn(base), FadeIn(self.byrne_dot(point_p, color=BYRNE_RED)))
        self.play(FadeIn(helper_circle))
        self.play(FadeIn(self.byrne_dot(cross_left)), FadeIn(self.byrne_dot(cross_right)))
        self.play(FadeIn(helper_chord))
        self.play(FadeIn(perpendicular), FadeIn(self.byrne_dot(foot)))
        self.play(FadeIn(right_mark))
        self.fade_construction(helper_circle, helper_chord)
        self.qed_hold()


class PropXIII(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Proposition XIII.")
        vertex = np.array([0.0, -0.2, 0.0])
        left = self.byrne_line(vertex, np.array([-4.0, -0.2, 0.0]), color=BYRNE_BLACK)
        right = self.byrne_line(vertex, np.array([4.0, -0.2, 0.0]), color=BYRNE_BLACK)
        standing = self.byrne_line(vertex, np.array([2.0, 2.4, 0.0]), color=BYRNE_RED)
        left_angle = self.byrne_angle(left, standing, color=BYRNE_YELLOW, radius=0.8)
        right_angle = self.byrne_angle(standing, right, color=BYRNE_BLUE, radius=1.0)
        label = _label(self, "180°", np.array([0.0, 1.6, 0.0]), font_size=28)

        self.play(FadeIn(title))
        self.play(FadeIn(left), FadeIn(right), FadeIn(standing))
        self.play(FadeIn(left_angle), FadeIn(right_angle))
        self.play(FadeIn(label))
        self.qed_hold()


class PropXV(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Proposition XV.")
        horizontal_left = self.byrne_line(
            np.array([0.0, 0.0, 0.0]), np.array([-4.0, -2.0, 0.0]), color=BYRNE_RED
        )
        horizontal_right = self.byrne_line(
            np.array([0.0, 0.0, 0.0]), np.array([4.0, 2.0, 0.0]), color=BYRNE_RED
        )
        vertical_left = self.byrne_line(
            np.array([0.0, 0.0, 0.0]), np.array([-4.0, 2.0, 0.0]), color=BYRNE_BLUE
        )
        vertical_right = self.byrne_line(
            np.array([0.0, 0.0, 0.0]), np.array([4.0, -2.0, 0.0]), color=BYRNE_BLUE
        )
        top_angle = self.byrne_angle(
            vertical_left, horizontal_right, color=BYRNE_YELLOW, radius=0.7
        )
        bottom_angle = self.byrne_angle(
            horizontal_left, vertical_right, color=BYRNE_YELLOW, radius=0.7
        )
        left_angle = self.byrne_angle(horizontal_left, vertical_left, color=BYRNE_BLACK, radius=1.0)
        right_angle = self.byrne_angle(
            vertical_right, horizontal_right, color=BYRNE_BLACK, radius=1.0
        )

        self.play(FadeIn(title))
        self.play(
            FadeIn(horizontal_left),
            FadeIn(horizontal_right),
            FadeIn(vertical_left),
            FadeIn(vertical_right),
        )
        self.play(FadeIn(top_angle), FadeIn(bottom_angle))
        self.play(FadeIn(left_angle), FadeIn(right_angle))
        self.qed_hold()


class PropXXXII(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Proposition XXXII.")
        point_a = np.array([-3.0, -1.2, 0.0])
        point_b = np.array([2.8, -1.2, 0.0])
        point_c = np.array([-0.2, 1.8, 0.0])
        extended = np.array([5.0, -1.2, 0.0])
        top_left = np.array([-3.4, 1.8, 0.0])
        top_right = np.array([4.0, 1.8, 0.0])

        triangle = VGroup(
            self.byrne_line(point_a, point_b, color=BYRNE_BLACK),
            self.byrne_line(point_b, point_c, color=BYRNE_RED),
            self.byrne_line(point_c, point_a, color=BYRNE_BLUE),
        )
        extension = self.byrne_dashed_line(point_b, extended, color=BYRNE_RED)
        parallel = self.byrne_dashed_line(top_left, top_right, color=BYRNE_BLUE)

        angle_a = self.byrne_angle(
            self.byrne_line(point_a, point_c, thick=False),
            self.byrne_line(point_a, point_b, thick=False),
            color=BYRNE_YELLOW,
            radius=0.35,
        )
        angle_b = self.byrne_angle(
            self.byrne_line(point_b, point_a, thick=False),
            self.byrne_line(point_b, point_c, thick=False),
            color=BYRNE_RED,
            radius=0.35,
        )
        angle_c = self.byrne_angle(
            self.byrne_line(point_c, point_b, thick=False),
            self.byrne_line(point_c, point_a, thick=False),
            color=BYRNE_BLUE,
            radius=0.45,
        )

        straight_left = (
            Sector(
                arc_center=np.array([-1.1, 2.7, 0.0]),
                radius=0.55,
                start_angle=0.0,
                angle=PI / 3,
                color=BYRNE_YELLOW,
            )
            .set_fill(BYRNE_YELLOW, opacity=0.25)
            .set_stroke(BYRNE_YELLOW, width=3)
        )
        straight_mid = (
            Sector(
                arc_center=np.array([-0.1, 2.7, 0.0]),
                radius=0.55,
                start_angle=PI / 3,
                angle=PI / 3,
                color=BYRNE_RED,
            )
            .set_fill(BYRNE_RED, opacity=0.25)
            .set_stroke(BYRNE_RED, width=3)
        )
        straight_right = (
            Sector(
                arc_center=np.array([0.9, 2.7, 0.0]),
                radius=0.55,
                start_angle=2 * PI / 3,
                angle=PI / 3,
                color=BYRNE_BLUE,
            )
            .set_fill(BYRNE_BLUE, opacity=0.25)
            .set_stroke(BYRNE_BLUE, width=3)
        )
        label = _label(self, "180°", np.array([-0.1, 3.4, 0.0]), font_size=28)

        self.play(FadeIn(title))
        self.play(FadeIn(triangle))
        self.play(FadeIn(angle_a), FadeIn(angle_b), FadeIn(angle_c))
        self.play(FadeIn(extension), FadeIn(parallel))
        self.play(
            FadeIn(straight_left), FadeIn(straight_mid), FadeIn(straight_right), FadeIn(label)
        )
        self.qed_hold()
