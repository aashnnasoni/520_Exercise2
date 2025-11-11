"""Solution variant for Problem 9 — GPT prompt 1."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the GPT-prompt-1 solution here."""
    def is_palindrome(h, m):
        s = f"{h:02d}{m:02d}"  # "hhmm"
        return s == s[::-1]

    time_str = input_data.strip()
    hh, mm = map(int, time_str.split(':'))
    minutes_slept = 0

    while True:
        if is_palindrome(hh, mm):
            return minutes_slept

        minutes_slept += 1
        mm += 1
        if mm == 60:
            mm = 0
            hh += 1
            if hh == 24:
                hh = 0



