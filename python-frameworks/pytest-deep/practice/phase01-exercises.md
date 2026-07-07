# 📝 pytest Practice

## Exercise 1: Shopping Cart

Write tests for a `ShoppingCart` class:

```python
class ShoppingCart:
    def __init__(self):
        self.items = []
    def add(self, name, price, quantity=1): ...
    def remove(self, name): ...
    def total(self): ...
    def clear(self): ...
    def apply_discount(self, percent): ...
```

Test: add items, calculate total, remove items, apply discount, clear cart. Use parametrize for multiple item combos.

## Exercise 2: Fixture Factory

Create a `make_user` fixture factory that creates users with different roles. Then write tests that:
- Test admin has full access
- Test user has read-only access  
- Test viewer has no access

Use indirect parametrization to run the same test with different roles.

## Exercise 3: Mock an API

Test a function that calls an external weather API:

```python
def get_weather(city):
    resp = requests.get(f"https://api.weather.com/v1/{city}")
    data = resp.json()
    return f"{data['temp']}°C, {data['condition']}"
```

Use `mocker.patch` to mock `requests.get`. Test: successful response, network error, malformed JSON.

## Exercise 4: File Processing

Write tests for a function that reads a CSV, processes rows, and writes results. Use `tmp_path` for input/output files. Test: empty file, valid data, missing columns, large file.

## Exercise 5: Test Suite for Task Manager

Extend the integration task manager (lesson 15) with:

- `update_task(task_id, **fields)` — update title/priority
- `search(query)` — search by title substring
- Bulk add: `add_many(tasks: list[dict])`
- Error: duplicate title detection

Write comprehensive tests covering all paths. Use marks to categorize tests (unit/slow/api).
