"""Built-in functions: data analysis toolkit — weekly sales"""

products = ["Widget", "Gadget", "Doohickey", "Thingy"]
prices = [12.99, 24.50, 5.75, 8.50]
weekly_sales = [34, 28, 51, 43]

# --- METADATA ---
print("=== Data Overview ===")
print(f"Products: {len(products)} items, type={type(prices)}, id={id(products)}")
print(f"repr(sales)={repr(weekly_sales)}, hash('Widget')={hash('Widget')}")

# --- MATH ---
print("\n=== Sales Summary ===")
total, lo, hi = sum(weekly_sales), min(weekly_sales), max(weekly_sales)
print(f"Total: {total} | Min: {lo} | Max: {hi}")
print(f"Avg price: ${round(sum(prices)/len(prices), 2)}")
print(f"Spread: ${round(abs(max(prices)-min(prices)), 2)}")

# --- SORTING & ORDERING ---
print("\n=== Rankings (high to low) ===")
for rank, (prod, sales) in enumerate(
    sorted(zip(products, weekly_sales), key=lambda x: x[1], reverse=True), 1
):
    print(f"  #{rank}: {prod} ({sales})")

print("Products reversed:", list(reversed(products)))
for i in range(len(products)):
    print(f"  range({i}): {products[i]}")

# --- TRANSFORMATION ---
print("\n=== Data Transformation ===")
price_per_unit = list(map(lambda p, s: round(p / s, 2), prices, weekly_sales))
print(f"Price per unit: {price_per_unit}")

high_volume = list(filter(lambda s: s > 30, weekly_sales))
print(f"Weeks >30 sold: {high_volume}")

# --- BOOLEAN CHECKS ---
print("\n=== Boolean Checks ===")
print(f"Any product >$20? {any(p > 20 for p in prices)}")
print(f"All < $50? {all(p < 50 for p in prices)}")
print(f"prices[0] is float? {isinstance(prices[0], float)}")
