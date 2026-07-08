"""Browser basics — launch, navigate, screenshot, close."""
from playwright.sync_api import sync_playwright

print("=== Browser Basics ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")
    print(f"Title: {page.title()}")
    print(f"URL:   {page.url}")
    page.screenshot(path="example.png")
    print("Screenshot saved to example.png")
    browser.close()

print("\n✅ Browser launched, navigated, screenshotted, closed.")
