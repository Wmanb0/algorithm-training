# @url https://codeforces.com/contest/2259/problem/B
# @primary arithmetic
# @topics arithmetic
# @rating 800
# @division div3
# @note
# Idea: Classify every value into one of three groups: odd numbers, numbers congruent to 2 modulo 4, and numbers divisible by 4. Count the size of each group and output the largest count.
# Key observation: The code's classification depends only on divisibility by 2 and 4, so every array element belongs to exactly one of the three relevant residue classes.
# Complexity: O(N) time and O(N) space per test case for the input array.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n = int(input().strip())
    a = list(map(int, input().strip().split()))
    od = 0
    ev1 = 0
    ev2 = 0
    for i in a:
        if i % 2 == 0: 
            if (i // 2) % 2 == 0: ev2 += 1
            else: ev1 += 1
        else: od += 1
    print(max(od, ev1, ev2))
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()