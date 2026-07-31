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


from functools import lru_cache

import pygame as pg

from mgtf.core.custom_types import Colour


@lru_cache(maxsize=1024)
def crop_text_to_fit(font: pg.font.Font, text: str, max_width: int) -> str:
    if font.size(text)[0] <= max_width:
        return text

    ellipsis_char = "…"

    if font.size(ellipsis_char)[0] > max_width:
        return ""

    known_good = ""

    for char in text:
        candidate = known_good + char + ellipsis_char
        if font.size(candidate)[0] >= max_width:
            return known_good + ellipsis_char
        known_good += char

    return known_good


@lru_cache(maxsize=1024)
def _get_text_surf(font: pg.font.Font, text: str, colour: Colour) -> pg.Surface:
    return font.render(text, True, colour)

def get_text_surf(font: pg.font.Font, text: str, colour: Colour) -> pg.Surface:
    return _get_text_surf(font, text, colour)
