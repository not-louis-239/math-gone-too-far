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


GLITCH_CHARS = "!@#$%&?£¢§Ø"


class GlitchyString(str):
    def __init__(self, value: str) -> None:
        self._true_value = value

    def __repr__(self) -> str:
        return f"GlitchyString({self._true_value!r})"

    def __str__(self) -> str:
        return "".join(random.choice(GLITCH_CHARS) for _ in self._true_value)


def _test():
    import time

    gs = GlitchyString('Error')
    print(f"Repr: {gs!r}")

    for _ in range(200):  # 2 seconds simulated
        print(f"\rStr:  {gs}", end='')
        time.sleep(0.01)

    print()


if __name__ == "__main__":
    _test()
