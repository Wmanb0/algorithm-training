
# @url https://codeforces.com/contest/2008/problem/E
# @primary enumeration
# @topics case-analysis, incremental-construction
# @note
# Idea: For even length, independently choose the most frequent character on odd and even positions. For odd length, enumerate the deleted position while maintaining character frequencies on the left and right.
# Key observation: After deleting one character, the parity of every position to its right is reversed, so the resulting odd-position count combines left odd positions with right even positions, and vice versa.
# Complexity: O(26N) time and O(26) space per test case.
# @endnote


import sys

input = sys.stdin.readline


def solve_case():
    n = int(input())
    s = ' ' + input().strip()
    res = 0

    al = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    
    if n % 2 == 0:
        od = {}
        ev = {}
        for i in range(1, n + 1):
            if i % 2 == 0: ev[s[i]] = ev.get(s[i], 0) + 1
            else : od[s[i]] = od.get(s[i], 0) + 1
        
        res = n - max(od.values()) - max(ev.values())
    else:
        res = 1e6 
        od = {}
        ev = {}
        for i in range(1, n + 1):
            if i % 2 == 0: ev[s[i]] = ev.get(s[i], 0) + 1
            else : od[s[i]] = od.get(s[i], 0) + 1
        # od ev分别是,奇数位偶数位最多的字母, 且不删
        lfod = {}
        lfev = {}
        # 这两个是从做往右枚举的
        for i in range(1, n + 1):
            # 枚举删第 i 个, 如果要删，带来的影响是后面奇数位偶数位互换

            # 1. 首先把自己删掉
            if i % 2 == 0: ev[s[i]] = max(0, ev.get(s[i], 0) - 1)
            else :         od[s[i]] = max(0, od.get(s[i], 0) - 1)

            res_od, res_ev = {}, {}
            # 2. 算左边和右边的值, 因为奇偶互换了所以左奇数加右偶数,左偶数加右奇数
            for j in al:
                res_ev[j] = lfev.get(j, 0) + od.get(j, 0)
                res_od[j] = lfod.get(j, 0) + ev.get(j, 0)

            # 3. 计算当前删掉 第 i 个 的答案
            res = min(res, n - max(res_od.values()) - max(res_ev.values()))

            #还原
            # 如果删的是 第 i + 1 个，是需要lfod\lfev存档的左, 没有删除的奇偶性是不改变的
            if i % 2 == 0: lfev[s[i]] = lfev.get(s[i], 0) + 1
            else : lfod[s[i]] = lfod.get(s[i], 0) + 1

        res = max(1, res)

    return res



def main():
    t = int(input())

    for _ in range(t):
        print(solve_case())


if __name__ == "__main__":
    main()