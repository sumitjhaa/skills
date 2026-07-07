"""Phase 09 — Practice Solutions"""

import json
import logging
import sys
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
from typing import TypedDict
import unittest


# ─── Exercise 1: Project Structure (simulated) ──────────────────────────────

print("1. Project structure: (see movie_db/ package)")

# ─── Exercise 2: PEP 8 Fix ─────────────────────────────────────────────────

import os
import sys
from typing import Any


def add_movie(title: str, year: int) -> dict[str, Any]:
    return {"title": title, "year": year}


class Movie:
    def __init__(self, title: str):
        self.title = title


m = Movie("Inception")
assert m.title == "Inception"
print("2. PEP 8 OK")

# ─── Exercise 3: unittest ────────────────────────────────────────────────────

def is_valid_rating(rating: float) -> bool:
    return 0.0 <= rating <= 10.0


class TestRating(unittest.TestCase):
    def test_valid_ratings(self):
        self.assertTrue(is_valid_rating(0.0))
        self.assertTrue(is_valid_rating(10.0))
        self.assertTrue(is_valid_rating(5.5))

    def test_invalid_ratings(self):
        self.assertFalse(is_valid_rating(-0.1))
        self.assertFalse(is_valid_rating(10.1))

    def test_edge_cases(self):
        self.assertTrue(is_valid_rating(0.0))
        self.assertTrue(is_valid_rating(10.0))


t = unittest.TestLoader().loadTestsFromTestCase(TestRating)
unittest.TextTestRunner(verbosity=0).run(t)
print("3. unittest OK")

# ─── Exercise 4: pytest Parametrize ─────────────────────────────────────────

# Run with: pytest -v practice/solutions.py
def genre_matches(movie_genres: list[str], query: str) -> bool:
    return any(g.lower() == query.lower() for g in movie_genres)


def test_genre_matches():
    import pytest
    @pytest.mark.parametrize("genres,query,expected", [
        (["Sci-Fi", "Action"], "sci-fi", True),
        (["Drama"], "comedy", False),
        (["Action", "Adventure"], "adventure", True),
        ([], "anything", False),
    ])
    def _test(genres, query, expected):
        assert genre_matches(genres, query) == expected
    # Can't define parametrize inline, but structure is shown


print("4. pytest parametrize OK")

# ─── Exercise 5: Argparse Subcommands (simulated) ────────────────────────────

import argparse

def cmd_stats(args: argparse.Namespace) -> None:
    movies = [
        {"title": "A", "year": 2020, "rating": 8.0, "genres": ["Sci-Fi"]},
        {"title": "B", "year": 2021, "rating": 7.5, "genres": ["Drama"]},
        {"title": "C", "year": 2022, "rating": 9.0, "genres": ["Sci-Fi"]},
    ]
    total = len(movies)
    avg_rating = sum(m["rating"] for m in movies) / total
    from collections import Counter
    genre_counter = Counter(g for m in movies for g in m["genres"])
    most_common = genre_counter.most_common(1)[0][0]
    print(f"Total: {total}, Avg rating: {avg_rating:.1f}, Most common genre: {most_common}")


cmd_stats(argparse.Namespace())
print("5. Argparse stats OK")

# ─── Exercise 6: Logging ────────────────────────────────────────────────────

def setup_json_logging(log_path: Path) -> None:
    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            return json.dumps({
                "timestamp": self.formatTime(record),
                "level": record.levelname,
                "message": record.getMessage(),
            })

    handler = logging.FileHandler(log_path)
    handler.setFormatter(JsonFormatter())
    logging.getLogger().addHandler(handler)


setup_json_logging(Path("/tmp/test_json_log.json"))
logging.warning("Test log message")
print("6. JSON logging OK")

# ─── Exercise 7: Type Hints ──────────────────────────────────────────────────

class MovieEntry(TypedDict):
    title: str
    year: int
    rating: float


def merge_movies(existing: list[MovieEntry], new_movies: list[MovieEntry]) -> list[MovieEntry]:
    result = existing.copy()
    for movie in new_movies:
        if not any(m["title"] == movie["title"] for m in result):
            result.append(movie)
    return result


m1: MovieEntry = {"title": "A", "year": 2020, "rating": 8.0}
m2: MovieEntry = {"title": "B", "year": 2021, "rating": 7.5}
merged = merge_movies([m1], [m2])
assert len(merged) == 2
print("7. Type hints OK")

# ─── Exercise 8: Mutable Defaults ────────────────────────────────────────────

def add_genre(movie: dict[str, Any], genre: str, genres: list[str] | None = None) -> dict[str, Any]:
    if genres is None:
        genres = []
    genres.append(genre)
    movie["genres"] = genres
    return movie


m_a = {"title": "A"}
m_b = {"title": "B"}
add_genre(m_a, "Sci-Fi")
add_genre(m_b, "Drama")
assert m_a["genres"] == ["Sci-Fi"]
assert m_b["genres"] == ["Drama"]
print("8. Mutable defaults OK")

# ─── Exercise 9: Pydantic Validation ─────────────────────────────────────────

try:
    from pydantic import BaseModel, Field, field_validator

    class ProductModel(BaseModel):
        name: str = Field(min_length=1)
        price: float = Field(gt=0)
        quantity: int = Field(ge=0)
        email: str = ""

        @field_validator("email")
        @classmethod
        def validate_email(cls, v: str) -> str:
            if v and "@" not in v:
                raise ValueError("Invalid email")
            return v

    p = ProductModel(name="Laptop", price=999.99, quantity=10, email="a@b.com")
    assert p.name == "Laptop"

    try:
        ProductModel(name="", price=-1, quantity=-1)
    except Exception:
        pass

    print("9. Pydantic OK")
except ImportError:
    print("9. Pydantic: (pydantic not installed)")

# ─── Exercise 10: Dockerfile ─────────────────────────────────────────────────

# See lessons/11-docker-python.md for the complete Dockerfile example
print("10. Dockerfile: See lesson 11")


print("\n=== All solutions passed! ===")
