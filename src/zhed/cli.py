import logging
import time
from pathlib import Path
from typing import Annotated

import yaml
from pydantic import TypeAdapter
from typer import Option, Typer

from zhed.logging_utils import init_logging
from zhed.models import Level
from zhed.printer import Printer
from zhed.solver import Solver

logger = logging.getLogger(__name__)


app = Typer(pretty_exceptions_enable=False)


@app.command()
def noop() -> None:
    """A no-op command to force a command name."""


@app.command()
def solve(
    *,
    info: Annotated[bool, Option("--info/--no-info")] = False,
    debug: Annotated[bool, Option("--debug/--no-debug")] = False,
) -> None:
    init_logging(info=info, debug=debug)

    printer = Printer.new()

    levels = load_levels()
    for level in levels:
        board = level.get_board()
        printer.print_board(board)
        start_time = time.time()
        for solution in Solver.solve(board):
            elapsed_time = time.time() - start_time
            printer.console.print(f"Level {level.number} solved in {elapsed_time:.2f} seconds.")
            printer.print_solution(solution)
            break


def load_levels() -> list[Level]:
    levels_filepath = Path(__file__).parent / "levels.yaml"
    with levels_filepath.open("r", encoding="utf-8") as fp:
        levels_obj = yaml.safe_load(fp)
        return TypeAdapter(list[Level]).validate_python(levels_obj["levels"])
