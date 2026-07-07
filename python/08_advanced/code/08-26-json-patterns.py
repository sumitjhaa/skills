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
