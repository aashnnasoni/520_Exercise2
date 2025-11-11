"""Solution variant for Problem 5 — Claude prompt 1."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the Claude-prompt-1 solution here."""
    a, b, c = map(int, input_data.split())

    if c == 0:
        return "YES" if a == b else "NO"
    else:
        if (b - a) % c == 0:
            i = (b - a) // c + 1
            return "YES" if i > 0 else "NO"
        else:
            return "NO"


