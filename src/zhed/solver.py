from dataclasses import dataclass
from typing import Iterator

from zhed import utils
from zhed.models import Board, Direction, Loc, Move
from zhed.mover import Mover


@dataclass
class Solver:
    @classmethod
    def solve(cls, board: Board) -> Iterator[list[Move]]:
        for goal_loc in utils.iter_goal_locs(board):
            for goal_aligned_move in utils.iter_loc_aligned(board, goal_loc):
                goal_aligned_loc, _ = goal_aligned_move
                yield from cls.solve_rec(
                    board=board,
                    moves=[goal_aligned_move],
                    candidates=[],
                    visited={goal_aligned_loc},
                    loc_a=goal_aligned_loc,
                    loc_b=goal_loc,
                )

    @classmethod
    def solve_rec(  # noqa: PLR0913
        cls,
        *,
        board: Board,
        moves: list[Move],
        candidates: list[tuple[Move, Loc]],
        visited: set[Loc],
        loc_a: Loc,
        loc_b: Loc,
    ) -> Iterator[list[Move]]:
        is_win, edits = Mover.make_moves(board, moves)
        if is_win:
            yield moves
            return
        else:
            Mover.undo_edits(board, edits)

        new_candidates = list(utils.iter_path_aligned(board, loc_a, loc_b))
        for path_aligned_candidate, rest_new_candidates in utils.iter_one_and_rest(new_candidates):
            move, path_loc = path_aligned_candidate
            move_loc, _ = move

            if move_loc in visited:
                continue

            yield from cls.solve_rec(
                board=board,
                moves=[move, *moves],
                candidates=rest_new_candidates + candidates,
                visited=visited | {move_loc},
                loc_a=move_loc,
                loc_b=path_loc,
            )

        for candidate, rest_candidates in utils.iter_one_and_rest(candidates):
            move, path_loc = candidate
            move_loc, _ = move

            if move_loc in visited:
                continue

            yield from cls.solve_rec(
                board=board,
                moves=[move, *moves],
                candidates=rest_candidates,
                visited=visited | {move_loc},
                loc_a=move_loc,
                loc_b=path_loc,
            )

    @classmethod
    def solve_slow(cls, board: Board) -> Iterator[list[Move]]:
        return cls.solve_slow_rec(board, [])

    @classmethod
    def solve_slow_rec(cls, board: Board, moves: list[Move]) -> Iterator[list[Move]]:
        for loc in utils.iter_number_locs(board):
            for direction in Direction:
                move = (loc, direction)
                has_won, edits = Mover.make_move(board, move)
                new_moves = [*moves, move]
                if has_won:
                    yield new_moves
                yield from cls.solve_slow_rec(board, new_moves)
                Mover.undo_edits(board, edits)
