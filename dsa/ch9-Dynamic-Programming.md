# Chapter 9 — Dynamic Programming (DP)

## Overview
DP solves problems by breaking them into overlapping subproblems and storing results to avoid recomputation. Two approaches: top-down (memoization) and bottom-up (tabulation).

**Key identification:** Optimal substructure + overlapping subproblems

---

## MCQ

### Q1: Which property must a problem have for DP to be applicable?

**Options:**
- Greedy choice property.
- Optimal substructure and overlapping subproblems.
- The input must be sorted.
- The problem must involve graph traversal.

**Answer:** Optimal substructure and overlapping subproblems.

---

### Q2: What is the main advantage of bottom-up DP over top-down memoization?

**Options:**
- Bottom-up always uses less memory.
- Bottom-up avoids recursion depth limits and has no function call overhead.
- Bottom-up is easier to write for every problem.
- Bottom-up always runs in O(1) time.

**Answer:** Bottom-up avoids recursion depth limits and has no function call overhead.

---

## Coding Problems

### Problem 1: Fibonacci Numbers (Bottom-Up)

```go
func fib(n int) int {
    if n <= 1 { return n }
    dp := make([]int, n+1)
    dp[0], dp[1] = 0, 1
    for i := 2; i <= n; i++ {
        dp[i] = dp[i-1] + dp[i-2]
    }
    return dp[n]
}

// Space optimized
func fibOptimized(n int) int {
    if n <= 1 { return n }
    prev2, prev1 := 0, 1
    for i := 2; i <= n; i++ {
        curr := prev1 + prev2
        prev2 = prev1
        prev1 = curr
    }
    return prev1
}
```

### Problem 2: 0/1 Knapsack

```go
func knapsack(weights []int, values []int, capacity int) int {
    n := len(weights)
    dp := make([][]int, n+1)
    for i := range dp {
        dp[i] = make([]int, capacity+1)
    }
    for i := 1; i <= n; i++ {
        for w := 1; w <= capacity; w++ {
            if weights[i-1] <= w {
                dp[i][w] = max(values[i-1]+dp[i-1][w-weights[i-1]], dp[i-1][w])
            } else {
                dp[i][w] = dp[i-1][w]
            }
        }
    }
    return dp[n][capacity]
}
```

### Problem 3: Longest Common Subsequence (LCS)

```go
func longestCommonSubsequence(text1 string, text2 string) int {
    m, n := len(text1), len(text2)
    dp := make([][]int, m+1)
    for i := range dp {
        dp[i] = make([]int, n+1)
    }
    for i := 1; i <= m; i++ {
        for j := 1; j <= n; j++ {
            if text1[i-1] == text2[j-1] {
                dp[i][j] = dp[i-1][j-1] + 1
            } else {
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
            }
        }
    }
    return dp[m][n]
}
```

### Problem 4: Coin Change (Minimum Coins)

```go
func coinChange(coins []int, amount int) int {
    dp := make([]int, amount+1)
    for i := 1; i <= amount; i++ {
        dp[i] = amount + 1 // sentinel for impossible
    }
    for i := 1; i <= amount; i++ {
        for _, coin := range coins {
            if coin <= i {
                dp[i] = min(dp[i], dp[i-coin]+1)
            }
        }
    }
    if dp[amount] > amount { return -1 }
    return dp[amount]
}
```

### Problem 5: Longest Increasing Subsequence

```go
func lengthOfLIS(nums []int) int {
    dp := make([]int, len(nums))
    maxLen := 0
    for i := 0; i < len(nums); i++ {
        dp[i] = 1
        for j := 0; j < i; j++ {
            if nums[i] > nums[j] {
                dp[i] = max(dp[i], dp[j]+1)
            }
        }
        maxLen = max(maxLen, dp[i])
    }
    return maxLen
}
```

### Problem 6: Edit Distance (Levenshtein Distance)

```go
func minDistance(word1 string, word2 string) int {
    m, n := len(word1), len(word2)
    dp := make([][]int, m+1)
    for i := range dp {
        dp[i] = make([]int, n+1)
        dp[i][0] = i
    }
    for j := 0; j <= n; j++ {
        dp[0][j] = j
    }
    for i := 1; i <= m; i++ {
        for j := 1; j <= n; j++ {
            if word1[i-1] == word2[j-1] {
                dp[i][j] = dp[i-1][j-1]
            } else {
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
            }
        }
    }
    return dp[m][n]
}
```

### Problem 7: House Robber

```go
func rob(nums []int) int {
    if len(nums) == 0 { return 0 }
    if len(nums) == 1 { return nums[0] }
    prev2, prev1 := nums[0], max(nums[0], nums[1])
    for i := 2; i < len(nums); i++ {
        curr := max(prev1, prev2+nums[i])
        prev2 = prev1
        prev1 = curr
    }
    return prev1
}
```
