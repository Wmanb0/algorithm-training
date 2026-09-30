# @url https://codeforces.com/contest/2254/problem/C2
# @primary sorting-greedy
# @topics sorting-greedy, comparison-sorting
# @rating 1200
# @division div3
# @note
# Idea: Record the positions of ones in both strings separately for even and odd indices. If the corresponding counts differ, output -1; otherwise sort each position list, pair positions in order, and sum half of their absolute distances.
# Key observation: A one can move only between positions of the same parity, and each operation shifts it by two positions. Pairing the sorted positions in the same order minimizes the total movement within each parity class.
# Complexity: O(N log N) time and O(N) space per test case.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n = int(input().strip())
    a = input().strip()
    b = input().strip()
    oda = []
    eva = []
    odb = []
    evb = []
    for i in range(n):
        if i % 2 == 0:
            if a[i] == '1': eva.append(i + 1)
            if b[i] == '1': evb.append(i + 1)
        else:
            if a[i] == '1': oda.append(i + 1)
            if b[i] == '1': odb.append(i + 1)

    if len(eva) == len(evb) and len(oda) == len(odb): 
        res = 0
        eva = sorted(eva)
        evb = sorted(evb)
        oda = sorted(oda)
        odb = sorted(odb)
        k = len(eva)
        for i in range(k):
            res += abs(evb[i] - eva[i]) // 2
        k = len(odb)
        for i in range(k):
            res += abs(oda[i] - odb[i]) // 2
        print(res)
    else: print("-1")
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()