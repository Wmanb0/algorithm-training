# @url https://codeforces.com/contest/2244/problem/B
# @primary general-greedy
# @topics general-greedy, arithmetic
# @rating 800
# @division div3
# @note
# Idea: Process the stacks from left to right. For each position i, require at least i books, fix it to exactly i, and transfer all surplus books to the next position.
# Key observation: Books can only move to the right, so after leaving position i its value can no longer be increased from the right. Keeping exactly the minimum required value i leaves the maximum possible surplus for later stacks.
# Complexity: O(N) time and O(N) space per test case.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n = int(input().strip())
    a = [0] + list(map(int, input().strip().split()))
    for i in range(1, n):
        if a[i] < i: 
            print("NO")
            return
        k = a[i] - i
        a[i + 1] += k
        a[i] = i
    if a[n] <= a[n - 1]: print("NO")
    else: print("YES")
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()