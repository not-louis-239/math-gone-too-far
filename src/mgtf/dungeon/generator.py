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

import random
from collections import deque
from dataclasses import dataclass

from mgtf.core.utils import chance
from mgtf.dungeon.dungeon import Dungeon
from mgtf.dungeon.tile import Tile, TileType
from mgtf.dungeon.constants import (
    MIN_AREA_COEFF,
    ROOM_SPAWN_COEFF,
    ROOM_H_MIN,
    ROOM_H_MAX,
    ROOM_W_MIN,
    ROOM_W_MAX,
    MAX_RETRIES,
    HALLWAY_W,
    DUNGEON_GEN_W,
    DUNGEON_GEN_H
)
from mgtf.objects.entity import Facing


_DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))


@dataclass
class _Room:
    left: int
    top: int
    width: int
    height: int

    def __hash__(self) -> int:
        return hash((self.left, self.top, self.width, self.height))

    @property
    def right(self) -> int:
        return self.left + self.width - 1

    @property
    def bottom(self) -> int:
        return self.top + self.height - 1

    @property
    def centre_x(self) -> int:
        return self.left + self.width // 2

    @property
    def centre_y(self) -> int:
        return self.top + self.height // 2

    @property
    def centre(self) -> tuple[int, int]:
        return self.centre_x, self.centre_y

    def touches(self, other: _Room) -> bool:
        # Return True if `self` is touching `other`

        bounding_left = self.left - 1
        bounding_right = self.left + self.width + 1
        bounding_top = self.top - 1
        bounding_bottom = self.top + self.height + 1

        # using AABB bounds checking
        return not (
            other.left > bounding_right
            or other.left + other.width < bounding_left
            or other.top > bounding_bottom
            or other.top + other.height < bounding_top
        )


def _get_reachable_points(dungeon: Dungeon, start_pos: tuple[int, int]) -> set[tuple[int, int]]:
    dungeon_w, dungeon_h = len(dungeon.tiles[0]), len(dungeon.tiles)

    if not 0 <= start_pos[0] < dungeon_w or not 0 <= start_pos[1] < dungeon_h or dungeon[start_pos[0], start_pos[1]].typ == TileType.WALL:
        return set()

    reachable: set[tuple[int, int]] = {start_pos}
    seen: set[tuple[int, int]] = {start_pos}
    to_check: deque[tuple[int, int]] = deque([start_pos])

    while to_check:
        cx, cy = to_check.popleft()
        current_vacant = dungeon[cx, cy].typ != TileType.WALL

        neighbours: list[tuple[int, int]] = []
        for dx, dy in _DIRS:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < dungeon_w and 0 <= ny < dungeon_h and (nx, ny) not in seen and dungeon[nx, ny].typ != TileType.WALL:
                neighbours.append((nx, ny))
                if current_vacant:
                    reachable.add((nx, ny))

        for n in neighbours:
            to_check.append(n)
            seen.add(n)

    return reachable


def _make_dungeon(width: int, height: int) -> Dungeon:
    dungeon = Dungeon(width, height)
    dungeon_area = width * height
    dungeon_centre_x, dungeon_centre_y = width // 2, height // 2
    room_spawn_radius_sq = min(width // 2, height // 2) ** 2 - max(ROOM_W_MAX, ROOM_H_MAX)

    num_room_spawn_attempts = int(dungeon_area * ROOM_SPAWN_COEFF)

    # Plan the rooms
    rooms: list[_Room] = []  # (left, top, width, height)

    for _ in range(num_room_spawn_attempts):
        for _ in range(MAX_RETRIES):
            # Select some random coordinates for the centre of the room
            # Then choose a width and height
            r_width, r_height = random.randint(ROOM_W_MIN, ROOM_W_MAX), random.randint(ROOM_H_MIN, ROOM_H_MAX)

            # Keep rolling a centre until it is inside the bounding circle
            while True:
                centre_x, centre_y = random.randint(r_width, width - 1 - r_width), random.randint(r_height, height - 1 - r_height)
                if (centre_x - dungeon_centre_x) ** 2 + (centre_y - dungeon_centre_y) ** 2 <= room_spawn_radius_sq:
                    break

            # Calculate left and top, and clamp
            r_left, r_top = max(0, centre_x - r_width), max(0, centre_y - r_height)
            r_width, r_height = min(width - r_left, 2 * r_width + 1), min(height - r_top, 2 * r_height + 1)

            room = _Room(r_left, r_top, r_width, r_height)
            if not any(room.touches(r) for r in rooms):
                rooms.append(room)
                break

    # Carve the rooms
    for room in rooms:
        for x in range(room.left, room.left + room.width):
            for y in range(room.top, room.top + room.height):
                dungeon[x, y].typ = TileType.EMPTY

    # For each room, carve a hallway leading from it to the closest other rooms
    # If the vertical positions are similar enough, draw a horizontal line from the first room to the other
    # If the horizontal positions are similar enough, draw a vertical line
    # Otherwise, draw an L-shape

    for room in rooms:
        by_closest = sorted(
            (r for r in rooms if r is not room),
            key=lambda r: (
                (r.centre_x - room.centre_x) ** 2
                + (r.centre_y - room.centre_y) ** 2
            )
        )

        # Draw hallways to the few closest rooms
        for closest in by_closest[:3]:
            if (
                room.bottom - closest.top >= 2 * HALLWAY_W
                and closest.bottom - room.top >= 2 * HALLWAY_W
            ):
                if closest.top >= room.top and closest.bottom <= room.bottom:
                    y = closest.centre_y
                elif room.top >= closest.top and room.bottom <= closest.bottom:
                    y = room.centre_y
                elif closest.centre_y < room.centre_y:
                    y = random.randint(room.top + 1, closest.bottom - 1)
                else:
                    y = random.randint(closest.top + 1, room.bottom - 1)

                for x in range(room.centre_x, closest.centre_x):
                    dungeon[x, y].typ = TileType.EMPTY
            elif (
                room.right - closest.left >= 2 * HALLWAY_W
                and closest.right - room.left >= 2 * HALLWAY_W
            ):
                if closest.left >= room.left and closest.right <= room.right:
                    x = closest.centre_x
                elif room.left >= closest.left and room.right <= closest.right:
                    x = room.centre_x
                elif closest.centre_x < room.centre_x:
                    x = random.randint(room.left + 1, closest.right - 1)
                else:
                    x = random.randint(closest.left + 1, room.right - 1)

                for y in range(room.centre_y, closest.centre_y):
                    dungeon[x, y].typ = TileType.EMPTY
            elif (
                (closest.top - room.bottom >= 2 or room.top - closest.bottom >= 2)
                and (closest.left - room.right >= 2 or room.left - closest.right >= 2)
            ):
                y_dir = 1 if closest.centre_y > room.centre_y else -1
                for y in range(room.centre_y, closest.centre_y + y_dir, y_dir):
                    dungeon[room.centre_x, y].typ = TileType.EMPTY
                x_dir = 1 if closest.centre_x > room.centre_x else -1
                for x in range(room.centre_x, closest.centre_x + x_dir, x_dir):
                    dungeon[x, closest.centre_y].typ = TileType.EMPTY

    # Make doors in the rooms
    for room in rooms:
        # Upper and lower edge
        for y, facing in ((room.top - 1, Facing.NORTH), (room.top + room.height, Facing.SOUTH)):
            if 0 <= y < height:
                # Generate doors
                chain: list[tuple[int, int]] = []
                for x in range(room.left, room.left + room.width):
                    if dungeon[y][x].typ == TileType.EMPTY:
                        chain.append((x, y))
                    else:
                        if len(chain) == 1:
                            dungeon[chain[0]].typ = TileType.DOOR_CLOSED
                            dungeon[chain[0]].flipped = chance(0.5)
                            dungeon[chain[0]].facing = facing

                        elif len(chain) == 2:
                            dungeon[chain[0]].typ = TileType.DOOR_CLOSED
                            dungeon[chain[0]].flipped = True
                            dungeon[chain[0]].facing = facing

                            dungeon[chain[1]].typ = TileType.DOOR_CLOSED
                            dungeon[chain[1]].facing = facing

                        chain.clear()

        # Left and right edge
        for x, facing in ((room.left - 1, Facing.WEST), (room.left + room.width, Facing.EAST)):
            if 0 <= x < width:
                # Generate doors
                chain: list[tuple[int, int]] = []
                for y in range(room.top, room.top + room.height):
                    if dungeon[y][x].typ == TileType.EMPTY:
                        chain.append((x, y))
                    else:
                        if len(chain) == 1:
                            dungeon[chain[0]].typ = TileType.DOOR_CLOSED
                            dungeon[chain[0]].flipped = chance(0.5)
                            dungeon[chain[0]].facing = facing

                        elif len(chain) == 2:
                            dungeon[chain[0]].typ = TileType.DOOR_CLOSED
                            dungeon[chain[0]].flipped = True
                            dungeon[chain[0]].facing = facing

                            dungeon[chain[1]].typ = TileType.DOOR_CLOSED
                            dungeon[chain[1]].facing = facing

                        chain.clear()

    # Find the empty space that has the most unbroken area, and use that
    # Then cull all other tiles that are disconnected from said area

    scouts: deque[tuple[int, int]] = deque(r.centre for r in rooms)
    fills: list[set[tuple[int, int]]] = []

    while scouts:
        scout = scouts.popleft()

        # if the scout is already covered, move on
        # run flood fill to find all reachable spaces from the initial scout point

        if not any(scout in fill for fill in fills):
            reachable = _get_reachable_points(dungeon, scout)
            fills.append(reachable)

    # Pick the largest fill and copy its area onto the dungeon
    # This is to cull unreachable areas
    fills.sort(key=len, reverse=True)
    chosen_fill = fills[0]

    final_dungeon = Dungeon(width, height)

    for y in range(height):
        for x in range(width):
            if (x, y) in chosen_fill:
                final_dungeon[x, y] = dungeon[x, y]

    # Get all the rooms that are still there after cutting off unreachable areas
    rooms = [r for r in rooms if (r.left, r.top) in chosen_fill]

    # Add a row of solid tiles on each side so that the dungeon is sealed off
    for row in final_dungeon:
        row.insert(0, Tile(typ=TileType.WALL))
        row.append(Tile(typ=TileType.WALL))
    final_dungeon.tiles.insert(0, [Tile(typ=TileType.WALL) for _ in range(final_dungeon.width)])
    final_dungeon.tiles.append([Tile(typ=TileType.WALL) for _ in range(final_dungeon.width)])

    # Adjust room coordinates to account for padding
    for room in rooms:
        room.left += 1
        room.top += 1

    # Pick a random room and one of its four corners to be the entrance
    entrance_room = random.choice(rooms)
    entrance_x, entrance_flipped = random.choice(((entrance_room.left, False), (entrance_room.right, True)))
    entrance_z = random.choice((entrance_room.top, entrance_room.bottom))
    final_dungeon[entrance_x, entrance_z].typ = TileType.ENTRANCE
    final_dungeon[entrance_x, entrance_z].flipped = entrance_flipped

    return final_dungeon


def generate_dungeon() -> Dungeon:
    """Make a dungeon, enforcing `MIN_AREA_COEFF`"""

    min_area = DUNGEON_GEN_W * DUNGEON_GEN_H * MIN_AREA_COEFF

    for _ in range(MAX_RETRIES):
        test_dungeon = _make_dungeon(DUNGEON_GEN_W, DUNGEON_GEN_H)

        non_wall = sum(
            1 for x in range(DUNGEON_GEN_W)
            for y in range(DUNGEON_GEN_H)
            if test_dungeon[x, y].typ != TileType.WALL
        )

        if non_wall >= min_area:
            break

    return test_dungeon  # type: ignore
