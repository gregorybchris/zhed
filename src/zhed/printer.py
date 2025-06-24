from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from rich.console import Console

from zhed.models import Board, Direction, Moves, Tile


@dataclass(kw_only=True)
class Printer:
    console: Console

    @classmethod
    def new(cls, console: Optional[Console] = None) -> Printer:
        if console is None:
            console = Console()
        return cls(console=console)

    def print_board(self, board: Board) -> None:
        ret = ""
        for row in range(board.height):
            for col in range(board.width):
                loc = (row, col)
                tile = board.get(loc)
                if tile == Tile.Goal:
                    ret += "[white]@[/white] "
                elif tile == Tile.Empty:
                    ret += ". "
                elif tile == Tile.Blank:
                    ret += "o "
                else:
                    ret += f"[blue]{tile}[/blue] "
            ret += "\n"
        self.console.print(ret.strip())

    def print_moves(self, moves: Moves) -> None:
        ret = "Solution:\n"
        for move in moves:
            loc, direction = move
            row, col = loc
            direction_color = self.direction_to_color(direction)
            ret += (
                f"[white]- [reset]([white]{row}[reset], [white]{col}[reset]) [white]-> [{direction_color}]{direction}\n"
            )
        self.console.print(ret.strip())

    def direction_to_color(self, direction: Direction) -> str:
        match direction:
            case Direction.Up:
                return "red"
            case Direction.Down:
                return "green"
            case Direction.Left:
                return "blue"
            case Direction.Right:
                return "yellow"
            case _:
                msg = f"Unknown direction: {direction}"
                raise ValueError(msg)
