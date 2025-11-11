"""Solution variant for Problem 4 — Claude prompt 2."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the Claude-prompt-2 solution here."""
    it = iter(input_data.strip().splitlines())
    n, k = map(int, next(it).split())
    main_courses = list(map(int, next(it).split()))

    # Build adjacency list for dependencies
    dependencies = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        line = list(map(int, next(it).split()))
        t = line[0]
        if t > 0:
            dependencies[i] = line[1:t+1]

    # States: 0 = unvisited, 1 = visiting, 2 = visited
    state = [0] * (n + 1)
    result = []

    def dfs(course):
        if state[course] == 1:  # Cycle detected
            return False
        
        if state[course] == 2:  # Already processed
            return True
        
        state[course] = 1  # Mark as visiting
        
        # Visit all dependencies first
        for prereq in dependencies[course]:
            if not dfs(prereq):
                return False
        
        state[course] = 2  # Mark as visited
        result.append(course)
        return True

    # Start DFS from all main courses
    has_cycle = False
    for main in main_courses:
        if state[main] == 0:
            if not dfs(main):
                has_cycle = True
                break

    if has_cycle:
        return "-1"
    else:
        return f"{len(result)}\n" + " ".join(map(str, result))



