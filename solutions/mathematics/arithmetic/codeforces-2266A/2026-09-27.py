# @url https://codeforces.com/contest/2266/problem/A
# @primary arithmetic
# @topics arithmetic
# @division div3
# @note
# Idea: Compute how many participants must be weak for each problem as n - a, n - b, and n - c, then take the maximum of these three values.
# Key observation: At most min(a, b, c) participants can have solved all three problems, so the minimum number of weak participants is n - min(a, b, c), which is equivalent to max(n - a, n - b, n - c).
# Complexity: O(1) time and O(1) space per test case.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n = int(input().strip())
    a, b, c = map(int, input().strip().split())
    print(max(n - a, n - b, n - c))
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()