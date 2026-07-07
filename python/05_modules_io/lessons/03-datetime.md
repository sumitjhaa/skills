# 📅 Datetime
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** How to work with dates, times, timedeltas, formatting, parsing, and timezone-aware datetimes.

> 💡 **TL;DR — The whole point:** Time is messy — `datetime` gives you tools to handle dates, durations, formatting, and timezones without going crazy.

## 🔗 Why This Matters
Math/Random gave you numbers. Real systems deal with time: booking systems need availability checks, logs need timestamps, APIs need timezone-aware dates.

## The Concept
The `datetime` module provides:
- `datetime` — date + time (most common)
- `date` — date only
- `time` — time only
- `timedelta` — duration / arithmetic
- `timezone` — timezone info (use `pytz` or `zoneinfo` in Python 3.9+)

Python datetimes are either **naive** (no timezone) or **aware** (with timezone). Always prefer aware datetimes for production systems.

## Code Example

```python
"""Booking system — availability checking and log timestamps."""

from datetime import datetime, timedelta, timezone


def check_availability(bookings: list, start: datetime, end: datetime) -> bool:
    """Check if a time slot is available (no overlapping bookings)."""
    for b_start, b_end in bookings:
        if start < b_end and end > b_start:
            return False
    return True


def format_timestamp(dt: datetime = None) -> str:
    """Format a datetime as an ISO-like log timestamp."""
    dt = dt or datetime.now(timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def days_until(target_date: str) -> int:
    """Calculate days from now until a date string."""
    target = datetime.strptime(target_date, "%Y-%m-%d").date()
    return (target - datetime.now().date()).days


bookings = [
    (datetime(2024, 6, 1, 10, 0), datetime(2024, 6, 1, 12, 0)),
    (datetime(2024, 6, 1, 14, 0), datetime(2024, 6, 1, 16, 0)),
]

print(f"Available 11-13? {check_availability(bookings, datetime(2024, 6, 1, 11, 0), datetime(2024, 6, 1, 13, 0))}")
print(f"Available 15-17? {check_availability(bookings, datetime(2024, 6, 1, 15, 0), datetime(2024, 6, 1, 17, 0))}")
print(f"Log: {format_timestamp()}")
print(f"Days to Christmas: {days_until('2024-12-25')}")
```

## 🔍 How It Works
- `datetime.now()` returns current local time (naive)
- `datetime.now(timezone.utc)` returns UTC (aware)
- `timedelta` supports `+`, `-`, `*`, `//` for date arithmetic
- `strftime` / `strptime` use C `strftime` format codes
- Always store UTC in databases; convert to local time for display

## ⚠️ Common Pitfall
Ignoring timezones. A naive datetime is ambiguous — "10:00" could be UTC, EST, or anything. Always use aware datetimes in production.

## 🧠 Memory Aid
**"strftime = string from time, strptime = string parse time"**: `f` for "format" (dt→string), `p` for "parse" (string→dt).

## 🏃 Try It
Write a function `working_days_between(start, end)` that counts the number of weekdays between two dates (exclude weekends).

## 🔗 Related
- [Math & Random →](./02-math-random.md)
- [File I/O →](./04-file-io.md)

## ➡️ Next
[File I/O](./04-file-io.md)
