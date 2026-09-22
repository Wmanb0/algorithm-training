# @url https://usaco.org/index.php?page=viewproblem2&cpid=594&lang=en
# @primary binary-search-on-answer
# @topics binary-search-on-answer, interval-covering, comparison-sorting
# @note
# Idea: Sort the haybale positions and binary search the minimum explosion radius. For each candidate radius, greedily start coverage from the leftmost uncovered haybale and cover every haybale within an interval of length 2R before using another cow.
# Key observation: Covering the leftmost uncovered haybale as far to the right as possible is optimal for a fixed radius, and if radius R is feasible then every larger radius is also feasible.
# Complexity: O(N log N + N log V) time and O(N) space.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    n, k = map(int, input().split())
    a = [-1] 
    for _ in range(n):
        a.append(int(input().rstrip()))
    a = sorted(a)

    l = 0
    r = 1e10

    def check(x):

        i = 0
        now = 1
        right = a[1] + 2 * x
        while i <= n:
            
            i += 1
            if i <= n and a[i] > right:
                now += 1
                if now > k: return False
                right = a[i] + 2 * x
        
        return True
            
    while l < r:
        mid = (l + r) // 2
        if check(mid): r = mid
        else: l = mid + 1
    
    print(int(l))
    pass


if __name__ == "__main__":
    solve()