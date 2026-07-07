# 🏋️ Practice Exercises — Phase 10: Python Ecosystem

## Exercise 1: Threading (🟢)
Write a script that downloads 5 URLs concurrently using `threading.Thread`. Use a list to collect results. Print the total time taken. Compare with sequential execution.

## Exercise 2: Multiprocessing (🟡)
Write a function `is_prime(n: int) -> bool`. Use `multiprocessing.Pool(4)` to check which numbers from 1 to 100,000 are prime. Time it and compare with a single-threaded version.

## Exercise 3: Asyncio Basics (🟡)
Write an async function `fetch_post(id: int)` that simulates an API call with `asyncio.sleep(0.2)` and returns `{"id": id, "title": f"Post {id}"}`. Use `asyncio.gather` to fetch 10 posts concurrently. Print results.

## Exercise 4: Async Queue (🔴)
Implement a producer/consumer pattern with `asyncio.Queue`. The producer generates 20 numbers (one per 0.05s). Two consumers each square numbers and print them. Use `TaskGroup`.

## Exercise 5: FastAPI Endpoint (🟡)
Create a FastAPI endpoint `GET /search?q=python&limit=5` that returns a list of simulated search results (list of dicts with `title`, `url`, `score`). Add a `Depends` for API key validation.

## Exercise 6: SQLAlchemy Models (🔴)
Define `Author` (id, name) and `Book` (id, title, year, author_id) models with a relationship. Write a query that fetches all authors with their books eagerly loaded. Print author name + book titles.

## Exercise 7: Pandas Groupby (🟡)
Load this data into a DataFrame and compute: total sales per region, average quantity per product, and the top 3 products by revenue.
```python
data = [
    {"region": "NA", "product": "Widget", "qty": 10, "price": 9.99},
    {"region": "EU", "product": "Widget", "qty": 5, "price": 9.99},
    {"region": "NA", "product": "Gadget", "qty": 3, "price": 49.99},
    {"region": "APAC", "product": "Widget", "qty": 8, "price": 9.99},
    {"region": "EU", "product": "Gadget", "qty": 2, "price": 49.99},
]
```

## Exercise 8: NumPy Broadcasting (🟡)
Create a 4×3 array of product prices (4 stores, 3 products). Create a 1×3 array of discounts. Use broadcasting to compute discounted prices. Then use `np.where` to flag products under $10.

## Exercise 9: Health Check (🔴)
Write a FastAPI `/health` endpoint that checks if a SQLite database file exists (path from env var `DB_PATH`) and if a simulated Redis ping succeeds (random 90% success). Return 200 or 503 with details.

## Exercise 10: Structured Logging (🔴)
Create a FastAPI middleware that logs every request as a JSON object with: timestamp, method, path, status_code, duration_ms, and a unique request_id (use `uuid.uuid4()`). Include an endpoint `/error` that raises an exception and logs the error.

---

## New Advanced Concurrency & Networking Exercises

## Exercise 11: Thread-safe Counter with Lock (🟡)
Use `threading.Thread` (8 threads) to increment a shared counter 10,000 times each. Use `threading.Lock` to protect the counter. Print the final value (should be 80,000). Then try without the lock to show the race condition.

## Exercise 12: ProcessPoolExecutor for CPU-bound Tasks (🟡)
Write a function `sum_squares(n: int) -> int` that sums squares from 1 to n. Use `concurrent.futures.ProcessPoolExecutor` to process `[10**6, 2*10**6, 3*10**6, 4*10**6]` in parallel. Time it and compare with `ThreadPoolExecutor` to demonstrate the GIL difference.

## Exercise 13: Async Producer-Consumer with Queue (🔴)
Use `asyncio.Queue` with `maxsize=5`. A producer coroutine generates 30 messages (one per 0.02s). Three consumer coroutines each process messages (simulate with `asyncio.sleep(0.05)`) and print the consumer name + message. Use `TaskGroup` for structured concurrency.

## Exercise 14: Simple TCP Echo Server (🔴)
Write a single-threaded TCP echo server using `socket` and `selectors`. Listen on `127.0.0.1:8888`. The server should handle up to 10 connections non-blockingly, echoing back any data received. Write a client that sends "hello" and prints the response.

## Exercise 15: Graceful Shutdown with Signal Handlers (🔴)
Write a script that registers `SIGTERM` and `SIGINT` handlers. On receiving either signal, print "Shutting down gracefully...", set a global `shutdown_requested = True` flag, and exit cleanly. Also register an `atexit` handler that prints "Cleanup complete." Test by running and pressing Ctrl+C.

## Exercise 16: ContextVar for Request Tracing (🔴)
Define a `ContextVar` for `request_id`. Write an async function `handle_request(name: str)` that sets `request_id` to a unique value, simulates work with `asyncio.sleep(0.1)`, and prints the request_id. Run 5 concurrent requests and verify each has its own request_id. Then use `copy_context()` to snapshot and replay a context.

---

## New Introductory Exercises

## Exercise 17: Concurrency Model Comparison (🟢)
Write a script that benchmarks three concurrency approaches for downloading 12 simulated posts (each takes `time.sleep(0.1)`):
1. **Sequential** — loop and call `download_post()` one by one
2. **Threading** — `threading.Thread` with a `threading.Lock` to collect results
3. **Multiprocessing** — `multiprocessing.Pool(4)` with `pool.map()`

Print the elapsed time for each approach and explain which wins for I/O-bound vs CPU-bound work. Include a CPU-bound function `count_words` that processes a large document using `Pool`.

## Exercise 18: REST API Client with urllib (🟢)
Using only the standard library (`urllib.request`), write functions to:
- `GET /posts` — fetch all posts from `https://jsonplaceholder.typicode.com/posts`
- `GET /posts/{id}` — fetch a single post
- `POST /posts` — create a new post with `title`, `body`, `userId` (send as JSON)
- `GET /posts/{id}/comments` — fetch comments for a post (query param `?postId=1`)

Print the number of posts fetched, the title of post 1, and the confirmation of a created post. Handle HTTP errors by checking status codes. Then re-implement the same functionality using `requests.Session()` to show connection pooling.

## Exercise 19: Data Science Pipeline — Social Media Analytics (🟡)
Build a data pipeline using SQLite, NumPy, Pandas, and Matplotlib:

1. **SQLite** — create a `posts` table (id, user_id, content, likes, shares, created_at) and insert 8 sample posts
2. **NumPy** — compute mean, median, max, and min of likes and shares
3. **Pandas** — load the table into a DataFrame, filter posts with likes > 100, group by user_id to find average likes per user
4. **Matplotlib** — plot a bar chart of total shares per user_id and save it as `shares_per_user.png`

All SQL queries must use `?` placeholders (no f-string injection). Use vectorized operations instead of loops.

## Exercise 20: Async Context Manager & Iterator (🔴)
Implement an async context manager `AsyncDBConnection` that simulates connecting to a database:
- `__aenter__` prints "Connecting to {db_name}..." and sleeps 0.05s
- `__aexit__` prints "Closing {db_name}..." and sleeps 0.02s
- `query(sql)` sleeps 0.1s and returns `[{"result": "ok"}]`

Then implement an async iterator `PaginatedAPI` that yields batches of items across pages:
- Initialize with `total_pages` (default 5) and `page_size` (default 3)
- Each page yield returns a list of f"item_{page}_{i}" strings
- Raises `StopAsyncIteration` after the last page

Finally, use `asyncio.TaskGroup` with a producer/consumer pattern using `asyncio.Queue(maxsize=5)` to process 15 items, and wrap a slow coroutine with `asyncio.timeout(0.3)` to demonstrate timeout handling.

---

## Phase 10 Extensions — New Lessons 15–16

## Exercise 21: Web Scraper for Product Listings (🟡)
Write a function `scrape_products(html: str) -> list[dict]` that uses `BeautifulSoup` to parse a product listing page. Extract:
- Product name (from `h2.product-name` tags)
- Price (from `span.price` tags, strip `$` and convert to float)
- Rating (from `div.rating` tags, extract data-rating attribute)

```python
html = """<div class="product"><h2 class="product-name">Widget</h2>
<span class="price">$19.99</span><div class="rating" data-rating="4.5"></div></div>
<div class="product"><h2 class="product-name">Gadget</h2>
<span class="price">$29.99</span><div class="rating" data-rating="3.8"></div></div>"""
products = scrape_products(html)
# Should return: [{"name": "Widget", "price": 19.99, "rating": 4.5}, ...]
```

## Exercise 22: MongoDB Product Catalog CRUD (🔴)
Write a class `ProductCatalog` that wraps a MongoDB collection with methods:
- `add_product(name, category, price, stock)` — inserts a new product and returns the `ObjectId`
- `find_by_category(category)` — returns all products in a category, sorted by price ascending
- `apply_discount(category, percent)` — uses `update_many` with `$mul` to apply a percentage discount
- `top_products(limit=5)` — uses aggregation pipeline with `$sort` by price descending and `$limit`

Implement both a real-PyMongo version and a mock fallback using in-memory dicts, so the test is runnable without a MongoDB server.

```python
catalog = ProductCatalog()  # Uses mock by default
pid = catalog.add_product("Widget", "Electronics", 19.99, 100)
assert len(catalog.find_by_category("Electronics")) >= 1
catalog.apply_discount("Electronics", 10)  # 10% off
```
