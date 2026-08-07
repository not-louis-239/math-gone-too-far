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

from dataclasses import dataclass

import pygame as pg

from mgtf.objects.entity import Facing, Hitbox


_DOOR_W = 1
_DOOR_H = 1
_DOOR_D = 4 / 48

_DOOR_NORTH_HITBOX_INFO = pg.Vector3(0, 0, -0.5 + _DOOR_D / 2), Hitbox(_DOOR_W, _DOOR_H, _DOOR_D)
_DOOR_EAST_HITBOX_INFO = pg.Vector3(0, 0, 0.5 - _DOOR_D / 2), Hitbox(_DOOR_W, _DOOR_H, _DOOR_D)
_DOOR_SOUTH_HITBOX_INFO = pg.Vector3(-0.5 + _DOOR_D / 2, 0, 0), Hitbox(_DOOR_D, _DOOR_H, _DOOR_W)
_DOOR_WEST_HITBOX_INFO = pg.Vector3(0.5 - _DOOR_D / 2, 0, 0), Hitbox(_DOOR_D, _DOOR_H, _DOOR_W)


@dataclass(kw_only=True)
class TileProperties:
    solid: bool = False
    opaque: bool = False
    map_colour: tuple[int, int, int]

    def __post_init__(self) -> None:
        # auto convert hex colours
        if isinstance(self.map_colour, str):
            map_colour = self.map_colour.strip("#")
            self.map_colour = (int(map_colour[0:2], 16), int(map_colour[2:4], 16), int(map_colour[4:6], 16))


class TileType(StrEnum):
    # these must match the tile type keys in `assets/lore/tiles.json`

    EMPTY = "empty"
    WALL = "wall"
    DOOR_CLOSED = "door_closed"
    DOOR_OPEN = "door_open"


class Tile:
    def __init__(self, typ: TileType) -> None:
        self.typ = typ
        self.explored: bool = False
        self.facing: Facing = Facing.SOUTH
        self.flipped: bool = False

    def get_hitbox_info(self) -> tuple[pg.Vector3, Hitbox]:
        """Returns (hitbox_offset_from_centre, hitbox)"""

        if self.typ == TileType.DOOR_CLOSED:
            if self.facing == Facing.NORTH:
                return _DOOR_NORTH_HITBOX_INFO
            elif self.facing == Facing.SOUTH:
                return _DOOR_EAST_HITBOX_INFO
            elif self.facing == Facing.WEST:
                return _DOOR_SOUTH_HITBOX_INFO
            else:
                return _DOOR_WEST_HITBOX_INFO

        elif self.typ == TileType.DOOR_OPEN:
            if self.facing == Facing.NORTH:
                return _DOOR_WEST_HITBOX_INFO if self.flipped else _DOOR_EAST_HITBOX_INFO
            elif self.facing == Facing.SOUTH:
                return _DOOR_WEST_HITBOX_INFO if self.flipped else _DOOR_EAST_HITBOX_INFO
            elif self.facing == Facing.WEST:
                return _DOOR_NORTH_HITBOX_INFO if self.flipped else _DOOR_SOUTH_HITBOX_INFO
            else:
                return _DOOR_NORTH_HITBOX_INFO if self.flipped else _DOOR_SOUTH_HITBOX_INFO

        return pg.Vector3(), Hitbox(1, 1, 1)
