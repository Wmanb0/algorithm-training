# @url https://codeforces.com/contest/1398/problem/C
# @primary prefix-sum
# @topics hash-map
# @rating 1600
# @note
# Idea: Convert each prefix sum into pre[i] - (i + 1) and count how many previous prefixes have the same transformed value.
# Key observation: A subarray has digit sum equal to its length exactly when the transformed prefix values at its two boundaries are equal.
# Complexity: O(N) time and O(N) space per test case.
# @endnote

import sys
from collections import defaultdict
input = sys.stdin.readline


def solve_case():
    n = int(input())
    s = input().strip()
    a = []
    for i in s: 
        a.append(int(i))
    pre = [0] * (n + 1)
    pre[0] = a[0]
    for i in range(1, n):
        pre[i] = pre[i - 1] + a[i]

    res = 0
    cnt = defaultdict(int)
    cnt[0] = 1
    # 以 i 结尾出现了多少次， pre[i] - i
    for i in range(n):
        x = pre[i] - (i + 1)
        
        res += cnt[x]
        cnt[x] += 1

    print(res)

    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()