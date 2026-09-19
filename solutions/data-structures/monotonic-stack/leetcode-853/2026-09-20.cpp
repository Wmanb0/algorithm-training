/*
@url https://leetcode.com/problems/car-fleet/
@primary monotonic-stack
@topics comparison-sorting, ordered-map, general-greedy
@note
核心思路：
按照车辆与终点的距离，从最靠近终点的车辆开始向后处理。
每辆车单独到达终点所需时间为 (target - position[i]) / speed[i]。

如果后车的到达时间小于等于前方车队的到达时间，它一定会在终点前
或恰好在终点追上前方车队，因此不会形成新的车队。
只有当前车辆的到达时间严格大于前方最后一个车队的到达时间时，
才会产生一个新的车队。

代码中使用 map 的负位置作为键，使遍历顺序从位置最大到位置最小。
到达时间形成单调序列；由于这里只需要统计车队数量，所以不需要保存
完整的单调栈，只需要保存当前最后一个车队的到达时间 cur。

复杂度：
时间复杂度 O(n log n)，其中排序由 map 完成。
空间复杂度 O(n)。

复习重点：
1. 必须从最靠近终点的车辆向后判断。
2. 相同到达时间属于同一个车队，所以只有 time > cur 时答案才加一。
3. 这道题虽然代码没有显式使用 stack，但本质是 Monotonic Stack 模型。
@endnote
*/

#include <map>
#include <vector>
using namespace std;

class Solution {
public:
    int carFleet(int target, vector<int>& position, vector<int>& speed) {
        map<int, double> cars;

        const int n = static_cast<int>(position.size());
        for (int i = 0; i < n; ++i) {
            cars[-position[i]] =
                static_cast<double>(target - position[i]) / speed[i];
        }

        int fleets = 0;
        double latestArrivalTime = 0.0;

        for (const auto& [negativePosition, arrivalTime] : cars) {
            (void)negativePosition;
            if (arrivalTime > latestArrivalTime) {
                latestArrivalTime = arrivalTime;
                ++fleets;
            }
        }

        return fleets;
    }
};

