# Authentication

Save and restore browser authentication state (cookies + localStorage) to skip repeated logins and maintain session context.

## Key Concepts
- `context.storage_state()` — export cookies and localStorage to a JSON file
- `browser.new_context(storage_state=path)` — restore a saved state
- Useful for reusing authenticated sessions across multiple test runs
- Combine with `context.add_cookies()` and `page.evaluate()` for localStorage

## Code Example

```python
import asyncio
from playwright.async_api import async_playwright


STORAGE_FILE = "auth.json"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # --- Login phase ---
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://example.com")
        # Simulate login: fill form, click submit, wait for redirect
        # await page.fill("#username", "user")
        # await page.fill("#password", "pass")
        # await page.click("button[type='submit']")
        # await page.wait_for_url("**/dashboard")

        # Save auth state
        await context.storage_state(path=STORAGE_FILE)
        await context.close()

        # --- Reuse phase ---
        context2 = await browser.new_context(storage_state=STORAGE_FILE)
        page2 = await context2.new_page()
        await page2.goto("https://example.com")
        print(f"Reused session — title: {await page2.title()}")
        await context2.close()
        await browser.close()


asyncio.run(main())
```

Run with: `python ../code/09-authentication.py`

## Key Takeaways
- `storage_state` captures both cookies and localStorage.
- Never commit `auth.json` to version control — add it to `.gitignore`.
- Storage state is browser-context-specific; incognito contexts start fresh.
