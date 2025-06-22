from dataclasses import dataclass
from typing import Iterator

from zhed.models import Board, Direction, Edit, Loc, Move, Solution, Tile


@dataclass
class Solver:
    @classmethod
    def solve(cls, board: Board) -> Iterator[Solution]:
        return cls.solve_rec(board, [])

    @classmethod
    def solve_rec(cls, board: Board, moves: list[Move]) -> Iterator[Solution]:
        for loc in cls.iter_number_locs(board):
            for direction in Direction:
                move = (loc, direction)
                has_won, edits = cls.make_move(board, move)
                new_moves = [*moves, move]
                if has_won:
                    yield new_moves
                yield from cls.solve_rec(board, new_moves)
                cls.undo_move(board, edits)

    @classmethod
    def iter_number_locs(cls, board: Board) -> Iterator[Loc]:
        for row in range(board.height):
            for col in range(board.width):
                loc = (row, col)
                value = board.get(loc)
                if value not in (Tile.Empty, Tile.Blank, Tile.Goal):
                    yield loc

    @classmethod
    def make_move(cls, board: Board, move: Move) -> tuple[bool, list[Edit]]:
        loc, direction = move
        value = board.get(loc)
        assert value not in (Tile.Empty, Tile.Blank, Tile.Goal)

        board.set(loc, Tile.Blank)
        edits = [(loc, value)]
        has_won = False

        offset = 1
        while offset <= value:
            new_loc = cls.translate(loc, direction, offset)
            if not board.in_bounds(new_loc):
                break

            if board.get(new_loc) == Tile.Empty:
                board.set(new_loc, Tile.Blank)
                edits.append(((new_loc), Tile.Empty))
            elif board.get(new_loc) == Tile.Blank:
                value += 1
            elif board.get(new_loc) == Tile.Goal:
                has_won = True
            else:
                value += 1
            offset += 1
        return has_won, edits

    @classmethod
    def undo_move(cls, board: Board, edits: list[Edit]) -> None:
        for edit in edits:
            loc, value = edit
            board.set(loc, value)

    @classmethod
    def translate(cls, loc: Loc, direction: Direction, offset: int) -> Loc:
        row, col = loc
        match direction:
            case Direction.Up:
                return (row - offset, col)
            case Direction.Down:
                return (row + offset, col)
            case Direction.Left:
                return (row, col - offset)
            case Direction.Right:
                return (row, col + offset)
