# 🕷️ Selenium & Dynamic Web Scraping
<!-- ⏱️ 14 min | 🔴 Advanced | 🧠 Production -->

**What You'll Learn:** Scrape JavaScript-rendered websites using Selenium — handling dynamic content, waiting for elements, and avoiding detection.

> 💡 **TL;DR — The whole point:** BeautifulSoup can't execute JavaScript. For SPAs (React, Vue, Angular) or content loaded after page load, you need Selenium — a browser automation tool that drives a real Chrome/Firefox.

## 🔗 Why This Matters
Modern websites are built with JavaScript frameworks. The content you see in your browser doesn't exist in the HTML — it's rendered by JS after page load. BeautifulSoup sees an empty page. Selenium drives a real browser that runs the JS, then you extract the rendered content.

## The Concept

| Tool | When to Use |
|------|------------|
| `httpx` + `BeautifulSoup` | Static HTML pages, simple APIs |
| `requests-html` | Light JS rendering (Chromium-based) |
| **Selenium** | Full browser automation, SPAs, complex interactions |
| `Playwright` / `Puppeteer` | Modern alternatives (faster, better API) |

## Code Example

```python
"""Selenium — dynamic web scraping with browser automation."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

print("=== Selenium Demo ===")
print("""
This script demonstrates the Selenium pattern for dynamic scraping.
Install: pip install selenium webdriver-manager

The actual browser automation is commented out — it requires a
running browser. The code below shows the complete pattern.
""")

DEMO_CODE = '''
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup (auto-downloads chromedriver)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # run without visible window
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options,
)

try:
    driver.get("https://example.com")

    # Wait for an element to be present (up to 10 seconds)
    heading = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    print(f"Page title: {driver.title}")
    print(f"Heading: {heading.text}")

    # Find elements
    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links[:5]:
        print(f"  {link.text}: {link.get_attribute('href')}")

    # Execute JavaScript (for scrolling, clicking, etc.)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Take screenshot
    driver.save_screenshot("screenshot.png")

finally:
    driver.quit()
'''

print(DEMO_CODE)

print("\n=== Key Wait Strategies ===")
waits = [
    ("presence_of_element_located", "Element exists in DOM (may be hidden)"),
    ("visibility_of_element_located", "Element is visible (display != none)"),
    ("element_to_be_clickable", "Element is visible and enabled"),
    ("text_to_be_present_in_element", "Element contains specific text"),
    ("staleness_of", "Element removed from DOM (e.g., loading spinner)"),
]
for name, desc in waits:
    print(f"  EC.{name} — {desc}")

print("\n=== Common Selectors ===")
print("  By.ID, By.CLASS_NAME, By.TAG_NAME, By.CSS_SELECTOR")
print("  By.XPATH — most powerful: //div[@class='product']//h2")

print("\n=== Anti-Detection Tips ===")
tips = [
    "Set a realistic user-agent (mobile/desktop)",
    "Add random delays between actions (time.sleep(random.uniform(1,3)))",
    "Use headless mode cautiously — some sites block headless browsers",
    "Rotate IP addresses via proxies for large-scale scraping",
    "Respect robots.txt and terms of service",
    "Use Playwright as a modern alternative to Selenium",
]
for i, tip in enumerate(tips, 1):
    print(f"  {i}. {tip}")
```

## 🔍 How It Works
- `webdriver.Chrome()` launches a real Chrome instance (automated, not user-mode)
- `--headless` runs Chrome without a visible window (faster, no display needed)
- `WebDriverWait(driver, timeout).until(EC.condition)` polls the DOM until the condition is met
- `find_element(By.ID, "price")` returns the first match; `find_elements` returns all matches
- `driver.execute_script("return window.pageYOffset")` runs arbitrary JS in the browser
- `driver.save_screenshot("page.png")` captures a screenshot — useful for debugging

## ⚠️ Common Pitfall
- Not waiting for elements — Selenium is fast, the page is slow. Always `WebDriverWait` before interacting
- Stale elements — if JS re-renders the DOM, a previously-found element is "stale". Re-find it
- Implicit vs explicit wait mixing — don't mix `driver.implicitly_wait()` with `WebDriverWait`
- Not closing the driver — leaks memory and zombie Chrome processes. Use `try/finally` or context manager

## 🧠 Memory Aid
"WebDriverWait + EC + By — the holy trinity of Selenium. Wait for elements, find by selectors, clean up with driver.quit()."

## 🏃 Try It
Write a Selenium script that opens a product page (e.g., Amazon or a demo site), waits for the price element to appear, extracts the price and product name, and saves a screenshot. Add random delays to be respectful.

## 🔗 Related
- [Web Scraping](15-web-scraping.md) — BeautifulSoup + httpx (static pages)
- [Asyncio Intro](02-asyncio-intro.md) — async scraping with aiohttp
- [Web Frameworks](17-flask-django.md) — building APIs that serve scraped data

## ➡️ Next
Course Complete! Review the [Master Index](../00_curriculum/03-course-index.md) to revisit any topic.
