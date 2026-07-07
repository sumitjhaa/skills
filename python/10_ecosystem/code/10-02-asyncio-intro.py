"""Asyncio Introduction — gather, sleep, and async context managers.
Run: python 10-02-asyncio-intro.py
"""

import asyncio
import time
from typing import Any


async def fetch_user_profile(user_id: int) -> dict[str, Any]:
    await asyncio.sleep(0.2)
    return {"user_id": user_id, "name": f"User{user_id}", "followers": 1000}


async def fetch_recent_posts(user_id: int) -> list[dict[str, Any]]:
    await asyncio.sleep(0.3)
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
