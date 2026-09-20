# @url https://atcoder.jp/contests/abc474/tasks/abc474_e
# @primary sorting-greedy
# @topics enumeration, prefix-sum, exchange-argument
# @note
# Idea: Start from the total cost of choosing A for every product, sort the savings A-B in descending order, and enumerate the number k of products bought using coupons.
# Key observation: For a fixed k, choosing the k largest savings is optimal. If k exceeds N/2, exactly 2k-N additional coupons are required, and each can be obtained with the minimum A cost.
# Complexity: O(N log N) time and O(N) space per test case.
# @endnote

import sys
input = sys.stdin.readline


def solve_case():
    n = int(input())

    s = 0
    p = 10**30
    d = []

    for _ in range(n):
        a, b = map(int, input().split())

        s += a
        p = min(p, a)
        d.append(a - b)

    d.sort(reverse=True)

    ans = s
    pre = 0

    for k in range(1, n + 1):
        pre += d[k - 1]

        cost = s - pre
        if k >= n / 2: cost += (2 * k - n) * p

        ans = min(ans, cost)

    print(ans)


def main():
    T = int(input())

    for _ in range(T):
        solve_case()


if __name__ == "__main__":
    main()