# Locators & Selectors

Locators are Playwright's auto-waiting, resilient way to find elements on a page. They support CSS, text, and XPath strategies.

## Key Concepts
- `page.locator(selector)` returns a Locator object that can perform actions
- CSS selectors: `button`, `#submit`, `.btn`, `[data-testid="login"]`
- Text selectors: `text="Sign Up"`, `text=Sign Up`
- XPath selectors: `//button[@type="submit"]`
- Locators are lazy — they don't query the DOM until an action is called

## Code Example

```python
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://example.com")

        # CSS selector
        heading = page.locator("h1")
        print(f"CSS: {await heading.inner_text()}")

        # Text selector
        link = page.locator("text=More information")
        print(f"Text selector href: {await link.get_attribute('href')}")

        # XPath selector
        div = page.locator("//div/p")
        print(f"XPath: {await div.inner_text()}")

        await browser.close()


asyncio.run(main())
```

Run with: `python ../code/02-locators-selectors.py`

## Key Takeaways
- Prefer CSS and text selectors — they are faster and more readable.
- Locators automatically wait for elements before acting (auto-waiting).
- Avoid chaining raw `page.query_selector()` — stick to `page.locator()`.
