# @url https://codeforces.com/contest/2254/problem/B
# @primary string-simulation
# @topics string-simulation
# @rating 900
# @division div3
# @note
# Idea: Scan the string to choose an internal character whose removal can best merge neighboring runs. Then rebuild the compressed string while skipping that position and output its resulting length.
# Key observation: Deleting one internal character can only affect the runs containing that character and its two neighbors, so the useful deletion is determined by the local pattern around the removed position.
# Complexity: O(N^2) worst-case time and O(N) space per test case.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n = int(input().strip())
    s = input().strip()
    k = 0
    idx = -1
    for i in range(1, n - 1):
        if s[i] != s[i - 1] and s[i] != s[i + 1] and k == 0:
            k = 1
            idx = i
        if s[i] != s[i - 1] and s[i] != s[i + 1] and s[i + 1] == s[i - 1]:
            k = 2
            idx = i

    ss = s[0]
    kk = 1
    for i in range(1, n):
        if s[i] != ss[kk - 1] and i != idx: 
            ss += s[i]
            kk += 1
    print(len(ss))
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()