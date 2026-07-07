"""08-15-bisect-heapq-array.py — A* pathfinding priority queue, leaderboard, numeric storage."""

import bisect
import heapq
from array import array


def maintain_sorted_list():
    scores = [10, 30, 50]
    bisect.insort(scores, 40)
    bisect.insort(scores, 20)
    assert scores == [10, 20, 30, 40, 50]
    idx = bisect.bisect_left(scores, 35)
    print(f"Sorted scores: {scores}, insert 35 at index {idx}")
    return scores


class PriorityQueue:
    def __init__(self):
        self._heap = []

    def push(self, priority: float, item: str):
        heapq.heappush(self._heap, (priority, item))

    def pop(self) -> str:
        return heapq.heappop(self._heap)[1]

    def __bool__(self):
        return bool(self._heap)


def astar_pathfinding():
    pq = PriorityQueue()
    pq.push(3, "Start → A → Goal")
    pq.push(2, "Start → B → Goal")
    pq.push(1, "Start → C → Goal")
    path = pq.pop()
    print(f"A* chose: {path}")
    return path


def streaming_top_k(scores, k=3):
    return heapq.nlargest(k, scores)


def numeric_array_storage():
    arr = array("d", [1.5, 2.5, 3.5])
    arr.append(4.5)
    print(f"Array: {list(arr)}, itemsize={arr.itemsize}, typecode={arr.typecode}")
    return arr


if __name__ == "__main__":
    maintain_sorted_list()
    astar_pathfinding()
    print(f"Top scores: {streaming_top_k([55, 88, 72, 91, 63, 85])}")
    numeric_array_storage()
