# @url https://usaco.org/index.php?page=viewproblem2&cpid=1303&lang=en
# @primary binary-search
# @topics binary-search, comparison-sorting, points-and-vectors
# @note
# Idea: Sort all grazing events by time. For each alibi, use binary search to locate the neighboring grazing times and test whether the cow can travel between the corresponding points within the available time using squared Euclidean distance.
# Key observation: For an alibi at time t, only the closest grazing events immediately around t in chronological order constrain its feasibility; the travel condition can be checked as squared distance <= squared time difference.
# Complexity: O(N log N + M log N) time and O(N) space.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    n, m = map(int, input().split())
    a = [[0, 0, -1e10]]

    for _ in range(n):
        a.append(list(map(int, input().split())))
    a = sorted(a, key=lambda x : x[2])

    res = 0

    for _ in range(m):
        x, y, t = map(int, input().split())

        l = 1
        r = n
        while l < r:
            mid = (l + r + 1) // 2
            if a[mid][2] <= t: l = mid
            else: r = mid - 1

        l = int(l)
        if (x - a[l][0]) ** 2 + (y - a[l][1]) ** 2 <= (t - a[l][2]) ** 2:
            l1 = l + 1
            r1 = n
            while l1 < r1:
                mid = (l1 + r1) // 2
                if a[mid][2] >= t: r1 = mid
                else: l1 = mid + 1

            l1 = int(l1)
            if l1 > n:
                if l != 1: 
                    l1 = l
                    l = l - 1
                else: l1 = 1

            if (x - a[l1][0]) ** 2 + (y - a[l1][1]) ** 2 <= (t - a[l1][2]) ** 2:
                res += 1



    print(m - res)
    pass


if __name__ == "__main__":
    solve()