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

from mgtf.core.paths import FONTS_DIR


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
        pass


class Sounds:
    def __init__(self) -> None:
        pass


class Assets:
    def __init__(self) -> None:
        self.fonts = Fonts()
        self.images = Images()
        self.sounds = Sounds()
