# @url https://codeforces.com/contest/2244/problem/A
# @primary string-simulation
# @topics string-simulation
# @rating 800
# @division div3
# @note
# Idea: Scan the string and measure the length of every consecutive block of '#'. Keep the maximum block length and output half of it rounded up.
# Key observation: A line of length L is erased from both ends simultaneously, so it requires ceil(L / 2) seconds; therefore only the longest consecutive '#' block matters.
# Complexity: O(N) time and O(N) space per test case.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n = int(input())
    s = input().strip()
    k = 0
    i = 0
    while i < n:
        p = 0
        while i < n and s[i] == "#":
            p += 1
            i += 1
        k = max(k, p)
        i += 1   

    print((k + 1) // 2)
    pass


def main():
    
    t = int(input().strip())
    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()