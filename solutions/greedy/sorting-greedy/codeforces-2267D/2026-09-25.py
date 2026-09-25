# @url https://codeforces.com/contest/2267/problem/D
# @primary sorting-greedy
# @topics sorting-greedy, comparison-sorting, hash-map
# @note
# Idea: Separate values by their original index parity and sort both groups. Construct a candidate sequence by repeatedly taking the smallest available value of the required parity that is at least the previous value; after reaching n, rebuild the remaining values in descending order and continue by taking the largest valid value below the previous one.
# Key observation: Values can only be selected from the parity class required by the current position, so the construction greedily chooses the closest feasible value in the required direction while frequency maps prevent reusing elements.
# Complexity: O(N log N) time and O(N) space per test case.
# @endnote

import sys

input = sys.stdin.readline


def solve_case():
    n = int(input())

    a = [0] + list(map(int, input().strip().split()))
    od = {}
    ev = {}
    odl = []
    evl = []
    m = 1
    for i in range(1, n + 1):
        if i % 2 != 0: 
            od[a[i]] = od.get(a[i], 0) + 1
            odl.append(a[i])
        else: 
            if a[i] == n: m = 2
            evl.append(a[i])
            ev[a[i]] = ev.get(a[i], 0) + 1

    flag = 0

    for i in range(1, n):
        if a[i] < a[i - 1]: flag = 1
    if not flag: return "YES"
    

    odl = sorted(odl)
    evl = sorted(evl)
    resl = [0]
    flag = 0
    # flag == 0 的时候没有找到 n
    k, j = 0, 0
    cnt = 0
    # 找大的，找小的
    len_evl = len(evl)
    len_odl = len(odl)
    for i in range(1, n + 1):
        if flag == 0:
            if i % 2 == 0:
                while k < len_evl and evl[k] < resl[cnt]: k += 1
                if k < len_evl: 
                    resl.append(evl[k])
                    cnt += 1
                    ev[evl[k]] -= 1 #这个数有没有被用过
                    if evl[k] == n: flag = 1
                
            else:
                while j < len_odl and odl[j] < resl[cnt]: j += 1
                if j < len_odl: 
                    resl.append(odl[j])
                    cnt += 1
                    od[odl[j]] -= 1
                    if odl[j] == n: flag = 1
                
        else:
            if flag == 1:
                odll = []
                evll = []
                for ttt in ev:
                    if ev[ttt] > 0: evll.append(ttt)
                for ttt in od:
                    if od[ttt] > 0: odll.append(ttt)
                flag += 1
                k, j = 0, 0
                odll = sorted(odll, reverse=True)
                evll = sorted(evll, reverse=True)
                lk = len(evll)
                lj = len(odll)

                if i % 2 == 0:
                    while k < lk and evll[k] > resl[cnt]: k += 1
                    if k < lk: 
                        resl.append(evll[k])
                        cnt += 1
                else:
                    while j < lj and odll[j] > resl[cnt]: j += 1
                    if j < lj: 
                        resl.append(odll[j])
                        cnt += 1
            else:
                if i % 2 == 0:
                    while k < lk and evll[k] > resl[cnt]: k += 1
                    if k < lk: 
                        resl.append(evll[k])
                        cnt += 1
                else:
                    while j < lj and odll[j] > resl[cnt]: j += 1
                    if j < lj: 
                        resl.append(odll[j])
                        cnt += 1

    if len(resl) - 1 == n: return "YES"
    else: return "NO"
    pass


def main():
    t = int(input())

    for _ in range(t):
        print(solve_case())


if __name__ == "__main__":
    main()