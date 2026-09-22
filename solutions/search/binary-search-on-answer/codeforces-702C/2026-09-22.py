# @url https://codeforces.com/contest/702/problem/C
# @primary binary-search-on-answer
# @topics binary-search-on-answer, two-pointers, comparison-sorting
# @rating 1500
# @division div1, div2
# @note
# Idea: Sort the city and tower positions, then binary search the minimum radius. For each candidate radius, scan the cities and towers with two pointers and advance past every city covered by the current tower.
# Key observation: If radius r covers every city, then every radius greater than r is also feasible, so the feasibility condition is monotonic and can be binary searched.
# Complexity: O(N log N + M log M + (N + M) log V) time and O(N + M) space.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    n, m = map(int, input().split())
    a = [-2e11] + list(map(int, input().split()))
    b = [-2e11] + list(map(int, input().split()))

    a = sorted(a)
    b = sorted(b)

    l = 0
    r = 2e10

    def check(x):

        i = 1
        j = 1

        while j <= m and i <= n:

            while i <= n and  j <= m and (b[j] - x <= a[i] <= b[j] + x): i += 1

            j += 1
        
        if i > n: return True
        else: return False


    while l < r:
        mid = (l + r) // 2
        if check(mid): r = mid
        else: l = mid + 1

    
    print(int(l))
    pass


if __name__ == "__main__":
    solve()