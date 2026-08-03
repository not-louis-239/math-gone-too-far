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


from typing import overload, Iterator

from mgtf.core.asset_manager import TILE_PROPERTIES
from mgtf.dungeon.tile import Tile, TileType
from mgtf.objects.hitbox import Hitbox


class Dungeon:
    def __init__(self, width: int, depth: int) -> None:
        self.tiles: list[list[Tile]] = [[Tile(typ=TileType.WALL) for _ in range(width)] for _ in range(depth)]
        self.width = width
        self.depth = depth

    @overload
    def __getitem__(self, key: int) -> list[Tile]: ...
    @overload
    def __getitem__(self, key: tuple[int, int]) -> Tile: ...
    def __getitem__(self, key: int | tuple[int, int]) -> list[Tile] | Tile:
        if isinstance(key, int):
            return self.tiles[key]
        return self.tiles[key[1]][key[0]]

    def __setitem__(self, key: tuple[int, int], value: Tile):
        self.tiles[key[1]][key[0]] = value

    def __iter__(self) -> Iterator[list[Tile]]:
        for row in self.tiles:
            yield row

    def is_vacant(self, pos: tuple[int, int], hitbox: Hitbox) -> bool:
        """Determine, given a `pos` and a `hitbox`, whether `pos` is vacant and does not overlap
        any walls."""
        px, pz = pos
        left, right = px - hitbox.w / 2, px + hitbox.w / 2
        back, front = pz - hitbox.d / 2, pz + hitbox.d / 2

        for tx in range(px - 1, px + 2):
            for tz in range(pz - 1, pz + 2):
                if (
                    TILE_PROPERTIES[self[tx, tz].typ].solid
                    and not (
                        left > tx + 0.5
                        or right < tx - 0.5
                        or back > tz + 0.5
                        or front < tz - 0.5
                    )
                ):
                    return False

        return True
