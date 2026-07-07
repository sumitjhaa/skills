"""Asyncio Primitives Deep — Lock, Semaphore, Event, Queue, TaskGroup, timeout.
Run: python 10-12-asyncio-primitives-deep.py
"""

import asyncio
import random


async def fetch(url: str, sem: asyncio.Semaphore) -> str:
    async with sem:
        await asyncio.sleep(random.uniform(0.1, 0.3))
        return f"Fetched {url}"


async def main() -> None:
    # ── Semaphore + TaskGroup ──
    sem = asyncio.Semaphore(5)
    urls = [f"https://api.example.com/item/{i}" for i in range(20)]

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(url, sem)) for url in urls]

    results = [t.result() for t in tasks]
    print(f"TaskGroup: fetched {len(results)} URLs")

    # ── Queue producer-consumer ──
    sentinel = object()

    async def producer(q: asyncio.Queue) -> None:
        for i in range(10):
            await q.put(i)
            await asyncio.sleep(0.02)
        for _ in range(2):
            await q.put(sentinel)

    async def consumer(q: asyncio.Queue, name: str) -> None:
        while True:
            item = await q.get()
            if item is sentinel:
                q.task_done()
                break
            print(f"  [{name}] processed {item}")
            q.task_done()

    q: asyncio.Queue = asyncio.Queue()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(producer(q))
        tg.create_task(consumer(q, "A"))
        tg.create_task(consumer(q, "B"))
    await q.join()

    # ── Event ──
    event = asyncio.Event()

    async def waiter(n: int) -> None:
        await event.wait()
        print(f"  [Waiter {n}] event triggered")

    async with asyncio.TaskGroup() as tg:
        for i in range(3):
            tg.create_task(waiter(i))
        await asyncio.sleep(0.1)
        event.set()

    # ── timeout ──
    try:
        async with asyncio.timeout(0.1):
            await asyncio.sleep(10)
    except TimeoutError:
        print("Timeout: correctly raised after 0.1s")

    # ── to_thread ──
    def blocking_io(n: int) -> int:
        return n * 2

    result = await asyncio.to_thread(blocking_io, 21)
    print(f"to_thread: 21 * 2 = {result}")

    print("All asyncio primitives examples OK")


if __name__ == "__main__":
    asyncio.run(main())
