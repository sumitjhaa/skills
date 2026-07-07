"""Data processing pipeline — pipe patterns and middleware chains."""


def pipe(*funcs):
    def applied(x):
        for f in funcs:
            x = f(x)
        return x
    return applied


def compose(*funcs):
    def applied(x):
        for f in reversed(funcs):
            x = f(x)
        return x
    return applied


def process_sales_order(order: dict) -> dict:
    def validate(o):
        if "items" not in o or not o["items"]:
            raise ValueError("Order has no items")
        return o

    def calculate_totals(o):
        o["subtotal"] = sum(item["price"] * item["qty"] for item in o["items"])
        o["tax"] = round(o["subtotal"] * 0.08, 2)
        o["total"] = round(o["subtotal"] + o["tax"], 2)
        return o

    def format_response(o):
        o["summary"] = f"Order {o['id']}: {len(o['items'])} items, total ${o['total']}"
        return o

    return pipe(validate, calculate_totals, format_response)(order)


def clean(text: str) -> str:
    return text.strip().lower()


def tokenize(text: str) -> list:
    return text.split()


def count_words(tokens: list) -> dict:
    counts = {}
    for t in tokens:
        counts[t] = counts.get(t, 0) + 1
    return counts


order = {"id": "ORD-42", "items": [{"name": "Laptop", "price": 1200, "qty": 1}, {"name": "Mouse", "price": 25, "qty": 2}]}
result = process_sales_order(order)
print(result["summary"])

pipeline = pipe(clean, tokenize, count_words)
print(pipeline("Hello world hello hello"))
