# Chapter 3 — Binary Search Pattern

## Overview
Binary Search finds an element in a sorted array by repeatedly dividing the search interval in half. Advanced variants include searching in rotated arrays, finding boundaries (first/last occurrence), and binary search on answer spaces.

**Time Complexity:** O(log n)
**Space Complexity:** O(1)

---

## MCQ

### Q1: Binary search requires which precondition to work correctly?

**Options:**
- The array must contain unique elements only.
- The array must be sorted in either ascending or descending order.
- The array must be of size that is a power of two.
- The array must be stored as a contiguous memory block.

**Answer:** The array must be sorted in either ascending or descending order.

---

### Q2: What is the most common bug in binary search implementations?

**Options:**
- Using `for left < right` when the loop condition should be `for left <= right`.
- Using integer division where the divisor is 3 instead of 2.
- Not using recursion for the implementation.
- Sorting the array before each search call.

**Answer:** Off-by-one errors in loop condition and mid calculation (using `left <= right` vs `left < right`, and updating `left = mid + 1` vs `left = mid`).

---

## Coding Problems

### Problem 1: Classic Binary Search

```go
func binarySearch(nums []int, target int) int {
    left, right := 0, len(nums)-1
    for left <= right {
        mid := left + (right-left)/2
        if nums[mid] == target {
            return mid
        } else if nums[mid] < target {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }
    return -1
}
```

### Problem 2: First and Last Position of Element in Sorted Array

```go
func searchRange(nums []int, target int) []int {
    first := findBound(nums, target, true)
    if first == -1 {
        return []int{-1, -1}
    }
    last := findBound(nums, target, false)
    return []int{first, last}
}

func findBound(nums []int, target int, isFirst bool) int {
    left, right := 0, len(nums)-1
    result := -1
    for left <= right {
        mid := left + (right-left)/2
        if nums[mid] == target {
            result = mid
            if isFirst {
                right = mid - 1
            } else {
                left = mid + 1
            }
        } else if nums[mid] < target {
            left = mid + 1
        } else {
            right = mid - 1
        }
    }
    return result
}
```

### Problem 3: Search in Rotated Sorted Array

```go
func search(nums []int, target int) int {
    left, right := 0, len(nums)-1
    for left <= right {
        mid := left + (right-left)/2
        if nums[mid] == target {
            return mid
        }
        if nums[left] <= nums[mid] {
            // left half is sorted
            if target >= nums[left] && target < nums[mid] {
                right = mid - 1
            } else {
                left = mid + 1
            }
        } else {
            // right half is sorted
            if target > nums[mid] && target <= nums[right] {
                left = mid + 1
            } else {
                right = mid - 1
            }
        }
    }
    return -1
}
```

### Problem 4: Find Minimum in Rotated Sorted Array

```go
func findMin(nums []int) int {
    left, right := 0, len(nums)-1
    for left < right {
        mid := left + (right-left)/2
        if nums[mid] > nums[right] {
            left = mid + 1
        } else {
            right = mid
        }
    }
    return nums[left]
}
```

### Problem 5: Binary Search on Answer — Koko Eating Bananas

```go
func minEatingSpeed(piles []int, h int) int {
    left, right := 1, 0
    for _, p := range piles {
        right = max(right, p)
    }
    for left < right {
        mid := left + (right-left)/2
        hours := 0
        for _, p := range piles {
            hours += (p + mid - 1) / mid
        }
        if hours <= h {
            right = mid
        } else {
            left = mid + 1
        }
    }
    return left
}
```
