"""Solution variant for Problem 8 — GPT prompt 2."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the GPT-prompt-2 solution here."""
    s = input_data.strip()
    n = len(s)

    # Precompute minimum suffix characters to decide pop timing
    min_suf = ['z'] * (n + 1)
    for i in range(n - 1, -1, -1):
        min_suf[i] = min(s[i], min_suf[i + 1])

    t = []
    u = []

    for i in range(n):
        t.append(s[i])
        # Pop as long as current top ≤ next smallest character ahead
        while t and t[-1] <= min_suf[i + 1]:
            u.append(t.pop())

    return ''.join(u)



