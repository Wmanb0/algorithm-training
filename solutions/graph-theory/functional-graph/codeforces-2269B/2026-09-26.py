# @url https://codeforces.com/contest/2269/problem/B
# @primary functional-graph
# @topics functional-graph, hash-map, simulation
# @division div2
# @note
# Idea: For every starting number, repeatedly replace it by the sum of squares of its digits while storing visited states and their indices until reaching either a fixed point or a cycle. Then compare every pair using their fixed points or their states at a common time inside their eventual cycles.
# Key observation: The digit-square transformation is deterministic, so every starting value eventually enters a fixed point or directed cycle. Two sequences are permanently identical exactly when they reach the same state at the same time and therefore follow the same deterministic suffix forever.
# Complexity: O(NL + N^2) time and O(NL) space per test case, where L is the maximum generated sequence length before repetition.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n = int(input().strip())
    a = [0] + input().strip().split()
    b = [0] * (n + 1)
    def solve(x):

        t = 0
        last = t
        for i in x:
            t += int(i) * int(i)
        k = {}
        p = []
        q = 0
        while t != last and k.get(t, -1) == -1:
            last = t
            k[last] = q
            p.append(last)
            q += 1

            t = 0
            for i in str(last):
                t += int(i) * int(i)


        if t == last: return [True, t]
        else: return [False, q, p, k[t]]

    for i in range(1, n + 1):
        b[i] = solve(a[i])

    res = 0
    for i in range(1, n):
        if b[i][0] == True:
            for j in range(i + 1, n + 1):
                if b[j][0] == True and b[j][1] == b[i][1]: res += 1
        else:
            for j in range(i + 1, n + 1):
                if b[j][0] == False:
                    l = max(b[i][3], b[j][3])

                    if l < b[i][1]:
                        x = b[i][2][l]
                    else:
                        x = b[i][2][b[i][3] + (l - b[i][3]) % (b[i][1] - b[i][3])]

                    
                    if l < b[j][1]:
                        y = b[j][2][l]
                    else:
                        y = b[j][2][b[j][3] + (l - b[j][3]) % (b[j][1] - b[j][3])]
                        
                    if x == y:
                        res += 1
    print(res)
    
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()