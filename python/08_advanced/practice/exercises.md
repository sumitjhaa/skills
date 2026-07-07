# 🏋️ Practice Exercises — Phase 08: Advanced Python

## Exercise 1: Timing Decorator (🟢)
Write a decorator `@timer` that prints how long a function took to run (in milliseconds).

```python
@timer
def slow_sum(n):
    return sum(range(n))

slow_sum(100000)  # e.g., "slow_sum took 3.21ms"
```

## Exercise 2: Generator Pipeline (🟢)
Write a pipeline that:
1. Generates infinite integers starting from 1
2. Filters to keep only even numbers
3. Takes the first 10 and squares them

Use generator functions (no lists).

## Exercise 3: Custom Iterator (🟡)
Write a `Fibonacci` class that implements the iterator protocol and yields Fibonacci numbers up to a given limit.

```python
for n in Fibonacci(100):
    print(n)  # 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89
```

## Exercise 4: itertools Challenge (🟡)
Given a list of words, use `itertools` to:
- Find all unique 2-word combinations (order doesn't matter)
- Find all unique 2-word permutations (order matters)

```python
words = ["cat", "dog", "bird"]
# combinations: ("cat", "dog"), ("cat", "bird"), ("dog", "bird")
```

## Exercise 5: Collection Counter (🟡)
Write a function `analyze_votes(votes: list[str]) -> dict` that uses `Counter` to:
- Find the winner (most votes)
- Find the top 3 candidates
- Compute the difference between first and second place

```python
analyze_votes(["alice", "bob", "alice", "charlie", "bob", "alice"])
# returns {winner: "alice", top3: [...], margin: 1}
```

## Exercise 6: Context Manager for File Processing (🟡)
Write a context manager using `@contextmanager` that opens a file, yields a csv reader, and ensures the file is closed. Use it to count rows in a CSV-like string.

## Exercise 7: Functools Dispatch (🟡)
Write a function `format_value` using `singledispatch` that:
- For `int`: returns `"int: {n}"`
- For `str`: returns `"str: '{s}'"`
- For `list`: returns `"list[{len}]"`
- For anything else: returns `"unknown"`

## Exercise 8: TypedDict + Protocol (🟡)
Define a `Song` TypedDict with keys `title: str`, `artist: str`, `duration: float`. Then create a `Playable` Protocol with a method `play() -> None`. Write a function `play_song(song: Song)` that takes a Song and prints its info.

## Exercise 9: ThreadPoolExecutor Web Checker (🔴)
Write a function `check_urls(urls: list[str])` that uses `ThreadPoolExecutor` to fetch HTTP status codes for 10 URLs. Use `as_completed` to print results as they arrive. Handle connection errors gracefully.

## Exercise 10: Plugin System with \_\_init\_subclass\_\_ (🔴)
Create a `NotificationPlugin` base class with `__init_subclass__` that auto-registers subclasses by name. Implement `EmailNotifier`, `SMSNotifier`, `PushNotifier`. Write a `send_notification(method, message)` factory function that looks up the plugin by name.

---

## Phase 08 Extensions — New Lessons 15-19

## Exercise 11: heapq Task Scheduler (🟡)
Build a `TaskScheduler` class using `heapq` that supports:
- `add_task(name, priority)` — adds a task
- `next_task()` — pops the highest priority task
- `list_tasks()` — returns all tasks sorted by priority (without modifying heap)

```python
scheduler = TaskScheduler()
scheduler.add_task("Backup", 3)
scheduler.add_task("Critical alert", 1)
scheduler.add_task("Send report", 2)
assert scheduler.next_task() == "Critical alert"
```

## Exercise 12: Binary File Header Parser (🟡)
Use `struct` to parse a simple binary header format:
- Bytes 0-3: magic number (`<I`, must be `0xDEADBEEF`)
- Bytes 4-7: version (`<I`)
- Bytes 8-11: data length (`<I`)
- Bytes 12-15: checksum (`<I`)

Write `parse_header(data: bytes) -> dict` that returns `{"magic": ..., "version": ..., "data_len": ..., "checksum": ...}`. Raise `ValueError` if magic doesn't match.

## Exercise 13: Find a Memory Leak with gc (🔴)
Write a function `find_leak()` that:
1. Creates a circular reference between two classes `Parent` and `Child` (each holds a reference to the other)
2. Deletes all external references
3. Uses `gc.get_objects()` and `gc.get_referrers()` to find the leaked objects
4. Breaks the cycle and calls `gc.collect()`
5. Verifies the objects are gone

```python
found = find_leak()
# Should print both Parent and Child instances, then confirm cleanup
```

## Exercise 14: Custom Sequence with Type Validation (🟡)
Create `IntList(MutableSequence)` that:
- Only allows `int` values (raises `TypeError` on insert/set with non-int)
- Implements all required MutableSequence methods
- Has a `sum()` method that returns the sum of all elements

```python
il = IntList([1, 2, 3])
il.append(4)
assert list(il) == [1, 2, 3, 4]
assert il.sum() == 10
try:
    il.append("bad")
except TypeError:
    pass  # OK
```

## Exercise 15: "Did you mean?" with difflib (🟡)
Write a function `did_you_mean(input_word: str, word_list: list[str]) -> str | None` that:
- Uses `difflib.get_close_matches` with cutoff 0.6
- Returns the best match if any, otherwise `None`
- If the input matches exactly, returns `None` (no suggestion needed)

```python
words = ["apple", "banana", "cherry", "date"]
assert did_you_mean("aple", words) == "apple"
assert did_you_mean("banana", words) is None   # exact match
assert did_you_mean("xyz", words) is None      # no close match

---

## Phase 08 Advanced Nitigrities — New Lessons 20-25

## Exercise 16: contextlib — ExitStack + suppress (🟡)
Write a function `safe_process_files(filenames: list[str]) -> list[str]` that:
1. Uses `ExitStack` to open multiple files
2. Uses `suppress(FileNotFoundError)` so missing files are skipped silently
3. Returns the content of all successfully opened files

```python
result = safe_process_files(["exists.txt", "missing.txt", "also_exists.txt"])
# Only the two existing files' contents are returned
```

## Exercise 17: functools — cached_property + cache (🟡)
Create an `AnalysisReport` class with:
- A `@cached_property` called `summary` that computes and caches an expensive summary (simulate with `time.sleep(0.1)`)
- A `@cached_property` called `full_report` that depends on `summary` and extends it
- A `@cache`-decorated `@staticmethod` called `compress(data: str) -> str` that simulates compression

```python
report = AnalysisReport("large dataset")
first = report.summary    # Takes 0.1s
second = report.summary    # Instant (cached)
```

## Exercise 18: itertools — batched + pairwise + islice (🟡)
Write a pipeline that:
1. Generates numbers from 1 to 20
2. Groups them into batches of 5
3. For each batch, computes pairwise differences between consecutive numbers
4. Uses `islice` to take only the first 2 batches

```python
result = process_numbers(range(1, 21))
# result: [[1,1,1,1], [1,1,1,1]]  (first 2 batches, each with 4 pairwise diffs)
```

## Exercise 19: typing — NewType + Annotated + Literal (🟡)
Create a type-safe configuration validator:
- Define `Port = NewType('Port', int)` — only valid ports 1024-65535
- Use `Annotated` to add metadata "valid_port" to Port
- Write a function `configure(env: Literal["dev","prod"], port: Port) -> dict`
- Validate that port is between 1024-65535 and return a config dict

```python
cfg = configure("dev", Port(8080))   # OK
try:
    configure("dev", Port(80))       # Should raise ValueError
except ValueError:
    pass
```

## Exercise 20: pathlib — rglob + with_suffix + stat (🟡)
Write a function `backup_and_report(directory: str)` that:
1. Uses `rglob("*.txt")` to find all .txt files
2. Copies each to a .txt.bak file using `shutil.copy2`
3. Uses `stat()` to print old size → new size for each file
4. Returns the total bytes backed up

```python
total = backup_and_report("/tmp/mydata")
# Output: "file1.txt: 100B → 100B", "Total: 200B"
```

## Exercise 21: re — named groups + lookahead (🔴)
Write a function `parse_access_log(log_lines: list[str]) -> list[dict]` that:
1. Compiles a regex with `re.VERBOSE` and named groups for IP, timestamp, method, path, status, size
2. Uses `finditer` to avoid building giant match lists
3. Filters out lines where status is NOT followed by a 2xx or 3xx code (use lookahead)

```python
lines = [
    '192.168.1.1 - - [10/Jan/2024:13:55:36] "GET /api/users HTTP/1.1" 200 2326',
    '10.0.0.1 - - [10/Jan/2024:13:55:37] "POST /api/login HTTP/1.1" 500 123',
]
result = parse_access_log(lines)
# Only the 200-status line is included
```
```

---

## Phase 08 Advanced Nitigrities — New Lessons 26-30

## Exercise 22: JSON Custom Serializer (🟡)
Write a `CustomEncoder` class that serializes `datetime`, `Decimal`, and `UUID` to JSON. Then write a `custom_decoder` function for `json.loads(object_hook=...)` that restores `datetime` from ISO strings.

```python
data = {"ts": datetime.now(), "amount": Decimal("9.99"), "id": UUID("12345678-1234-5678-1234-567812345678")}
encoded = json.dumps(data, cls=CustomEncoder)
decoded = json.loads(encoded, object_hook=custom_decoder)
assert type(decoded["ts"]).__name__ == "datetime"
```

## Exercise 23: Structured Logger Setup (🟡)
Use `logging.config.dictConfig` to configure a logger with two handlers:
- Console handler with `"%(levelname)s | %(message)s"` format
- Rotating file handler with JSON format (`'{"msg":"%(message)s"}'`)
Set root logger to INFO. Log a test message with `extra={"user_id": 42}`.

```python
# After config, this should print to console AND write JSON to file
logger.info("User login", extra={"user_id": 42})
```

## Exercise 24: CSV Dialect Sniffer (🟡)
Write a function `parse_csv(text: str) -> list[dict]` that:
1. Uses `csv.Sniffer().sniff()` to detect delimiter and dialect
2. Uses `csv.DictReader` with the detected dialect
3. Returns the parsed rows as a list of dicts

```python
data = "name|age|city\nAlice|30|NYC\nBob|25|LAX"
result = parse_csv(data)
assert result[0]["name"] == "Alice"
```

## Exercise 25: WeakValueDictionary Cache (🔴)
Implement a `WeakCache` class that stores objects by key using `weakref.WeakValueDictionary`. When an object is garbage collected, it should automatically disappear from the cache.

```python
class ExpensiveObj:
    def __init__(self, name): self.name = name

cache = WeakCache()
obj = ExpensiveObj("data")
cache.set("key", obj)
assert cache.get("key").name == "data"
del obj  # Object is now eligible for GC
import gc; gc.collect()
assert cache.get("key") is None  # Auto-evicted
```

## Exercise 26: Mock an External API Call (🟡)
Write a function `get_user_name(user_id: int) -> str` that calls `requests.get(f"https://api.example.com/users/{user_id}")` and returns `response.json()["name"]`. Then write a test using `@patch("requests.get")` that mocks the API call without making a real HTTP request.

```python
# Test should not make real HTTP requests
with patch("requests.get") as mock_get:
    mock_get.return_value.json.return_value = {"name": "Alice"}
    name = get_user_name(1)
    assert name == "Alice"
```
