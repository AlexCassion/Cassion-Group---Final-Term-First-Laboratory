# Distributed Order Processing – CS323 Lab 1

## Members
Alex Cassion = Cassion 

potato715 = Pabellan 

CS3C = Soriano

Michael Andres = Cabot

Bjurnh = Camariosa


## Overview
This project implements a distributed order processing system using `mpi4py` for inter-process communication and Python's `multiprocessing` module for shared memory and synchronization. A master process generates customer orders and distributes them to worker processes, which simulate processing time before returning results. The master then collects everything into a shared list protected by a lock.

## Reflection Questions

### 1. How did you distribute orders among worker processes?
- The master (rank 0) generates a list of 5–8 orders and uses a round-robin approach to assign them. Each order's index is taken modulo the number of workers, which gives the target worker rank. For example with 3 workers, Order #1 goes to Worker 1, Order #2 to Worker 2, Order #3 to Worker 3, Order #4 back to Worker 1, and so on. The actual sending is done through comm.send(), and workers block on comm.recv() until a message arrives. After all orders are sent, the master sends None to each worker as a shutdown signal.

### 2. What happens if there are more orders than workers?
- Because of the round-robin distribution, extra orders just wrap back around to the first worker again. So if there are 7 orders and 3 workers, Workers 1 and 2 end up with 2 orders each while Worker 3 gets 1. This means some workers finish earlier than others — they receive their shutdown signal and exit while other workers are still processing. It's not perfectly balanced but it works without any worker sitting idle. A smarter approach would be a work-stealing queue where idle workers pull the next available task, but that's more complex to implement.

### 3. How did processing delays affect the order completion?
- placeholder for answer

### 4. How did you implement shared memory, and where was it initialized?
- Shared memory was set up using `multiprocessing.Manager` at the top of the script, before MPI takes over. `manager.list()` returns a proxy object — basically a list that lives in a separate manager server process, and any process that has a reference to it can read and write through that proxy. Since the master is the one collecting results from workers (via MPI), the master is also the one writing to `shared_orders`. The manager and list are initialized at module level so they're ready before the MPI communicator even checks ranks.

### 5. What issues occurred when multiple workers wrote to shared memory simultaneously?
- placeholder for answer

### 6. How did you ensure consistent results when using multiple processes?
- The fix was wrapping every append inside a `with lock:` block. The `Lock()` from `multiprocessing` acts as a mutual exclusion mechanism — only one process can hold the lock at a time. Any other process trying to enter the critical section has to wait until the lock is released. This guarantees that writes to `shared_orders` happen one at a time, preventing any overlap. After adding the lock, the master consistently printed a complete list with the correct number of entries every run, regardless of how the timing played out.
