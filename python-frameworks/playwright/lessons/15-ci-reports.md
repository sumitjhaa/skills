# CI & Reports

Generate HTML and JUnit reports from Playwright runs, and integrate tests into GitHub Actions, GitLab CI, or Jenkins.

## Key Concepts
- `pytest --html=report.html` — generate a self-contained HTML report
- `pytest --junitxml=report.xml` — JUnit XML for CI dashboard integration
- `pytest-playwright` includes retry, video, and screenshot-on-failure options
- CI patterns: headless mode, retry flaky tests, store reports as artifacts
- Environment variables (`CI`, `PLAYWRIGHT_BROWSERS_PATH`) configure the runner

## Code Example

```python
# pytest.ini
"""
[pytest]
addopts =
    --headed  ; set to --headed=False in CI
    --screenshot=only-on-failure
    --video=retain-on-failure
    --html=reports/test-report.html
    --junitxml=reports/junit.xml
testpaths = tests
"""

# GitHub Actions snippet (for reference):
# - name: Run Playwright tests
#   run: pytest -n auto --headed=false
# - name: Upload test report
#   uses: actions/upload-artifact@v4
#   if: always()
#   with:
#     name: playwright-report
#     path: reports/


import pytest
from playwright.async_api import Page, expect


@pytest.mark.asyncio
async def test_example(page: Page):
    await page.goto("https://example.com")
    await expect(page.locator("h1")).to_be_visible()
```

Run with: `pytest --html=report.html --junitxml=report.xml ../code/15-ci-reports.py`

## Key Takeaways
- HTML reports include screenshots, video links, and stack traces — great for debugging.
- JUnit XML integrates with Jenkins, GitLab, and GitHub Actions test dashboards.
- Always upload reports and traces as CI artifacts to inspect failures after a run.
