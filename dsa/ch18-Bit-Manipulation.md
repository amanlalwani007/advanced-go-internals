# Chapter 18 — Bit Manipulation Pattern

## Overview
Bit manipulation uses bitwise operators (&, |, ^, ~, <<, >>) to solve problems efficiently. Common patterns: checking/setting/clearing bits, XOR tricks, counting bits, power of two checks.

**Time Complexity:** O(1) or O(number of bits)
**Space Complexity:** O(1)

---

## MCQ

### Q1: What does `n & (n-1)` do?

**Options:**
- Checks if n is a multiple of 4.
- Clears (sets to 0) the lowest set bit in n.
- Toggles all bits in n.
- Returns n multiplied by 2.

**Answer:** Clears (sets to 0) the lowest set bit in n.

---

### Q2: Which XOR property is used to find the non-repeating element in an array where all other elements appear twice?

**Options:**
- x ^ 0 = x
- x ^ x = 0
- XOR is commutative and associative.
- All of the above combine to cancel duplicate values.

**Answer:** All of the above combine to cancel duplicate values.

---

## Coding Problems

### Problem 1: Single Number (Find non-repeating element)

```go
func singleNumber(nums []int) int {
    result := 0
    for _, num := range nums {
        result ^= num
    }
    return result
}
```

### Problem 2: Number of 1 Bits (Hamming Weight)

```go
func hammingWeight(n int) int {
    count := 0
    for n != 0 {
        n = n & (n - 1) // clear lowest set bit
        count++
    }
    return count
}
```

### Problem 3: Power of Two

```go
func isPowerOfTwo(n int) bool {
    return n > 0 && (n & (n - 1)) == 0
}
```

### Problem 4: Missing Number (0..n)

```go
func missingNumber(nums []int) int {
    n := len(nums)
    missing := n
    for i, num := range nums {
        missing ^= i ^ num
    }
    return missing
}
```

### Problem 5: Reverse Bits

```go
func reverseBits(num uint32) uint32 {
    var result uint32 = 0
    for i := 0; i < 32; i++ {
        result <<= 1
        result |= num & 1
        num >>= 1
    }
    return result
}
```

### Problem 6: Subsets using Bitmask

```go
func subsets(nums []int) [][]int {
    n := len(nums)
    total := 1 << n
    result := make([][]int, total)
    for mask := 0; mask < total; mask++ {
        subset := make([]int, 0)
        for i := 0; i < n; i++ {
            if mask & (1 << i) != 0 {
                subset = append(subset, nums[i])
            }
        }
        result[mask] = subset
    }
    return result
}
```

### Problem 7: Sum of Two Integers (Without + or -)

```go
func getSum(a int, b int) int {
    for b != 0 {
        carry := a & b
        a = a ^ b
        b = carry << 1
    }
    return a
}
```
