"""Solution variant for Problem 2 — Claude prompt 2."""

from __future__ import annotations
import math


def solve(input_data: str) -> str:
    """Implement the Claude-prompt-2 solution here."""


    n, a, b, p, q = map(int, input_data.split())

    # Calculate LCM of a and b
    lcm_ab = (a * b) // math.gcd(a, b)

    # Count tiles divisible by a, b, and both
    tiles_a = n // a
    tiles_b = n // b
    tiles_both = n // lcm_ab

    # Tiles exclusively divisible by a or b
    tiles_only_a = tiles_a - tiles_both
    tiles_only_b = tiles_b - tiles_both

    # Maximum chocolates: 
    # - Paint all "only a" tiles Red
    # - Paint all "only b" tiles Blue
    # - Paint "both" tiles with the color giving more chocolates
    total_chocolates = tiles_only_a * p + tiles_only_b * q + tiles_both * max(p, q)

    return str(total_chocolates)
