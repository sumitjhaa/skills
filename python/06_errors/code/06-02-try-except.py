"""File operations and database transactions with robust error handling."""
import json


def read_user_data(filepath: str) -> dict:
    result = {"status": "unknown", "data": None}
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] File not found")
        result["status"] = "not_found"
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON: {e}")
        result["status"] = "invalid_data"
    except PermissionError:
        print(f"[ERROR] Permission denied")
        result["status"] = "no_permission"
    else:
        print(f"[OK] Loaded {len(data)} records")
        result["status"] = "success"
        result["data"] = data
    finally:
        print(f"[LOG] Read attempt: {result['status']}")
    return result


def safe_divide_list(values: list, divisor: float) -> list:
    results = []
    for v in values:
        try:
            results.append(v / divisor)
        except ZeroDivisionError:
            results.append(None)
        except TypeError:
            results.append(None)
    return results


print(read_user_data("/tmp/nonexistent.json"))
with open("/tmp/empty.json", "w") as f:
    f.write("not valid json")
print(read_user_data("/tmp/empty.json"))
print(safe_divide_list([10, 0, "a", 20], 2))
