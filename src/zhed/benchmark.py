import logging
import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Optional, Union

import rich.box
from rich.console import Console
from rich.live import Live
from rich.table import Table

from zhed.loading import load_levels
from zhed.models import Board
from zhed.solver import Solver

logger = logging.getLogger(__name__)


@dataclass
class SuccessResult:
    elapsed_time: float


@dataclass
class FailureResult:
    error_message: str


class Speed(StrEnum):
    Fast = auto()
    Slow = auto()


Result = Union[SuccessResult, FailureResult]
ResultKey = tuple[int, Speed]


def solve(board: Board, speed: Speed) -> Optional[float]:
    match speed:
        case Speed.Fast:
            solutions = Solver.solve(board)
        case Speed.Slow:
            solutions = Solver.solve_slow(board)

    start_time = time.time()
    first_solution = next(solutions, None)
    elapsed_time = time.time() - start_time

    return elapsed_time if first_solution is not None else None


def result_to_str(result: Result) -> str:
    match result:
        case SuccessResult(elapsed_time):
            return f"{elapsed_time:.5f}s"
        case FailureResult(error_message):
            return error_message


def create_benchmark_table(levels: list[int], results_map: dict[ResultKey, Result]) -> Table:
    table = Table(title="Zhed Solver Benchmark", box=rich.box.SIMPLE)
    table.add_column("Level", justify="center", style="bold")
    table.add_column("Slow Solver", justify="right")
    table.add_column("Fast Solver", justify="right")
    table.add_column("Speedup", justify="right", style="green")

    for level_num in sorted(levels):
        result_fast = results_map.get((level_num, Speed.Fast), FailureResult("..."))
        result_slow = results_map.get((level_num, Speed.Slow), FailureResult("..."))

        fast_display = result_to_str(result_fast)
        slow_display = result_to_str(result_slow)

        speedup_display = ""
        if isinstance(result_slow, SuccessResult) and isinstance(result_fast, SuccessResult):
            if result_fast.elapsed_time == 0:
                speedup_display = "∞x"
            else:
                speedup = result_slow.elapsed_time / result_fast.elapsed_time
                speedup_display = f"{speedup:.1f}x"

        table.add_row(str(level_num), slow_display, fast_display, speedup_display)

    return table


def run_benchmark(
    n_levels: int,
    timeout: int,
    max_workers: int,
    refresh_per_second: int = 10,
) -> None:
    logging.basicConfig(level=logging.INFO)

    console = Console()

    results_map: dict[ResultKey, Result] = {}
    levels = load_levels()
    level_numbers = [level.number for level in levels[:n_levels]]

    with (
        Live(
            create_benchmark_table(level_numbers, results_map),
            console=console,
            refresh_per_second=refresh_per_second,
        ) as live,
        ThreadPoolExecutor(max_workers=max_workers) as executor,
    ):
        future_to_key: dict[Future[Optional[float]], ResultKey] = {}
        for level in levels[:n_levels]:
            for speed in (Speed.Fast, Speed.Slow):
                board = level.get_board()
                future = executor.submit(solve, board, speed)
                future_to_key[future] = (level.number, speed)

        for future in as_completed(future_to_key.keys()):
            key = future_to_key[future]
            try:
                if result := future.result(timeout=timeout):
                    elapsed_time = result
                    results_map[key] = SuccessResult(elapsed_time)
                else:
                    results_map[key] = FailureResult("No solutions")
            except TimeoutError:
                results_map[key] = FailureResult("Timeout")

            live.update(create_benchmark_table(level_numbers, results_map))
