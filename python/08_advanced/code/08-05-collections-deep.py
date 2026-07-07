"""08-05-collections-deep.py — E-commerce: Counter, defaultdict, deque, ChainMap."""

from collections import Counter, defaultdict, deque, ChainMap

sales = ["Laptop", "Mouse", "Laptop", "Keyboard", "Laptop", "Mouse", "Monitor"]
popularity = Counter(sales)
print(f"Most common: {popularity.most_common(3)}")
print(f"Laptop sales: {popularity['Laptop']}")

orders = [
    ("Alice", "Laptop"), ("Bob", "Mouse"), ("Alice", "Keyboard"),
    ("Bob", "Monitor"), ("Alice", "Mouse"),
]
customer_orders = defaultdict(list)
for customer, product in orders:
    customer_orders[customer].append(product)
print(f"\nAlice's orders: {customer_orders['Alice']}")

inventory = defaultdict(int)
inventory["Laptop"] += 5
inventory["Laptop"] -= 1
print(f"Laptop stock: {inventory['Laptop']}")

recent_views = deque(maxlen=5)
for action in ["viewed Laptop", "added to cart", "viewed Mouse", "searched Keyboard", "viewed Monitor", "checked out"]:
    recent_views.append(action)
print(f"\nRecent: {list(recent_views)}")

defaults = {"theme": "light", "lang": "en", "page_size": 20}
user_prefs = {"theme": "dark", "page_size": 50}
session = {"lang": "fr"}
config = ChainMap(session, user_prefs, defaults)
print(f"\nConfig: theme={config['theme']}, lang={config['lang']}, page={config['page_size']}")
