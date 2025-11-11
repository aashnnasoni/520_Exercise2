"""Solution variant for Problem 5 — GPT prompt 1."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the GPT-prompt-1 solution here."""
    data = input_data.strip().split()
    if not data:
        raise ValueError("Expected three integers.")
    a, b, c = map(int, data)

    if c == 0:
        return "YES" if a == b else "NO"
    else:
        if (b - a) % c == 0 and (b - a) // c >= 0:
            return "YES"
        else:
            return "NO"


