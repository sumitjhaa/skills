"""PEP 8 style guide examples — before and after formatting."""

import os
import sys
from typing import Dict, List, Optional


class Movie:
    """Represents a movie with title, year, and rating."""

    def __init__(self, title: str, year: int, rating: Optional[float] = None) -> None:
        self.title = title
        self.year = year
        self.rating = rating

    def __repr__(self) -> str:
        return f"Movie({self.title!r}, {self.year}, {self.rating})"


def filter_by_year(movies: List[Movie], year: int) -> List[Movie]:
    """Return movies released in the given year."""
    return [m for m in movies if m.year == year]


def average_rating(movies: List[Movie]) -> float:
    """Calculate average rating of a list of movies."""
    ratings = [m.rating for m in movies if m.rating is not None]
    if not ratings:
        return 0.0
    return sum(ratings) / len(ratings)


def main() -> None:
    movies = [
        Movie("The Shawshank Redemption", 1994, 9.3),
        Movie("The Godfather", 1972, 9.2),
        Movie("The Dark Knight", 2008, 9.0),
        Movie("Pulp Fiction", 1994, 8.9),
    ]
    print(f"Average rating: {average_rating(movies):.1f}")
    print(f"Movies from 1994: {filter_by_year(movies, 1994)}")


if __name__ == "__main__":
    main()
