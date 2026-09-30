# @url https://usaco.org/index.php?page=viewproblem2&cpid=644
# @primary breadth-first-search
# @topics breadth-first-search, connected-components
# @note
# Idea: Maintain which barns are still open. After each closure step, start BFS from any currently open barn and count how many open barns are reachable, then compare this count with the total number of barns that should still be open.
# Key observation: The remaining farm is connected exactly when a BFS started from any open barn reaches every currently open barn.
# Complexity: O(N(N + M)) time and O(N + M) space.
# @endnote

import sys
from collections import deque
input = sys.stdin.readline


def solve():
    n, m = map(int, input().strip().split())
    adj = [[] for _ in range(n)]

    for _ in range(m):
        a, b = map(int, input().strip().split())
        a -= 1
        b -= 1
        adj[a].append(b)
        adj[b].append(a)


    st = [1 for i in range(n + 1)]
    for _ in range(n):
        cnt = 0
        t = int(input().strip())
        t -= 1
        
        for i in range(n):
            cnt = 0
            if st[i] != 0:
                q = deque([i])
                cnt += 1
                vis = [False] * (n + 5)
                vis[i] = True
                while q:
                    x = q.popleft()
                    for j in adj[x]:
                        if vis[j] == False and st[j] == 1:
                            vis[j] = True
                            cnt += 1
                            q.append(j)
                break
            
        st[t] = 0
        if cnt == n - _:print("YES")
        else:print("NO")


if __name__ == "__main__":
    solve()
