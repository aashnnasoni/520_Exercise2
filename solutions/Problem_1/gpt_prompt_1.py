"""Solution variant for Problem 1 — GPT prompt 1."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the GPT-prompt-1 solution here."""
    data = input_data.strip().split()
    if not data:
        raise ValueError("Expected a single integer input.")

    n = int(data[0])
    r = n % 7
    d = n // 7
    min_days = 2 * d + max(0, r - 5)
    max_days = 2 * d + min(r, 2)
    return f"{min_days} {max_days}"


 
