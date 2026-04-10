import math

import numpy as np
import pytest

from byrne_euclid.utils import (
    angle_between_lines,
    circle_intersection,
    line_intersection,
    midpoint,
    perpendicular_foot,
    point_on_circle,
)


def test_circle_intersection_returns_the_two_expected_points() -> None:
    upper, lower = circle_intersection(
        np.array([0.0, 0.0, 0.0]),
        1.0,
        np.array([1.0, 0.0, 0.0]),
        1.0,
    )

    expected_upper = np.array([0.5, math.sqrt(3) / 2, 0.0])
    expected_lower = np.array([0.5, -math.sqrt(3) / 2, 0.0])

    assert np.allclose(upper, expected_upper)
    assert np.allclose(lower, expected_lower)


def test_circle_intersection_raises_for_non_intersecting_circles() -> None:
    with pytest.raises(ValueError):
        circle_intersection(
            np.array([0.0, 0.0, 0.0]),
            1.0,
            np.array([3.0, 0.0, 0.0]),
            1.0,
        )


def test_line_intersection_returns_expected_point() -> None:
    intersection = line_intersection(
        np.array([-1.0, 0.0, 0.0]),
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, -1.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
    )

    assert np.allclose(intersection, np.array([0.0, 0.0, 0.0]))


def test_perpendicular_foot_returns_projection_on_line() -> None:
    foot = perpendicular_foot(
        np.array([2.0, 3.0, 0.0]),
        np.array([0.0, 0.0, 0.0]),
        np.array([4.0, 0.0, 0.0]),
    )

    assert np.allclose(foot, np.array([2.0, 0.0, 0.0]))


def test_midpoint_returns_expected_centre() -> None:
    assert np.allclose(
        midpoint(np.array([-2.0, 4.0, 0.0]), np.array([2.0, 0.0, 0.0])),
        np.array([0.0, 2.0, 0.0]),
    )


def test_point_on_circle_returns_expected_position() -> None:
    point = point_on_circle(np.array([1.0, 1.0, 0.0]), 2.0, math.pi / 2)
    assert np.allclose(point, np.array([1.0, 3.0, 0.0]))


def test_angle_between_lines_returns_expected_radians() -> None:
    angle = angle_between_lines(
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
    )

    assert angle == pytest.approx(math.pi / 2)
