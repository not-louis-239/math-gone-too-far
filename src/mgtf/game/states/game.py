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
import random
from typing import TYPE_CHECKING

import pygame as pg
from pygame import Surface, Event
from pygame.key import ScancodeWrapper

from .base import State
import mgtf.core.colours as cols
from mgtf.core.controls import Controls
from mgtf.objects.hitbox import collides
from mgtf.dungeon.generator import generate_dungeon
from mgtf.dungeon.tile import TileType
from mgtf.dungeon.dungeon import Dungeon
from mgtf.dungeon.constants import DUNGEON_W, DUNGEON_H
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

        self.player = Player((random.randint(0, DUNGEON_W), 0, random.randint(0, DUNGEON_H)), self.game.assets.images.player)
        self.floor = 1

        self.reset()

    @property
    def current_floor(self) -> Dungeon:
        return self.dungeon_levels[self.floor]

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

        # if the player is touching a wall, push them away from the wall
        for x in range(max(0, math.floor(self.player.pos.x) - 2), min(DUNGEON_W, math.floor(self.player.pos.x) + 3)):
            for z in range(max(0, math.floor(self.player.pos.z) - 2), min(DUNGEON_H, math.floor(self.player.pos.z) + 3)):
                tile = self.current_floor[x, z]
                if (
                    self.game.assets.lore.tile_properties[tile.typ].solid
                    and collides(
                        self.player.pos,
                        self.player.hitbox,
                        (x, 0, z),
                        (1, 1, 1)
                    )
                ):
                    print((x, 0, z))
                    print(self.player.pos)
                    self.player.pos.move_towards_ip((x, 0, z), -self.player.speed * dt_s)

    def draw(self, surface: Surface) -> None:
        surface.fill(cols.BG)
        all_entities = [self.player]

        render_left = max(0, math.floor(self.player.pos.x) - RENDER_DISTANCE_X)
        render_right = min(DUNGEON_W - 1, math.floor(self.player.pos.x) + RENDER_DISTANCE_X)
        render_back = max(0, math.floor(self.player.pos.z) - RENDER_DISTANCE_Z)
        render_front = min(DUNGEON_H - 1, math.floor(self.player.pos.z) + RENDER_DISTANCE_Z)

        for z in range(render_back, render_front + 1):
            # Draw tiles first
            for x in range(render_left, render_right + 1):
                tile = self.current_floor[x, z]

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

            for entity in (e for e in all_entities if z - 0.5 <= e.pos.z < z + 0.5):
                entity_top = SCREEN_CENTRE_Z + (entity.pos.z - self.player.pos.z - entity.hitbox.d / 2) * TILE_DEPTH - entity.hitbox.h * TILE_HEIGHT
                entity_left = SCREEN_CENTRE_X + (entity.pos.x - self.player.pos.x - entity.hitbox.w / 2) * TILE_WIDTH
                surface.blit(entity.image, (entity_left, entity_top))

                if self.game.diagnostics.enabled:
                    pg.draw.rect(surface, cols.DIAG_HITBOX_TOP, (entity_left, entity_top, entity.hitbox.w * TILE_WIDTH, entity.hitbox.d * TILE_DEPTH), width=2)
                    pg.draw.rect(surface, cols.DIAG_HITBOX_BOTTOM, (entity_left, entity_top + TILE_HEIGHT * entity.hitbox.h, entity.hitbox.w * TILE_WIDTH, entity.hitbox.d * TILE_DEPTH), width=2)
                    pg.draw.rect(surface, cols.DIAG_HITBOX_FRONT, (entity_left, entity_top + TILE_DEPTH * entity.hitbox.d, entity.hitbox.w * TILE_WIDTH, entity.hitbox.h * TILE_HEIGHT), width=2)
