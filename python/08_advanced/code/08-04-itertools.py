"""08-04-itertools.py — E-commerce: itertools for inventory and pricing."""

from itertools import chain, cycle, islice, product, combinations, groupby, accumulate, count

products = {"Laptop": 1200, "Mouse": 25, "Keyboard": 80, "Monitor": 400, "Webcam": 60}

categories = {"Electronics": ["Laptop", "Monitor"], "Accessories": ["Mouse", "Keyboard", "Webcam"]}
all_items = list(chain.from_iterable(categories.values()))
print(f"All items: {all_items}")

daily_sales = [1200, 800, 1500, 900, 2000]
running_total = list(accumulate(daily_sales))
print(f"Running total: {running_total}")

bundle_base = ["Laptop", "Desktop"]
bundle_addons = ["Mouse", "Keyboard"]
bundles = list(product(bundle_base, bundle_addons))
print(f"Bundles: {bundles}")

price_tiers = [19.99, 29.99, 49.99]
combo_prices = list(combinations(price_tiers, 2))
print(f"Price combos: {combo_prices}")

def price_range(price: float) -> str:
    return "budget" if price < 50 else "mid" if price < 500 else "premium"

sorted_prods = sorted(products.items(), key=lambda x: price_range(x[1]))
for group, items in groupby(sorted_prods, key=lambda x: price_range(x[1])):
    print(f"  {group}: {[name for name, _ in items]}")

recs = cycle(["Laptop", "Mouse", "Keyboard"])
print(f"First 5 recs: {list(islice(recs, 5))}")

ids = list(islice(count(start=1000, step=2), 5))
print(f"Generated IDs: {ids}")
