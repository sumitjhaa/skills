"""Asyncio Deep — context managers, iterators, Queue, TaskGroup, timeout.
Run: python 10-05-asyncio-deep.py
"""

import asyncio
import random
from typing import AsyncIterator


class AsyncDBConnection:
    def __init__(self, db_name: str):
        self.db_name = db_name

    async def __aenter__(self) -> "AsyncDBConnection":
        await asyncio.sleep(0.05)
        print(f"  [DB] Connected to {self.db_name}")
        return self

    async def __aexit__(self, *_: object) -> None:
        await asyncio.sleep(0.02)
        print(f"  [DB] Closed {self.db_name}")

    async def query(self, sql: str) -> list[dict]:
        await asyncio.sleep(0.1)
        return [{"result": f"data for: {sql[:20]}"}]


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


async def producer(queue: asyncio.Queue[str]) -> None:
    for i in range(10):
        await asyncio.sleep(random.uniform(0.05, 0.15))
        item = f"post_{i}"
        await queue.put(item)
        print(f"  [Producer] Added {item}")
    await queue.put(None)


async def consumer(queue: asyncio.Queue, name: str) -> None:
    while True:
        item = await queue.get()
        if item is None:
            await queue.put(None)
            break
        await asyncio.sleep(0.05)
        print(f"  [Consumer {name}] Processed {item}")


async def main() -> None:
    async with AsyncDBConnection("social_db") as db:
        data = await db.query("SELECT * FROM posts LIMIT 5")
        print(f"  DB result: {data}")

    print("  Paginated results:")
    async for page in PaginatedAPI(total_pages=3):
        print(f"    Page: {page}")

    queue: asyncio.Queue[str] = asyncio.Queue()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(producer(queue))
        tg.create_task(consumer(queue, "A"))
        tg.create_task(consumer(queue, "B"))

    try:
        async with asyncio.timeout(0.5):
            await asyncio.sleep(1)
    except TimeoutError:
        print("  [Timeout] Task exceeded 0.5s")


if __name__ == "__main__":
    asyncio.run(main())
