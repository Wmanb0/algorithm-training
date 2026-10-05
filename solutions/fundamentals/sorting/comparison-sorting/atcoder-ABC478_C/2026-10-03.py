# @url https://atcoder.jp/contests/abc478/tasks/abc478_c
# @primary comparison-sorting
# @topics comparison-sorting, array
# @note
# Idea: Sort a copy of the whole array and find the first position where the original array differs from the globally sorted order. Sort the prefix extending through K positions from that point, rebuild the array, and check whether the result is nondecreasing.
# Key observation: Before the first mismatch, the original array already agrees with the final sorted order, so the code chooses the earliest relevant position and tests whether sorting the corresponding region makes the entire sequence sorted.
# Complexity: O(N log N) time and O(N) space.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    n, k = map(int, input().strip().split())
    a = [0] + list(map(int, input().strip().split()))
    t = sorted(a)
    p = 1
    for i in range(1, n - k + 2):
        if a[i] != t[i]:
            p = i
            break
    b = a[: p + k]
    b = sorted(b)
    c = b + a[p + k:]

    
    for i in range(2,  n + 1):
        if c[i] < c[i - 1]: 
            print("No")
            return
    print("Yes")

    pass


if __name__ == "__main__":
    solve()