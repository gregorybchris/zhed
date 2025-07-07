from zhed.models import Board, Direction
from zhed.solver import Solver


class TestSolver:
    def test_solve(self, board_5: Board) -> None:
        solutions = list(Solver.solve(board_5))
        assert len(solutions) == 1
        assert solutions[0] == [
            ((5, 2), Direction.Up),
            ((4, 1), Direction.Right),
            ((5, 4), Direction.Up),
            ((2, 3), Direction.Right),
        ]
