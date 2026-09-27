# @url https://codeforces.com/contest/2266/problem/B
# @primary arithmetic
# @topics arithmetic
# @division div3
# @note
# Idea: Directly compute the two candidate final differences |a + c - b| and |a - b|, then output their maximum.
# Key observation: Alice's optimal result is determined by the better of taking all stones from the third pile and taking none, so only these two endpoint outcomes need to be compared.
# Complexity: O(1) time and O(1) space per test case.
# @endnote
import sys

input = sys.stdin.readline


def solve_case():
    a, b, c = map(int, input().strip().split())

    print(max(abs(a + c - b), abs(a - b)))

    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()