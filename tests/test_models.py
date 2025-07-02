from zhed.models import Board, Tile


class TestBoard:
    def test_new_board(self) -> None:
        board = Board.new(3, 4)
        assert board.n_rows == 3
        assert board.n_cols == 4
        assert all(tile == Tile.Empty for row in board.tiles for tile in row)

    def test_get_set(self) -> None:
        board = Board.new(3, 4)
        loc = (1, 2)
        board.set(loc, Tile.Blank)
        assert board.get(loc) == Tile.Blank

    def test_in_bounds(self) -> None:
        board = Board.new(3, 4)
        assert board.in_bounds((0, 0))
        assert not board.in_bounds((3, 0))
        assert not board.in_bounds((0, 4))
        assert not board.in_bounds((-1, 0))
        assert not board.in_bounds((0, -1))
