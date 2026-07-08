# Fixtures & Parallel Execution

Pytest fixtures give you reusable, isolated test setup. Combined with parallel workers, they dramatically speed up test suites.

## Key Concepts
- `@pytest.fixture` — define a fixture that yields a page or context
- `scope="function"` (default) — fresh state per test
- `conftest.py` — share fixtures across multiple test modules
- `pytest -n auto` — run tests in parallel with `pytest-xdist`
- Playwright's `page` fixture (from `pytest-playwright`) is auto-scoped to function

## Code Example

```python
import pytest
from playwright.async_api import Page, expect


# conftest.py can provide shared fixtures:
# @pytest_asyncio.fixture
# async def logged_in_page(page: Page):
#     await page.goto("https://example.com/login")
#     await page.fill("#user", "admin")
#     await page.fill("#pass", "secret")
#     await page.click("button[type='submit']")
#     yield page


@pytest.mark.asyncio
async def test_title(page: Page):
    await page.goto("https://example.com")
    await expect(page).to_have_title("Example Domain")


@pytest.mark.asyncio
async def test_heading(page: Page):
    await page.goto("https://example.com")
    heading = page.locator("h1")
    await expect(heading).to_be_visible()
    await expect(heading).to_have_text("Example Domain")
```

Run with: `pytest -n auto ../code/14-fixtures-parallel.py`

## Key Takeaways
- `pytest-xdist` with `-n auto` uses CPU count workers — ideal for CI.
- Each test gets an isolated browser context (no shared state).
- Use `conftest.py` for fixtures that set up authentication or common page objects.
