"""Frames & windows — frame locators, popup handling."""
from playwright.sync_api import sync_playwright

print("=== Frames & Windows ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("data:text/html,<iframe srcdoc='<h1>Inside Frame</h1>'></iframe>")
    frame = page.frame_locator("iframe")
    text = frame.locator("h1").text_content()
    print(f"Frame heading: {text}")

    with page.expect_popup() as popup_info:
        page.evaluate("window.open('https://example.com')")
    popup = popup_info.value
    popup.wait_for_load_state()
    print(f"Popup title: {popup.title()}")
    popup.close()

    browser.close()

print("\n✅ Frames and popups handled.")
