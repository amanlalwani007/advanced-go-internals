# Chapter 8 — DFS (Depth First Search)

## Overview
DFS explores as far as possible along each branch before backtracking. It is used for tree traversals (preorder/inorder/postorder), graph connectivity, pathfinding, and detecting cycles.

**Time Complexity:** O(V + E)
**Space Complexity:** O(h) where h is the height of the tree/depth of recursion

---

## MCQ

### Q1: Which DFS traversal of a BST produces elements in sorted order?

**Options:**
- Preorder
- Inorder
- Postorder
- Level order

**Answer:** Inorder

---

### Q2: The maximum depth of recursion stack in DFS on a graph equals:

**Options:**
- The number of edges in the graph.
- The number of vertices in the graph.
- The longest path in the graph (depth).
- The total number of connected components.

**Answer:** The longest path in the graph (depth).

---

## Coding Problems

### Problem 1: Binary Tree Inorder Traversal (Iterative)

```go
func inorderTraversal(root *TreeNode) []int {
    var result []int
    stack := make([]*TreeNode, 0)
    curr := root
    for curr != nil || len(stack) > 0 {
        for curr != nil {
            stack = append(stack, curr)
            curr = curr.Left
        }
        curr = stack[len(stack)-1]
        stack = stack[:len(stack)-1]
        result = append(result, curr.Val)
        curr = curr.Right
    }
    return result
}
```

### Problem 2: Number of Islands

```go
func numIslands(grid [][]byte) int {
    if len(grid) == 0 { return 0 }
    count := 0
    for r := 0; r < len(grid); r++ {
        for c := 0; c < len(grid[0]); c++ {
            if grid[r][c] == '1' {
                count++
                dfsIsland(grid, r, c)
            }
        }
    }
    return count
}

func dfsIsland(grid [][]byte, r, c int) {
    if r < 0 || c < 0 || r >= len(grid) || c >= len(grid[0]) || grid[r][c] != '1' {
        return
    }
    grid[r][c] = '0' // mark visited
    dfsIsland(grid, r-1, c)
    dfsIsland(grid, r+1, c)
    dfsIsland(grid, r, c-1)
    dfsIsland(grid, r, c+1)
}
```

### Problem 3: Clone Graph

```go
type Node struct {
    Val       int
    Neighbors []*Node
}

func cloneGraph(node *Node) *Node {
    if node == nil { return nil }
    visited := make(map[*Node]*Node)
    return dfsClone(node, visited)
}

func dfsClone(node *Node, visited map[*Node]*Node) *Node {
    if clone, ok := visited[node]; ok {
        return clone
    }
    clone := &Node{Val: node.Val}
    visited[node] = clone
    for _, neighbor := range node.Neighbors {
        clone.Neighbors = append(clone.Neighbors, dfsClone(neighbor, visited))
    }
    return clone
}
```

### Problem 4: Pacific Atlantic Water Flow

```go
func pacificAtlantic(heights [][]int) [][]int {
    if len(heights) == 0 { return nil }
    rows, cols := len(heights), len(heights[0])
    pac := make([][]bool, rows)
    atl := make([][]bool, rows)
    for i := 0; i < rows; i++ {
        pac[i] = make([]bool, cols)
        atl[i] = make([]bool, cols)
    }
    for c := 0; c < cols; c++ {
        dfsOcean(heights, pac, 0, c, rows, cols)
        dfsOcean(heights, atl, rows-1, c, rows, cols)
    }
    for r := 0; r < rows; r++ {
        dfsOcean(heights, pac, r, 0, rows, cols)
        dfsOcean(heights, atl, r, cols-1, rows, cols)
    }
    var result [][]int
    for r := 0; r < rows; r++ {
        for c := 0; c < cols; c++ {
            if pac[r][c] && atl[r][c] {
                result = append(result, []int{r, c})
            }
        }
    }
    return result
}

func dfsOcean(heights [][]int, ocean [][]bool, r, c, rows, cols int) {
    ocean[r][c] = true
    dirs := [][2]int{{-1,0},{1,0},{0,-1},{0,1}}
    for _, d := range dirs {
        nr, nc := r+d[0], c+d[1]
        if nr >= 0 && nr < rows && nc >= 0 && nc < cols && !ocean[nr][nc] && heights[nr][nc] >= heights[r][c] {
            dfsOcean(heights, ocean, nr, nc, rows, cols)
        }
    }
}
```

### Problem 5: Max Area of Island

```go
func maxAreaOfIsland(grid [][]int) int {
    maxArea := 0
    for r := 0; r < len(grid); r++ {
        for c := 0; c < len(grid[0]); c++ {
            if grid[r][c] == 1 {
                area := dfsArea(grid, r, c)
                maxArea = max(maxArea, area)
            }
        }
    }
    return maxArea
}

func dfsArea(grid [][]int, r, c int) int {
    if r < 0 || c < 0 || r >= len(grid) || c >= len(grid[0]) || grid[r][c] != 1 {
        return 0
    }
    grid[r][c] = 0
    return 1 + dfsArea(grid, r-1, c) + dfsArea(grid, r+1, c) +
               dfsArea(grid, r, c-1) + dfsArea(grid, r, c+1)
}
```
