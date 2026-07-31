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


import pygame as pg
from pygame import Rect, Surface

from .widget import Widget
from .alignment_enums import HAlign, VAlign


class _Box(Widget):
    def __init__(self, children: list[Widget], gap: int = 0) -> None:
        self.children = children
        self.gap = gap

    def draw(self, surface: Surface) -> None:
        for child in self.children:
            child.draw(surface)

class HBox(_Box):
    def preferred_size(self) -> tuple[int, int]:
        total_w, max_h = 0, 0
        for child in self.children:
            child_w, child_h = child.preferred_size()
            max_h = max(max_h, child_h)
            total_w += child_w

        gaps = max(0, len(self.children) - 1)
        total_w += gaps * self.gap

        return (total_w, max_h)

    def layout(self, rect: pg.Rect) -> None:
        self.rect = rect

        fixed_width = 0
        flex_children: list[Widget] = []

        for child in self.children:
            if child.flex:
                flex_children.append(child)
                continue

            w, _ = child.preferred_size()
            fixed_width += w

        gap_w = self.gap * max(0, len(self.children) - 1)
        remaining = max(0, rect.width - fixed_width - gap_w)

        total_flex = sum(child.flex for child in self.children)
        flex_widths: dict[Widget, int] = {}

        if total_flex:
            for child in flex_children:
                flex_widths[child] = int(remaining * (child.flex / total_flex))

        x = rect.left
        y = rect.top
        h = rect.height

        for child in self.children:
            w, _ = child.preferred_size()
            if child in flex_widths:
                w = flex_widths[child]

            child.layout(pg.Rect(x, y, w, h))
            x += w + self.gap


class VBox(_Box):
    def preferred_size(self) -> tuple[int, int]:
        max_w, total_h = 0, 0
        for child in self.children:
            child_w, child_h = child.preferred_size()
            max_w = max(max_w, child_w)
            total_h += child_h

        gaps = max(0, len(self.children) - 1)
        total_h += gaps * self.gap

        return (max_w, total_h)

    def layout(self, rect: Rect) -> None:
        self.rect = rect

        fixed_height = 0
        flex_children: list[Widget] = []

        for child in self.children:
            if child.flex:
                flex_children.append(child)
                continue

            _, h = child.preferred_size()
            fixed_height += h

        gap_h = self.gap * max(0, len(self.children) - 1)
        remaining = max(0, rect.height - fixed_height - gap_h)

        total_flex = sum(child.flex for child in self.children)
        flex_heights: dict[Widget, int] = {}

        if total_flex:
            for child in flex_children:
                flex_heights[child] = int(remaining * (child.flex / total_flex))

        x = rect.left
        y = rect.top
        w = rect.width

        for child in self.children:
            _, h = child.preferred_size()
            if child in flex_heights:
                h = flex_heights[child]

            child.layout(pg.Rect(x, y, w, h))
            y += h + self.gap

class SBox(_Box):
    def __init__(
            self, child: Widget, *,
            forced_width: int | None = None, forced_height: int | None = None,
            h_align: HAlign = HAlign.CENTRE,
            v_align: VAlign = VAlign.CENTRE
        ) -> None:
        super().__init__(children=[child])
        self.child = child

        self.forced_width = forced_width
        self.forced_height = forced_height
        self.h_align = h_align
        self.v_align = v_align

    def preferred_size(self) -> tuple[int, int]:
        child_w, child_h = self.child.preferred_size()
        w = self.forced_width if self.forced_width is not None else child_w
        h = self.forced_height if self.forced_height is not None else child_h
        return (w, h)

    def layout(self, rect: pg.Rect) -> None:
        child_w, child_h = self.child.preferred_size()
        child_rect = pg.Rect(0, 0, min(child_w, rect.width), min(child_h, rect.height))

        match self.h_align:
            case HAlign.LEFT:
                child_rect.left = rect.left
            case HAlign.CENTRE:
                child_rect.centerx = rect.centerx
            case HAlign.RIGHT:
                child_rect.right = rect.right

        match self.v_align:
            case VAlign.TOP:
                child_rect.top = rect.top
            case VAlign.CENTRE:
                child_rect.centery = rect.centery
            case VAlign.BOTTOM:
                child_rect.bottom = rect.bottom

        self.rect = rect
        self.child.layout(child_rect)

    def draw(self, surface: pg.Surface) -> None:
        self.child.draw(surface=surface)
