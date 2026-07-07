"""Type checking with mypy — Protocol, TypedDict, generics, and strict mode.

Run: mypy --strict 09-07-type-checking.py
"""

from typing import Protocol, TypeVar, Generic, TypedDict, Sequence


# --- Protocol (structural subtyping) ---

class Drawable(Protocol):
    def draw(self) -> str: ...


def render(obj: Drawable) -> str:
    return obj.draw()


class Circle:
    def draw(self) -> str:
        return "Circle"


class Square:
    def draw(self) -> str:
        return "Square"


class NotDrawable:
    def paint(self) -> str:
        return "Paint"


# --- TypedDict ---

class MovieDict(TypedDict):
    title: str
    year: int
    rating: float | None


def movie_summary(movie: MovieDict) -> str:
    rating = movie["rating"]
    rating_str = f"{rating}/10" if rating else "unrated"
    return f"{movie['title']} ({movie['year']}) — {rating_str}"


# --- Generics ---

T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T | None:
        return self._items.pop() if self._items else None


def first(items: Sequence[T]) -> T | None:
    return items[0] if items else None


# --- Type aliases ---

MovieList = list[MovieDict]


def filter_by_year(movies: MovieList, year: int) -> MovieList:
    return [m for m in movies if m["year"] == year]


# --- Main ---

def main() -> None:
    # Protocol
    print(render(Circle()))
    print(render(Square()))
    # render(NotDrawable())  # mypy would error here

    # TypedDict
    movie: MovieDict = {"title": "Inception", "year": 2010, "rating": 8.8}
    print(movie_summary(movie))

    # Generics
    s: Stack[int] = Stack()
    s.push(1)
    s.push(2)
    print(s.pop())

    # Sequence
    print(first([10, 20, 30]))

    # MovieList type alias
    movies: MovieList = [
        {"title": "The Matrix", "year": 1999, "rating": 8.7},
    ]
    print(filter_by_year(movies, 1999))


if __name__ == "__main__":
    main()
