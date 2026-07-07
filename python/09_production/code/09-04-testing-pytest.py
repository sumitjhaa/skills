"""Testing with pytest — fixtures, parametrize, monkeypatch, and coverage."""

import pytest
import json
import tempfile
import os
from pathlib import Path


# --- Production code ---

def add_movie(database: list[dict], title: str, year: int, rating: float | None = None) -> list[dict]:
    """Add a movie to the database."""
    database.append({"title": title, "year": year, "rating": rating})
    return database


def search_movies(database: list[dict], query: str) -> list[dict]:
    """Search movies by title (case-insensitive partial match)."""
    query_lower = query.lower()
    return [m for m in database if query_lower in m["title"].lower()]


def load_database(path: str) -> list[dict]:
    """Load movie database from a JSON file."""
    with open(path) as f:
        return json.load(f)


def save_database(path: str, database: list[dict]) -> None:
    """Save movie database to a JSON file."""
    with open(path, "w") as f:
        json.dump(database, f, indent=2)


# --- Fixtures ---

@pytest.fixture
def empty_db():
    """Return an empty movie database."""
    return []


@pytest.fixture
def sample_db():
    """Return a sample movie database."""
    return [
        {"title": "Inception", "year": 2010, "rating": 8.8},
        {"title": "The Matrix", "year": 1999, "rating": 8.7},
        {"title": "Interstellar", "year": 2014, "rating": 8.6},
    ]


@pytest.fixture
def temp_json_file():
    """Create a temporary JSON file with sample data."""
    db = [
        {"title": "Inception", "year": 2010, "rating": 8.8},
    ]
    tmp = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json")
    json.dump(db, tmp)
    tmp.close()
    yield tmp.name
    os.unlink(tmp.name)


# --- Tests ---

class TestAddMovie:
    def test_add_to_empty(self, empty_db):
        result = add_movie(empty_db, "Test", 2024)
        assert len(result) == 1
        assert result[0]["title"] == "Test"

    def test_add_to_existing(self, sample_db):
        result = add_movie(sample_db, "Dunkirk", 2017)
        assert len(result) == 4


class TestSearchMovies:
    def test_exact_match(self, sample_db):
        results = search_movies(sample_db, "Inception")
        assert len(results) == 1

    def test_partial_match(self, sample_db):
        results = search_movies(sample_db, "the")
        assert len(results) == 1

    def test_no_match(self, sample_db):
        results = search_movies(sample_db, "zzzzz")
        assert results == []

    @pytest.mark.parametrize("query,expected_count", [
        ("inception", 1),
        ("matrix", 1),
        ("star", 0),
    ])
    def test_parametrized_search(self, sample_db, query, expected_count):
        results = search_movies(sample_db, query)
        assert len(results) == expected_count


class TestDatabasePersistence:
    def test_save_and_load(self, temp_json_file):
        db = [{"title": "New Movie", "year": 2024, "rating": 9.0}]
        save_database(temp_json_file, db)
        loaded = load_database(temp_json_file)
        assert loaded == db

    def test_load_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_database("/nonexistent/path.json")

    def test_load_existing(self, temp_json_file):
        db = load_database(temp_json_file)
        assert len(db) == 1
        assert db[0]["title"] == "Inception"


class TestMonkeypatch:
    def test_monkeypatch_env(self, monkeypatch, sample_db):
        monkeypatch.setenv("DB_PATH", "/fake/path.json")
        assert os.environ["DB_PATH"] == "/fake/path.json"
