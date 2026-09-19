/*
@url https://leetcode.com/problems/min-stack/
@primary stack
@topics array, implementation
@note
核心思路：
栈中的每个元素同时保存两个值：
1. 当前压入的实际数值。
2. 从栈底到当前位置为止的最小值。

push 时，新位置的最小值等于 min(val, 之前的最小值)。
pop 时，数值和对应的最小值一起删除。
因此 top 和 getMin 都只需要访问最后一个元素，不需要重新遍历整个栈。

状态表示：
st[i][0] 表示第 i 个元素的实际值。
st[i][1] 表示包含第 i 个元素在内的整个栈的最小值。

复杂度：
push、pop、top、getMin 的时间复杂度均为 O(1)。
保存 n 个元素的空间复杂度为 O(n)。

复习重点：
把需要快速查询的历史状态与每个栈元素一起保存。
这是典型的“辅助状态随主状态同步入栈和出栈”模型。
@endnote
*/

#include <algorithm>
#include <array>
#include <vector>
using namespace std;

class MinStack {
private:
    vector<array<int, 2>> st;

public:
    MinStack() = default;

    void push(int val) {
        const int minimum = st.empty() ? val : min(val, st.back()[1]);
        st.push_back({val, minimum});
    }

    void pop() {
        st.pop_back();
    }

    int top() {
        return st.back()[0];
    }

    int getMin() {
        return st.back()[1];
    }
};

