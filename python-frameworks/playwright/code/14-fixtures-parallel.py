"""Fixtures & parallel — pytest integration pattern."""
from playwright.sync_api import sync_playwright

print("=== Fixtures & Parallel Testing ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    contexts = []
    pages = []
    for i in range(3):
        ctx = browser.new_context()
        pg = ctx.new_page()
        pg.goto("https://example.com")
        contexts.append(ctx)
        pages.append(pg)
        print(f"  Context {i+1}: title = {pg.title()}, isolated")

    for ctx in contexts:
        ctx.close()
    browser.close()

print("\nThree isolated contexts created (simulating parallel test isolation).")
print("In pytest-playwright:")
print("  @pytest.fixture")
print("  def page(page): return page  # built-in isolation")

print("\n✅ Fixture isolation pattern demonstrated.")
