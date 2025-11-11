"""Solution variant for Problem 1 — GPT prompt 2."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the GPT-prompt-2 solution here."""
    data = input_data.strip().split()
    if not data:
        raise ValueError("Expected one integer input.")
    n = int(data[0])

    # Full weeks and remaining days
    weeks = n // 7
    rem = n % 7

    # Each week contributes exactly 2 days off
    min_off = weeks * 2 + max(0, rem - 5)   # spillover into weekend if >5 leftover days
    max_off = weeks * 2 + min(2, rem)       # at most 2 days off per leftover segment
    return f"{min_off} {max_off}"
