# @url https://codeforces.com/contest/2264/problem/B
# @primary priority-queue
# @topics priority-queue, general-greedy
# @rating 1000
# @division div2
# @note
# Idea: Scan the array from left to right while maintaining the smallest M-1 previous values in a max-heap implemented with negated values. For each possible final element a[i], evaluate m * a[i] minus the sum of those selected previous values and maximize the result.
# Key observation: Once a[i] is fixed as the final selected value, maximizing the expression requires minimizing the sum of the other M-1 selected earlier values, so only the M-1 smallest values seen so far need to be retained.
# Complexity: O(N log M) time and O(N + M) space per test case.
# @endnote

import sys
import heapq
input = sys.stdin.readline


def solve_case():

    n, m = map(int, input().strip().split())

    a = [-10**30] + list(map(int, input().strip().split()))
    
    if m == 1:
        print(max(a))
        return

    q = []
    s = 0
    res = -10**30

    for i in range(1, n + 1):

        if len(q) == m - 1:
            res = max(res, m * a[i] - s)

        heapq.heappush(q, -a[i])
        s += a[i]

        if len(q) > m - 1:
            x = -heapq.heappop(q)
            s -= x

    print(res)


    pass


def main():
    t = int(input().strip())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()