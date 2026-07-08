# Lesson 05.53: Streaming Algorithms

## Learning Objectives
- Understand data stream processing constraints
- Implement reservoir sampling for stream sampling
- Apply Count-Min Sketch for frequency estimation
- Design Bloom filters for membership testing
- Estimate cardinality with HyperLogLog

## Challenge
Process data in one pass with $O(\log n)$ or $O(1)$ memory:
- Cannot store all data
- Cannot revisit past data
- Must process at line rate

## Reservoir Sampling
Sample $k$ items uniformly from stream of unknown length $n$:

```
for i = 1 to k:
    reservoir[i] = stream[i]
for i = k+1 to n:
    j = random(1, i)
    if j <= k:
        reservoir[j] = stream[i]
```

**Proof**: Each item has probability $k/n$ of being in the reservoir.

**Weighted reservoir sampling**: Use weight $w_i$, accept with probability $w_i / \sum w_j$.

## Count-Min Sketch
Approximate frequency query with error $\varepsilon$ and confidence $\delta$:

- $d = \lceil \log(1/\delta) \rceil$ hash functions $h_1, \dots, h_d$
- $w = \lceil e/\varepsilon \rceil$ counters per hash function

**Update**: For each hash $h_j$, increment $\text{count}[j][h_j(x)]$.

**Query**: $\hat{f}_x = \min_j \text{count}[j][h_j(x)]$.

**Guarantee**: $f_x \leq \hat{f}_x \leq f_x + \varepsilon N$ with probability $\geq 1 - \delta$.

## Bloom Filter
Set membership test with false positives (no false negatives):

- $k$ hash functions, $m$-bit array (initially all 0)
- **Insert**: Set bits $h_1(x), \dots, h_k(x)$ to 1
- **Query**: Check all $k$ bits are 1

**Optimal**: $k = (m/n) \ln 2$ for $n$ items.

**False positive rate**: $\left(1 - e^{-kn/m}\right)^k$

## HyperLogLog
Cardinality estimation using $O(\log \log n)$ memory:

1. Split stream into $m = 2^b$ buckets via first $b$ bits of hash
2. For each item: find bucket, count leading zeros in remaining hash bits
3. Estimate: $\hat{n} = \alpha_m \cdot m^2 \cdot \left(\sum_{j=1}^m 2^{-M_j}\right)^{-1}$

**Error**: $\approx 1.04 / \sqrt{m}$ (standard error $2\%$ for $m=2048$)

## Heavy Hitters (Frequent Algorithm)
Find items exceeding $\phi n$ frequency (e.g., $\phi = 0.01$):

**Misra-Gries**:
```
k = floor(1/phi)
counters = {}
for x in stream:
    if x in counters:
        counters[x] += 1
    elif len(counters) < k - 1:
        counters[x] = 1
    else:
        for key in counters:
            counters[key] -= 1
            if counters[key] == 0:
                del counters[key]
```

Final counters are heavy hitters (may include some false positives).

**Space-Saving**: Better tracking with min-heap for minimum count.

## Code: Count-Min Sketch

```python
import numpy as np
from hashlib import md5

class CountMinSketch:
    def __init__(self, eps=0.01, delta=0.05):
        self.w = int(np.ceil(np.exp(1) / eps))
        self.d = int(np.ceil(np.log(1 / delta)))
        self.counts = np.zeros((self.d, self.w), dtype=int)

    def _hash(self, item, i):
        return int(md5(f"{i}_{item}".encode()).hexdigest(), 16) % self.w

    def add(self, item, count=1):
        for i in range(self.d):
            self.counts[i, self._hash(item, i)] += count

    def query(self, item):
        return min(self.counts[i, self._hash(item, i)] for i in range(self.d))
```

## Practical Considerations
- **Choosing $\varepsilon, \delta$**: CMS needs 10-100x less memory than exact counting
- **Hash functions**: Use universal hashing (MurmurHash, xxHash)
- **Stream order**: Deterministic algorithms (not randomized) may be vulnerable to adversarial streams
- **Mergeability**: CMS and HyperLogLog can be merged across distributed workers
- **Count-Min vs Count-Sketch**: Count-Sketch uses signed counts, unbiased estimates, higher variance
- **Deletions**: CMS (and Count-Sketch) support deletions (subtract from counters)

## Applications
- **Network traffic monitoring**: Heavy hitter detection, flow cardinality
- **Web analytics**: Unique visitors (HyperLogLog), popular pages (CMS)
- **Database optimization**: Approximate query processing (AQUA project)
- **NLP**: Word frequency statistics for large corpora
- **Sensor networks**: IoT data summarization
- **Fraud detection**: IP address frequency monitoring

## References
- Vitter, "Random Sampling with a Reservoir" (ACM Trans. Math. Software, 1985)
- Cormode & Muthukrishnan, "An Improved Data Stream Summary: The Count-Min Sketch and its Applications" (J. Algorithms, 2005)
- Bloom, "Space/Time Trade-offs in Hash Coding with Allowable Errors" (CACM, 1970)
- Flajolet et al., "HyperLogLog: The Analysis of a Near-Optimal Cardinality Estimation Algorithm" (Discrete Math., 2007)
- Misra & Gries, "Finding Repeated Elements" (Science of Computer Programming, 1982)
- Cormode & Hadjieleftheriou, "Methods for Finding Frequent Items in Data Streams" (VLDB J., 2010)
