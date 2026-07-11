# Chapter 7 — BFS (Breadth First Search)

## Overview
BFS explores a graph level by level using a queue. It finds the shortest path in unweighted graphs and is essential for tree level-order traversal, connected components, and topological sorting (Kahn's algorithm).

**Time Complexity:** O(V + E)
**Space Complexity:** O(V)

---

## MCQ

### Q1: Which data structure is fundamental to BFS traversal?

**Options:**
- Stack
- Queue
- Priority Queue
- Set

**Answer:** Queue

---

### Q2: BFS guarantees the shortest path when:

**Options:**
- The graph is a tree with weighted edges.
- The graph is unweighted (all edges have equal weight).
- The graph is directed and acyclic.
- The graph contains negative edge weights.

**Answer:** The graph is unweighted (all edges have equal weight).

---

## Coding Problems

### Problem 1: Binary Tree Level Order Traversal

```go
type TreeNode struct {
    Val   int
    Left  *TreeNode
    Right *TreeNode
}

func levelOrder(root *TreeNode) [][]int {
    var result [][]int
    if root == nil { return result }
    queue := []*TreeNode{root}
    for len(queue) > 0 {
        levelSize := len(queue)
        level := make([]int, levelSize)
        for i := 0; i < levelSize; i++ {
            node := queue[0]
            queue = queue[1:]
            level[i] = node.Val
            if node.Left != nil { queue = append(queue, node.Left) }
            if node.Right != nil { queue = append(queue, node.Right) }
        }
        result = append(result, level)
    }
    return result
}
```

### Problem 2: Word Ladder

```go
func ladderLength(beginWord string, endWord string, wordList []string) int {
    wordSet := make(map[string]bool)
    for _, w := range wordList {
        wordSet[w] = true
    }
    if !wordSet[endWord] {
        return 0
    }
    queue := []string{beginWord}
    depth := 1
    for len(queue) > 0 {
        size := len(queue)
        for i := 0; i < size; i++ {
            word := queue[0]
            queue = queue[1:]
            if word == endWord {
                return depth
            }
            for j := 0; j < len(word); j++ {
                for c := 'a'; c <= 'z'; c++ {
                    next := []byte(word)
                    next[j] = byte(c)
                    s := string(next)
                    if wordSet[s] {
                        queue = append(queue, s)
                        delete(wordSet, s)
                    }
                }
            }
        }
        depth++
    }
    return 0
}
```

### Problem 3: Rotting Oranges

```go
func orangesRotting(grid [][]int) int {
    rows, cols := len(grid), len(grid[0])
    queue := make([][2]int, 0)
    fresh := 0
    for r := 0; r < rows; r++ {
        for c := 0; c < cols; c++ {
            if grid[r][c] == 2 {
                queue = append(queue, [2]int{r, c})
            } else if grid[r][c] == 1 {
                fresh++
            }
        }
    }
    if fresh == 0 { return 0 }
    dirs := [][2]int{{-1,0}, {1,0}, {0,-1}, {0,1}}
    minutes := 0
    for len(queue) > 0 {
        size := len(queue)
        for i := 0; i < size; i++ {
            r, c := queue[0][0], queue[0][1]
            queue = queue[1:]
            for _, d := range dirs {
                nr, nc := r+d[0], c+d[1]
                if nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] == 1 {
                    grid[nr][nc] = 2
                    fresh--
                    queue = append(queue, [2]int{nr, nc})
                }
            }
        }
        minutes++
    }
    if fresh > 0 { return -1 }
    return minutes - 1
}
```

### Problem 4: Course Schedule (Kahn's Topological Sort)

```go
func canFinish(numCourses int, prerequisites [][]int) bool {
    graph := make([][]int, numCourses)
    inDegree := make([]int, numCourses)
    for _, pre := range prerequisites {
        graph[pre[1]] = append(graph[pre[1]], pre[0])
        inDegree[pre[0]]++
    }
    queue := make([]int, 0)
    for i := 0; i < numCourses; i++ {
        if inDegree[i] == 0 {
            queue = append(queue, i)
        }
    }
    count := 0
    for len(queue) > 0 {
        node := queue[0]
        queue = queue[1:]
        count++
        for _, neighbor := range graph[node] {
            inDegree[neighbor]--
            if inDegree[neighbor] == 0 {
                queue = append(queue, neighbor)
            }
        }
    }
    return count == numCourses
}
```
