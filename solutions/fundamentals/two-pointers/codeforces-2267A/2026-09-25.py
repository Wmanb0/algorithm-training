# @url https://codeforces.com/contest/2267/problem/A
# @primary two-pointers
# @topics two-pointers, string-simulation
# @note
# Idea: Use two pointers from both ends of the string. For every mismatched mirrored pair, add two changes, but subtract one if either character already equals the target character c.
# Key observation: Each mirrored pair is independent: equal characters need no change, while a mismatched pair costs two operations unless one side is already c, in which case only one additional change is needed.
# Complexity: O(N) time and O(N) space per test case.
# @endnote
import sys

input = sys.stdin.readline


def solve_case():
    n, c = input().strip().split()
    n = int(n)

    s = input()

    i = 0
    j = n - 1
    res = 0
    while i < j:
        if s[i] != s[j]:
            res += 2
            if s[i] == c or s[j] == c:
                res -= 1
        i += 1
        j -= 1
    print(res)

    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()