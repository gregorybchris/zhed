from dataclasses import dataclass
from typing import Iterator

from zhed.models import Board, Direction, Edit, Loc, Move, Tile


@dataclass
class Solver:
    @classmethod
    def solve(cls, board: Board) -> Iterator[list[Move]]:
        return cls.solve_rec(board, [])

    @classmethod
    def solve_rec(cls, board: Board, moves: list[Move]) -> Iterator[list[Move]]:
        for loc in cls.iter_number_locs(board):
            for direction in Direction:
                move = (loc, direction)
                has_won, edits = cls.make_move(board, move)
                new_moves = [*moves, move]
                if has_won:
                    yield new_moves
                yield from cls.solve_rec(board, new_moves)
                cls.undo_edits(board, edits)

    @classmethod
    def iter_number_locs(cls, board: Board) -> Iterator[Loc]:
        for row in range(board.n_rows):
            for col in range(board.n_cols):
                loc = (row, col)
                if board.is_number(loc):
                    yield loc

    @classmethod
    def iter_goal_locs(cls, board: Board) -> Iterator[Loc]:
        for row in range(board.n_rows):
            for col in range(board.n_cols):
                loc = (row, col)
                if board.get(loc) == Tile.Goal:
                    yield loc

    @classmethod
    def iter_aligned_locs(cls, board: Board, loc: Loc) -> Iterator[Loc]:
        r, c = loc
        for row, col in cls.iter_number_locs(board):
            # Same row or column, but not the same loc
            if (row == r) != (col == c):
                yield (row, col)

    @classmethod
    def iter_path_locs(cls, loc_a: Loc, loc_b: Loc) -> Iterator[Loc]:
        row_a, col_a = loc_a
        row_b, col_b = loc_b

        assert loc_a != loc_b, f"Locs {loc_a} and {loc_b} must be different."
        assert row_a == row_b or col_a == col_b, f"Locs {loc_a} and {loc_b} must be aligned"

        if row_a == row_b:  # Horizontal path
            yield from ((row_a, col) for col in range(min(col_a, col_b), max(col_a, col_b) + 1))
        elif col_a == col_b:  # Vertical path
            yield from ((row, col_a) for row in range(min(row_a, row_b), max(row_a, row_b) + 1))

    @classmethod
    def iter_path_aligned_locs(cls, board: Board, loc_a: Loc, loc_b: Loc) -> Iterator[Loc]:
        row_a, col_a = loc_a
        row_b, col_b = loc_b

        assert loc_a != loc_b, f"Locs {loc_a} and {loc_b} must be different."
        assert row_a == row_b or col_a == col_b, f"Locs {loc_a} and {loc_b} must be aligned"

        if row_a == row_b:  # Horizontal path
            for col in range(min(col_a, col_b) + 1, max(col_a, col_b)):
                for row in range(board.n_rows):
                    if row != row_a and board.is_number((row, col)):
                        yield (row, col)

            step = -1 if col_a < col_b else 1
            col = col_a + step
            while 0 <= col < board.n_cols:
                if board.is_number((row_a, col)):
                    yield (row_a, col)
                col += step

        elif col_a == col_b:  # Vertical path
            for row in range(min(row_a, row_b) + 1, max(row_a, row_b)):
                for col in range(board.n_cols):
                    if col != col_a and board.is_number((row, col)):
                        yield (row, col)

            step = -1 if row_a < row_b else 1
            row = row_a + step
            while 0 <= row < board.n_rows:
                if board.is_number((row, col_a)):
                    yield (row, col_a)
                row += step

    @classmethod
    def make_move(cls, board: Board, move: Move) -> tuple[bool, list[Edit]]:
        loc, direction = move
        value = board.get(loc)
        assert board.is_number(loc), f"Cannot move from {loc} which is not a number tile."

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
    def make_moves(cls, board: Board, moves: list[Move]) -> tuple[bool, list[Edit]]:
        edits = []
        has_won = False
        for move in moves:
            move_has_won, move_edits = cls.make_move(board, move)
            edits.extend(move_edits)
            if move_has_won:
                has_won = True
        return has_won, edits

    @classmethod
    def undo_edits(cls, board: Board, edits: list[Edit]) -> None:
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
