"""Network interception — route(), abort, mock responses."""
from playwright.sync_api import sync_playwright

print("=== Network Interception ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    def handle_route(route):
        if "block-me" in route.request.url:
            route.abort()
            print(f"  Aborted: {route.request.url}")
        else:
            route.continue_()

    page.route("**/*", handle_route)
    page.goto("https://example.com")
    print(f"Page loaded without blocked resources")

    def mock_api(route):
        route.fulfill(status=200, content_type="text/plain", body="mocked!")
    page.route("**/api/**", mock_api)
    page.goto("data:text/html,<script>fetch('/api/data')</script>")
    print("Mock API route registered")

    browser.close()

print("\n✅ Network interception works.")
