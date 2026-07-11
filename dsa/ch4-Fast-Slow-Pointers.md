# Chapter 4 — Fast & Slow Pointers (Tortoise & Hare)

## Overview
Uses two pointers moving at different speeds to detect cycles in linked lists, find middle elements, and solve related problems.

**Time Complexity:** O(n)
**Space Complexity:** O(1)

---

## MCQ

### Q1: Why does Floyd's Cycle Detection algorithm guarantee the fast and slow pointers will meet if a cycle exists?

**Options:**
- Because the fast pointer moves at exactly twice the speed of the slow pointer, making the relative speed 1 step per iteration, so the distance between them shrinks by 1 each step.
- Because the fast pointer teleports to the start of the linked list after 100 iterations.
- Because both pointers are guaranteed to land on the same node index due to modular arithmetic.
- Because the slow pointer stops completely once it enters the cycle.

**Answer:** Because the fast pointer moves at exactly twice the speed of the slow pointer, making the relative speed 1 step per iteration, so the distance between them shrinks by 1 each step.

---

### Q2: After detecting a cycle, how do you find the start node of the cycle?

**Options:**
- Move the fast pointer back to head and move both pointers one step at a time; they meet at the cycle start.
- The meeting point itself is always the start of the cycle.
- Traverse the entire list backwards from the meeting point.
- Use a hash set to find the first duplicate node.

**Answer:** Move the fast pointer back to head and move both pointers one step at a time; they meet at the cycle start.

---

## Coding Problems

### Problem 1: Linked List Cycle Detection

```go
type ListNode struct {
    Val  int
    Next *ListNode
}

func hasCycle(head *ListNode) bool {
    slow, fast := head, head
    for fast != nil && fast.Next != nil {
        slow = slow.Next
        fast = fast.Next.Next
        if slow == fast {
            return true
        }
    }
    return false
}
```

### Problem 2: Find the Start of Cycle (Linked List Cycle II)

```go
func detectCycle(head *ListNode) *ListNode {
    slow, fast := head, head
    for fast != nil && fast.Next != nil {
        slow = slow.Next
        fast = fast.Next.Next
        if slow == fast {
            fast = head
            for fast != slow {
                fast = fast.Next
                slow = slow.Next
            }
            return slow
        }
    }
    return nil
}
```

### Problem 3: Find Middle of Linked List

```go
func middleNode(head *ListNode) *ListNode {
    slow, fast := head, head
    for fast != nil && fast.Next != nil {
        slow = slow.Next
        fast = fast.Next.Next
    }
    return slow
}
```

### Problem 4: Happy Number

```go
func isHappy(n int) bool {
    slow, fast := n, n
    for {
        slow = digitSquareSum(slow)
        fast = digitSquareSum(digitSquareSum(fast))
        if fast == 1 {
            return true
        }
        if slow == fast {
            return false
        }
    }
}

func digitSquareSum(n int) int {
    sum := 0
    for n > 0 {
        d := n % 10
        sum += d * d
        n /= 10
    }
    return sum
}
```
