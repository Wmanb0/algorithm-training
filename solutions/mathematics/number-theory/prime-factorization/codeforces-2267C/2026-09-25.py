# @url https://codeforces.com/contest/2267/problem/c
# @primary prime-factorization
# @topics prime-factorization, arithmetic
# @note
# Idea: Extract all distinct prime factors of m by trial division. For each prime factor p, scan the array and sum every element divisible by p, then take the maximum such sum.
# Key observation: Only distinct prime divisors of m need to be considered, and for a fixed divisor p the required contribution is exactly the sum of array elements divisible by p.
# Complexity: O(sqrt(M) + NP) time and O(P) space per test case, where P is the number of distinct prime factors of M.
# @endnote
import sys

input = sys.stdin.readline


def solve_case():
    n, m = map(int, input().strip().split())

    a = list(map(int, input().strip().split()))

    p = []

    d = 2
    while d <= m // d:

        if m % d == 0:
            p.append(d)
            while m % d == 0:
                m //= d
        d += 1

    if m > 1: p.append(m)

    res = 0

    for i in p:
        v = 0
        for j in range(n):
            if a[j] % i == 0:
                v += a[j]

        res = max(res, v)

    print(res)

    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()