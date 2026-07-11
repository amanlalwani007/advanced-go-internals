# Chapter 12 — Trie (Prefix Tree)

## Overview
A Trie is a tree-like data structure for storing strings, where each node represents a character. It enables fast prefix-based lookups (O(L) where L is word length).

**Time Complexity:** O(L) for insert/search/startsWith
**Space Complexity:** O(N * L) where N is number of words and L is average length

---

## MCQ

### Q1: What is the main advantage of a Trie over a Hash Set for string storage?

**Options:**
- Tries use less memory for all cases.
- Tries support efficient prefix-based searches (words with a common prefix).
- Tries support O(1) lookup for any string.
- Tries can store non-string data types.

**Answer:** Tries support efficient prefix-based searches (words with a common prefix).

---

### Q2: The height of a Trie node corresponds to:

**Options:**
- The number of words stored.
- The length of the word ending at that node.
- The alphabet size (26 for English).
- The total number of characters stored.

**Answer:** The length of the word ending at that node.

---

## Coding Problems

### Problem 1: Implement Trie (Prefix Tree)

```go
type TrieNode struct {
    children [26]*TrieNode
    isEnd    bool
}

type Trie struct {
    root *TrieNode
}

func Constructor() Trie {
    return Trie{root: &TrieNode{}}
}

func (t *Trie) Insert(word string) {
    node := t.root
    for _, ch := range word {
        idx := ch - 'a'
        if node.children[idx] == nil {
            node.children[idx] = &TrieNode{}
        }
        node = node.children[idx]
    }
    node.isEnd = true
}

func (t *Trie) Search(word string) bool {
    node := t.root
    for _, ch := range word {
        idx := ch - 'a'
        if node.children[idx] == nil {
            return false
        }
        node = node.children[idx]
    }
    return node.isEnd
}

func (t *Trie) StartsWith(prefix string) bool {
    node := t.root
    for _, ch := range prefix {
        idx := ch - 'a'
        if node.children[idx] == nil {
            return false
        }
        node = node.children[idx]
    }
    return true
}
```

### Problem 2: Word Search II (Board + Trie)

```go
func findWords(board [][]byte, words []string) []string {
    // build trie
    root := &TrieNode{}
    for _, w := range words {
        node := root
        for _, ch := range w {
            idx := ch - 'a'
            if node.children[idx] == nil {
                node.children[idx] = &TrieNode{}
            }
            node = node.children[idx]
        }
        node.isEnd = true
    }
    result := make(map[string]bool)
    visited := make([][]bool, len(board))
    for i := range visited {
        visited[i] = make([]bool, len(board[0]))
    }
    var dfs func(r, c int, node *TrieNode, path []byte)
    dfs = func(r, c int, node *TrieNode, path []byte) {
        if node.isEnd {
            result[string(path)] = true
        }
        if r < 0 || c < 0 || r >= len(board) || c >= len(board[0]) || visited[r][c] {
            return
        }
        idx := board[r][c] - 'a'
        if node.children[idx] == nil {
            return
        }
        visited[r][c] = true
        path = append(path, board[r][c])
        dfs(r-1, c, node.children[idx], path)
        dfs(r+1, c, node.children[idx], path)
        dfs(r, c-1, node.children[idx], path)
        dfs(r, c+1, node.children[idx], path)
        path = path[:len(path)-1]
        visited[r][c] = false
    }
    for r := 0; r < len(board); r++ {
        for c := 0; c < len(board[0]); c++ {
            dfs(r, c, root, []byte{})
        }
    }
    var res []string
    for word := range result {
        res = append(res, word)
    }
    return res
}
```

### Problem 3: Replace Words

```go
func replaceWords(dictionary []string, sentence string) string {
    root := &TrieNode{}
    for _, word := range dictionary {
        node := root
        for _, ch := range word {
            idx := ch - 'a'
            if node.children[idx] == nil {
                node.children[idx] = &TrieNode{}
            }
            node = node.children[idx]
        }
        node.isEnd = true
    }
    words := strings.Split(sentence, " ")
    for i, word := range words {
        node := root
        prefix := ""
        for _, ch := range word {
            idx := ch - 'a'
            if node.children[idx] == nil {
                break
            }
            prefix += string(ch)
            node = node.children[idx]
            if node.isEnd {
                words[i] = prefix
                break
            }
        }
    }
    return strings.Join(words, " ")
}
```
