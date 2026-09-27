# @url https://codeforces.com/contest/2266/problem/C
# @primary enumeration
# @topics enumeration, string-simulation
# @division div3
# @note
# Idea: Count the total number of zeros and ones, then scan every possible split position. Maintain the number of ones on the left and zeros on the right, and minimize their sum.
# Key observation: A sorted binary string has the form 000...111, so for any fixed split, every 1 on the left and every 0 on the right must be changed. Enumerating all splits therefore finds the minimum number of required operations.
# Complexity: O(N) time and O(N) space per test case.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():

    n = int(input().strip())
    s = input().strip()
    cnt_0 = s.count('0')
    cnt_1 = s.count('1')

    if s[0] == '1':
        print(cnt_0)
    else:
        last_1 = cnt_1
        last_0 = cnt_0 - 1
        res = last_0
        cnt1 = 0
        cnt0 = 1
        # 全变成1的,就是 cnt_0 - 1
        for i in range(1, n):
            if s[i] == '1': 
                cnt1 += 1
                last_1 -= 1
            else: 
                cnt0 += 1
                last_0 -= 1

            res = min(res, cnt1 + last_0)
        print(res)

    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()