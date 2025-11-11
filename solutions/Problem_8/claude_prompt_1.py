"""Solution variant for Problem 8 — Claude prompt 1."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the Claude-prompt-1 solution here."""
    s = input_data.strip()
    t = ""
    u = ""
    
    while s or t:
        # Determine what character we'd get from each move
        option1 = None  # Move 1: take first char from s, append to t
        option2 = None  # Move 2: take last char from t, append to u
        
        if s:
            option1 = s[0]
        
        if t:
            option2 = t[-1]
        
        # Choose the move that gives us the lexicographically smaller result
        # We want to minimize the next character added to u
        
        if option2 is not None:
            # We can add to u from t
            if option1 is not None:
                # Both moves possible - we need to decide
                # If we can add to u now and it's beneficial, or if waiting is better
                # Greedy: compare what we'd add to u
                
                # Take from t if it's <= the first char of s
                # This ensures u grows with smaller characters when possible
                if option2 <= option1:
                    u += t[-1]
                    t = t[:-1]
                else:
                    t += s[0]
                    s = s[1:]
            else:
                # Only option 2 available
                u += t[-1]
                t = t[:-1]
        else:
            # Can only do move 1
            if s:
                t += s[0]
                s = s[1:]
    
    return u





