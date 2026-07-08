# Waiting Strategies

Playwright auto-waits for elements to be actionable, but explicit waits give you fine-grained control over page timing.

## Key Concepts
- `page.wait_for_selector()` — wait for an element to appear in the DOM
- `page.wait_for_load_state()` — wait for network events like `networkidle`
- `page.wait_for_url()` — block until the URL matches a pattern
- `page.wait_for_function()` — wait for a JavaScript expression to return truthy
- Auto-waiting: locator actions (click, fill, etc.) automatically wait for visibility, stability, and enabled state

## Code Example

```python
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://example.com")

        # Explicitly wait for the heading to appear
        heading = page.locator("h1")
        await heading.wait_for(state="visible", timeout=5000)

        # Wait until the page has no open network connections for 500ms
        await page.wait_for_load_state("networkidle")

        # Wait for the URL to change (helpful after navigation)
        # await page.wait_for_url("**/some-page")

        print(f"Heading visible: {await heading.is_visible()}")
        await browser.close()


asyncio.run(main())
```

Run with: `python ../code/04-waiting-strategies.py`

## Key Takeaways
- Prefer auto-waiting locators over manual waits — they reduce flakiness.
- Use `wait_for_load_state("networkidle")` sparingly; it can slow tests.
- Always set explicit timeouts to avoid indefinite blocking.
