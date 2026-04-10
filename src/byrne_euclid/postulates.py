from __future__ import annotations

import numpy as np
from manim import FadeIn

from byrne_euclid.style import BYRNE_BLUE, BYRNE_RED, ByrneScene


def _label(scene: ByrneScene, text: str, point: np.ndarray, font_size: int = 22):
    return scene.byrne_title(text, font_size=font_size).move_to(point)


class PostulateI(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Postulate I.")
        point_a = np.array([-2.5, 0.0, 0.0])
        point_b = np.array([2.5, 0.0, 0.0])

        self.play(FadeIn(title))
        self.play(FadeIn(self.byrne_dot(point_a)), FadeIn(self.byrne_dot(point_b)))
        self.construct_line(point_a, point_b)
        self.qed_hold()


class PostulateII(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Postulate II.")
        segment = self.byrne_line(np.array([-2.5, 0.0, 0.0]), np.array([1.5, 0.0, 0.0]))
        extension = self.byrne_dashed_line(
            np.array([1.5, 0.0, 0.0]), np.array([5.5, 0.0, 0.0]), color=BYRNE_BLUE
        )

        self.play(FadeIn(title))
        self.play(FadeIn(segment))
        self.play(FadeIn(extension))
        self.qed_hold()


class PostulateIII(ByrneScene):
    def construct(self) -> None:
        title = self.byrne_title("Postulate III.")
        centre = np.array([0.0, 0.0, 0.0])
        radius = 2.0
        radius_end = centre + np.array([radius, 0.0, 0.0])

        self.play(FadeIn(title))
        self.play(FadeIn(self.byrne_dot(centre)))
        self.play(FadeIn(self.byrne_line(centre, radius_end, color=BYRNE_RED)))
        self.sweep_circle(centre, radius, color=BYRNE_BLUE)
        self.qed_hold()
