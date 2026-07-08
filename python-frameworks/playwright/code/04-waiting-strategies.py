"""Waiting strategies — wait_for_selector, auto-waiting."""
from playwright.sync_api import sync_playwright

print("=== Waiting Strategies ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("data:text/html,<div id='late' style='display:none'>Appeared</div>")
    page.eval_on_selector("#late", "el => setTimeout(() => el.style.display='block', 200)")
    page.wait_for_selector("#late", state="visible")
    text = page.locator("#late").text_content()
    print(f"Element appeared: {text}")

    page.goto("https://example.com")
    page.wait_for_load_state("networkidle")
    print(f"Page fully loaded: {page.title()}")

    locator = page.locator("h1")
    print(f"Auto-waiting text: {locator.text_content()}")

    browser.close()

print("\n✅ Waiting strategies work.")
