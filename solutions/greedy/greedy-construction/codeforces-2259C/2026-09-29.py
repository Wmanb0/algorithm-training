# @url https://codeforces.com/contest/2259/problem/C
# @primary greedy-construction
# @topics greedy-construction, array
# @rating 1000
# @division div3
# @note
# Idea: Scan the array from left to right while tracking how many fixed or constructed 1s already exist and how many 1s and -1s remain. Replace each -1 with 0 or 1 according to these counts so that suitable 1s are preserved on both sides while unnecessary -1s become 0.
# Key observation: Once a 1 already exists on the left and another usable endpoint can still remain on the right, an intermediate -1 can safely become 0; otherwise the current -1 must become 1 to create or preserve an endpoint.
# Complexity: O(N) time and O(N) space per test case.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n = int(input().strip())
    a = [0] + list(map(int, input().strip().split()))

    cnt_1 = a.count(1)
    now_1 = 0
    cnt_11 = a.count(-1)
    for i in range(1, n + 1):
        if a[i] == 1: 
            now_1 += 1
            cnt_1 -= 1

        #
        if a[i] == -1:
            if now_1 > 0 and (cnt_11 > 1 or cnt_1 > 0): # 已经有 1 并且不是最后一个 -1
                a[i] = 0
            #如果没有1
            if now_1 == 0:
                a[i] = 1
                now_1 += 1
            # 如果是最后一个-1且后面没有1
            if cnt_11 == 1 and cnt_1 == 0:
                a[i] = 1
            cnt_11 -= 1

    print(*a[1:])
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()