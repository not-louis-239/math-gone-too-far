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


import json
from pathlib import Path

from mgtf.core.paths import LORE_DIR
from mgtf.dungeon.tile import TileProperties, TileTypeID
from mgtf.objects.difficulty import DifficultyID, Difficulty


TILE_PROPERTIES: dict[TileTypeID, TileProperties] = {
    tile_type: TileProperties(**properties)
    for tile_type, properties in json.loads((LORE_DIR / "tiles.json").read_text()).items()
}

DIFFICULTIES: dict[DifficultyID, Difficulty] = {
    diff_id: Difficulty(**attrs)
    for diff_id, attrs in json.loads((LORE_DIR / "difficulties.json").read_text()).items()
}
