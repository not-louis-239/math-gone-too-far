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
from dataclasses import dataclass

import pygame as pg
from pygame import Surface, Event
from pygame.key import ScancodeWrapper

from mgtf.objects.entity import Facing

from .base import State
import mgtf.core.colours as cols
from mgtf.core.controls import Controls
from mgtf.core.lore_loader import TILE_PROPERTIES
from mgtf.dungeon.generator import generate_dungeon
from mgtf.dungeon.tile import TileType
from mgtf.dungeon.dungeon import Dungeon
from mgtf.dungeon.constants import DUNGEON_W, DUNGEON_H
from mgtf.objects.player import Player, PLAYER_HITBOX
from mgtf.objects.entity import Entity
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

MINIMAP_TOP = 20
MINIMAP_LEFT = 20
MINIMAP_TILE_SIZE = 5
MINIMAP_SIZE = 150
MINIMAP_PLAYER_POINTER_SIZE = 2


@dataclass
class _Render:
    surface: pg.Surface
    priority: float  # higher = drawn later
    world_pos: tuple[float, float, float]  # top-left-back corner


class GameState(State):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self.minimap_surface = pg.Surface((MINIMAP_SIZE, MINIMAP_SIZE))
        self.player = Player((random.randint(0, DUNGEON_W), 0, random.randint(0, DUNGEON_H)), self.game.assets.images.player, PLAYER_HITBOX)
        self.floor = 1

        self.reset()

    def _world_to_screen_pos(self, world_pos: tuple[float, float, float] | pg.Vector3) -> tuple[float, float]:
        wx, wy, wz = world_pos
        return SCREEN_CENTRE_X + (wx - self.player.pos.x) * TILE_WIDTH, SCREEN_CENTRE_Z + (wz - self.player.pos.z) * TILE_DEPTH - (wy - self.player.pos.y) * TILE_HEIGHT

    def _draw_minimap(self, surface: pg.Surface) -> None:
        half_size = MINIMAP_SIZE / 2
        self.minimap_surface.fill(cols.MINIMAP_OOB)

        # Determine render bounds
        render_left = max(0, round(self.player.pos.x - half_size / MINIMAP_TILE_SIZE))
        render_right = min(DUNGEON_W - 1, round(self.player.pos.x + half_size / MINIMAP_TILE_SIZE))
        render_back = max(0, round(self.player.pos.z - half_size / MINIMAP_TILE_SIZE))
        render_front = min(DUNGEON_H - 1, round(self.player.pos.z + half_size / MINIMAP_TILE_SIZE))

        # Draw the tiles
        for z in range(render_back, render_front + 1):
            for x in range(render_left, render_right + 1):
                tile = self.current_floor[x, z]
                screen_x, screen_y = half_size + (x - self.player.pos.x - 0.5) * MINIMAP_TILE_SIZE, half_size + (z - self.player.pos.z - 0.5) * MINIMAP_TILE_SIZE
                pg.draw.rect(self.minimap_surface, TILE_PROPERTIES[tile.typ].map_colour, (screen_x, screen_y, MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE))

        # Blit the minimap surface onto the main surface
        surface.blit(self.minimap_surface, (MINIMAP_LEFT, MINIMAP_TOP))

        # Draw the player pointer
        pg.draw.circle(surface, cols.MINIMAP_PLAYER_POINTER, (MINIMAP_LEFT + half_size, MINIMAP_TOP + half_size), 2)

        # Draw the border
        pg.draw.rect(surface, cols.MINIMAP_BORDER, (MINIMAP_LEFT, MINIMAP_TOP, MINIMAP_SIZE, MINIMAP_SIZE), width=2)


    def _draw_hud(self, surface: Surface) -> None:
        self._draw_minimap(surface)

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

        for event in events:
            if event.type == pg.KEYDOWN and event.key == Controls.INTERACT:
                if self.player.facing == Facing.NORTH:
                    dx, dz = 0, -1
                elif self.player.facing == Facing.SOUTH:
                    dx, dz = 0, 1
                elif self.player.facing == Facing.EAST:
                    dx, dz = 1, 0
                elif self.player.facing == Facing.WEST:
                    dx, dz = -1, 0

                # Try to open the current door first, then the
                for candidate_dx, candidate_dz in ((0, 0), (dx, dz)):
                    focused_tile_coord = round(self.player.pos.x) + candidate_dx, round(self.player.pos.z) + candidate_dz
                    if self.current_floor[focused_tile_coord].typ == TileType.DOOR_CLOSED:
                        self.current_floor[focused_tile_coord].typ = TileType.DOOR_OPEN
                        # TODO: handle door hitboxes for opened doors
                        break

    def draw(self, surface: Surface) -> None:
        surface.fill(cols.BG)
        all_entities = [self.player]

        render_left = max(0, round(self.player.pos.x) - RENDER_DISTANCE_X)
        render_right = min(DUNGEON_W - 1, round(self.player.pos.x) + RENDER_DISTANCE_X)
        render_back = max(0, round(self.player.pos.z) - RENDER_DISTANCE_Z)
        render_front = min(DUNGEON_H - 1, round(self.player.pos.z) + RENDER_DISTANCE_Z + 1)

        # Pick render elements to draw
        render_elems: list[tuple[tuple[int, int] | Entity, float]] = []

        for z in range(render_back, render_front + 1):
            # Draw tiles first
            for x in range(render_left, render_right + 1):
                # Skip rendering wall tiles that are entirely surrounded by walls
                tile = self.current_floor[x, z]
                t_hitbox_offset, t_hitbox = tile.get_hitbox_info()

                if not (
                    tile.typ == TileType.WALL
                    and all(
                        self.current_floor[x + dx, z + dz].typ == TileType.WALL
                        for dx, dz in NEIGHBOURS
                        if 0 <= x + dx < DUNGEON_W and 0 <= z + dz < DUNGEON_H
                    )
                ):
                    render_elems.append(((x, z), z + t_hitbox_offset.z + t_hitbox.d / 2 - (1 if tile.typ == TileType.EMPTY else 0)))

        for entity in all_entities:
            render_elems.append((entity, entity.pos.z + entity.hitbox.d / 2))

        # Sort by depth
        render_elems.sort(key=lambda elem: elem[1])

        for elem in render_elems:
            if isinstance(elem[0], Entity):
                # It's an entity!
                entity = elem[0]
                entity_vis_left, entity_vis_top = self._world_to_screen_pos((entity.pos.x - entity.images[entity.facing].width / 2 / TILE_WIDTH, entity.pos.y + entity.hitbox.h, entity.pos.z - entity.hitbox.d / 2))
                surface.blit(entity.images[entity.facing], (entity_vis_left, entity_vis_top))

                # Show hitboxes
                if self.game.diagnostics.enabled:
                    entity_hit_left, entity_hit_top = self._world_to_screen_pos((entity.pos.x - entity.hitbox.w / 2, entity.pos.y + entity.hitbox.h, entity.pos.z - entity.hitbox.d / 2))
                    pg.draw.rect(surface, cols.DIAG_HITBOX_TOP, (entity_hit_left, entity_hit_top, entity.hitbox.w * TILE_WIDTH, entity.hitbox.d * TILE_DEPTH), width=2)
                    pg.draw.rect(surface, cols.DIAG_HITBOX_BOTTOM, (entity_hit_left, entity_hit_top + TILE_HEIGHT * entity.hitbox.h, entity.hitbox.w * TILE_WIDTH, entity.hitbox.d * TILE_DEPTH), width=2)
                    pg.draw.rect(surface, cols.DIAG_HITBOX_FRONT, (entity_hit_left, entity_hit_top + TILE_DEPTH * entity.hitbox.d, entity.hitbox.w * TILE_WIDTH, entity.hitbox.h * TILE_HEIGHT), width=2)

            else:
                # It's a tile!
                x, z = elem[0]
                tile = self.current_floor[elem[0]]
                tile_left, tile_top = self._world_to_screen_pos((x - 0.5, 1, z - 0.5))

                if (x, z) == self.current_floor.entrance_pos:
                    image = self.game.assets.images.entrance
                elif tile.typ == TileType.WALL:
                    image = self.game.assets.images.wall

                elif tile.typ == TileType.DOOR_CLOSED:
                    surface.blit(self.game.assets.images.floor, (tile_left, tile_top))
                    if tile.facing == Facing.NORTH:
                        image = self.game.assets.images.door_north_flipped if tile.flipped else self.game.assets.images.door_north
                    elif tile.facing == Facing.EAST:
                        image = self.game.assets.images.door_east
                    elif tile.facing == Facing.SOUTH:
                        image = self.game.assets.images.door_south_flipped if tile.flipped else self.game.assets.images.door_south
                    else:
                        image = self.game.assets.images.door_west
                elif tile.typ == TileType.DOOR_OPEN:
                    surface.blit(self.game.assets.images.floor, (tile_left, tile_top))
                    if tile.facing == Facing.NORTH:
                        image = self.game.assets.images.door_west if tile.flipped else self.game.assets.images.door_east
                    elif tile.facing == Facing.EAST:
                        image = self.game.assets.images.door_north if tile.flipped else self.game.assets.images.door_south
                    elif tile.facing == Facing.SOUTH:
                        image = self.game.assets.images.door_west if tile.flipped else self.game.assets.images.door_east
                    else:
                        image = self.game.assets.images.door_north_flipped if tile.flipped else self.game.assets.images.door_south_flipped

                elif tile.typ == TileType.EMPTY:
                    image = self.game.assets.images.floor
                else:
                    raise ValueError(f"unhandled tile type: '{tile.typ}'")

                surface.blit(image, (tile_left, tile_top))

        # Show diagnostics for the four tiles immediately adjacent to the player
        if self.game.diagnostics.enabled:
            for dx, dz in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nx, nz = round(self.player.pos.x) + dx, round(self.player.pos.z) + dz
                tile_left, tile_top = self._world_to_screen_pos((nx - 0.5, 0, nz - 0.5))
                pg.draw.rect(surface, cols.DIAG_TILE_NEIGHBOURS, (tile_left, tile_top, TILE_WIDTH, TILE_HEIGHT), width=2)

        self._draw_hud(surface)
