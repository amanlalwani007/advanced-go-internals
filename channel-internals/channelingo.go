// Many developers think of channels as a magical conduit, but under the hood, a channel is just a struct protected by a mutex, managed entirely on the heap.

// The Theory
// When you initialize a channel using make(chan T, hint), Go allocates an hchan struct on the heap. Its critical fields look like this:

// Go
// type hchan struct {
//     qcount   uint           // Total data items currently in the queue
//     dataqsiz uint           // Size of the circular queue buffer
//     buf      unsafe.Pointer // Points to an array of dataqsiz elements
//     elemsize uint16
//     closed   uint32
//     elemtype *_type          // Element type
//     sendx    uint           // Buffer index where the next send will write
//     recvx    uint           // Buffer index where the next receive will read
//     recvq    waitq          // List of blocked receivers (sudog linked list)
//     sendq    waitq          // List of blocked senders (sudog linked list)
//     lock     mutex          // Protects all fields in hchan
// }
// Here is exactly what happens during channel operations:

// Buffered Channel Send: Go locks the channel, copies your data into the circular ring buffer (buf), increments sendx, and unlocks. It does not allocate memory dynamically here; it just moves bytes into the pre-allocated buffer.

// Blocking Scenario: If a channel is full (or unbuffered) and a goroutine tries to send data, it can't write to the buffer. The Go runtime creates a wrapper struct called a sudog representing the current goroutine, packs your data into it, appends it to the sendq linked list, and calls gopark() to put the goroutine to sleep.

// Direct Copy Optimization: When a receiver finally arrives, the Go runtime does a brilliant optimization: it removes the sleeping sender from sendq, copies the data directly from the sender's stack to the receiver's stack, and wakes the sender up. The data bypasses the channel buffer entirely!

package main

import "fmt"

func main() {
	ch := make(chan int, 2)
	// 1. Sending data updates internal counters
	ch <- 10
	ch <- 20
	fmt.Printf("Sent 2 elements to a buffered channel of capacity 2.\n")

	// what happen if we close a channel ?
	close(ch)
	fmt.Println("Channel closed.")

	// Go internals allows you to  drain a closed channel buffer
	val1, ok1 := <-ch
	fmt.Printf("Read 1: %d, Open %t\n ", val1, ok1)

	val2, ok2 := <-ch
	fmt.Printf("Read 1: %d, Open %t\n ", val2, ok2)
	// 3. once empty reading a closed channel returns the zero values immediately
	//
	val3, ok3 := <-ch
	fmt.Printf("Read 3 (Empty & Closed): %d, Open: %t\n", val3, ok3)

	// 4. panic testing : Sending to a closed channel causes a immediate panic
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf("Caught expected runtime panic: %v\n", r)
		}
	}()
	ch <- 30 // this will trigger  panic

}
