# ⚡ Asyncio Primitives Deep
<!-- ⏱️ 25 min read | 🔴 Mastery | 🧠 Applied -->

**What You'll Learn:** `asyncio.Lock`, `Semaphore`, `Event`, `Condition`, `Queue`, `TaskGroup`, `timeout`, `Runner`, subprocess, and event loop internals — all async equivalents of threading primitives.

> 💡 **TL;DR — The whole point:** asyncio primitives mirror `threading` but are cooperative (no GIL contention). They're the building blocks of robust async applications. `TaskGroup` (3.11+) gives structured concurrency; `timeout()` prevents hung coroutines.

## 🔗 Why This Matters
Async web scrapers, API gateways, and DB connection pools need rate limiting (Semaphore), signaling (Event), producer-consumer pipelines (Queue), and timeouts — all without blocking the event loop.

## The Concept

| Primitive | Job |
|-----------|-----|
| `Lock` | mutual exclusion in async code |
| `Semaphore` | limit concurrent coroutines (N connections) |
| `Event` | signal one or many waiters |
| `Condition` | await a predicate change |
| `Queue` | async producer-consumer (maxsize, join, task_done) |
| `TaskGroup` | structured concurrency (3.11+) |
| `timeout` / `timeout_at` | raise TimeoutError after a deadline (3.11+) |
| `Runner` | context manager for event loop (3.11+) |
| `subprocess` | async shell commands |
| `run_coroutine_threadsafe` | bridge sync → async |
| `to_thread` | run blocking code in thread pool |

## Code Example

```python
"""Async web scraper with rate limiting and task group."""
import asyncio
import random


async def fetch(url: str, sem: asyncio.Semaphore) -> str:
    async with sem:
        await asyncio.sleep(random.uniform(0.1, 0.3))
        return f"Fetched {url}"


async def main() -> None:
    sem = asyncio.Semaphore(5)  # max 5 concurrent fetches
    urls = [f"https://api.example.com/item/{i}" for i in range(20)]

    # TaskGroup: structured concurrency
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(url, sem)) for url in urls]

    results = [t.result() for t in tasks]
    print(f"Fetched {len(results)} URLs")

    # Queue: producer-consumer
    async def producer(q: asyncio.Queue[int]) -> None:
        for i in range(10):
            await q.put(i)
            await asyncio.sleep(0.05)
        for _ in range(2):
            await q.put(None)  # sentinel

    async def consumer(q: asyncio.Queue, name: str) -> None:
        while True:
            item = await q.get()
            if item is None:
                await q.put(None)  # pass sentinel
                q.task_done()
                break
            print(f"  [{name}] got {item}")
            q.task_done()

    q: asyncio.Queue[int] = asyncio.Queue()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(producer(q))
        tg.create_task(consumer(q, "A"))
        tg.create_task(consumer(q, "B"))


if __name__ == "__main__":
    asyncio.run(main())
```

## 🔍 How It Works
- `asyncio.Lock` — `async with lock:` — only one coroutine enters the critical section
- `asyncio.Semaphore(N)` — `async with sem:` — limits N concurrent coroutines
- `asyncio.Event` — `await event.wait()` blocks until `event.set()`; `event.clear()` resets
- `asyncio.Condition(lock)` — `await cond.wait_for(predicate)` + `cond.notify()`
- `asyncio.Queue(maxsize)` — `await q.put(x)` / `await q.get()`; `q.join()` blocks until all processed
- `TaskGroup` — tasks are cancelled if any task raises; `create_task` schedules a child task
- `asyncio.timeout(5)` — `async with asyncio.timeout(5):` raises `TimeoutError` if block takes >5s
- `asyncio.to_thread(blocking_fn, arg)` — runs in a thread-pool so the event loop isn't blocked
- `asyncio.run_coroutine_threadsafe(coro, loop)` — submit a coroutine from a non-async thread
- `loop.call_soon(fn)` / `loop.call_later(delay, fn)` / `loop.call_at(when, fn)` — schedule callbacks

## ⚠️ Common Pitfall
**Mixing sync and async blocking:** `time.sleep(n)` in a coroutine blocks the entire event loop. Always use `asyncio.sleep(n)`. For blocking I/O (file reads, legacy DB drivers), use `asyncio.to_thread()`.

**Forgetting sentinels:** In async queues, always send a sentinel value (like `None` or a sentinel object) to signal consumers to stop. Count the number of consumers and send that many sentinels.

## 🧠 Memory Aid
"Lock = async with. Semaphore = async with + max N. Event = await wait() until set(). Queue = async put + async get. TaskGroup = structured concurrency (fail one = fail all). Timeout = 'if not done by then, cancel.'"

## 🏃 Try It
Write an async web scraper that fetches 50 pages from `https://httpbin.org/delay/{n}` with a Semaphore of 5 and a per-request timeout of 3 seconds. Print how many succeeded vs timed out.

## 🔗 Related
- [Threading Deep](10-threading-deep.md) — threading equivalents
- [Asyncio Intro](02-asyncio-intro.md) — async fundamentals
- [Socket Networking](13-socket-networking.md) — low-level network I/O

## ➡️ Next
[Socket Networking & Selectors I/O](13-socket-networking.md)
