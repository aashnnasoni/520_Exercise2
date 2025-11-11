"""Solution variant for Problem 3 — Claude prompt 1."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the Claude-prompt-1 solution here."""
    lines = input_data.strip().splitlines()
    if len(lines) < 2:
        raise ValueError("Expected two input lines: n and string of trophies.")
    n = int(lines[0])
    s = lines[1].strip()

    # Count total golden trophies
    total_gold = s.count('G')

    # If no gold or all gold, no improvement possible
    if total_gold == 0:
        return "0"
    elif total_gold == n:
        return str(n)
    else:
        # Find all segments of consecutive G's
        segments = []
        i = 0
        while i < n:
            if s[i] == 'G':
                start = i
                while i < n and s[i] == 'G':
                    i += 1
                segments.append((start, i - 1, i - start))
            else:
                i += 1
        
        max_length = max(seg[2] for seg in segments) if segments else 0
        
        # Try merging adjacent segments separated by exactly one 'S'
        for i in range(len(segments) - 1):
            seg1 = segments[i]
            seg2 = segments[i + 1]
            
            # Check if separated by exactly one 'S'
            if seg2[0] - seg1[1] == 2:
                # Can merge these two segments
                merged_length = seg1[2] + seg2[2]
                
                # If there's a G outside these segments, we can add 1
                if total_gold > merged_length:
                    merged_length += 1
                
                max_length = max(max_length, merged_length)
        
        # Try extending any segment by 1 (swap an adjacent S with G from elsewhere)
        for seg in segments:
            if total_gold > seg[2]:  # There's a G outside this segment
                max_length = max(max_length, seg[2] + 1)

        return str(max_length)

