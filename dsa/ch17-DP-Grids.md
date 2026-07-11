# Chapter 17 — Dynamic Programming on Grids

## Overview
DP on grids involves problems like unique paths, minimum path sum, maximal square, etc. The state usually represents the optimal value at cell (i,j), derived from neighbors (top, left, diagonal).

---

## MCQ

### Q1: In a DP grid where you can only move right or down, the number of unique paths to cell (i,j) is:

**Options:**
- dp[i][j] = dp[i-1][j] + dp[i][j-1]
- dp[i][j] = dp[i-1][j-1] + 1
- dp[i][j] = dp[i-1][j] * dp[i][j-1]
- dp[i][j] = max(dp[i-1][j], dp[i][j-1])

**Answer:** dp[i][j] = dp[i-1][j] + dp[i][j-1]

---

## Coding Problems

### Problem 1: Unique Paths

```go
func uniquePaths(m int, n int) int {
    dp := make([][]int, m)
    for i := range dp {
        dp[i] = make([]int, n)
        dp[i][0] = 1
    }
    for j := 0; j < n; j++ {
        dp[0][j] = 1
    }
    for i := 1; i < m; i++ {
        for j := 1; j < n; j++ {
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
        }
    }
    return dp[m-1][n-1]
}

// Space optimized O(n)
func uniquePathsOptimized(m int, n int) int {
    dp := make([]int, n)
    for j := range dp { dp[j] = 1 }
    for i := 1; i < m; i++ {
        for j := 1; j < n; j++ {
            dp[j] += dp[j-1]
        }
    }
    return dp[n-1]
}
```

### Problem 2: Minimum Path Sum

```go
func minPathSum(grid [][]int) int {
    m, n := len(grid), len(grid[0])
    dp := make([][]int, m)
    for i := range dp {
        dp[i] = make([]int, n)
    }
    dp[0][0] = grid[0][0]
    for i := 1; i < m; i++ { dp[i][0] = dp[i-1][0] + grid[i][0] }
    for j := 1; j < n; j++ { dp[0][j] = dp[0][j-1] + grid[0][j] }
    for i := 1; i < m; i++ {
        for j := 1; j < n; j++ {
            dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
        }
    }
    return dp[m-1][n-1]
}
```

### Problem 3: Maximal Square

```go
func maximalSquare(matrix [][]byte) int {
    if len(matrix) == 0 { return 0 }
    rows, cols := len(matrix), len(matrix[0])
    dp := make([][]int, rows)
    for i := range dp {
        dp[i] = make([]int, cols)
    }
    maxSide := 0
    for i := 0; i < rows; i++ {
        for j := 0; j < cols; j++ {
            if matrix[i][j] == '1' {
                if i == 0 || j == 0 {
                    dp[i][j] = 1
                } else {
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
                }
                maxSide = max(maxSide, dp[i][j])
            }
        }
    }
    return maxSide * maxSide
}
```

### Problem 4: Dungeon Game

```go
func calculateMinimumHP(dungeon [][]int) int {
    m, n := len(dungeon), len(dungeon[0])
    dp := make([][]int, m+1)
    for i := range dp {
        dp[i] = make([]int, n+1)
        for j := range dp[i] {
            dp[i][j] = 1<<31 - 1
        }
    }
    dp[m][n-1], dp[m-1][n] = 1, 1
    for i := m - 1; i >= 0; i-- {
        for j := n - 1; j >= 0; j-- {
            need := min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j]
            if need <= 0 {
                dp[i][j] = 1
            } else {
                dp[i][j] = need
            }
        }
    }
    return dp[0][0]
}
```
