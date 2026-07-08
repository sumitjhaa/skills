# Performance Metrics

Measure page load performance, capture console logs, and record trace files to diagnose slow or broken pages.

## Key Concepts
- `page.evaluate("window.performance.timing")` — navigation timing metrics
- `page.on("console")` — listen to browser console messages
- `context.tracing.start()` / `stop()` — record a trace for the Playwright Trace Viewer
- `page.metrics()` — runtime metrics (JS heap, DOM nodes, layouts)
- Console listeners can assert no errors are logged during a test

## Code Example

```python
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        # Record a trace
        await context.tracing.start(screenshots=True, snapshots=True)

        page = await context.new_page()

        # Listen to console messages
        page.on("console", lambda msg: print(f"[{msg.type}] {msg.text}"))

        await page.goto("https://example.com")

        # Performance timing
        timing = await page.evaluate("window.performance.timing")
        load_time = timing["loadEventEnd"] - timing["navigationStart"]
        print(f"Page load time: {load_time}ms")

        # Runtime metrics
        metrics = await page.metrics()
        print(f"JS heap used: {metrics['JSHeapUsedSize'] / 1024:.1f} KB")

        # Stop and save trace
        await context.tracing.stop(path="trace.zip")

        await browser.close()


asyncio.run(main())
```

Run with: `python ../code/12-performance-metrics.py`

## Key Takeaways
- Open `trace.zip` in the Playwright Trace Viewer (trace.playwright.dev) for a full replay.
- Console listeners help catch JS errors early during CI.
- Performance timings are most reliable when measured with `wait_for_load_state("networkidle")`.
