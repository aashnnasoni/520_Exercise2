"""Solution variant for Problem 6 — Claude prompt 2."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the Claude-prompt-2 solution here."""
    lines = input_data.strip().split()
    cnt1, cnt2, cnt3, cnt4 = map(int, lines[:4])

    # Special case: if no strings at all
    if cnt1 + cnt2 + cnt3 + cnt4 == 0:
        return "1"
    elif cnt1 == 0 and cnt3 > 0:
        # )( cannot be placed without (( before it
        return "0"
    elif cnt4 == 0 and cnt3 > 0:
        # )( cannot be placed without )) after it
        return "0"
    elif 2 * cnt1 + cnt2 + cnt3 != cnt2 + cnt3 + 2 * cnt4:
        # Total balance check
        return "0"
    else:
        return "1"



