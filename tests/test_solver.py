import re

import pytest

from zhed.models import Board, Direction, Tile
from zhed.solver import Solver


class TestSolver:
    def test_make_move(self, board_5: Board) -> None:
        move_1 = ((5, 2), Direction.Up)
        has_won_1, edits_1 = Solver.make_move(board_5, move_1)
        assert not has_won_1
        assert edits_1 == [((5, 2), 1), ((4, 2), Tile.Empty)]
        assert board_5.get((5, 2)) == Tile.Blank
        assert board_5.get((4, 2)) == Tile.Blank
        assert board_5.get((3, 2)) == Tile.Empty

        move_2 = ((4, 1), Direction.Right)
        has_won_2, edits_2 = Solver.make_move(board_5, move_2)
        assert not has_won_2
        assert edits_2 == [((4, 1), 2), ((4, 3), Tile.Empty), ((4, 4), Tile.Empty)]
        assert board_5.get((4, 1)) == Tile.Blank
        assert board_5.get((4, 2)) == Tile.Blank
        assert board_5.get((4, 3)) == Tile.Blank
        assert board_5.get((4, 4)) == Tile.Blank
        assert board_5.get((4, 5)) == Tile.Empty

    def test_make_moves(self, board_5: Board) -> None:
        moves = [((5, 2), Direction.Up), ((4, 1), Direction.Right)]
        has_won, edits = Solver.make_moves(board_5, moves)
        assert not has_won
        assert edits == [
            ((5, 2), 1),
            ((4, 2), Tile.Empty),
            ((4, 1), 2),
            ((4, 3), Tile.Empty),
            ((4, 4), Tile.Empty),
        ]
        assert board_5.get((5, 2)) == Tile.Blank
        assert board_5.get((4, 1)) == Tile.Blank
        assert board_5.get((4, 2)) == Tile.Blank
        assert board_5.get((4, 3)) == Tile.Blank
        assert board_5.get((4, 4)) == Tile.Blank
        assert board_5.get((4, 5)) == Tile.Empty

    def test_make_move_raises_on_non_number(self, board_5: Board) -> None:
        move = ((0, 0), Direction.Up)
        with pytest.raises(AssertionError, match=re.escape("Cannot move from (0, 0) which is not a number tile.")):
            Solver.make_move(board_5, move)

    def test_undo_edits(self, board_5: Board) -> None:
        move_1 = ((5, 2), Direction.Up)
        _, edits_1 = Solver.make_move(board_5, move_1)

        move_2 = ((4, 1), Direction.Right)
        _, edits_2 = Solver.make_move(board_5, move_2)

        Solver.undo_edits(board_5, edits_2)
        assert board_5.get((4, 1)) == 2
        assert board_5.get((4, 2)) == Tile.Blank
        assert board_5.get((4, 3)) == Tile.Empty
        assert board_5.get((4, 4)) == Tile.Empty
        assert board_5.get((4, 5)) == Tile.Empty

        Solver.undo_edits(board_5, edits_1)
        assert board_5.get((5, 2)) == 1
        assert board_5.get((4, 2)) == Tile.Empty
        assert board_5.get((3, 2)) == Tile.Empty
        assert board_5.get((2, 2)) == Tile.Empty

    def test_solve(self, board_5: Board) -> None:
        solutions = list(Solver.solve(board_5))
        assert len(solutions) == 1
        assert solutions[0] == [
            ((5, 2), Direction.Up),
            ((4, 1), Direction.Right),
            ((5, 4), Direction.Up),
            ((2, 3), Direction.Right),
        ]
