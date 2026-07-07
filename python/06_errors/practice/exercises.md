# Phase 06: Error Handling — Practice Exercises

## 1. 🟢 Safe Division with Context
Write `safe_divide_file(input_path, output_path)` that reads numbers from a file, divides the first by the second, and writes the result. Handle `FileNotFoundError`, `ZeroDivisionError`, and `ValueError`. Use `with` for file handling.
> 💡 Hint: Nest try/except inside `with`; read both numbers, convert to float.

## 2. 🟢 Custom Validation Error
Write `validate_age(age)` that raises `ValueError` if age is not between 0 and 150. Use `assert` to verify the return value is positive.
> 💡 Hint: `raise ValueError(f"Invalid age: {age}")` for invalid ranges.

## 3. 🟡 Bank Transfer with Custom Exceptions
Create `AccountError(Exception)` as base, with `InsufficientBalanceError` and `NegativeAmountError` subclasses. Write `Account` class with `deposit()` and `withdraw()`.
> 💡 Hint: `super().__init__(f"message")` in each custom exception.

## 4. 🟡 Context Manager: Timing Block
Write a `timed()` context manager using `@contextmanager` that prints how long a block took. Accept an optional `label` parameter.
> 💡 Hint: Use `time.perf_counter()` before and after `yield`.

## 5. 🟡 Logging Setup
Write `setup_logger(name, log_file)` that creates a logger with both console (INFO) and file (DEBUG) handlers. Return the logger.
> 💡 Hint: `logger.addHandler(StreamHandler())` + `logger.addHandler(FileHandler(log_file))`.

## 6. 🟡 Exception Chaining with Context
Write `parse_settings(path)` that reads a JSON config file. If JSON parsing fails, chain it to a `RuntimeError("config loading failed")`. If file not found, let it propagate.
> 💡 Hint: `raise RuntimeError("config failed") from e` inside the except block.

## 7. 🔴 ExceptionGroup: Batch Data Validation
Write `validate_products(products)` that checks each product has `name`, `price`, `quantity`. Collect all `ValueError`s into an `ExceptionGroup`.
> 💡 Hint: Loop through products; append `ValueError(...)` to a list; `raise ExceptionGroup(...)` if any errors.

## 8. 🔴 Retry with Backoff
Write a decorator `@retry_with_backoff(max_retries=3, base_delay=1.0)` that retries on specified exceptions with exponential backoff.
> 💡 Hint: `delay = base_delay * (2 ** attempt)` for exponential backoff.

## 9. 🔴 Atomic File Update with Context Manager
Write an `atomic_write(filepath)` context manager that writes to a `.tmp` file, and on `__exit__`, renames it to the target. On exception, delete the `.tmp` file.
> 💡 Hint: In `__exit__`, use `os.replace(tmp, filepath)` on success, `os.remove(tmp)` on failure.

## 10. 🔴 Multi-Service Health Check
Write `check_endpoints(urls)` that calls multiple URLs (simulated), collects all exceptions in an `ExceptionGroup`, and returns a dict of healthy/unhealthy counts.
> 💡 Hint: Use random to simulate failures; collect `(url, error)` tuples; group by error type with `except*`.
