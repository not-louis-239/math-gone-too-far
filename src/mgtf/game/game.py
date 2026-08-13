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

from mgtf.core.asset_manager import Assets
from mgtf.core.controls import Controls
from mgtf.debug.diagnostics import Diagnostics
from mgtf.game.states import GameState, State, TitleState, DifficultyState
from mgtf.game.states.base import StateID
from mgtf.objects.environment import Environment
from mgtf.objects.player import Player, PLAYER_HITBOX


class Game:
    def __init__(self) -> None:
        self.assets = Assets()
        self.diagnostics = Diagnostics(self.assets)

        self.env = Environment(self)
        self.player = Player((0, 0, 0), self.assets.images.player, PLAYER_HITBOX)

        self.state: StateID = StateID.TITLE
        self.states: dict[StateID, State] = {
            StateID.TITLE: TitleState(self),
            StateID.DIFFICULTY: DifficultyState(self),
            StateID.GAME: GameState(self)
        }

    def set_state(self, state: StateID) -> None:
        self.state = state

    def update(self, dt_s: float) -> None:
        self.states[self.state].update(dt_s)

    def take_input(self, keys: pg.key.ScancodeWrapper, events: list[pg.event.Event], dt_s: float) -> None:
        self.states[self.state].take_input(keys, events, dt_s)

        for event in events:
            if event.type == pg.KEYDOWN and event.key == Controls.DEBUG_TOGGLE:
                self.diagnostics.toggle_visibility()

    def draw(self, screen: pg.Surface) -> None:
        self.states[self.state].draw(screen)
