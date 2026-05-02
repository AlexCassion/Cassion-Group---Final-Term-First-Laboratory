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
- placeholder for answer

### 5. What issues occurred when multiple workers wrote to shared memory simultaneously?
- placeholder for answer

### 6. How did you ensure consistent results when using multiple processes?
- placeholder for answer
