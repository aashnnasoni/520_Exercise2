#!/usr/bin/env bash
set -euo pipefail

# Run coverage for all 40 solution variants (10 problems × 4 variants)
# Usage: bash scripts/run_all_coverage.sh [EXAMPLES_PATH]
#   EXAMPLES_PATH defaults to data/test_10_examples.json

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXAMPLES_PATH="${1:-data/test_10_examples.json}"

variants=(gpt_prompt_1 gpt_prompt_2 claude_prompt_1 claude_prompt_2)

cd "$ROOT_DIR"

echo "==> Erasing previous coverage data"
coverage erase || true

RESULTS_JSONL="$ROOT_DIR/run_results.jsonl"
: > "$RESULTS_JSONL"

for pid in {1..10}; do
  idx=$((pid - 1))
  for v in "${variants[@]}"; do
    module="solutions.Problem_${pid}.${v}"
    echo "\n==> Running $module on problem-index $idx"
    # Continue on failure so other variants still run
    tmp_out="$(mktemp -t cov_run_XXXXXX)"
    coverage run \
      --branch \
      --source=solutions \
      --append \
      "$ROOT_DIR/test_and_execution_script.py" \
      --examples-path "$ROOT_DIR/$EXAMPLES_PATH" \
      --problem-index "$idx" \
      --solution-module "$module" \
      >"$tmp_out" 2>&1 || echo "WARN: $module failed (skipping)"

    # Extract pass summary from harness output and append JSONL record
    summary_line="$(grep -E 'Summary: [0-9]+/[0-9]+ test cases passed' "$tmp_out" | tail -n 1 || true)"
    passed=0; total=0
    if [[ -n "$summary_line" ]]; then
      if [[ "$summary_line" =~ Summary:\ ([0-9]+)\/([0-9]+) ]]; then
        passed="${BASH_REMATCH[1]}"; total="${BASH_REMATCH[2]}"
      fi
    fi
    printf '{"module":"%s","problem_index":%d,"passed":%d,"total":%d}\n' "$module" "$idx" "$passed" "$total" >> "$RESULTS_JSONL"
    rm -f "$tmp_out"
  done
done

echo "\n==> Combined coverage (line + branch)"
coverage report -m || true

echo "\n==> Generating HTML report in htmlcov/"
coverage html -d "$ROOT_DIR/htmlcov" || true

echo "\n==> Writing machine-readable JSON and summary with branch %"
coverage json -o "$ROOT_DIR/coverage.json" || true
python3 "$ROOT_DIR/scripts/summarize_coverage.py" "$ROOT_DIR/coverage.json" "$ROOT_DIR/coverage_summary.md" "$RESULTS_JSONL" || true
echo "Summary written to: $ROOT_DIR/coverage_summary.md"
echo "Open: $ROOT_DIR/htmlcov/index.html"
