import logging
import time
from pathlib import Path
from typing import Annotated, Optional

import yaml
from pydantic import TypeAdapter
from rich.logging import RichHandler
from typer import Argument, Option, Typer

from zhed.models import Level
from zhed.printer import Printer
from zhed.solver import Solver

logger = logging.getLogger(__name__)

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
        printer.print_board(board, number=level.number)
        start_time = time.time()
        for moves in Solver.solve(board):
            elapsed_time = time.time() - start_time
            printer.console.print(f"Level {level.number} solved in {elapsed_time:.2f} seconds.")
            printer.print_moves(moves)
            break


@app.command()
def view(
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

        printer.print_level(level)


def load_levels() -> list[Level]:
    levels_filepath = Path(__file__).parent / "data" / "levels.yaml"
    with levels_filepath.open("r", encoding="utf-8") as fp:
        levels_obj = yaml.safe_load(fp)
        return TypeAdapter(list[Level]).validate_python(levels_obj["levels"])
