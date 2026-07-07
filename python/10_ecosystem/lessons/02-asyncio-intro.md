# ⚡ Asyncio Introduction
<!-- ⏱️ 16 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** `async`/`await` syntax, event loops, coroutines, `asyncio.gather`, `asyncio.run`, and async context managers for real-world I/O.

> 💡 **TL;DR — The whole point:** asyncio lets you write concurrent code that looks sequential. `await` = "pause here, let other tasks run, resume when ready." It's perfect for I/O-bound work like web scraping, API calls, and database queries.

## 🔗 Why This Matters
A social-media dashboard needs to fetch 50 user profiles, 200 posts, and 500 comments from an API. Doing that sequentially takes forever. With asyncio, all requests happen concurrently — the total time is the *slowest* request, not the sum of all requests.

## The Concept
- **Coroutine:** `async def` function — calling it returns a coroutine object (doesn't run yet)
- **Event loop:** the scheduler that runs coroutines and dispatches I/O
- **`await`:** hands control back to the event loop until the awaited operation completes
- **`asyncio.gather`:** run multiple coroutines concurrently and collect results
- **`asyncio.run`:** create, run, and close the event loop

## Code Example
```python
"""Social-media: fetch user profiles and posts concurrently."""

import asyncio
import time
from typing import Any


async def fetch_user_profile(user_id: int) -> dict[str, Any]:
    await asyncio.sleep(0.2)  # simulate API call
    return {"user_id": user_id, "name": f"User{user_id}", "followers": 1000}


async def fetch_recent_posts(user_id: int) -> list[dict[str, Any]]:
    await asyncio.sleep(0.3)  # simulate API call
    return [
        {"id": 1, "content": f"Post by user {user_id}"},
        {"id": 2, "content": f"Another post by user {user_id}"},
    ]


async def get_user_dashboard(user_id: int) -> dict[str, Any]:
    profile, posts = await asyncio.gather(
        fetch_user_profile(user_id),
        fetch_recent_posts(user_id),
    )
    return {"profile": profile, "posts": posts}


async def main() -> None:
    start = time.perf_counter()
    dashboards = await asyncio.gather(
        get_user_dashboard(1),
        get_user_dashboard(2),
        get_user_dashboard(3),
    )
    elapsed = time.perf_counter() - start
    for d in dashboards:
        print(f"User {d['profile']['user_id']}: {len(d['posts'])} posts, {d['profile']['followers']} followers")
    print(f"Total time: {elapsed:.3f}s")


if __name__ == "__main__":
    asyncio.run(main())
```

## 🔍 How It Works
- `asyncio.run(main())` — creates a new event loop, runs `main()`, closes the loop
- `await asyncio.sleep(0.2)` — simulates I/O; the coroutine sleeps without blocking the thread
- `asyncio.gather(*coros)` — runs all coroutines concurrently; waits for all to finish
- Coroutines don't start until they are `await`ed or passed to `asyncio.gather`
- The event loop switches between coroutines whenever they `await`

## ⚠️ Common Pitfall
Calling an `async def` function without `await`. `x = fetch_user_profile(1)` gives you a coroutine object, not the result. Always use `await` or pass to `asyncio.gather`. Also, don't `time.sleep()` inside a coroutine — use `asyncio.sleep()`.

## 🧠 Memory Aid
"`async def` = 'this function can pause.' `await` = 'pause and let others run.' `gather` = 'run all at once.' `asyncio.run` = 'start the engine.'"

## 🏃 Try It
Write an async function that fetches the title of 5 posts from `https://jsonplaceholder.typicode.com/posts/{id}` using `httpx.AsyncClient`. Hint: `httpx.AsyncClient().get()`.

## 🔗 Related
- [Concurrency Introduction](01-concurrency-intro.md) — threads vs processes vs async
- [Asyncio Deep](05-asyncio-deep.md) — advanced asyncio patterns
- [Asyncio Primitives Deep](12-asyncio-primitives-deep.md) — Lock, Semaphore, Queue, TaskGroup
- [Signal & ContextVars](14-signal-contextvars.md) — async-safe per-request context

## ➡️ Next
Continue with [Asyncio Deep](05-asyncio-deep.md) for deeper async patterns, or jump to [Web & APIs](03-web-apis.md) for practical HTTP.
