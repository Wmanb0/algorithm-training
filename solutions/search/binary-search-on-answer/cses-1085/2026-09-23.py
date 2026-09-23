# @url https://cses.fi/problemset/task/1085/
# @primary binary-search-on-answer
# @topics binary-search-on-answer, general-greedy
# @note
# Idea: Binary search the minimum possible maximum subarray sum. For each candidate value, greedily extend the current subarray while its sum stays within the limit, starting a new subarray whenever adding the next value would exceed it.
# Key observation: For a fixed maximum sum x, greedily making each subarray as long as possible minimizes the number of required subarrays. If x is feasible using at most K subarrays, every larger value is also feasible.
# Complexity: O(N log V) time and O(N) space, where V = sum(a) - max(a) + 1.
# @endnote
import sys
input = sys.stdin.readline


def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    l = max(a)
    r = sum(a)

    def check(x):
        groups = 1
        cur = 0

        for v in a:
            if cur + v <= x:
                cur += v
            else:
                groups += 1
                cur = v

        return groups <= k

    while l < r:
        mid = (l + r) // 2

        if check(mid): r = mid
        else: l = mid + 1

    print(l)


if __name__ == "__main__":
    solve()