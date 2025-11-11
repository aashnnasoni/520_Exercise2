"""Solution variant for Problem 1 — Claude prompt 2."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the Claude-prompt-2 solution here."""
    data = input_data.strip().split()
    if not data:
        raise ValueError("Expected one integer input.")
    n = int(data[0])

    complete_weeks = n // 7
    remaining = n % 7

    min_days_off = complete_weeks * 2 + max(0, remaining - 5)
    max_days_off = complete_weeks * 2 + min(remaining, 2)

    return f"{min_days_off} {max_days_off}"
