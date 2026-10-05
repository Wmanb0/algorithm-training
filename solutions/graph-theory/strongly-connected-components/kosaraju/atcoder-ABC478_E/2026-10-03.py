# @url https://atcoder.jp/contests/abc478/tasks/abc478_e
# @primary kosaraju
# @topics kosaraju, topological-sort, dag-dp
# @note
# Idea: Build the constraint graph and use Kosaraju's algorithm to compute its strongly connected components. Reject if a strict inequality lies inside one component, then build the condensation DAG and process it topologically while propagating d[y] = max(d[y], d[x] + t).
# Key observation: Vertices in the same strongly connected component must receive equal values, so a strict edge inside one component is impossible. After contracting SCCs, the graph is a DAG and each edge requires the destination value to be at least the source value plus t.
# Complexity: O(N + Q) time and O(N + Q) space.
# @endnote

import sys
from collections import deque
input = sys.stdin.readline


def solve():
    n, q = map(int, input().strip().split())
    adj = [[] for _ in range(n)]
    radj = [[] for _ in range(n)]
    op = []

    for _ in range(q):
        t, u, v = map(int, input().strip().split())
        u -= 1
        v -= 1
        adj[u].append(v)
        radj[v].append(u)
        op.append([t, u, v])

    vis = [False] * (n)
    b = []

    def dfs(x):
        vis[x] = True

        for i in adj[x]:
            if not vis[i]:
                dfs(i)

        b.append(x)

    for i in range(n):
        if not vis[i]:
            dfs(i)

    comp = [-1] * n
    cnt = 0

    def dfs2(x):
        comp[x] = cnt

        for i in radj[x]:
            if comp[i] == -1:
                dfs2(i)

    for i in reversed(b):
        if comp[i] == -1:
            dfs2(i)
            cnt += 1

    for t, u, v in op:
        # scc 中有 小于号
        if t == 1 and comp[u] == comp[v]:
            print("No")
            return

    g = [[] for _ in range(cnt)]
    idx = [0] * cnt

    for t, u, v in op:
        x = comp[u]
        y = comp[v]

        if x != y: 
            g[x].append([y, t])
            idx[y] += 1

    d = [1] * cnt
    q = deque()

    for i in range(cnt):
        if idx[i] == 0:
            q.append(i)

    while q:
        x = q.popleft()

        for y, t in g[x]:

            d[y] = max(d[y], d[x] + t) # 如果是 小于 就 加 1

            idx[y] -= 1
            if idx[y] == 0:
                q.append(y)

    res = [0] * n

    for i in range(n):
        res[i] = d[comp[i]]

    print("Yes")
    print(*res)


    pass


if __name__ == "__main__":
    sys.setrecursionlimit(int(10 ** 6))
    solve()