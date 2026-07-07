# ⚙️ Multiprocessing Deep Dive
<!-- ⏱️ 25 min read | 🔴 Mastery | 🧠 Applied -->

**What You'll Learn:** Every `multiprocessing` primitive — Process, Pool, Queue, Pipe, Lock, Manager, shared_memory, Value, Array — and when multiprocessing beats threading.

> 💡 **TL;DR — The whole point:** Multiprocessing bypasses the GIL by running separate Python processes. Use `Pool` for CPU-bound data-parallel work, `Queue`/`Pipe` for inter-process communication, and `Manager` for shared state. Spawn is safer than fork on modern systems.

## 🔗 Why This Matters
Image processing, video transcoding, ML training, and scientific computing need true parallelism. Multiprocessing is how Python harnesses all CPU cores.

## The Concept

| Primitive | Job |
|-----------|-----|
| `Process` | spawn + manage OS processes |
| `Pool` | worker pool for data-parallel tasks |
| `Queue` | thread- and process-safe FIFO |
| `Pipe` | duplex byte stream between 2 processes |
| `Lock`/`RLock`/`Semaphore` | sync primitives (same API as threading) |
| `Manager` | shared dict/list/Namespace across processes |
| `shared_memory` | zero-copy shared memory buffer (3.8+) |
| `Value`/`Array` | ctypes shared memory |

**Start methods:** `fork` (fast, but unsafe with threads), `spawn` (slow, safe, default on macOS/Windows), `forkserver` (fast + safe).

## Code Example

```python
"""CPU-bound batch image processing with Pool, shared counter, and Manager."""
import multiprocessing as mp
import time
import random


def process_image(pixel_data: list[int]) -> list[int]:
    """CPU-bound: apply filter to each pixel."""
    return [min(255, p * 2) for p in pixel_data]


# Pool.map for data-parallel work
images = [[random.randint(0, 255) for _ in range(100_000)] for _ in range(8)]
start = time.perf_counter()
with mp.Pool(4) as pool:
    results = pool.map(process_image, images)
print(f"Pool.map processed {len(results)} images in {time.perf_counter()-start:.2f}s")

# Manager for shared state
def worker(shared_dict: dict, idx: int) -> None:
    shared_dict[f"worker_{idx}"] = idx * 10

with mp.Manager() as manager:
    d = manager.dict()
    procs = [mp.Process(target=worker, args=(d, i)) for i in range(4)]
    for p in procs: p.start()
    for p in procs: p.join()
    print(f"Manager dict: {dict(d)}")
```

## 🔍 How It Works
- `Process(target=fn, args=(x,))` — spawns an OS process; `.start()` runs it; `.join()` waits; `.terminate()` kills; `.kill()` (3.7+) force-kills
- `Pool.map(fn, iterable)` — splits iterable across workers; `starmap` for multiple args; `map_async` for non-blocking; `imap` for lazy iteration; `imap_unordered` for results as they come
- `Queue` — safe for multiple producers/consumers across processes
- `Pipe` — `parent_conn, child_conn = Pipe()`; `.send()`/`.recv()` for duplex
- `Manager` — proxy objects that sync via a background server process
- `shared_memory.SharedMemory` — creates a named memory block; `.buf` is a `memoryview`; must `close()` and `unlink()`
- `Value('i', 0)` / `Array('d', [1.0, 2.0])` — ctypes shared memory with automatic lock

## ⚠️ Common Pitfall
**Sharing state without locks:** Processes don't share memory by default. `Manager.dict()` is synchronized but slower. `shared_memory` is fast but needs manual synchronization. Never share a regular `list` or `dict` between processes — use `Queue`, `Pipe`, or `Manager`.

**Fork safety:** On macOS, Python 3.8+ defaults to `spawn`. On Linux, `fork` can deadlock if threads hold locks at fork time. Use `mp.set_start_method('spawn')` for safety.

## 🧠 Memory Aid
"Pool = parallel map. Queue = process-safe pipeline. Pipe = two-way direct line. Manager = shared office whiteboard. SharedMemory = zero-copy pass-through. Fork = cheap but risky. Spawn = safe but slower."

## 🏃 Try It
Write a batch image processor that uses `Pool.imap_unordered` to apply a sepia filter to 100 synthetic images. Use `Value` to track progress as a counter and print every 10 images.

## 🔗 Related
- [Threading Deep](10-threading-deep.md) — I/O-bound concurrency
- [Socket Networking](13-socket-networking.md) — network I/O
- [Concurrency Intro](01-concurrency-intro.md) — choosing the right model

## ➡️ Next
[Asyncio Primitives Deep](12-asyncio-primitives-deep.md)
