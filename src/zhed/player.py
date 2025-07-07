import curses
import logging
import time

from zhed.models import Board, Direction, Edit, Move, Tile
from zhed.mover import Mover

logger = logging.getLogger(__name__)


def start_curses_cli(  # noqa: PLR0912, PLR0915
    window: curses.window,
    board: Board,
    enable_edits: bool,
) -> tuple[Board, list[Move]]:
    curses.curs_set(0)
    window.nodelay(True)
    window.keypad(True)
    window.timeout(50)

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLUE, -1)  # Numbers
    curses.init_pair(2, curses.COLOR_BLACK, -1)  # Empty tiles
    curses.init_pair(3, curses.COLOR_GREEN, -1)  # Goal tiles
    curses.init_pair(4, curses.COLOR_BLACK, -1)  # Blank tiles
    curses.init_pair(5, curses.COLOR_RED, -1)  # Errors

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

                attr = curses.A_NORMAL
                if value == Tile.Goal:
                    char = "◎"
                    attr = curses.color_pair(3)
                elif value == Tile.Empty:
                    char = "□"
                    attr = curses.color_pair(2)
                elif value == Tile.Blank:
                    char = "■"
                    attr = curses.color_pair(4)
                elif isinstance(value, int):
                    char = str(value)
                    attr = curses.color_pair(1)
                else:
                    char = " "

                if (r, c) == (row, col) and cursor_visible:
                    window.addch(r, 2 * c, " ")
                else:
                    window.addch(r, 2 * c, char, attr)

        prompt = """
Controls:
• Arrow keys: move cursor
• 1-9 keys: set tile to numbers
• g key: set goal tile
• e key: set empty tile
• b key: set blank tile
• w/a/s/d keys: make move
• z/u keys: undo move
• r key: reset board
• q key: quit
"""
        window.addstr(board.n_rows + 2, 0, prompt)

        if error:
            attr = curses.color_pair(5)
            window.addstr(n_rows + 1, 0, f"Error: {error}", attr)

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
            elif key in range(ord("1"), ord("9") + 1) and enable_edits:
                board.set((row, col), key - ord("0"))
            elif key == ord("g") and enable_edits:
                board.set((row, col), Tile.Goal)
            elif key == ord("e") and enable_edits:
                board.set((row, col), Tile.Empty)
            elif key == ord("b") and enable_edits:
                board.set((row, col), Tile.Blank)
            # Making moves on board
            elif key in (ord("w"), ord("a"), ord("s"), ord("d")):
                direction = key_to_direction(key)
                move = ((row, col), direction)
                has_won, edits = Mover.make_move(board, move)
                moves.append(move)
                edit_history.append(edits)
                if has_won:
                    break
            elif key in (ord("z"), ord("u")) and len(moves) > 0:
                edits = edit_history.pop()
                moves.pop()
                Mover.undo_edits(board, edits)
            elif key == ord("r"):
                for edits in reversed(edit_history):
                    Mover.undo_edits(board, edits)
                edit_history = []
                moves = []
        except Exception as exc:  # noqa: BLE001
            error = str(exc)
        else:
            if key != -1:
                error = ""

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


def play_cli(board: Board, *, enable_edits: bool) -> tuple[Board, list[Move]]:
    def curses_func(window: curses.window) -> tuple[Board, list[Move]]:
        return start_curses_cli(window, board, enable_edits)

    return curses.wrapper(curses_func)
