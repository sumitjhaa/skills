"""Concurrency Introduction — threading, multiprocessing, subprocess.
Run: python 10-01-concurrency-intro.py
"""

import threading
import time
from multiprocessing import Pool
from typing import Any

posts_to_download = [f"post_{i}" for i in range(8)]


def download_post(post_id: str) -> dict[str, Any]:
    time.sleep(0.1)
    return {"id": post_id, "likes": 42, "shares": 7}


def threaded_download() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    lock = threading.Lock()

    def worker(post: str) -> None:
        post_data = download_post(post)
        with lock:
            results.append(post_data)

    threads = [threading.Thread(target=worker, args=(p,)) for p in posts_to_download]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return results


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
elapsed = time.perf_counter() - start
print(f"Threaded download: {len(results)} posts in {elapsed:.3f}s")
