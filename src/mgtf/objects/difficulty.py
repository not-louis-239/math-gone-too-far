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

from dataclasses import dataclass
from functools import total_ordering
from enum import StrEnum


class DifficultyID(StrEnum):
    # must match the keys in `assets/lore/difficulties.json`

    APPLICATIONS = "applications"
    METHODS = "methods"
    SPECIALIST = "specialist"
    VALUE_ERROR = "value_error"


@dataclass
@total_ordering
class Difficulty:
    # Name and ranking
    rank: int
    display_name: str

    # Enemy stats
    enemy_health_mult: float
    enemy_contact_damage_mult: float
    enemy_projectile_damage_mult: float
    enemy_knockback_resistance_mult: float
    enemy_aggro_radius_mult: float
    enemy_coin_drops_mult: float

    # Debuffs
    debuff_chance_mult: float
    debuff_duration_mult: float

    # Bogeytan
    bogey_spawn_delay_secs: int
    bogey_speed_mult: float
    bogey_destroy_walls_per_sec: float
    bogey_damage_to_enemies: int

    # Light mechanics
    light_decay_per_sec: float
    max_light_radius: float

    # Combat
    defence_effectiveness_mult: float
    enemy_spawn_rate_mult: float

    # Dungeon generation
    item_stands_per_floor_min: float
    item_stands_per_floor_max: float
    door_spawn_probability: float
    jar_frequency_mult: float

    # Loot luck and rarities
    loot_luck_modifier: float
    jar_loot_tier_modifier: int

    def __gt__(self, other: Difficulty):
        return self.rank > other.rank
