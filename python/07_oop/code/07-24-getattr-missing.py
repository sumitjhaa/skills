"""__getattr__, __getattribute__, __missing__ — dynamic attribute handling"""

class DefaultDict(dict):
    def __missing__(self, key):
        return f"<{key}: not found>"

class APIClient:
    BASE = "https://api.example.com/v1"

    def __getattr__(self, name):
        return f"{self.BASE}/{name}"

    def __dir__(self):
        return super().__dir__() + ["users", "orders", "products"]

d = DefaultDict({"name": "Alice"})
print(f"name={d['name']}, missing={d['xyz']}")

api = APIClient()
print(f"Users URL: {api.users}")
print(f"Orders URL: {api.orders}")
print(f"Known endpoints: {'users' in dir(api)}")
