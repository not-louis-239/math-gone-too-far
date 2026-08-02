#!/usr/bin/env python3

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


import sys
import time
from pathlib import Path

import pygame as pg

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from mgtf.core.constants import WN_W, WN_H, FPS
from mgtf.game.game import Game


def _run():
    game = Game()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WN_W, WN_H), pg.DOUBLEBUF)
    pg.display.set_caption("Math Gone Too Far")

    running = True
    while running:
        dt_s = clock.tick(FPS) / 1_000.0
        keys = pg.key.get_pressed()
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                running = False

        t_i = time.perf_counter()
        game.update(dt_s)
        t_update = time.perf_counter()
        game.take_input(keys, events, dt_s)
        t_input = time.perf_counter()
        game.draw(screen)
        t_draw = time.perf_counter()

        game.diagnostics.snapshot_container.record(t_i, t_update, t_input, t_draw)
        game.diagnostics.snapshot_container.prune()

        if game.diagnostics.enabled:
            game.diagnostics.draw_fps_diagnostic(screen)
            game.diagnostics.draw_debug_mouse_pointer(screen)

        pg.display.flip()


def main():
    pg.init()

    try:
        _run()
    except KeyboardInterrupt:
        pass

    pg.quit()

if __name__ == "__main__":
    main()
