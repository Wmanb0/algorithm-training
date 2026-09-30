# @url https://codeforces.com/contest/2254/problem/C1
# @primary implementation
# @topics implementation, arithmetic
# @rating 1000
# @division div3
# @note
# Idea: Count the number of ones in a and b separately on even and odd indices. Output YES exactly when the corresponding parity counts are equal in both strings.
# Key observation: Every allowed transformation moves a one by exactly two positions, so index parity is preserved. Therefore the number of ones on each parity class is invariant and completely determines reachability.
# Complexity: O(N) time and O(1) auxiliary space per test case.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n = int(input().strip())
    a = input().strip()
    b = input().strip()
    oda = 0
    eva = 0
    odb = 0
    evb = 0
    for i in range(n):
        if i % 2 == 0:
            if a[i] == '1': eva += 1
            if b[i] == '1': evb += 1
        else:
            if a[i] == '1': oda += 1
            if b[i] == '1': odb += 1

    if eva == evb and oda == odb: print("YES")
    else: print("NO")
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()