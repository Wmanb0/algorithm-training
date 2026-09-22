# @url https://usaco.org/index.php?page=viewproblem2&cpid=858&lang=zh
# @primary binary-search-on-answer
# @topics binary-search-on-answer, sorting-greedy, comparison-sorting
# @note
# Idea: Sort the cow arrival times and binary search the minimum allowed maximum waiting time. For each candidate value, greedily process cows from left to right, filling the current bus before starting the next one when the waiting-time or capacity condition requires it.
# Key observation: If all cows can be transported with maximum waiting time x using at most M buses, then any larger waiting time is also feasible, so feasibility is monotonic.
# Complexity: O(N log N + N log V) time and O(N) space.
# @endnote
import sys

input = sys.stdin.readline


def solve():
    iiii = input()
    n, m, c = map(int, input().split())
    t = [-1] + list(map(int, input().split()))

    t = sorted(t)

    l = 0
    r = 1e10

    def check(x):

        now = 1
        mval = t[1] + x
        h = 0
        for i in range(1, n + 1):
            # need new car
            if t[i] > mval or h > c:
                now += 1
                mval = t[i] + x
                h = 1
                if now > m: return False
                continue

            h += 1


        return True

    while l < r:
        mid = (l + r) // 2
        if check(mid): r = mid
        else: l = mid + 1

    print(int(l))
    pass


if __name__ == "__main__":
    solve()