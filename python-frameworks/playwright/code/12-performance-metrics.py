"""Performance metrics — timing, console, tracing."""
from playwright.sync_api import sync_playwright

print("=== Performance Metrics ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    logs = []
    page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))
    page.evaluate("console.log('hello from page')")

    page.goto("https://example.com")
    timing = page.evaluate("() => JSON.stringify(window.performance.timing)")
    import json
    timings = json.loads(timing)
    load_time = timings.get("loadEventEnd", 0) - timings.get("navigationStart", 0)
    print(f"Page load time: {load_time}ms")

    print(f"Console logs captured: {logs}")

    context.tracing.start(screenshots=True, snapshots=True)
    page.goto("https://example.com")
    context.tracing.stop(path="/tmp/trace.zip")
    import os; print(f"Trace saved: {os.path.getsize('/tmp/trace.zip')} bytes"); os.remove("/tmp/trace.zip")

    context.close()
    browser.close()

print("\n✅ Performance metrics collected.")
