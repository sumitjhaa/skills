# Frames & Windows

Modern pages embed `<iframe>` elements and open pop-up windows. Playwright provides first-class APIs for both scenarios.

## Key Concepts
- `page.frame_locator()` — locate elements inside an iframe
- `page.frames` — list of all frames on the page
- `page.context.on("page")` — listen for new tab/popup events
- `context.new_page()` — programmatically open a new tab
- Popups are automatically handled as `Page` objects

## Code Example

```python
import asyncio
from playwright.async_api import async_playwright, expect


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://example.com")

        # Listen for popup windows
        async with context.expect_page() as popup_info:
            await page.locator("text=More information").click()
        popup = await popup_info.value
        print(f"Popup URL: {popup.url}")

        # Working with iframes (example — adapt selector & frame)
        # frame = page.frame_locator("#my-iframe")
        # await frame.locator("button").click()

        await browser.close()


asyncio.run(main())
```

Run with: `python ../code/06-frames-windows.py`

## Key Takeaways
- Use `frame_locator()` to scope locators inside an iframe — actions auto-wait as usual.
- `context.expect_page()` captures popups opened by user actions.
- Always close extra pages to keep test state predictable.
