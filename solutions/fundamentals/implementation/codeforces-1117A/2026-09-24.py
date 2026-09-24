# @url https://codeforces.com/contest/1117/problem/A
# @primary implementation
# @topics implementation
# @rating 1100
# @division div2
# @note
# Idea: Find the maximum array value, then scan the array and measure the length of every consecutive run consisting only of that maximum value. Keep the longest such run.
# Key observation: The maximum possible subarray average equals the maximum element of the array, and a subarray achieves this average only if every element in it equals that maximum.
# Complexity: O(N) time and O(N) space.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))

    v = max(a)
    res = 0
    i = 0

    while i < n:
        r = 0

        while i < n and a[i] == v:
            r += 1
            i += 1

        res = max(res, r)
        i += 1

    print(res)


if __name__ == "__main__":
    solve()