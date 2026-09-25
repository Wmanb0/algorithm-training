# @url https://codeforces.com/contest/2267/problem/B
# @primary comparison-sorting
# @topics comparison-sorting, hash-map
# @note
# Idea: Count the frequency of every value, sort the distinct values in descending order, then repeatedly scan them and output one remaining copy of each value until all elements are printed.
# Key observation: Each pass outputs every currently available distinct value exactly once in descending order, while the frequency table determines how many future passes each value survives.
# Complexity: O(N + U log U + NU) time and O(N + U) space per test case, where U is the number of distinct values.
# @endnote
import sys

input = sys.stdin.readline


def solve_case():
    n = int(input())
    l = list(map(int, input().strip().split()))

    k = {}
    for i in range(n):
        k[l[i]] = k.get(l[i], 0) + 1

    
    l = list(set(l))
    l = sorted(l, reverse=True)
    cnt = 0
    while cnt < n:

        for i in l:
            if k[i] > 0:
                k[i] -= 1
                print(i, end=' ')
                cnt += 1
    print()
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()