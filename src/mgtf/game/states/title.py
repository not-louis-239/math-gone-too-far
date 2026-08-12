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


from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

import mgtf.core.colours as cols
from mgtf.core.constants import WN_W, WN_H, UI_PADDING

from .base import State

from mgtf.ui.elements import Label, VBox, RectButton, Spacer, HBox

if TYPE_CHECKING:
    from mgtf.game.game import Game


class TitleState(State):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self.start_button = RectButton(text="Start", font=self.game.assets.fonts.button, inset=UI_PADDING)

        self.display_vbox = VBox(
            HBox(
                Spacer(flex=1),
                Label(text="Math Gone Too Far", font=game.assets.fonts.title, colour=cols.FG_HEADER),
                Spacer(flex=1)
            ),
            Spacer(flex=1),
            HBox(
                Spacer(flex=1),
                self.start_button,
                Spacer(flex=1)
            )
        )

        self.display_vbox.layout(pg.Rect(UI_PADDING, UI_PADDING, WN_W - 2 * UI_PADDING, WN_H - 2 * UI_PADDING))

    def reset(self) -> None:
        pass

    def update(self, dt_s: float) -> None:
        pass

    def take_input(self, keys: pg.key.ScancodeWrapper, events: list[pg.Event], dt_s: float) -> None:
        pass

    def draw(self, surface: pg.Surface) -> None:
        surface.fill(cols.BG)
        self.display_vbox.draw(surface)
