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


from abc import abstractmethod

import pygame as pg

from .widget import Widget

from mgtf.core.custom_types import Colour
from mgtf.core.constants import BORDER_W
from mgtf.core.utils import get_text_surf


class _Button(Widget):
    def __init__(
            self, *, flex: int = 0,
            text: str, font: pg.font.Font, inset: int = 0,
            col_bg: Colour, col_fg: Colour, col_border: Colour
        ) -> None:
        super().__init__(flex=flex)
        self.text = text
        self.font = font
        self.inset = inset

        self.col_bg = col_bg
        self.col_fg = col_fg
        self.col_border = col_border

    @abstractmethod
    def check_click(self, mouse_pos: tuple[int, int]) -> bool:
        ...

    def preferred_size(self) -> tuple[int, int]:
        width, height = self.font.size(self.text)
        return width + 2 * self.inset, height + 2 * self.inset

    def layout(self, rect: pg.Rect) -> None:
        self.rect = rect

class RectButton(_Button):
    def check_click(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)

    def draw(self, surface: pg.Surface) -> None:
        pg.draw.rect(surface, self.col_bg, self.rect)
        pg.draw.rect(surface, self.col_border, self.rect, width=BORDER_W)

        text_surf = get_text_surf(self.font, self.text, self.col_fg)
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))
