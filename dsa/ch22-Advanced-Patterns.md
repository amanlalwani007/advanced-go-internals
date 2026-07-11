# Chapter 22 — Advanced Patterns (K-way Merge, Ordered Set, Sweep Line)

## Overview
Less common but important patterns: K-way merge (merge K sorted lists), ordered set (TreeMap for range queries), sweep line (interval events), Reservoir sampling, Quickselect.

---

## MCQ

### Q1: K-way merge combines K sorted arrays into one sorted array. What is its time complexity?

**Options:**
- O(K * N)
- O(NK log K) using a min-heap of K elements
- O(N log K)
- O(K log N)

**Answer:** O(NK log K) using a min-heap of K elements, where N is the average length of each list.

---

## Coding Problems

### Problem 1: Quickselect (Kth Largest Element)

```go
func findKthLargest(nums []int, k int) int {
    target := len(nums) - k
    left, right := 0, len(nums)-1
    for {
        pivotIdx := partition(nums, left, right)
        if pivotIdx == target {
            return nums[pivotIdx]
        } else if pivotIdx < target {
            left = pivotIdx + 1
        } else {
            right = pivotIdx - 1
        }
    }
}

func partition(nums []int, left, right int) int {
    pivot := nums[right]
    i := left
    for j := left; j < right; j++ {
        if nums[j] <= pivot {
            nums[i], nums[j] = nums[j], nums[i]
            i++
        }
    }
    nums[i], nums[right] = nums[right], nums[i]
    return i
}
```

### Problem 2: Sweep Line — The Skyline Problem (Outline)

```go
func getSkyline(buildings [][]int) [][]int {
    type event struct{ x, h int; start bool }
    events := make([]event, 0, len(buildings)*2)
    for _, b := range buildings {
        events = append(events, event{b[0], b[2], true})
        events = append(events, event{b[1], b[2], false})
    }
    sort.Slice(events, func(i, j int) bool {
        if events[i].x != events[j].x { return events[i].x < events[j].x }
        if events[i].start != events[j].start {
            if events[i].start { return true } // start before end at same x
            return false
        }
        if events[i].start { return events[i].h > events[j].h } // higher start first
        return events[i].h < events[j].h // lower end first
    })
    heights := &MaxIntHeap{}
    heap.Init(heights)
    heap.Push(heights, 0)
    prevMax := 0
    var result [][]int
    for _, e := range events {
        if e.start {
            heap.Push(heights, e.h)
        } else {
            removeFromHeap(heights, e.h)
        }
        currMax := heights.Peek()
        if currMax != prevMax {
            result = append(result, []int{e.x, currMax})
            prevMax = currMax
        }
    }
    return result
}

type MaxIntHeap []int
func (h MaxIntHeap) Len() int { return len(h) }
func (h MaxIntHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h MaxIntHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *MaxIntHeap) Push(x interface{}) { *h = append(*h, x.(int)) }
func (h *MaxIntHeap) Pop() interface{} {
    old := *h; n := len(old); x := old[n-1]; *h = old[:n-1]; return x
}
func (h MaxIntHeap) Peek() int { return h[0] }

func removeFromHeap(h *MaxIntHeap, val int) {
    for i, v := range *h {
        if v == val {
            heap.Remove(h, i)
            break
        }
    }
}
```

### Problem 3: Find Median from Data Stream (Ordered Set approach using two heaps — see ch14)

### Problem 4: Reservoir Sampling — Random Pick Index

```go
type Solution struct {
    nums []int
}

func Constructor(nums []int) Solution {
    return Solution{nums: nums}
}

func (s *Solution) Pick(target int) int {
    count, result := 0, 0
    for i, num := range s.nums {
        if num == target {
            count++
            if rand.Intn(count) == 0 {
                result = i
            }
        }
    }
    return result
}
```
