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
from mgtf.core.utils import get_reduced_alpha_tile
from mgtf.dungeon.generator import generate_dungeon
from mgtf.dungeon.tile import TileType
from mgtf.dungeon.dungeon import Dungeon
from mgtf.dungeon.constants import DUNGEON_GEN_W, DUNGEON_GEN_H
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

MINIMAP_TOP = 20
MINIMAP_LEFT = 20
MINIMAP_TILE_SIZE = 5
MINIMAP_SIZE = 150
MINIMAP_PLAYER_POINTER_SIZE = 2


@dataclass
class _Render:
    surface: pg.Surface
    priority: float  # higher = drawn later
    screen_pos: tuple[float, float]  # top-left-back corner


class GameState(State):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        self.minimap_surface = pg.Surface((MINIMAP_SIZE, MINIMAP_SIZE))
        self.player = Player((random.randint(0, DUNGEON_GEN_W), 0, random.randint(0, DUNGEON_GEN_H)), self.game.assets.images.player, PLAYER_HITBOX)
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
        render_right = min(DUNGEON_GEN_W - 1, round(self.player.pos.x + half_size / MINIMAP_TILE_SIZE))
        render_back = max(0, round(self.player.pos.z - half_size / MINIMAP_TILE_SIZE))
        render_front = min(DUNGEON_GEN_H - 1, round(self.player.pos.z + half_size / MINIMAP_TILE_SIZE))

        # Draw the tiles
        for z in range(render_back, render_front + 1):
            for x in range(render_left, render_right + 1):
                tile = self.current_floor[x, z]
                screen_x, screen_y = half_size + (x - self.player.pos.x - 0.5) * MINIMAP_TILE_SIZE, half_size + (z - self.player.pos.z - 0.5) * MINIMAP_TILE_SIZE

                if (
                    tile.typ == TileType.WALL
                    and all(
                        self.current_floor[x + dx, z + dz].typ == TileType.WALL
                        for dx, dz in NEIGHBOURS
                        if 0 <= x + dx < DUNGEON_GEN_W and 0 <= z + dz < DUNGEON_GEN_H
                    )
                ):
                    colour = cols.MINIMAP_SOLID
                else:
                    colour = TILE_PROPERTIES[tile.typ].map_colour

                pg.draw.rect(self.minimap_surface, colour, (screen_x, screen_y, MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE))

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

        entrance_x, entrance_z = self.dungeon_levels[1].get_entrance_pos()
        entrance_tile = self.current_floor[entrance_x, entrance_z]
        self.player.pos.x, self.player.pos.z = entrance_x + (-1 if entrance_tile.flipped else 1), entrance_z

    def update(self, dt_s: float) -> None:
        # Push the player away if they are inside a wall
        if not self.current_floor.is_vacant((self.player.pos.x, self.player.pos.z), self.player.hitbox):
            x, z = round(self.player.pos.x), round(self.player.pos.z)
            tile = self.current_floor[x, z]
            tile_x_offset, tile_z_offset = tile.get_hitbox_info()[0].xz
            tile_x, tile_z = x + tile_x_offset, z + tile_z_offset
            self.player.pos.move_towards_ip((tile_x, self.player.pos.y, tile_z), -dt_s)  # quick fix

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

                # Try to open the current door first, then the one that is just one tile away in the direction
                # the player is facing
                for candidate_dx, candidate_dz in ((0, 0), (dx, dz)):
                    focused_tile_coord = round(self.player.pos.x) + candidate_dx, round(self.player.pos.z) + candidate_dz
                    if self.current_floor[focused_tile_coord].typ == TileType.DOOR_CLOSED:
                        self.current_floor[focused_tile_coord].typ = TileType.DOOR_OPEN
                        break

    def draw(self, surface: Surface) -> None:
        surface.fill(cols.BG)
        all_entities = [self.player]

        render_left = max(0, round(self.player.pos.x) - RENDER_DISTANCE_X)
        render_right = min(self.current_floor.width - 1, round(self.player.pos.x) + RENDER_DISTANCE_X)
        render_back = max(0, round(self.player.pos.z) - RENDER_DISTANCE_Z)
        render_front = min(self.current_floor.depth - 1, round(self.player.pos.z) + RENDER_DISTANCE_Z + 1)

        # Pick render elements to draw
        render_elems: list[_Render] = []

        player_rect = pg.Rect(
            SCREEN_CENTRE_X - TILE_WIDTH * PLAYER_HITBOX.w / 2,
            SCREEN_CENTRE_Z - TILE_HEIGHT * PLAYER_HITBOX.h - TILE_DEPTH * PLAYER_HITBOX.d / 2,
            TILE_WIDTH * PLAYER_HITBOX.w,
            TILE_HEIGHT * PLAYER_HITBOX.h + TILE_DEPTH * PLAYER_HITBOX.d
        )

        for z in range(render_back, render_front + 1):
            # Draw tiles first
            for x in range(render_left, render_right + 1):
                # Skip rendering wall tiles that are entirely surrounded by walls
                tile = self.current_floor[x, z]
                t_hitbox_offset, t_hitbox = tile.get_hitbox_info()

                if (
                    tile.typ == TileType.WALL
                    and all(
                        self.current_floor[x + dx, z + dz].typ == TileType.WALL
                        for dx, dz in NEIGHBOURS
                        if 0 <= x + dx < DUNGEON_GEN_W and 0 <= z + dz < DUNGEON_GEN_H
                    )
                ):
                    continue

                if tile.typ == TileType.ENTRANCE:
                    image = self.game.assets.images.entrance_flipped if tile.flipped else self.game.assets.images.entrance

                elif tile.typ == TileType.WALL:
                    image = self.game.assets.images.wall

                elif tile.typ == TileType.DOOR_CLOSED:
                    if tile.facing == Facing.NORTH:
                        image = self.game.assets.images.door_north_flipped if tile.flipped else self.game.assets.images.door_north
                    elif tile.facing == Facing.EAST:
                        image = self.game.assets.images.door_east
                    elif tile.facing == Facing.SOUTH:
                        image = self.game.assets.images.door_south_flipped if tile.flipped else self.game.assets.images.door_south
                    else:
                        image = self.game.assets.images.door_west

                elif tile.typ == TileType.DOOR_OPEN:
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

                left = x - 0.5
                top = 1
                back = z - 0.5
                priority = z + t_hitbox_offset.z + t_hitbox.d / 2 if tile.typ != TileType.EMPTY else 0

                if tile.typ in (TileType.DOOR_CLOSED, TileType.DOOR_OPEN):
                    # Some tiles, like closed doors, require an extra floor tile to be rendered underneath
                    render_elems.append(_Render(self.game.assets.images.floor, 0, self._world_to_screen_pos((left, top, back))))

                # Draw the tile at half alpha if it is immediately infront of the player
                tile_rect = pg.Rect(*self._world_to_screen_pos((left, top, back)), TILE_WIDTH, TILE_HEIGHT + TILE_DEPTH)

                if z > self.player.pos.z and player_rect.colliderect(tile_rect) and TILE_PROPERTIES[tile.typ].solid:
                    image = get_reduced_alpha_tile(image)  # the half-alpha version of the tile

                render_elems.append(_Render(image, priority, self._world_to_screen_pos((left, top, back))))

        for entity in all_entities:
            x = entity.pos.x - entity.hitbox.w / 2
            y = entity.pos.y + entity.hitbox.h
            z = entity.pos.z - entity.hitbox.d / 2
            priority = entity.pos.z + entity.hitbox.d / 2

            render_elems.append(_Render(entity.images[entity.facing], priority, self._world_to_screen_pos((x, y, z))))

        # Sort by depth
        render_elems.sort(key=lambda elem: elem.priority)
        blitters = [(elem.surface, elem.screen_pos) for elem in render_elems]
        surface.blits(blitters)

        self._draw_hud(surface)
