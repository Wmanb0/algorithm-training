# @url https://codeforces.com/contest/2254/problem/A
# @primary arithmetic
# @topics arithmetic
# @rating 800
# @division div3
# @note
# Idea: If any two token counts are already equal, output zero. Otherwise find the middle value among the three counts and output the smaller distance from it to either the minimum or maximum value.
# Key observation: Each round decreases the current maximum by one and increases the current minimum by one while the middle value remains unchanged, so the game ends when one of the two extremes reaches the middle value.
# Complexity: O(1) time and O(1) space per test case.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    a, b, c = map(int, input().strip().split())
    if a == b or b == c or a == c: print(0)
    else:
        x = sum([a, b, c]) - max(a, b, c) - min(a, b, c)
        
        print(min(max(a, b, c) - x, x - min(a, b, c)))
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()