# @url https://codeforces.com/contest/2241/problem/A
# @primary arithmetic
# @topics arithmetic
# @rating 800
# @division div3
# @note
# Idea: Check whether a is divisible by b and output YES exactly when a % b equals zero.
# Key observation: Repeatedly dividing a by divisors is equivalent to removing one divisor equal to a / b, which is possible exactly when b divides a.
# Complexity: O(1) time and O(1) space per test case.
# @endnote
import sys

input = sys.stdin.readline


def solve_case():
    a, b = map(int, input().strip().split())
    if a % b == 0: print("YES")
    else: print("NO")
    pass


def main():
    t = int(input().strip())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()