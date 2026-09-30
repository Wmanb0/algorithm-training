# @url https://usaco.org/index.php?page=viewproblem2&cpid=944
# @primary connected-components
# @topics connected-components, breadth-first-search, points-and-vectors
# @note
# Idea: Traverse every connected component with BFS while maintaining the minimum and maximum x and y coordinates of its cows. Compute the perimeter of the component's axis-aligned bounding rectangle and keep the minimum.
# Key observation: Every connected component must be enclosed independently, and the smallest axis-aligned rectangle containing a component is determined solely by its minimum and maximum x and y coordinates.
# Complexity: O(N + M) time and O(N + M) space.
# @endnote

import sys
from collections import deque
input = sys.stdin.readline


def solve():
    n, m = map(int, input().strip().split())
    adj = [[] for _ in range(n + 1)]
    op = [[]]
    for i in range(n):
        x, y = map(int, input().strip().split())
        op.append([x, y])

    for _ in range(m):
        a, b = map(int, input().strip().split())
        adj[a].append(b)
        adj[b].append(a)

    res = int(1e10)
    vis = [False] * (n + 1)
    for i in range(1, n + 1):
        if not vis[i]:
            minx = op[i][0]
            maxx = op[i][0]
            miny = op[i][1]
            maxy = op[i][1]
            q = deque([i])
            vis[i] = True
            while q:
                x = q.popleft()
                for j in adj[x]:
                    if not vis[j]:
                        q.append(j)
                        vis[j] = True
                        minx = min(minx, op[j][0])
                        maxx = max(maxx, op[j][0])
                        miny = min(miny, op[j][1])
                        maxy = max(maxy, op[j][1])
            res = min(res, ((maxx - minx) + (maxy - miny)) * 2)
    print(res)
    pass


if __name__ == "__main__":
    solve()