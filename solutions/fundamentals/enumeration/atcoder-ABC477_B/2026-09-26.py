# @url https://atcoder.jp/contests/abc477/tasks/abc477_b
# @primary enumeration
# @topics enumeration, array
# @note
# Idea: For every person, scan all other people and check whether any distance is smaller than D. Output the indices for which no such person exists.
# Key observation: A person is valid exactly when every pairwise distance from that person to another person is at least D, so checking all ordered pairs directly is sufficient.
# Complexity: O(N^2) time and O(N) space.
# @endnote
import sys

input = sys.stdin.readline


def solve():
    n, d = map(int, input().strip().split())
    a = list(map(int, input().strip().split()))

    res = []
    for i in range(n):
        t = 0
        for j in range(n):
            if j != i:
                if abs(a[i] - a[j]) < d:
                    t = 1
        if t == 0: res.append(i + 1)

    if len(res) == 0:print(0)
    else:
        print(len(res))
        print(*res, end = ' ')

    pass


if __name__ == "__main__":
    solve()