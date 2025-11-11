"""Solution variant for Problem 3 — GPT prompt 1."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the GPT-prompt-1 solution here."""
    lines = input_data.strip().splitlines()
    if len(lines) < 2:
        raise ValueError("Expected two input lines: n and string of trophies.")
    n = int(lines[0])
    trophies = lines[1].strip()

    segments = []
    count = 0

    # Step 1: Identify all G-segments
    for ch in trophies:
        if ch == 'G':
            count += 1
        else:
            if count > 0:
                segments.append(count)
                count = 0
    if count > 0:
        segments.append(count)

    total_g = sum(segments)
    if total_g == n:
        return str(n)
    if total_g == 0:
        return "0"

    # Step 2: Max existing segment
    max_beauty = max(segments)

    # Step 3: Try merging across single S
    for i in range(len(trophies)):
        # Find pattern G...S...G
        if trophies[i] == 'S':
            left = 0
            j = i - 1
            while j >= 0 and trophies[j] == 'G':
                left += 1
                j -= 1

            right = 0
            j = i + 1
            while j < n and trophies[j] == 'G':
                right += 1
                j += 1

            merged = left + right
            if merged < total_g:
                merged += 1  # we can bring one more G from somewhere else
            max_beauty = max(max_beauty, merged)

    return str(max_beauty)
