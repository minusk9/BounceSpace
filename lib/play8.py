# Play8

# Play
# Play8 9
# Written by Athos Toniolo

from __future__ import annotations

from enum import Enum
import os
from pathlib import Path
from typing import Any, Iterable, NewType, Optional, Union

import pygame
import pygame.image


AnyPath = Union[str, os.PathLike]
Font = NewType('Font', pygame.Surface)


# FIXME BITS requires this to be 16, any other value breaks the graphics
SCALE_FACTOR = 16


def bytes_shape(line, size):
    """???"""
    lst = list()
    for x in range(0, len(line), size):
        i = x + size
        lst.append(line[x:i])
    return lst


def config_parse(config):
    # FIXME this should not be passed as string, but read from a file
    config_items = (item for item in config.split(";") if item)
    mapping = {}
    for item in config_items:
        tokens = item.split(':', 1)
        try:
            key, value = tokens
        except ValueError:
            key = tokens[0]
            value = ""
        mapping.setdefault(key, value)
    return mapping


class Color:
    __slots__ = ['_r', '_g', '_b']

    def __init__(self, r: int, g: int, b: int) -> None:
        if not all(0 <= x <= 255 for x in (r, g, b)):
            raise ValueError("RGB triplet values must be between 0 and 255")
        self._r = r
        self._g = g
        self._b = b

    @property
    def r(self) -> int:
        return self._r

    @property
    def g(self) -> int:
        return self._g

    @property
    def b(self) -> int:
        return self._b

    def as_tuple(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)


class C64:
    class Colors(Enum):
        FOREGROUND = Color(108, 94, 181)
        BACKGROUND = Color(53, 40, 121)

        def as_tuple(self):
            return self.value.as_tuple()

    @classmethod
    def load_font(cls, font_path: AnyPath, bank: int) -> Font:
        """Load a font from the resource directory `font_path`."""
        filename = f"bank_{bank}.p8.png"
        font = pygame.image.load(Path(font_path) / "res" / filename)
        return Font(font.convert())

    @classmethod
    def render_rows(cls, font: Font, rows: Iterable[Any]) -> pygame.Surface:
        actual_size = SCALE_FACTOR * len(rows[0]), SCALE_FACTOR * len(rows)
        surface = pygame.Surface(actual_size)
        for i, row in enumerate(rows):
            coords = 0, i
            cls.render_row_to_surface(font, row, surface, coords)
        return surface

    # screen64 view
    @classmethod
    def render_screen(
        cls,
        internal_resolution: tuple[int, int],
        background: Optional[pygame.Surface] = None,
    ):
        x, y = internal_resolution
        origin = 0, 0
        actual_resolution = SCALE_FACTOR * x, SCALE_FACTOR * y
        if background:
            return background.subsurface(
                pygame.Rect(origin, actual_resolution)
            )
        pygame.display.set_mode(actual_resolution)
        return pygame.display.get_surface()

    # screen64 printall
    @classmethod
    def render_rows_to_surface(
        cls,
        font: Font,
        rows: Iterable[Iterable[Any]],
        surface: pygame.Surface,
        coords: tuple[int, int],
    ):
        """Display the given `rows` at `coords`.

        :param font:
        :param rows: the lines to draw
        :param surface: the surface on which to draw
        :param coords: a pair denoting the coordinates (x, y) at which to draw
        :returns: `(x, y + len(rows))`
        """
        x, y = coords
        for row in rows:
            cls.render_row_to_surface(font, row, surface, (x, y))
            y += 1
        return x, y

    # screen64 printrow
    @classmethod
    def render_row_to_surface(
        cls,
        font: Font,
        line: Iterable[Any],
        surface: pygame.Surface,
        coords: tuple[int, int],
    ):
        """display the given `line` at `spos`.

        :param font:
        :param line: the line to draw
        :param surface: the surface on which to draw
        :param coords: a pair denoting the coordinates (x, y) at which to draw
        :returns: `(x + len(line), y)`
        """
        x, y = coords
        for item in line:
            actual_coords = SCALE_FACTOR * x, SCALE_FACTOR * y
            r = pygame.Rect(SCALE_FACTOR * item, 0, SCALE_FACTOR, SCALE_FACTOR)
            surface.blit(font, actual_coords, r)
            x += 1
        return x, y

    # screen64 progress
    @classmethod
    def render_progress_bar(
        cls,
        font: Font,
        reversed_font: Font,
        progress: float,
        line: Iterable[Any],
        surface: pygame.Surface,
        coords: tuple[int, int],
    ):
        """Display a font-based progress bar.

        :param font:
        :param reversed_font: the "reversed" font for the filled part of
          the bar
        :param progress: the progress rate (min. 0, max. 1)
        :param line: the line to draw
        :param surface: the surface on which to draw
        :param coords: a pair denoting the coordinates (x, y) at which
          to draw
        """
        filled_chars = int(progress * len(line))
        fill_end_coords = C64.render_row_to_surface(
            reversed_font, line[:filled_chars], surface, coords
        )
        C64.render_row_to_surface(
            font, line[filled_chars:], surface, fill_end_coords
        )
