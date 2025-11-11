from __future__ import annotations

import pytest

from solutions.Problem_3.gpt_prompt_1 import solve as gpt1
from solutions.Problem_3.gpt_prompt_2 import solve as gpt2
from solutions.Problem_3.claude_prompt_1 import solve as claude1
from solutions.Problem_3.claude_prompt_2 import solve as claude2


CASES = [
    ("3\nSSS\n", "0"),          # total_gold == 0
    ("1\nS\n", "0"),            # minimal all silver
    ("4\nGGGG\n", "4"),         # total_gold == n
    ("1\nG\n", "1"),            # minimal all gold
    ("10\nGGGSGGGSGG\n", "7"),  # provided sample
    ("3\nGSG\n", "2"),         # merge across single S without spare
    ("5\nGGSGG\n", "4"),        # two segments with one S between, no spare
    ("2\nGS\n", "1"),           # boundary short strings
    ("2\nSG\n", "1"),
    ("3\nGSS\n", "1"),           # trailing S
    ("3\nSSG\n", "1"),           # leading S
    ("4\nGSSG\n", "2"),          # separated by two S, one swap improves to 2
    ("5\nGGSSG\n", "3"),         # separated by two S, one swap improves to 3
]


@pytest.mark.parametrize(
    "solver",
    [gpt1, gpt2, claude1, claude2],
    ids=["gpt1", "gpt2", "claude1", "claude2"],
)
@pytest.mark.parametrize("inp,expected", CASES)
def test_problem_03_extra(solver, inp: str, expected: str):
    assert solver(inp) == expected


@pytest.mark.parametrize(
    "solver",
    [gpt1, gpt2, claude1, claude2],
    ids=["gpt1", "gpt2", "claude1", "claude2"],
)
@pytest.mark.parametrize("bad_inp", ["3\n", "", "\n\n"])  # len(lines) < 2
def test_problem_03_invalid_input_raises(solver, bad_inp: str):
    with pytest.raises(ValueError):
        solver(bad_inp)
