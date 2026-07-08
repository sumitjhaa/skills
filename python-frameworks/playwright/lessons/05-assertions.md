# Assertions

Playwright's `expect()` API provides async matchers that retry until the condition is met or a timeout expires.

## Key Concepts
- `expect(locator).to_be_visible()` — element is visible on the page
- `expect(locator).to_have_text()` — exact or regex text match
- `expect(page).to_have_url()` — page URL matches a string or regex
- `expect(locator).to_have_count()` — number of matching elements
- All assertions retry automatically (default 5 s, configurable via `timeout`)

## Code Example

```python
import asyncio
from playwright.async_api import async_playwright, expect


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://example.com")

        # Assert element is visible
        heading = page.locator("h1")
        await expect(heading).to_be_visible()

        # Assert exact text
        await expect(heading).to_have_text("Example Domain")

        # Assert the URL
        await expect(page).to_have_url("https://example.com/")

        # Assert element has attribute
        link = page.locator("a")
        await expect(link).to_have_attribute("href", "https://www.iana.org/domains/example")

        print("All assertions passed.")
        await browser.close()


asyncio.run(main())
```

Run with: `python ../code/05-assertions.py`

## Key Takeaways
- `expect()` failures include a detailed diff — great for debugging.
- Prefer `to_have_text` with regex over fragile exact-match strings.
- Assertions are async and must be awaited.
