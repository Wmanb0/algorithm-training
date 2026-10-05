# @url https://atcoder.jp/contests/abc478/tasks/abc478_d
# @primary interval-merging
# @topics interval-merging, difference-array, hash-map, comparison-sorting
# @note
# Idea: Group all intervals by their inserted value X. For each value, sort its intervals and merge overlapping intervals so each position is counted at most once for that X, then add every merged interval to a global difference array.
# Key observation: Multiple operations inserting the same X into the same position still contribute only one distinct set element, so intervals belonging to the same X must first be replaced by their union.
# Complexity: O(Q log Q + N) time and O(N + Q) space.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    n, q = map(int, input().strip().split())
    d = {}
    for _ in range(q):
        l, r, x = map(int, input().strip().split())
        if d.get(x, 0) == 0:
            d[x] = [[l, r]]
        else: d[x].append([l, r])
        

    diff = [0] * (n + 5)
    for x in d:
        d[x] = sorted(d[x], key=lambda x : (x[0], x[1]))
        m = len(d[x])
        l = d[x][0][0]
        r = d[x][0][1]
        
        for i in range(1, m):
            
            if d[x][i][0] <= r:
                r = max(r, d[x][i][1])
            else:
                diff[l] += 1
                diff[r + 1] -= 1
                l = d[x][i][0]
                r = d[x][i][1]
        
        diff[l] += 1
        diff[r + 1] -= 1

    for i in range(1, n + 1):
        diff[i] += diff[i - 1]
        print(diff[i], end=' ')
    
    pass


if __name__ == "__main__":
    solve()