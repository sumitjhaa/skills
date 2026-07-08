# Interactions

Playwright locators provide rich action methods that simulate real user interactions with automatic waiting built in.

## Key Concepts
- `locator.click()` — single left-click
- `locator.fill()` — clear and type text into an input
- `locator.select_option()` — choose an `<option>` from a `<select>` element
- `locator.check()` / `locator.uncheck()` — toggle checkbox/radio states
- `locator.dblclick()` — double-click for events like file-open

## Code Example

```python
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://example.com")

        # Click a link
        await page.locator("text=More information").click()

        # Fill a search field (hypothetical — adapt to real page)
        # await page.locator("#search").fill("Playwright")
        # Select an option from a dropdown
        # await page.locator("select#country").select_option("us")
        # Check a checkbox
        # await page.locator("#agree").check()
        # Double-click a row
        # await page.locator("tr.selected").dblclick()

        print("Interactions done.")
        await browser.close()


asyncio.run(main())
```

Run with: `python ../code/03-interactions.py`

## Key Takeaways
- `fill()` clears the field first — use `type()` if you need character-by-character typing.
- `select_option()` accepts value, label, or index.
- Check/uncheck throw if the element is not a checkbox or radio button.
