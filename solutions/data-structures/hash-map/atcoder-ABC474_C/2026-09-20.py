
# @url https://atcoder.jp/contests/abc474/tasks/abc474_c
# @primary hash-map
# @topics comparison-sorting
# @note
# Idea: Store the latest timestamp of each value in a hash map, overwrite it whenever the value appears again, then sort values by their final timestamps.
# Key observation: The final timestamp represents the last position of each distinct value after processing all updates.
# Complexity: O(N + Q + M log M) time and O(M) space, where M is the number of distinct values.
# @endnote


n, q = map(int, input().split())
a = list(map(int, input().split()))
k = {}
t = 1
for i in a:
    k[i] = t
    t += 1
for i in range(q):
    m = int(input())
    k[m] = t
    t += 1

k = dict(sorted(k.items(), key=lambda x: x[1]))
for v in k:
    print(v, end = ' ')
