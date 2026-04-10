from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np


def _point(value: Sequence[float] | np.ndarray) -> np.ndarray:
    point = np.array(value, dtype=float)
    if point.shape == (2,):
        return np.array([point[0], point[1], 0.0], dtype=float)
    if point.shape != (3,):
        raise ValueError(f"Expected a 2D or 3D point, got shape {point.shape}.")
    return point


def circle_intersection(
    c1_centre: Sequence[float] | np.ndarray,
    c1_radius: float,
    c2_centre: Sequence[float] | np.ndarray,
    c2_radius: float,
) -> tuple[np.ndarray, np.ndarray]:
    c1 = _point(c1_centre)
    c2 = _point(c2_centre)
    delta = c2 - c1
    distance = np.linalg.norm(delta[:2])

    if np.isclose(distance, 0.0) and np.isclose(c1_radius, c2_radius):
        raise ValueError("Coincident circles have infinitely many intersections.")
    if distance > c1_radius + c2_radius or distance < abs(c1_radius - c2_radius):
        raise ValueError("Circles do not intersect.")

    a = ((c1_radius**2) - (c2_radius**2) + (distance**2)) / (2 * distance)
    h_sq = (c1_radius**2) - (a**2)
    if h_sq < 0 and not np.isclose(h_sq, 0.0):
        raise ValueError("Circles do not intersect.")

    h = math.sqrt(max(h_sq, 0.0))
    midpoint = c1 + (a / distance) * delta
    perpendicular = np.array([-delta[1], delta[0], 0.0]) / distance

    upper = midpoint + (h * perpendicular)
    lower = midpoint - (h * perpendicular)
    return (
        upper if upper[1] >= lower[1] else lower,
        lower if upper[1] >= lower[1] else upper,
    )


def line_intersection(
    p1: Sequence[float] | np.ndarray,
    p2: Sequence[float] | np.ndarray,
    p3: Sequence[float] | np.ndarray,
    p4: Sequence[float] | np.ndarray,
) -> np.ndarray:
    a1 = _point(p1)
    a2 = _point(p2)
    b1 = _point(p3)
    b2 = _point(p4)

    x1, y1 = a1[:2]
    x2, y2 = a2[:2]
    x3, y3 = b1[:2]
    x4, y4 = b2[:2]

    denominator = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))
    if np.isclose(denominator, 0.0):
        raise ValueError("Lines are parallel and do not intersect.")

    determinant_a = (x1 * y2) - (y1 * x2)
    determinant_b = (x3 * y4) - (y3 * x4)

    x = ((determinant_a * (x3 - x4)) - ((x1 - x2) * determinant_b)) / denominator
    y = ((determinant_a * (y3 - y4)) - ((y1 - y2) * determinant_b)) / denominator
    return np.array([x, y, 0.0], dtype=float)


def perpendicular_foot(
    point: Sequence[float] | np.ndarray,
    line_start: Sequence[float] | np.ndarray,
    line_end: Sequence[float] | np.ndarray,
) -> np.ndarray:
    source = _point(point)
    start = _point(line_start)
    end = _point(line_end)
    line = end - start
    scale = np.dot(source - start, line) / np.dot(line, line)
    projection = start + (scale * line)
    projection[2] = 0.0
    return projection


def midpoint(a: Sequence[float] | np.ndarray, b: Sequence[float] | np.ndarray) -> np.ndarray:
    return (_point(a) + _point(b)) / 2


def point_on_circle(
    centre: Sequence[float] | np.ndarray,
    radius: float,
    angle_radians: float,
) -> np.ndarray:
    base = _point(centre)
    return np.array(
        [
            base[0] + (radius * math.cos(angle_radians)),
            base[1] + (radius * math.sin(angle_radians)),
            0.0,
        ],
        dtype=float,
    )


def angle_between_lines(
    p1: Sequence[float] | np.ndarray,
    p2: Sequence[float] | np.ndarray,
    p3: Sequence[float] | np.ndarray,
) -> float:
    a = _point(p1) - _point(p2)
    b = _point(p3) - _point(p2)
    magnitude = np.linalg.norm(a) * np.linalg.norm(b)
    if np.isclose(magnitude, 0.0):
        raise ValueError("Cannot measure an angle with a zero-length side.")
    cosine = np.dot(a, b) / magnitude
    return float(np.arccos(np.clip(cosine, -1.0, 1.0)))
