from mpi4py import MPI
from multiprocessing import Manager, Lock
import time
import random
import sys

# ─────────────────────────────────────────────
#  Shared-memory helpers (used by master only)
# ─────────────────────────────────────────────
manager = Manager()
shared_orders = manager.list()
lock = Lock()


def worker_process(comm, rank):
    """
    Receive orders from master, simulate processing,
    then send the result back.
    """
    while True:
        # block until master sends something
        msg = comm.recv(source=0, tag=MPI.ANY_TAG, status=MPI.Status())

        # None is our shutdown signal
        if msg is None:
            print(f"[Worker {rank}] No more orders, shutting down.")
            sys.stdout.flush()
            break

        order_id = msg["id"]
        item     = msg["item"]

        print(f"[Worker {rank}] Picked up Order #{order_id} → {item}")
        sys.stdout.flush()
