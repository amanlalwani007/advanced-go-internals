// Many developers think a slice is an array, but it’s actually a small, lightweight header (a struct) that points to a backing array.

// The Theory
// Under the hood, a slice header is defined in the Go runtime (reflect.SliceHeader) as:

// Go
// type SliceHeader struct {
//     Data uintptr // Pointer to the underlying backing array
//     Len  int     // Current length of the slice
//     Cap  int     // Total capacity of the backing array
// }
// When you pass a slice to a function, Go passes this header by value (copies the pointer, length, and capacity). If the slice grows beyond its capacity during an append, Go allocates a new, larger backing array, copies the old data over, and updates the pointer.

package main

import (
	"fmt"
)

func main() {
	s1 := make([]int, 2, 2)
	s1[0] = 10
	s1[1] = 20
	// Inspect the underlying backing array address
	// Inspect the underlying backing array address
	fmt.Printf("s1: len=%d, cap=%d, backing_array_ptr=%p\n", len(s1), cap(s1), s1)

	s2 := append(s1, 30)
	fmt.Printf("s")
	fmt.Printf("s2 (after append): len=%d, cap=%d, backing_array_ptr=%p\n", len(s2), cap(s2), s2)
	fmt.Println("Notice that the backing array pointer changed because Go allocated a new array!")

	printSeparator()
	// 3. Sub-slicing shares the SAME backing array if capacity isn't exceeded
	base := []int{1, 2, 3, 4, 5}
	sub := base[1:3] // len=2, cap=4 (from index 1 to the end of base's backing array)

	fmt.Printf("base: %v, ptr=%p\n", base, base)
	fmt.Printf("sub : %v, ptr=%p (Points to &base[1])\n", sub, sub)

	// Modifying sub modifies base!
	sub[0] = 99
	fmt.Printf("After modifying sub[0]: base=%v, sub=%v\n", base, sub)

}

func printSeparator() {
	fmt.Println("\n--------------------------------------------------\n")
}
