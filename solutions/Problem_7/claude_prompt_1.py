"""Solution variant for Problem 7 — Claude prompt 1."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the Claude-prompt-1 solution here."""
    n, k, t = map(int, input_data.split())

    if t <= k:
        return str(t)
    elif t <= n:
        return str(k)
    else:
        return str(n + k - t)



