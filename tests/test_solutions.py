import logging

from zhed.loading import get_solution, load_levels
from zhed.mover import Mover

logger = logging.getLogger(__name__)


class TestSolutions:
    def test_solutions(self) -> None:
        levels = load_levels()

        n_tested = 0
        for level in levels:
            solution = get_solution(level.number)

            if solution is None:
                continue

            board = level.get_board()
            try:
                has_won, _ = Mover.make_moves(board, solution.moves)
            except Exception as exc:
                msg = f"Exception raised when applying solution for level {level.number}: {exc}"
                raise AssertionError(msg) from exc
            assert has_won, f"Solution for level {level.number} did not result in a win"
            n_tested += 1

        logger.info("Tested %d solutions", n_tested)
