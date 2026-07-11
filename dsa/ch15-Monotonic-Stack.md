# Chapter 15 — Monotonic Stack Pattern

## Overview
A monotonic stack maintains elements in increasing or decreasing order. It is used for problems involving "next greater element", "previous smaller element", and similar range queries.

**Time Complexity:** O(n)
**Space Complexity:** O(n)

---

## MCQ

### Q1: A monotonic stack is particularly well-suited for:

**Options:**
- Sorting an array in O(n log n).
- Finding the next greater/smaller element for each position in O(n).
- Detecting cycles in a graph.
- Finding the shortest path between two nodes.

**Answer:** Finding the next greater/smaller element for each position in O(n).

---

### Q2: In a monotonic decreasing stack, when encountering an element larger than the stack's top, what happens?

**Options:**
- The new element is pushed directly.
- Elements are popped from the stack until the stack's top is larger than the new element, then push the new element.
- The stack is cleared and reset.
- The new element is ignored.

**Answer:** Elements are popped from the stack until the stack's top is larger than the new element, then push the new element.

---

## Coding Problems

### Problem 1: Next Greater Element I

```go
func nextGreaterElement(nums1 []int, nums2 []int) []int {
    nextGreater := make(map[int]int)
    stack := make([]int, 0)
    for _, num := range nums2 {
        for len(stack) > 0 && stack[len(stack)-1] < num {
            top := stack[len(stack)-1]
            stack = stack[:len(stack)-1]
            nextGreater[top] = num
        }
        stack = append(stack, num)
    }
    result := make([]int, len(nums1))
    for i, num := range nums1 {
        if val, ok := nextGreater[num]; ok {
            result[i] = val
        } else {
            result[i] = -1
        }
    }
    return result
}
```

### Problem 2: Daily Temperatures (Next Greater Element Distance)

```go
func dailyTemperatures(temperatures []int) []int {
    n := len(temperatures)
    result := make([]int, n)
    stack := make([]int, 0)
    for i := 0; i < n; i++ {
        for len(stack) > 0 && temperatures[stack[len(stack)-1]] < temperatures[i] {
            idx := stack[len(stack)-1]
            stack = stack[:len(stack)-1]
            result[idx] = i - idx
        }
        stack = append(stack, i)
    }
    return result
}
```

### Problem 3: Largest Rectangle in Histogram

```go
func largestRectangleArea(heights []int) int {
    n := len(heights)
    stack := make([]int, 0)
    maxArea := 0
    for i := 0; i <= n; i++ {
        var h int
        if i == n {
            h = 0
        } else {
            h = heights[i]
        }
        for len(stack) > 0 && heights[stack[len(stack)-1]] > h {
            height := heights[stack[len(stack)-1]]
            stack = stack[:len(stack)-1]
            width := i
            if len(stack) > 0 {
                width = i - stack[len(stack)-1] - 1
            }
            maxArea = max(maxArea, height*width)
        }
        stack = append(stack, i)
    }
    return maxArea
}
```

### Problem 4: Trapping Rain Water (using Monotonic Stack)

```go
func trap(height []int) int {
    stack := make([]int, 0)
    water := 0
    for i := 0; i < len(height); i++ {
        for len(stack) > 0 && height[i] > height[stack[len(stack)-1]] {
            top := stack[len(stack)-1]
            stack = stack[:len(stack)-1]
            if len(stack) == 0 {
                break
            }
            distance := i - stack[len(stack)-1] - 1
            boundedHeight := min(height[i], height[stack[len(stack)-1]]) - height[top]
            water += distance * boundedHeight
        }
        stack = append(stack, i)
    }
    return water
}
```
