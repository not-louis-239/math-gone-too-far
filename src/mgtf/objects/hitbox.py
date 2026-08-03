# repo at: https://github.com/not-louis-239/math-gone-too-far/

# Math Gone Too Far
# Copyright (C) 2026  Louis Masarei-Boulton <243234869+not-louis-239@users.noreply.github.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from __future__ import annotations

from typing import Iterator

import pygame as pg


class Hitbox:
    def __init__(self, w: float, h: float, d: float) -> None:
        self.w = w  # x
        self.h = h  # y
        self.d = d  # z

    def __iter__(self) -> Iterator[float]:
        yield self.w
        yield self.h
        yield self.d


def collides(
        point1: tuple[float, float, float] | pg.Vector3,
        hit1: tuple[float, float, float] | Hitbox,
        point2: tuple[float, float, float] | pg.Vector3,
        hit2: tuple[float, float, float] | Hitbox
    ) -> bool:
    """Determine collision between two point and hitbox pairs.
    Assumes that hit1's bottom-centre is positioned at point1, and same for hit2."""

    x1, y1, z1 = point1
    w1, h1, d1 = hit1
    x2, y2, z2 = point2
    w2, h2, d2 = hit2

    return not (
        x1 + w1 / 2 < x2 - w2 / 2
        or x1 - w1 / 2 > x2 + w2 / 2
        or y1 + h1 < y2 - h2
        or y1 - h1 > y2 + h2
        or z1 + d1 / 2 < z2 - d2 / 2
        or z1 - d1 / 2 > z2 + d2 / 2
    )


