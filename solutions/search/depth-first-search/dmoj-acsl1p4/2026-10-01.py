# @url https://dmoj.ca/problem/acsl1p4
# @primary depth-first-search
# @topics depth-first-search
# @note
# Idea: Build a directed graph from each match result, directing the edge from the winner to the loser. Start a DFS from every vertex and check whether the search can return to its starting vertex; count every starting vertex for which this is possible.
# Key observation: A vertex belongs to a directed cycle exactly when there exists a directed path starting from that vertex that eventually returns to itself.
# Complexity: O(N(N + K)) time and O(N + K) space.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    n, k = map(int, input().split())

    adj = [[] for _ in range(n)]

    for _ in range(k):
        a, b, sa, sb = map(int, input().split())
        a -= 1
        b -= 1

        if sa > sb:
            adj[a].append(b)
        else:
            adj[b].append(a)

    cycle = set()

    for start in range(n):
        vis = [False] * n
        vis[start] = True

        def dfs(x):
            for y in adj[x]:
                if y == start:
                    return True

                if not vis[y]:
                    vis[y] = True
                    if dfs(y):
                        return True

            return False

        if dfs(start):
            cycle.add(start)

    print(len(cycle))


if __name__ == "__main__":
    solve()