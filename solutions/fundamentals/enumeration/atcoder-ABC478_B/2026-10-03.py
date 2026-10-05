# @url https://atcoder.jp/contests/abc478/tasks/abc478_b
# @primary enumeration
# @topics enumeration, arithmetic
# @note
# Idea: Enumerate every triple of distinct topping indices i < j < k. If their total price i+j+k+3 does not exceed V, update the maximum total happiness.
# Key observation: N is small enough to examine every possible set of three toppings, so directly evaluating every triple guarantees that the maximum feasible happiness is found.
# Complexity: O(N^3) time and O(N) space.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    n, v = map(int, input().strip().split())
    a = list(map(int, input().strip().split()))
    res = 0

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if i + j + k + 3 <= v:
                    res = max(res, a[i] + a[j] + a[k])
    print(res)

    pass


if __name__ == "__main__":
    solve()