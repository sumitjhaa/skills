"""Visual testing — screenshots, comparison."""
from playwright.sync_api import sync_playwright

print("=== Visual Testing ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")

    baseline = page.screenshot()
    print(f"Baseline screenshot: {len(baseline)} bytes")

    page.evaluate("document.querySelector('h1').style.color = 'red'")
    current = page.screenshot()
    print(f"Modified screenshot: {len(current)} bytes")
    print(f"Different from baseline: {baseline != current}")

    page.screenshot(path="/tmp/fullpage.png", full_page=True)
    import os; print(f"Full page screenshot: {os.path.getsize('/tmp/fullpage.png')} bytes"); os.remove("/tmp/fullpage.png")

    masked = page.screenshot(mask=[page.locator("h1")])
    print(f"With mask: {len(masked)} bytes")

    browser.close()

print("\n✅ Visual testing capabilities demonstrated.")
