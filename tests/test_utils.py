from zhed import utils
from zhed.models import Board, Direction


class TestUtils:
    def test_translate(self) -> None:
        loc = (2, 2)
        assert utils.translate(loc, Direction.Up, 1) == (1, 2)
        assert utils.translate(loc, Direction.Down, 1) == (3, 2)
        assert utils.translate(loc, Direction.Left, 1) == (2, 1)
        assert utils.translate(loc, Direction.Right, 1) == (2, 3)

    def test_iter_number_locs(self, board_5: Board) -> None:
        number_locs = list(utils.iter_number_locs(board_5))
        assert number_locs == [(2, 3), (4, 1), (5, 2), (5, 4)]

        empty_board = Board.new(8, 8)
        assert list(utils.iter_number_locs(empty_board)) == []

    def test_iter_goal_locs(self, board_5: Board) -> None:
        goal_locs = list(utils.iter_goal_locs(board_5))
        assert goal_locs == [(2, 6)]

        empty_board = Board.new(8, 8)
        assert list(utils.iter_goal_locs(empty_board)) == []

    def test_iter_loc_aligned(self, board_5: Board) -> None:
        assert list(utils.iter_loc_aligned(board_5, (2, 6))) == [((2, 3), Direction.Right)]
        assert list(utils.iter_loc_aligned(board_5, (4, 2))) == [
            ((4, 1), Direction.Right),
            ((5, 2), Direction.Up),
        ]

    def test_iter_path_locs(self) -> None:
        assert list(utils.iter_path_locs((2, 3), (2, 6))) == [(2, 3), (2, 4), (2, 5), (2, 6)]
        assert list(utils.iter_path_locs((4, 4), (4, 1))) == [(4, 1), (4, 2), (4, 3), (4, 4)]
        assert list(utils.iter_path_locs((5, 5), (1, 5))) == [(1, 5), (2, 5), (3, 5), (4, 5), (5, 5)]

    def test_iter_path_aligned_yields_locs_perpendicular_to_path(self, board_10: Board) -> None:
        loc_a = (4, 2)
        loc_b = (4, 5)
        path_aligned = list(utils.iter_path_aligned(board_10, loc_a, loc_b))
        assert path_aligned == [
            (((1, 3), Direction.Down), (4, 3)),
            (((2, 4), Direction.Down), (4, 4)),
        ]

    def test_iter_path_aligned_yields_locs_before_in_line(self, board_10: Board) -> None:
        loc_a = (5, 5)
        loc_b = (7, 5)
        path_aligned = list(utils.iter_path_aligned(board_10, loc_a, loc_b))
        assert path_aligned == [
            (((2, 5), Direction.Down), (7, 5)),
        ]

    def test_iter_one_and_rest(self) -> None:
        xs = [1, 2, 3, 4]
        one_and_rest = list(utils.iter_one_and_rest(xs))
        assert one_and_rest == [
            (1, [2, 3, 4]),
            (2, [1, 3, 4]),
            (3, [1, 2, 4]),
            (4, [1, 2, 3]),
        ]
        assert list(utils.iter_one_and_rest([])) == []
