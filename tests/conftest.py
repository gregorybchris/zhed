import pytest

from zhed.models import Board, Tile


@pytest.fixture(name="board")
def board_fixture() -> Board:
    """
    ╭─────────────────╮
    | Level 5         |
    ├─────────────────┤
    | □ □ □ □ □ □ □ □ |
    | □ □ □ □ □ □ □ □ |
    | □ □ □ 2 □ □ ◎ □ |
    | □ □ □ □ □ □ □ □ |
    | □ 2 □ □ □ □ □ □ |
    | □ □ 1 □ 2 □ □ □ |
    | □ □ □ □ □ □ □ □ |
    | □ □ □ □ □ □ □ □ |
    ╰─────────────────╯
    """
    board = Board.new(8, 8)
    board.set((2, 3), 2)
    board.set((4, 1), 2)
    board.set((5, 2), 1)
    board.set((5, 4), 2)
    board.set((2, 6), Tile.Goal)
    return board
