#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def pct(n: int, d: int) -> float:
    if d == 0:
        return 100.0
    return 100.0 * n / d


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: summarize_coverage.py COVERAGE_JSON [OUTPUT_MD] [RESULTS_JSONL]", file=sys.stderr)
        return 2

    src = Path(argv[1])
    out = Path(argv[2]) if len(argv) > 2 else None
    results_path = Path(argv[3]) if len(argv) > 3 else None

    data = json.loads(src.read_text())
    files = data.get("files", {})

    # Optional results mapping module -> (passed,total)
    results: dict[str, tuple[int, int]] = {}
    if results_path and results_path.exists():
        for line in results_path.read_text().splitlines():
            try:
                rec = json.loads(line)
            except Exception:
                continue
            mod = rec.get("module")
            if not isinstance(mod, str):
                continue
            results[mod] = (int(rec.get("passed", 0)), int(rec.get("total", 0)))

    rows = []
    for path, info in files.items():
        # Only include our solution files (relative or absolute paths)
        norm = path.replace('\\', '/')
        if 'solutions/' not in norm:
            continue
        summary = info.get("summary", {})
        stmts = int(summary.get("num_statements", 0))
        # Coverage.py JSON v7 uses covered_lines or executed_lines
        covered_stmts = int(
            summary.get(
                "covered_lines",
                summary.get("executed_lines", summary.get("covered_statements", 0)),
            )
        )
        num_branches = int(summary.get("num_branches", 0))
        covered_branches = int(summary.get("covered_branches", 0))

        # Prefer percent_covered if provided by coverage.json
        try:
            line_pct = float(summary.get("percent_covered", pct(covered_stmts, stmts)))
        except Exception:
            line_pct = pct(covered_stmts, stmts)
        branch_pct = pct(covered_branches, num_branches)

        # Derive module name for results lookup: solutions/Problem_X/file.py -> solutions.Problem_X.file
        mod = None
        try:
            rel = norm.split('solutions/', 1)[1]
            if rel.endswith('.py'):
                mod = 'solutions.' + rel[:-3].replace('/', '.')
        except Exception:
            mod = None

        passed_total = results.get(mod)
        rows.append((path, stmts, line_pct, num_branches, branch_pct, passed_total))

    rows.sort()

    lines = []
    lines.append("| File | Stmts | Line % | Branches | Branch % | Tests |")
    lines.append("|------|-------:|-------:|---------:|---------:|------:|")
    for path, stmts, line_pct, num_branches, branch_pct, passed_total in rows:
        tests_cell = ""
        if passed_total is not None:
            tests_cell = f"{passed_total[0]}/{passed_total[1]}"
        lines.append(
            f"| {path} | {stmts} | {line_pct:.1f} | {num_branches} | {branch_pct:.1f} | {tests_cell} |",
        )

    out_text = "\n".join(lines) + "\n"
    if out:
        out.write_text(out_text)
    print(out_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
