# @url https://atcoder.jp/contests/abc478/tasks/abc478_a
# @primary simulation
# @topics simulation, array
# @note
# Idea: Simulate distributing the M grapes one at a time. Repeatedly increment person k mod N and advance k until no grapes remain.
# Key observation: The recipients repeat periodically in the fixed order 1,2,...,N, so taking the distribution index modulo N directly identifies the next person.
# Complexity: O(M + N) time and O(N) space.
# @endnote
import sys

input = sys.stdin.readline


def solve():
    n, m = map(int, input().strip().split())
    res = [0] * (n)
    k = 0
    while m > 0:
        res[k % n] += 1
        k += 1
        m -= 1
    for i in res:
        print(i)
    pass


if __name__ == "__main__":
    solve()