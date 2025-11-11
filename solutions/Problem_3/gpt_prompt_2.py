"""Solution variant for Problem 3 — GPT prompt 2."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the GPT-prompt-2 solution here."""
    lines = input_data.strip().splitlines()
    if len(lines) < 2:
        raise ValueError("Expected two input lines: n and string of trophies.")
    n = int(lines[0])
    trophies = lines[1].strip()

    # Step 1: Count total golden trophies
    total_g = trophies.count('G')

    # Step 2: Handle trivial edge cases
    if total_g == 0:
        return "0"
    if total_g == n:
        return str(n)

    # Step 3: Track maximum possible merged golden segment
    max_beauty = 0

    for i in range(n):
        if trophies[i] == 'S':  # Only check where swap could happen
            # Count Gs to the left
            left = 0
            j = i - 1
            while j >= 0 and trophies[j] == 'G':
                left += 1
                j -= 1

            # Count Gs to the right
            right = 0
            j = i + 1
            while j < n and trophies[j] == 'G':
                right += 1
                j += 1

            merged = left + right
            # We can add one more G if there exists any spare G outside this segment
            if merged < total_g:
                merged += 1
            max_beauty = max(max_beauty, merged)

    # Step 4: Also consider already-existing segments without any swap
    current = 0
    for ch in trophies:
        if ch == 'G':
            current += 1
            max_beauty = max(max_beauty, current)
        else:
            current = 0

  
    return str(max_beauty)
