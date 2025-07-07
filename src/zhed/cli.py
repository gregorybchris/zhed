import logging
import time
from pathlib import Path
from typing import Annotated, Optional

import yaml
from pydantic import TypeAdapter
from rich.console import Console
from rich.logging import RichHandler
from typer import Argument, Option, Typer

from zhed.models import Board, Level, Solution
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
    board, moves = play_cli(board)
    printer.print_board(board)
    printer.print_moves(moves)


@app.command()
def play(
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
    board = level.get_board()
    board, moves = play_cli(board)
    printer = Printer.new()
    printer.print_board(board)
    printer.print_moves(moves)


def get_level(level_number: int) -> Optional[Level]:
    levels = load_levels()
    for level in levels:
        if level.number == level_number:
            return level
    return None


def get_solution(level_number: int) -> Optional[Solution]:
    solutions = load_solutions()
    for solution in solutions:
        if solution.number == level_number:
            return solution
    return None


def load_levels() -> list[Level]:
    levels_filepath = Path(__file__).parent / "data" / "levels.yaml"
    with levels_filepath.open("r", encoding="utf-8") as fp:
        levels_obj = yaml.safe_load(fp)
        return TypeAdapter(list[Level]).validate_python(levels_obj["levels"])


def load_solutions() -> list[Solution]:
    solutions_filepath = Path(__file__).parent / "data" / "solutions.yaml"
    with solutions_filepath.open("r", encoding="utf-8") as fp:
        solutions_obj = yaml.safe_load(fp)
        return TypeAdapter(list[Solution]).validate_python(solutions_obj["solutions"])
