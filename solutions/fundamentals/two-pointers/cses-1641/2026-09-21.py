# @url https://cses.fi/problemset/task/1641/
# @primary two-pointers
# @topics comparison-sorting
# @note
# Idea: Sort the values together with their original indices, fix one element, and use two pointers to find two remaining values whose sum completes the target.
# Key observation: In sorted order, increasing the left pointer increases the sum and decreasing the right pointer decreases it.
# Complexity: O(N^2) time and O(N) space.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    b = sorted((v, i) for i, v in enumerate(a))

    for i in range(n):
        l = i + 1
        r = n - 1

        while l < r:
            s = b[i][0] + b[l][0] + b[r][0]

            if s == x:
                print(b[i][1] + 1, b[l][1] + 1, b[r][1] + 1)
                return

            if s < x:
                l += 1
            else:
                r -= 1
            
    print("IMPOSSIBLE")
    pass


if __name__ == "__main__":
    solve()