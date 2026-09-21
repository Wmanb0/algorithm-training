# @url https://usaco.org/index.php?page=viewproblem2&cpid=643
# @primary two-pointers
# @topics comparison-sorting
# @note
# Idea: Sort the diamond sizes and use a monotonic right pointer to compute the largest valid group starting at each position. Build suffix maxima of these group sizes and combine two non-overlapping groups.
# Key observation: After sorting, every valid group forms a contiguous interval, and the right endpoint never moves backward as the left endpoint increases.
# Complexity: O(N log N) time and O(N) space.
# @endnote

import sys

input = sys.stdin.readline

def solve():

    n, k = map(int, input().strip().split())
    a = [-1]
    res = 0
    for i in range(n): a.append(int(input().strip()))
    a.sort()
    pre = [0 for _ in range(n + 5)]
    bac = [0 for _ in range(n + 5)]
    r = 1
    for i in range(1, n + 1):
        while r <= n and abs(a[r] - a[i]) <= k: r += 1
        pre[i] = r - i
    r = n
    for i in range(n, 0, -1):
        bac[i] = max(bac[i + 1], pre[i])
    res = 0
    for i in range(1, n):
        res = max(res, pre[i] + bac[i + pre[i]])
    print(res)
    pass


if __name__ == "__main__":
    solve()