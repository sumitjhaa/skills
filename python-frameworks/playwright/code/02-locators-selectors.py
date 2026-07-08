"""Locators & selectors — CSS, text, XPath."""
from playwright.sync_api import sync_playwright

print("=== Locators & Selectors ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")

    css_h1 = page.locator("h1")
    print(f"CSS 'h1' text: {css_h1.text_content()}")

    text_locator = page.locator("text=Example Domain")
    print(f"Text locator exists: {text_locator.count() > 0}")

    xpath_h1 = page.locator("//h1")
    print(f"XPath '//h1' text: {xpath_h1.text_content()}")

    all_text = page.locator("body").inner_text()[:100]
    print(f"Body text (first 100 chars): {all_text.strip()}")

    browser.close()

print("\n✅ Multiple selector strategies work.")
