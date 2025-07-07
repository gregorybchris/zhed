from dataclasses import dataclass
from typing import Iterator

from zhed import utils
from zhed.models import Board, Direction, Move
from zhed.mover import Mover


@dataclass
class Solver:
    @classmethod
    def solve(cls, board: Board) -> Iterator[list[Move]]:
        return cls.solve_rec(board, [])

    @classmethod
    def solve_rec(cls, board: Board, moves: list[Move]) -> Iterator[list[Move]]:
        for loc in utils.iter_number_locs(board):
            for direction in Direction:
                move = (loc, direction)
                has_won, edits = Mover.make_move(board, move)
                new_moves = [*moves, move]
                if has_won:
                    yield new_moves
                yield from cls.solve_rec(board, new_moves)
                Mover.undo_edits(board, edits)
