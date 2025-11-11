"""Problem 11 solution placeholder."""

from __future__ import annotations
import math


def solve(input_data: str) -> str:
    """Solve problem 11. Replace with your implementation."""
    
    n, a, b, p, q = map(int, input_data.split())
    lcm_ab = a * b // math.gcd(a, b)
    red_count = n // a
    blue_count = n // b
    overlap = n // lcm_ab
    red_unique = red_count - overlap
    blue_unique = blue_count - overlap
    best_overlap_value = overlap * max(p, q)
    total = red_unique * p + blue_unique * q + best_overlap_value
    return str(total)



