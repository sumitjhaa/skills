"""Network error handling and API error categorization."""
import random


def call_api(endpoint: str) -> dict:
    error_type = random.choice(["network", "timeout", "auth", "rate_limit", None])
    if error_type == "network":
        raise ConnectionError(f"Cannot connect to {endpoint}")
    elif error_type == "timeout":
        raise TimeoutError(f"{endpoint} timed out")
    elif error_type == "auth":
        raise PermissionError(f"Authentication failed for {endpoint}")
    elif error_type == "rate_limit":
        raise RuntimeError("Rate limit exceeded")
    return {"status": 200, "data": {"endpoint": endpoint, "result": "ok"}}


def safe_api_call(endpoint: str) -> dict | None:
    try:
        return call_api(endpoint)
    except ConnectionError as e:
        print(f"[NETWORK] {e}")
    except TimeoutError as e:
        print(f"[TIMEOUT] {e}")
    except PermissionError as e:
        print(f"[AUTH] {e}")
    except RuntimeError as e:
        print(f"[SYSTEM] {e}")
    return None


def get_user_input(val):
    if val == "value":
        raise ValueError("Invalid value")
    elif val == "type":
        raise TypeError("Wrong type")
    elif val == "key":
        raise KeyError("Key not found")
    return "ok"


random.seed(42)
result = safe_api_call("/users")
if result:
    print("API succeeded:", result)

for v in ["value", "type", "key"]:
    try:
        get_user_input(v)
    except ValueError as e:
        print(f"ValueError: {e}")
    except TypeError as e:
        print(f"TypeError: {e}")
    except KeyError as e:
        print(f"KeyError: {e}")
