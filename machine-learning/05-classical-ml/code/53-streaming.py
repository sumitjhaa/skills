"""Streaming Algorithms (Reservoir sampling, Bloom filter, Count-Min Sketch) from scratch."""
import numpy as np

class ReservoirSampling:
    def __init__(self, k):
        self.k = k
        self.sample = []
        self.n = 0

    def process(self, x):
        self.n += 1
        if len(self.sample) < self.k:
            self.sample.append(x)
        else:
            j = np.random.randint(self.n)
            if j < self.k:
                self.sample[j] = x

    def get_sample(self):
        return np.array(self.sample)

class BloomFilter:
    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.bits = np.zeros(m, dtype=bool)

    def _hashes(self, item):
        h = []
        x = hash(str(item))
        for i in range(self.k):
            x = (x * 0x9e3779b97f4a7c15 + i) & 0xFFFFFFFFFFFFFFFF
            h.append(x % self.m)
        return h

    def add(self, item):
        for h in self._hashes(item):
            self.bits[h] = True

    def __contains__(self, item):
        return all(self.bits[h] for h in self._hashes(item))

class CountMinSketch:
    def __init__(self, width=1000, depth=5):
        self.width = width
        self.depth = depth
        self.counts = np.zeros((depth, width), dtype=int)
        self.seeds = np.random.randint(0, 2**31, depth)

    def _hash(self, item, d):
        return (hash(str(item)) ^ self.seeds[d]) % self.width

    def add(self, item, count=1):
        for d in range(self.depth):
            self.counts[d, self._hash(item, d)] += count

    def query(self, item):
        return min(self.counts[d, self._hash(item, d)] for d in range(self.depth))

if __name__ == "__main__":
    rs = ReservoirSampling(k=10)
    for i in range(1000):
        rs.process(i)
    print(f"Reservoir sample (10 from 1000): {sorted(rs.get_sample()[:5])}...")

    bf = BloomFilter(m=100, k=3)
    for i in range(20):
        bf.add(i)
    print(f"Bloom filter: 15 in set? {15 in bf}  (true)")
    print(f"Bloom filter: 99 in set? {99 in bf} (may be false positive)")

    cms = CountMinSketch(width=100, depth=5)
    for i in range(100):
        for _ in range(np.random.randint(1, 10)):
            cms.add(f"item_{i}")
    print(f"Count-Min Sketch: item_5 count ≈ {cms.query('item_5')}")
