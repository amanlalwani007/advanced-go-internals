# Chapter 6 — Cyclic Sort Pattern

## Overview
Cyclic Sort works when you have numbers in a fixed range [1, n] and need to sort them in O(n) time. Place each number at its correct index (value-1) by swapping.

**Time Complexity:** O(n)
**Space Complexity:** O(1)

---

## MCQ

### Q1: Cyclic sort is ideal when:

**Options:**
- The array contains floating-point numbers.
- The array contains integers from 1 to n (or 0 to n-1).
- The array is already nearly sorted.
- The array contains negative numbers.

**Answer:** The array contains integers from 1 to n (or 0 to n-1).

---

### Q2: In cyclic sort, after placing all elements at correct positions, how do you find missing numbers?

**Options:**
- Check which indices don't match their expected value.
- Sum all elements and subtract from expected sum.
- Use binary search on the sorted result.
- Count frequency of each element.

**Answer:** Check which indices don't match their expected value.

---

## Coding Problems

### Problem 1: Cyclic Sort (Sort 1..n)

```go
func cyclicSort(nums []int) {
    i := 0
    for i < len(nums) {
        correctPos := nums[i] - 1
        if nums[i] != nums[correctPos] {
            nums[i], nums[correctPos] = nums[correctPos], nums[i]
        } else {
            i++
        }
    }
}
```

### Problem 2: Find the Missing Number (0..n)

```go
func missingNumber(nums []int) int {
    i, n := 0, len(nums)
    for i < n {
        if nums[i] < n && nums[i] != nums[nums[i]] {
            nums[i], nums[nums[i]] = nums[nums[i]], nums[i]
        } else {
            i++
        }
    }
    for i = 0; i < n; i++ {
        if nums[i] != i {
            return i
        }
    }
    return n
}
```

### Problem 3: Find All Duplicates in an Array

```go
func findDuplicates(nums []int) []int {
    var result []int
    i := 0
    for i < len(nums) {
        correctPos := nums[i] - 1
        if nums[i] != nums[correctPos] {
            nums[i], nums[correctPos] = nums[correctPos], nums[i]
        } else {
            i++
        }
    }
    for i, num := range nums {
        if num != i+1 {
            result = append(result, num)
        }
    }
    return result
}
```

### Problem 4: First Missing Positive

```go
func firstMissingPositive(nums []int) int {
    i, n := 0, len(nums)
    for i < n {
        if nums[i] > 0 && nums[i] <= n && nums[i] != nums[nums[i]-1] {
            nums[i], nums[nums[i]-1] = nums[nums[i]-1], nums[i]
        } else {
            i++
        }
    }
    for i = 0; i < n; i++ {
        if nums[i] != i+1 {
            return i + 1
        }
    }
    return n + 1
}
```
