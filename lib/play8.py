# Play8

# Play
# Play8 9
# Written by Athos Toniolo

import os.path
import pygame
import pygame.image


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


# screen64 screen
def screen64_screen(fore):
    """Return RGB triplet of foreground or background"""
    if fore:
        return 108, 94, 181
    return 53, 40, 121


# screen64 font
def screen64_font(path, bank):
    # FIXME the font should be configurable
    filename = f"bank_{bank}.p8.png"
    image_font = pygame.image.load(os.path.join(path, "res", filename))
    return image_font.convert()


# screen64 make
def screen64_make(font, rows):
    i = len(rows[0])
    t = SCALE_FACTOR * i, SCALE_FACTOR * len(rows)
    s = pygame.Surface(t)
    i = 0
    for x in rows:
        t = 0, i
        screen64_printrow(font, x, s, t)
        i += 1
    return s


# screen64 view
def screen64_view(internal_resolution, back=None):
    x, y = internal_resolution
    origin = 0, 0
    actual_resolution = SCALE_FACTOR * x, SCALE_FACTOR * y
    if back:
        return back.subsurface(pygame.Rect(origin, actual_resolution))
    pygame.display.set_mode(actual_resolution)
    return pygame.display.get_surface()


# screen64 printall
def screen64_printall(font, rows, dest, spos):
    """Display the given `rows` at `spos`.

    :param font:
    :param rows: the lines to draw
    :param dest: the surface on which to draw
    :param spos: a pair denoting the coordinates (x, y) at which to draw
    :returns: `(x, y + len(rows))`
    """
    x, y = spos
    for row in rows:
        screen64_printrow(font, row, dest, (x, y))
        y += 1
    return x, y


# screen64 printrow
def screen64_printrow(font, line, dest, spos):
    """Display the given `line` at `spos`.

    :param font:
    :param line: the line to draw
    :param dest: the surface on which to draw
    :param spos: a pair denoting the coordinates (x, y) at which to draw
    :returns: `(x + len(line), y)`
    """
    x, y = spos
    for item in line:
        actual_coords = SCALE_FACTOR * x, SCALE_FACTOR * y
        r = pygame.Rect(SCALE_FACTOR * item, 0, SCALE_FACTOR, SCALE_FACTOR)
        dest.blit(font, actual_coords, r)
        x += 1
    return x, y


# screen64 progress
def screen64_progress(font, rvrs, progress, line, dest, spos):
    """Display a font-based progress bar.

    :param font:
    :param rvrs: the "reversed" font for the filled part of the bar
    :param progress: the progress rate (min. 0, max. 1)
    :type progress: float
    :param line: the line to draw
    :param dest: the surface on which to draw
    :param spos: a pair denoting the coordinates (x, y) at which to draw
    """
    # FIXME there are no checks on the progress
    i = int(progress * len(line))
    r = screen64_printrow(rvrs, line[:i], dest, spos)
    screen64_printrow(font, line[i:], dest, r)
