# @url https://codeforces.com/contest/2259/problem/D
# @primary greedy-construction
# @topics greedy-construction, array
# @rating 1200
# @division div3
# @note
# Idea: Count the number of zeros first. If there is exactly one zero, report that no construction exists. Otherwise construct the assignment string directly: with no zeros, cycle through A, B, C; with at least two zeros, place the first two zeros into different groups and assign the remaining elements using the fixed pattern in the code.
# Key observation: The construction only needs special handling for zero values because the MEX of each multiset is determined by whether zero and subsequent required values are present; a single zero cannot be shared across multiple multisets, while zero zeros or at least two zeros allow the code's direct construction.
# Complexity: O(N) time and O(N) space per test case for the input array.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n = int(input().strip())
    a = list(map(int, input().split()))
    if a.count(0) == 1:
        print("NO")
        return
    print("YES")
    if a.count(0) == 0:
        for i in range(n):
            if i % 3 == 0: print("A", end='')
            elif i % 3 == 1: print("B", end='')
            else:print("C", end='')
    else:
        cnt_0 = 0
        for i in range(n):
            if a[i] == 0 and cnt_0 == 0: 
                print("A", end='')
                cnt_0 += 1
            elif a[i] == 0 and cnt_0 == 1: 
                print("B", end='')
                cnt_0 += 1
            elif a[i] == 0: print("A", end='')
            else:print("C", end='')
    print()
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()