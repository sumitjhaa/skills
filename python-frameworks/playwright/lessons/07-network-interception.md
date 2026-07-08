# Network Interception

Intercept and modify network requests with `page.route()` — useful for mocking APIs, blocking resources, or simulating failures.

## Key Concepts
- `page.route(pattern, handler)` — intercept requests matching a URL glob
- `route.abort()` — block a request (e.g. images, analytics)
- `route.fulfill()` — respond with a custom payload (mock)
- `route.continue_()` — let the request proceed unchanged
- Routes apply to the page and all child frames

## Code Example

```python
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Block all image requests
        await page.route("**/*.{png,jpg,jpeg,gif,svg}", lambda route: route.abort())

        # Mock an API response
        async def mock_api(route):
            await route.fulfill(
                status=200,
                content_type="application/json",
                body='{"message": "mocked"}',
            )
        await page.route("**/api/data", mock_api)

        await page.goto("https://example.com")
        print("Network interception active — images blocked, API mocked.")
        await browser.close()


asyncio.run(main())
```

Run with: `python ../code/07-network-interception.py`

## Key Takeaways
- `route.abort()` is great for blocking third-party scripts and speeding tests.
- `route.fulfill()` lets you test error responses and edge cases.
- Use `route.continue_()` with overrides to modify headers or post data mid-flight.
