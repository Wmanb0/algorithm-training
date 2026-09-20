# @url https://atcoder.jp/contests/abc474/tasks/abc474_d
# @primary constructive-algorithms
# @topics case-analysis
# @note
# Idea: Construct W independently for each position, assigning 1 when A[i] <= B[i] and a sufficiently large value otherwise.
# Key observation: A valid construction exists exactly when at least one position satisfies A[i] > B[i].
# Complexity: O(N) time and O(N) space.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    flag = False
    w = []
    p = 0
    for i in range(n):
        if a[i] <= b[i]: 
            w.append(1)
            p += b[i] - a[i]
        else: 
            w.append(int(1e18))
            flag = True
    
    if flag: 
        print("Yes")
        print(*w, sep=' ')
    else: print("No")


if __name__ == "__main__":
    solve()