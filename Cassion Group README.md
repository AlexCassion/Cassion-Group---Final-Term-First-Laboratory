# Distributed Order Processing – CS323 Lab 1

## Members
Alex Cassion = Cassion 

potato715 = Pabellan 

CS3C = Soriano

Michael Andres = Cabot

Bjurnh = Camariosa


## Overview
This project implements a distributed order processing system using `mpi4py` for inter-process communication
and Python's `multiprocessing` module for shared memory and synchronization. A master process generates customer orders and distributes them to worker processes,
which simulate processing time before returning results. The master then collects everything into a shared list protected by a lock.

## Reflection Questions

### 1. How did you distribute orders among worker processes?
- placeholder for answer

### 2. What happens if there are more orders than workers?
- placeholder for answer

### 3. How did processing delays affect the order completion?
- placeholder for answer

### 4. How did you implement shared memory, and where was it initialized?
- Shared memory was set up using `multiprocessing.Manager` at the top of the script, before MPI takes over. `manager.list()` returns a proxy object — basically a list that lives in a separate manager server process, and any process that has a reference to it can read and write through that proxy. 

### 5. What issues occurred when multiple workers wrote to shared memory simultaneously?
- placeholder for answer

### 6. How did you ensure consistent results when using multiple processes?
- placeholder for answer
