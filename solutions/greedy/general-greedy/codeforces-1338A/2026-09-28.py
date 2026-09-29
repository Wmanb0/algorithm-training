# @url https://codeforces.com/contest/1338/problem/A
# @primary general-greedy
# @topics general-greedy, arithmetic
# @rating 1500
# @division div1
# @note
# Idea: Scan the array from left to right and keep it nondecreasing by raising every element that is smaller than the previous adjusted value. For each required increase, compute how many binary bits are needed to represent that difference and keep the maximum.
# Key observation: After T seconds, any individual position can receive any total increment from 0 to 2^T - 1 by choosing the corresponding powers of two. Therefore a required increase d can be achieved exactly when d < 2^T, so the answer is the maximum bit length of any required correction.
# Complexity: O(N log V) time and O(N) space per test case, where V is the maximum required increase.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n = int(input().strip())
    a = [0] + list(map(int, input().strip().split()))
    res = 0
    for i in range(2, n + 1):
        if a[i] < a[i - 1]:
            t = a[i - 1] - a[i]
            k = 0
            while t != 0:
                k += 1
                t >>= 1
            a[i] = a[i - 1]
            res = max(res, k)
    print(res)

    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()