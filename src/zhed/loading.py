import logging
from pathlib import Path
from typing import Optional

import yaml
from pydantic import TypeAdapter

from zhed.models import Level, Solution

logger = logging.getLogger(__name__)


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
