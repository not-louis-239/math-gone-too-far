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


from typing import overload

from mgtf.dungeon.tile import Tile, TileType


class Dungeon:
    def __init__(self, width: int, height: int) -> None:
        self.tiles: list[list[Tile]] = [[Tile(typ=TileType.WALL) for _ in range(width)] for _ in range(height)]

    @overload
    def __getitem__(self, key: int) -> list[Tile]: ...
    @overload
    def __getitem__(self, key: tuple[int, int]) -> Tile: ...
    def __getitem__(self, key: int | tuple[int, int]) -> list[Tile] | Tile:
        if isinstance(key, int):
            return self.tiles[key]
        return self.tiles[key[1]][key[0]]
