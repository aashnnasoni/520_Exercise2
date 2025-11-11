# 520 Exercise 2 Workspace

This repository is organized to support the Part 1–3 workflow (baseline
coverage, LLM-assisted test authoring, and fault-injection checks).

## Directory layout

- `data/` – cached benchmark payloads from the CodeParrot APPS dataset.
- `solutions/` – one module per problem (`problem_<id>.py`) exposing a
  `solve(input_data: str) -> str` function plus a CLI shim.
- `tests/benchmark/` – the original benchmark-provided tests (organized per
  problem).
- `tests/llm_generated/` – cumulative LLM-authored tests, grouped by
  problem and iteration.
- `scripts/` – helpers for running coverage, generating reports, etc.
- `test_and_execution_script.py` – harness to execute solutions against the
  cached benchmark IO pairs for quick pass/fail counts.

## Typical workflow

1. Drop the APPS subset (e.g., `test_10_examples.json`) into `data/`.
2. Implement each problem inside `solutions/problem_<id>.py`.
3. Run `python test_and_execution_script.py --problem-index N` to verify
   behavior for the Nth cached problem. Use `--solution-module` to compare
   multiple solution modules.
4. Create/organize benchmark tests inside `tests/benchmark/` and additional
   LLM-generated tests inside `tests/llm_generated/` before running
   `coverage.py` for the assignment report.
