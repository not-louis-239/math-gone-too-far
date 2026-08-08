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
import math
from functools import lru_cache

import pygame as pg

from mgtf.core.custom_types import Colour


@lru_cache(maxsize=1024)
def crop_text_to_fit(font: pg.font.Font, text: str, max_width: int) -> str:
    if font.size(text)[0] <= max_width:
        return text

    ellipsis_char = "…"

    if font.size(ellipsis_char)[0] > max_width:
        return ""

    known_good = ""

    for char in text:
        candidate = known_good + char + ellipsis_char
        if font.size(candidate)[0] >= max_width:
            return known_good + ellipsis_char
        known_good += char

    return known_good


@lru_cache(maxsize=1024)
def _get_text_surf(font: pg.font.Font, text: str, colour: Colour) -> pg.Surface:
    return font.render(text, True, colour)

def get_text_surf(font: pg.font.Font, text: str, colour: Colour) -> pg.Surface:
    # This is a typed wrapper because using `@lru_cache` directly breaks type hinting
    return _get_text_surf(font, text, colour)


@lru_cache(maxsize=128)
def get_reduced_alpha_tile(surface: pg.Surface):
    surface_copy = surface.copy()
    surface_copy.set_alpha(128)
    return surface_copy


def get_blackened_tile(surface: pg.Surface, factor: float) -> pg.Surface:
    black_surface = pg.Surface(surface.get_size(), pg.SRCALPHA)
    black_surface.fill((0, 0, 0))
    black_surface.set_alpha(int(factor * 255))
    surface_copy = surface.copy()
    surface_copy.blit(black_surface)
    return surface_copy


def lerp_colours(c1: Colour, c2: Colour, t: float) -> Colour:
    return (
        int(c1[0] * (1 - t) + c2[0] * t),
        int(c1[1] * (1 - t) + c2[1] * t),
        int(c1[2] * (1 - t) + c2[2] * t)
    )


def clamp(val: float, lower: float, upper: float) -> float:
    return max(lower, min(val, upper))


def chance(p: float) -> bool:
    return random.random() < p


# TODO: use this for deciding how many item stands to put in a floor,
# e.g. 2.5 = 50% chance of 2, 50% chance of 3
def collapse(val: float) -> int:
    """Stochastically collapse a `float` down to an `int` based
    on its decimal portion."""
    val_down = math.floor(val)
    round_up_chance = val - val_down
    return val_down + chance(round_up_chance)


def _test():
    collapsed_values = [collapse(3.14159) for _ in range(20)]
    print(f"Collapsed values for test value collapse(3.14159): {", ".join(str(v) for v in collapsed_values)}")
    print("You should see mostly 3s with a couple 4s.")


if __name__ == "__main__":
    _test()
