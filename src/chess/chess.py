#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=trailing-whitespace

""" Python3 Chess game and engine

Using bitboards, this chess implementation maintains the board state, generates
a list of moves, and performs move validation. It also allows saving board
states and entire games as a sequence of packed bytes. It can communicate with
an external graphical chess board via a simple protocol, but it can also render
simple ASCII chess boards as an array of strings.
"""

from typing import List, Optional

Color = bool

COLORS = DARK, LIGHT = (False, True)
""" light and dark `Color`s """

COLOR_NAMES = ("dark", "light")
""" color names """

# Bitboard type
Bitboard = int

# Piece type
PieceType = int

PIECE_TYPES = P_NONE, P_PAWN, P_KNIGHT, P_BISHOP, P_ROOK, P_QUEEN, P_KING = tuple(range(7))
""" Chess piece types """

PIECE_NAMES = ("empty", "pawn", "knight", "bishop", "rook", "queen", "king")
""" Chess piece names """

PIECE_CHARS = ("_", "p", "n", "b", "r", "q", "k")
""" Chess piece character symbols """

CH_ZERO = ord("0")

FILE_NAMES = [chr(i + ord("a")) for i in range(8)]
""" name of files from left to right """

RANK_NAMES = [chr(i + CH_ZERO) for i in range(8, 0, -1)]
""" name of rank from top to bottom """

Square = int

SQUARES = (
    A8, B8, C8, D8, E8, F8, G8, H8,
    A7, B7, C7, D7, E7, F7, G7, H7,
    A6, B6, C6, D6, E6, F6, G6, H6,
    A5, B5, C5, D5, E5, F5, G5, H5,
    A4, B4, C4, D4, E4, F4, G4, H4,
    A3, B3, C3, D3, E3, F3, G3, H3,
    A2, B2, C2, D2, E2, F2, G2, H2,
    A1, B1, C1, D1, E1, F1, G1, H1,
) = tuple(range(64))
""" All `Square`s from 0 (top-left) to 63 (bottom-right) """

SQUARE_NAMES = [f + r for r in RANK_NAMES for f in FILE_NAMES]
""" name of square from top-left to bottom-right """

Bitboard = int

BB_NONE = 0
""" Bitboard where all 64 are bits empty """

BB_ALL = (1 << 64) - 1
""" Bitboard  """

BB_SQUARES = [
    BB_A8, BB_B8, BB_C8, BB_D8, BB_E8, BB_F8, BB_G8, BB_H8,
    BB_A7, BB_B7, BB_C7, BB_D7, BB_E7, BB_F7, BB_G7, BB_H7,
    BB_A6, BB_B6, BB_C6, BB_D6, BB_E6, BB_F6, BB_G6, BB_H6,
    BB_A5, BB_B5, BB_C5, BB_D5, BB_E5, BB_F5, BB_G5, BB_H5,
    BB_A4, BB_B4, BB_C4, BB_D4, BB_E4, BB_F4, BB_G4, BB_H4,
    BB_A3, BB_B3, BB_C3, BB_D3, BB_E3, BB_F3, BB_G3, BB_H3,
    BB_A2, BB_B2, BB_C2, BB_D2, BB_E2, BB_F2, BB_G2, BB_H2,
    BB_A1, BB_B1, BB_C1, BB_D1, BB_E1, BB_F1, BB_G1, BB_H1,
] = [1 << i for i in range(64)]
""" Bitboard of all squares """

BB_CORNERS = BB_A1 | BB_H1 | BB_A8 | BB_H8
""" TODO """
BB_CENTER = BB_D4 | BB_E4 | BB_D5 | BB_E5
""" TODO """

BB_LIGHT_SQUARES = 0x55aa55aa55aa55aa
""" TODO """
BB_DARK_SQUARES = 0xaa55aa55aa55aa55
""" TODO """

BB_FILES = [
    BB_FILE_A,
    BB_FILE_B,
    BB_FILE_C,
    BB_FILE_D,
    BB_FILE_E,
    BB_FILE_F,
    BB_FILE_G,
    BB_FILE_H,
] = [0x101010101010101 << i for i in range(8)]
""" TODO """

BB_RANKS = [
    BB_RANK_8,
    BB_RANK_7,
    BB_RANK_6,
    BB_RANK_5,
    BB_RANK_4,
    BB_RANK_3,
    BB_RANK_2,
    BB_RANK_1,
] = [0xff << (8 * i) for i in range(8)]
""" TODO """

BB_BACKRANKS = BB_RANK_1 | BB_RANK_8
""" TODO """


class Piece():
    """ A piece with a type and color
    """

    def __init__(self, typ: Optional[PieceType], color: bool) -> None:
        """ docstring TODO """
        self.type = typ
        self.piece_color = color

    def __str__(self):
        """ docstring TODO """
        name = PIECE_CHARS[self.type]
        if self.piece_color:
            name = name.upper()
        return name

    def __repr__(self):
        """ docstring TODO """
        if self.type:
            return "{} {}".format(COLOR_NAMES[self.piece_color], PIECE_NAMES[self.type])
        else:
            return "Empty"

    def __eq__(self, other):
        """ docstring TODO """
        return self.type == other.type and self.piece_color == other.piece_color

    def __hash__(self):
        """ docstring TODO """
        return self.type + 6 * self.piece_color


class BaseBoard():
    """ A board storing all of the bit boards

    This class specifically only stores the bitboards for `active_all`,
    `active_co` (both `LIGHT` and `DARK`), `pawns`, `knights`, `bishops`,
    `rooks`, `queens,` and `kings` as well as a type array map to make creating
    and using `BaseBoard`s fast.

    Converting a `BaseBoard` to a string implicitly or explicitly with str() or
    repr() will format it nicely so that it stores useful information. str() is
    less verbose and returns the SAN of the board, while repr() is more verbose
    and prints the hex numbers of the bitboards as well as each 8x8
    representation of 1s and 0s of each bitboard in addition to the type array
    map at the end.

    .. todo:: allow BaseBoard to validate state. potentially with a status
       bitfield or some other other external BaseStatus Object
    """

    standard_san = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    """ SAN notation for starting positions for standard/classical chess """

    def __init__(self, san: str = None) -> None:
        self._set_san(san if san else BaseBoard.standard_san, assume_start=True)

    def empty(self) -> None:
        """ zeros all bitboards to create an empty board """

        # pylint: disable=attribute-defined-outside-init

        self.active_all: Bitboard = BB_NONE
        self.active_co: List[Bitboard] = [BB_NONE, BB_NONE]
        self.bb_pieces = [BB_NONE] * len(PIECE_TYPES)
        self.type_arr: PieceType = [P_NONE] * 64

    @property
    def san(self) -> str:
        """ docstring TODO """
        return self._get_san()

    @san.setter
    def san(self, san: Optional[str]) -> None:
        """ docstring TODO """
        self._set_san(san)

    def _get_san(self) -> str:
        """ docstring TODO """
        builder = []
        ws_count = 0
        for square in range(64):
            if square % 8 == 0:
                if ws_count:
                    builder.append(chr(ws_count + CH_ZERO))
                    ws_count = 0
                if square != 0:
                    builder.append("/")
            bit = 1 << square
            if self.active_all & bit:
                if ws_count:
                    builder.append(chr(ws_count + CH_ZERO))
                    ws_count = 0

                builder.append("pnbrqkPNBRQK"[6 * bool(self.active_co[LIGHT] & bit) + (
                    (
                    (self.bb_pieces[P_PAWN] & bit)
                    | (2 * (self.bb_pieces[P_KNIGHT] & bit))
                    | (3 * (self.bb_pieces[P_BISHOP] & bit))
                    | (4 * (self.bb_pieces[P_ROOK] & bit))
                    | (5 * (self.bb_pieces[P_QUEEN] & bit))
                    | (6 * (self.bb_pieces[P_KING] & bit))
                    ) >> square) - 1])
            else:
                ws_count += 1
        if ws_count:
            builder.append(chr(ws_count + CH_ZERO))
        return ''.join(builder)


    def _set_san(self, san: Optional[str], assume_start: bool = False) -> None:
        """ docstring TODO """
        self.empty()
        split_san = (san if san else BaseBoard.standard_san).split("/")
        if len(split_san) != 8:
            raise ValueError(
                "expected SAN to have 8 rows separated by a '/'; got invalid SAN, \"{}\""
                .format(san)
            )
        flag_num = False
        for rank_ind, row in enumerate(split_san):
            file_ind = 0
            for char in row:
                if char in RANK_NAMES:
                    if flag_num:
                        raise ValueError("invalid consecutive numbers in SAN, \"{}\"".format(san))
                    file_ind += ord(char) - CH_ZERO
                    flag_num = True
                else:
                    flag_num = False
                    lower = char.lower()
                    square = file_ind + 8 * rank_ind
                    bit = 1 << square
                    self.active_co[char != lower] |= bit
                    # next line of code fails with value error if lower not in PIECE_TYPES
                    piece_type = PIECE_TYPES[PIECE_CHARS.index(lower)]
                    self.type_arr[square] = piece_type
                    self.bb_pieces[piece_type] |= bit
                    file_ind += 1
            if file_ind != 8:
                raise ValueError(
                    "invalid number of pieces specified in rank {} in SAN"
                    .format(rank_ind + 1)
                )
            flag_num = False
        self.active_all = self.active_co[LIGHT] | self.active_co[DARK]


    def __str__(self):
        """
        when a BaseBoard is printed or converted to a str with str(), format it
        nicely as a SAN

        :Example:

        >>> import chess
        >>> b = chess.BaseBoard()
        >>> print(b)
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR

        """

        return self._get_san()

    def __repr__(self):
        """
        when repr() is called on a BaseBoard, print all bitboards as hex numbers
        and as 8x8 bitboards and also print the type array as a 64-char string
        and as a board

        :Example:

        >>> import chess
        >>> b = chess.BaseBoard()
        >>> b
        all: ffff00000000ffff
        lights: ffff000000000000
        darks: 000000000000ffff
        pawns: 00ff00000000ff00
        knights: 4200000000000042
        bishops: 2400000000000024
        rooks: 8100000000000081
        queens: 0800000000000008
        kings: 1000000000000010
        types: rnbqkbnrpppppppp________________________________pppppppprnbqkbnr
        ------------------------------------------------------------------------------------------
        all      lights   darks    pawns    knights  bishops  rooks    queens   kings    types    
        11111111 00000000 11111111 00000000 01000010 00100100 10000001 00010000 00001000 rnbqkbnr
        11111111 00000000 11111111 11111111 00000000 00000000 00000000 00000000 00000000 pppppppp
        00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 ________
        00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 ________
        00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 ________
        00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 ________
        11111111 11111111 00000000 11111111 00000000 00000000 00000000 00000000 00000000 pppppppp
        11111111 11111111 00000000 00000000 01000010 00100100 10000001 00010000 00001000 rnbqkbnr

        """

        piece_types = PIECE_TYPES[1:]
        builder = []
        builder.append("all: {:016x}".format(self.active_all))
        builder.append("lights: {:016x}".format(self.active_co[LIGHT]))
        builder.append("darks: {:016x}".format(self.active_co[DARK]))
        for pt in piece_types:
            builder.append("{}s: {:016x}".format(PIECE_NAMES[pt], self.bb_pieces[pt]))
        builder.append("types: {}".format("".join(PIECE_CHARS[n] for n in self.type_arr)))
        builder.append("-" * 90)
        builder.append(("{:8s} " * 10).format(
            "all",
            "lights",
            "darks",
            "pawns",
            "knights",
            "bishops",
            "rooks",
            "queens",
            "kings",
            "types",
        ))
        for i in range(0, 64, 8):
            inner_builder = [
                "{:08b}".format((self.active_all >> i) & 0xff)[::-1],
                "{:08b}".format((self.active_co[LIGHT] >> i) & 0xff)[::-1],
                "{:08b}".format((self.active_co[DARK] >> i) & 0xff)[::-1],
            ]
            for pt in piece_types:
                inner_builder.append("{:08b}".format((self.bb_pieces[pt] >> i) & 0xff)[::-1])
            inner_builder.append("".join(PIECE_CHARS[n] for n in self.type_arr[i:i+8]))
            builder.append(" ".join(inner_builder))
        return "\n".join(builder)

    def get_piece_type_at(self, square: Square) -> PieceType:
        """ docstring TODO """
        return self.type_arr[square]

    def get_piece_at(self, square: Square) -> Piece:
        """ docstring TODO """
        return Piece(self.type_arr[square], bool(self.active_co[LIGHT] & 1 << square))

    def has_piece_at(self, square: Square) -> bool:
        """ docstring TODO """
        return self.active_all & 1 << square

    def move(self, from_sq: Square, to_sq: Square) -> None:
        """ docstring TODO """
        to_mask = 1 << to_sq
        from_mask = 1 << from_sq
        if not self.active_all & from_mask:
            return
        n_from_mask = ~from_mask
        color = bool(self.active_co[LIGHT] & from_mask)
        from_piece_type = self.type_arr[from_sq]
        # set 0 at from_mask
        self.active_all ^= from_mask
        self.active_co[color] ^= from_mask
        self.bb_pieces[from_piece_type] ^= from_mask
        # set 1 at to_mask
        self.active_all |= to_mask
        self.active_co[color] |= to_mask
        self.bb_pieces[from_piece_type] |= to_mask
        # update type_arr to P_NONE at from_sq and from_piece_type at to_sq
        self.type_arr[from_sq] = P_NONE
        self.type_arr[to_sq] = from_piece_type
