from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from rich.console import Console

from zhed.models import Board, Direction, Level, Move, Tile


@dataclass(kw_only=True)
class Printer:
    console: Console

    @classmethod
    def new(cls, console: Optional[Console] = None) -> Printer:
        if console is None:
            console = Console()
        return cls(console=console)

    def print_level(self, level: Level) -> None:
        board = level.get_board()
        self.print_board(board, number=level.number)

    def print_board(self, board: Board, number: Optional[int] = None) -> None:
        ret = ""
        ret += "[white]╭" + "─" * (board.n_cols * 2 + 1) + "╮\n"
        if number is not None:
            num_len = len(str(number))
            ret += f"[white]│[bold] Level {number} [/bold]" + " " * (board.n_cols * 2 - num_len - 7) + "│[/white]\n"
            ret += "[white]├" + "─" * (board.n_cols * 2 + 1) + "┤\n"
        for row in range(board.n_rows):
            ret += "[white]│[/white] "
            for col in range(board.n_cols):
                loc = (row, col)
                tile = board.get(loc)
                if tile == Tile.Goal:
                    ret += "[green]◎[/green] "
                elif tile == Tile.Empty:
                    ret += "[black]□[/black] "
                elif tile == Tile.Blank:
                    ret += "[black]■[/black] "
                else:
                    ret += f"[blue]{tile}[/blue] "
            ret += "[white]│[/white]\n"
        ret += "[white]╰" + "─" * (board.n_cols * 2 + 1) + "╯\n"
        self.console.print(ret.strip())

    def print_moves(self, moves: list[Move]) -> None:
        ret = "Solution:\n"
        for move in moves:
            loc, direction = move
            row, col = loc
            direction_color = self.direction_to_color(direction)
            ret += (
                f"[white]• [reset]([white]{row}[reset], [white]{col}[reset]) [white]→ [{direction_color}]{direction}\n"
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
