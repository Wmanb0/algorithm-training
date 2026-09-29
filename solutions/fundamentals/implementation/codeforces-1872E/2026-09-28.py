# @url https://codeforces.com/contest/1872/problem/E
# @primary implementation
# @topics implementation, array
# @rating 1500
# @division div3
# @note
# Idea: Compute the XOR of the values currently belonging to groups 0 and 1, and build a prefix XOR array over a. For a type-1 query, obtain the XOR of a[l..r] from the prefix array and XOR it into both group values; for a type-2 query, output the stored XOR of the requested group.
# Key observation: Flipping every bit of s on [l, r] moves every corresponding a[i] from one group to the other. Therefore the XOR of the entire interval must be removed from one group and added to the other, which is achieved by XORing the same interval value into both maintained group XORs.
# Complexity: O(N + Q) time and O(N) space per test case.
# @endnote
import sys

input = sys.stdin.readline


def solve_case():

    n = int(input().strip())
    a = [0] + list(map(int, input().strip().split()))
    s = '2' + input().strip()
    q = int(input().strip())

    x0 = 0
    x1 = 0
    v = [0]
    for i in range(1, n + 1):
        if s[i] == '0': x0 ^= a[i]
        else: x1 ^= a[i]
        v.append(v[i - 1] ^ a[i])

    for _ in range(q):
        op = input().strip().split()
        if op[0] == '2':
            if op[1] == '1': print(x1, end=' ')
            else: print(x0, end=' ')
            pass
        else:
            l, r = int(op[1]), int(op[2])

            V = v[r] ^ v[l - 1]
            x0 ^= V
            x1 ^= V
    print()
    pass


def main():
    t = int(input())

    for _ in range(t):
        solve_case()


if __name__ == "__main__":
    main()