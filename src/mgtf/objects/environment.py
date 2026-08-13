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

from mgtf.objects.player import Player, PLAYER_HITBOX
from mgtf.objects.entity import Entity
from mgtf.dungeon.dungeon import Dungeon
from mgtf.dungeon.generator import generate_dungeon

if TYPE_CHECKING:
    from mgtf.game.game import Game


class Environment:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.reset()

    def reset(self):
        # Reset the player and clear the floor dictionary
        # TODO: reset player stats
        self.floors: dict[int, Dungeon] = {1: generate_dungeon()}

        # Relocate player to the entrance of the first floor
        entrance_x, entrance_z = self.floors[1].get_entrance_pos()
        entrance_tile = self.current_floor()[entrance_x, entrance_z]
        self.game.player.pos.x, self.game.player.pos.z = entrance_x + (-1 if entrance_tile.flipped else 1), entrance_z

    def current_floor(self) -> Dungeon:
        return self.floors[self.game.player.data.floor]
