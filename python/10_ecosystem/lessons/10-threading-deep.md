# 🧵 Threading Deep Dive
<!-- ⏱️ 25 min read | 🔴 Mastery | 🧠 Applied -->

**What You'll Learn:** Every `threading` primitive — Thread, Lock, RLock, Semaphore, Event, Condition, Barrier, Timer, local — plus GIL semantics and thread-safety patterns.

> 💡 **TL;DR — The whole point:** `threading` is for I/O-bound concurrency. The GIL lets threads share memory but only one runs bytecode at a time. Use Locks to protect shared data, Events to signal, Queues to hand off work, and `threading.local()` for per-thread state.

## 🔗 Why This Matters
Web scrapers, DB connection pools, background workers, and GUI apps all need threads. Knowing `Lock` vs `RLock`, when to use `Semaphore`, and how to avoid deadlocks separates production code from toy scripts.

## The Concept

| Primitive | Job |
|-----------|-----|
| `Thread` | spawn + manage threads |
| `Lock` | mutual exclusion (non-reentrant) |
| `RLock` | reentrant lock (same thread can re-acquire) |
| `Semaphore` | limit concurrent access to N resources |
| `BoundedSemaphore` | Semaphore that can't be released too many times |
| `Event` | one-shot signaling (wait/set/clear) |
| `Condition` | wait/notify for producer-consumer |
| `Barrier` | N threads meet at a rendezvous point |
| `Timer` | call a function after a delay |
| `local()` | thread-local storage |

**GIL:** Only one thread holds the GIL at a time. Threads *release* the GIL during I/O (network, disk, sleep), which is why threading speeds up I/O-bound work. For CPU-bound work, use `multiprocessing`.

**Daemon threads:** automatically killed when all non-daemon threads exit. Good for background monitoring.

## Code Example

```python
"""Threading primitives in action — web scraper with rate limiting."""
import threading
import time
import random
from queue import Queue

# ── Semaphore: limit to 3 concurrent downloads ──
rate_limiter = threading.Semaphore(3)

def download(url: str) -> str:
    with rate_limiter:
        time.sleep(random.uniform(0.1, 0.3))
        return f"OK: {url}"

# ── Event: signal all threads to stop ──
stop_event = threading.Event()

def worker(q: Queue) -> None:
    while not stop_event.is_set():
        try:
            url = q.get(timeout=0.5)
            result = download(url)
            print(result)
            q.task_done()
        except Exception:
            pass

q: Queue[str] = Queue()
for url in [f"https://site.com/page/{i}" for i in range(10)]:
    q.put(url)

threads = [threading.Thread(target=worker, args=(q,), daemon=True) for _ in range(4)]
for t in threads:
    t.start()

q.join()
stop_event.set()
print(f"Active threads: {threading.active_count()}")
```

## 🔍 How It Works
- `Thread(target=fn, args=(x,), daemon=True)` — create; `.start()` begins execution; `.join()` blocks until done
- `Lock` — `with lock:` enters; another thread trying to `acquire()` blocks until released
- `RLock` — same thread can call `acquire()` multiple times (e.g. recursive function)
- `Semaphore(N)` — `acquire()` decrements; if 0, blocks until someone `release()`s
- `Event` — `wait()` blocks until `set()` is called; `clear()` resets; `is_set()` checks state
- `Condition` — `wait()` releases lock and blocks; `notify()` wakes one waiter; `notify_all()` wakes all
- `Barrier(N)` — each thread calls `wait()`; all N block until the Nth arrives, then all proceed
- `Timer(interval, fn)` — starts a thread that calls `fn` after `interval` seconds; `.cancel()` to abort
- `threading.local()` — attribute namespace unique to each thread (like Flask's `g`)

## ⚠️ Common Pitfall
**Deadlock:** Thread A holds Lock1 and waits for Lock2; Thread B holds Lock2 and waits for Lock1. Fix: always acquire locks in the same order. Use `threading.TIMEOUT_MAX` with `acquire(timeout=...)` for deadlock detection.

**GIL confusion:** Threading 8 CPU-bound workers is NOT 8× faster — it's ~1× (plus context-switch overhead). Only `multiprocessing` or NumPy/C-extensions bypass the GIL.

## 🧠 Memory Aid
"Lock = bathroom key (one person). RLock = same person can re-enter. Semaphore = parking lot with N spaces. Event = starting pistol. Condition = meeting room (wait until everyone's ready). Barrier = group photo (wait until all arrive)."

## 🏃 Try It
Write a web scraper that downloads 20 URLs but limits concurrency to 5 with `Semaphore`. Use `threading.local()` to store a per-thread HTTP session.

## 🔗 Related
- [Multiprocessing Deep](11-multiprocessing-deep.md) — CPU-bound parallel work
- [Asyncio Primitives Deep](12-asyncio-primitives-deep.md) — async equivalents
- [Concurrency Intro](01-concurrency-intro.md) — choosing the right model

## ➡️ Next
[Multiprocessing Deep](11-multiprocessing-deep.md)
