"""Utility script to evaluate solution snippets against local test cases.

This is a cleaned-up version of a former notebook cell. It loads the cached
`test_10_examples.json` file, executes each provided solution against the
selected problem's input/output pairs, and reports pass@k metrics.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable, List, Sequence


DEFAULT_TIMEOUT = 5.0
DEFAULT_EXAMPLES_PATH = Path(__file__).with_name("test_10_examples.json")


def run_code_with_input(code_str: str, test_input: str, timeout: float) -> str:
    """Executes the supplied Python code with the provided stdin payload."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as handle:
        handle.write(code_str)
        code_path = Path(handle.name)

    try:
        result = subprocess.run(
            ["python3", str(code_path)],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return (result.stdout or "").strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as exc:  # pragma: no cover - defensive branch
        return f"ERROR: {exc}"
    finally:
        try:
            code_path.unlink(missing_ok=True)
        except Exception:
            pass


def evaluate_solution(
    code_str: str,
    inputs: Sequence[str],
    outputs: Sequence[str],
    timeout: float,
) -> bool:
    """Runs one solution across all test cases and prints a short report."""
    passed = 0

    for idx, (inp, expected) in enumerate(zip(inputs, outputs), 1):
        predicted = run_code_with_input(code_str, inp, timeout)
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


def test_multiple_solutions(
    solution_codes: Sequence[str],
    input_output_json: str,
    timeout: float,
) -> dict[str, float | int]:
    """Runs a batch of solutions and prints aggregate statistics."""
    data = json.loads(input_output_json)
    inputs = data["inputs"]
    outputs = data["outputs"]

    print(f"Evaluating {len(solution_codes)} generated solutions...\n")

    results = []
    for idx, code in enumerate(solution_codes, 1):
        print(f"========== Solution {idx} ==========")
        passed_all = evaluate_solution(code, inputs, outputs, timeout)
        results.append(passed_all)
        status = "✅ Passed all tests" if passed_all else "❌ Failed some tests"
        print(f"Solution {idx}: {status}\n")

    total = len(solution_codes)
    passed = sum(results)
    pass1 = round(pass_at_k(total, passed, 1), 4)
    pass2 = round(pass_at_k(total, passed, 2), 4)

    print(f"\nTotal passing solutions: {passed}/{total}")
    print("\n=== pass@k Results ===")
    print(f"pass@1: {pass1}")
    print(f"pass@2: {pass2}")

    return {"pass@1": pass1, "pass@2": pass2, "passed": passed, "total": total}


def load_problem_blob(path: Path, index: int) -> str:
    """Returns the raw JSON string containing inputs/outputs for a problem."""
    if not path.exists():
        raise FileNotFoundError(f"Examples file not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    try:
        return data["input_output"][index]
    except (KeyError, IndexError) as exc:
        raise ValueError(
            f"Problem index {index} is invalid for {path.name}",
        ) from exc


def load_solution_codes(path: Path) -> List[str]:
    """Parses a JSON file that contains a list of Python code strings."""
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
        raise ValueError("Solutions file must be a JSON array of strings.")
    return data


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute locally generated solutions against cached tests.",
    )
    parser.add_argument(
        "--examples-path",
        type=Path,
        default=DEFAULT_EXAMPLES_PATH,
        help=f"Path to test examples JSON (default: {DEFAULT_EXAMPLES_PATH.name}).",
    )
    parser.add_argument(
        "--problem-index",
        type=int,
        default=8,
        help="Zero-based index into the `input_output` array.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="Per-test execution timeout in seconds.",
    )
    parser.add_argument(
        "--solutions-json",
        type=Path,
        help="Optional JSON file containing a list of Python solution strings.",
    )
    return parser.parse_args(argv)


SOLUTION_CODES = [
    """def solve_game(s):
    n = len(s)
    min_suffix = [''] * (n + 1)
    min_suffix[n] = chr(ord('z') + 1)

    for i in range(n - 1, -1, -1):
        min_suffix[i] = min(s[i], min_suffix[i + 1])

    t = []
    u = []
    pos = 0

    while pos < n or t:
        while t and (pos >= n or t[-1] <= min_suffix[pos]):
            u.append(t.pop())

        if pos < n:
            t.append(s[pos])
            pos += 1

    return ''.join(u)


if __name__ == '__main__':
    s = input().strip()
    print(solve_game(s))
""",
    """def solve_game(s):
    n = len(s)
    min_suffix = [''] * (n + 1)
    min_suffix[n] = chr(ord('z') + 1)

    for i in range(n - 1, -1, -1):
        min_suffix[i] = min(s[i], min_suffix[i + 1])

    t = []
    u = []
    pos = 0

    while pos < n or t:
        if t and (pos >= n or t[-1] <= min_suffix[pos]):
            u.append(t.pop())
        else:
            t.append(s[pos])
            pos += 1

    return ''.join(u)


if __name__ == '__main__':
    s = input().strip()
    print(solve_game(s))
""",
]


def main() -> None:
    args = parse_args()

    if args.solutions_json:
        solution_codes = load_solution_codes(args.solutions_json)
    else:
        solution_codes = SOLUTION_CODES

    if not solution_codes:
        raise SystemExit("No solution code snippets were provided.")

    problem_blob = load_problem_blob(args.examples_path, args.problem_index)
    test_multiple_solutions(solution_codes, problem_blob, args.timeout)


if __name__ == "__main__":
    main()
