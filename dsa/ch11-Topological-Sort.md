# Chapter 11 — Topological Sort Pattern

## Overview
Topological sort produces a linear ordering of vertices in a DAG such that for every directed edge u→v, u comes before v. Two approaches: Kahn's algorithm (BFS using in-degree) and DFS with post-order.

**Time Complexity:** O(V + E)
**Space Complexity:** O(V)

---

## MCQ

### Q1: Topological sort is only valid for what type of graph?

**Options:**
- Any connected graph.
- Directed Acyclic Graph (DAG).
- Undirected graph with cycles.
- Complete binary tree.

**Answer:** Directed Acyclic Graph (DAG).

---

### Q2: In Kahn's algorithm, what does a queue containing all remaining nodes at the end indicate?

**Options:**
- The graph has multiple valid topological orders.
- The graph contains a cycle.
- The graph is disconnected.
- The algorithm has finished successfully.

**Answer:** The graph contains a cycle.

---

## Coding Problems

### Problem 1: Course Schedule II (Topological Order)

```go
func findOrder(numCourses int, prerequisites [][]int) []int {
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
    var result []int
    for len(queue) > 0 {
        node := queue[0]
        queue = queue[1:]
        result = append(result, node)
        for _, neighbor := range graph[node] {
            inDegree[neighbor]--
            if inDegree[neighbor] == 0 {
                queue = append(queue, neighbor)
            }
        }
    }
    if len(result) != numCourses {
        return nil // cycle detected
    }
    return result
}
```

### Problem 2: Alien Dictionary

```go
func alienOrder(words []string) string {
    graph := make(map[byte][]byte)
    inDegree := make(map[byte]int)
    for _, w := range words {
        for i := 0; i < len(w); i++ {
            graph[w[i]] = []byte{}
            inDegree[w[i]] = 0
        }
    }
    for i := 0; i < len(words)-1; i++ {
        w1, w2 := words[i], words[i+1]
        minLen := min(len(w1), len(w2))
        if len(w1) > len(w2) && w1[:minLen] == w2[:minLen] {
            return ""
        }
        for j := 0; j < minLen; j++ {
            if w1[j] != w2[j] {
                graph[w1[j]] = append(graph[w1[j]], w2[j])
                inDegree[w2[j]]++
                break
            }
        }
    }
    queue := make([]byte, 0)
    for ch := range graph {
        if inDegree[ch] == 0 {
            queue = append(queue, ch)
        }
    }
    var result []byte
    for len(queue) > 0 {
        ch := queue[0]
        queue = queue[1:]
        result = append(result, ch)
        for _, neighbor := range graph[ch] {
            inDegree[neighbor]--
            if inDegree[neighbor] == 0 {
                queue = append(queue, neighbor)
            }
        }
    }
    if len(result) != len(graph) {
        return ""
    }
    return string(result)
}
```

### Problem 3: Minimum Height Trees

```go
func findMinHeightTrees(n int, edges [][]int) []int {
    if n == 1 { return []int{0} }
    adj := make([][]int, n)
    degree := make([]int, n)
    for _, e := range edges {
        adj[e[0]] = append(adj[e[0]], e[1])
        adj[e[1]] = append(adj[e[1]], e[0])
        degree[e[0]]++
        degree[e[1]]++
    }
    queue := make([]int, 0)
    for i := 0; i < n; i++ {
        if degree[i] == 1 {
            queue = append(queue, i)
        }
    }
    remaining := n
    for remaining > 2 {
        size := len(queue)
        remaining -= size
        for i := 0; i < size; i++ {
            node := queue[0]
            queue = queue[1:]
            for _, neighbor := range adj[node] {
                degree[neighbor]--
                if degree[neighbor] == 1 {
                    queue = append(queue, neighbor)
                }
            }
        }
    }
    return queue
}
```
