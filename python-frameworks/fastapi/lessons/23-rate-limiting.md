# 🚦 Rate Limiting
<!-- ⏱️ 10 min | 🟢 Supplement -->

**What You'll Learn:** Token bucket, sliding window, per-IP/user limits, burst handling.

## Token Bucket

```python
import time

class TokenBucket:
    def __init__(self, rate: float, burst: int):
        self.rate = rate       # tokens per second
        self.burst = burst     # max tokens
        self.tokens = burst
        self.last = time.time()

    def consume(self) -> bool:
        now = time.time()
        self.tokens = min(self.burst, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

<!-- Buckets refill over time. `rate=5, burst=10` = up to 10 immediate requests, then 5/sec. -->

## Sliding Window

Count requests in a rolling time window:

```python
from collections import deque

class SlidingWindow:
    def __init__(self, max_req: int, window: int = 60):
        self.max = max_req
        self.window = window
        self.timestamps: deque[float] = deque()

    def allow(self) -> bool:
        now = time.time()
        while self.timestamps and self.timestamps[0] < now - self.window:
            self.timestamps.popleft()
        if len(self.timestamps) < self.max:
            self.timestamps.append(now)
            return True
        return False
```

## Per-IP vs Per-User

| Key | Granularity | Example |
|-----|-------------|---------|
| `ip:{client_ip}` | Anonymous users | `ip:10.0.0.1` |
| `user:{user_id}` | Authenticated users | `user:42` |
| `endpoint:{path}` | Per-endpoint | `endpoint:/login` |

## Response Headers

```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 3
X-RateLimit-Reset: 1623456789
```

## Run the Code

```bash
python code/23-rate-limiting.py
```
