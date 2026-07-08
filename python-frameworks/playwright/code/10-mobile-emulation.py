"""Mobile emulation — device presets, viewport, geolocation."""
from playwright.sync_api import sync_playwright

print("=== Mobile Emulation ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    iphone = p.devices["iPhone 13"]
    context = browser.new_context(**iphone)
    page = context.new_page()

    page.goto("https://example.com")
    print(f"Viewport: {page.viewport_size}")
    print(f"Title: {page.title()}")

    context2 = browser.new_context(
        viewport={"width": 375, "height": 812},
        user_agent="CustomMobile/1.0",
        locale="en-US",
        geolocation={"latitude": 48.8566, "longitude": 2.3522},
        permissions=["geolocation"],
    )
    page2 = context2.new_page()
    page2.goto("https://example.com")
    print(f"Custom viewport: {page2.viewport_size}")
    print(f"User-agent: custom mobile")
    context2.close()

    context.close()
    browser.close()

print("\n✅ Mobile emulation configured.")
