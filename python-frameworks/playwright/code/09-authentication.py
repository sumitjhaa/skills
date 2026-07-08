"""Authentication — storageState, cookies, localStorage."""
from playwright.sync_api import sync_playwright
import json

print("=== Authentication ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://example.com")
    page.evaluate("localStorage.setItem('token', 'abc123')")
    context.add_cookies([{
        "name": "session",
        "value": "user123",
        "url": "https://example.com"
    }])
    context.storage_state(path="/tmp/state.json")

    with open("/tmp/state.json") as f:
        state = json.load(f)
    cookies = state.get("cookies", [])
    origins = state.get("origins", [])
    print(f"Cookies saved: {len(cookies)}")
    print(f"Origins saved: {len(origins)}")

    new_context = browser.new_context(storage_state="/tmp/state.json")
    restored_page = new_context.new_page()
    restored_page.goto("https://example.com")
    token = restored_page.evaluate("localStorage.getItem('token')")
    print(f"Restored token: {token}")
    new_context.close()

    import os; os.remove("/tmp/state.json")
    browser.close()

print("\n✅ Authentication state saved and restored.")
