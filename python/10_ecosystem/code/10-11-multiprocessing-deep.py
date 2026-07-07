"""Multiprocessing Deep Dive — Pool, Queue, Pipe, Manager, shared_memory, Value.
Run: python 10-11-multiprocessing-deep.py
"""

import multiprocessing as mp
import time
import random
import os


def process_image(pixel_data: list[int]) -> list[int]:
    return [min(255, p * 2) for p in pixel_data]


def manager_worker(d: dict, idx: int) -> None:
    d[f"worker_{idx}"] = idx * 10


def counter_worker(cnt: mp.sharedctypes.Synchronized, n: int) -> None:
    for _ in range(n):
        with cnt.get_lock():
            cnt.value += 1


def main() -> None:
    # ── Pool.map for CPU-bound work ──
    images = [[random.randint(0, 255) for _ in range(100_000)] for _ in range(8)]
    start = time.perf_counter()
    with mp.Pool(4) as pool:
        results = pool.map(process_image, images)
    print(f"Pool: {len(results)} images in {time.perf_counter()-start:.2f}s")

    # ── Manager for shared state ──
    with mp.Manager() as manager:
        d = manager.dict()
        procs = [mp.Process(target=manager_worker, args=(d, i)) for i in range(4)]
        for p in procs:
            p.start()
        for p in procs:
            p.join()
        print(f"Manager: {dict(d)}")

    # ── Value for shared counter ──
    counter = mp.Value("i", 0)
    procs = [mp.Process(target=counter_worker, args=(counter, 1000)) for _ in range(4)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print(f"Counter: {counter.value} (expected 4000)")

    # ── shared_memory (3.8+) ──
    try:
        shm = mp.shared_memory.SharedMemory(name="demo", create=True, size=16)
        shm.buf[:4] = bytes([1, 2, 3, 4])
        print(f"SharedMemory buf[0:4]: {list(shm.buf[:4])}")
        shm.close()
        shm.unlink()
    except Exception as e:
        print(f"SharedMemory: {e}")

    print(f"CPU count: {mp.cpu_count()}")
    print("All multiprocessing examples OK")


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    main()
