# @url https://atcoder.jp/contests/abc477/tasks/abc477_c
# @primary binary-search
# @topics binary-search, string-simulation
# @note
# Idea: Enumerate every occurrence of t in s and store its start and end positions. For each query interval, use binary search on the sorted occurrence starts to find occurrences nearest to the left boundary and check whether one lies completely inside the interval.
# Key observation: Occurrence start positions are stored in increasing order, so only occurrences around the query's left boundary need to be inspected after binary search.
# Complexity: O(|S||T| + Q log M) time and O(M) space, where M is the number of occurrences of T in S.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    Q = int(input().strip())
    s = input().strip()
    t = input().strip()
    len_t = len(t)
    len_s = len(s)
    ls = []
    for i in range(len_s - len_t + 1):
        flag = 1
        for j in range(len_t):
            if s[i + j] != t[j]: flag = 0
        if flag:
            ls.append([i + 1, i + len_t])


    len_ls = len(ls)
    if len_ls == 0:
        for _ in range(Q):
            l, r = map(int, input().strip().split())
            print("No")
    else:
        for _ in range(Q):
            l, r = map(int, input().strip().split())
            if r - l + 1 < len_t:
                print("No")
                continue
            # t in s[l : r + 1]
            # 最靠近l的
            # 左边最靠近
            ll = 0
            rr = len_ls - 1
            while ll < rr:
                mid = (ll + rr) // 2
                if ls[mid][0] >= l: rr = mid
                else: ll = mid + 1

            lll = 0
            rrr = len_ls - 1
            while lll < rrr:
                mid = (lll + rrr + 1) // 2
                if ls[mid][0] <= l: lll = mid
                else: rrr = mid - 1


            if (r >= ls[lll][1] and l <= ls[lll][0]) or (r >= ls[ll][1] and l <= ls[ll][0]): print("Yes")
            else: print("No")


    pass


if __name__ == "__main__":
    solve()