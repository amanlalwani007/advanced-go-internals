// Go’s GC is designed for low latency. It targets sub-millisecond stop-the-world (STW) pauses. To achieve this, it uses a Tri-color Concurrent Mark and Sweep algorithm backed by a Write Barrier.

// The Theory
// During the collection phase, objects on the heap are color-coded into three conceptual sets:

// White: Candidate objects for garbage collection.

// Grey: Reachable objects, but their referenced child objects haven't been scanned yet.

// Black: Reachable objects whose references have been fully scanned. They will not be deleted.

// The Process:
// Mark Phase: The GC starts by looking at the "Roots" (global variables, stacks, registers) and marks those objects as Grey.

// Concurrent Scanning: While your application code runs, background GC workers pick up Grey objects, turn them Black, and turn any objects they point to into Grey.

// The Write Barrier: Because your code is running concurrently with the GC, your code might create a new pointer or shift objects around. The runtime activates a Write Barrier—a tiny piece of code hooked onto pointer mutations. If your application attempts to hide a White object behind a Black object, the Write Barrier catches it and forces the object to turn Grey, preventing the GC from accidentally deleting active memory.

// Sweep Phase: Once all Grey objects are exhausted, everything left as White is completely unreachable and its memory is reclaimed.
//

package main

import (
	"fmt"
	"runtime"
	"time"
)

func main() {
	var m runtime.MemStats
	// read baseline memory stats
	runtime.ReadMemStats(&m)
	fmt.Printf("Baseline heap alloc: %d KB\n", m.HeapAlloc/1024)

	// allocate a singnificat chuck of memory
	allocateHeapMemory()
	runtime.ReadMemStats(&m)
	fmt.Printf("After Allocation Heap Alloc: %d KB\n", m.HeapAlloc/1024)

	// 2. Explicitly force a Garbage Collection cycle
	fmt.Println("\nForcing Garbage Collection...")
	runtime.GC()
	// Give the concurrent sweep a millisecond to stabilize stats
	time.Sleep(50 * time.Millisecond)

	runtime.ReadMemStats(&m)
	fmt.Printf("Post-GC Heap Alloc: %d KB\n", m.HeapAlloc/1024)
	fmt.Printf("Number of GC Cycles completed: %d\n", m.NumGC)

}

func allocateHeapMemory() {
	// creating a large slice of slices forces heap allocation
	lotsOfData := make([][]byte, 1000)
	for i := range lotsOfData {
		lotsOfData[i] = make([]byte, 1024) // 1 kb each
	}
	// Once this function exits, lotsOfData is out of scope and eligible for GC
	_ = lotsOfData
}
