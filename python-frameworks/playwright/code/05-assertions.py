"""Assertions — expect() API matchers."""
from playwright.sync_api import sync_playwright, expect

print("=== Assertions ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")

    h1 = page.locator("h1")
    expect(h1).to_be_visible()
    expect(h1).to_have_text("Example Domain")
    expect(page).to_have_url("https://example.com/")
    expect(page.locator("p")).to_have_count(2)
    expect(page.locator("body")).to_contain_text("domain")

    print("✅ All assertions passed:")
    print("  to_be_visible ✓")
    print("  to_have_text ✓")
    print("  to_have_url ✓")
    print("  to_have_count ✓")
    print("  to_contain_text ✓")

    browser.close()

print("\n✅ Assertions verified.")
