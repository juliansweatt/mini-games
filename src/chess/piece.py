# -*- coding: utf-8 -*-

from color import Color
from enum import Enum, unique
from typing import Optional

@unique
class PieceType(Enum):
    """ A piece type that can be either blank or on of the set containing pawn,
        knight, bishop, rook, queen, or king

        >>> from piece import PieceType
        >>> list(pt.char for pt in PieceType)
        ['p', 'n', 'b', 'r', 'q', 'k']
        >>> list(str(pt) for pt in PieceType)
        ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        >>> assert PieceType("p") == PieceType.pawn

    """
    pawn = "p"
    knight = "n"
    bishop = "b"
    rook = "r"
    queen = "q"
    king = "k"

    def __str__(self):
        return self.name

    def __repr__(self):
        return "PieceType.{}".format(self.name)

    @property
    def char(self):
        return self.value

class Piece():
    """ A chess piece that has a PieceType and a Color
    """

    def __init__(self, pt: PieceType, c: Color) -> None:
        self.type = pt
        self.color = c

    def __str__(self) -> str:
        char = self.type.char
        return char if self.color else char.upper()

    def __repr__(self):
        return "Piece.{}".format(self.__str__())

    @classmethod
    def from_char(cls, char):
        lower = char.lower()
        pt = PieceType(lower)
        color = Color(char == lower)
        return cls(pt, color)
