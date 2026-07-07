"""Booking system — availability checking and log timestamps."""
from datetime import datetime, timedelta, timezone


def check_availability(bookings: list, start: datetime, end: datetime) -> bool:
    for b_start, b_end in bookings:
        if start < b_end and end > b_start:
            return False
    return True


def format_timestamp(dt: datetime = None) -> str:
    dt = dt or datetime.now(timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def days_until(target_date: str) -> int:
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
