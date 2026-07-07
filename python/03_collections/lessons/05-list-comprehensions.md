# 🎯 List Comprehensions
<!-- ⏱️ 9 min read | 🟡 Medium | 🧠 Applied -->

**What You'll Learn:** Build lists concisely with comprehension syntax — including filters, conditional expressions, and nested loops.

> 💡 **TL;DR — The whole point:** `[expr for item in iterable if condition]` creates a list in one line — combining map, filter, and loop in a single readable expression.

## 🔗 Why This Matters
Building lists with `for` loops and `.append()` (Lessons 03-04) works, but it's verbose. List comprehensions are the Pythonic way — shorter, faster, and more readable once you get used to them. They're used everywhere in real Python code for data transformation: filtering weather data, extracting stock prices, or mapping scores to grades.

## The Concept

A list comprehension is a compact way to create a list by applying an expression to each item in an iterable. The basic form is `[expression for item in iterable]` — it reads like English: "make a list of `expression` for each `item` in `iterable`."

Add `if` to filter items, use `if/else` (ternary) to transform conditionally, and nest comprehensions for nested loops. The rule of thumb: if the logic fits on one line, use a comprehension; if it needs multiple lines, stick with a regular loop.

## Code Example

```python
"""Weather data analysis — list comprehensions for temperature processing"""

# Raw temperature readings (°C) from sensors
temps = [23.5, 18.0, 35.2, 28.8, 15.1, 32.7, 22.4, 30.0, 12.3, 27.6]

print("=== Weather Analysis ===")

# Basic — convert all to Fahrenheit
fahrenheit = [(t * 9 / 5 + 32) for t in temps]
print(f"Temps in °F: {[round(f, 1) for f in fahrenheit]}")

# With filter — only hot days (above 30°C)
hot_days = [t for t in temps if t > 30]
print(f"\nHot days (>{30}°C): {hot_days}")

# With if/else — classify each temperature
labels = ["Hot" if t > 30 else "Warm" if t > 20 else "Cool" for t in temps]
for i, (temp, label) in enumerate(zip(temps, labels), 1):
    print(f"  Day {i}: {temp}°C — {label}")

# String transformation
cities = ["london", "paris", "new york", "tokyo"]
capitalized = [city.title() for city in cities]
print(f"\nCities: {capitalized}")

# Filtering with string condition
long_cities = [city.title() for city in cities if len(city) > 5]
print(f"Long city names: {long_cities}")

# Nested comprehension — 3x3 grid of coordinates
grid = [(x, y) for x in range(3) for y in range(3)]
print(f"\nCoordinate grid: {grid}")

# Flat from nested list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
print(f"Flattened matrix: {flattened}")
```

## 🔍 How It Works

- `[(t * 9/5 + 32) for t in temps]` — applies the Fahrenheit formula to each temperature, creating a new list
- `[t for t in temps if t > 30]` — filter: only includes temps where the condition is True
- `["Hot" if t > 30 else "Warm" if t > 20 else "Cool" for t in temps]` — ternary inside: different string per temperature range
- `[city.title() for city in cities]` — transforms each string with `.title()`
- `[(x, y) for x in range(3) for y in range(3)]` — nested loops: for each x (0,1,2), iterate through all y (0,1,2) = 9 pairs
- `[num for row in matrix for num in row]` — flatten: outer loop gets each row, inner loop gets each number in that row

## ⚠️ Common Pitfall

Putting the `if` after the expression instead of after the iterable: `[x * 2 if x > 5 for x in nums]` is a syntax error. The `if` filter goes *after* the `for`: `[x * 2 for x in nums if x > 5]`. The ternary `x * 2 if x > 5 else x` is different — it goes *before* the `for` and applies to every element.

Also, overly complex comprehensions become unreadable. If it spans more than one line or has multiple nested loops, use a regular `for` loop instead.

## 🧠 Memory Aid

**"Think of a comprehension as a factory assembly line: [what_to_make for each_item in supply_room if item_is_good_enough]."** The expression is the manufacturing step, the `for` is the conveyor belt, and the `if` is the quality control checkpoint.

## 🏃 Try It

Run the code file:
```bash
python code/03-05-list-comprehensions.py
```
Then create a comprehension that takes a list of stock prices `[150.25, 75.50, 200.00, 45.75]` and returns `"High"` for prices above 100, `"Low"` otherwise.

## 🔗 Related

- [Lists I](03-lists-i.md) — the traditional way to build lists (for comparison)
- [Dictionaries](07-dictionaries.md) — dict comprehensions (`{k: v for ...}`)

## ➡️ Next

→ [06 — Tuples](06-tuples.md)
