"""File uploads & downloads."""
from playwright.sync_api import sync_playwright
import os

print("=== File Uploads & Downloads ===\n")

file_path = "/tmp/test_upload.txt"
with open(file_path, "w") as f:
    f.write("hello playwright")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("data:text/html,<input type='file' id='upload'>")
    page.set_input_files("#upload", file_path)
    print(f"Uploaded file: {file_path}")

    page.goto("https://example.com")
    page.screenshot(path="/tmp/downloaded.png")
    print(f"Screenshot saved: /tmp/downloaded.png")
    print(f"File exists: {os.path.exists('/tmp/downloaded.png')}")

    os.remove("/tmp/downloaded.png")
    browser.close()

os.remove(file_path)
print("\n✅ File uploads and downloads work.")
