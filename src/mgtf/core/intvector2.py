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


class IntVector2:
    """Vector class for storing discrete entity positions."""

    __slots__ = ('x', 'y')

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def __add__(self, other: IntVector2):
        return IntVector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: IntVector2):
        return IntVector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int):
        return IntVector2(self.x * scalar, self.y * scalar)
