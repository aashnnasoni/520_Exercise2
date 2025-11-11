"""Solution variant for Problem 2 — Claude prompt 1."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the Claude-prompt-1 solution here."""
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return (a * b) // gcd(a, b)

    n, a, b, p, q = map(int, input_data.split())

    # Count tiles for each category
    count_a = n // a
    count_b = n // b
    count_both = n // lcm(a, b)

    # Strategy: 
    # - Paint tiles divisible only by a with Red (p chocolates each)
    # - Paint tiles divisible only by b with Blue (q chocolates each)
    # - Paint tiles divisible by both with the color giving more chocolates

    # Calculate maximum chocolates
    if p >= q:
        # Paint all 'a' tiles red, and remaining 'b' tiles blue
        total = count_a * p + (count_b - count_both) * q
    else:
        # Paint all 'b' tiles blue, and remaining 'a' tiles red
        total = count_b * q + (count_a - count_both) * p

    
    return str(total)
