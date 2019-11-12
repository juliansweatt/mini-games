# -*- coding: utf-8 -*-

""" python3 chess game and engine

Using bitboards, this chess implementation maintains the state of a chess game for all of the
pieces. The game state, such as castling rights; en passant; etc, is also used to create a playable
game. The :class:`BaseBoard` stores all bitboards as .The chess engine is (will be) capable of using
a `Game`

For desigining this game, `chessprogramming.org <https://www.chessprogramming.org/Main_Page>`_ has
been very helpful
"""

import enum
import functools
import operator
import struct

from typing import Optional, Tuple

CH_0 = ord("0")

CH_a = ord("a")

FILE_NAMES = tuple(chr(i + CH_a) for i in range(8))

RANK_NAMES = tuple(chr(i + CH_0) for i in range(8, 0, -1))

@enum.unique
class Square(enum.IntFlag):
    (A8, B8, C8, D8, E8, F8, G8, H8,
     A7, B7, C7, D7, E7, F7, G7, H7,
     A6, B6, C6, D6, E6, F6, G6, H6,
     A5, B5, C5, D5, E5, F5, G5, H5,
     A4, B4, C4, D4, E4, F4, G4, H4,
     A3, B3, C3, D3, E3, F3, G3, H3,
     A2, B2, C2, D2, E2, F2, G2, H2,
     A1, B1, C1, D1, E1, F1, G1, H1,
    ) = ((i, 1 << i) for i in range(64))

    def __new__(cls, ind, mask):
        obj = enum.IntFlag.__new__(cls, mask)
        obj._value_ = mask
        obj.index = ind
        return obj

    @classmethod
    def from_index(cls, ind):
        return cls(1 << ind)


BitBoard = Square
BB_ALL = Square(-1)
BB_RANKS = BB_RANK_8, BB_RANK_7, BB_RANK_6, BB_RANK_5, BB_RANK_4, BB_RANK_3, BB_RANK_2, BB_RANK_1 = tuple(functools.reduce(operator.or_, (Square.from_index(i) for i in range(j * 8, 8 + j * 8))) for j in range(8))
BB_FILES = BB_FILE_A, BB_FILE_B, BB_FILE_C, BB_FILE_D, BB_FILE_E, BB_FILE_F, BB_FILE_G, BB_FILE_H = tuple(functools.reduce(operator.or_, (Square.from_index(i) for i in range(j, 64 + j * 8, 8))) for j in range(8))

# equal to BaseBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
STANDARD_BITBOARD = struct.pack(">9Q",
    BB_RANK_8 | BB_RANK_7 | BB_RANK_2 | BB_RANK_1,  # all
    BB_RANK_2 | BB_RANK_1,  # lights
    BB_RANK_8 | BB_RANK_7,  # darks
    BB_RANK_7 | BB_RANK_2,  # pawns
    Square.B8 | Square.G8 | Square.B1 | Square.G1,  # knights
    Square.C8 | Square.F8 | Square.C1 | Square.F1,  # bishops
    Square.A8 | Square.H8 | Square.A1 | Square.H1,  # rooks
    Square.D8 | Square.D1,  # queens
    Square.E8 | Square.E1,  # kings
)


COLOR_CHARS = {
    0: "w",
    1: "b",
}

CHAR_COLORS = {
    "w": 0,
    "b": 1,
}


@enum.unique
class Color(enum.IntEnum):
    """ Color: just light or dark
    """
    LIGHT = 0
    DARK = 1

    def __init__(self, val) -> None:
        self.char = COLOR_CHARS[val]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "Color.{}".format(self.name)

    @classmethod
    def from_char(cls, char):
        return cls(CHAR_COLORS[char])


# piece type char to int
PIECE_INTS = {
    "p": 1,
    "n": 2,
    "b": 3,
    "r": 4,
    "q": 5,
    "k": 6,
}

# int to piece type char
INT_PIECES = {
    1: "p",
    2: "n",
    3: "b",
    4: "r",
    5: "q",
    6: "k",
}


@enum.unique
class PieceType(enum.Enum):
    """ Type of a piece sans color
    """
    PAWN = "p"
    KNIGHT = "n"
    BISHOP = "b"
    ROOK = "r"
    QUEEN = "q"
    KING = "k"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "PieceType.{}".format(self.name)

    def __int__(self) -> int:
        return PIECE_INTS[self.value]

    def __bool__(self) -> bool:
        return bool(self.__int__())

    def __hash__(self) -> int:
        return self.__int__()

    @classmethod
    def from_int(cls, i):
        return cls(INT_PIECES[i])


class Piece():
    """ Piece with a Color and PieceType
    """
    __slots__ = "type", "color", "char"

    def __init__(self, color: Color, typ: PieceType):
        self.color = color
        self.type = typ
        if typ is None:
            self.char = " "
        else:
            self.char = typ.value if color else typ.value.upper()

    def __str__(self) -> str:
        return self.type.value if self.color else self.type.value.upper()

    def __repr__(self) -> str:
        return "Piece({!r}, {!r})".format(self.color, self.type)

    def __eq__(self, other) -> bool:
        return hasattr(other, "char") and self.char == other.char

    def __hash__(self) -> int:
        return int(self.type) + 6 * int(self.color)

    @classmethod
    def from_char(cls, c):
        """
        >>> from arcade.games.chess.chess import Piece, Color, PieceType
        >>> assert Piece(Color.LIGHT, PieceType.ROOK) == Piece.from_char("R")
        >>> assert Piece(Color.DARK, PieceType.QUEEN) == Piece.from_char("q")
        """
        l = c.lower()
        return cls(Color(l == c), PieceType(l))


class BaseBoard():
    """ BaseBoard that stores 9 bitboards (1 for all, 2 for each color, and 6 for all the pieces)
        and provides simple functionality for moving and getting pieces
    """
    # __slots__ = "bb_all", "bb_colors", "bb_pieces"

    def __init__(self, bb: Optional[str] = None) -> None:
        """ BaseBoard initializer

        :param bb: bitboard to initialize the board; if empty, set to standard
        """
        self.set_bitboards(bb if bb else STANDARD_BITBOARD)

    def __iter__(self):
        for sq in Square:
            yield self[sq]

    def __getitem__(self, sq: Square) -> Optional[Piece]:
        return self.get_piece_at(sq)

    def __setitem__(self, sq: Square, piece: Optional[Piece]) -> None:
        self.set_piece_at(sq, piece)

    def __str__(self):
        return self.get_san()

    def __repr__(self):
        return "BaseBoard.from_san({!r})".format(self.get_san())

    def empty(self) -> None:
        self.bb_all = 0
        self.bb_colors = [0, 0]
        self.bb_pieces = dict((pt, 0) for pt in PieceType)

    @classmethod
    def from_san(cls, san: str) -> None:
        baseb = cls()
        baseb.set_san(san)

    def set_san(self, san: str) -> None:
        self.empty()
        split_san = san.split("/")
        if len(split_san) != 8:
            raise ValueError("Invalid SAN: {!r}; expected 8 rows.".format(san))
        for rank_ind, row in enumerate(split_san):
            file_ind = 0
            for char in row:
                if char.isdigit():
                    if num_flag:
                        raise ValueError("Invalid SAN: {!r}; consecutive numbers.".format(san))
                    file_ind += ord(char) - CH_0
                    num_flag = True
                else:
                    num_flag = False
                    lower = char.lower()
                    sq = Square.from_index(file_ind + 8 * rank_ind)
                    self.bb_colors[char != lower] |= sq
                    piece_type = PieceType(lower)
                    self.bb_pieces[piece_type] |= sq
                    file_ind += 1
            if file_ind != 8:
                raise ValueError("Invalid SAN: {!r}; too many spaces in rank ".format(
                        san, rank_ind + 1))
            num_flag = False
        self.bb_all = self.bb_colors[Color.LIGHT] | self.bb_colors[Color.DARK]

    def get_san(self) -> str:
        builder = []
        ws_count = 0
        for sq in Square:
            if sq.index % 8 == 0:
                if ws_count:
                    builder.append(chr(ws_count + CH_0))
                    ws_count = 0
                if sq.index != 0:
                    builder.append("/")
            p = self.get_piece_at(sq)
            if p is None:
                ws_count += 1
            else:
                if ws_count:
                    builder.append(chr(ws_count + CH_0))
                    ws_count = 0
                builder.append(p.char)
        if ws_count:
            builder.append(chr(ws_count + CH_0))
        return "".join(builder)

    def set_bitboards(self, bbs: bytes) -> None:
        self.empty()
        s = struct.unpack(">9Q", bbs)
        self.bb_all = Square(s[0])
        self.bb_colors[0] = Square(s[1])
        self.bb_colors[1] = Square(s[2])
        for i, pt in enumerate(PieceType, start=3):
            self.bb_pieces[pt] = Square(s[i])

    def get_bitboards(self) -> bytes:
        return struct.pack(">9Q",
            self.bb_all,
            *self.bb_colors,
            *self.bb_pieces.values()
        )

    def pretty_bitboards(self) -> str:
        title = ("{:8s} "*9).format("all", "lights", "dark", *(str(pt).lower() for pt in PieceType))
        bbs = (" ".join("{:08b}".format((bb >> i) & 0xff)[::-1]
                for bb in (self.bb_all, *self.bb_colors, *self.bb_pieces.values()))
                for i in range(0, 64, 8))
        return "{}\n{}".format(title, "\n".join(bbs))

    def has_piece_at(self, sq: Square) -> bool:
        return bool(self.bb_all & sq)

    def get_piecetype_at(self, sq: Square) -> Optional[PieceType]:
        for pt in PieceType:
            if self.bb_pieces[pt] & sq:
                return pt
        return None

    def get_color_at(self, sq: Square) -> Optional[Color]:
        if self.bb_colors[Color.LIGHT] & sq:
            return Color.LIGHT
        if self.bb_colors[Color.DARK] & sq:
            return Color.DARK
        return None

    def get_piece_at(self, sq: Square) -> Optional[Piece]:
        if not self.has_piece_at(sq):
            return None
        return Piece(self.get_color_at(sq), self.get_piecetype_at(sq))

    def set_piece_at(self, sq: Square, piece: Optional[Piece]):
        nsq = ~sq
        if piece is None:
            self.bb_all &= nsq
            for c in Color:
                self.bb_colors[c] &= nsq
            for pt in PieceType:
                self.bb_pieces[pt] &= nsq
        else:
            self.bb_all |= sq
            self.bb_colors[piece.color] |= sq
            self.bb_colors[not piece.color] &= nsq
            t = piece.type
            for pt in PieceType:
                if pt == t:
                    self.bb_pieces[pt] |= sq
                else:
                    self.bb_pieces[pt] &= nsq

    def move(self, fsq: Square, tsq: Square) -> None:
        self[tsq] = self[fsq]
        self[fsq] = None


class CastleRights(enum.IntFlag):
    K = 1  # king-side for light
    Q = 2  # queen-side for light
    k = 4  # king-side for dark
    q = 8  # queen-side for dark

    def __str__(self):
        value = self.value
        members = self.__class__.__members__
        out = []
        for key in members:
            member = members[key]
            if member & value:
                out += member.name
        return "".join(out)

    def __format__(self, fmt):
        return str.__format__(self.__str__(), fmt)


class Board(BaseBoard):
    # __slots__ = "baseboard", "turn", "castle", "ep_target", "halfmoves", "moves", "editable"

    def __init__(self, bb: Optional[BitBoard] = None, turn: Color = Color.LIGHT,
            castle: CastleRights = CastleRights(0b1111), ep_target: Optional[Square] = None,
            halfmoves: int = 0, moves: int = 1, editable: bool = False) -> None:
        super().__init__(bb)
        self.turn = turn
        self.castle = CastleRights(-1)
        self.ep_target = ep_target
        self.halfmoves = halfmoves
        self.moves = moves
        self.editable = editable

    def __str__(self) -> str:
        return self.get_fen()

    def __repr__(self) -> str:
        return "Board.from_fen({!r})".format(self.get_fen())

    def set_fen(self, fen: str) -> None:
        # raises ValueError if not enough or too many components
        san, turn, castle, ep_target, halfmoves, moves = fen.split()
        # convert turn to Color; raises KeyError if turn.lower() is not CHAR_COLOR key
        self.turn = Color.from_char(turn.lower())
        # convert castle to CastleRights
        self.castle = CastleRights(0)
        if castle != "-":
            for letter in castle:
                # raises KeyError if letter is not a CastleRights member
                self.castle |= CastleRights[letter]
        # convert ep_target to Square; raises KeyError if ep_target.upper() is not a Square member
        self.ep_target = Square[ep_target.upper()]
        # convert halfmoves to int; raises ValueError if invalid int
        self.halfmoves = int(halfmoves)
        # convert moves to int; raises ValueError if invalid int
        self.moves = int(moves)
        # set baseboard's SAN; raises ValueError if invalid SAN
        self.set_san(san)

    def get_fen(self):
        return "{} {} {} {} {} {}".format(self.get_san(), self.turn.char, self.castle,
                self.ep_target if self.ep_target else "-", self.halfmoves, self.moves)

    def move(self, fsq: Square, tsq: Square) -> bool:
        if not self.valid_move(fsq, tsq):
            return False
        if self.get_piecetype_at(tsq) is None:
            self.halfmoves += 1
        if self.turn == Color.DARK:
            self.moves += 1
        super().move(fsq, tsq)
        self.turn = not self.turn

    def valid_move(self, fsq: Square, tsq: Square) -> bool:
        from_piece = self[fsq]
        if from_piece is None:
            return False
        if from_piece.color != self.turn:
            return False
        return True
