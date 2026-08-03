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




from enum import StrEnum
from typing import Iterator

import pygame as pg



class Hitbox:
    def __init__(self, w: float, h: float, d: float) -> None:
        self.w = w  # width, x
        self.h = h  # height, y
        self.d = d  # depth, z

    def __iter__(self) -> Iterator[float]:
        yield self.w
        yield self.h
        yield self.d


class Facing(StrEnum):
    NORTH = "n"
    EAST = "e"
    SOUTH = "s"
    WEST = "w"


class Entity:
    def __init__(self, pos: tuple[int, int, int], images: dict[Facing, pg.Surface], base_hitbox: Hitbox) -> None:
        self.pos: pg.Vector3 = pg.Vector3(pos[0], pos[1], pos[2])
        self.facing: Facing = Facing.NORTH
        self.images = images
        self._base_hitbox = base_hitbox  # hitbox when facing south
        self._perp_hitbox = Hitbox(base_hitbox.d, base_hitbox.h, base_hitbox.w)

    @property
    def hitbox(self) -> Hitbox:
        return self._base_hitbox if self.facing in (Facing.NORTH, Facing.SOUTH) else self._perp_hitbox

    @property
    def left(self) -> float:
        return self.pos.x - self._base_hitbox.w / 2

    @property
    def right(self) -> float:
        return self.pos.x + self._base_hitbox.w / 2

    @property
    def top(self) -> float:
        return self.pos.y + self._base_hitbox.h

    @property
    def bottom(self) -> float:
        return self.pos.y

    @property
    def back(self) -> float:
        return self.pos.z - self._base_hitbox.d / 2

    @property
    def front(self) -> float:
        return self.pos.z + self._base_hitbox.d / 2


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
