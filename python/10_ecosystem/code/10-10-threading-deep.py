"""Threading Deep Dive — Lock, RLock, Semaphore, Event, Condition, Barrier, Timer, local.
Run: python 10-10-threading-deep.py
"""

import threading
import time
import random
from queue import Queue


def download(url: str, sem: threading.Semaphore) -> str:
    with sem:
        time.sleep(random.uniform(0.1, 0.3))
        return f"OK: {url}"


if __name__ == "__main__":
    # ── Semaphore: limit concurrent downloads ──
    rate_limiter = threading.Semaphore(3)
    results: list[str] = []
    results_lock = threading.Lock()
    stop_event = threading.Event()

    def worker(q: Queue) -> None:
        local_session = threading.local()
        local_session.id = threading.current_thread().name
        while not stop_event.is_set():
            try:
                url = q.get(timeout=0.5)
                result = download(url, rate_limiter)
                with results_lock:
                    results.append(result)
                q.task_done()
            except Exception:
                pass

    q: Queue[str] = Queue()
    for i in range(10):
        q.put(f"https://site.com/page/{i}")

    threads = [
        threading.Thread(target=worker, args=(q,), daemon=True, name=f"worker-{i}")
        for i in range(4)
    ]
    for t in threads:
        t.start()

    q.join()
    stop_event.set()
    for t in threads:
        t.join(timeout=1)

    print(f"Downloaded {len(results)} URLs")
    print(f"Active threads: {threading.active_count()}")
    print(f"Main thread: {threading.main_thread().name}")

    # ── Barrier: rendezvous ──
    arrived: list[int] = []
    barrier = threading.Barrier(3)

    def rendezvous(idx: int) -> None:
        time.sleep(random.uniform(0.1, 0.5))
        arrived.append(idx)
        barrier.wait()
        print(f"Thread {idx} passed barrier at {time.perf_counter():.3f}")

    threads2 = [threading.Thread(target=rendezvous, args=(i,)) for i in range(3)]
    for t in threads2:
        t.start()
    for t in threads2:
        t.join()

    print(f"Barrier released, all arrived: {sorted(arrived)}")
    print("All threading examples OK")
