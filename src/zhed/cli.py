import logging
import time
from typing import Annotated, Optional

from rich.console import Console
from rich.logging import RichHandler
from typer import Argument, Option, Typer

from zhed.loading import get_level, get_solution, load_levels
from zhed.models import Board
from zhed.player import play_cli
from zhed.printer import Printer
from zhed.solver import Solver

logger = logging.getLogger(__name__)

console = Console()
app = Typer(pretty_exceptions_enable=False)


def init_logging(info: bool = True, debug: bool = False) -> None:
    if debug:
        logging.basicConfig(level=logging.DEBUG, handlers=[RichHandler()])
    elif info:
        logging.basicConfig(level=logging.INFO, handlers=[RichHandler()])
    else:
        logging.basicConfig(level=logging.WARNING, handlers=[RichHandler()])


@app.command()
def noop() -> None:
    """A no-op command to force a command name."""


@app.command()
def solve(
    *,
    level_number: Annotated[Optional[int], Argument()] = None,
    info: Annotated[bool, Option("--info/--no-info")] = False,
    debug: Annotated[bool, Option("--debug/--no-debug")] = False,
) -> None:
    init_logging(info=info, debug=debug)

    printer = Printer.new()

    levels = load_levels()
    for level in levels:
        if level_number is not None and level.number != level_number:
            continue

        board = level.get_board()
        print()
        printer.print_board(board, number=level.number)
        start_time = time.time()
        for moves in Solver.solve(board):
            elapsed_time = time.time() - start_time
            console.print(f"Level {level.number} solved in {elapsed_time:.2f} seconds.")
            printer.print_moves(moves)
            break


@app.command()
def lookup(
    *,
    level_number: Annotated[int, Argument()],
    info: Annotated[bool, Option("--info/--no-info")] = False,
    debug: Annotated[bool, Option("--debug/--no-debug")] = False,
) -> None:
    init_logging(info=info, debug=debug)

    printer = Printer.new()

    solution = get_solution(level_number)
    if solution is None:
        console.print(f"[red]No solution previously found for level {level_number}")
        return

    printer.print_moves(solution.moves)


@app.command()
def view(
    *,
    level_number: Annotated[int, Argument()],
    info: Annotated[bool, Option("--info/--no-info")] = False,
    debug: Annotated[bool, Option("--debug/--no-debug")] = False,
) -> None:
    init_logging(info=info, debug=debug)

    printer = Printer.new()

    level = get_level(level_number)
    if level is None:
        console.print(f"[red]Level {level_number} not found")
        return

    printer.print_level(level)


@app.command()
def edit(
    *,
    n_rows: Annotated[int, Argument()],
    n_cols: Annotated[int, Argument()],
    info: Annotated[bool, Option("--info/--no-info")] = False,
    debug: Annotated[bool, Option("--debug/--no-debug")] = False,
) -> None:
    init_logging(info=info, debug=debug)

    printer = Printer.new()
    board = Board.new(n_rows, n_cols)
    board, moves = play_cli(board, enable_edits=True)
    printer.print_board(board)
    printer.print_moves(moves)


@app.command()
def play(
    *,
    level_number: Annotated[int, Argument()],
    use_yaml: Annotated[bool, Option("--yaml/--no-yaml")] = False,
    info: Annotated[bool, Option("--info/--no-info")] = False,
    debug: Annotated[bool, Option("--debug/--no-debug")] = False,
) -> None:
    init_logging(info=info, debug=debug)

    printer = Printer.new()

    level = get_level(level_number)
    if level is None:
        console.print(f"[red]Level {level_number} not found")
        return

    printer.print_level(level)
    board = level.get_board()
    board, moves = play_cli(board, enable_edits=False)
    printer = Printer.new()
    printer.print_board(board)
    if use_yaml:
        printer.print_moves_yaml(moves)
    else:
        printer.print_moves(moves)
