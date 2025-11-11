"""Solution variant for Problem 2 — GPT prompt 2."""

from __future__ import annotations
import math


def solve(input_data: str) -> str:
    """Implement the GPT-prompt-2 solution here."""
    n, a, b, p, q = map(int, input_data.split())

    # Count of multiples of a, b, and their overlap (lcm)
    red_tiles = n // a
    blue_tiles = n // b
    both = n // (a * b // math.gcd(a, b))  # count of tiles divisible by both a and b

    # If red gives more chocolates, color the overlapping ones red; else blue
    if p > q:
        total = red_tiles * p + (blue_tiles - both) * q
    else:
        total = (red_tiles - both) * p + blue_tiles * q


    return str(total)
