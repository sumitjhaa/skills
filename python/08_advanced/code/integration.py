"""Phase 08 Integration: Netflix Recommendation Engine
Combines: decorators, generators, itertools, collections, context managers, typing, functools, concurrent futures.
"""

from collections import Counter, defaultdict, deque
from contextlib import contextmanager
from functools import lru_cache
from itertools import chain, cycle, islice, product
from typing import NamedTuple, Generator
import time


class Show(NamedTuple):
    title: str
    genre: str
    year: int
    rating: float


ALL_SHOWS = [
    Show("Stranger Things", "Sci-Fi", 2016, 8.7), Show("The Crown", "Drama", 2016, 8.6),
    Show("BoJack Horseman", "Animation", 2014, 8.8), Show("Black Mirror", "Sci-Fi", 2011, 8.8),
    Show("Narcos", "Crime", 2015, 8.8), Show("The Witcher", "Fantasy", 2019, 8.2),
    Show("Dark", "Sci-Fi", 2017, 8.7), Show("Squid Game", "Thriller", 2021, 8.0),
    Show("Arcane", "Animation", 2021, 9.0), Show("Money Heist", "Crime", 2017, 8.3),
    Show("Bridgerton", "Drama", 2020, 7.3), Show("The Office", "Comedy", 2005, 8.9),
    Show("Wednesday", "Comedy", 2022, 8.1), Show("Cyberpunk: Edgerunners", "Animation", 2022, 8.6),
]


def timed(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [{func.__name__}] took {elapsed:.4f}s")
        return result
    return wrapper


@contextmanager
def recommendation_session(user_id: int):
    print(f"\n[Session start] user={user_id}")
    yield
    print(f"[Session end] user={user_id}")


def genre_generator(shows: list[Show]) -> Generator[Show, None, None]:
    for show in shows:
        yield show


@lru_cache(maxsize=128)
def cached_top(genre: str, count: int) -> tuple[Show, ...]:
    filtered = [s for s in ALL_SHOWS if s.genre.lower() == genre.lower()]
    filtered.sort(key=lambda s: s.rating, reverse=True)
    return tuple(filtered[:count])


class NetflixRecommender:
    def __init__(self, shows: list[Show]):
        self._shows = shows
        self._history: deque[Show] = deque(maxlen=10)
        self._genre_freq: Counter = Counter()
        self._watch_count: defaultdict[str, int] = defaultdict(int)

    def watch(self, show: Show) -> None:
        self._history.append(show)
        self._genre_freq[show.genre] += 1
        self._watch_count[show.title] += 1

    def recent_history(self) -> list[Show]:
        return list(self._history)

    def favorite_genre(self) -> str | None:
        if not self._genre_freq:
            return None
        return self._genre_freq.most_common(1)[0][0]

    def recommendations(self, count: int = 5) -> list[Show]:
        genre = self.favorite_genre()
        if genre is None:
            return list(islice(cycle(self._shows), count))
        recommended = list(cached_top(genre, count * 2))
        seen = {s.title for s in self._history}
        return [s for s in recommended if s.title not in seen][:count]

    def genre_explosion(self, base: str, others: list[str]) -> list[tuple[Show, Show]]:
        base_shows = [s for s in self._shows if s.genre.lower() == base.lower()]
        cross = [[s for s in self._shows if s.genre.lower() == g.lower()] for g in others]
        return list(product(base_shows, *cross))[:6]


@timed
def main():
    recommender = NetflixRecommender(ALL_SHOWS)

    print("=== Watch History ===")
    for show in ALL_SHOWS[:5]:
        recommender.watch(show)
    for show in recommender.recent_history():
        print(f"  watched: {show.title}")

    print(f"\n=== Genre Frequency ===")
    for genre, count in recommender._genre_freq.most_common(3):
        print(f"  {genre}: {count}")

    print(f"\n=== Recommendations ===")
    with recommendation_session(user_id=42):
        for r in recommender.recommendations(3):
            print(f"  recommend: {r.title} ({r.genre}, {r.rating})")

    print(f"\n=== Genre Explosion ===")
    for a, b in recommender.genre_explosion("Sci-Fi", ["Animation"]):
        print(f"  {a.title} x {b.title}")

    print(f"\n=== Cache Info ===")
    print(f"  {cached_top.cache_info()}")

    print(f"\n=== Generator ===")
    gen = genre_generator(ALL_SHOWS)
    print(f"  {next(gen).title}")
    print(f"  {next(gen).title}")


if __name__ == "__main__":
    main()
