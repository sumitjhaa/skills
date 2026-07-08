# Visual Testing

Capture page screenshots and compare them pixel-by-pixel to detect unintended visual regressions.

## Key Concepts
- `page.screenshot()` — capture a full-page or element screenshot
- `locator.screenshot()` — capture only a specific element
- `expect(page).to_have_screenshot()` — built-in snapshot comparison
- `full_page=True` — capture the scrollable page, not just the viewport
- `mask=locators` — hide dynamic elements (dates, ads) during comparison

## Code Example

```python
import asyncio
from playwright.async_api import async_playwright, expect


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://example.com")

        # Full-page screenshot
        await page.screenshot(path="screenshots/full-page.png", full_page=True)

        # Element screenshot
        heading = page.locator("h1")
        await heading.screenshot(path="screenshots/heading.png")

        # Assert against a stored baseline
        # await expect(page).to_have_screenshot(
        #     "screenshots/baseline.png",
        #     max_diff_pixels=100,
        # )

        print("Screenshots captured.")
        await browser.close()


asyncio.run(main())
```

Run with: `python ../code/11-visual-testing.py`

## Key Takeaways
- Store baseline screenshots in version control and review PR diffs carefully.
- Use `max_diff_pixels` or `max_diff_ratio` to allow minor anti-aliasing differences.
- Mask dynamic regions with `page.screenshot(mask=[locator])` to avoid false positives.
