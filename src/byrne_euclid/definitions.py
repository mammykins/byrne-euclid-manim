from __future__ import annotations

from manim import FadeIn, VGroup

from byrne_euclid.style import (
    BYRNE_BLACK,
    BYRNE_BLUE,
    BYRNE_RED,
    BYRNE_YELLOW,
    ByrneScene,
)


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
