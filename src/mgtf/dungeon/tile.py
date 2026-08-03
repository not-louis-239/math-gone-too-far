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
import json

from dataclasses import dataclass


@dataclass(kw_only=True)
class TileProperties:
    solid: bool = False
    opaque: bool = False


class TileType(StrEnum):
    # these must match the tile type keys in `assets/lore/tiles.json`

    EMPTY = "empty"
    WALL = "wall"
    DOOR = "door"
    ENTRANCE = "entrance"


class TileFacing(StrEnum):
    NORTH = "n"
    EAST = "e"
    SOUTH = "s"
    WEST = "w"


class Tile:
    def __init__(self, typ: TileType) -> None:
        self.typ = typ
        self.explored: bool = False

        self.activated: bool = False
        self.facing: TileFacing = TileFacing.SOUTH
        self.flipped: bool = False
