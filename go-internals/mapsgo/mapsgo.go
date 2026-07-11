// Go maps are implemented as hash tables made of "buckets". Understanding how they work explains why map iteration order is completely randomized.

// The Theory
// A Go map pointer points to an hmap struct.

// An hmap contains an array of buckets (bmap).

// Each bucket holds up to 8 key-value pairs.

// When you look up a key, Go hashes it. The lower bits of the hash determine which bucket to look in. The high bits (Top Hash) find the specific key inside that bucket.

// If a bucket fills up, Go chains an overflow bucket to it. If there are too many overflow buckets, Go triggers a gradual evacuation/eviction to double the bucket count.

// Internal Fact: Go explicitly randomizes map iteration. Because a map's layout changes during growth, relying on a specific order would cause subtle bugs. Go forces a random starting bucket every time you use range.

// 2. How the Time Complexity is $O(1)$In computer science, $O(1)$ (Constant Time) means the time it takes to find an item does not depend on how many items are in the map. Whether the map has 10 items or 10,000,000 items, the operation takes roughly the same number of steps.Here is exactly why Go maps achieve this:Step A: Direct Array Indexing via Hashing (Constant Time)When you call val := myMap["key"], Go passes "key" through a hash function. This operation takes a constant amount of time because hashing a string or integer depends only on the size of the key itself, not how full the map is.Let's say the hash output is a 64-bit integer: 10110101...00110Go looks at hmap.B. If B = 3, there are $2^3 = 8$ buckets.Go takes the last 3 bits of the hash (110 in binary = 6 in decimal).It goes directly to hmap.buckets[6]. Because buckets is a contiguous array in memory, jumping to index 6 is a direct memory address calculation (an $O(1)$ operation).

// type hmap struct {
//     count     int    // Number of elements currently in the map
//     flags     uint8  // Flags (e.g., if the map is currently being written to)
//     B         uint8  // Log2 of number of buckets (total buckets = 2^B)
//     noverflow uint16 // Approximate number of overflow buckets
//     hash0     uint32 // Hash seed (randomized at map creation for security)

//     buckets    unsafe.Pointer // Pointer to an array of 2^B Buckets
//     oldbuckets unsafe.Pointer // Pointer to previous bucket array (only during growing)
//     nevacuate  uintptr        // Progress counter for resizing/evacuation

//     extra *mapextra // Optional fields (like pointers to overflow buckets)
// }

// Step A: Direct Array Indexing via Hashing (Constant Time)When you call val := myMap["key"], Go passes "key" through a hash function. This operation takes a constant amount of time because hashing a string or integer depends only on the size of the key itself, not how full the map is.Let's say the hash output is a 64-bit integer: 10110101...00110Go looks at hmap.B. If B = 3, there are $2^3 = 8$ buckets.Go takes the last 3 bits of the hash (110 in binary = 6 in decimal).It goes directly to hmap.buckets[6]. Because buckets is a contiguous array in memory, jumping to index 6 is a direct memory address calculation (an $O(1)$ operation).Step B: Scanning a Fixed-Size Bucket (Constant Time)Once Go is inside bucket 6, it has to find the exact key.It loops through the tophash array.Because a bucket size is hard-coded to a maximum of 8 elements, this loop will run at most 8 times.In big-O notation, looping a maximum of 8 times is a constant bounding factor ($O(8)$ simplifies to $O(1)$).What about Overflow Buckets? (The Worst Case)If many keys map to the exact same bucket (a hash collision), Go attaches an overflow bucket. If you had to traverse a chain of 1,000 overflow buckets, the time complexity would degrade to $O(N)$ (linear time).Go prevents this degradation using two mechanisms:Cryptographic Hashing Seed (hash0): Every time you create a new map, Go generates a random hash0 seed. This ensures that even if an attacker tries to feed your map identical-looking keys to force collisions (a Hash DoS attack), the keys will hash to completely different buckets on every run.Evacuation / Resizing: Go monitors the Load Factor (number of items / number of buckets). If the load factor exceeds 6.5 (meaning buckets are averaging more than 6.5 items out of 8), Go triggers a resize. It doubles the bucket array size (B = B + 1) and gradually moves items over.

package main

import "fmt"

func main() {
	m := map[string]int{
		"apple":  1,
		"banana": 2,
		"cherry": 3,
		"date":   4,
	}
	// Test 1: Random Iteration Order
	fmt.Println("Run 1:")
	for k, v := range m {
		fmt.Printf("%s: %d | ", k, v)
	}
	fmt.Println("\n\nRun 2:")
	for k, v := range m {
		fmt.Printf("%s: %d | ", k, v)
	}
	fmt.Println("\n\n(If you run this program multiple times, the order will shuffle.)")

	// Test 2: Map elements are NOT addressable
	// The line below will fail to compile if uncommented:
	// ptr := &m["apple"]
	// Error: cannot take the address of m["apple"]

	fmt.Println("\nWhy can't we take the address of a map element?")
	fmt.Println("Because as the map grows, it evacuates buckets and moves items to new memory addresses!")
}
