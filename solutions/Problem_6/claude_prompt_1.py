"""Solution variant for Problem 6 — Claude prompt 1."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the Claude-prompt-1 solution here."""
    lines = input_data.strip().split()
    cnt1, cnt2, cnt3, cnt4 = map(int, lines[:4])

    total_open = 2 * cnt1 + cnt2 + cnt3
    total_close = cnt2 + cnt3 + 2 * cnt4

    if total_open != total_close:
        return "0"
    elif cnt1 + cnt2 >= cnt3:
        return "1"
    else:
        return "0"



