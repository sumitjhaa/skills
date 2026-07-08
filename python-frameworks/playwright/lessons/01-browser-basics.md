# Browser Basics

Launch a Chromium browser instance, open a new page, navigate to a URL, take a screenshot, and cleanly close the browser.

## Key Concepts
- `playwright.chromium.launch()` to start a browser instance
- `browser.new_page()` to create a fresh page tab
- `page.goto()` to navigate to a URL
- `page.screenshot()` to capture a visible snapshot
- `browser.close()` to release system resources

## Code Example

```python
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://example.com")
        await page.screenshot(path="example.png")
        print(f"Title: {await page.title()}")
        await browser.close()


asyncio.run(main())
```

Run with: `python ../code/01-browser-basics.py`

## Key Takeaways
- Always use async context managers (`async with`) to handle Playwright's lifecycle.
- The headless flag controls whether you see the browser window.
- Screenshots render the full page viewport by default.
