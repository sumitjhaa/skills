# API Testing

Playwright's `request` context lets you send HTTP requests directly from tests, enabling API-level assertions without a browser.

## Key Concepts
- `playwright.request.new_context()` — create an API request context (no browser needed)
- `context.get()`, `context.post()`, `context.put()`, `context.delete()` — HTTP methods
- `response.status`, `response.ok`, `response.json()` — assertion helpers
- Reuse storage state from a browser context to authenticate API calls
- Combine API testing with UI testing for end-to-end coverage

## Code Example

```python
import asyncio
from playwright.async_api import async_playwright, expect


async def main():
    async with async_playwright() as p:
        # Create a request context (independent of any browser)
        request_context = await p.request.new_context()

        # GET
        resp = await request_context.get("https://jsonplaceholder.typicode.com/posts/1")
        assert resp.status == 200
        data = await resp.json()
        print(f"GET: {data['title']}")

        # POST
        resp = await request_context.post(
            "https://jsonplaceholder.typicode.com/posts",
            data={"title": "foo", "body": "bar", "userId": 1},
        )
        assert resp.ok
        print(f"POST status: {resp.status}")

        # PUT
        resp = await request_context.put(
            "https://jsonplaceholder.typicode.com/posts/1",
            data={"title": "updated"},
        )
        assert resp.ok

        # DELETE
        resp = await request_context.delete(
            "https://jsonplaceholder.typicode.com/posts/1"
        )
        assert resp.ok

        print("All API assertions passed.")
        await request_context.dispose()


asyncio.run(main())
```

Run with: `python ../code/13-api-testing.py`

## Key Takeaways
- Use `request.new_context(base_url="...")` to avoid repeating the host.
- API request contexts are lightweight and don't launch a browser.
- Dispose of the request context when done to free connections.
