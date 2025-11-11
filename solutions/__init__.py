"""Helpers for loading individual problem solutions."""

from __future__ import annotations

from importlib import import_module
from types import ModuleType


def load_solution_module(problem_id: int) -> ModuleType:
    """Dynamically imports `solutions.problem_{id}` and returns the module."""
    module_name = f"{__name__}.problem_{problem_id}"
    try:
        module = import_module(module_name)
    except ModuleNotFoundError as exc:  # pragma: no cover - defensive
        raise ModuleNotFoundError(
            f"Solution module {module_name} was not found.",
        ) from exc

    if not hasattr(module, "solve"):
        raise AttributeError(f"{module_name} is missing a `solve` function.")

    return module
