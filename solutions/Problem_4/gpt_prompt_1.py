"""Solution variant for Problem 4 — GPT prompt 1."""

from __future__ import annotations


def solve(input_data: str) -> str:
    """Implement the GPT-prompt-1 solution here."""
    import sys
    sys.setrecursionlimit(200000)

    it = iter(input_data.strip().splitlines())
    n, k = map(int, next(it).split())
    main_courses = list(map(int, next(it).split()))

    graph = [[] for _ in range(n + 1)]  # adjacency: dep -> course
    for i in range(1, n + 1):
        data = list(map(int, next(it).split()))
        t, prereqs = data[0], data[1:]
        for pre in prereqs:
            graph[i].append(pre)  # i depends on pre  (edge i -> pre)

    needed = set()
    visited = [0] * (n + 1)
    cycle = [False]

    def dfs(u):
        if visited[u] == 1:  # visiting
            cycle[0] = True
            return
        if visited[u] == 2:
            return
        visited[u] = 1
        for v in graph[u]:
            dfs(v)
        visited[u] = 2
        needed.add(u)

    for course in main_courses:
        dfs(course)

    if cycle[0]:
        return "-1"

    # Build reverse edges (pre -> course) only for needed subset
    rev_graph = [[] for _ in range(n + 1)]
    for u in needed:
        for v in graph[u]:
            if v in needed:
                rev_graph[v].append(u)

    # Topological order via Kahn’s algorithm
    indeg = {x: 0 for x in needed}
    for u in needed:
        for v in rev_graph[u]:
            indeg[v] += 1

    from collections import deque
    q = deque([x for x in needed if indeg[x] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in rev_graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if len(order) != len(needed):
        return "-1"
    else:
        return f"{len(order)}\n" + " ".join(map(str, order))



