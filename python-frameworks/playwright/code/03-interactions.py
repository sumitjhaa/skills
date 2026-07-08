"""Interactions — click, fill, select, check, dblclick."""
from playwright.sync_api import sync_playwright

print("=== Interactions ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")

    link = page.locator("a")
    print(f"Link text: {link.text_content()}")

    page.goto("data:text/html,<input id='name'><button onclick='alert(\"hi\")'>Go</button>")
    page.fill("#name", "Alice")
    print(f"Input value: {page.input_value('#name')}")

    page.click("button")
    print("Button clicked")

    page.goto("data:text/html,<select id='s'><option>a<option>b<option>c</select>")
    page.select_option("#s", "b")
    print(f"Selected: {page.input_value('#s')}")

    page.goto("data:text/html,<input type='checkbox' id='c'>")
    page.check("#c")
    print(f"Checkbox checked: {page.is_checked('#c')}")

    browser.close()

print("\n✅ All interaction types work.")
