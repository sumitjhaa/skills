# 🏋️ Practice Exercises — Phase 09: Production Python

## Exercise 1: Project Structure (🟢)
Create a package called `movie_db` with:
```
movie_db/
├── __init__.py     # exports: Movie, add_movie, search_movies
├── models.py       # Movie dataclass
├── db.py           # load/save JSON functions
└── cli.py          # main() with argparse
```

## Exercise 2: PEP 8 Fix (🟢)
Fix the PEP 8 violations in this code:
```python
import os,sys
from typing import *
def addMovie(title,year):
  return{"title":title,"year":year}
class movie:
  def __init__(self,t):
    self.title=t
```

## Exercise 3: unittest (🟡)
Write a `unittest.TestCase` for `is_valid_rating(rating: float) -> bool` that returns `True` if rating is between 0.0 and 10.0. Test: 0.0, 10.0, -0.1, 10.1.

## Exercise 4: pytest Parametrize (🟡)
Write a pytest test using `@pytest.mark.parametrize` for `genre_matches(movie_genres: list[str], query: str) -> bool` that checks if any genre matches (case-insensitive).

## Exercise 5: Argparse Subcommands (🟡)
Extend the IMDb CLI with a `stats` command that prints: total movies, average rating, most common genre, movies per year (recent 5 years).

## Exercise 6: Logging (🟡)
Add a JSON log formatter to the IMDb CLI that outputs `{"timestamp": ..., "level": ..., "message": ...}`. Configure a separate file handler for JSON logs.

## Exercise 7: Type Hints (🟡)
Add complete type hints to this function using `TypedDict` and `list`:
```python
def merge_movies(existing, new_movies):
    result = existing.copy()
    for movie in new_movies:
        if not any(m["title"] == movie["title"] for m in result):
            result.append(movie)
    return result
```

## Exercise 8: Mutable Defaults (🟡)
Identify and fix mutable default bugs:
```python
def add_genre(movie, genre, genres=[]):
    genres.append(genre)
    movie["genres"] = genres
    return movie
```

## Exercise 9: Pydantic Validation (🔴)
Create a `ProductModel` with name (min 1 char), price (gt 0), quantity (ge 0). Add a `@field_validator` for email. Test both valid and invalid data.

## Exercise 10: Dockerfile (🔴)
Write a multi-stage Dockerfile for a Python FastAPI app. Stage 1: build deps. Stage 2: runtime with non-root user. Include `.dockerignore` for `__pycache__`, `.venv`, `.env`, `.git`. Add health check endpoint.

## Exercise 11: Docker Compose (🟡)
Write a `docker-compose.yml` for an e-commerce stack with three services:
- `api`: builds from `./api`, exposes port 8000, depends on `db`
- `db`: uses `postgres:16-alpine`, sets POSTGRES env vars, mounts a named volume `pgdata`
- `cache`: uses `redis:7-alpine`, exposes port 6379

Mount the local `./api` directory into the `api` container for hot-reload. Add a health check for the API.

## Exercise 12: Pre-commit Config (🟡)
Create a `.pre-commit-config.yaml` that runs:
- `ruff` (lint + format)
- `mypy` (with `--strict`)
- `trailing-whitespace` and `end-of-file-fixer` from `pre-commit-hooks`

Then write a Makefile with `lint`, `typecheck`, `test`, `clean`, and `help` targets. The `help` target should auto-generate descriptions from comments.

## Exercise 13: Pydantic Settings & Validation (🟡)
Create a `Settings` model using `pydantic_settings.BaseSettings` with:
- `app_name` (default "Inventory API")
- `database_url` (validated to start with "postgresql" or "sqlite")
- `max_items_per_page` (int, ge=1, le=100, default=50)
- `feature_flags` (set[str], validated to only contain known flags)

Then create a `BulkOrderRequest` model with:
- `orders` (list of `OrderItem`, min_length=1)
- `warehouse_code` (pattern like `WH-[A-Z]{3}`)
- A `@model_validator` that rejects orders with total cost over $50,000

## Exercise 14: HTTP Client with Retries (🟡)
Write a `WeatherAPIClient` class using `httpx.Client` that:
- Takes `api_key` and `base_url` in the constructor
- Has a `get_forecast(city: str, days: int) -> dict` method with 3 retry attempts and exponential backoff
- Sets a 10-second total timeout with a 5-second connect timeout
- Raises a custom `WeatherAPIError` on non-200 responses

Then write an async `BulkWeatherClient` that uses `httpx.AsyncClient` and `asyncio.gather` to fetch forecasts for 5 cities concurrently.

## Exercise 15: Advanced pytest Fixtures (🔴)
Write a complete test suite for this `ShoppingCart` class:

```python
from dataclasses import dataclass, field

@dataclass
class Item:
    sku: str
    name: str
    price: float
    quantity: int = 1

class ShoppingCart:
    def __init__(self):
        self.items: list[Item] = {}
        self._discount_code: str | None = None

    def add_item(self, item: Item) -> None: ...
    def remove_item(self, sku: str) -> None: ...
    def apply_discount(self, code: str) -> None: ...
    def total(self) -> float: ...
    def item_count(self) -> int: ...
```

Requirements:
1. A `conftest.py`-style fixture `sample_cart` that pre-populates a cart with 3 items
2. A parametrized test for `total()` with various item combinations using `@pytest.mark.parametrize`
3. A test using `tmp_path` that saves/loads the cart as JSON
4. A test using `monkeypatch` to override a discount lookup function
5. A test using `capsys` to capture printed receipt output
