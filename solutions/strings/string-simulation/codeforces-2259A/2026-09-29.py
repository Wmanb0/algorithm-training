# @url https://codeforces.com/contest/2259/problem/A
# @primary string-simulation
# @topics string-simulation, enumeration
# @rating 800
# @division div3
# @note
# Idea: Partition the string into consecutive blocks of length K and inspect each block independently. Count a block if it contains no '0', meaning all K characters are '1'.
# Key observation: The code only considers the fixed non-overlapping blocks [0,K), [K,2K), ...; therefore each block can be checked independently by testing whether its zero count is zero.
# Complexity: O(N) time and O(K) auxiliary space per test case due to substring slicing.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n, k = map(int, input().strip().split())
    s = input().strip()
    l = 0
    res = 0
    for i in range(n // k):
        t = s[l : l + k]
        if t.count('0') == 0: res += 1
        l += k
    print(res)
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()