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




import pygame as pg

from mgtf.objects.hitbox import Hitbox


class Entity:
    def __init__(self, pos: tuple[int, int, int], image: pg.Surface, hitbox: Hitbox) -> None:
        self.pos: pg.Vector3 = pg.Vector3(pos[0], pos[1], pos[2])
        self.image = image
        self.hitbox = hitbox

    @property
    def left(self) -> float:
        return self.pos.x - self.hitbox.w / 2

    @property
    def right(self) -> float:
        return self.pos.x + self.hitbox.w / 2

    @property
    def top(self) -> float:
        return self.pos.y + self.hitbox.h

    @property
    def bottom(self) -> float:
        return self.pos.y

    @property
    def back(self) -> float:
        return self.pos.z - self.hitbox.d / 2

    @property
    def front(self) -> float:
        return self.pos.z + self.hitbox.d / 2
