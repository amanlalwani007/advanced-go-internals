# Chapter 14 — Heap / Priority Queue Pattern

## Overview
A Heap is a complete binary tree where parent nodes have a specific ordering relative to children (min-heap or max-heap). Used for "Top K", "K smallest/largest", median finding, and scheduling problems.

**Time Complexity:** O(log n) for push/pop, O(1) for peek
**Space Complexity:** O(n)

---

## MCQ

### Q1: To find the K largest elements in an array of size n, the most efficient approach using a heap is:

**Options:**
- Build a max-heap of all n elements, then extract K times → O(n + K log n).
- Build a min-heap of the first K elements, then for each remaining element, compare and push/pop if needed → O(n log K).
- Use a binary search tree instead of a heap.
- Sort the array and take the last K.

**Answer:** Build a min-heap of the first K elements, then for each remaining element, compare and push/pop if needed → O(n log K).

---

### Q2: Which of the following problems is best solved with a Heap?

**Options:**
- Finding if a cycle exists in a linked list.
- Merging K sorted linked lists.
- Detecting a palindrome.
- Finding the shortest path in an unweighted graph.

**Answer:** Merging K sorted linked lists.

---

## Coding Problems

### Problem 1: Kth Largest Element in an Array

```go
func findKthLargest(nums []int, k int) int {
    h := &IntHeap{}
    for _, num := range nums {
        heap.Push(h, num)
        if h.Len() > k {
            heap.Pop(h)
        }
    }
    return heap.Pop(h).(int)
}

type IntHeap []int

func (h IntHeap) Len() int           { return len(h) }
func (h IntHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h IntHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *IntHeap) Push(x interface{}) { *h = append(*h, x.(int)) }
func (h *IntHeap) Pop() interface{} {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[:n-1]
    return x
}
```

### Problem 2: Merge K Sorted Lists

```go
type ListNode struct {
    Val  int
    Next *ListNode
}

type MinHeap []*ListNode

func (h MinHeap) Len() int           { return len(h) }
func (h MinHeap) Less(i, j int) bool { return h[i].Val < h[j].Val }
func (h MinHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *MinHeap) Push(x interface{}) { *h = append(*h, x.(*ListNode)) }
func (h *MinHeap) Pop() interface{} {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[:n-1]
    return x
}

func mergeKLists(lists []*ListNode) *ListNode {
    h := &MinHeap{}
    heap.Init(h)
    for _, list := range lists {
        if list != nil {
            heap.Push(h, list)
        }
    }
    dummy := &ListNode{}
    curr := dummy
    for h.Len() > 0 {
        node := heap.Pop(h).(*ListNode)
        curr.Next = node
        curr = curr.Next
        if node.Next != nil {
            heap.Push(h, node.Next)
        }
    }
    return dummy.Next
}
```

### Problem 3: Top K Frequent Elements

```go
func topKFrequent(nums []int, k int) []int {
    freq := make(map[int]int)
    for _, num := range nums {
        freq[num]++
    }
    h := &FreqHeap{}
    for num, count := range freq {
        heap.Push(h, Freq{num, count})
        if h.Len() > k {
            heap.Pop(h)
        }
    }
    result := make([]int, k)
    for i := k - 1; i >= 0; i-- {
        result[i] = heap.Pop(h).(Freq).num
    }
    return result
}

type Freq struct {
    num   int
    count int
}

type FreqHeap []Freq

func (h FreqHeap) Len() int           { return len(h) }
func (h FreqHeap) Less(i, j int) bool { return h[i].count < h[j].count }
func (h FreqHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *FreqHeap) Push(x interface{}) { *h = append(*h, x.(Freq)) }
func (h *FreqHeap) Pop() interface{} {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[:n-1]
    return x
}
```

### Problem 4: Find Median from Data Stream

```go
type MedianFinder struct {
    maxHeap *MaxHeap // left half (smaller numbers)
    minHeap *MinHeap // right half (larger numbers)
}

func Constructor() MedianFinder {
    return MedianFinder{
        maxHeap: &MaxHeap{},
        minHeap: &MinHeap{},
    }
}

func (mf *MedianFinder) AddNum(num int) {
    if mf.maxHeap.Len() == 0 || num <= mf.maxHeap.Peek() {
        heap.Push(mf.maxHeap, num)
    } else {
        heap.Push(mf.minHeap, num)
    }
    // balance
    if mf.maxHeap.Len() > mf.minHeap.Len()+1 {
        heap.Push(mf.minHeap, heap.Pop(mf.maxHeap))
    } else if mf.minHeap.Len() > mf.maxHeap.Len() {
        heap.Push(mf.maxHeap, heap.Pop(mf.minHeap))
    }
}

func (mf *MedianFinder) FindMedian() float64 {
    if mf.maxHeap.Len() > mf.minHeap.Len() {
        return float64(mf.maxHeap.Peek())
    }
    return float64(mf.maxHeap.Peek()+mf.minHeap.Peek()) / 2.0
}

type MaxHeap []int
func (h MaxHeap) Len() int           { return len(h) }
func (h MaxHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h MaxHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *MaxHeap) Push(x interface{}) { *h = append(*h, x.(int)) }
func (h *MaxHeap) Pop() interface{} {
    old := *h; n := len(old); x := old[n-1]; *h = old[:n-1]; return x
}
func (h MaxHeap) Peek() int { return h[0] }

type MinHeap []int
func (h MinHeap) Len() int           { return len(h) }
func (h MinHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h MinHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *MinHeap) Push(x interface{}) { *h = append(*h, x.(int)) }
func (h *MinHeap) Pop() interface{} {
    old := *h; n := len(old); x := old[n-1]; *h = old[:n-1]; return x
}
func (h MinHeap) Peek() int { return h[0] }
```
