from zhed import utils
from zhed.models import Board, Edit, Move, Tile


class Mover:
    @classmethod
    def make_move(cls, board: Board, move: Move) -> tuple[bool, list[Edit]]:
        loc, direction = move
        value = board.get(loc)
        assert board.is_number(loc), f"Cannot move from {loc} which is not a number tile."

        board.set(loc, Tile.Blank)
        edits = [(loc, value)]
        has_won = False

        offset = 1
        max_offset = value
        while offset <= max_offset:
            offset_loc = utils.translate(loc, direction, offset)
            if not board.in_bounds(offset_loc):
                break

            offset_value = board.get(offset_loc)
            match offset_value:
                case Tile.Empty:
                    board.set(offset_loc, Tile.Blank)
                    edits.append((offset_loc, Tile.Empty))
                case Tile.Blank:
                    max_offset += 1
                case Tile.Goal:
                    has_won = True
                case _:
                    max_offset += 1

            offset += 1
        return has_won, edits

    @classmethod
    def make_moves(cls, board: Board, moves: list[Move]) -> tuple[bool, list[Edit]]:
        edits = []
        has_won = False
        for move in moves:
            move_has_won, move_edits = cls.make_move(board, move)
            edits.extend(move_edits)
            if move_has_won:
                has_won = True
        return has_won, edits

    @classmethod
    def undo_edits(cls, board: Board, edits: list[Edit]) -> None:
        for edit in edits:
            loc, value = edit
            board.set(loc, value)
