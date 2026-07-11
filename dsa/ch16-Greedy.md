# Chapter 16 — Greedy Pattern

## Overview
Greedy algorithms make locally optimal choices at each step, aiming for a global optimum. Works when the problem has the "greedy choice property" and "optimal substructure".

**Examples:** Interval scheduling, coin change (canonical systems), Huffman coding, Dijkstra's algorithm.

---

## MCQ

### Q1: A greedy algorithm always produces the globally optimal solution when:

**Options:**
- The problem has optimal substructure and the greedy choice property.
- The input is sorted in ascending order.
- The problem is NP-hard.
- The problem constraints are small enough for brute force.

**Answer:** The problem has optimal substructure and the greedy choice property.

---

### Q2: Which problem is a classic counterexample where greedy fails?

**Options:**
- Activity selection (maximum non-overlapping intervals).
- Minimum spanning tree (Kruskal's / Prim's).
- 0/1 Knapsack (not fractional).
- Huffman coding.

**Answer:** 0/1 Knapsack (not fractional). Greedy fails because taking the most valuable per weight item doesn't guarantee optimality due to the 0/1 constraint.

---

## Coding Problems

### Problem 1: Jump Game II (Minimum Jumps)

```go
func jump(nums []int) int {
    jumps, currEnd, farthest := 0, 0, 0
    for i := 0; i < len(nums)-1; i++ {
        farthest = max(farthest, i+nums[i])
        if i == currEnd {
            jumps++
            currEnd = farthest
        }
    }
    return jumps
}
```

### Problem 2: Gas Station

```go
func canCompleteCircuit(gas []int, cost []int) int {
    total, tank, start := 0, 0, 0
    for i := 0; i < len(gas); i++ {
        diff := gas[i] - cost[i]
        total += diff
        tank += diff
        if tank < 0 {
            start = i + 1
            tank = 0
        }
    }
    if total < 0 { return -1 }
    return start
}
```

### Problem 3: Interval Scheduling Maximization (Non-overlapping Intervals)

```go
func eraseOverlapIntervals(intervals [][]int) int {
    if len(intervals) == 0 { return 0 }
    sort.Slice(intervals, func(i, j int) bool {
        return intervals[i][1] < intervals[j][1]
    })
    count, end := 1, intervals[0][1]
    for i := 1; i < len(intervals); i++ {
        if intervals[i][0] >= end {
            count++
            end = intervals[i][1]
        }
    }
    return len(intervals) - count
}
```

### Problem 4: Task Scheduler

```go
func leastInterval(tasks []byte, n int) int {
    freq := make([]int, 26)
    for _, t := range tasks {
        freq[t-'A']++
    }
    sort.Slice(freq, func(i, j int) bool { return freq[i] > freq[j] })
    maxFreq := freq[0]
    idle := (maxFreq - 1) * n
    for i := 1; i < 26 && freq[i] > 0; i++ {
        idle -= min(maxFreq-1, freq[i])
    }
    if idle < 0 { idle = 0 }
    return len(tasks) + idle
}
```

### Problem 5: Partition Labels

```go
func partitionLabels(s string) []int {
    last := make([]int, 26)
    for i, ch := range s {
        last[ch-'a'] = i
    }
    var result []int
    start, end := 0, 0
    for i, ch := range s {
        end = max(end, last[ch-'a'])
        if i == end {
            result = append(result, end-start+1)
            start = i + 1
        }
    }
    return result
}
```
