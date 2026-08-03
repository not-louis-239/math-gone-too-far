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


import time
import math
from dataclasses import dataclass

import pygame as pg

import mgtf.core.colours as cols
from mgtf.core.asset_manager import Assets
from mgtf.core.constants import WN_H, WN_W
from mgtf.core.utils import get_text_surf, lerp_colours


GRAPH_HEIGHT_PER_S = 5000

FPS_LINES = [30, 60]
MAX_HISTORY_LEN = 200

_BAR_WIDTH = WN_W / MAX_HISTORY_LEN
_MAX_GRAPH_H = GRAPH_HEIGHT_PER_S * 1 / FPS_LINES[0]

COL_UPDATE = (127, 255, 255)
COL_INPUT = (127, 127, 255)

COL_ERR = (255, 110, 110)
COL_WARN = (255, 255, 110)
COL_OK = (110, 255, 110)


@dataclass(frozen=True, kw_only=True)
class Interval:
    t_i: float
    t_f: float

    @property
    def duration(self) -> float:
        return self.t_f - self.t_i


@dataclass(frozen=True)
class Snapshot:
    intervals: list[Interval]

    def total_duration(self) -> float:
        return sum(i.duration for i in self.intervals)


class SnapshotContainer:
    def __init__(self) -> None:
        self.snapshots: list[Snapshot] = []

    def record(self, *times: float) -> None:
        if len(times) < 2:
            raise ValueError("must provide at least two times")
        self.snapshots.append(Snapshot([Interval(t_i=times[idx], t_f=times[idx + 1]) for idx in range(len(times) - 1)]))

    def prune(self, max_len: int = MAX_HISTORY_LEN) -> None:
        self.snapshots = self.snapshots[-max_len:]

    def avg_interval_frequency(self) -> float:
        """Returns the average frequency of intervals since the
        first interval in `self.intervals`."""
        t_first = self.snapshots[0].intervals[0].t_i
        now = time.perf_counter()
        return len(self.snapshots) / (now - t_first)


class Diagnostics:
    def __init__(self, assets: Assets) -> None:
        self.enabled = False
        self.snapshot_container = SnapshotContainer()
        self.fps_graph_font = pg.font.Font(assets.fonts.base_font_path, 25)
        self.mouse_pos_display_font = pg.font.Font(assets.fonts.base_font_path, 20)

        self.fps_graph_bg_surface = pg.Surface((WN_W, _MAX_GRAPH_H), pg.SRCALPHA)
        self.fps_graph_bg_surface.fill((0, 0, 0, 120))

    def toggle_visibility(self) -> None:
        self.enabled = not self.enabled
        pg.mouse.set_visible(not self.enabled)

    def _draw_fps_graph(self, surface: pg.Surface) -> None:
        for i, snapshot in enumerate(self.snapshot_container.snapshots):
            # Get durations first
            total_duration = sum(interval.duration for interval in snapshot.intervals)

            if total_duration > 0.05:
                col_draw = COL_ERR
            elif total_duration > 0.025:
                col_draw = lerp_colours(COL_WARN, COL_ERR, (total_duration - 0.025) / 0.025)
            else:
                col_draw = lerp_colours(COL_OK, COL_WARN, total_duration / 0.025)

            colours = (COL_UPDATE, COL_INPUT, col_draw)

            bar_y = WN_H
            for interval, colour in zip(snapshot.intervals, colours):
                bar_h = math.ceil(GRAPH_HEIGHT_PER_S * interval.duration)
                bar_y -= bar_h
                rect = pg.Rect(math.ceil(i * _BAR_WIDTH), bar_y, math.ceil(_BAR_WIDTH), bar_h)
                pg.draw.rect(surface, colour, rect)


        all_durs = [snapshot.total_duration() for snapshot in self.snapshot_container.snapshots]

        # minimum
        min_dur = min(all_durs, default=0.0)
        text_surf = get_text_surf(self.fps_graph_font, f"{min_dur * 1000:.2f} ms min", cols.FG)
        surface.blit(text_surf, text_surf.get_rect(centerx=WN_W // 2 - 240, top=WN_H - _MAX_GRAPH_H + 10))

        # average
        avg_dur = sum(all_durs) / len(all_durs) if all_durs else 0.0
        text_surf = get_text_surf(self.fps_graph_font, f"{avg_dur * 1000:.2f} ms avg", cols.FG)
        surface.blit(text_surf, text_surf.get_rect(centerx=WN_W // 2, top=WN_H - _MAX_GRAPH_H + 10))

        # maximum
        max_dur = max(all_durs, default=0.0)
        text_surf = get_text_surf(self.fps_graph_font, f"{max_dur * 1000:.2f} ms max", cols.FG)
        surface.blit(text_surf, text_surf.get_rect(centerx=WN_W // 2 + 240, top=WN_H - _MAX_GRAPH_H + 10))

    def _draw_fps_lines(self, surface: pg.Surface) -> None:
        for fps_count in FPS_LINES:
            line_h = WN_H - GRAPH_HEIGHT_PER_S / fps_count
            pg.draw.line(surface, cols.DIAG_FG, (0, line_h), (WN_W, line_h))

            label = f"{fps_count} fps"
            label_surf = self.fps_graph_font.render(label, True, cols.DIAG_FG)
            surface.blit(label_surf, (0, line_h))

    def draw_fps_diagnostic(self, surface: pg.Surface) -> None:
        surface.blit(self.fps_graph_bg_surface, (0, WN_H - _MAX_GRAPH_H))

        self._draw_fps_graph(surface)
        self._draw_fps_lines(surface)

    def draw_debug_mouse_pointer(self, wn: pg.Surface) -> None:
        mx, my = pg.mouse.get_pos()

        # Draw mouse cross
        cross_size = 8
        cross_colour = cols.DIAG_FG
        pg.draw.line(
            wn, cross_colour,
            (mx - cross_size, my),
            (mx + cross_size, my), 3
        )
        pg.draw.line(
            wn, cross_colour,
            (mx, my - cross_size),
            (mx, my + cross_size), 3
        )

        pg.draw.line(wn, cross_colour, (WN_W // 2, 0), (WN_W // 2, WN_H), 1)
        pg.draw.line(wn, cross_colour, (0, WN_H // 2), (WN_W, WN_H // 2), 1)

        # Show label (auto-align to stay onscreen)
        label = f"{mx}, {my}"
        offset = 10

        label_surf = self.mouse_pos_display_font.render(label, True, cols.DIAG_FG)
        text_w, text_h = label_surf.get_size()

        x = mx + offset
        y = my + offset

        if mx + offset + text_w > WN_W:
            x = mx - offset - text_w
        if my + offset + text_h > WN_H:
            y = my - offset - text_h

        wn.blit(label_surf, (x, y))
