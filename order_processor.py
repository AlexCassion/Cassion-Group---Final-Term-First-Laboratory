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

       # simulate real-world processing time
        delay = random.uniform(0.5, 2.0)
        time.sleep(delay)

        result = {
            "order_id"     : order_id,
            "item"         : item,
            "processed_by" : rank,
            "duration_s"   : round(delay, 2),
        }

        # send the finished result back to master
        comm.send(result, dest=0, tag=2)
        print(f"[Worker {rank}] Finished Order #{order_id} in {delay:.2f}s")
        sys.stdout.flush()


def master_process(comm, size):
    """
    Generate orders, hand them out to workers,
    collect results into shared memory with a Lock.
    """
    item_catalog = [
        "Laptop", "Mechanical Keyboard", "USB-C Hub", "Webcam",
        "Monitor", "Mouse Pad", "SSD", "RAM Kit",
    ]

    num_orders   = random.randint(5, 8)
    orders       = [{"id": i + 1, "item": random.choice(item_catalog)}
                    for i in range(num_orders)]
    worker_count = size - 1            # rank 0 is master

    print(f"\n[Master] Generated {num_orders} orders:")
    for o in orders:
        print(f"         Order #{o['id']} → {o['item']}")
    print()
    sys.stdout.flush()

# ── distribute orders (round-robin across workers) ──────────────────────
    for idx, order in enumerate(orders):
        target_worker = (idx % worker_count) + 1
        comm.send(order, dest=target_worker, tag=1)
        print(f"[Master] Sent Order #{order['id']} to Worker {target_worker}")
        sys.stdout.flush()

    # send shutdown signal to every worker
    for w in range(1, size):
        comm.send(None, dest=w, tag=0)

    # ── collect results & write to shared memory ─────────────────────────────
    print("\n[Master] Waiting for workers to finish...\n")
    sys.stdout.flush()

    for _ in range(num_orders):
        result = comm.recv(source=MPI.ANY_SOURCE, tag=2)

        # Lock ensures only one write at a time → no race conditions
        with lock:
            shared_orders.append(result)
            print(f"[Master] Stored result: {result}")
            sys.stdout.flush()
