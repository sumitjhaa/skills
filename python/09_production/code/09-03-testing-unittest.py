"""Testing with unittest — demo of TestCase, setUp, mock, and test discovery."""

import unittest
import json
import tempfile
import os
from unittest.mock import Mock, patch


# --- Production code ---

def load_movies(path: str) -> list[dict]:
    """Load movies from a JSON file."""
    with open(path) as f:
        return json.load(f)


def rate_movie(movies: list[dict], title: str, rating: int) -> list[dict]:
    """Update the rating of a movie by title."""
    for movie in movies:
        if movie["title"] == title:
            movie["rating"] = rating
            return movies
    raise ValueError(f"Movie '{title}' not found")


def fetch_movie_data(api_client, movie_id: str) -> dict:
    """Fetch movie data from an external API."""
    return api_client.get(f"/movies/{movie_id}")


# --- Tests ---

class TestLoadMovies(unittest.TestCase):
    """Tests for load_movies function."""

    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json")
        json.dump([{"title": "Inception", "year": 2010}], self.tmp)
        self.tmp.close()

    def tearDown(self):
        os.unlink(self.tmp.name)

    def test_load_movies(self):
        movies = load_movies(self.tmp.name)
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0]["title"], "Inception")


class TestRateMovie(unittest.TestCase):
    """Tests for rate_movie function."""

    def setUp(self):
        self.movies = [
            {"title": "Inception", "year": 2010, "rating": None},
            {"title": "The Matrix", "year": 1999, "rating": 8},
        ]

    def test_rate_existing_movie(self):
        result = rate_movie(self.movies, "Inception", 9)
        self.assertEqual(result[0]["rating"], 9)

    def test_rate_missing_movie(self):
        with self.assertRaises(ValueError):
            rate_movie(self.movies, "Nonexistent", 5)


class TestFetchMovieData(unittest.TestCase):
    """Tests for fetch_movie_data using Mock."""

    def test_fetch_movie_data(self):
        api = Mock()
        api.get.return_value = {"id": "tt1375666", "title": "Inception"}
        result = fetch_movie_data(api, "tt1375666")
        self.assertEqual(result["title"], "Inception")
        api.get.assert_called_once_with("/movies/tt1375666")


class TestSuiteSetupTeardown(unittest.TestCase):
    """Demonstrate setUpClass / tearDownClass."""

    data: list = []

    @classmethod
    def setUpClass(cls):
        cls.data = [{"title": "Test"}]

    @classmethod
    def tearDownClass(cls):
        cls.data.clear()

    def test_data_exists(self):
        self.assertEqual(len(self.data), 1)


if __name__ == "__main__":
    unittest.main()
