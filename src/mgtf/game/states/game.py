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


import math
from typing import TYPE_CHECKING

from pygame import Surface, Event
from pygame.key import ScancodeWrapper

from .base import State
import mgtf.core.colours as cols
from mgtf.core.controls import Controls
from mgtf.dungeon.generator import generate_dungeon
from mgtf.dungeon.tile import TileType
from mgtf.dungeon.dungeon import Dungeon
from mgtf.objects.player import Player
from mgtf.core.constants import (
    TILE_WIDTH,
    TILE_DEPTH,
    TILE_HEIGHT,
    SCREEN_CENTRE_X,
    SCREEN_CENTRE_Z,
    RENDER_DISTANCE_X,
    RENDER_DISTANCE_Z
)

if TYPE_CHECKING:
    from mgtf.game.game import Game


class GameState(State):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self.player = Player((0, 0, 0), self.game.assets.images.player)
        self.floor = 1

        self.reset()

    def reset(self) -> None:
        self.dungeon_levels: dict[int, Dungeon] = {1: generate_dungeon()}  # {floor: dungeon}
        self.player.reset()

    def update(self, dt_s: float) -> None:
        pass

    def take_input(self, keys: ScancodeWrapper, events: list[Event], dt_s: float) -> None:
        if keys[Controls.MOVE_UP]:
            self.player.pos.z -= self.player.speed * dt_s
        if keys[Controls.MOVE_DOWN]:
            self.player.pos.z += self.player.speed * dt_s
        if keys[Controls.MOVE_LEFT]:
            self.player.pos.x -= self.player.speed * dt_s
        if keys[Controls.MOVE_RIGHT]:
            self.player.pos.x += self.player.speed * dt_s

    def draw(self, surface: Surface) -> None:
        surface.fill(cols.BG)
        all_entities = [self.player]

        current_floor = self.dungeon_levels[self.floor]

        render_left = math.floor(self.player.pos.x) - RENDER_DISTANCE_X
        render_right = math.floor(self.player.pos.x) + RENDER_DISTANCE_X
        render_back = math.floor(self.player.pos.z) - RENDER_DISTANCE_Z
        render_front = math.floor(self.player.pos.z) + RENDER_DISTANCE_Z

        for z in range(render_back, render_front + 1):
            # Draw tiles first
            for x in range(render_left, render_right + 1):
                tile = current_floor[x, z]

                tile_left = SCREEN_CENTRE_X + (x - self.player.pos.x - 0.5) * TILE_WIDTH
                tile_top = SCREEN_CENTRE_Z + (z - self.player.pos.z - 1) * TILE_DEPTH - self.player.pos.y * TILE_HEIGHT


                if tile.typ == TileType.WALL:
                    image = self.game.assets.images.wall
                elif tile.typ == TileType.DOOR:
                    surface.blit(self.game.assets.images.floor, (tile_left, tile_top))
                    image = self.game.assets.images.door_south
                elif tile.typ == TileType.EMPTY:
                    image = self.game.assets.images.floor
                else:
                    raise ValueError(f"unhandled tile type: '{tile.typ}'")

                surface.blit(image, (tile_left, tile_top))

            # Draw entities infront
            for entity in (e for e in all_entities if z - 1 < e.pos.z < z):
                entity_left = SCREEN_CENTRE_X + (entity.pos.x - self.player.pos.x - 0.5) * TILE_WIDTH
                entity_top = SCREEN_CENTRE_Z + (entity.pos.z - self.player.pos.z - 1) * TILE_DEPTH
                surface.blit(entity.image, (entity_left, entity_top))
