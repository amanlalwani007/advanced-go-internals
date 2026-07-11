// Go is a garbage-collected language, but to write highly optimized code, you need to know whether your variables land on the Stack or the Heap.

// The Theory
// Stack Allocation: Incredibly fast. Memory is automatically cleaned up when the function returns.

// Heap Allocation: Slower. Requires the Garbage Collector (GC) to clean it up later, which consumes CPU cycles.

// Go uses a compiler phase called Escape Analysis to determine this automatically. If a variable's lifetime outlives the stack frame of the function that created it, it escapes to the heap.

package main

type Data struct {
	Value int
}

// Does NOT escape. Returning a value copies it onto the caller's stack frame.
func stayOnStack() Data {
	d := Data{Value: 42}
	return d
}

// ESCAPES to the heap. Returning a pointer means the caller needs to access
// memory allocated inside this function after this function vanishes.
func escapeToHeap() *Data {
	d := Data{Value: 100}
	return &d // Pointer escapes to heap!
}

func main() {
	_ = stayOnStack()
	_ = escapeToHeap()
}
