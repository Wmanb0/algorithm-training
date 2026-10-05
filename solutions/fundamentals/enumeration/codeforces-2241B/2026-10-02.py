# @url https://codeforces.com/contest/2241/problem/B
# @primary enumeration
# @topics enumeration, arithmetic, string-simulation
# @rating 1100
# @division div3
# @note
# Idea: Inspect the distinct decimal digits of the given number and handle the simple special cases directly. Otherwise enumerate multipliers from 1 through 7, multiply the number by each candidate, and inspect the distinct digits of the product.
# Key observation: Whether a number is good can be checked directly from the number of distinct digits in its decimal representation, so each bounded candidate multiplier can be tested independently.
# Complexity: O(log X) time and O(log X) space per test case.
# @endnote
import sys

input = sys.stdin.readline


def solve_case():
    n = input().strip()
    k = list(set(n))
    if len(k) < 2: print(10)
    elif '1' in k and '0' in k and len(k) == 2: print(10)
    else:
        t = int(n)
        d = 10
        for i in range(1, 8):
            a = str(i * t)
            p = list(set(a))
            aa = str(i)
            pp = list(set(aa))
            if len(p) <= 2 and len(pp) <= 2: print(t, i)

    
    pass


def main():
    t = int(input().strip())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()