# Distributed Order Processing – CS323 Lab 1

## Overview
This project implements a distributed order processing system using `mpi4py` for inter-process communication
and Python's `multiprocessing` module for shared memory and synchronization. A master process generates customer orders and distributes them to worker processes,
which simulate processing time before returning results. The master then collects everything into a shared list protected by a lock.
