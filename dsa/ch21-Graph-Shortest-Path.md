# Chapter 21 — Graph Shortest Path (Dijkstra, Bellman-Ford)

## Overview
Shortest path algorithms: Dijkstra (non-negative weights), Bellman-Ford (handles negative weights, detects cycles), Floyd-Warshall (all-pairs).

---

## MCQ

### Q1: Why does Dijkstra's algorithm fail with negative edge weights?

**Options:**
- It requires the adjacency list to be sorted.
- Once a node is visited (finalized), its distance is never updated — a later shorter path via negative edges would be missed.
- It cannot handle more than 1000 nodes.
- It requires undirected graphs.

**Answer:** Once a node is visited (finalized), its distance is never updated — a later shorter path via negative edges would be missed.

---

## Coding Problems

### Problem 1: Dijkstra's Algorithm (Network Delay Time)

```go
func networkDelayTime(times [][]int, n int, k int) int {
    graph := make([][][2]int, n+1)
    for _, t := range times {
        graph[t[0]] = append(graph[t[0]], [2]int{t[1], t[2]})
    }
    dist := make([]int, n+1)
    for i := 1; i <= n; i++ {
        dist[i] = 1<<31 - 1
    }
    dist[k] = 0
    pq := &PriorityQueue{}
    heap.Push(pq, Item{node: k, dist: 0})
    for pq.Len() > 0 {
        curr := heap.Pop(pq).(Item)
        if curr.dist > dist[curr.node] { continue }
        for _, edge := range graph[curr.node] {
            next, weight := edge[0], edge[1]
            newDist := curr.dist + weight
            if newDist < dist[next] {
                dist[next] = newDist
                heap.Push(pq, Item{node: next, dist: newDist})
            }
        }
    }
    maxTime := 0
    for i := 1; i <= n; i++ {
        if dist[i] == 1<<31-1 { return -1 }
        maxTime = max(maxTime, dist[i])
    }
    return maxTime
}

type Item struct {
    node int
    dist int
}
type PriorityQueue []Item
func (pq PriorityQueue) Len() int { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool { return pq[i].dist < pq[j].dist }
func (pq PriorityQueue) Swap(i, j int) { pq[i], pq[j] = pq[j], pq[i] }
func (pq *PriorityQueue) Push(x interface{}) { *pq = append(*pq, x.(Item)) }
func (pq *PriorityQueue) Pop() interface{} {
    old := *pq; n := len(old); x := old[n-1]; *pq = old[:n-1]; return x
}
```

### Problem 2: Bellman-Ford (Cheapest Flights Within K Stops)

```go
func findCheapestPrice(n int, flights [][]int, src int, dst int, k int) int {
    prices := make([]int, n)
    for i := 0; i < n; i++ {
        prices[i] = 1<<31 - 1
    }
    prices[src] = 0
    for i := 0; i <= k; i++ {
        temp := make([]int, n)
        copy(temp, prices)
        for _, f := range flights {
            from, to, price := f[0], f[1], f[2]
            if prices[from] == 1<<31-1 { continue }
            if prices[from]+price < temp[to] {
                temp[to] = prices[from] + price
            }
        }
        prices = temp
    }
    if prices[dst] == 1<<31-1 { return -1 }
    return prices[dst]
}
```
