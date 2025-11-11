from __future__ import annotations

import pytest

from solutions.Problem_2.gpt_prompt_1 import solve
from tests.conftest import load_apps_entry


def _cases():
    data = load_apps_entry(2)
    return list(zip(data["inputs"], data["outputs"]))


@pytest.mark.parametrize("inp,expected", _cases())
def test_problem_02(inp: str, expected: str):
    try:
        got = solve(inp)
    except NotImplementedError:
        pytest.xfail("Problem 2 solution not implemented")
    assert got == expected.strip()

