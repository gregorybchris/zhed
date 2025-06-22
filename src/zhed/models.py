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
Solution = list[Move]
Edit = tuple[Loc, int]


@dataclass(kw_only=True)
class Board:
    width: int
    height: int
    tiles: list[list[int]]

    @classmethod
    def new(cls, width: int, height: int) -> Board:
        tiles: list[list[int]] = [[Tile.Empty for _ in range(width)] for _ in range(height)]
        return cls(width=width, height=height, tiles=tiles)

    def get(self, loc: Loc) -> int:
        assert self.in_bounds(loc)
        row, col = loc
        return self.tiles[row][col]

    def set(self, loc: Loc, value: int) -> None:
        assert self.in_bounds(loc)
        row, col = loc
        self.tiles[row][col] = value

    def in_bounds(self, loc: Loc) -> bool:
        row, col = loc
        return row >= 0 and row < self.height and col >= 0 and col < self.width


class Level(BaseModel):
    number: int
    board_str: str
    solution: Solution

    def get_board(self) -> Board:
        rows = [row.split() for row in self.board_str.strip().splitlines()]
        height = len(rows)
        width = len(rows[0]) if height > 0 else 0
        board = Board.new(width, height)
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
