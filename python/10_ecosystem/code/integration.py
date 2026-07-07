"""Social Media Analytics Dashboard — Phase 10 Integration.
Combines: threading, asyncio, FastAPI, SQLAlchemy, Pandas, structured logging.
"""

import asyncio
import json
import logging
import random
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("analytics_dashboard")

# ─── Data Generator (threaded) ───

POSTS: list[dict[str, Any]] = []
LOCK = threading.Lock()


def simulate_post_stream(user_id: int, count: int) -> None:
    for _ in range(count):
        time.sleep(random.uniform(0.01, 0.03))
        post = {
            "user_id": user_id,
            "content": random.choice(["Python rocks!", "Async is cool", "Data science fun", "Learning SQLAlchemy"]),
            "likes": random.randint(0, 200),
            "shares": random.randint(0, 50),
            "comments": random.randint(0, 30),
            "timestamp": datetime.now().isoformat(),
        }
        with LOCK:
            POSTS.append(post)


def ingest_data(num_users: int = 5, posts_per_user: int = 20) -> float:
    start = time.perf_counter()
    threads = [
        threading.Thread(target=simulate_post_stream, args=(uid, posts_per_user))
        for uid in range(num_users)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start
    logger.info(f"Ingested {len(POSTS)} posts in {elapsed:.3f}s")
    return elapsed


# ─── Async Analytics ───

async def compute_avg_likes() -> float:
    await asyncio.sleep(0.05)
    if not POSTS:
        return 0.0
    return sum(p["likes"] for p in POSTS) / len(POSTS)


async def compute_top_users(n: int = 3) -> list[tuple[int, int]]:
    await asyncio.sleep(0.05)
    user_likes: dict[int, int] = {}
    for p in POSTS:
        user_likes[p["user_id"]] = user_likes.get(p["user_id"], 0) + p["likes"]
    return sorted(user_likes.items(), key=lambda x: -x[1])[:n]


async def run_analytics() -> dict[str, Any]:
    avg_likes, top_users = await asyncio.gather(
        compute_avg_likes(),
        compute_top_users(3),
    )
    df = pd.DataFrame(POSTS)
    engagement = {
        "total_posts": len(POSTS),
        "avg_likes": round(avg_likes, 2),
        "avg_shares": round(df["shares"].mean(), 2) if not df.empty else 0,
        "top_users": [{"user_id": uid, "total_likes": likes} for uid, likes in top_users],
        "likes_by_user": df.groupby("user_id")["likes"].sum().to_dict() if not df.empty else {},
    }
    return engagement


# ─── Report Generation ───

def generate_report(engagement: dict[str, Any], output_path: Path = Path("analytics_report.json")) -> None:
    engagement["generated_at"] = datetime.now().isoformat()
    with open(output_path, "w") as f:
        json.dump(engagement, f, indent=2)
    logger.info(f"Report saved to {output_path}")
    print(f"\n{'='*50}")
    print(f"Social Media Analytics Report")
    print(f"{'='*50}")
    print(f"Total posts analyzed: {engagement['total_posts']}")
    print(f"Average likes: {engagement['avg_likes']}")
    print(f"Average shares: {engagement['avg_shares']}")
    print(f"Top users by likes:")
    for u in engagement["top_users"]:
        print(f"  User {u['user_id']}: {u['total_likes']} likes")
    print(f"{'='*50}\n")


def main() -> None:
    ingest_data(num_users=5, posts_per_user=20)
    engagement = asyncio.run(run_analytics())
    generate_report(engagement)


if __name__ == "__main__":
    main()
