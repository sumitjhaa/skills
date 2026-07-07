# 🎯 HTTPX & Requests Deep
<!-- ⏱️ 16 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Use `httpx` for modern HTTP (sync/async, connection pooling, retries, timeouts) and deep-dive into `requests.Session`.

> 💡 **TL;DR — The whole point:** `httpx` is the modern replacement for `requests` — it supports async, HTTP/2, connection pooling, and has a cleaner API. `requests.Session` reuses connections efficiently.

## 🔗 Why This Matters
Every e-commerce app calls external APIs — payment gateways, shipping carriers, inventory providers. Proper HTTP clients with retry logic, timeouts, and connection pooling prevent production outages and performance bottlenecks.

## The Concept
- `httpx.Client()` — sync client with connection pooling
- `httpx.AsyncClient()` — async client for asyncio apps
- `retries` + `timeout` — production requirements
- `requests.Session()` — legacy but widely used
- Rate limiting — be a good API citizen

## Code Example
```python
"""E-commerce: HTTP client for payment gateway and shipping API."""

import asyncio
import time
from typing import Any

import httpx


# ─── Sync client with retries ───
class PaymentGatewayClient:
    def __init__(self, base_url: str, api_key: str):
        self.client = httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=httpx.Timeout(10.0, connect=5.0),
        )

    def charge(self, amount: float, currency: str = "USD") -> dict[str, Any]:
        for attempt in range(3):
            try:
                resp = self.client.post(
                    "/charges",
                    json={"amount": amount, "currency": currency},
                )
                resp.raise_for_status()
                return resp.json()
            except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
                if attempt == 2:
                    raise
                time.sleep(0.5 * (attempt + 1))  # exponential backoff
        return {}

    def close(self) -> None:
        self.client.close()


# Simulated usage
gateway = PaymentGatewayClient("https://api.stripe.example", "sk_test_123")
print("Payment client ready (simulated)")


# ─── Async client for concurrent requests ───
class ShippingRateClient:
    def __init__(self):
        self.timeout = httpx.Timeout(15.0)

    async def get_rate(self, carrier: str, weight_kg: float) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Simulated API call
            await asyncio.sleep(0.1)
            return {"carrier": carrier, "rate": round(weight_kg * 3.5, 2), "currency": "USD"}


async def compare_shipping_rates(weight_kg: float) -> list[dict]:
    client = ShippingRateClient()
    carriers = ["FedEx", "UPS", "DHL"]
    tasks = [client.get_rate(c, weight_kg) for c in carriers]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r for r in results if isinstance(r, dict) and "error" not in r]


# ─── requests.Session with connection pooling ───
def legacy_example():
    import requests
    session = requests.Session()
    session.headers.update({"User-Agent": "ecom-tools/0.1"})

    for product_id in range(5):
        resp = session.get(f"https://api.example.com/products/{product_id}", timeout=5)
        print(f"  Product {product_id}: {resp.status_code}")

    session.close()


# ─── Rate limiting ───
class RateLimitedClient:
    def __init__(self, calls_per_second: float = 10):
        self.client = httpx.Client()
        self.min_interval = 1.0 / calls_per_second
        self._last_call = 0.0

    def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        elapsed = time.perf_counter() - self._last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_call = time.perf_counter()
        return self.client.request(method, url, **kwargs)


# Run async example
async def main():
    print("\n=== Async shipping rate comparison ===")
    rates = await compare_shipping_rates(2.5)
    for r in rates:
        print(f"  {r['carrier']}: ${r['rate']}")


if __name__ == "__main__":
    asyncio.run(main())
```

## 🔍 How It Works
- `httpx.Client()` reuses TCP connections (connection pooling) — faster for multiple requests
- `httpx.Timeout(read=10.0, connect=5.0)` sets separate timeouts for each phase
- Exponential backoff: wait 0.5s, 1s, 2s between retries
- `async with httpx.AsyncClient()` for non-blocking HTTP in async apps
- `requests.Session()` also pools connections and persists cookies
- Rate limiting: sleep between requests to stay under API limits

## ⚠️ Common Pitfall
Not using `with` or `.close()` on clients. HTTP clients hold open connections. Always use `async with` for async clients or call `.close()` when done. Not closing leads to connection leaks.

## 🧠 Memory Aid
"httpx = requests + async + HTTP/2. `Client` = pooled connections. Retry + timeout = production. Rate limit = be polite."

## 🏃 Try It
Write an async function that fetches 5 product prices from `https://fakestoreapi.com/products` (or a mock). Use `httpx.AsyncClient` with `asyncio.gather`. Print the results with response times.

## 🔗 Related
- [Asyncio Deep](../10_ecosystem/lessons/05-asyncio-deep.md) — async/await basics
- [Concurrent Futures](../08_advanced/lessons/12-concurrent-futures.md) — parallel HTTP

## ➡️ Next
[Pytest Deep](15-pytest-deep.md)
