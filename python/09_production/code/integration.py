"""IMDb Movie Database CLI — Phase 09 Integration.
Combines: argparse, logging, type hints, JSON persistence, Pydantic-like validation.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field, asdict


@dataclass
class Movie:
    title: str
    year: int
    rating: float | None = None
    genres: list[str] = field(default_factory=list)


DB_PATH = Path(__file__).parent / "imdb_movies.json"
logger = logging.getLogger("imdb_cli")


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(Path.home() / ".imdb_cli.log"),
        ],
    )


def load_movies() -> list[dict[str, Any]]:
    if not DB_PATH.exists():
        return []
    try:
        with open(DB_PATH) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Failed to load: {e}")
        return []


def save_movies(movies: list[dict[str, Any]]) -> None:
    with open(DB_PATH, "w") as f:
        json.dump(movies, f, indent=2)
    logger.info(f"Saved {len(movies)} movies")


def find_movie(movies: list[dict[str, Any]], title: str) -> dict[str, Any] | None:
    for movie in movies:
        if movie["title"].lower() == title.lower():
            return movie
    return None


# ─── CLI Commands ───

def cmd_add(args: argparse.Namespace) -> None:
    movies = load_movies()
    if find_movie(movies, args.title):
        logger.error(f"Movie '{args.title}' already exists")
        sys.exit(1)
    genres = [g.strip() for g in args.genres.split(",")] if args.genres else []
    movie = asdict(Movie(args.title, args.year, args.rating, genres))
    movies.append(movie)
    save_movies(movies)
    logger.info(f"Added '{args.title}' ({args.year})")


def cmd_list(args: argparse.Namespace) -> None:
    movies = load_movies()
    if not movies:
        logger.info("No movies found.")
        return
    movies.sort(key=lambda m: (m["year"], m["title"]))
    print(f"\n{'Title':30s} {'Year':6s} {'Rating':8s}  Genres")
    print("-" * 70)
    for m in movies:
        rating = f"{m['rating']}/10" if m["rating"] else "—"
        genres = ", ".join(m.get("genres", [])) or "—"
        print(f"{m['title']:30s} {m['year']:<6d} {rating:<8s}  {genres}")
    print(f"\nTotal: {len(movies)} movies\n")


def cmd_search(args: argparse.Namespace) -> None:
    movies = load_movies()
    query = args.query.lower()
    results = [m for m in movies if query in m["title"].lower()]
    if not results:
        logger.info(f"No movies matching '{args.query}'.")
        return
    for m in results:
        rating = f"{m['rating']}/10" if m["rating"] else "unrated"
        genres = ", ".join(m.get("genres", [])) or "—"
        print(f"  {m['title']} ({m['year']}) — {rating} [{genres}]")


def cmd_rate(args: argparse.Namespace) -> None:
    movies = load_movies()
    movie = find_movie(movies, args.title)
    if not movie:
        logger.error(f"Movie '{args.title}' not found")
        sys.exit(1)
    movie["rating"] = args.rating
    save_movies(movies)
    logger.info(f"Rated '{movie['title']}' as {args.rating}/10")


def cmd_genre(args: argparse.Namespace) -> None:
    movies = load_movies()
    query = args.genre.lower()
    results = [m for m in movies if query in [g.lower() for g in m.get("genres", [])]]
    if not results:
        logger.info(f"No movies in genre '{args.genre}'.")
        return
    results.sort(key=lambda m: -(m["rating"] or 0))
    for m in results:
        rating = f"{m['rating']}/10" if m["rating"] else "unrated"
        print(f"  {m['title']} ({m['year']}) — {rating}")


# ─── Parser ───

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="IMDb Movie Database CLI")
    parser.add_argument("--verbose", "-v", action="store_true")

    sub = parser.add_subparsers(dest="command", help="Commands")

    p_add = sub.add_parser("add", help="Add movie")
    p_add.add_argument("title")
    p_add.add_argument("year", type=int)
    p_add.add_argument("--rating", type=float)
    p_add.add_argument("--genres", help="Comma-separated genres")

    sub.add_parser("list", help="List movies")

    p_search = sub.add_parser("search", help="Search movies")
    p_search.add_argument("query")

    p_rate = sub.add_parser("rate", help="Rate movie")
    p_rate.add_argument("title")
    p_rate.add_argument("rating", type=float)

    p_genre = sub.add_parser("genre", help="Movies by genre")
    p_genre.add_argument("genre")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    setup_logging(verbose=getattr(args, "verbose", False))

    commands = {"add": cmd_add, "list": cmd_list, "search": cmd_search, "rate": cmd_rate, "genre": cmd_genre}

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
