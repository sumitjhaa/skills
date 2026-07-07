"""Web scraping with BeautifulSoup — product listing scraper.
Run: python 10-15-web-scraping.py
"""
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

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
<div class="product" data-id="103">
  <h2 class="name">USB-C Hub</h2>
  <span class="price">$34.99</span>
  <div class="rating">★★★☆☆ 3.5</div>
</div>
</body></html>"""


def scrape_products(html: str) -> list[dict]:
    if not HAS_BS4:
        print("  [SKIP] pip install beautifulsoup4")
        return []
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for card in soup.select("div.product"):
        products.append({
            "id": card["data-id"],
            "name": card.find("h2", class_="name").text,
            "price": card.find("span", class_="price").text,
            "rating": card.find("div", class_="rating").text.split()[-1],
        })
    return products


def paginate(pages: int = 3) -> list[dict]:
    """Simulate pagination across multiple product pages (mock)."""
    all_products: list[dict] = []
    for page in range(1, pages + 1):
        page_html = HTML.replace("data-id=\"10", f"data-id=\"{page}")
        all_products.extend(scrape_products(page_html))
    return all_products


if __name__ == "__main__":
    print("═" * 40)
    print("Product Listing Scraper")
    print("═" * 40)

    products = scrape_products(HTML)
    for p in products:
        print(f"  {p['id']}: {p['name']} — {p['price']} (★ {p['rating']})")
    print()

    print("Pagination demo:")
    for p in paginate(2):
        print(f"  {p['id']}: {p['name']} — {p['price']}")
