# @url https://usaco.org/index.php?page=viewproblem2&cpid=668
# @primary breadth-first-search
# @topics breadth-first-search, points-and-vectors
# @note
# Idea: Build a directed graph where cow i has an edge to cow j whenever j lies within i's transmission radius. Run BFS starting from every cow and count how many cows are reachable, then output the maximum count.
# Key observation: Once a cow receives the broadcast, it can forward it using its own transmission radius, so the total number reached from one starting cow is exactly the number of vertices reachable from that cow in the directed graph.
# Complexity: O(N^3) time and O(N^2) space.
# @endnote

import sys
from collections import deque
input = sys.stdin.readline


def solve():
    n = int(input().strip())
    adj = [[] for _ in range(n + 1)]
    cow = []
    for i in range(n):
        x, y, p = map(int, input().strip().split())
        cow.append([x, y, p])
        
    for i in range(n):
        ax, ay, ap = cow[i][0], cow[i][1], cow[i][2]
        for j in range(i + 1, n):
            bx, by, bp = cow[j][0], cow[j][1], cow[j][2]
            dis = (ax - bx) * (ax - bx) + (ay - by) * (ay - by)
            if dis <= ap * ap:
                adj[i + 1].append(j + 1)

            if dis <= bp * bp:
                adj[j + 1].append(i + 1)

    res = 1
    for i in range(1, n + 1):
        cnt = 1
        q = deque([i])
        vis = [False] * (n + 1)
        vis[i] = True
        while q:
            x = q.popleft()
            for j in adj[x]:
                if not vis[j]:
                    cnt += 1
                    vis[j] = True
                    q.append(j)
        res = max(res, cnt)
    print(res)
    pass


if __name__ == "__main__":
    solve()