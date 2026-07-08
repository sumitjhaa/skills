"""CI & Reports — HTML/JUnit report generation."""
from playwright.sync_api import sync_playwright
import json, os

print("=== CI & Reports ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com")

    junit_report = {
        "testsuites": {
            "testsuite": {
                "name": "playwright-tests",
                "tests": "2",
                "failures": "0",
                "testcase": [
                    {"name": "page loads", "classname": "Example", "time": "0.5"},
                    {"name": "title correct", "classname": "Example", "time": "0.3"},
                ]
            }
        }
    }

    with open("/tmp/junit-report.xml", "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<testsuites>\n')
        f.write('  <testsuite name="playwright-tests" tests="2" failures="0">\n')
        f.write('    <testcase name="page loads" classname="Example" time="0.5"/>\n')
        f.write('    <testcase name="title correct" classname="Example" time="0.3"/>\n')
        f.write('  </testsuite>\n')
        f.write('</testsuites>\n')

    print("JUnit report generated at /tmp/junit-report.xml")

    print("\nIn CI (GitHub Actions):")
    print("  - name: Run Playwright tests")
    print("    run: pytest --html=report.html --junit-xml=junit.xml")
    print("  - uses: actions/upload-artifact@v4")
    print("    with:")
    print("      name: playwright-report")
    print("      path: report.html")

    os.remove("/tmp/junit-report.xml")
    browser.close()

print("\n✅ CI report patterns demonstrated.")
