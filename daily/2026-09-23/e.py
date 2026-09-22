# @url https://usaco.org/index.php?page=viewproblem2&cpid=597
# @primary category/subcategory
# @topics topic1, topic2
# @note
# Solution idea
# @endnote

import sys

input = sys.stdin.readline


def solve():

    n = int(input())
    b = [-1]
    for _ in range(n):
        b.append(int(input().strip()))
    b = sorted(b)
    
    if n == 1:
        print("{:.1f}".format(0))
        return
    L = [0] * (n + 5)
    R = [0] * (n + 5)
    
    for i in range(2, n + 1):
        L[i] = max(L[i - 1], b[i] - b[i - 1])
    for i in range(n - 1, 0, - 1):
        R[i] = max(R[i + 1], b[i + 1] - b[i])

    start = (b[1] + b[2]) / 2
    val = max(L[1], R[2])
    TG = 1
    for i in range(2, n):
        if max(L[1], R[i + 1]) < val:
            val = max(L[1], R[i + 1])
            start = (b[i] + b[i + 1]) / 2
            TG = i
    l = 0
    r = 1e10
    
    sp = 1
    for i in range(1, n + 1):
        if b[i] >= start:
            sp = i
            break
    def check(x):

        i = sp # 第一个大于 >= 的点
        phase = 0
        st = start
        last = start
        # 找左边
        while i >= 1:
            # 如果当前b[i] 可以通过第 phase 次爆炸到达
            if i >= 1:
                if b[i] >= st - (x - phase): 
                    last = i #记录一下这个点
                    i -= 1
                else:  # 如果通过 第 phase 次无法到达
                    phase += 1 # 阶段 + 1
                    st = b[last] #爆炸的扩散点应该是上一个草堆的点
                    if b[i] < st - (x - phase): #如果还无法到达
                        return False
                    else:
                        last = i
                        i -= 1
        # 找右边
        j = sp
        st = start
        jlast = start
        phasej = 0
        while j <= n:
            # 如果当前b[j] 可以通过第 phase 次爆炸到达
            if j <= n:
                if b[j] <= st + (x - phasej):
                    jlast = j
                    j += 1     
                else:    # 如果通过 第 phase 次无法到达
                    phasej += 1 # 阶段 + 1
                    st = b[jlast] #爆炸的扩散点应该是上一个草堆的点
                    if b[j] > st + (x - phasej): #如果还无法到达
                        return False
                    else:
                        jlast = j
                        j += 1        

        if i < 1 and j > n: return True
        else: return False

    esp = 1e-8
    while r - l < esp:
        mid = (l + r) / 2
        if check(mid): r = mid
        else: l = mid

    print("{:.1f}".format(min(L[TG], R[TG + 1], l)))
    pass


if __name__ == "__main__":
    solve()