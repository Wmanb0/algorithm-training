# @url https://codeforces.com/contest/2264/problem/A
# @primary implementation
# @topics implementation, array
# @rating 800
# @division div2
# @note
# Idea: Remove every element already equal to its target position, reverse the remaining values, and check whether this reversed sequence is nondecreasing.
# Key observation: The chosen operation reverses exactly the values placed at the selected indices while fixed positions may remain untouched, so the non-fixed values must appear in the reverse order required by the sorted permutation.
# Complexity: O(N) time and O(N) space per test case.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n = int(input().strip())
    a = [0] + list(map(int, input().strip().split()))

    b = []
    for i in range(1, n + 1):
        if a[i] != i:
            b.append(a[i])

    b = b[::-1]

    for i in range(1, len(b)):
        if b[i] < b[i - 1]: 
            print("NO")
            return
    
    print("YES")
    pass


def main():
    t = int(input().strip())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()