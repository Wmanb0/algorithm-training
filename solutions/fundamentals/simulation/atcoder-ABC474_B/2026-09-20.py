# @url https://atcoder.jp/contests/abc474/tasks/abc474_b
# @primary simulation
# @note
# Idea: Scan the sequence from left to right and increase the available threshold by 10 at every index divisible by 10.
# Key observation: The answer is "Yes" only if every A[i] is at most the threshold available at its position.
# Complexity: O(N) time and O(N) space.
# @endnote

n = int(input())
a = list(map(int, input().split()))
T = 0
res = "Yes"
for i in range(n):
    if i % 10 == 0: T += 10

    if a[i] > T:
        res = "No"

print(res)