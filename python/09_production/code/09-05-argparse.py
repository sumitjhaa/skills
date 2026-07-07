"""Argparse demo — CLI tool for managing a movie database.

Usage:
    python 09-05-argparse.py add "Inception" --year 2010 --rating 8.8
    python 09-05-argparse.py list
    python 09-05-argparse.py search "matrix"
    python 09-05-argparse.py rate "Inception" 9
"""

import argparse
import json
import os
import sys

DB_PATH = os.path.join(os.path.dirname(__file__), "movies.json")


def load_db() -> list[dict]:
    """Load movies from JSON file."""
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH) as f:
        return json.load(f)


def save_db(movies: list[dict]) -> None:
    """Save movies to JSON file."""
    with open(DB_PATH, "w") as f:
        json.dump(movies, f, indent=2)


def cmd_add(args: argparse.Namespace) -> None:
    """Add a new movie."""
    movies = load_db()
    movies.append({"title": args.title, "year": args.year, "rating": args.rating})
    save_db(movies)
    print(f"Added '{args.title}' ({args.year})")


def cmd_list(args: argparse.Namespace) -> None:
    """List all movies."""
    movies = load_db()
    if not movies:
        print("No movies found.")
        return
    for m in movies:
        rating = f"{m['rating']}/10" if m["rating"] else "unrated"
        print(f"  {m['title']} ({m['year']}) — {rating}")


def cmd_search(args: argparse.Namespace) -> None:
    """Search movies by title."""
    movies = load_db()
    query = args.query.lower()
    results = [m for m in movies if query in m["title"].lower()]
    if not results:
        print(f"No movies matching '{args.query}'.")
        return
    for m in results:
        rating = f"{m['rating']}/10" if m["rating"] else "unrated"
        print(f"  {m['title']} ({m['year']}) — {rating}")


def cmd_rate(args: argparse.Namespace) -> None:
    """Rate a movie."""
    movies = load_db()
    for m in movies:
        if m["title"].lower() == args.title.lower():
            m["rating"] = args.rating
            save_db(movies)
            print(f"Rated '{m['title']}' as {args.rating}/10")
            return
    print(f"Movie '{args.title}' not found.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Movie Database CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # add
    add_parser = subparsers.add_parser("add", help="Add a new movie")
    add_parser.add_argument("title", help="Movie title")
    add_parser.add_argument("--year", type=int, required=True, help="Release year")
    add_parser.add_argument("--rating", type=float, choices=[i / 2 for i in range(0, 21)], help="Rating 0.0-10.0")

    # list
    subparsers.add_parser("list", help="List all movies")

    # search
    search_parser = subparsers.add_parser("search", help="Search movies")
    search_parser.add_argument("query", help="Search query")

    # rate
    rate_parser = subparsers.add_parser("rate", help="Rate a movie")
    rate_parser.add_argument("title", help="Movie title")
    rate_parser.add_argument("rating", type=float, choices=[i / 2 for i in range(0, 21)], help="Rating 0.0-10.0")

    args = parser.parse_args()

    if args.command == "add":
        cmd_add(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "rate":
        cmd_rate(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
