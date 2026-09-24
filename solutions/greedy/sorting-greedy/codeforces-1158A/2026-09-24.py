# @url https://codeforces.com/problemset/problem/1158/A
# @primary sorting-greedy
# @topics sorting-greedy, comparison-sorting
# @rating 1500
# @division div1
# @note
# Idea: Reject the instance if the largest boy minimum exceeds the smallest girl maximum. Otherwise start from the baseline where every boy gives his minimum to every girl, then greedily add the extra amounts required to realize each girl's maximum while handling the smallest girl maximum separately when necessary.
# Key observation: All entries should remain at their boy minimum unless they must be increased to realize a girl's required maximum; these increases should use the largest boy minimum whenever possible, while preserving at least one occurrence of that boy's original minimum.
# Complexity: O(N log N + M log M) time and O(N + M) space.
# @endnote
import sys

input = sys.stdin.readline


def solve():
    n, m = map(int, input().strip().split())
    a = list(map(int, input().strip().split()))
    b = list(map(int, input().strip().split()))

    if max(a) > min(b):
        print(-1)
        return

    a = sorted(a, reverse=True)
    b = sorted(b, reverse=True)
    res = int(m * sum(a))

    for i in range(m):
        if b[i] > a[0] and i != m - 1: res += b[i] - a[0]
        if i == m - 1 and n > 1 and b[i] > a[0]: res += b[i] - a[1]

    print(res)            
    pass


if __name__ == "__main__":
    solve()