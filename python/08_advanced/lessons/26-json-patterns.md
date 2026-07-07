# 🎯 JSON Patterns: Custom Encoder/Decoder, object_hook
<!-- ⏱️ 13 min | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Write custom JSON encoders/decoders for `datetime`, `Decimal`, `UUID` and use `object_hook` for round-trip serialization.

> 💡 **TL;DR — The whole point:** `json.JSONEncoder.default()` lets you serialize non-native types (datetime, Decimal, UUID) by converting them to strings; `json.loads(object_hook=)` reverses the conversion on deserialization.

## 🔗 Why This Matters
Real APIs handle timestamps, monetary amounts (Decimal), and UUIDs daily. The default `json` module can't serialize these — your custom encoder makes them JSON-compatible and your decoder restores them.

## The Concept
Override `JSONEncoder.default(self, obj)` to check the type and return a JSON-safe representation (e.g., `datetime.isoformat()`). For decoding, pass an `object_hook` function to `json.loads()` that detects ISO strings and converts them back to Python objects. This gives you round-trip serialization for custom types.

## Code Example
```python
"""JSON patterns: custom encoder/decoder for datetime, Decimal, UUID — real APIs"""
import json
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

# --- 1. Custom encoder: handle types json.dumps can't serialize ---
class CustomEncoder(json.JSONEncoder):
    """Serializes datetime, Decimal, UUID into JSON-safe types"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # "2024-01-15T10:30:00" — ISO 8601 standard
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)  # Or str(obj) for exact precision
        if isinstance(obj, UUID):
            return str(obj)  # "550e8400-e29b-41d4-a716-446655440000"
        return super().default(obj)  # Let parent raise TypeError for unknown types

# --- 2. Custom decoder: convert back using object_hook ---
def custom_decoder(dct: dict) -> dict:
    """Reconstruct datetime/date from ISO strings — applied to every JSON object"""
    for key, value in dct.items():
        if isinstance(value, str):
            try:
                dct[key] = datetime.fromisoformat(value)  # Tries ISO 8601 parse
            except (ValueError, TypeError):
                pass  # Not a datetime — leave as string
    return dct

# --- Usage ---
data = {
    "event": "user_signup",
    "timestamp": datetime.now(),
    "id": UUID("550e8400-e29b-41d4-a716-446655440000"),
    "amount": Decimal("19.99"),
    "date": date.today(),
}
json_str = json.dumps(data, cls=CustomEncoder, indent=2, ensure_ascii=False)
print(f"Serialized:\n{json_str}")
restored = json.loads(json_str, object_hook=custom_decoder)
print(f"Restored datetime type: {type(restored['timestamp']).__name__}")
```

## 🔍 How It Works
- `JSONEncoder.default(self, obj)` is called for every object the encoder doesn't know how to serialize — return a JSON-safe type or call `super().default(obj)` to raise `TypeError`
- `object_hook(**callable**)` is called on every decoded dict — return the modified dict with reconstructed types
- `datetime.fromisoformat()` parses ISO 8601 strings back to `datetime` objects
- Using `float(obj)` for `Decimal` loses precision — use `str(obj)` if you need exactness

## ⚠️ Common Pitfall
`object_hook` modifies every dict in the JSON tree, not just the top-level one. If your JSON has nested dicts with string values that happen to look like ISO dates (e.g., a user's name "2024-01-15"), they'll be incorrectly converted. Use a schema-aware approach for production.

## 🧠 Memory Aid
"Encoder default = 'how to turn my type into JSON.' Decoder object_hook = 'how to turn it back.' isoformat() = 'the universal date language.'"

## 🏃 Try It
Extend `CustomEncoder` to handle `set` and `complex` types (convert set to sorted list, complex to `{"real": x, "imag": y}`). Write the corresponding decoder logic.

## 🔗 Related
- [JSON + CSV](../../../05_modules_io/lessons/06-json-csv.md) — JSON basics, `dump`/`load`, pretty-printing

## ➡️ Next
[Logging Patterns](27-logging-patterns.md)
