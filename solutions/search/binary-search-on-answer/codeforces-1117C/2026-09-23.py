# @url https://codeforces.com/problemset/problem/1117/C
# @primary binary-search-on-answer
# @topics binary-search-on-answer, string-simulation
# @rating 1900
# @division div2
# @note
# Idea: Binary search the minimum number of days. For each candidate x, compute the wind displacement from x // N complete forecast cycles and simulate the remaining x % N days, then check whether the destination is within Manhattan distance x of the resulting position.
# Key observation: After x days of wind, the ship can compensate by at most x Manhattan-distance units through its own movement. Thus x is feasible exactly when the remaining Manhattan distance is at most x, and feasibility is monotonic.
# Complexity: O(N log V) time and O(N) space, where V = 10^18.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    sx, sy = map(int, input().split())
    ex, ey = map(int, input().split())

    n = int(input().strip())
    s = ' ' + input().strip()
    # ob erreichen kann
    nx, ny = ex - sx, ey - sy
    hx, hy = 0, 0
    for i in range(1, n + 1):
        # wind
        if s[i] == 'L': 
            hx -= 1
        elif s[i] == 'R': 
            hx += 1
        elif s[i] == 'U': 
            hy += 1
        else: 
            hy -= 1



    l = 0
    r = int(1e18)

    def check(x):

        k = x // n
        px, py = k * hx, k * hy
        day = x % n
        for i in range(1, day + 1):
            if s[i] == 'L': px -= 1
            elif s[i] == 'R': px += 1
            elif s[i] == 'U': py += 1
            else: py -= 1

        tx, ty = sx + px, sy + py
        nw = abs(ex - tx) + abs(ey - ty)

        return x >= nw

        pass

    if not check(r):
        print("-1")
        return
    
    while l < r:
        mid = (l + r) // 2
        if check(mid): r = mid
        else: l = mid + 1

    print(int(l))
    pass


if __name__ == "__main__":
    solve()