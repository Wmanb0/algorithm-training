# @url https://codeforces.com/contest/762/problem/B
# @primary sorting-greedy
# @topics sorting-greedy, comparison-sorting
# @rating 1400
# @division div2
# @note
# Idea: Sort all devices by price and process them from cheapest to most expensive. Buy each device using a compatible dedicated port if available, otherwise use a universal port, until no compatible port remains.
# Key observation: Since every purchased device contributes exactly one unit to the device count, processing prices in ascending order ensures that for any achievable number of purchases, the chosen compatible devices have minimum total cost.
# Complexity: O(N log N) time and O(N) space.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    a, b, c = map(int, input().split())
    n = int(input().strip())
    list_m = []
    for _ in range(n):
        t = input().strip().split()
        list_m.append([int(t[0]), t[1]])

    list_m = sorted(list_m)
    res = a + b + c
    p = 0
    for i in range(n):
        if list_m[i][1] == 'USB':
            if a > 0: 
                a -= 1
                p += list_m[i][0]
            elif c > 0:
                c -= 1
                p += list_m[i][0]
        else:
            if b > 0: 
                b -= 1
                p += list_m[i][0]
            elif c > 0: 
                c -= 1
                p += list_m[i][0]

            
    print(res - a - b - c, p)
    pass


if __name__ == "__main__":
    solve()