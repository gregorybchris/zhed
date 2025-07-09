from typing import Iterator

from zhed.models import Board, Direction, Loc, Move, Tile


def iter_number_locs(board: Board) -> Iterator[Loc]:
    # TODO: Cache number locs to avoid iterating over the entire board
    for row in range(board.n_rows):
        for col in range(board.n_cols):
            loc = (row, col)
            if board.is_number(loc):
                yield loc


def iter_goal_locs(board: Board) -> Iterator[Loc]:
    # TODO: Cache goal locs to avoid iterating over the entire board
    for row in range(board.n_rows):
        for col in range(board.n_cols):
            loc = (row, col)
            if board.get(loc) == Tile.Goal:
                yield loc


def iter_loc_aligned(board: Board, loc: Loc) -> Iterator[Move]:
    r, c = loc
    for row, col in iter_number_locs(board):
        if row == r and col != c:
            direction = Direction.Left if col > c else Direction.Right
            yield ((row, col), direction)
        if col == c and row != r:
            direction = Direction.Up if row > r else Direction.Down
            yield ((row, col), direction)


def iter_path_locs(loc_a: Loc, loc_b: Loc) -> Iterator[Loc]:
    row_a, col_a = loc_a
    row_b, col_b = loc_b

    assert loc_a != loc_b, f"Locs {loc_a} and {loc_b} must be different."
    assert row_a == row_b or col_a == col_b, f"Locs {loc_a} and {loc_b} must be aligned"

    if row_a == row_b:  # Horizontal path
        yield from ((row_a, col) for col in range(min(col_a, col_b), max(col_a, col_b) + 1))
    elif col_a == col_b:  # Vertical path
        yield from ((row, col_a) for row in range(min(row_a, row_b), max(row_a, row_b) + 1))


def iter_path_aligned(board: Board, loc_a: Loc, loc_b: Loc) -> Iterator[tuple[Move, Loc]]:
    row_a, col_a = loc_a
    row_b, col_b = loc_b

    assert loc_a != loc_b, f"Locs {loc_a} and {loc_b} must be different."
    assert row_a == row_b or col_a == col_b, f"Locs {loc_a} and {loc_b} must be aligned"

    if row_a == row_b:  # Horizontal path
        for col in range(min(col_a, col_b) + 1, max(col_a, col_b)):
            for row in range(board.n_rows):
                if row != row_a and board.is_number((row, col)):
                    direction = Direction.Down if row < row_a else Direction.Up
                    yield ((row, col), direction), (row_a, col)

        step = -1 if col_a < col_b else 1
        col = col_a + step
        while 0 <= col < board.n_cols:
            if board.is_number((row_a, col)):
                direction = Direction.Right if col_a < col_b else Direction.Left
                yield ((row_a, col), direction), (row_a, col_b)
            col += step

    elif col_a == col_b:  # Vertical path
        for row in range(min(row_a, row_b) + 1, max(row_a, row_b)):
            for col in range(board.n_cols):
                if col != col_a and board.is_number((row, col)):
                    direction = Direction.Right if col < col_a else Direction.Left
                    yield ((row, col), direction), (row, col_a)

        step = -1 if row_a < row_b else 1
        row = row_a + step
        while 0 <= row < board.n_rows:
            if board.is_number((row, col_a)):
                direction = Direction.Down if row_a < row_b else Direction.Up
                yield ((row, col_a), direction), (row_b, col_a)
            row += step


def translate(loc: Loc, direction: Direction, offset: int) -> Loc:
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


def iter_one_and_rest[T](xs: list[T]) -> Iterator[tuple[T, list[T]]]:
    for i, x in enumerate(xs):
        yield x, xs[:i] + xs[i + 1 :]
