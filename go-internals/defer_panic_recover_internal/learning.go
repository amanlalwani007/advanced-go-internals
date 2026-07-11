// When you use the defer keyword, the compiler doesn't just queue a function call. It creates a _defer struct instance on the goroutine's local stack (or heap if it escapes).

// Go
// type _defer struct {
//     started bool
//     heap    bool
//     sp      uintptr  // Stack pointer where the defer was registered
//     pc      uintptr  // Program counter pointing to the deferred function
//     fn      *funcval // The actual function to execute
//     link    *_defer  // Linked list pointing to the NEXT deferred function
// }
// The Stack Linked List: Every goroutine has a _defer pointer pointing to a linked list of these structs. When you call defer, a new node is pushed to the head of the list (LIFO - Last In, First Out).

// Open-Coded Defers Optimization: In modern Go versions, if your defer statement is simple and not inside a loop, the compiler performs an optimization called open-coded defers. It removes the struct overhead completely and inserts the deferred code directly into the function’s exit paths, making it almost as fast as a regular function call.

// Panic Traversal: When a panic occurs, the runtime halts normal execution and begins walking up the _defer linked list of the current goroutine. It executes each deferred function one by one. If one of those functions contains a call to recover(), the runtime stops the panic loop, captures the panic value, and resumes normal execution context right after the function that deferred the recovery.
package main

import "fmt"

func main() {
	fmt.Println("Starting Execution")
	outerFunction()
	fmt.Println("Returned safely to main after recovery!")

}

func outerFunction() {
	// Recovering from panic must happen inside a deferred function
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf("Recovered in outerFunction! Panic Payload: %v\n", r)

		}
	}()
	fmt.Println("Calling innerFunction...")
	innerFunction()
	fmt.Println("This line will never print because innerFunction panics.")
}

func innerFunction() {
	i := 0

	// 2. Arguements to deferred functions are evaluated immediately , not at execution time
	// i is evaluated as 0 right now
	defer fmt.Printf("Deffered lina A(Evaluated when i=%d)\n", i)
	i = 10
	// 3. Defers are executed LIFO (Last In, First Out)
	defer fmt.Println("Deferred Line B (Executed first during unwind)")

	fmt.Println("About to panic...")
	panic("CRITICAL_FAILURE")
}
