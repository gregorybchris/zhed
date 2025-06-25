from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum

from pydantic import BaseModel


class Direction(StrEnum):
    Up = "U"
    Down = "D"
    Left = "L"
    Right = "R"


class Tile(IntEnum):
    Empty = -1
    Blank = -2
    Goal = -3


Loc = tuple[int, int]
Move = tuple[Loc, Direction]
Moves = list[Move]
Edit = tuple[Loc, int]


@dataclass(kw_only=True)
class Board:
    n_rows: int
    n_cols: int
    tiles: list[list[int]]

    @classmethod
    def new(cls, n_rows: int, n_cols: int) -> Board:
        tiles: list[list[int]] = [[Tile.Empty for _ in range(n_cols)] for _ in range(n_rows)]
        return cls(n_rows=n_rows, n_cols=n_cols, tiles=tiles)

    def get(self, loc: Loc) -> int:
        assert self.in_bounds(loc), f"OOB: {loc} with shape {self.shape}"
        row, col = loc
        return self.tiles[row][col]

    def set(self, loc: Loc, value: int) -> None:
        assert self.in_bounds(loc), f"OOB: {loc} with shape {self.shape}"
        row, col = loc
        self.tiles[row][col] = value

    def in_bounds(self, loc: Loc) -> bool:
        row, col = loc
        return row >= 0 and row < self.n_rows and col >= 0 and col < self.n_cols

    @property
    def shape(self) -> tuple[int, int]:
        return self.n_rows, self.n_cols


class Level(BaseModel):
    number: int
    board_str: str

    def get_board(self) -> Board:
        rows = [row.split() for row in self.board_str.strip().splitlines()]
        n_rows = len(rows)
        n_cols = len(rows[0]) if n_rows > 0 else 0
        board = Board.new(n_rows, n_cols)
        for r, row in enumerate(rows):
            for c, char in enumerate(row):
                loc = (r, c)
                if char == "@":
                    board.set(loc, Tile.Goal)
                elif char == ".":
                    board.set(loc, Tile.Empty)
                elif char == "o":
                    board.set(loc, Tile.Blank)
                else:
                    board.set(loc, int(char))
        return board


class Solution(BaseModel):
    number: int
    moves: list[Move]
