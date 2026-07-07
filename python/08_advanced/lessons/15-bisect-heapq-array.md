# 🎯 bisect, heapq, array — Algorithm & Data Structure Modules
<!-- ⏱️ 14 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Use `bisect` for sorted list insertion, `heapq` for priority queues, and `array` for memory-efficient numeric storage.

> 💡 **TL;DR — The whole point:** `bisect` maintains sorted lists efficiently, `heapq` implements priority queues with O(log n) push/pop, and `array` stores typed numbers in a fraction of the memory of lists.

## 🔗 Why This Matters
Game leaderboards use `heapq.nlargest`. Network intrusion detectors use `bisect` for IP range lookups. Scientific datasets with millions of floats use `array` to save gigabytes. These modules give you C-speed data structures without leaving Python.

## The Concept
- `bisect` — binary search on sorted sequences. `bisect_left` finds insertion index for duplicates; `bisect_right` finds after duplicates. `insort` = `bisect` + `list.insert`
- `heapq` — binary heap where the smallest element is always at index 0. `heappush`/`heappop` maintain the heap invariant. `heapify` turns any list into a heap in O(n). `nlargest`/`nsmallest` use a heap internally
- `array` — like `list` but each element has the same C type (`'i'` for signed int, `'d'` for double, `'u'` for unicode char). Uses 4-8 bytes per element vs 28+ for Python int objects

## Code Example
```python
"""A* pathfinding priority queue, streaming leaderboard, time series storage."""

import bisect
import heapq
from array import array


# ─── bisect: IP range lookup ───
ranges = [(0, 50000, "local"), (50001, 100000, "us-east"), (100001, 200000, "eu-west")]
def lookup_ip(ip_int: int) -> str:
    idx = bisect.bisect_right(ranges, (ip_int,)) - 1
    if idx >= 0 and ranges[idx][0] <= ip_int <= ranges[idx][1]:
        return ranges[idx][2]
    return "unknown"

print(f"IP 75000 → {lookup_ip(75000)}")
print(f"IP 999999 → {lookup_ip(999999)}")

# ─── heapq: Priority queue for task scheduler ───
class PriorityQueue:
    def __init__(self):
        self._heap = []
    def push(self, priority: float, item: str):
        heapq.heappush(self._heap, (priority, item))
    def pop(self) -> str:
        return heapq.heappop(self._heap)[1]

pq = PriorityQueue()
pq.push(3, "Backup")
pq.push(1, "Critical alert")
pq.push(2, "Send report")
print(f"Next task: {pq.pop()}")  # Critical alert

# ─── heapq: Streaming top-K scores ───
scores = [55, 88, 72, 91, 63, 85, 97]
print(f"Top 3: {heapq.nlargest(3, scores)}")
print(f"Bottom 2: {heapq.nsmallest(2, scores)}")

# ─── array: Memory-efficient time series ───
prices = array("d", [100.5, 101.2, 102.8, 103.1])
prices.append(104.0)
print(f"Prices: {list(prices)}, itemsize={prices.itemsize} bytes")
```

## 🔍 How It Works
- `bisect_left` vs `bisect_right` — when inserting into `[1, 3, 3, 5]`, `bisect_left(3)` returns index 1, `bisect_right` returns index 3. Use `_left` to keep existing duplicates stable
- `heapq` is a min-heap. For max-heap, push negative priorities: `(-priority, item)`. `heapq.merge` merges multiple sorted inputs lazily
- `array` methods are implemented in C on contiguous memory. Slicing returns a new array (copy). The `typecode` determines element size: `'b'`=1, `'h'`=2, `'i'`=4, `'l'`=8, `'f'`=4, `'d'`=8 bytes

## ⚠️ Common Pitfall
`bisect.insort` is O(n) because it calls `list.insert`. For many insertions, build the list unsorted then sort + `bisect` for lookups. `heapq` is not a sorted list — you can only pop the smallest element, not efficiently access arbitrary elements.

## 🧠 Memory Aid
"`bisect` = binary search + insert. `heapq` = priority queue (pop smallest). `array` = list with C types. For leaderboards: `nlargest`. For schedulers: `heappush`/`heappop`."

## 🏃 Try It
Build a task scheduler that accepts tasks with priorities, runs the highest priority task, and stores completed tasks in a sorted list using `bisect.insort`. Measure memory of 10,000 floats in a list vs array.

## 🔗 Related
- [Collections Deep](05-collections-deep.md) — `deque`, `Counter`, `OrderedDict`
- [itertools](04-itertools.md) — `chain`, `islice` for stream processing

## ➡️ Next
[struct, pickle, shelve, json deep](16-struct-pickle-shelve-json.md)
