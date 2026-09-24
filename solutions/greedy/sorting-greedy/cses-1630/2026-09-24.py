# @url https://cses.fi/problemset/task/1630
# @primary sorting-greedy
# @topics sorting-greedy, comparison-sorting
# @note
# Idea: Sort the tasks by duration in ascending order, execute them in that order, and accumulate each reward as deadline minus its completion time.
# Key observation: The sum of deadlines is independent of task order, so maximizing total reward is equivalent to minimizing the sum of completion times; placing shorter tasks before longer tasks minimizes that sum.
# Complexity: O(N log N) time and O(N) space.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    n = int(input().strip())
    t = []
    for _ in range(n):
        a, d = map(int, input().split())
        t.append([a, d])
    t = sorted(t, key=lambda x : (x[0], -x[1]))
    res = 0
    now = 0

    for i in range(n):
        now += t[i][0] 
        res += t[i][1] - now

    print(res)

    pass


if __name__ == "__main__":
    solve()