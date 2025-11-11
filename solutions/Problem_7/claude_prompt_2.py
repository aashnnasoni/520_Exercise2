"""Solution variant for Problem 7 — Claude prompt 2."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the Claude-prompt-2 solution here."""
    n, k, t = map(int, input_data.split())

    standing = min(t, k, n + k - t)
    return str(standing)



