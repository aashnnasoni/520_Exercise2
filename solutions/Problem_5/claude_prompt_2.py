"""Solution variant for Problem 5 — Claude prompt 2."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the Claude-prompt-2 solution here."""
  
    a, b, c = map(int, input_data.split())

    if c == 0:
        return "YES" if a == b else "NO"
    else:
        diff = b - a
        if diff % c == 0 and diff // c >= 0:
            return "YES"
        else:
            return "NO"



