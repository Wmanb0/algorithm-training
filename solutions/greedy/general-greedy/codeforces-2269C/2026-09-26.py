# @url https://codeforces.com/contest/2269/problem/C
# @primary general-greedy
# @topics general-greedy, arithmetic
# @division div2
# @note
# Idea: Compute the total array sum and determine the minimum value that must remain uncollected. For each symmetric pair that can contribute one surviving element, subtract the smaller value, and when the middle section is forced to remain, subtract those elements as well.
# Key observation: The operation structure determines which symmetric positions compete for a surviving slot, so maximizing the collected score is equivalent to minimizing the remaining sum by keeping the smaller value from every available symmetric pair.
# Complexity: O(N) time and O(N) space per test case.
# @endnote
import sys

input = sys.stdin.readline


def solve_case():
    n, k = map(int, input().strip().split())
    a = [0] + list(map(int, input().strip().split()))
    if k == 1:
        print(sum(a))
        return

    d = n - k + 1
    t = min(d, k - 1)

    val = 0
    for i in range(1, t + 1):
        val += min(a[i], a[n - i + 1])

    if k - 1 > d:
        for i in range(d + 1, n - d + 1):
            val += a[i]
    
    print(sum(a) - val)
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()