# Chapter 1 — Two Pointers Pattern

## Overview
The Two Pointers technique uses two pointers to iterate through a data structure (usually a sorted array or linked list) from different positions until a condition is met. Common variants: opposite ends, same direction (slow/fast), sliding window (covered separately).

**Time Complexity:** Typically O(n)
**Space Complexity:** Typically O(1)

---

## MCQ

### Q1: Given a sorted array `[1, 2, 3, 4, 5, 6]`, which two-pointer approach finds a pair summing to 8?

**Options:**
- Initialize both pointers at index 0; move both rightwards.
- Initialize left at 0, right at len-1; sum too small → move left right; sum too large → move right left.
- Initialize left at 0, right at index 1; move right until sum exceeds target, then move left.
- Use binary search for complement of each element.

**Answer:** Initialize left at 0, right at len-1; sum too small → move left right; sum too large → move right left.

---

### Q2: When can the two-pointer technique NOT be applied to an array problem?

**Options:**
- When the array is sorted and we need to find a pair with a specific sum.
- When the array is unsorted and we need to find a pair with a specific sum.
- When we need to remove duplicates from a sorted array.
- When we need to check if a string is a palindrome.

**Answer:** When the array is unsorted and we need to find a pair with a specific sum.

---

## Coding Problems

### Problem 1: Two Sum II — Input Array is Sorted

```go
func twoSum(numbers []int, target int) []int {
    left, right := 0, len(numbers)-1
    for left < right {
        sum := numbers[left] + numbers[right]
        if sum == target {
            return []int{left + 1, right + 1}
        } else if sum < target {
            left++
        } else {
            right--
        }
    }
    return nil
}
```

### Problem 2: Container With Most Water

```go
func maxArea(height []int) int {
    left, right := 0, len(height)-1
    maxArea := 0
    for left < right {
        h := min(height[left], height[right])
        w := right - left
        maxArea = max(maxArea, h*w)
        if height[left] < height[right] {
            left++
        } else {
            right--
        }
    }
    return maxArea
}

func min(a, b int) int { if a < b { return a }; return b }
func max(a, b int) int { if a > b { return a }; return b }
```

### Problem 3: 3Sum (Triplet Sum to Zero)

```go
func threeSum(nums []int) [][]int {
    sort.Ints(nums)
    var result [][]int
    for i := 0; i < len(nums)-2; i++ {
        if i > 0 && nums[i] == nums[i-1] {
            continue
        }
        left, right := i+1, len(nums)-1
        for left < right {
            sum := nums[i] + nums[left] + nums[right]
            if sum == 0 {
                result = append(result, []int{nums[i], nums[left], nums[right]})
                left++
                right--
                for left < right && nums[left] == nums[left-1] { left++ }
                for left < right && nums[right] == nums[right+1] { right-- }
            } else if sum < 0 {
                left++
            } else {
                right--
            }
        }
    }
    return result
}
```

### Problem 4: Trapping Rain Water

```go
func trap(height []int) int {
    left, right := 0, len(height)-1
    leftMax, rightMax := 0, 0
    water := 0
    for left < right {
        if height[left] < height[right] {
            if height[left] >= leftMax {
                leftMax = height[left]
            } else {
                water += leftMax - height[left]
            }
            left++
        } else {
            if height[right] >= rightMax {
                rightMax = height[right]
            } else {
                water += rightMax - height[right]
            }
            right--
        }
    }
    return water
}
```
