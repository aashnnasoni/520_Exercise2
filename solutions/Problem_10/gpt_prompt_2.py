"""Solution variant for Problem 10 — GPT prompt 2."""

from __future__ import annotations

def solve(input_data: str) -> str:
    """Implement the Claude-prompt-1 solution here."""
    parts = list(map(int, input_data.split()))
    n = parts[0]
    a = parts[1:]
    p1 = a.index(1)
    pn = a.index(n)
    return str(max(p1, pn, n - 1 - p1, n - 1 - pn))



