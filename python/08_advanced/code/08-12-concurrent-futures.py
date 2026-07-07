"""08-12-concurrent-futures.py — ThreadPoolExecutor, ProcessPoolExecutor."""

from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import math


def fetch_product_price(product_id: int) -> dict:
    time.sleep(0.2)
    return {"id": product_id, "price": round(10 + product_id * 1.5, 2)}


def batch_fetch_prices(product_ids: list[int]) -> list[dict]:
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_product_price, pid): pid for pid in product_ids}
        results = []
        for future in as_completed(futures):
            pid = futures[future]
            try:
                result = future.result()
                results.append(result)
                print(f"  [Done] Product {pid}: ${result['price']}")
            except Exception as e:
                print(f"  [Error] Product {pid}: {e}")
        return results


def compute_discount_matrix(prices: list[float]) -> list[list[float]]:
    N = len(prices)
    matrix = [[0.0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            matrix[i][j] = round(prices[i] * prices[j] * 0.01, 2)
    return matrix


def parallel_discount_matrix(prices: list[float]) -> list[list[float]]:
    chunk_size = math.ceil(len(prices) / 4)
    chunks = [prices[i:i + chunk_size] for i in range(0, len(prices), chunk_size)]
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(compute_discount_matrix, chunk) for chunk in chunks]
        results = [f.result() for f in futures]
    merged = []
    for chunk_result in results:
        merged.extend(chunk_result)
    return merged


def apply_coupon(price: float) -> float:
    time.sleep(0.05)
    return round(price * 0.9, 2)


if __name__ == "__main__":
    print("=== Fetching prices (I/O-bound) ===")
    start = time.perf_counter()
    prices_data = batch_fetch_prices(list(range(1, 11)))
    seq_time = time.perf_counter() - start
    print(f"Took {seq_time:.2f}s (sequential would be ~{len(prices_data) * 0.2:.1f}s)")

    print("\n=== Coupons (ThreadPoolExecutor.map) ===")
    prices = [p["price"] for p in prices_data]
    with ThreadPoolExecutor(max_workers=5) as executor:
        discounted = list(executor.map(apply_coupon, prices))
    print(f"Discounted: {[f'${p:.2f}' for p in discounted[:5]]}...")
