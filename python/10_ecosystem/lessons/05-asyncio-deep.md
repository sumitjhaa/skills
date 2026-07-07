# ⚡ Asyncio Deep
<!-- ⏱️ 18 min read | 🔴 Mastery | 🧠 Mastery -->

**What You'll Learn:** Async context managers (`__aenter__`/`__aexit__`), async iterators (`__aiter__`/`__anext__`), `asyncio.Queue`, `TaskGroup`, `asyncio.timeout`, and error handling in production async code.

> 💡 **TL;DR — The whole point:** Coroutines only get you so far. Async context managers manage resources (DB connections, HTTP clients). Async queues coordinate producers/consumers. Task groups and timeouts keep your app reliable.

## 🔗 Why This Matters
A real-time social-media dashboard connects to a WebSocket for live updates, queries a database for historical data, and calls an ML service for sentiment analysis — all concurrently. Managing these resources and coordinating their lifecycle requires advanced async patterns.

## The Concept
- **`__aenter__`/`__aexit__`** — async context manager protocol (`async with`)
- **`__aiter__`/`__anext__`** — async iterator protocol (`async for`)
- **`asyncio.Queue`** — coroutine-safe producer/consumer coordination
- **`TaskGroup`** — structured concurrency with automatic error propagation
- **`asyncio.timeout`** — raise an exception if a coroutine takes too long

## Code Example
```python
"""Social-media: real-time post processor with advanced async patterns."""

import asyncio
import random
from typing import AsyncIterator


# ─── Async context manager: DB connection ───
class AsyncDBConnection:
    def __init__(self, db_name: str):
        self.db_name = db_name

    async def __aenter__(self) -> "AsyncDBConnection":
        await asyncio.sleep(0.05)  # simulate connect
        print(f"  [DB] Connected to {self.db_name}")
        return self

    async def __aexit__(self, *_: object) -> None:
        await asyncio.sleep(0.02)  # simulate close
        print(f"  [DB] Closed {self.db_name}")

    async def query(self, sql: str) -> list[dict]:
        await asyncio.sleep(0.1)
        return [{"result": f"data for: {sql[:20]}"}]


# ─── Async iterator: paginated API ───
class PaginatedAPI:
    def __init__(self, total_pages: int = 3):
        self._total = total_pages
        self._page = 0

    def __aiter__(self) -> "PaginatedAPI":
        return self

    async def __anext__(self) -> list[str]:
        self._page += 1
        if self._page > self._total:
            raise StopAsyncIteration
        await asyncio.sleep(0.1)
        return [f"post_{self._page}_{i}" for i in range(3)]


# ─── Producer/consumer with Queue ───
async def producer(queue: asyncio.Queue[str]) -> None:
    for i in range(10):
        await asyncio.sleep(random.uniform(0.05, 0.15))
        item = f"post_{i}"
        await queue.put(item)
        print(f"  [Producer] Added {item}")
    await queue.put(None)  # sentinel


async def consumer(queue: asyncio.Queue, name: str) -> None:
    while True:
        item = await queue.get()
        if item is None:
            await queue.put(None)
            break
        await asyncio.sleep(0.05)
        print(f"  [Consumer {name}] Processed {item}")


# ─── Main with TaskGroup ───
async def main() -> None:
    # Async context manager
    async with AsyncDBConnection("social_db") as db:
        data = await db.query("SELECT * FROM posts LIMIT 5")
        print(f"  DB result: {data}")

    # Async iterator
    print("  Paginated results:")
    async for page in PaginatedAPI(total_pages=3):
        print(f"    Page: {page}")

    # Producer/Consumer with Queue
    queue: asyncio.Queue[str] = asyncio.Queue()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(producer(queue))
        tg.create_task(consumer(queue, "A"))
        tg.create_task(consumer(queue, "B"))

    # Timeout
    try:
        async with asyncio.timeout(0.5):
            await asyncio.sleep(1)
    except TimeoutError:
        print("  [Timeout] Task exceeded 0.5s")


if __name__ == "__main__":
    asyncio.run(main())
```

## 🔍 How It Works
- `async with AsyncDBConnection()` calls `__aenter__` on enter, `__aexit__` on exit
- `async for page in PaginatedAPI()` calls `__aiter__`, then `__anext__` until `StopAsyncIteration`
- `asyncio.Queue` is awaitable: `await queue.put(item)` and `await queue.get()`
- `None` sentinel signals consumers to shut down
- `TaskGroup` creates a scope where all tasks complete or all are cancelled on error
- `asyncio.timeout(0.5)` raises `TimeoutError` if the block takes > 0.5s

## ⚠️ Common Pitfall
Forgetting `async with asyncio.TaskGroup()` vs `asyncio.gather()`. `TaskGroup` propagates all exceptions and cancels remaining tasks. `gather` returns exception objects. Use `TaskGroup` for structured concurrency.

## 🧠 Memory Aid
"`__aenter__/__aexit__` = async context manager. `__aiter__/__anext__` = async for loop. Queue = producer/consumer channel. TaskGroup = structured concurrency. timeout = deadline."

## 🏃 Try It
Write an async producer coroutine that generates 20 numbers, one per 0.05s, and puts them on a Queue. Write an async consumer that squares numbers and prints them. Use a TaskGroup to run both.

## 🔗 Related
- [Asyncio Introduction](02-asyncio-intro.md) — async/await basics
- [Concurrent Futures](../08_advanced/lessons/12-concurrent-futures.md) — ThreadPoolExecutor

## ➡️ Next
[FastAPI Deep](06-fastapi-deep.md)
