"""Solution variant for Problem 6 — GPT prompt 2."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the GPT-prompt-2 solution here."""

    data = input_data.strip().split()
    if len(data) < 4:
        raise ValueError("Expected four integers.")
    cnt1, cnt2, cnt3, cnt4 = map(int, data[:4])

    if cnt1 == cnt4 and (cnt3 == 0 or cnt1 > 0):
        return "1"
    else:
        return "0"


