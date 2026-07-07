# 🕸️ Web Scraping with BeautifulSoup
<!-- ⏱️ 15 min | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Fetch HTML with httpx, parse it with BeautifulSoup, extract data with `find()` and CSS selectors, and simulate pagination.

> 💡 **TL;DR — The whole point:** BeautifulSoup turns messy HTML into a navigable tree — use `find()`/`select()` to pull out exactly the data you need (prices, names, ratings). Always respect `robots.txt` and add delays between requests.

## 🔗 Why This Matters
Price monitoring, data journalism, lead generation, and competitor analysis all start with scraping public web data.

## The Concept

1. **Fetch** HTML with `httpx.get(url)` (or `requests`)
2. **Parse** with `BeautifulSoup(html, "html.parser")`
3. **Extract** with `.find()` (first match), `.find_all()` (all), or `.select()` (CSS selectors)
4. **Pagination** — loop through `?page=N` query params

## Code Example

```python
"""Web scraping with BeautifulSoup — product listing scraper."""

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

# Simulated HTML — like a real e-commerce listing page
HTML = """\
<html><body>
<div class="product" data-id="101">
  <h2 class="name">Wireless Mouse</h2>
  <span class="price">$29.99</span>
  <div class="rating">★★★★☆ 4.2</div>
</div>
<div class="product" data-id="102">
  <h2 class="name">Mechanical Keyboard</h2>
  <span class="price">$89.99</span>
  <div class="rating">★★★★★ 4.8</div>
</div>
</body></html>"""


def scrape_products(html: str) -> list[dict]:
    if not HAS_BS4:
        return []
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for card in soup.select("div.product"):
        products.append({
            "id": card["data-id"],
            "name": card.find("h2", class_="name").text,
            "price": card.find("span", class_="price").text,
            "rating": card.find("div", class_="rating").text,
        })
    return products


if __name__ == "__main__":
    for p in scrape_products(HTML):
        print(f"{p['id']}: {p['name']} — {p['price']}")
```

## 🔍 How It Works
- `BeautifulSoup(html, "html.parser")` — builds a parse tree from the HTML string
- `soup.select("div.product")` — CSS selector; returns all `<div class="product">` elements
- `card.find("h2", class_="name")` — finds first `<h2 class="name">` inside the card
- `.text` — strips all tags, returns the inner text
- `card["data-id"]` — reads an HTML attribute like a dict key

## ⚠️ Common Pitfall
**Parsing large pages in memory.** Download the full HTML first, then parse — don't stream-parse HTML. Add `time.sleep(1)` between pagination requests to avoid rate-limiting. Check `robots.txt` before scraping.

## 🧠 Memory Aid
"BS4 = find (first), find_all (all), select (CSS). `.text` strips tags. `tag["attr"]` reads attributes."

## 🏃 Try It
Add a `min_price` filter to `scrape_products()` that skips products under a given price, then call it with `min_price=50`.

## 🏎️ Beyond Static HTML: Selenium

BeautifulSoup can't execute JavaScript. For modern SPAs (React, Vue) where content loads dynamically:

```python
# Pattern for JavaScript-rendered pages (pip install selenium webdriver-manager)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # run without visible window
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://example.com")
    # Wait for dynamic content to render
    products = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "product"))
    )
    # Now the HTML has all the JS-rendered content
    html = driver.page_source
    # Pass to BeautifulSoup as usual
finally:
    driver.quit()
```

Use `requests` + `BeautifulSoup` for static pages. Use **Selenium** for pages that load content via JavaScript. See [Selenium & Dynamic Scraping](20-selenium-dynamic-scraping.md) for the full guide.

## 🔗 Related
- [Selenium & Dynamic Scraping](20-selenium-dynamic-scraping.md) — full dynamic scraping guide
- [03-Web APIs](../03-web-apis.md) — consuming structured JSON APIs
- [14-httpx-requests-deep](../../09_production/lessons/14-httpx-requests-deep.md) — HTTP client deep dive

## ➡️ Next
[16-Python MongoDB](16-python-mongodb.md)
