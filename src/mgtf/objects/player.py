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


from pygame import Surface
from dataclasses import dataclass

from mgtf.objects.entity import Entity, Facing, Hitbox
from mgtf.lore.difficulty import DifficultyID


PLAYER_HITBOX = Hitbox(38 / 48, 48 / 48, 38 / 48)


@dataclass
class PlayerData:
    difficulty: DifficultyID = DifficultyID.APPLICATIONS
    light_radius: float = 0
    max_light_radius: float = 0
    distance_travelled: float = 0
    num_wrongs: int = 0

    hp: int = 0
    max_hp: int = 0
    floor: int = 1


class Player(Entity):
    def __init__(self, pos: tuple[int, int, int], images: dict[Facing, Surface], hitbox: Hitbox) -> None:
        super().__init__(pos, images, hitbox)
        self.speed = 5
        self.data = PlayerData()

    def reset(self) -> None:
        pass
