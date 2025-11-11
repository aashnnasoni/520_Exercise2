"""Utility script to exercise problem solutions against cached benchmarks.

Usage flow for this repository:
1. Implement each problem inside `solutions/problem_<id>.py`.
2. Keep the benchmark inputs/outputs in `data/test_10_examples.json`.
3. Run this script to sanity-check how many benchmark tests pass per problem.
"""

from __future__ import annotations

import argparse
import builtins
import io
import json
import math
import sys
from dataclasses import dataclass
from importlib import import_module
import re
from pathlib import Path
from typing import Callable, Iterable, Sequence


DEFAULT_EXAMPLES_PATH = Path(__file__).with_name("data") / "test_10_examples.json"


@dataclass
class SolutionRunner:
    """Callable wrapper for a problem solution module."""

    name: str
    solve: Callable[[str], str]


@dataclass
class ProblemBundle:
    """Container for the per-problem payload pulled from the dataset cache."""

    problem_id: int
    question: str
    input_output_blob: str


def build_solution_runner(module_name: str) -> SolutionRunner:
    """Loads `module_name.solve` and wraps it in a SolutionRunner instance."""
    module = import_module(module_name)
    if not hasattr(module, "solve"):
        raise AttributeError(f"{module_name} is missing a `solve(input_data)` function.")

    solve_fn = getattr(module, "solve")

    if not callable(solve_fn):
        raise TypeError(f"{module_name}.solve must be callable.")

    def wrapped(test_input: str) -> str:
        buffer = io.StringIO(test_input)
        original_input = builtins.input
        original_stdin = sys.stdin

        def fake_input(prompt: str | None = None) -> str:  # pragma: no cover - shim
            line = buffer.readline()
            if line == "":
                raise EOFError("No more input data.")
            return line.rstrip("\n")

        try:
            builtins.input = fake_input
            sys.stdin = buffer
            result = solve_fn(test_input)
        finally:
            builtins.input = original_input
            sys.stdin = original_stdin

        if not isinstance(result, str):
            result = str(result)
        return result.strip()

    return SolutionRunner(name=module_name, solve=wrapped)


def evaluate_runner(
    runner: SolutionRunner,
    inputs: Sequence[str],
    outputs: Sequence[str],
) -> bool:
    """Runs one solution across all test cases and prints a short report."""
    passed = 0

    for idx, (inp, expected) in enumerate(zip(inputs, outputs), 1):
        predicted = runner.solve(inp)
        expected = expected.strip()

        if predicted == expected:
            result = "✅ Passed"
            passed += 1
        else:
            result = "❌ Failed"
            print(f"--- Test {idx} ---")
            print(f"Input: {repr(inp)}")
            print(f"Expected: {repr(expected)}")
            print(f"Got: {repr(predicted)}")

        print(f"Test {idx}: {result}")

    print(f"\nSummary: {passed}/{len(inputs)} test cases passed.\n")
    return passed == len(inputs)


def pass_at_k(n: int, c: int, k: int) -> float:
    """Computes pass@k according to the OpenAI HumanEval definition."""
    if c == 0:
        return 0.0
    if n - c < k:
        return 1.0
    return 1 - math.comb(n - c, k) / math.comb(n, k)


def test_multiple_runners(
    runners: Sequence[SolutionRunner],
    input_output_json: str,
) -> dict[str, float | int]:
    """Runs a batch of solution modules and prints aggregate statistics."""
    data = json.loads(input_output_json)
    inputs = data["inputs"]
    outputs = data["outputs"]

    print(f"Evaluating {len(runners)} solution module(s)...\n")

    results = []
    for idx, runner in enumerate(runners, 1):
        print(f"========== Solution {idx}: {runner.name} ==========")
        passed_all = evaluate_runner(runner, inputs, outputs)
        results.append(passed_all)
        status = "✅ Passed all tests" if passed_all else "❌ Failed some tests"
        print(f"{runner.name}: {status}\n")

    total = len(runners)
    passed = sum(results)
    pass1 = round(pass_at_k(total, passed, 1), 4)
    pass2 = round(pass_at_k(total, passed, 2), 4)

    print(f"\nTotal passing solutions: {passed}/{total}")
    print("\n=== pass@k Results ===")
    print(f"pass@1: {pass1}")
    print(f"pass@2: {pass2}")

    return {"pass@1": pass1, "pass@2": pass2, "passed": passed, "total": total}


def load_problem_bundle(path: Path, index: int) -> ProblemBundle:
    """Returns metadata and IO blob for a single problem index.

    Be tolerant of trailing commas in cached JSON files produced by notebooks.
    """
    if not path.exists():
        raise FileNotFoundError(f"Examples file not found: {path}")

    # Read and sanitize potential trailing commas before strict JSON parse
    text = path.read_text(encoding="utf-8")
    text = re.sub(r",\s*([\]}])", r"\1", text)
    data = json.loads(text)

    try:
        problem_id = data["id"][index]
        question = data["question"][index]
        io_blob = data["input_output"][index]
    except (KeyError, IndexError) as exc:
        raise ValueError(
            f"Problem index {index} is invalid for {path.name}",
        ) from exc

    return ProblemBundle(problem_id=problem_id, question=question, input_output_blob=io_blob)


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute local solution modules against cached benchmark tests.",
    )
    parser.add_argument(
        "--examples-path",
        type=Path,
        default=DEFAULT_EXAMPLES_PATH,
        help="Path to the cached problems JSON.",
    )
    parser.add_argument(
        "--problem-index",
        type=int,
        default=0,
        help="Zero-based index into the cached `input_output` array.",
    )
    parser.add_argument(
        "--solution-module",
        action="append",
        dest="solution_modules",
        help="Fully-qualified module path exposing `solve(input_data)` (repeatable).",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args()
    bundle = load_problem_bundle(args.examples_path, args.problem_index)

    modules = args.solution_modules
    if not modules:
        modules = [f"solutions.problem_{bundle.problem_id}"]

    runners = [build_solution_runner(module) for module in modules]
    test_multiple_runners(runners, bundle.input_output_blob)


if __name__ == "__main__":
    main()
