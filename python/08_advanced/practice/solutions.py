"""Phase 08 — Practice Solutions"""

import time
import itertools
from collections import Counter
from contextlib import contextmanager
from functools import singledispatch, wraps

# ─── Exercise 1: Timing Decorator ──────────────────────────────────────────

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{func.__name__} took {elapsed:.2f}ms")
        return result
    return wrapper


@timer
def slow_sum(n):
    return sum(range(n))


result = slow_sum(100000)
print(f"1. slow_sum result = {result}")

# ─── Exercise 2: Generator Pipeline ────────────────────────────────────────

def infinite_ints():
    n = 1
    while True:
        yield n
        n += 1


def even_only(gen):
    for n in gen:
        if n % 2 == 0:
            yield n


def take(gen, count):
    for i, val in enumerate(gen):
        if i >= count:
            break
        yield val


def square(gen):
    for n in gen:
        yield n * n


pipeline = square(take(even_only(infinite_ints()), 10))
result2 = list(pipeline)
assert result2 == [4, 16, 36, 64, 100, 144, 196, 256, 324, 400]
print(f"2. Pipeline: {result2}")

# ─── Exercise 3: Fibonacci Iterator ────────────────────────────────────────

class Fibonacci:
    def __init__(self, limit: int):
        self.limit = limit
        self.a, self.b = 1, 1

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.a > self.limit:
            raise StopIteration
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        return result


fib = list(Fibonacci(100))
assert fib == [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
print(f"3. Fibonacci: {fib}")

# ─── Exercise 4: itertools Challenge ────────────────────────────────────────

words = ["cat", "dog", "bird"]
combs = list(itertools.combinations(words, 2))
perms = list(itertools.permutations(words, 2))
assert len(combs) == 3
assert len(perms) == 6
print(f"4. Combinations: {combs}")
print(f"   Permutations: {perms}")

# ─── Exercise 5: Collection Counter ────────────────────────────────────────

def analyze_votes(votes: list[str]) -> dict:
    counter = Counter(votes)
    most_common = counter.most_common()
    winner = most_common[0][0]
    margin = most_common[0][1] - most_common[1][1]
    return {"winner": winner, "top3": most_common[:3], "margin": margin}


result5 = analyze_votes(["alice", "bob", "alice", "charlie", "bob", "alice"])
assert result5["winner"] == "alice"
assert result5["margin"] == 1
print(f"5. Votes: {result5}")

# ─── Exercise 6: Context Manager ─────────────────────────────────────────────

@contextmanager
def csv_reader(csv_string: str):
    lines = [line.split(",") for line in csv_string.strip().split("\n")]
    yield lines


csv_data = "a,b,c\n1,2,3\n4,5,6\n7,8,9"
with csv_reader(csv_data) as rows:
    row_count = len(rows) - 1  # exclude header
assert row_count == 3
print(f"6. CSV rows: {row_count}")

# ─── Exercise 7: Functools Dispatch ─────────────────────────────────────────

@singledispatch
def format_value(value) -> str:
    return "unknown"


@format_value.register(int)
def _(value: int) -> str:
    return f"int: {value}"


@format_value.register(str)
def _(value: str) -> str:
    return f"str: '{value}'"


@format_value.register(list)
def _(value: list) -> str:
    return f"list[{len(value)}]"


assert format_value(42) == "int: 42"
assert format_value("hi") == "str: 'hi'"
assert format_value([1, 2, 3]) == "list[3]"
print(f"7. Dispatch: int={format_value(42)}, str={format_value('hi')}, list={format_value([1,2,3])}")

# ─── Exercise 8: TypedDict + Protocol ────────────────────────────────────────

from typing import TypedDict, Protocol


class Song(TypedDict):
    title: str
    artist: str
    duration: float


class Playable(Protocol):
    def play(self) -> None: ...


def play_song(song: Song) -> None:
    print(f"Playing '{song['title']}' by {song['artist']} ({song['duration']}s)")


song: Song = {"title": "Bohemian Rhapsody", "artist": "Queen", "duration": 354.0}
print(f"8. Song: {song['title']}")

# ─── Exercise 9: ThreadPoolExecutor Web Checker ──────────────────────────────

from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request


def check_url(url: str) -> tuple[str, int | str]:
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            return url, resp.status
    except Exception as e:
        return url, str(e)


urls = ["https://example.com", "https://python.org", "https://github.com", "https://nonexistent.example"]
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(check_url, url): url for url in urls}
    for future in as_completed(futures):
        url = futures[future]
        try:
            url, status = future.result()
            print(f"  [{status}] {url}")
        except Exception as e:
            print(f"  [Error] {url}: {e}")
print(f"9. URL checker done")

# ─── Exercise 10: Plugin System ──────────────────────────────────────────────

class NotificationPlugin:
    registry: dict[str, type["NotificationPlugin"]] = {}

    def __init_subclass__(cls, name: str | None = None, **kwargs):
        super().__init_subclass__(**kwargs)
        final_name = name if name else cls.__name__.lower().replace("notifier", "")
        cls.name = final_name
        NotificationPlugin.registry[final_name] = cls

    def send(self, message: str) -> str:
        raise NotImplementedError


class EmailNotifier(NotificationPlugin, name="email"):
    def send(self, message: str) -> str:
        return f"[Email] {message}"


class SMSNotifier(NotificationPlugin, name="sms"):
    def send(self, message: str) -> str:
        return f"[SMS] {message}"


class PushNotifier(NotificationPlugin, name="push"):
    def send(self, message: str) -> str:
        return f"[Push] {message}"


def send_notification(method: str, message: str) -> str:
    cls = NotificationPlugin.registry.get(method)
    if not cls:
        return f"Unknown: {method}"
    return cls().send(message)


r1 = send_notification("email", "Welcome!")
r2 = send_notification("sms", "Your code is 1234")
assert "Email" in r1 and "SMS" in r2
print(f"10. Plugin: {r1}, {r2}")

# ─── Exercise 11: heapq Task Scheduler ───────────────────────────────────────

import heapq


class TaskScheduler:
    def __init__(self):
        self._heap: list[tuple[int, str]] = []
        self._counter = 0

    def add_task(self, name: str, priority: int) -> None:
        self._counter += 1
        heapq.heappush(self._heap, (priority, self._counter, name))

    def next_task(self) -> str:
        return heapq.heappop(self._heap)[2]

    def list_tasks(self) -> list[str]:
        return sorted(self._heap)


scheduler = TaskScheduler()
scheduler.add_task("Backup", 3)
scheduler.add_task("Critical alert", 1)
scheduler.add_task("Send report", 2)
assert scheduler.next_task() == "Critical alert"
print(f"11. Task scheduler: Critical alert extracted")


# ─── Exercise 12: Binary File Header Parser ──────────────────────────────────

import struct


def parse_header(data: bytes) -> dict:
    magic, version, data_len, checksum = struct.unpack_from("<IIII", data, 0)
    if magic != 0xDEADBEEF:
        raise ValueError(f"Bad magic: {magic:#010x}")
    return {"magic": magic, "version": version, "data_len": data_len, "checksum": checksum}


header_data = struct.pack("<IIII", 0xDEADBEEF, 1, 1024, 0xABCD)
parsed = parse_header(header_data)
assert parsed["version"] == 1
assert parsed["data_len"] == 1024
print(f"12. Binary header parsed: {parsed}")

try:
    parse_header(b"\x00" * 16)
    assert False, "Should raise"
except ValueError:
    print(f"12. Bad magic correctly rejected")


# ─── Exercise 13: Find a Memory Leak with gc ─────────────────────────────────

import gc


class Parent:
    def __init__(self):
        self.child = None

class Child:
    def __init__(self):
        self.parent = None


def find_leak():
    gc.collect()
    before = len([o for o in gc.get_objects() if isinstance(o, (Parent, Child))])

    p = Parent()
    c = Child()
    p.child = c
    c.parent = p

    del p, c
    gc.collect()

    after = len([o for o in gc.get_objects() if isinstance(o, (Parent, Child))])
    leaked = after - before
    print(f"  Objects before: {before}, after: {after}, leaked: {leaked}")

    # Break cycles manually
    for o in gc.get_objects():
        if isinstance(o, Parent):
            o.child = None
        if isinstance(o, Child):
            o.parent = None

    gc.collect()
    final = len([o for o in gc.get_objects() if isinstance(o, (Parent, Child))])
    assert final <= before + 1
    print(f"  After cleanup: {final}")
    return leaked > 0


result = find_leak()
print(f"13. Memory leak found: {result}")


# ─── Exercise 14: Custom Sequence with Type Validation ────────────────────────

from collections.abc import MutableSequence


class IntList(MutableSequence):
    def __init__(self, items=None):
        self._data = list(items) if items else []

    def _validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Expected int, got {type(value).__name__}")

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._validate(value)
        self._data[index] = value

    def __delitem__(self, index):
        del self._data[index]

    def __len__(self):
        return len(self._data)

    def insert(self, index, value):
        self._validate(value)
        self._data.insert(index, value)

    def __repr__(self):
        return f"IntList({self._data})"

    def sum(self) -> int:
        return sum(self._data)


il = IntList([1, 2, 3])
il.append(4)
assert list(il) == [1, 2, 3, 4]
assert il.sum() == 10
try:
    il.append("bad")
    assert False, "Should raise"
except TypeError:
    pass
print(f"14. IntList: {list(il)}, sum={il.sum()}, type validation OK")


# ─── Exercise 15: "Did you mean?" with difflib ────────────────────────────────

import difflib


def did_you_mean(input_word: str, word_list: list[str]) -> str | None:
    if input_word in word_list:
        return None
    matches = difflib.get_close_matches(input_word, word_list, n=1, cutoff=0.6)
    return matches[0] if matches else None


words = ["apple", "banana", "cherry", "date"]
assert did_you_mean("aple", words) == "apple"
assert did_you_mean("banana", words) is None
assert did_you_mean("xyz", words) is None
print(f"15. Did you mean? aple → {did_you_mean('aple', words)}, banan → {did_you_mean('banan', words)}")


# ─── Exercise 22: JSON Custom Serializer ──────────────────────────────────────

import json
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)


def custom_decoder(dct: dict) -> dict:
    for key, value in dct.items():
        if isinstance(value, str):
            try:
                dct[key] = datetime.fromisoformat(value)
            except (ValueError, TypeError):
                pass
    return dct


data = {"ts": datetime.now(), "amount": Decimal("9.99"), "id": UUID("12345678-1234-5678-1234-567812345678")}
encoded = json.dumps(data, cls=CustomEncoder)
decoded = json.loads(encoded, object_hook=custom_decoder)
assert type(decoded["ts"]).__name__ == "datetime"
print(f"22. JSON custom encode/decode OK — ts type: {type(decoded['ts']).__name__}")


# ─── Exercise 23: Structured Logger Setup ──────────────────────────────────────

import logging.config

logging.config.dictConfig({
    "version": 1,
    "formatters": {
        "simple": {"format": "%(levelname)s | %(message)s"},
        "json": {"format": '{"msg":"%(message)s"}'},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "ex23.log", "maxBytes": 1024*1024, "backupCount": 1,
            "formatter": "json",
        },
    },
    "loggers": {
        "": {"handlers": ["console", "file"], "level": "INFO"},
    },
})

log23 = logging.getLogger("ex23")
log23.info("User login", extra={"user_id": 42})
print("23. Structured logger configured — console + rotating file")


# ─── Exercise 24: CSV Dialect Sniffer ──────────────────────────────────────────

import csv, io


def parse_csv(text: str) -> list[dict]:
    dialect = csv.Sniffer().sniff(text)
    return list(csv.DictReader(io.StringIO(text), dialect=dialect))


data24 = "name|age|city\nAlice|30|NYC\nBob|25|LAX"
result24 = parse_csv(data24)
assert result24[0]["name"] == "Alice"
assert result24[1]["city"] == "LAX"
print(f"24. CSV sniffer: delimiter='|', rows={result24}")


# ─── Exercise 25: WeakValueDictionary Cache ────────────────────────────────────

import weakref


class WeakCache:
    def __init__(self):
        self._data: weakref.WeakValueDictionary[str, object] = weakref.WeakValueDictionary()

    def set(self, key: str, value: object) -> None:
        self._data[key] = value

    def get(self, key: str) -> object | None:
        return self._data.get(key)


class ExpensiveObj:
    def __init__(self, name: str):
        self.name = name


cache = WeakCache()
obj = ExpensiveObj("data")
cache.set("key", obj)
assert cache.get("key").name == "data"
del obj
import gc; gc.collect()
assert cache.get("key") is None
print("25. WeakCache: auto-eviction on GC confirmed")


# ─── Exercise 26: Mock an External API Call ────────────────────────────────────

from unittest.mock import patch
import requests


def get_user_name(user_id: int) -> str:
    resp = requests.get(f"https://api.example.com/users/{user_id}")
    return resp.json()["name"]


with patch("requests.get") as mock_get:
    mock_get.return_value.json.return_value = {"name": "Alice"}
    name = get_user_name(1)
    assert name == "Alice"
    mock_get.assert_called_once_with("https://api.example.com/users/1")
print("26. Mocked API call: get_user_name(1) → Alice")


# ─── Exercise 16: contextlib — ExitStack + suppress ────────────────────────────

from contextlib import ExitStack, suppress
from pathlib import Path
import tempfile, shutil

def safe_process_files(filenames: list[str]) -> list[str]:
    contents = []
    with ExitStack() as stack:
        for fname in filenames:
            with suppress(FileNotFoundError):
                f = stack.enter_context(open(fname))
                contents.append(f.read())
    return contents


tmp16 = Path(tempfile.mkdtemp())
(tmp16 / "exists.txt").write_text("data1\n")
(tmp16 / "also_exists.txt").write_text("data2\n")
result16 = safe_process_files([
    str(tmp16 / "exists.txt"),
    str(tmp16 / "missing.txt"),
    str(tmp16 / "also_exists.txt"),
])
assert len(result16) == 2
assert b"data1" in result16[0].encode()
print(f"16. contextlib: {len(result16)} files processed")
shutil.rmtree(tmp16)


# ─── Exercise 17: functools — cached_property + cache ─────────────────────────

from functools import cached_property, cache
import time

class AnalysisReport:
    def __init__(self, data: str):
        self.data = data

    @cached_property
    def summary(self) -> str:
        time.sleep(0.1)
        return f"Summary of {self.data[:10]}..."

    @cached_property
    def full_report(self) -> str:
        return f"{self.summary}\n---\nFull details for {self.data}"

    @staticmethod
    @cache
    def compress(data: str) -> str:
        return f"compressed({len(data)}→{len(data)//2})"


report = AnalysisReport("very large dataset " * 100)
t1 = time.time()
s1 = report.summary
t1 = time.time() - t1
t2 = time.time()
s2 = report.summary
t2 = time.time() - t2
assert s1 == s2
assert t2 < t1 / 2  # Second call should be much faster (cached)
print(f"17. functools: summary first={t1:.3f}s, cached={t2:.3f}s")


# ─── Exercise 18: itertools — batched + pairwise + islice ──────────────────────

from itertools import batched, pairwise, islice

def process_numbers(nums):
    batches = batched(nums, 5)
    first_two = islice(batches, 2)
    return [list(pairwise(b)) for b in first_two]


result18 = process_numbers(range(1, 21))
assert result18 == [[(1,2),(2,3),(3,4),(4,5)], [(6,7),(7,8),(8,9),(9,10)]]
print(f"18. itertools: {result18}")


# ─── Exercise 19: typing — NewType + Annotated + Literal ──────────────────────

from typing import NewType, Annotated, Literal

Port = NewType('Port', int)

def configure(env: Literal["dev", "prod"], port: Port) -> dict:
    if not (1024 <= port <= 65535):
        raise ValueError(f"Port {port} out of range (1024-65535)")
    return {"env": env, "port": port}


cfg19 = configure("dev", Port(8080))
assert cfg19["port"] == 8080
try:
    configure("dev", Port(80))
    assert False, "Should raise"
except ValueError:
    pass
print(f"19. typing: {cfg19}, invalid port rejected")


# ─── Exercise 20: pathlib — rglob + with_suffix + stat ────────────────────────

import pathlib, shutil, tempfile

def backup_and_report(directory: str) -> int:
    total = 0
    src_dir = pathlib.Path(directory)
    for f in src_dir.rglob("*.txt"):
        bak = f.with_suffix(".txt.bak")
        shutil.copy2(f, bak)
        st = f.stat()
        print(f"  {f.name}: {st.st_size}B -> {bak.name}: {st.st_size}B")
        total += st.st_size
    return total


tmp20 = pathlib.Path(tempfile.mkdtemp())
(tmp20 / "a.txt").write_text("hello")
(tmp20 / "sub").mkdir()
(tmp20 / "sub" / "b.txt").write_text("world")
total20 = backup_and_report(str(tmp20))
assert total20 > 0
print(f"20. pathlib: Total backed up = {total20}B")
shutil.rmtree(tmp20)


# ─── Exercise 21: re — named groups + lookahead ──────────────────────────────

import re

def parse_access_log(log_lines: list[str]) -> list[dict]:
    pat = re.compile(r"""
        (?P<ip>\d+\.\d+\.\d+\.\d+) \s+ \S+ \s+ \S+ \s+
        \[(?P<ts>[^\]]+)\] \s+
        "(?P<method>GET|POST|PUT|DELETE) \s+ (?P<path>/\S*) .*?" \s+
        (?P<status>\d{3})
    """, re.VERBOSE)
    result = []
    for line in log_lines:
        m = pat.search(line)
        if m and m.group("status").startswith(("2", "3")):
            result.append(m.groupdict())
    return result


lines21 = [
    '192.168.1.1 - - [10/Jan/2024:13:55:36] "GET /api/users HTTP/1.1" 200 2326',
    '10.0.0.1 - - [10/Jan/2024:13:55:37] "POST /api/login HTTP/1.1" 500 123',
    '10.0.0.2 - - [10/Jan/2024:13:55:38] "GET /health HTTP/1.1" 301 0',
]
parsed21 = parse_access_log(lines21)
assert len(parsed21) == 2  # 200 and 301, not 500
print(f"21. re: {len(parsed21)} parsed entries (200 & 301), {lines21[1]} excluded")


print("\n=== All solutions passed! ===")
