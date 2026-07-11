# Chapter 2 — Sliding Window Pattern

## Overview
Sliding Window converts nested loops into a single loop by maintaining a subset of elements (window) that slides across the array. Two variants: fixed-size window and variable-size window (expand/shrink).

**Time Complexity:** O(n)
**Space Complexity:** O(1) or O(k) where k is window size

### Common Pattern Template (Variable Size)
```go
left := 0
for right := 0; right < len(arr); right++ {
    // add arr[right] to window state
    for /* condition violated */ {
        // remove arr[left] from window state
        left++
    }
    // update answer
}
```

---

## MCQ

### Q1: A sliding window approach is most beneficial compared to a brute-force nested loop when:

**Options:**
- The input size is less than 10 elements.
- The problem involves contiguous subarrays/substrings and we need O(n) instead of O(n²).
- The data is stored in a linked list rather than an array.
- The window size changes randomly at each step.

**Answer:** The problem involves contiguous subarrays/substrings and we need O(n) instead of O(n²).

---

### Q2: In a variable-size sliding window for "Longest Substring Without Repeating Characters", which condition triggers the window to shrink?

**Options:**
- When the current character is a vowel.
- When a duplicate character is detected in the current window.
- When the window size exceeds k.
- When the substring is a palindrome itself.

**Answer:** When a duplicate character is detected in the current window.

---

## Coding Problems

### Problem 1: Maximum Sum Subarray of Size K (Fixed Window)

```go
func maxSumSubarray(arr []int, k int) int {
    if len(arr) < k {
        return 0
    }
    windowSum := 0
    for i := 0; i < k; i++ {
        windowSum += arr[i]
    }
    maxSum := windowSum
    for i := k; i < len(arr); i++ {
        windowSum += arr[i] - arr[i-k]
        maxSum = max(maxSum, windowSum)
    }
    return maxSum
}
```

### Problem 2: Longest Substring Without Repeating Characters

```go
func lengthOfLongestSubstring(s string) int {
    lastSeen := make(map[byte]int)
    left, maxLen := 0, 0
    for right := 0; right < len(s); right++ {
        if idx, ok := lastSeen[s[right]]; ok && idx >= left {
            left = idx + 1
        }
        lastSeen[s[right]] = right
        maxLen = max(maxLen, right-left+1)
    }
    return maxLen
}
```

### Problem 3: Minimum Window Substring

```go
func minWindow(s string, t string) string {
    need := make(map[byte]int)
    for i := 0; i < len(t); i++ {
        need[t[i]]++
    }
    left, right, start := 0, 0, 0
    matched, minLen := 0, len(s)+1
    for right < len(s) {
        if need[s[right]]--; need[s[right]] >= 0 {
            matched++
        }
        right++
        for matched == len(t) {
            if right-left < minLen {
                minLen = right - left
                start = left
            }
            if need[s[left]]++; need[s[left]] > 0 {
                matched--
            }
            left++
        }
    }
    if minLen > len(s) {
        return ""
    }
    return s[start : start+minLen]
}
```

### Problem 4: Longest Repeating Character Replacement

```go
func characterReplacement(s string, k int) int {
    count := make([]int, 26)
    left, maxFreq, maxLen := 0, 0, 0
    for right := 0; right < len(s); right++ {
        count[s[right]-'A']++
        maxFreq = max(maxFreq, count[s[right]-'A'])
        for (right-left+1)-maxFreq > k {
            count[s[left]-'A']--
            left++
        }
        maxLen = max(maxLen, right-left+1)
    }
    return maxLen
}
```
