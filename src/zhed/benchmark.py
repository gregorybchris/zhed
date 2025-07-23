import logging
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Any, Optional

import rich.box
from rich.console import Console
from rich.live import Live
from rich.table import Table

from zhed.loading import load_levels
from zhed.models import Board
from zhed.solver import Solver

logger = logging.getLogger(__name__)


@dataclass
class Result:
    elapsed_time: Optional[float] = None
    error_message: Optional[str] = None


class Speed(StrEnum):
    Fast = auto()
    Slow = auto()


ResultKey = tuple[int, Speed]


class TimeoutError(Exception):
    pass


def solve(board: Board, speed: Speed, result_container: list[Any]) -> None:
    match speed:
        case Speed.Fast:
            solutions = Solver.solve(board)
        case Speed.Slow:
            solutions = Solver.solve_slow(board)

    start_time = time.time()
    first_solution = next(solutions, None)
    elapsed_time = time.time() - start_time

    if first_solution is not None:
        result_container.append(elapsed_time)
    else:
        result_container.append(None)


def run_solve_thread(board: Board, speed: Speed, timeout: int) -> Optional[float]:
    result_container: list[Any] = []
    thread = threading.Thread(target=solve, args=(board, speed, result_container))
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        msg = "Operation timed out"
        raise TimeoutError(msg)

    if len(result_container) == 0:
        msg = "Thread completed but no result available"
        raise RuntimeError(msg)

    return result_container[0]


def result_to_str(result: Result) -> str:
    if result.elapsed_time is not None:
        return f"{result.elapsed_time:.6f}"
    if result.error_message is not None:
        return result.error_message
    msg = f"Unexpected result: {result!r}"
    raise ValueError(msg)


def create_benchmark_table(levels: list[int], results_map: dict[ResultKey, Result]) -> Table:
    table = Table(title="Zhed Solver Benchmark", box=rich.box.SIMPLE)
    table.add_column("Level", justify="center", style="bold")
    table.add_column("Slow Solver (s)", justify="right")
    table.add_column("Fast Solver (s)", justify="right")
    table.add_column("Speedup", justify="right", style="green")

    for level_num in sorted(levels):
        result_fast = results_map.get((level_num, Speed.Fast), Result(error_message="..."))
        result_slow = results_map.get((level_num, Speed.Slow), Result(error_message="..."))

        fast_display = result_to_str(result_fast)
        slow_display = result_to_str(result_slow)

        speedup_display = ""
        if result_slow.elapsed_time is not None and result_fast.elapsed_time is not None:
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
                future = executor.submit(run_solve_thread, board, speed, timeout)
                future_to_key[future] = (level.number, speed)

        for future in as_completed(future_to_key.keys()):
            key = future_to_key[future]
            try:
                if result := future.result():
                    elapsed_time = result
                    results_map[key] = Result(elapsed_time=elapsed_time)
                else:
                    results_map[key] = Result(error_message="no solutions")
            except TimeoutError:
                results_map[key] = Result(error_message="timeout")

            live.update(create_benchmark_table(level_numbers, results_map))
