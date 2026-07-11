# Chapter 5 — Merge Intervals Pattern

## Overview
Merge Intervals deals with overlapping intervals. The core approach is: sort by start time, then iterate, merging overlapping intervals by extending the end time.

**Time Complexity:** O(n log n) — dominated by sorting
**Space Complexity:** O(n) for result storage

---

## MCQ

### Q1: What is the first step in solving any "merge intervals" problem?

**Options:**
- Reverse the list of intervals.
- Sort the intervals by their end value.
- Sort the intervals by their start value.
- Remove all intervals with negative values.

**Answer:** Sort the intervals by their start value.

---

### Q2: Two intervals [a1, a2] and [b1, b2] overlap if:

**Options:**
- a1 == b2
- a2 >= b1
- a2 < b1
- a1 > b2 && b1 < a2

**Answer:** a2 >= b1 (assuming sorted by start, so a1 <= b1)

---

## Coding Problems

### Problem 1: Merge Overlapping Intervals

```go
type Interval struct {
    Start, End int
}

func merge(intervals [][]int) [][]int {
    if len(intervals) <= 1 {
        return intervals
    }
    sort.Slice(intervals, func(i, j int) bool {
        return intervals[i][0] < intervals[j][0]
    })
    result := [][]int{intervals[0]}
    for i := 1; i < len(intervals); i++ {
        last := result[len(result)-1]
        if intervals[i][0] <= last[1] {
            // overlap — merge
            if intervals[i][1] > last[1] {
                last[1] = intervals[i][1]
            }
        } else {
            result = append(result, intervals[i])
        }
    }
    return result
}
```

### Problem 2: Insert Interval

```go
func insert(intervals [][]int, newInterval []int) [][]int {
    var result [][]int
    i := 0
    // add all intervals ending before new interval starts
    for i < len(intervals) && intervals[i][1] < newInterval[0] {
        result = append(result, intervals[i])
        i++
    }
    // merge overlapping intervals
    for i < len(intervals) && intervals[i][0] <= newInterval[1] {
        newInterval[0] = min(newInterval[0], intervals[i][0])
        newInterval[1] = max(newInterval[1], intervals[i][1])
        i++
    }
    result = append(result, newInterval)
    // add remaining
    for i < len(intervals) {
        result = append(result, intervals[i])
        i++
    }
    return result
}
```

### Problem 3: Non-Overlapping Intervals (find min to remove)

```go
func eraseOverlapIntervals(intervals [][]int) int {
    if len(intervals) == 0 {
        return 0
    }
    sort.Slice(intervals, func(i, j int) bool {
        return intervals[i][1] < intervals[j][1]
    })
    count := 1 // non-overlapping count
    end := intervals[0][1]
    for i := 1; i < len(intervals); i++ {
        if intervals[i][0] >= end {
            count++
            end = intervals[i][1]
        }
    }
    return len(intervals) - count
}
```

### Problem 4: Meeting Rooms II (Min Conference Rooms)

```go
func minMeetingRooms(intervals [][]int) int {
    starts := make([]int, len(intervals))
    ends := make([]int, len(intervals))
    for i, iv := range intervals {
        starts[i] = iv[0]
        ends[i] = iv[1]
    }
    sort.Ints(starts)
    sort.Ints(ends)
    rooms, endIdx := 0, 0
    for i := 0; i < len(starts); i++ {
        if starts[i] < ends[endIdx] {
            rooms++
        } else {
            endIdx++
        }
    }
    return rooms
}
```
