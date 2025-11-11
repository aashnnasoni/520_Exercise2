"""Solution variant for Problem 3 — Claude prompt 2."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the Claude-prompt-2 solution here."""

    lines = input_data.strip().splitlines()
    if len(lines) < 2:
        raise ValueError("Expected two input lines: n and string of trophies.")
    n = int(lines[0])
    s = lines[1].strip()
    
    total_gold = s.count('G')
    
    # Edge cases
    if total_gold == 0:
        return 0
    if total_gold == n:
        return str(n)

    max_length = 0
    
    # Try all possible positions to place consecutive G's
    # Consider segments separated by at most 1 'S'
    
    i = 0
    while i < n:
        if s[i] == 'G':
            # Count first segment of G's
            first_count = 0
            while i < n and s[i] == 'G':
                first_count += 1
                i += 1
            
            # Check if there's exactly one 'S' after
            if i < n and s[i] == 'S':
                j = i + 1
                # Count second segment of G's
                second_count = 0
                while j < n and s[j] == 'G':
                    second_count += 1
                    j += 1
                
                if second_count > 0:
                    # Can potentially merge
                    merged = first_count + second_count
                    # Add 1 if there's a spare G outside these segments
                    if total_gold > merged:
                        merged += 1
                    max_length = max(max_length, merged)
                
                # Also consider just extending first segment
                if total_gold > first_count:
                    max_length = max(max_length, first_count + 1)
            else:
                # No 'S' after or end of string
                if total_gold > first_count:
                    max_length = max(max_length, first_count + 1)
                else:
                    max_length = max(max_length, first_count)
        else:
            i += 1

    return str(max_length)

