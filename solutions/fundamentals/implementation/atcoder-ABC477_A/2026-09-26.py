# @url https://atcoder.jp/contests/abc477/tasks/abc477_a
# @primary implementation
# @topics implementation
# @note
# Idea: Read the current traffic-light color and directly output the next color in the fixed cycle B -> Y -> R -> B.
# Key observation: There are only three possible input states, so the next state can be determined with constant-time case analysis.
# Complexity: O(1) time and O(1) space.
# @endnote
import sys

input = sys.stdin.readline


def solve():
    c = input().strip()
    
    if c == 'B':print("Y")
    elif c == 'Y': print("R")
    else:print("B")
    pass


if __name__ == "__main__":
    solve()