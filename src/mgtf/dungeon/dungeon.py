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

from mgtf.core.lore_loader import TILE_PROPERTIES
from mgtf.dungeon.tile import Tile, TileType
from mgtf.objects.entity import Hitbox


class Dungeon:
    def __init__(self, width: int, depth: int) -> None:
        self.tiles: list[list[Tile]] = [[Tile(typ=TileType.WALL) for _ in range(width)] for _ in range(depth)]

    @property
    def width(self) -> int:
        return len(self.tiles[0])

    @property
    def depth(self) -> int:
        return len(self.tiles)

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

    def is_vacant(self, pos: tuple[float, float], hitbox: Hitbox) -> bool:
        """Determine, given a `pos` and a `hitbox`, whether `pos` is vacant and does not overlap
        any walls."""
        px, pz = pos
        left, right = px - hitbox.w / 2, px + hitbox.w / 2
        back, front = pz - hitbox.d / 2, pz + hitbox.d / 2

        for tx in range(max(0, round(px) - 1), min(self.width, round(px) + 2)):
            for tz in range(max(0, round(pz) - 1), min(self.depth, round(pz) + 2)):
                tile = self[tx, tz]
                t_hitbox_offset, t_hitbox = tile.get_hitbox_info()

                if (
                    TILE_PROPERTIES[tile.typ].solid
                    and not (
                        left > tx + t_hitbox_offset.x + t_hitbox.w / 2
                        or right < tx + t_hitbox_offset.x - t_hitbox.w / 2
                        or back > tz + t_hitbox_offset.z + t_hitbox.d / 2
                        or front < tz + t_hitbox_offset.z - t_hitbox.d / 2
                    )
                ):
                    return False

        return True

    def get_entrance_pos(self) -> tuple[int, int]:
        """Returns the position of the first cell, starting from the top-left, that is a
        `TileType.ENTRANCE` tile. Return a sentinel if no such tile exists."""
        for z in range(self.depth):
            for x in range(self.width):
                if self[x, z].typ == TileType.ENTRANCE:
                    return (x, z)

        return (-1, -1)

    def line_of_sight(self, start_pos: tuple[int, int], end_pos: tuple[int, int]) -> bool:
        """Returns `True` if there are no solid tiles between
        `start_pos` and `end_pos`.
        LOS will be not be blocked regardless of whether `start_pos`
        or `end_pos` themselves are solid tiles."""

        # Uses an adaptation of Bresenham's line algorithm to check
        # tiles along the way.

        x1, z1 = start_pos
        x2, z2 = end_pos

        dx = abs(x2 - x1)
        sx = 1 if x2 > x1 else -1

        dz = -abs(z2 - z1)
        sz = 1 if z2 > z1 else -1

        error = dx + dz

        while True:
            if (x1, z1) == end_pos:
                return True
            if TILE_PROPERTIES[self[x1, z1].typ].opaque and (x1, z1) != start_pos:
                return False

            e_times_2 = 2 * error

            if e_times_2 >= dz:
                error += dz
                x1 += sx

            if e_times_2 <= dx:
                error += dx
                z1 += sz
