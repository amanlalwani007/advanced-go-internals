// ypassing the GC with sync.Pool
// Now that you know the Garbage Collector sweeps up White objects on the heap, let's learn how elite Go engineers bypass the GC entirely for high-throughput systems (like network routers or JSON parsers).

// The Theory
// Every time you allocate a struct or a byte slice on the heap, you give the GC work to do later. If you do this tens of thousands of times per second, your application will choke on GC cycles.

// sync.Pool provides a way to reuse previously allocated objects.

// Under the Hood:
// A sync.Pool manages a local cache of objects distributed across your logical processors (P).

// When you call Pool.Get(), Go checks if the current P has a cached object in its private slot or shared list. If it does, it returns it instantly without any new heap allocation.

// If the pool is empty, it runs your custom New() allocation function.

// When you are done, you call Pool.Put(x) to return the object to the pool.

// GC Interaction: Objects in a sync.Pool are automatically cleared during garbage collection cycles if they aren't actively referenced anywhere else. This prevents memory leaks.
package main

import (
	"fmt"
	"runtime"
	"sync"
)

type LargeBuffer struct {
	Data [1024]byte // 1 Kb bufffer
}

var bufferPool = sync.Pool{
	New: func() interface{} {
		// this runs when pool is empty
		return &LargeBuffer{}
	},
}
var EscapeSink *LargeBuffer

func main() {
	// measures memory allocation for standard aloocation heap
	var m1, m2 runtime.MemStats
	// Add a global variable at the top of your file

	runtime.GC()
	runtime.ReadMemStats(&m1)
	// Simulation 1 :- No pool (creating new objects constantly)
	for i := 0; i < 10000; i++ {
		b := &LargeBuffer{}
		b.Data[0] = 1
		// b falls out of scope , leave garbage on heap
		EscapeSink = b
	}
	runtime.ReadMemStats(&m2)
	fmt.Printf("Without Pool -> Heap Allocations Raised By: %d KB\n", (m2.TotalAlloc-m1.TotalAlloc)/1024)
	// Force clean slate again
	runtime.GC()
	runtime.ReadMemStats(&m1)

	// Simulation 2: Using sync.Pool
	for i := 0; i < 10000; i++ {
		// Borrow from pool (Assert type to pointer)
		b := bufferPool.Get().(*LargeBuffer)
		b.Data[0] = 1

		// Reset data state before putting back to prevent data corruption/leaks
		b.Data[0] = 0

		// Return to pool for immediate reuse by the next iteration
		bufferPool.Put(b)
	}
	runtime.ReadMemStats(&m2)
	fmt.Printf("With sync.Pool -> Heap Allocations Raised By: %d KB\n", (m2.TotalAlloc-m1.TotalAlloc)/1024)
	fmt.Println("\nNotice how sync.Pool dramatically dropped total memory allocations to almost zero!")

}

// KEY INTERNAL FACT: Go maps are implemented as hash tables built of buckets (bmap structs).
// 1. Direct Lookups: Go hashes the key. The lower hash bits jump to the target bucket,
//    while the higher bits (Top Hash) fast-scan the 8-slot array inside that bucket -> O(1) average time.
// 2. Map Evacuation: As the map grows, buckets double, and data shifts to new memory addresses.
// 3. Forced Randomization: To prevent developers from relying on a transient order, the Go runtime
//    actively randomizes the starting bucket and slot index every time a 'for range' loop begins.
