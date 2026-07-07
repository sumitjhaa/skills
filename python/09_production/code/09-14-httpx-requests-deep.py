"""HTTPX & Requests Deep — HTTP clients for e-commerce payment & shipping.
Run: python 09-14-httpx-requests-deep.py
"""

import asyncio
import time
from typing import Any
import httpx


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
                time.sleep(0.5 * (attempt + 1))
        return {}

    def close(self) -> None:
        self.client.close()


gateway = PaymentGatewayClient("https://api.stripe.example", "sk_test_123")
print("Payment client ready (simulated)")


class ShippingRateClient:
    def __init__(self):
        self.timeout = httpx.Timeout(15.0)

    async def get_rate(self, carrier: str, weight_kg: float) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            await asyncio.sleep(0.1)
            return {"carrier": carrier, "rate": round(weight_kg * 3.5, 2), "currency": "USD"}


async def compare_shipping_rates(weight_kg: float) -> list[dict]:
    client = ShippingRateClient()
    carriers = ["FedEx", "UPS", "DHL"]
    tasks = [client.get_rate(c, weight_kg) for c in carriers]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r for r in results if isinstance(r, dict) and "error" not in r]


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


async def main():
    print("\n=== Async shipping rate comparison ===")
    rates = await compare_shipping_rates(2.5)
    for r in rates:
        print(f"  {r['carrier']}: ${r['rate']}")


if __name__ == "__main__":
    asyncio.run(main())
