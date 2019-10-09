# -*- coding: utf-8 -*-

from enum import IntEnum, unique

@unique
class Color(IntEnum):
    """ A color type; used for Piece and Square

        >>> from color import Color
        >>> list(Color)
        [Color.light, Color.dark]
        >>> list(bool(c) for c in Color)
        [False, True]
        >>> list(str(c) for c in Color)
        ['light', 'dark']
        >>> list(int(c) for c in Color)
        [0, 1]

    """
    light = 0
    dark = 1

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Color.{}".format(self.name)

