# 🧵 Concurrency Introduction — Choose Your Weapon
<!-- ⏱️ 18 min read | 🟢 Core | 🧠 Core -->

**What You'll Learn:** The four concurrency models in Python — `threading`, `multiprocessing`, `asyncio`, and `subprocess` — and how to choose the right one for the job.

> 💡 **TL;DR — The whole point:** Python gives you four concurrency tools. Threads for I/O-bound work (shared memory, GIL-limited). Processes for CPU-bound work (separate memory, no GIL). asyncio for high-concurrency I/O (cooperative multitasking). Subprocess for external tools. Pick by bottleneck: I/O → threads or asyncio; CPU → processes.

## 🔗 Why This Matters
A web scraper downloading 1000 pages is I/O-bound — threads or asyncio make it 1000× faster. Processing 1M images is CPU-bound — multiprocessing makes it N× faster on N cores. Using the wrong model wastes resources and adds complexity.

## The Concept

| Model | Primitive | Sharing | GIL | Best For |
|-------|-----------|---------|-----|----------|
| **Threading** | `threading.Thread` | Shared memory | GIL-bound | I/O-bound, blocking APIs |
| **Multiprocessing** | `multiprocessing.Process` | Separate memory | No GIL | CPU-bound |
| **Asyncio** | `async def` / `await` | Cooperative | No contention | High-concurrency I/O |
| **Subprocess** | `subprocess.run` / `Popen` | None (pipes) | N/A | External tools |

**Lock:** prevents race conditions when threads modify shared data.
**GIL:** Global Interpreter Lock — only one thread runs Python bytecode at a time.

## Code Example

```python
"""Compare threading vs multiprocessing vs asyncio for I/O and CPU work."""
import threading
import time
from multiprocessing import Pool
from typing import Any

# I/O-bound (simulated)
posts_to_download = [f"post_{i}" for i in range(8)]

def download_post(post_id: str) -> dict[str, Any]:
    time.sleep(0.1)
    return {"id": post_id, "likes": 42}

def threaded_download() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    lock = threading.Lock()
    def worker(post: str) -> None:
        data = download_post(post)
        with lock:
            results.append(data)
    threads = [threading.Thread(target=worker, args=(p,)) for p in posts_to_download]
    for t in threads: t.start()
    for t in threads: t.join()
    return results

# CPU-bound (simulated word count)
def count_words(text: str) -> dict[str, int]:
    freq: dict[str, int] = {}
    for word in text.split():
        freq[word] = freq.get(word, 0) + 1
    return freq

def parallel_word_count(documents: list[str]) -> list[dict[str, int]]:
    with Pool(4) as pool:
        return pool.map(count_words, documents)

start = time.perf_counter()
results = threaded_download()
print(f"Threaded download: {len(results)} posts in {time.perf_counter() - start:.3f}s")
```

## 🔍 How It Works
- `Thread(target=fn, args=(x,))` — creates a thread; `.start()` launches, `.join()` waits
- `Lock` — `with lock:` ensures only one thread modifies shared data at a time
- `multiprocessing.Pool(4)` — creates 4 worker processes; `.map()` distributes work
- GIL: threads release the GIL during I/O — threading works for I/O-bound tasks
- `subprocess.run(["ffmpeg", ...])` — run any external tool, capture output via pipes

## ⚠️ Common Pitfall
Using threads for CPU-bound work. The GIL caps performance at ~1 core. 8 threads processing images are no faster than 1 thread. Always use `multiprocessing` or NumPy for CPU-heavy work.

## 🧠 Memory Aid
"Threads = I/O waiting (shared memory). Processes = CPU crunching (separate memory). Async = cooperative I/O (one thread, many tasks). Subprocess = 'call external tool.' GIL = 'one bytecode thread at a time.' Lock = 'don't corrupt shared data.'"

## 🏃 Try It
Write a script that downloads 10 URLs from `https://httpbin.org/delay/1` using threads, then using asyncio+httpx. Time both and compare with sequential. Then compute prime numbers up to 100,000 with processes vs threads to see the CPU-bound difference.

## 🔗 Deep Dives
- [Threading Deep — Lock, RLock, Semaphore, Event, Condition, Barrier, local](10-threading-deep.md)
- [Multiprocessing Deep — Pool, Queue, Pipe, Manager, shared_memory](11-multiprocessing-deep.md)
- [Asyncio Intro — fundamentals, gather, run](02-asyncio-intro.md)
- [Asyncio Primitives Deep — Lock, Semaphore, Queue, TaskGroup, timeout](12-asyncio-primitives-deep.md)

## ➡️ Next
Choose your path:
- I need the full threading primer → [Threading Deep](10-threading-deep.md)
- I want async fundamentals first → [Asyncio Introduction](02-asyncio-intro.md)
