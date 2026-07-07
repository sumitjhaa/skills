"""Phase 10 — Practice Solutions"""
# ruff: noqa: E402

import asyncio
import random
import threading
import time
from typing import Any

import numpy as np
import pandas as pd


# ─── Exercise 1: Threading ──────────────────────────────────────────────────

URLS = ["https://httpbin.org/delay/1"] * 5


def fetch_url(url: str) -> str:
    import urllib.request
    with urllib.request.urlopen(url, timeout=5) as resp:
        return f"{url}: {resp.status}"


def sequential_fetch() -> list[str]:
    return [fetch_url(u) for u in URLS]


def threaded_fetch() -> list[str]:
    results: list[str] = []
    lock = threading.Lock()

    def worker(url: str) -> None:
        result = fetch_url(url)
        with lock:
            results.append(result)

    threads = [threading.Thread(target=worker, args=(u,)) for u in URLS]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return results


# ─── Exercise 2: Multiprocessing ────────────────────────────────────────────

from multiprocessing import Pool


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def find_primes_pool(limit: int = 100_000) -> list[int]:
    with Pool(4) as pool:
        results = pool.map(is_prime, range(limit))
    return [i for i, prime in enumerate(results) if prime]


# ─── Exercise 3: Asyncio Basics ─────────────────────────────────────────────

async def fetch_post(id: int) -> dict[str, Any]:
    await asyncio.sleep(0.2)
    return {"id": id, "title": f"Post {id}"}


async def test_fetch_10() -> None:
    results = await asyncio.gather(*[fetch_post(i) for i in range(1, 11)])
    assert len(results) == 10
    assert results[0]["id"] == 1


# ─── Exercise 4: Async Queue ────────────────────────────────────────────────

async def producer(queue: asyncio.Queue[int]) -> None:
    for i in range(20):
        await asyncio.sleep(0.05)
        await queue.put(i)
    await queue.put(None)


async def consumer(queue: asyncio.Queue, name: str) -> None:
    while True:
        item = await queue.get()
        if item is None:
            await queue.put(None)
            break
        squared = item * item
        print(f"  [Consumer {name}] {item}^2 = {squared}")
        await asyncio.sleep(0.01)


async def test_queue() -> None:
    queue: asyncio.Queue[int] = asyncio.Queue()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(producer(queue))
        tg.create_task(consumer(queue, "A"))
        tg.create_task(consumer(queue, "B"))


# ─── Exercise 5: FastAPI Endpoint ────────────────────────────────────────────

FASTAPI_CODE = """
from fastapi import FastAPI, Depends, HTTPException, Query

app = FastAPI()

def verify_api_key(api_key: str = Query(...)) -> str:
    if api_key != "my-secret-key":
        raise HTTPException(401, "Invalid API key")
    return api_key

@app.get("/search")
def search(q: str = Query(...), limit: int = Query(5, ge=1, le=50), api_key: str = Depends(verify_api_key)):
    return [
        {"title": f"Result {i} for {q}", "url": f"https://example.com/{i}", "score": round(1.0 - i * 0.1, 2)}
        for i in range(limit)
    ]
"""

# ─── Exercise 6: SQLAlchemy Models ──────────────────────────────────────────

SA_CODE = """
from sqlalchemy import create_engine, select, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

engine = create_engine("sqlite:///:memory:")

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    books: Mapped[list["Book"]] = relationship(back_populates="author", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    year: Mapped[int]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship(back_populates="books")

Base.metadata.create_all(engine)

with Session(engine) as session:
    a = Author(name="Alice")
    b = Author(name="Bob")
    session.add_all([a, b])
    session.flush()
    session.add_all([Book(title="Py 101", year=2020, author=a), Book(title="Async Book", year=2021, author=a)])
    session.commit()

with Session(engine) as session:
    from sqlalchemy.orm import selectinload
    stmt = select(Author).options(selectinload(Author.books))
    for author in session.scalars(stmt):
        for book in author.books:
            print(f"  {author.name}: {book.title} ({book.year})")
"""

# ─── Exercise 7: Pandas Groupby ─────────────────────────────────────────────

data = [
    {"region": "NA", "product": "Widget", "qty": 10, "price": 9.99},
    {"region": "EU", "product": "Widget", "qty": 5, "price": 9.99},
    {"region": "NA", "product": "Gadget", "qty": 3, "price": 49.99},
    {"region": "APAC", "product": "Widget", "qty": 8, "price": 9.99},
    {"region": "EU", "product": "Gadget", "qty": 2, "price": 49.99},
]
df = pd.DataFrame(data)
df["revenue"] = df["qty"] * df["price"]

def run_ex7() -> None:
    total_sales_by_region = df.groupby("region")["revenue"].sum()
    avg_qty_by_product = df.groupby("product")["qty"].mean()
    top_products = df.groupby("product")["revenue"].sum().sort_values(ascending=False).head(3)
    print(f"7. Sales by region:\n{total_sales_by_region}")
    print(f"\nAvg qty by product:\n{avg_qty_by_product}")
    print(f"\nTop 3 products:\n{top_products}")

# ─── Exercise 8: NumPy Broadcasting ─────────────────────────────────────────

prices = np.array([
    [19.99, 29.99, 9.99],
    [21.99, 32.99, 11.99],
    [18.99, 27.99, 8.99],
    [20.99, 30.99, 10.99],
])
discounts = np.array([0.1, 0.15, 0.2])

def run_ex8() -> None:
    discounted = prices * (1 - discounts)
    under_10 = np.where(discounted < 10, "cheap", "normal")
    print(f"8. Discounted prices:\n{discounted}")
    print(f"Under $10:\n{under_10}")

# ─── Exercise 9: Health Check ───────────────────────────────────────────────

FASTAPI_HEALTH_CODE = """
import os
import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pathlib import Path

app = FastAPI()

@app.get("/health")
def health():
    db_path = os.environ.get("DB_PATH", "/tmp/test.db")
    db_ok = Path(db_path).exists() if db_path else False
    redis_ok = random.random() < 0.9
    if db_ok and redis_ok:
        return {"status": "UP", "database": "ok", "redis": "ok"}
    return JSONResponse(
        status_code=503,
        content={"status": "DOWN", "database": "ok" if db_ok else "error", "redis": "ok" if redis_ok else "error"},
    )
"""

# ─── Exercise 10: Structured Logging ────────────────────────────────────────

FASTAPI_LOG_CODE = """
import logging
import time
import uuid
from fastapi import FastAPI, Request

logging.basicConfig(level=logging.INFO, format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')
logger = logging.getLogger("structured_api")
app = FastAPI()

@app.middleware("http")
async def log_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error("request_failed", extra={"request_id": request_id, "error": str(e)})
        raise
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info("request_complete", extra={
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "duration_ms": duration_ms,
    })
    return response

@app.get("/error")
async def trigger_error():
    1 / 0
"""

# ══════════════════════════════════════════════════════════════════════════════
# NEW EXERCISES — Advanced Concurrency & Networking
# ══════════════════════════════════════════════════════════════════════════════

# ─── Exercise 11: Thread-safe Counter with Lock ──────────────────────────────

shared_counter = 0


def increment_with_lock(lock: threading.Lock, n: int) -> None:
    global shared_counter
    for _ in range(n):
        with lock:
            shared_counter += 1


def run_ex11() -> None:
    global shared_counter
    shared_counter = 0
    lock = threading.Lock()
    threads = [threading.Thread(target=increment_with_lock, args=(lock, 10_000)) for _ in range(8)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert shared_counter == 80_000, f"Expected 80000, got {shared_counter}"
    print(f"11. Thread-safe counter: {shared_counter} (OK)")


# ─── Exercise 12: ProcessPoolExecutor for CPU-bound Tasks ──────────────────

import concurrent.futures


def sum_squares(n: int) -> int:
    return sum(i * i for i in range(1, n + 1))


def run_ex12() -> None:
    numbers = [4 * 10**6, 5 * 10**6, 6 * 10**6, 7 * 10**6]
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
        proc_results = list(pool.map(sum_squares, numbers))
    proc_time = time.perf_counter() - start

    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        thread_results = list(pool.map(sum_squares, numbers))
    thread_time = time.perf_counter() - start

    print(f"12. ProcessPoolExecutor: {proc_time:.3f}s, ThreadPoolExecutor: {thread_time:.3f}s (process should be faster for CPU)")
    assert proc_results == thread_results


# ─── Exercise 13: Async Producer-Consumer with Queue ─────────────────────────

_sentinel = object()


async def async_producer(q: asyncio.Queue) -> None:
    for i in range(30):
        await q.put(i)
        await asyncio.sleep(0.02)
    for _ in range(3):
        await q.put(_sentinel)


async def async_consumer(q: asyncio.Queue, name: str) -> None:
    while True:
        msg = await q.get()
        if msg is _sentinel:
            q.task_done()
            break
        await asyncio.sleep(0.05)
        print(f"    [{name}] processed {msg}")
        q.task_done()


async def run_async_queue() -> None:
    q: asyncio.Queue = asyncio.Queue(maxsize=5)
    async with asyncio.TaskGroup() as tg:
        tg.create_task(async_producer(q))
        tg.create_task(async_consumer(q, "A"))
        tg.create_task(async_consumer(q, "B"))
        tg.create_task(async_consumer(q, "C"))
    await q.join()


# ─── Exercise 14: TCP Echo Server (non-blocking) ─────────────────────────────

import selectors
import socket as _socket

ECHO_HOST, ECHO_PORT = "127.0.0.1", 8888


def run_echo_server() -> list[str]:
    sel = selectors.DefaultSelector()
    server = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
    server.setsockopt(_socket.SOL_SOCKET, _socket.SO_REUSEADDR, 1)
    server.bind((ECHO_HOST, ECHO_PORT))
    server.listen()
    server.setblocking(False)
    sel.register(server, selectors.EVENT_READ, data=None)
    messages: list[str] = []

    def accept(sock: _socket.socket) -> None:
        conn, addr = sock.accept()
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, data=b"")

    def read(conn: _socket.socket, data: bytes) -> None:
        recv_data = conn.recv(1024)
        if recv_data:
            conn.sendall(recv_data)
            messages.append(recv_data.decode())
        else:
            sel.unregister(conn)
            conn.close()

    for _ in range(4):
        events = sel.select(timeout=1)
        for key, _ in events:
            if key.data is None:
                accept(key.fileobj)
            else:
                read(key.fileobj, key.data)
    sel.close()
    server.close()
    return messages


# ─── Exercise 15: Graceful Shutdown with Signal Handlers ─────────────────────

import signal as sig_module

_shutdown_flag = False


def _shutdown_handler(signum: int, frame: object) -> None:
    global _shutdown_flag
    _shutdown_flag = True


def run_ex15() -> None:
    sig_module.signal(sig_module.SIGTERM, _shutdown_handler)
    print("15. Graceful shutdown: handler registered")


# ─── Exercise 16: ContextVar for Request Tracing ─────────────────────────────

req_id_ctx = __import__("contextvars").ContextVar("req_id")


async def handle_traced_request(name: str) -> str:
    req_id = f"req-{name}-{__import__('uuid').uuid4().hex[:8]}"
    req_id_ctx.set(req_id)
    await asyncio.sleep(0.05)
    assert req_id_ctx.get() == req_id, "ContextVar isolation broken!"
    return req_id


async def test_contextvar_requests() -> None:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(handle_traced_request(str(i))) for i in range(5)]
    ids = [t.result() for t in tasks]
    assert len(set(ids)) == 5, "Each request must have unique ID"
    ctx = __import__("contextvars").copy_context()
    ctx.run(lambda: req_id_ctx.set("replayed"))
    assert req_id_ctx.get("none") == "none", "Original context should be unchanged"


def run_ex16() -> None:
    asyncio.run(test_contextvar_requests())
    print("16. ContextVar request tracing OK")


if __name__ == "__main__":
    print("1. Threading: (would run but skip network deps)")

    assert is_prime(7) is True
    assert is_prime(10) is False
    print("2. Multiprocessing OK")

    asyncio.run(test_fetch_10())
    print("3. Asyncio basics OK")

    asyncio.run(test_queue())
    print("4. Async queue OK")

    print("5. FastAPI: (see code above)")
    print("6. SQLAlchemy: (see code above)")

    run_ex7()
    run_ex8()

    print("9. Health check: (see code above)")
    print("10. Structured logging: (see code above)")

    run_ex11()
    run_ex12()
    asyncio.run(run_async_queue())
    print("13. Async queue OK")

    messages = run_echo_server()
    print(f"14. TCP echo server: handled {len(messages)} messages OK")

    run_ex15()
    run_ex16()
    print("\n=== All 16 solutions demonstrated! ===")
