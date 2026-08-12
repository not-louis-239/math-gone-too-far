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
from pygame import Event, Surface
from pygame.key import ScancodeWrapper

from .base import State
from mgtf.core import colours as cols
from mgtf.core.constants import UI_PADDING, WN_W, WN_H
from mgtf.core.glitchy_string import GlitchyString
from mgtf.ui.elements import HBox, VBox, RectButton, Label, Spacer
from mgtf.objects.difficulty import DifficultyID

if TYPE_CHECKING:
    from mgtf.game.game import Game


class DifficultyState(State):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self.difficulty_buttons: dict[RectButton, DifficultyID] = {
            RectButton(text="Applications", font=self.game.assets.fonts.button): DifficultyID.APPLICATIONS,
            RectButton(text="Methods", font=self.game.assets.fonts.button): DifficultyID.METHODS,
            RectButton(text="Specialist", font=self.game.assets.fonts.button): DifficultyID.SPECIALIST,
            RectButton(text=GlitchyString("ValueError"), font=self.game.assets.fonts.button): DifficultyID.VALUE_ERROR
        }

        self.display_vbox = VBox(
            HBox(
                Spacer(),
                Label(text="Select Difficulty", font=self.game.assets.fonts.title),
                Spacer()
            ),
            Spacer(),
            *(HBox(
                Spacer(),
                button,
                Spacer(),
            ) for button in self.difficulty_buttons),
            Spacer(),
            gap=UI_PADDING
        )

        self.display_vbox.layout(pg.Rect(UI_PADDING, UI_PADDING, WN_W - 2 * UI_PADDING, WN_H - 2 * UI_PADDING))

    def update(self, dt_s: float) -> None:
        pass

    def take_input(self, keys: ScancodeWrapper, events: list[Event], dt_s: float) -> None:
        pass

    def draw(self, surface: Surface) -> None:
        surface.fill(cols.BG)
        self.display_vbox.draw(surface)
