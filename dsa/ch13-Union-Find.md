# Chapter 13 — Union-Find (Disjoint Set Union)

## Overview
Union-Find tracks elements partitioned into disjoint sets. It supports two operations: Find (which set does an element belong to) and Union (merge two sets). Optimizations: path compression + union by rank/size.

**Time Complexity:** O(α(n)) amortized — practically constant
**Space Complexity:** O(n)

---

## MCQ

### Q1: The two key optimizations in Union-Find for near-constant time operations are:

**Options:**
- Binary search and merge sort.
- Path compression and union by rank.
- Red-black tree balancing and hash indexing.
- Quick sort partitioning and tail recursion.

**Answer:** Path compression and union by rank.

---

### Q2: Initially, each element is its own parent. After union(A,B) and union(B,C), find(A) == find(C) returns:

**Options:**
- False
- True
- Depends on implementation.
- Error — invalid operation.

**Answer:** True (they are in the same set).

---

## Coding Problems

### Problem 1: Union-Find Implementation

```go
type UnionFind struct {
    parent []int
    rank   []int
}

func NewUnionFind(n int) *UnionFind {
    parent := make([]int, n)
    rank := make([]int, n)
    for i := 0; i < n; i++ {
        parent[i] = i
    }
    return &UnionFind{parent, rank}
}

func (uf *UnionFind) Find(x int) int {
    if uf.parent[x] != x {
        uf.parent[x] = uf.Find(uf.parent[x]) // path compression
    }
    return uf.parent[x]
}

func (uf *UnionFind) Union(x, y int) {
    rootX := uf.Find(x)
    rootY := uf.Find(y)
    if rootX == rootY { return }
    if uf.rank[rootX] < uf.rank[rootY] {
        uf.parent[rootX] = rootY
    } else if uf.rank[rootX] > uf.rank[rootY] {
        uf.parent[rootY] = rootX
    } else {
        uf.parent[rootY] = rootX
        uf.rank[rootX]++
    }
}
```

### Problem 2: Number of Connected Components in an Undirected Graph

```go
func countComponents(n int, edges [][]int) int {
    uf := NewUnionFind(n)
    for _, e := range edges {
        uf.Union(e[0], e[1])
    }
    components := make(map[int]bool)
    for i := 0; i < n; i++ {
        components[uf.Find(i)] = true
    }
    return len(components)
}
```

### Problem 3: Number of Islands (Union-Find approach)

```go
func numIslands(grid [][]byte) int {
    if len(grid) == 0 { return 0 }
    rows, cols := len(grid), len(grid[0])
    uf := NewUnionFind(rows * cols)
    dirs := [][2]int{{0,1},{1,0}}
    waterCount := 0
    for r := 0; r < rows; r++ {
        for c := 0; c < cols; c++ {
            if grid[r][c] == '0' {
                waterCount++
                continue
            }
            idx := r*cols + c
            for _, d := range dirs {
                nr, nc := r+d[0], c+d[1]
                if nr < rows && nc < cols && grid[nr][nc] == '1' {
                    uf.Union(idx, nr*cols+nc)
                }
            }
        }
    }
    // count unique roots among land cells
    landRoots := make(map[int]bool)
    for r := 0; r < rows; r++ {
        for c := 0; c < cols; c++ {
            if grid[r][c] == '1' {
                landRoots[uf.Find(r*cols+c)] = true
            }
        }
    }
    return len(landRoots)
}
```

### Problem 4: Accounts Merge

```go
func accountsMerge(accounts [][]string) [][]string {
    n := len(accounts)
    uf := NewUnionFind(n)
    emailToID := make(map[string]int)
    for i, acc := range accounts {
        for _, email := range acc[1:] {
            if id, ok := emailToID[email]; ok {
                uf.Union(i, id)
            } else {
                emailToID[email] = i
            }
        }
    }
    idToEmails := make(map[int][]string)
    for email, id := range emailToID {
        root := uf.Find(id)
        idToEmails[root] = append(idToEmails[root], email)
    }
    var result [][]string
    for id, emails := range idToEmails {
        sort.Strings(emails)
        acc := append([]string{accounts[id][0]}, emails...)
        result = append(result, acc)
    }
    return result
}
```
