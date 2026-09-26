# @url https://atcoder.jp/contests/abc477/tasks/abc477_d
# @primary offline-processing
# @topics offline-processing, hash-set, simulation
# @note
# Idea: Store all operations and process them in reverse. Maintain a set of positions whose final color is not yet determined; when a painting operation is encountered, assign its color to every currently unresolved exposed position, and reverse toggle operations update which positions are exposed.
# Key observation: Once a position receives its final color during reverse processing, it never needs to be colored again. Therefore each position is processed by the painting loops at most once overall.
# Complexity: O(N + Q) expected time and O(N + Q) space.
# @endnote

import sys

input = sys.stdin.readline


def solve():
    n, q = map(int, input().strip().split())
    s = [[0, []] for _ in range(n + 5)]
    op = []
    color = [[0, 'a']]
    for _ in range(q):
        a, b = input().strip().split()
        a = int(a)
        if a == 1: 
            op.append([a, int(b)])
            s[int(b)][0] ^= 1   # 找上一次违背盖住
        else: 
            color.append([_ + 1, b])
            op.append([a, b])
    

    res = ['a' for _ in range(n + 5)]
    last = [0 for _ in range(n + 5)] #是否确定
    ss = set()
    for i in range(1, n + 1):
        if s[i][0] == 0:  #要是没有被盖住的话
            ss.add(i)

    # 倒着找
    for i in range(q - 1, -1, -1):
        a, b = op[i][0], op[i][1]

        if a == 2: #如果涂色了
            for j in ss:  #就把没旗子的涂上去
                res[j] = b
                last[j] = 1
            ss.clear()
        else:
            if s[b][0] == 1:
                s[b][0] = 0
                if last[b] == 0:
                    ss.add(b)
            else:
                s[b][0] = 1
                ss.discard(b)

    for i in range(1, n + 1):
        print(res[i], end='')
    pass


if __name__ == "__main__":
    solve()