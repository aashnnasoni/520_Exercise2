"""Solution variant for Problem 8 — Claude prompt 2."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the Claude-prompt-2 solution here."""
    s = input_data.strip()
    n = len(s)
    
    # Precompute minimum character from each position to the end
    min_suffix = [''] * (n + 1)
    min_suffix[n] = chr(ord('z') + 1)  # Sentinel value larger than any letter
    
    for i in range(n - 1, -1, -1):
        min_suffix[i] = min(s[i], min_suffix[i + 1])
    
    t = []
    u = []
    pos = 0
    
    while pos < n or t:
        # Pop from t to u if:
        # 1. t is not empty AND
        # 2. Either s is exhausted OR top of t <= all remaining chars in s
        while t and (pos >= n or t[-1] <= min_suffix[pos]):
            u.append(t.pop())
        
        # Push from s to t if s is not exhausted
        if pos < n:
            t.append(s[pos])
            pos += 1
    
    return ''.join(u)




