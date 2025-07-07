import curses
import time

from zhed.models import Board, Direction, Edit, Move, Tile
from zhed.mover import Mover


def start_curses_cli(window: curses.window, board: Board) -> tuple[Board, list[Move]]:  # noqa: PLR0912, PLR0915
    curses.curs_set(0)
    window.nodelay(True)
    window.keypad(True)

    cursor_toggle_time = time.time()
    cursor_visible = True
    cursor_toggle_delay = 0.3

    n_rows = board.n_rows
    n_cols = board.n_cols

    row = 0
    col = 0

    edit_history: list[list[Edit]] = []
    moves: list[Move] = []
    error = ""

    while True:
        window.clear()

        for r in range(n_rows):
            for c in range(n_cols):
                value = board.get((r, c))

                if (r, c) == (row, col) and cursor_visible:
                    char = " "
                elif value == Tile.Empty:
                    char = "."
                elif value == Tile.Blank:
                    char = "■"
                elif value == Tile.Goal:
                    char = "◎"
                else:
                    char = str(value)
                window.addch(r, 2 * c, char)

        window.addstr(n_rows + 1, 0, "Use arrow keys to move cursor. 1-9 to set numbers. g: goal, e: empty, b: blank.")

        if error:
            window.addstr(n_rows + 2, 0, f"Error: {error}")

        current_time = time.time()
        if current_time - cursor_toggle_time > cursor_toggle_delay:
            cursor_visible = not cursor_visible
            cursor_toggle_time = current_time

        key = window.getch()

        try:
            if key == ord("q"):
                break
            # Moving cursor around board
            if key == curses.KEY_UP:
                row = max(0, row - 1)
            elif key == curses.KEY_DOWN:
                row = min(n_rows - 1, row + 1)
            elif key == curses.KEY_LEFT:
                col = max(0, col - 1)
            elif key == curses.KEY_RIGHT:
                col = min(n_cols - 1, col + 1)
            # Setting tiles on board
            elif key in range(ord("1"), ord("9") + 1):
                board.set((row, col), key - ord("0"))
            elif key == ord("g"):
                board.set((row, col), Tile.Goal)
            elif key == ord("e"):
                board.set((row, col), Tile.Empty)
            elif key == ord("b"):
                board.set((row, col), Tile.Blank)
            # Making moves on board
            elif key in (ord("w"), ord("a"), ord("s"), ord("d")):
                direction = key_to_direction(key)
                move = ((row, col), direction)
                moves.append(move)
                has_won, edits = Mover.make_move(board, move)
                edit_history.append(edits)
                if has_won:
                    break
            elif key == ord("u") and len(edit_history) > 0:
                edits = edit_history.pop()
                moves.pop()
                Mover.undo_edits(board, edits)
        except Exception as exc:  # noqa: BLE001
            error = str(exc)

        window.refresh()

    return board, moves


def key_to_direction(key: int) -> Direction:
    if key == ord("w"):
        return Direction.Up
    if key == ord("a"):
        return Direction.Left
    if key == ord("s"):
        return Direction.Down
    if key == ord("d"):
        return Direction.Right

    msg = f"Invalid key for direction: {key}"
    raise ValueError(msg)


def play_cli(board: Board) -> tuple[Board, list[Move]]:
    def curses_func(window: curses.window) -> tuple[Board, list[Move]]:
        return start_curses_cli(window, board)

    return curses.wrapper(curses_func)
