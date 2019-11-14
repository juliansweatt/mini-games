# -*- coding: utf-8 -*-

""" python3 chess game and engine

Using bitboards, this chess implementation maintains the state of a chess game for all of the
pieces. The game state, such as castling rights; en passant; etc, is also used to create a playable
game. The :class:`BaseBoard` stores all bitboards as .The chess engine is (will be) capable of using
a `Game`

For desigining this game, `chessprogramming.org <https://www.chessprogramming.org/Main_Page>`_ has
been very helpful
"""

from typing import List, Optional, Tuple
import enum
import functools
import operator
import struct

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

    def __init__(self, ind: int, mask: int):
        self.W = 0 if ind % 8 == 0 else 1 << (ind - 1)
        self.E = 0 if ind % 8 == 7 else 1 << (ind + 1)
        self.N = 0 if ind // 8 == 0 else 1 << (ind - 8)
        self.S = 0 if ind // 8 == 7 else 1 << (ind + 8)
        self.NW = 0 if (self.N * self.W == 0) else 1 << (ind - 9)
        self.NE = 0 if (self.N * self.E == 0) else 1 << (ind - 7)
        self.SW = 0 if (self.S * self.W == 0) else 1 << (ind + 7)
        self.SE = 0 if (self.S * self.E == 0) else 1 << (ind + 9)

    def __new__(cls, ind: int, mask: int):
        obj = enum.IntFlag.__new__(cls, mask)
        obj._value_ = mask
        obj.index = ind
        return obj

    def __iter__(self): # not efficient
        value = self.value
        for i in range(64):
            if (1 << i) & value:
                yield self.__class__(1 << i)

    def __str__(self):
        return self._name_ if self._name_ else "[invalid square]"

    def __format__(self, fmt):
        return str.__format__(self.__str__(), fmt)

    def valid(self):
        return self._name_ is not None

    @classmethod
    def from_index(cls, ind):
        # if ind < 0 or ind > 63:
        #     return None
        return cls(1 << ind)

    def pretty_list(self) -> List[str]:
        builder = []
        inner_builder = []
        for i, sq in enumerate(self.__class__):
            inner_builder.append("1" if sq in self else ".")
            if i % 8 == 7:
                builder.append(" ".join(inner_builder))
                inner_builder = []
        return builder

    def pretty_str(self) -> str:
        return "\n".join(self.pretty_list())

    def pprint(self) -> None:
        print(self.pretty_str())


# convert Square.{cardinal} into appropriate Square (where {cardinal} is N, S, W, E or any combo/intercadinal);
# can't do in __init__ since each Square is create incrementally
for sq in Square:
    sq.W = Square(sq.W)
    sq.E = Square(sq.E)
    sq.N = Square(sq.N)
    sq.S = Square(sq.S)
    sq.NW = Square(sq.NW)
    sq.NE = Square(sq.NE)
    sq.SW = Square(sq.SW)
    sq.SE = Square(sq.SE)

# generate additional attributes
for sq in Square:
    sq.NNW = sq.NW.N if sq.NW and sq.NW.N else Square(0)
    sq.NWW = sq.NW.W if sq.NW and sq.NW.W else Square(0)
    sq.NNE = sq.NE.N if sq.NE and sq.NE.N else Square(0)
    sq.NEE = sq.NE.E if sq.NE and sq.NE.E else Square(0)
    sq.SSW = sq.SW.S if sq.SW and sq.SW.S else Square(0)
    sq.SWW = sq.SW.W if sq.SW and sq.SW.W else Square(0)
    sq.SSE = sq.SE.S if sq.SE and sq.SE.S else Square(0)
    sq.SEE = sq.SE.E if sq.SE and sq.SE.E else Square(0)
    # NN/SS: for pawns if they can jump two squares
    sq.NN = sq.N.N if sq.N else Square(0)
    sq.SS = sq.S.S if sq.S else Square(0)
    # BB_KING: mask for squares a king can move to
    sq.BB_KING = sq.N|sq.W|sq.S|sq.E|sq.NW|sq.NE|sq.SE|sq.SW
    # BB_KNIGHT: mask for squares a knight can jump to
    sq.BB_KNIGHT = sq.NNW|sq.NWW|sq.NNE|sq.NEE|sq.SSW|sq.SWW|sq.SSE|sq.SEE
    # div and mod locals
    div = sq.index // 8
    mod = sq.index % 8
    # BB_FILE: mask for files (rooks, queens)
    sq.BB_FILE = Square(0)
    tmpsq = Square.from_index(mod)
    while tmpsq:
        sq.BB_FILE |= tmpsq
        tmpsq = tmpsq.S
    # BB_RANK: mask for ranks (rooks, queens)
    sq.BB_RANK = Square(0)
    tmpsq = Square.from_index(div * 8)
    while tmpsq:
        sq.BB_RANK |= tmpsq
        tmpsq = tmpsq.E
    # BB_FDIAG: falling (top-left to bottom-right) diagonals
    sq.BB_FDIAG = Square(0)
    d = div - mod
    tmpsq = Square.from_index(-d) if d < 0 else Square.from_index(d * 8)
    while tmpsq:
        sq.BB_FDIAG |= tmpsq
        tmpsq = tmpsq.SE
    # BB_RDIAG: rising (bottom-left to top-right) diagonals
    sq.BB_RDIAG = Square(0)
    d = div + mod - 7
    tmpsq = Square.from_index(7 + d) if d < 0 else Square.from_index(7 + 8 * d)
    while tmpsq:
        sq.BB_RDIAG |= tmpsq
        tmpsq = tmpsq.SW
    # BB_ORTHOGONALS: BB_RANK and BB_FILE
    sq.BB_ORTHOGONALS = sq.BB_RANK | sq.BB_FILE
    # BB_DIAGS: FDIAGS and RDIAGS
    sq.BB_DIAGS = sq.BB_FDIAG | sq.BB_RDIAG
    # BB_LINES: BB_ORTHOGONALS and BB_DIAGS
    sq.BB_LINES = sq.BB_ORTHOGONALS | sq.BB_DIAGS
    # ALL: BB_LINES and BB_KNIGHT
    sq.ALL = sq.BB_LINES | sq.BB_KNIGHT



BitBoard = Square
BB_ALL = Square(-1)
BB_RANKS = BB_RANK_8, BB_RANK_7, BB_RANK_6, BB_RANK_5, BB_RANK_4, BB_RANK_3, BB_RANK_2, BB_RANK_1 = tuple(functools.reduce(operator.or_, (Square.from_index(i) for i in range(j, j + 8))) for j in range(0, 64, 8))
BB_FILES = BB_FILE_A, BB_FILE_B, BB_FILE_C, BB_FILE_D, BB_FILE_E, BB_FILE_F, BB_FILE_G, BB_FILE_H = tuple(functools.reduce(operator.or_, (Square.from_index(i) for i in range(j, 64, 8))) for j in range(0, 8))

ByteBoard = int  # packed ``BitBoard``s
# equal to BaseBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
BYTB_STD = struct.pack(">9Q",
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

    def __init__(self, val):
        self.char = COLOR_CHARS[val]
        self.lname = self.name.lower()

    def __str__(self) -> str:
        return self.lname

    def __repr__(self) -> str:
        return "Color.{}".format(self.name)

    def __format__(self, fmt) -> str:
        return str.__format__(self.__str__(), fmt)

    def __invert__(self) -> "Color":
        return Color(not self)

    @classmethod
    def from_char(cls, char: str) -> "Color":
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

    def __init__(self, value):
        self.lname = self.name.lower()

    def __str__(self) -> str:
        return self.lname

    def __repr__(self) -> str:
        return "PieceType.{}".format(self.name)

    def __int__(self) -> int:
        return PIECE_INTS[self.value]

    def __bool__(self) -> bool:
        return bool(self.__int__())

    def __hash__(self) -> int:
        return self.__int__()

    @classmethod
    def from_int(cls, i: int) -> "PieceType":
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
        return self.char

    def __repr__(self) -> str:
        return "Piece({!r}, {!r})".format(self.color, self.type)

    def __eq__(self, other) -> bool:
        return hasattr(other, "char") and self.char == other.char

    def __hash__(self) -> int:
        return int(self.type) + 6 * int(self.color)

    @classmethod
    def from_char(cls, c) -> "Piece":
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
    def __init__(self, bb: Optional[str] = None) -> None:
        """ BaseBoard initializer

        :param bb: bitboard to initialize the board; if empty, set to standard
        """
        self.set_byteboard(bb if bb else BYTB_STD)

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

    def set_byteboard(self, bbs: bytes) -> None:
        self.empty()
        s = struct.unpack(">9Q", bbs)
        self.bb_all = Square(s[0])
        self.bb_colors[0] = Square(s[1])
        self.bb_colors[1] = Square(s[2])
        for i, pt in enumerate(PieceType, start=3):
            self.bb_pieces[pt] = Square(s[i])

    def get_byteboard(self) -> bytes:
        return struct.pack(">9Q",
            self.bb_all,
            *self.bb_colors,
            *self.bb_pieces.values()
        )

    def pretty_bitboards(self) -> str:
        title = ("| {:15s} "*9).format("all", "lights", "dark", *(str(pt).lower() for pt in PieceType))
        # for bline in (bb.pretty_list() for bb in (self.bb_all, *self.bb_colors, *self.bb_pieces.values())):
        #     print(bline)
        bbs = (" | ".join(bline) for bline in zip(*(bb.pretty_list() for bb in (self.bb_all, *self.bb_colors, *self.bb_pieces.values()))))
        return "{}|\n| {} |".format(title, " |\n| ".join(bbs))

    def pprint_bitboards(self) -> None:
        print(self.pretty_bitboards())

    def pretty_board(self) -> List[str]:
        builder = []
        inner = []
        for i, p in enumerate(self):
            inner.append(p.char if p else ".")
            if i % 8 == 7:
                builder.append(inner)
                inner = []
        return builder

    def pprint(self) -> str:
        print("\n".join(" ".join(char for char in line) for line in self.pretty_board()))

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

    def set_piece_at(self, sq: Square, piece: Optional[Piece]) -> None:
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


class CastleRight(enum.IntFlag):
    K = 1  # king-side for light
    Q = 2  # queen-side for light
    k = 4  # king-side for dark
    q = 8  # queen-side for dark

    def __str__(self) -> str:
        value = self.value
        members = self.__class__.__members__
        out = []
        for key in members:
            member = members[key]
            if member & value:
                out += member.name
        return "".join(out)

    def __format__(self, fmt) -> str:
        return str.__format__(self.__str__(), fmt)


class Board(BaseBoard):
    """ Board that inherits BaseBoard but adds state, fen conversion and move validation """

    def __init__(self, bb: Optional[BitBoard] = None, turn: Color = Color.LIGHT,
            castle: CastleRight = CastleRight(0b1111), ep_target: Optional[Square] = None,
            halfmoves: int = 0, moves: int = 1, startcolor: Color = Color.LIGHT,
            editable: bool = False):
        super().__init__(bb)
        self.startcolor = startcolor
        self.turn = turn
        self.castle = CastleRight(-1)
        self.ep_target = ep_target
        self.halfmoves = halfmoves
        self.moves = moves
        self.editable = editable
        self.movestatus = 0b0000000  # capture; pawn moved; castle K; castle Q; castle k; castle q
        # NOTE: en passant denoted with capture and pawn moved

    def __str__(self) -> str:
        return self.get_fen()

    def __repr__(self) -> str:
        return "Board.from_fen({!r})".format(self.get_fen())

    def set_fen(self, fen: str) -> None:
        # raises ValueError if not enough or too many components
        san, turn, castle, ep_target, halfmoves, moves = fen.split()
        # convert turn to Color; raises KeyError if turn.lower() is not CHAR_COLOR key
        self.turn = Color.from_char(turn.lower())
        # convert castle to CastleRight
        self.castle = CastleRight(0)
        if castle != "-":
            for letter in castle:
                # raises KeyError if letter is not a CastleRight member
                self.castle |= CastleRight[letter]
        # convert ep_target to Square; raises KeyError if ep_target.upper() is not a Square member
        self.ep_target = Square[ep_target.upper()]
        # convert halfmoves to int; raises ValueError if invalid int
        self.halfmoves = int(halfmoves)
        # convert moves to int; raises ValueError if invalid int
        self.moves = int(moves)
        # set baseboard's SAN; raises ValueError if invalid SAN
        self.set_san(san)

    def get_fen(self) -> str:
        return "{} {} {} {} {} {}".format(self.get_san(), self.turn.char, self.castle,
                self.ep_target if self.ep_target else "-", self.halfmoves, self.moves)

    def move(self, fsq: Square, tsq: Square) -> bool:
        if fsq is None or tsq is None or not self.valid_move(fsq, tsq):
            return False
        if self.movestatus & 0b100000:
            # captured
            print("capture")
            if self.movestatus & 0b010000:
                if not self.has_piece_at(tsq):
                    print(f"en passant on target square {self.ep_target}")
                    # capture and pawn moved: en passant
                    if tsq in BB_RANK_6:
                        # light en passant
                        print(f"light en passant capture", tsq.S)
                        self[tsq.S] = None
                    elif tsq in BB_RANK_3:
                        # dark en passant
                        print(f"dark en passant capture", tsq.N)
                        self[tsq.N] = None
                    else:
                        raise RuntimeError(f"valid_move yielded en passant for invalid rank for move {fsq}{tsq}")
                # else: normal pawn capture
        elif self.movestatus & 0b010000:
            # pawn move
            if tsq == fsq.NN:
                # light double push
                self.ep_target = fsq.N
                print(f"set ep target to {self.ep_target}")
            elif tsq == fsq.SS:
                # dark double push
                self.ep_target = fsq.S
                print(f"set ep target to {self.ep_target}")
            else:
                self.ep_target = None  # reset ep_target each successful move
        else:
            self.ep_target = None
        super().move(fsq, tsq)
        if self.movestatus & 0b001000:
            # light king-side castle
            super().move(Square.H1, Square.F1)
        elif self.movestatus & 0b000100:
            # light queen-side castle
            super().move(Square.A1, Square.D1)
        elif self.movestatus & 0b000010:
            # dark king-side castle
            super().move(Square.H8, Square.F8)
        elif self.movestatus & 0b000001:
            # dark queen-side castle
            super().move(Square.A8, Square.D8)
        # update halfmoves appropriately per
        # https://www.chessprogramming.org/Halfmove_Clock
        if self.movestatus & 0b110000:
            self.halfmoves = 0
        else:
            self.halfmoves += 1
        if self.turn == (not self.startcolor):
            self.moves += 1
        self.turn = not self.turn
        print(f"moves: {self.moves}; halfmoves: {self.halfmoves}; {self.turn} to move")
        return True

    def valid_move(self, fsq: Square, tsq: Square) -> bool:
        self.movestatus = 0b000000
        print(fsq, tsq)
        ftype = self.get_piecetype_at(fsq)
        if ftype is None:
            # no piece selected in from square
            print(f"invalid move {fsq}{tsq}: no piece selected")
            return False
        fcolor = self.get_color_at(fsq)
        if fcolor != self.turn:
            # wrong color trying to move
            print(f"invalid move {fsq}{tsq}: it is not {fcolor}'s turn")
            return False
        tcolor = self.get_color_at(tsq)
        if tcolor is not None:
            # add capture flag to movestatus
            self.movestatus |= 0b100000
        if fcolor == tcolor:
            # trying to capture own piece
            print(f"invalid move {fsq}{tsq}: cannot move {fcolor} piece onto same color")
            return False
        if ftype == PieceType.PAWN:
            if fcolor:
                # dark pawn
                if tsq == fsq.SS:
                    # double push attempt
                    if fsq not in BB_RANK_7:
                        # not in correct rank
                        print(f"invalid move {fsq}{tsq}: cannot advance {fcolor} pawn twice unless it's on rank 7")
                        return False
                    if self.has_piece_at(fsq.S | tsq):
                        # piece on target square or blocking
                        print(f"invalid move {fsq}{tsq}: cannot advance pawn twice because it is blocked by another piece")
                        return False
                    # add pawn moved to movestatus
                    self.movestatus |= 0b010000
                elif tsq in fsq.SW | fsq.SE:
                    # pawn capture attempt
                    if not (tsq == self.ep_target or self.has_piece_at(tsq)):
                        # target square is not en passant target square and target square doesn't have enemy
                        print(f"invalid move {fsq}{tsq}: pawn cannot capture an empty square unless it's the en passant target")
                        return False
                    # add capture and pawn moved to movestatus to denote en passant
                    print("add capture and pawn moved to movestatus")
                    self.movestatus |= 0b110000
                elif tsq != fsq.S:
                    # pawn not moved to invalid square
                    print(f"invalid move {fsq}{tsq}: pawn cannot advance here")
                    return False
                elif self.has_piece_at(tsq):
                    # pawn cannot move vertically to square with piece
                    print(f"invalid move {fsq}{tsq}: pawn cannot advance onto another piece")
                    return False
                # else: pawn advanced one square
                # add pawn moved to movestatus
                self.movestatus |= 0b010000
            else:
                # light pawn
                if tsq == fsq.NN:
                    # double push attempt
                    if fsq not in BB_RANK_2:
                        print(f"invalid move {fsq}{tsq}: cannot advance {fcolor} pawn twice unless it's on rank 2")
                        # not in correct rank
                        return False
                    if self.has_piece_at(fsq.N | tsq):
                        # piece on target square or blocking
                        print(f"invalid move {fsq}{tsq}: cannot advance pawn twice because it is blocked by another piece")
                        return False
                    # add pawn moved to movestatus
                    self.movestatus |= 0b010000
                elif tsq in fsq.NW | fsq.NE:
                    # pawn capture attempt
                    if not (tsq == self.ep_target or self.has_piece_at(tsq)):
                        # target square is not en passant target square and target square doesn't have enemy
                        print(f"invalid move {fsq}{tsq}: pawn cannot capture an empty square unless it's the en passant target")
                        return False
                    # add capture and pawn moved to movestatus to denote en passant
                    print("add capture and pawn moved to movestatus")
                    self.movestatus |= 0b110000
                elif tsq != fsq.N:
                    # pawn not moved to invalid square
                    print(f"invalid move {fsq}{tsq}: pawn cannot be moved here")
                    return False
                elif self.has_piece_at(tsq):
                    # pawn cannot move vertically to square with piece
                    print(f"invalid move {fsq}{tsq}: pawn cannot advance onto another piece")
                    return False
                # else: pawn advanced one square
                # add pawn moved to movestatus
                self.movestatus |= 0b010000
        elif ftype == PieceType.KNIGHT:
            if tsq not in fsq.BB_KNIGHT:
                # knight not moved to proper square
                print(f"invalid move {fsq}{tsq}: knight must move to one of: {', '.join(str(sq) for sq in fsq.BB_KNIGHT)}")
                return False
        elif ftype == PieceType.BISHOP:
            if tsq in fsq.BB_FDIAG:
                # moved along falling diagonal
                if tsq > fsq:
                    # moved south-east
                    nsq = fsq.SE
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between to and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.SE
                else:
                    # moved north-west
                    nsq = fsq.NW
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between to and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.NW
            elif tsq in fsq.BB_RDIAG:
                # moved along rising diagonal
                if tsq > fsq:
                    # moved south-west
                    nsq = fsq.SW
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between to and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.SW
                else:
                    # moved north-east
                    nsq = fsq.NE
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between to and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.NE
            else:
                # bishop not moved to a diagonal square
                print(f"invalid move {fsq}{tsq}: bishop must move along a diagonal")
                return False
        elif ftype == PieceType.ROOK:
            if tsq in fsq.BB_RANK:
                # moved along rank
                if tsq > fsq:
                    # move is east
                    nsq = fsq.E
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between t and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.E
                else:
                    # move is west
                    nsq = fsq.W
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between t and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.W
            elif tsq in fsq.BB_FILE:
                # moved along file
                if tsq > fsq:
                    # move is south
                    nsq = fsq.S
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between t and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.S
                else:
                    # move is north
                    nsq = fsq.N
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between t and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.N
            else:
                # rook not moved to an orthogonal square
                print(f"invalid move {fsq}{tsq}: rook must move along a rank or file")
                return False
        elif ftype == PieceType.QUEEN:
            if tsq in fsq.BB_FDIAG:
                # moved along falling diagonal
                if tsq > fsq:
                    # moved south-east
                    nsq = fsq.SE
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between to and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.SE
                else:
                    # moved north-west
                    nsq = fsq.NW
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between to and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.NW
            elif tsq in fsq.BB_RDIAG:
                # moved along rising diagonal
                if tsq > fsq:
                    # moved south-west
                    nsq = fsq.SW
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between to and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.SW
                else:
                    # moved north-east
                    nsq = fsq.NE
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between to and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.NE
            elif tsq in fsq.BB_RANK:
                # moved along rank
                if tsq > fsq:
                    # move is east
                    nsq = fsq.E
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between t and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.E
                else:
                    # move is west
                    nsq = fsq.W
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between t and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.W
            elif tsq in fsq.BB_FILE:
                # moved along file
                if tsq > fsq:
                    # move is south
                    nsq = fsq.S
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between t and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.S
                else:
                    # move is north
                    nsq = fsq.N
                    while nsq != tsq:
                        if self.has_piece_at(nsq):
                            # piece between t and from square
                            print(f"invalid move {fsq}{tsq}: piece blocking move")
                            return False
                        nsq = nsq.N
            else:
                # queen not moved to a diagonal or orthogonal square
                print(f"invalid move {fsq}{tsq}: queen must move along a diagonal, rank, or file")
                return False
        elif ftype == PieceType.KING:
            if (tsq == Square.G1 and fcolor == Color.LIGHT
            and self[Square.H1] == Piece(Color.LIGHT, PieceType.ROOK)):
                # light king-side castle attempt
                if self.has_piece_at(Square.F1 | Square.G1):
                    # piece blocking castle
                    print(f"invalid move {fsq}{tsq}: cannot castle; at least one piece blocking {fcolor} king")
                    return False
                elif CastleRight.K not in self.castle:
                    # light king-side castle rights destroyed
                    print(f"invalid move {fsq}{tsq}: {fcolor} unable to king-side castle")
                    return False
                # add light king-side castle to movestatus
                self.movestatus |= 0b001000
            elif (tsq == Square.C1 and fcolor == Color.LIGHT
            and self[Square.A1] == Piece(Color.LIGHT, PieceType.ROOK)):
                # light queen-side castle attempt
                if self.has_piece_at(Square.B1 | Square.C1 | Square.D1):
                    # piece blocking castle
                    print(f"invalid move {fsq}{tsq}: cannot castle; at least one piece blocking {fcolor} king")
                    return False
                elif CastleRight.Q not in self.castle:
                    # light queen-side castle rights destroyed
                    print(f"invalid move {fsq}{tsq}: {fcolor} unable to queen-side castle")
                    return False
                # add light queen-side castle to movestatus
                self.movestatus |= 0b000100
            elif (tsq == Square.G8 and fcolor == Color.DARK
            and self[Square.H8] == Piece(Color.DARK, PieceType.ROOK)):
                # dark king-side castle attempt
                if self.has_piece_at(Square.F8 | Square.G8):
                    # piece blocking castle
                    print(f"invalid move {fsq}{tsq}: cannot castle; at least one piece blocking {fcolor} king")
                    return False
                elif CastleRight.k not in self.castle:
                    # dark king-side castle rights destroyed
                    print(f"invalid move {fsq}{tsq}: {fcolor} unable to king-side castle")
                    return False
                # add dark king-side castle to movestatus
                self.movestatus |= 0b000010
            elif (tsq == Square.C8 and fcolor == Color.DARK
            and self[Square.A8] == Piece(Color.DARK, PieceType.ROOK)):
                # dark queen-side castle attempt
                if self.has_piece_at(Square.B8 | Square.C8 | Square.D8):
                    # piece blocking castle
                    print(f"invalid move {fsq}{tsq}: cannot castle; at least one piece blocking {fcolor} king")
                    return False
                elif CastleRight.q not in self.castle:
                    # dark queen-side castle rights destroyed
                    print(f"invalid move {fsq}{tsq}: {fcolor} unable to queen-side castle")
                    return False
                # add dark queen-side castle to movestatus
                self.movestatus |= 0b000001
            elif tsq not in fsq.BB_KING:
                # king not moved to adjacent square
                print(f"invalid move {fsq}{tsq}: king can only move to an adjacent square or castle")
                return False
        return True
