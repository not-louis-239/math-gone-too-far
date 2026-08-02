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


from mgtf.dungeon.dungeon import Dungeon
from mgtf.dungeon.tile import TileType
from mgtf.dungeon.constants import MIN_AREA_COEFF, MAX_RETRIES


def _make_dungeon(width: int, height: int) -> Dungeon:
    ...


def generate_dungeon(width: int, height: int) -> Dungeon:
    """Make a dungeon, enforcing `MIN_AREA_COEFF`"""

    min_area = width * height * MIN_AREA_COEFF

    for _ in range(MAX_RETRIES):
        test_dungeon = _make_dungeon(width, height)

        non_wall = sum(
            1 for x in range(width)
            for y in range(height)
            if test_dungeon.tiles[y][x].typ != TileType.WALL
        )

        if non_wall >= min_area:
            break

    return test_dungeon
