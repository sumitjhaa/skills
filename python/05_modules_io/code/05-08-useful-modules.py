"""hashlib, statistics, pprint — password hashing, data analysis, debug output."""
import hashlib
import statistics
from pprint import pprint
from io import StringIO


def hash_password(password: str) -> str:
    salt = "static_salt"
    return hashlib.sha256((password + salt).encode()).hexdigest()


def analyze_survey(data: list) -> dict:
    return {"mean": round(statistics.mean(data), 2), "median": statistics.median(data), "stdev": round(statistics.stdev(data), 2) if len(data) > 1 else 0, "min": min(data), "max": max(data)}


def process_data(data: str) -> str:
    buf = StringIO(data)
    lines = [line.strip().upper() for line in buf if line.strip()]
    return "\n".join(lines)


stored = hash_password("my_secure_password")
print(f"Hashed: {stored[:20]}...")

ratings = [4, 5, 3, 4, 5, 2, 4, 5, 5, 4]
pprint(analyze_survey(ratings))

print(f"Processed:\n{process_data('  hello  \n  world  \n\n  python  ')}")
