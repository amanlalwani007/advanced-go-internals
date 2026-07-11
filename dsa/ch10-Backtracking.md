# Chapter 10 — Backtracking Pattern

## Overview
Backtracking systematically explores all possible configurations by building candidates incrementally and abandoning ("pruning") those that fail constraints. Core pattern: make a choice → recurse → undo the choice.

**Time Complexity:** Often O(2^n) or O(n!) in worst case
**Space Complexity:** O(n) for recursion stack

---

## MCQ

### Q1: Backtracking is most suitable when:

**Options:**
- The problem requires finding the single optimal solution using greedy choices.
- The problem requires exploring all permutations, combinations, or subsets.
- The problem has overlapping subproblems with optimal substructure.
- The input size is extremely large (10⁶+).

**Answer:** The problem requires exploring all permutations, combinations, or subsets.

---

### Q2: What is the key difference between backtracking and simple brute force?

**Options:**
- Backtracking uses dynamic programming tables.
- Backtracking prunes invalid paths early, reducing the search space.
- Backtracking only works on sorted inputs.
- Backtracking always runs in O(n log n) time.

**Answer:** Backtracking prunes invalid paths early, reducing the search space.

---

## Coding Problems

### Problem 1: Subsets (All possible subsets)

```go
func subsets(nums []int) [][]int {
    var result [][]int
    var current []int
    var backtrack func(idx int)
    backtrack = func(idx int) {
        tmp := make([]int, len(current))
        copy(tmp, current)
        result = append(result, tmp)
        for i := idx; i < len(nums); i++ {
            current = append(current, nums[i])
            backtrack(i + 1)
            current = current[:len(current)-1]
        }
    }
    backtrack(0)
    return result
}
```

### Problem 2: Permutations

```go
func permute(nums []int) [][]int {
    var result [][]int
    used := make([]bool, len(nums))
    var backtrack func(current []int)
    backtrack = func(current []int) {
        if len(current) == len(nums) {
            tmp := make([]int, len(current))
            copy(tmp, current)
            result = append(result, tmp)
            return
        }
        for i := 0; i < len(nums); i++ {
            if used[i] { continue }
            used[i] = true
            current = append(current, nums[i])
            backtrack(current)
            current = current[:len(current)-1]
            used[i] = false
        }
    }
    backtrack([]int{})
    return result
}
```

### Problem 3: Combination Sum

```go
func combinationSum(candidates []int, target int) [][]int {
    var result [][]int
    var current []int
    var backtrack func(idx, remaining int)
    backtrack = func(idx, remaining int) {
        if remaining == 0 {
            tmp := make([]int, len(current))
            copy(tmp, current)
            result = append(result, tmp)
            return
        }
        if remaining < 0 { return }
        for i := idx; i < len(candidates); i++ {
            current = append(current, candidates[i])
            backtrack(i, remaining-candidates[i])
            current = current[:len(current)-1]
        }
    }
    backtrack(0, target)
    return result
}
```

### Problem 4: N-Queens

```go
func solveNQueens(n int) [][]string {
    var result [][]string
    board := make([][]byte, n)
    for i := 0; i < n; i++ {
        board[i] = make([]byte, n)
        for j := 0; j < n; j++ {
            board[i][j] = '.'
        }
    }
    cols := make([]bool, n)
    diag1 := make([]bool, 2*n-1) // r+c
    diag2 := make([]bool, 2*n-1) // r-c+n-1
    var backtrack func(row int)
    backtrack = func(row int) {
        if row == n {
            solution := make([]string, n)
            for i := 0; i < n; i++ {
                solution[i] = string(board[i])
            }
            result = append(result, solution)
            return
        }
        for col := 0; col < n; col++ {
            if cols[col] || diag1[row+col] || diag2[row-col+n-1] {
                continue
            }
            board[row][col] = 'Q'
            cols[col] = true
            diag1[row+col] = true
            diag2[row-col+n-1] = true
            backtrack(row + 1)
            board[row][col] = '.'
            cols[col] = false
            diag1[row+col] = false
            diag2[row-col+n-1] = false
        }
    }
    backtrack(0)
    return result
}
```

### Problem 5: Palindrome Partitioning

```go
func partition(s string) [][]string {
    var result [][]string
    var current []string
    var backtrack func(idx int)
    backtrack = func(idx int) {
        if idx >= len(s) {
            tmp := make([]string, len(current))
            copy(tmp, current)
            result = append(result, tmp)
            return
        }
        for end := idx; end < len(s); end++ {
            if isPalindrome(s, idx, end) {
                current = append(current, s[idx:end+1])
                backtrack(end + 1)
                current = current[:len(current)-1]
            }
        }
    }
    backtrack(0)
    return result
}

func isPalindrome(s string, l, r int) bool {
    for l < r {
        if s[l] != s[r] { return false }
        l++
        r--
    }
    return true
}
```
