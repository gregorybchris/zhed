import pytest

from zhed.models import Board, Tile


@pytest.fixture(name="board_5")
def board_5_fixture() -> Board:
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


@pytest.fixture(name="board_10")
def board_10_fixture() -> Board:
    """
    ╭─────────────────╮
    │ Level 10        │
    ├─────────────────┤
    │ □ □ □ □ □ □ □ □ │
    │ □ □ □ 2 □ □ □ □ │
    │ □ □ □ □ 1 2 □ □ │
    │ □ □ □ □ □ □ □ □ │
    │ □ □ 2 □ □ □ □ □ │
    │ □ □ □ □ □ 1 □ □ │
    │ □ □ □ □ □ □ □ □ │
    │ □ □ □ □ □ ◎ □ □ │
    ╰─────────────────╯
    """
    board = Board.new(8, 8)
    board.set((1, 3), 2)
    board.set((2, 4), 1)
    board.set((2, 5), 2)
    board.set((4, 2), 2)
    board.set((5, 5), 1)
    board.set((7, 5), Tile.Goal)
    return board
