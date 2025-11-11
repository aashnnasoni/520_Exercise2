from __future__ import annotations

import pytest

from solutions.problem_10 import solve
from tests.conftest import load_apps_entry


def _cases():
    # In the current cached file, this problem is id=1
    data = load_apps_entry(1)
    return list(zip(data["inputs"], data["outputs"]))


@pytest.mark.parametrize("inp,expected", _cases())
def test_problem_10(inp: str, expected: str):
    assert solve(inp) == expected.strip()
