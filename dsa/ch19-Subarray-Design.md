# Chapter 19 — Design & Subarray Patterns (Prefix Sum, Hash Map)

## Overview
Prefix sums and hash maps are used for subarray/sum problems: find subarray with given sum, longest subarray with equal 0s and 1s, contiguous array with sum k.

---

## MCQ

### Q1: Using prefix sum + hash map, finding a subarray with sum = k can be done in:

**Options:**
- O(n²) — iterate all subarrays.
- O(n log n) — binary search on prefix sums.
- O(n) — check if prefix_sum - k exists in hash map.
- O(1) — direct lookup.

**Answer:** O(n) — check if prefix_sum - k exists in hash map.

---

## Coding Problems

### Problem 1: Subarray Sum Equals K

```go
func subarraySum(nums []int, k int) int {
    prefixSum := 0
    count := 0
    sumMap := make(map[int]int)
    sumMap[0] = 1
    for _, num := range nums {
        prefixSum += num
        if val, ok := sumMap[prefixSum-k]; ok {
            count += val
        }
        sumMap[prefixSum]++
    }
    return count
}
```

### Problem 2: Contiguous Array (Equal 0s and 1s)

```go
func findMaxLength(nums []int) int {
    sumMap := make(map[int]int)
    sumMap[0] = -1
    maxLen := 0
    sum := 0
    for i, num := range nums {
        if num == 0 { sum-- } else { sum++ }
        if idx, ok := sumMap[sum]; ok {
            maxLen = max(maxLen, i-idx)
        } else {
            sumMap[sum] = i
        }
    }
    return maxLen
}
```

### Problem 3: Product of Array Except Self

```go
func productExceptSelf(nums []int) []int {
    n := len(nums)
    result := make([]int, n)
    // prefix product
    result[0] = 1
    for i := 1; i < n; i++ {
        result[i] = result[i-1] * nums[i-1]
    }
    // suffix product
    suffix := 1
    for i := n - 1; i >= 0; i-- {
        result[i] *= suffix
        suffix *= nums[i]
    }
    return result
}
```

### Problem 4: Longest Consecutive Sequence

```go
func longestConsecutive(nums []int) int {
    numSet := make(map[int]bool)
    for _, num := range nums {
        numSet[num] = true
    }
    maxLen := 0
    for num := range numSet {
        if !numSet[num-1] { // start of a sequence
            curr := num
            length := 1
            for numSet[curr+1] {
                curr++
                length++
            }
            maxLen = max(maxLen, length)
        }
    }
    return maxLen
}
```

### Problem 5: Insert Delete GetRandom O(1)

```go
type RandomizedSet struct {
    nums []int
    idx  map[int]int
}

func Constructor() RandomizedSet {
    return RandomizedSet{nums: []int{}, idx: make(map[int]int)}
}

func (rs *RandomizedSet) Insert(val int) bool {
    if _, ok := rs.idx[val]; ok { return false }
    rs.idx[val] = len(rs.nums)
    rs.nums = append(rs.nums, val)
    return true
}

func (rs *RandomizedSet) Remove(val int) bool {
    i, ok := rs.idx[val]
    if !ok { return false }
    last := len(rs.nums) - 1
    rs.nums[i] = rs.nums[last]
    rs.idx[rs.nums[i]] = i
    rs.nums = rs.nums[:last]
    delete(rs.idx, val)
    return true
}

func (rs *RandomizedSet) GetRandom() int {
    return rs.nums[rand.Intn(len(rs.nums))]
}
```
