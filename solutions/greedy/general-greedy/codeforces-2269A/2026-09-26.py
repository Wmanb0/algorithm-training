# @url https://codeforces.com/contest/2269/problem/A
# @primary general-greedy
# @topics general-greedy, arithmetic
# @division div2
# @note
# Idea: Place the K withdrawal days at the end. Let the balance grow through the first N-K days, withdraw after the next doubling, then withdraw every remaining day while the account repeatedly resets to 1.
# Key observation: The withdrawal amounts are powers of two determined by the lengths of the K growth segments. Since their lengths are positive and sum to N, the total is maximized by making one segment as long as possible and all remaining segments length 1.
# Complexity: O(N) time and O(N) space per test case.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()
import sys

input = sys.stdin.readline


def solve_case():
    n, k = map(int, input().split())
    p = [0] * (n + 1)
    for i in range(k):
        p[n - i] = 1
    res = 0
    t = 1
    for i in range(1, n + 1):
        if p[i] == 0: t *= 2
        else:
            t *= 2
            res += t
            t = 1
    print(res)
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()