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

from .widget import Widget
from mgtf.core.custom_types import Colour
from mgtf.core.utils import crop_text_to_fit, get_text_surf


class Label(Widget):
    def __init__(self, *, flex: int = 0, text: str, font: pg.font.Font, colour: Colour) -> None:
        super().__init__(flex=flex)
        self._colour = colour
        self._font = font
        self._text = text
        self._cached_surface = self._refresh_text_surface()

    def _refresh_text_surface(self) -> pg.Surface:
        text = crop_text_to_fit(self._text, self._font, self.rect.width)
        surface = get_text_surf(self._font, text, self._colour)
        return surface

    def set_text(self, text: str) -> None:
        self._text = text
        self._cached_surface = self._refresh_text_surface()

    def preferred_size(self) -> tuple[int, int]:
        return self._font.size(self._text)

    def layout(self, rect: pg.Rect) -> None:
        self.rect = rect

    def draw(self, surface: pg.Surface) -> None:
        surface.blit(self._cached_surface, self.rect)
