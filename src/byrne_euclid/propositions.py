from __future__ import annotations

import numpy as np
from manim import FadeIn

from byrne_euclid.style import BYRNE_BLUE, BYRNE_RED, BYRNE_YELLOW, ByrneScene
from byrne_euclid.utils import circle_intersection


class PropI(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Proposition I.")
        self.play(FadeIn(title))

        point_a = np.array([-2.4, -1.5, 0.0])
        point_b = np.array([2.4, -1.5, 0.0])
        radius = np.linalg.norm(point_b - point_a)
        point_c, _ = circle_intersection(point_a, radius, point_b, radius)

        dot_a = self.byrne_dot(point_a)
        dot_b = self.byrne_dot(point_b)
        self.play(FadeIn(dot_a), FadeIn(dot_b))

        self.construct_line(point_a, point_b)
        circle_a = self.sweep_circle(point_a, radius, color=BYRNE_BLUE)
        circle_b = self.sweep_circle(point_b, radius, color=BYRNE_RED)

        dot_c = self.byrne_dot(point_c)
        self.play(FadeIn(dot_c))

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
