# @url https://atcoder.jp/contests/abc474/tasks/abc474_a
# @primary arithmetic
# @note
# Idea: Compute the answer directly using N modulo 3.
# Key observation: The required result repeats with period 3, so N % 3 + 1 gives the answer.
# Complexity: O(1) time and O(1) space.
# @endnote

n = int(input())
print(n % 3 + 1)