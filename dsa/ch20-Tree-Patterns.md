# Chapter 20 — Tree Patterns (Binary Trees & BST)

## Overview
Tree patterns including LCA, diameter, max path sum, serialization, and BST construction. These problems test recursive thinking and tree traversal mastery.

---

## MCQ

### Q1: The diameter of a binary tree is:

**Options:**
- The height of the tree.
- The longest path between any two nodes (may or may not pass through root).
- The number of leaf nodes in the tree.
- The total number of nodes in the longest root-to-leaf path.

**Answer:** The longest path between any two nodes (may or may not pass through root).

---

## Coding Problems

### Problem 1: Lowest Common Ancestor of a Binary Tree

```go
func lowestCommonAncestor(root, p, q *TreeNode) *TreeNode {
    if root == nil || root == p || root == q {
        return root
    }
    left := lowestCommonAncestor(root.Left, p, q)
    right := lowestCommonAncestor(root.Right, p, q)
    if left != nil && right != nil {
        return root
    }
    if left != nil { return left }
    return right
}
```

### Problem 2: Diameter of Binary Tree

```go
func diameterOfBinaryTree(root *TreeNode) int {
    diameter := 0
    var dfs func(node *TreeNode) int
    dfs = func(node *TreeNode) int {
        if node == nil { return 0 }
        left := dfs(node.Left)
        right := dfs(node.Right)
        diameter = max(diameter, left+right)
        return 1 + max(left, right)
    }
    dfs(root)
    return diameter
}
```

### Problem 3: Binary Tree Maximum Path Sum

```go
func maxPathSum(root *TreeNode) int {
    maxSum := -1 << 31
    var dfs func(node *TreeNode) int
    dfs = func(node *TreeNode) int {
        if node == nil { return 0 }
        left := max(0, dfs(node.Left))
        right := max(0, dfs(node.Right))
        maxSum = max(maxSum, left+right+node.Val)
        return node.Val + max(left, right)
    }
    dfs(root)
    return maxSum
}
```

### Problem 4: Serialize and Deserialize Binary Tree

```go
type Codec struct{}

func Constructor() Codec { return Codec{} }

func (c *Codec) serialize(root *TreeNode) string {
    var sb strings.Builder
    var dfs func(node *TreeNode)
    dfs = func(node *TreeNode) {
        if node == nil {
            sb.WriteString("null,")
            return
        }
        sb.WriteString(fmt.Sprintf("%d,", node.Val))
        dfs(node.Left)
        dfs(node.Right)
    }
    dfs(root)
    return sb.String()
}

func (c *Codec) deserialize(data string) *TreeNode {
    nodes := strings.Split(data, ",")
    var idx int
    var dfs func() *TreeNode
    dfs = func() *TreeNode {
        if nodes[idx] == "null" {
            idx++
            return nil
        }
        val, _ := strconv.Atoi(nodes[idx])
        idx++
        node := &TreeNode{Val: val}
        node.Left = dfs()
        node.Right = dfs()
        return node
    }
    return dfs()
}
```

### Problem 5: Convert Sorted Array to BST

```go
func sortedArrayToBST(nums []int) *TreeNode {
    if len(nums) == 0 { return nil }
    mid := len(nums) / 2
    root := &TreeNode{Val: nums[mid]}
    root.Left = sortedArrayToBST(nums[:mid])
    root.Right = sortedArrayToBST(nums[mid+1:])
    return root
}
```

### Problem 6: Validate Binary Search Tree

```go
func isValidBST(root *TreeNode) bool {
    return validate(root, nil, nil)
}

func validate(node *TreeNode, min, max *int) bool {
    if node == nil { return true }
    if (min != nil && node.Val <= *min) || (max != nil && node.Val >= *max) {
        return false
    }
    return validate(node.Left, min, &node.Val) &&
           validate(node.Right, &node.Val, max)
}
```
