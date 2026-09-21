# @url https://codeforces.com/contest/1826/problem/D
# @primary general-dp
# @topics enumeration
# @note
# Idea: Precompute the best value of a[j] + j on every prefix and a[k] - k on every suffix, then enumerate the middle index.
# Key observation: Once the middle index is fixed, the optimal left and right choices are independent and can be obtained from the precomputed prefix and suffix maxima.
# Complexity: O(N) time and O(N) space per test case.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    res = 0
    n = int(input())
    a = list(map(int, input().strip().split()))
    bi = [-1e18] * (n + 5)
    bk = [-1e18] * (n + 5)
    for i in range(1, n + 1):
        bi[i] = max(bi[i - 1], a[i - 1] + i)
    for i in range(n, 0, -1):
        bk[i] = max(bk[i + 1], a[i - 1] - i)

    for i in range(1, n - 1):
        res = max(res, a[i] + bi[i] + bk[i + 2])
    print(res)


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()