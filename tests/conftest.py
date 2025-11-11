from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Any


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "test_10_examples.json"


def _read_payload() -> dict:
    """Reads the cached JSON, tolerating trailing commas if present."""
    text = DATA_PATH.read_text(encoding="utf-8")
    # Strip trailing commas before ] or } which break strict JSON
    text = re.sub(r",\s*([\]}])", r"\1", text)
    return json.loads(text)


def load_apps_entry(problem_id: int) -> Dict[str, Any]:
    payload = _read_payload()
    ids = payload.get("id", [])

    # Prefer exact id match; otherwise treat as 1-based index if in range
    idx = None
    if problem_id in ids:
        idx = ids.index(problem_id)
    elif 1 <= problem_id <= len(ids):
        idx = problem_id - 1
    else:
        raise AssertionError(
            f"Problem id/index {problem_id} not found in {DATA_PATH} (have ids: {ids}).",
        )

    io_blob = payload["input_output"][idx]
    return json.loads(io_blob)
