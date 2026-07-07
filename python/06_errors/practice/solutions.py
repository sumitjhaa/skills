"""Phase 06: Error Handling — Practice Solutions."""
import logging
import time
import json
import os
from contextlib import contextmanager
from functools import wraps


def ex1_safe_divide_file():
    def safe_divide_file(in_path, out_path):
        try:
            with open(in_path) as f:
                lines = f.readlines()
            a, b = float(lines[0].strip()), float(lines[1].strip())
            with open(out_path, "w") as f:
                f.write(str(a / b))
            return a / b
        except FileNotFoundError:
            return "File not found"
        except (ValueError, ZeroDivisionError) as e:
            return f"Error: {e}"
    with open("/tmp/ex1_input.txt", "w") as f:
        f.write("10\n2\n")
    result = safe_divide_file("/tmp/ex1_input.txt", "/tmp/ex1_out.txt")
    assert result == 5.0
    os.remove("/tmp/ex1_input.txt")
    os.remove("/tmp/ex1_out.txt")
    print("1. Safe divide: OK")


def ex2_validate_age():
    def validate_age(age):
        if not isinstance(age, (int, float)) or age < 0 or age > 150:
            raise ValueError(f"Invalid age: {age}")
        assert age >= 0
        return age
    assert validate_age(25) == 25
    try:
        validate_age(-1)
    except ValueError:
        pass
    print("2. Validate age: OK")


def ex3_bank_account():
    class AccountError(Exception):
        pass

    class InsufficientBalanceError(AccountError):
        def __init__(self, balance, amount):
            super().__init__(f"need {amount}, have {balance}")

    class NegativeAmountError(AccountError):
        def __init__(self, amount):
            super().__init__(f"negative amount: {amount}")

    class Account:
        def __init__(self, owner, balance=0):
            self.owner = owner
            self.balance = balance

        def deposit(self, amount):
            if amount < 0:
                raise NegativeAmountError(amount)
            self.balance += amount

        def withdraw(self, amount):
            if amount < 0:
                raise NegativeAmountError(amount)
            if amount > self.balance:
                raise InsufficientBalanceError(self.balance, amount)
            self.balance -= amount

    acct = Account("Alice", 100)
    acct.deposit(50)
    assert acct.balance == 150
    acct.withdraw(30)
    assert acct.balance == 120
    print("3. Bank account: OK")


def ex4_timing_context():
    @contextmanager
    def timed(label="Block"):
        start = time.perf_counter()
        yield
        elapsed = time.perf_counter() - start
        print(f"  [{label}] took {elapsed:.4f}s")

    with timed("Test"):
        time.sleep(0.01)
    print("4. Timing context: OK")


def ex5_setup_logger():
    def setup_logger(name, log_file):
        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        fh = logging.FileHandler(log_file, mode="w")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        log.addHandler(ch)
        log.addHandler(fh)
        return log

    log = setup_logger("ex5", "/tmp/ex5.log")
    log.info("test")
    assert open("/tmp/ex5.log").read().strip()
    os.remove("/tmp/ex5.log")
    print("5. Logger setup: OK")


def ex6_exception_chaining():
    def parse_settings(path):
        try:
            with open(path) as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise RuntimeError("config loading failed") from e

    with open("/tmp/ex6_bad.json", "w") as f:
        f.write("{bad json}")
    try:
        parse_settings("/tmp/ex6_bad.json")
    except RuntimeError as e:
        assert "config loading failed" in str(e)
    os.remove("/tmp/ex6_bad.json")
    print("6. Exception chaining: OK")


def ex7_exceptiongroup():
    def validate_products(products):
        errors = []
        for i, p in enumerate(products):
            if "name" not in p:
                errors.append(ValueError(f"Product {i}: missing name"))
            if "price" not in p or not isinstance(p.get("price"), (int, float)):
                errors.append(ValueError(f"Product {i}: invalid price"))
        if errors:
            raise ExceptionGroup("Product validation failed", errors)
        return products

    products = [{"name": "A", "price": 10}, {"price": 20}, {"name": "C"}]
    try:
        validate_products(products)
    except ExceptionGroup as eg:
        assert len(eg.exceptions) == 2
    print("7. ExceptionGroup: OK")


def ex8_retry_backoff():
    def retry_with_backoff(max_retries=3, base_delay=0.1):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                last_exc = None
                for attempt in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_exc = e
                        time.sleep(base_delay * (2 ** attempt))
                raise last_exc
            return wrapper
        return decorator

    call_count = 0

    @retry_with_backoff(max_retries=3)
    def flaky():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("fail")
        return "ok"

    assert flaky() == "ok"
    assert call_count == 3
    print("8. Retry backoff: OK")


def ex9_atomic_write():
    @contextmanager
    def atomic_write(filepath):
        tmp = filepath + ".tmp"
        try:
            yield tmp
            os.replace(tmp, filepath)
        except Exception:
            if os.path.exists(tmp):
                os.remove(tmp)
            raise

    with atomic_write("/tmp/ex9_atomic.txt") as tmp:
        with open(tmp, "w") as f:
            f.write("atomic!")
    assert open("/tmp/ex9_atomic.txt").read() == "atomic!"
    os.remove("/tmp/ex9_atomic.txt")
    print("9. Atomic write: OK")


def ex10_multi_service_check():
    import random

    def check_endpoints(urls):
        healthy = 0
        unhealthy = 0
        errors = []
        for url in urls:
            try:
                roll = random.randint(1, 10)
                if roll <= 3:
                    raise ConnectionError(f"{url} unreachable")
                if roll <= 5:
                    raise TimeoutError(f"{url} timed out")
                healthy += 1
            except (ConnectionError, TimeoutError) as e:
                unhealthy += 1
                errors.append(e)
        if errors:
            raise ExceptionGroup("Health check failures", errors)
        return {"healthy": healthy, "unhealthy": unhealthy}

    urls = ["https://api1.com", "https://api2.com", "https://api3.com", "https://api4.com"]
    random.seed(42)
    try:
        result = check_endpoints(urls)
        print(f"  10. Result: {result}")
    except ExceptionGroup as eg:
        print(f"  10. {len(eg.exceptions)} failures")
    print("10. Multi-service check: OK")


if __name__ == "__main__":
    print("=== Phase 06 Solutions ===\n")
    ex1_safe_divide_file()
    ex2_validate_age()
    ex3_bank_account()
    ex4_timing_context()
    ex5_setup_logger()
    ex6_exception_chaining()
    ex7_exceptiongroup()
    ex8_retry_backoff()
    ex9_atomic_write()
    ex10_multi_service_check()
    print("\nAll solutions passed!")
