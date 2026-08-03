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


from enum import IntEnum

import pygame as pg


class Controls(IntEnum):
    MOVE_BACK = pg.K_w
    MOVE_FWD = pg.K_s
    MOVE_LEFT = pg.K_a
    MOVE_RIGHT = pg.K_d

    INVENTORY = pg.K_e
    GENERIC_ESCAPE = pg.K_ESCAPE

    CONFIRM = pg.K_z
    BACK = pg.K_x

    DEBUG_TOGGLE = pg.K_F10
