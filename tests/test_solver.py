import pytest

from zhed.models import Board, Direction, Tile
from zhed.solver import Solver


@pytest.fixture(name="board")
def board_fixture() -> Board:
    """
    ╭─────────────────╮
    │ Level 5         │
    ├─────────────────┤
    │ □ □ □ □ □ □ □ □ │
    │ □ □ □ □ □ □ □ □ │
    │ □ □ □ 2 □ □ ◎ □ │
    │ □ □ □ □ □ □ □ □ │
    │ □ 2 □ □ □ □ □ □ │
    │ □ □ 1 □ 2 □ □ □ │
    │ □ □ □ □ □ □ □ □ │
    │ □ □ □ □ □ □ □ □ │
    ╰─────────────────╯
    """
    board = Board.new(8, 8)
    board.set((2, 3), 2)
    board.set((4, 1), 2)
    board.set((5, 2), 1)
    board.set((5, 4), 2)
    board.set((2, 6), Tile.Goal)
    return board


class TestSolver:
    def test_translate(self) -> None:
        loc = (2, 2)
        assert Solver.translate(loc, Direction.Up, 1) == (1, 2)
        assert Solver.translate(loc, Direction.Down, 1) == (3, 2)
        assert Solver.translate(loc, Direction.Left, 1) == (2, 1)
        assert Solver.translate(loc, Direction.Right, 1) == (2, 3)

    def test_make_move(self, board: Board) -> None:
        move_1 = ((5, 2), Direction.Up)
        has_won_1, edits_1 = Solver.make_move(board, move_1)
        assert not has_won_1
        assert edits_1 == [((5, 2), 1), ((4, 2), Tile.Empty)]
        assert board.get((5, 2)) == Tile.Blank
        assert board.get((4, 2)) == Tile.Blank
        assert board.get((3, 2)) == Tile.Empty

        move_2 = ((4, 1), Direction.Right)
        has_won_2, edits_2 = Solver.make_move(board, move_2)
        assert not has_won_2
        assert edits_2 == [((4, 1), 2), ((4, 3), Tile.Empty), ((4, 4), Tile.Empty)]
        assert board.get((4, 1)) == Tile.Blank
        assert board.get((4, 2)) == Tile.Blank
        assert board.get((4, 3)) == Tile.Blank
        assert board.get((4, 4)) == Tile.Blank
        assert board.get((4, 5)) == Tile.Empty

    def test_make_moves(self, board: Board) -> None:
        moves = [((5, 2), Direction.Up), ((4, 1), Direction.Right)]
        has_won, edits = Solver.make_moves(board, moves)
        assert not has_won
        assert edits == [
            ((5, 2), 1),
            ((4, 2), Tile.Empty),
            ((4, 1), 2),
            ((4, 3), Tile.Empty),
            ((4, 4), Tile.Empty),
        ]
        assert board.get((5, 2)) == Tile.Blank
        assert board.get((4, 1)) == Tile.Blank
        assert board.get((4, 2)) == Tile.Blank
        assert board.get((4, 3)) == Tile.Blank
        assert board.get((4, 4)) == Tile.Blank
        assert board.get((4, 5)) == Tile.Empty

    def test_undo_edits(self, board: Board) -> None:
        move_1 = ((5, 2), Direction.Up)
        _, edits_1 = Solver.make_move(board, move_1)

        move_2 = ((4, 1), Direction.Right)
        _, edits_2 = Solver.make_move(board, move_2)

        Solver.undo_edits(board, edits_2)
        assert board.get((4, 1)) == 2
        assert board.get((4, 2)) == Tile.Blank
        assert board.get((4, 3)) == Tile.Empty
        assert board.get((4, 4)) == Tile.Empty
        assert board.get((4, 5)) == Tile.Empty

        Solver.undo_edits(board, edits_1)
        assert board.get((5, 2)) == 1
        assert board.get((4, 2)) == Tile.Empty
        assert board.get((3, 2)) == Tile.Empty
        assert board.get((2, 2)) == Tile.Empty

    def test_iter_number_locs(self, board: Board) -> None:
        number_locs = list(Solver.iter_number_locs(board))
        assert number_locs == [(2, 3), (4, 1), (5, 2), (5, 4)]

        empty_board = Board.new(8, 8)
        assert list(Solver.iter_number_locs(empty_board)) == []

    def test_iter_goal_locs(self, board: Board) -> None:
        goal_locs = list(Solver.iter_goal_locs(board))
        assert goal_locs == [(2, 6)]

        empty_board = Board.new(8, 8)
        assert list(Solver.iter_goal_locs(empty_board)) == []

    def test_iter_aligned_locs(self, board: Board) -> None:
        assert list(Solver.iter_aligned_locs(board, (2, 6))) == [(2, 3)]
        assert list(Solver.iter_aligned_locs(board, (4, 2))) == [(4, 1), (5, 2)]

    def test_iter_path_locs(self) -> None:
        assert list(Solver.iter_path_locs((2, 3), (2, 6))) == [(2, 3), (2, 4), (2, 5), (2, 6)]
        assert list(Solver.iter_path_locs((4, 4), (4, 1))) == [(4, 1), (4, 2), (4, 3), (4, 4)]
        assert list(Solver.iter_path_locs((5, 5), (1, 5))) == [(1, 5), (2, 5), (3, 5), (4, 5), (5, 5)]
