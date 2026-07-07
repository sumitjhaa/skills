"""Mutable, identity & copy — is vs ==, mutable defaults, shallow vs deep copy, __slots__."""

import copy
import sys


# --- is vs == ---

def identity_demo() -> None:
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a

    print("--- is vs == ---")
    print(f"a == b: {a == b}")  # True (same value)
    print(f"a is b: {a is b}")  # False (different objects)
    print(f"a is c: {a is c}")  # True (same object)

    # Integer interning
    x = 256
    y = 256
    print(f"x is y (256): {x is y}")  # True (interned)

    x = 257
    y = 257
    print(f"x is y (257): {x is y}")  # False (not interned)


# --- Mutable default argument trap ---

def add_movie_bad(title: str, movie_list: list = []) -> list:
    """Bad — mutable default persists across calls."""
    movie_list.append(title)
    return movie_list


def add_movie_good(title: str, movie_list: list | None = None) -> list:
    """Good — None default, create new list each call."""
    if movie_list is None:
        movie_list = []
    movie_list.append(title)
    return movie_list


def mutable_default_demo() -> None:
    print("\n--- Mutable default arguments ---")
    print("Bad version (shared list):")
    print(f"  First:  {add_movie_bad('Inception')}")
    print(f"  Second: {add_movie_bad('Matrix')}")  # Bug! Both present

    print("Good version (new list each call):")
    print(f"  First:  {add_movie_good('Inception')}")
    print(f"  Second: {add_movie_good('Matrix')}")


# --- Shallow vs deep copy ---

def copy_demo() -> None:
    print("\n--- Shallow vs deep copy ---")
    original = [{"title": "Inception", "rating": 8.8}, {"title": "Matrix", "rating": 8.7}]

    shallow = copy.copy(original)
    deep = copy.deepcopy(original)

    # Modify a nested dict
    shallow[0]["rating"] = 9.0  # Affects original!
    deep[1]["rating"] = 10.0    # Does not affect original

    print(f"Original: {original}")
    print(f"Shallow:  {shallow}")
    print(f"Deep:     {deep}")


# --- __slots__ ---

class MovieWithSlots:
    """Uses __slots__ for memory efficiency."""
    __slots__ = ("title", "year", "rating")

    def __init__(self, title: str, year: int, rating: float | None = None) -> None:
        self.title = title
        self.year = year
        self.rating = rating


class MovieRegular:
    """Regular class without __slots__."""

    def __init__(self, title: str, year: int, rating: float | None = None) -> None:
        self.title = title
        self.year = year
        self.rating = rating


def slots_demo() -> None:
    print("\n--- __slots__ memory comparison ---")
    regular = MovieRegular("Test", 2020)
    slots = MovieWithSlots("Test", 2020)

    print(f"Regular instance __dict__ size: {sys.getsizeof(regular.__dict__)} bytes")
    try:
        slots.__dict__  # type: ignore
    except AttributeError:
        print("Slots instance has no __dict__ (more memory efficient)")

    # Can't add new attributes to slots class
    try:
        slots.extra = "forbidden"  # type: ignore
    except AttributeError as e:
        print(f"Cannot add attribute to __slots__ class: {e}")


def main() -> None:
    identity_demo()
    mutable_default_demo()
    copy_demo()
    slots_demo()


if __name__ == "__main__":
    main()
