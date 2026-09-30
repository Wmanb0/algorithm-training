# @url https://codeforces.com/contest/2259/problem/E
# @primary greedy-construction
# @topics greedy-construction, difference-array
# @rating 1500
# @division div3
# @note
# Idea: Use a difference array to mark every position that cannot contain treasure because it lies strictly inside the required distance interval of a known positive value. First force every known zero position to contain treasure, then for each positive a[i], place treasure at one of the two possible endpoints i-a[i] or i+a[i] if neither endpoint has already satisfied the constraint.
# Key observation: For a known positive distance a[i], no treasure may appear strictly closer than a[i], while at least one valid endpoint exactly a[i] away must contain treasure. The difference array lets the code test forbidden positions in O(1) after preprocessing.
# Complexity: O(N) time and O(N) space per test case.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n = int(input().strip())
    a = [0] + list(map(int, input().strip().split()))
    if a.count(-1) == n:
        print(1,end='')
        print("0"*(n-1))
        return

    dif = [0] * (n + 5)

    for i in range(1, n + 1):
        if a[i] != -1 and a[i] > 0:
            l = max(1, i - a[i] + 1)
            r = min(n, i + a[i] - 1)
            if l <= r:
                dif[l] += 1
                dif[r + 1] -= 1

    pre = [0] * (n + 5)
    for i in range(1, n + 1):
        pre[i] = pre[i - 1] + dif[i]

    res = [0] * (n)

    for i in range(1, n + 1):
        if a[i] == 0:
            if pre[i] > 0:
                print("-1")
                return
            res[i - 1] = 1

    for i in range(1, n + 1):
        if a[i] != -1 and a[i] > 0:
            l = i - a[i]
            r = i + a[i]

            if l >= 1 and res[l - 1] == 1:
                continue
            if r <= n and res[r - 1] == 1:
                continue

            if l >= 1 and pre[l] == 0:
                res[l - 1] = 1
            elif r <= n and pre[r] == 0:
                res[r - 1] = 1
            else:
                print("-1")
                return

    for i in res:
        print(i, end='')
    print()
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()