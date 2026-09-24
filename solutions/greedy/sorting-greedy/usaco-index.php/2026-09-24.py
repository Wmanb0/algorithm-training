# @url https://usaco.org/index.php?page=viewproblem2&cpid=573&lang=en
# @primary sorting-greedy
# @topics sorting-greedy, two-pointers, comparison-sorting
# @note
# Idea: Split Elsie's cards into the two halves of the game and sort them in the required directions. Use Bessie's larger cards to greedily beat as many cards as possible in the first half, then use her smaller cards to greedily play below as many cards as possible in the second half.
# Key observation: In each half, using the weakest card that can still win preserves stronger or smaller useful cards for later rounds, so the sorted greedy matching maximizes the number of wins.
# Complexity: O(N log N) time and O(N) space.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    n = int(input())

    a = []
    k = {}
    b = []
    for _ in range(n):
        t = int(input().strip())
        k[t] = 1
        a.append(t)
    for i in range(1, 2 * n + 1):
        if k.get(i, 0) == 0: b.append(i)

    d = a[:n // 2]
    d = sorted(d)
    dd = a[n // 2:]
    dd = sorted(dd, reverse=True)

    res = 0
    j = 0
    bb = b[n // 2:]
    for i in range(n // 2):

        if bb[i] > d[j]:
            j += 1
            res += 1


    j = 0
    bbb = b[:n // 2]
    bbb = sorted(bbb, reverse=True)
    for i in range(n // 2):
        if bbb[i] < dd[j]:
            j += 1
            res += 1

    print(res)
    pass


if __name__ == "__main__":
    solve()