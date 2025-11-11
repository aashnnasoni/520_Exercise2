"""Solution variant for Problem 4 — GPT prompt 2."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the GPT-prompt-2 solution here."""
   
    import sys
    sys.setrecursionlimit(300000)

    it = iter(input_data.strip().splitlines())
    n, k = map(int, next(it).split())
    mains = list(map(int, next(it).split()))

    prereq = [[] for _ in range(n + 1)]
    adj = [[] for _ in range(n + 1)]

    for i in range(1, n + 1):
        data = list(map(int, next(it).split()))
        t, arr = data[0], data[1:]
        prereq[i] = arr
        for p in arr:
            adj[p].append(i)

    # Step 1: find all necessary courses
    need = [0] * (n + 1)
    stack = mains[:]
    for m in mains:
        need[m] = 1

    while stack:
        u = stack.pop()
        for pre in prereq[u]:
            if not need[pre]:
                need[pre] = 1
                stack.append(pre)

    # Step 2: DFS topological sort (no reversal)
    visited = [0] * (n + 1)
    order = []
    cycle = [False]

    def dfs(u):
        visited[u] = 1
        for v in sorted(prereq[u]):  # ensure deterministic order
            if not need[v]:
                continue
            if visited[v] == 0:
                dfs(v)
                if cycle[0]:
                    return
            elif visited[v] == 1:
                cycle[0] = True
                return
        visited[u] = 2
        order.append(u)

    for i in range(1, n + 1):
        if need[i] and not visited[i]:
            dfs(i)
            if cycle[0]:
                return "-1"

    # order already in correct topological direction
    result = [x for x in order if need[x]]
    return f"{len(result)}\n" + " ".join(map(str, result))



