from __future__ import annotations

import pytest

from solutions.Problem_4.gpt_prompt_1 import solve as gpt1
from solutions.Problem_4.gpt_prompt_2 import solve as gpt2
from solutions.Problem_4.claude_prompt_1 import solve as claude1
from solutions.Problem_4.claude_prompt_2 import solve as claude2


def parse_order(out: str):
    if out.strip() == "-1":
        return -1, []
    lines = out.strip().splitlines()
    cnt = int(lines[0])
    order = list(map(int, lines[1].split())) if len(lines) > 1 else []
    return cnt, order


def is_topological(order, prereq_map):
    pos = {v: i for i, v in enumerate(order)}
    for u, deps in prereq_map.items():
        for d in deps:
            if d not in pos or u not in pos:
                return False
            if pos[d] > pos[u]:
                return False
    return True


@pytest.mark.parametrize(
    "solver",
    [gpt1, gpt2, claude1, claude2],
    ids=["gpt1", "gpt2", "claude1", "claude2"],
)
def test_problem_04_cycle_detection(solver):
    # 2-node cycle: 1->2, 2->1; main is 1
    inp = """2 1
1
1 2
1 1
"""
    out = solver(inp)
    assert out.strip() == "-1"


@pytest.mark.parametrize(
    "solver",
    [gpt1, gpt2, claude1, claude2],
    ids=["gpt1", "gpt2", "claude1", "claude2"],
)
def test_problem_04_simple_chain(solver):
    # 1 <- 2 <- 3, main=3; expected needed {1,2,3} in topological order
    inp = """3 1
3
0
1 1
1 2
"""
    out = solver(inp)
    cnt, order = parse_order(out)
    assert cnt == 3
    prereq = {1: [], 2: [1], 3: [2]}
    assert set(order) == {1, 2, 3}
    assert is_topological(order, prereq)


@pytest.mark.parametrize(
    "solver",
    [gpt1, gpt2, claude1, claude2],
    ids=["gpt1", "gpt2", "claude1", "claude2"],
)
def test_problem_04_only_mains_no_deps(solver):
    # mains: {2,3}, no dependencies; solution should list only those two
    inp = """3 2
2 3
0
0
0
"""
    out = solver(inp)
    cnt, order = parse_order(out)
    assert cnt == 2
    assert set(order) == {2, 3}


@pytest.mark.parametrize(
    "solver",
    [gpt1, gpt2, claude1, claude2],
    ids=["gpt1", "gpt2", "claude1", "claude2"],
)
def test_problem_04_shared_prerequisite(solver):
    # mains: {2,3} both depend on course 1
    # Expected needed {1,2,3} with 1 before 2 and 3
    inp = """3 2
2 3
0
1 1
1 1
"""
    out = solver(inp)
    cnt, order = parse_order(out)
    assert cnt == 3
    prereq = {1: [], 2: [1], 3: [1]}
    assert set(order) == {1, 2, 3}
    assert is_topological(order, prereq)
