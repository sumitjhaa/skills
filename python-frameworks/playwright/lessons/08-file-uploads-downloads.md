# File Uploads & Downloads

Playwright can upload files from disk and download files triggered by page actions, with both handled through simple, robust APIs.

## Key Concepts
- `locator.set_input_files()` — select files for an `<input type="file">` element
- `page.expect_download()` — capture a download triggered by a click or navigation
- `Download` object provides `save_as()`, `suggested_filename`, `url`
- Uploads accept file paths, `File` objects, or `bytes`

## Code Example

```python
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://example.com")

        # Upload a file (use a real input selector)
        # await page.locator('input[type="file"]').set_input_files("data.csv")

        # Download a file
        async with page.expect_download() as download_info:
            await page.locator("text=More information").click()
        download = await download_info.value
        await download.save_as(f"downloads/{download.suggested_filename}")
        print(f"Downloaded: {download.suggested_filename}")

        await browser.close()


asyncio.run(main())
```

Run with: `python ../code/08-file-uploads-downloads.py`

## Key Takeaways
- `set_input_files()` replaces any previously selected files.
- `expect_download()` must be scoped to the exact action that triggers the download.
- Use `pathlib.Path` for cross-platform file paths in uploads.
