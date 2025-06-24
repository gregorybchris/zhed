from dataclasses import dataclass
from typing import Iterator

from zhed.models import Board, Direction, Edit, Loc, Move, Moves, Tile


@dataclass
class Solver:
    @classmethod
    def solve(cls, board: Board) -> Iterator[Moves]:
        return cls.solve_rec(board, [])

    @classmethod
    def solve_rec(cls, board: Board, moves: list[Move]) -> Iterator[Moves]:
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
        max_offset = value
        while offset <= max_offset:
            offset_loc = cls.translate(loc, direction, offset)
            if not board.in_bounds(offset_loc):
                break

            offset_value = board.get(offset_loc)
            match offset_value:
                case Tile.Empty:
                    board.set(offset_loc, Tile.Blank)
                    edits.append((offset_loc, Tile.Empty))
                case Tile.Blank:
                    max_offset += 1
                case Tile.Goal:
                    has_won = True
                case _:
                    max_offset += 1

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
