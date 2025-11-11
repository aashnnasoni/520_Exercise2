from __future__ import annotations

import pytest

from solutions.problem_11 import solve
from tests.conftest import load_apps_entry


def _cases():
    # In the current cached file, this problem is id=2
    data = load_apps_entry(2)
    return list(zip(data["inputs"], data["outputs"]))


@pytest.mark.parametrize("inp,expected", _cases())
def test_problem_11(inp: str, expected: str):
    assert solve(inp) == expected.strip()
