"""Error aggregation — multiple API calls that all can fail."""
import random


def check_service(service_name: str) -> str:
    roll = random.randint(1, 10)
    if roll <= 3:
        raise ConnectionError(f"{service_name} is unreachable")
    if roll <= 5:
        raise TimeoutError(f"{service_name} timed out")
    return f"{service_name} is healthy"


def check_all_services(services: list) -> list:
    results = []
    errors = []
    for service in services:
        try:
            results.append(check_service(service))
        except (ConnectionError, TimeoutError) as e:
            errors.append(e)
    if errors:
        raise ExceptionGroup("Multiple service failures", errors)
    return results


def validate_batch(data_list: list) -> list:
    errors = []
    for item in data_list:
        if not isinstance(item, int) or item < 0:
            errors.append(ValueError(f"Invalid item: {item}"))
    if errors:
        raise ExceptionGroup("Validation failed", errors)
    return data_list


services = ["database", "cache", "auth", "api-gateway", "payment"]
random.seed(42)

try:
    results = check_all_services(services)
    print("All healthy:", results)
except* ConnectionError as e:
    print(f"[NETWORK] {len(e.exceptions)} failures:")
    for exc in e.exceptions:
        print(f"  - {exc}")
except* TimeoutError as e:
    print(f"[TIMEOUT] {len(e.exceptions)} failures:")

try:
    validate_batch([1, -2, "bad", 4])
except* ValueError as e:
    print(f"[VALIDATION] {len(e.exceptions)} errors")
