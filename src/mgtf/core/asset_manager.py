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

from mgtf.core.paths import FONTS_DIR, IMAGES_DIR, LORE_DIR
from mgtf.objects.entity import Facing


class Fonts:
    def __init__(self) -> None:
        self.base_font_path = FONTS_DIR / "RobotoMono-Regular.ttf"

        self.title = pg.font.Font(self.base_font_path, 50)
        self.header = pg.font.Font(self.base_font_path, 36)
        self.text = pg.font.Font(self.base_font_path, 28)

        self.button = pg.font.Font(self.base_font_path, 36)
        self.small = pg.font.Font(self.base_font_path, 16)


class Images:
    def __init__(self) -> None:
        def load(name: str) -> pg.Surface:
            return pg.image.load(IMAGES_DIR / name).convert_alpha()

        # tiles
        self.floor = load("floor.png")
        self.wall = load("wall.png")
        self.door_north = load("door_north.png")
        self.door_north_flipped = pg.transform.flip(self.door_north, True, False)
        self.door_south = load("door_south.png")
        self.door_south_flipped = pg.transform.flip(self.door_south, True, False)
        self.door_east = load("door_east.png")
        self.door_west = load("door_west.png")
        self.entrance = load("entrance.png")

        # entities
        self.player: dict[Facing, pg.Surface] = {
            Facing.NORTH: load("player_north.png"),
            Facing.EAST: load("player_east.png"),
            Facing.SOUTH: load("player_south.png"),
            Facing.WEST: load("player_west.png")
        }


class Sounds:
    def __init__(self) -> None:
        pass


# Load lore
class Assets:
    def __init__(self) -> None:
        self.fonts = Fonts()
        self.images = Images()
        self.sounds = Sounds()
