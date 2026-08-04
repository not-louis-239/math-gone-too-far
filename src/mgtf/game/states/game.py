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


import random
from typing import TYPE_CHECKING

import pygame as pg
from pygame import Surface, Event
from pygame.key import ScancodeWrapper

from mgtf.objects.entity import Facing

from .base import State
import mgtf.core.colours as cols
from mgtf.core.controls import Controls
from mgtf.objects.entity import collides
from mgtf.dungeon.generator import generate_dungeon
from mgtf.dungeon.tile import TileType
from mgtf.dungeon.dungeon import Dungeon
from mgtf.dungeon.constants import DUNGEON_W, DUNGEON_H
from mgtf.core.asset_manager import TILE_PROPERTIES
from mgtf.objects.player import Player, PLAYER_HITBOX
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


NEIGHBOURS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))


class GameState(State):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self.player = Player((random.randint(0, DUNGEON_W), 0, random.randint(0, DUNGEON_H)), self.game.assets.images.player, PLAYER_HITBOX)
        self.floor = 1

        self.reset()

    def _world_to_screen_pos(self, world_pos: tuple[float, float, float] | pg.Vector3) -> tuple[float, float]:
        wx, wy, wz = world_pos
        return SCREEN_CENTRE_X + (wx - self.player.pos.x) * TILE_WIDTH, SCREEN_CENTRE_Z + (wz - self.player.pos.z) * TILE_DEPTH - (wy - self.player.pos.y) * TILE_HEIGHT

    @property
    def current_floor(self) -> Dungeon:
        return self.dungeon_levels[self.floor]

    def reset(self) -> None:
        self.dungeon_levels: dict[int, Dungeon] = {1: generate_dungeon()}  # {floor: dungeon}
        self.player.reset()
        self.player.pos.x, self.player.pos.z = self.dungeon_levels[1].entrance_pos

    def update(self, dt_s: float) -> None:
        pass

    def take_input(self, keys: ScancodeWrapper, events: list[Event], dt_s: float) -> None:
        if keys[Controls.MOVE_BACK]:
            self.player.facing = Facing.NORTH
            target_pos = (self.player.pos.x, self.player.pos.z - self.player.speed * dt_s)
            if self.current_floor.is_vacant(target_pos, self.player.hitbox):
                self.player.pos.x, self.player.pos.z = target_pos

        if keys[Controls.MOVE_FWD]:
            target_pos = (self.player.pos.x, self.player.pos.z + self.player.speed * dt_s)
            self.player.facing = Facing.SOUTH
            if self.current_floor.is_vacant(target_pos, self.player.hitbox):
                self.player.pos.x, self.player.pos.z = target_pos

        if keys[Controls.MOVE_LEFT]:
            self.player.facing = Facing.WEST
            target_pos = (self.player.pos.x - self.player.speed * dt_s, self.player.pos.z)
            if self.current_floor.is_vacant(target_pos, self.player.hitbox):
                self.player.pos.x, self.player.pos.z = target_pos

        if keys[Controls.MOVE_RIGHT]:
            self.player.facing = Facing.EAST
            target_pos = (self.player.pos.x + self.player.speed * dt_s, self.player.pos.z)
            if self.current_floor.is_vacant(target_pos, self.player.hitbox):
                self.player.pos.x, self.player.pos.z = target_pos

    def draw(self, surface: Surface) -> None:
        surface.fill(cols.BG)
        all_entities = [self.player]

        render_left = max(0, round(self.player.pos.x) - RENDER_DISTANCE_X)
        render_right = min(DUNGEON_W - 1, round(self.player.pos.x) + RENDER_DISTANCE_X)
        render_back = max(0, round(self.player.pos.z) - RENDER_DISTANCE_Z)
        render_front = min(DUNGEON_H - 1, round(self.player.pos.z) + RENDER_DISTANCE_Z + 1)

        for z in range(render_back, render_front + 1):
            # Draw tiles first
            for x in range(render_left, render_right + 1):
                tile = self.current_floor[x, z]

                # Skip rendering wall tiles that are entirely surrounded by walls
                if (
                    tile.typ == TileType.WALL
                    and all(
                        self.current_floor[x + dx, z + dz].typ == TileType.WALL
                        for dx, dz in NEIGHBOURS
                        if 0 <= x + dx < DUNGEON_W and 0 <= z + dz < DUNGEON_H
                    )
                ):
                    continue

                tile_left, tile_top = self._world_to_screen_pos((x - tile.hitbox.w / 2, tile.hitbox.h, z - tile.hitbox.d / 2))

                if (x, z) == self.current_floor.entrance_pos:
                    image = self.game.assets.images.entrance
                elif tile.typ == TileType.WALL:
                    image = self.game.assets.images.wall
                elif tile.typ == TileType.DOOR:
                    surface.blit(self.game.assets.images.floor, (tile_left, tile_top))
                    if not tile.activated:
                        if tile.facing == Facing.NORTH:
                            image = self.game.assets.images.door_north
                        elif tile.facing == Facing.EAST:
                            image = self.game.assets.images.door_east
                        elif tile.facing == Facing.SOUTH:
                            image = self.game.assets.images.door_south
                        else:
                            image = self.game.assets.images.door_west
                    else:
                        # DEBUG placeholder for activated doors
                        if tile.facing == Facing.NORTH:
                            image = self.game.assets.images.door_north
                        elif tile.facing == Facing.EAST:
                            image = self.game.assets.images.door_east
                        elif tile.facing == Facing.SOUTH:
                            image = self.game.assets.images.door_south
                        else:
                            image = self.game.assets.images.door_west

                elif tile.typ == TileType.EMPTY:
                    image = self.game.assets.images.floor
                else:
                    raise ValueError(f"unhandled tile type: '{tile.typ}'")

                surface.blit(image, (tile_left, tile_top))

            for entity in (e for e in all_entities if z == round(e.pos.z)):
                entity_left, entity_top = self._world_to_screen_pos((entity.pos.x - entity.hitbox.w / 2, entity.pos.y + entity.hitbox.h, entity.pos.z - entity.hitbox.d / 2))
                surface.blit(entity.images[entity.facing], (entity_left, entity_top))

                # Show hitboxes
                if self.game.diagnostics.enabled:
                    pg.draw.rect(surface, cols.DIAG_HITBOX_TOP, (entity_left, entity_top, entity.hitbox.w * TILE_WIDTH, entity.hitbox.d * TILE_DEPTH), width=2)
                    pg.draw.rect(surface, cols.DIAG_HITBOX_BOTTOM, (entity_left, entity_top + TILE_HEIGHT * entity.hitbox.h, entity.hitbox.w * TILE_WIDTH, entity.hitbox.d * TILE_DEPTH), width=2)
                    pg.draw.rect(surface, cols.DIAG_HITBOX_FRONT, (entity_left, entity_top + TILE_DEPTH * entity.hitbox.d, entity.hitbox.w * TILE_WIDTH, entity.hitbox.h * TILE_HEIGHT), width=2)

        # Show diagnostics for the four tiles immediately adjacent to the player
        if self.game.diagnostics.enabled:
            for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nx, nz = round(self.player.pos.x) + dx, round(self.player.pos.z) + dz
                tile_left, tile_top = self._world_to_screen_pos((nx - 0.5, tile.hitbox.h, nz - 0.5))
                pg.draw.rect(surface, cols.DIAG_TILE_NEIGHBOURS, (tile_left, tile_top, TILE_WIDTH, TILE_HEIGHT), width=2)
