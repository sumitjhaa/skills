# 🎯 Type Casting
<!-- ⏱️ 8 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** Convert values between types using `int()`, `float()`, `str()`, and `bool()`, and handle the `ValueError` trap safely.

> 💡 **TL;DR — The whole point:** Use `int()`, `float()`, `str()`, and `bool()` to convert between types; `int("5.5")` crashes — convert to float first with `int(float("5.5"))`.

## 🔗 Why This Matters
Input (Lesson 05) always returns strings. String formatting (Lesson 06) needs strings. But math needs numbers. Type casting bridges these worlds — like a weather app that reads "23" from a text field, converts it to 23 (integer), compares it to a threshold, then converts the result back to display text.

## The Concept

Type casting (type conversion) changes a value from one type to another. The cast functions are named after the types: `int()`, `float()`, `str()`, `bool()`.

The most common use: `input()` returns a string, but you need a number for calculations. Cast it with `int()` or `float()`.

The **ValueError trap**: `int("5.5")` crashes because `int()` expects a string that looks like an integer (no decimal point). Convert to `float()` first, then to `int()`. Similarly, `float("abc")` crashes. Always validate or use `try/except` for risky conversions.

## Code Example

```python
"""Weather app — converting temperature strings for comparison"""

print("=== Weather Station ===")

# Reading from a sensor (simulated as string input)
temp_string = input("Enter current temperature (°C): ")
humidity_string = input("Enter humidity percentage: ")

# Cast strings to numbers for calculation
temperature = float(temp_string)
humidity = int(humidity_string)

# Categorize the weather
print(f"\nCurrent temperature: {temperature}°C")
print(f"Humidity: {humidity}%")

# Comparison after casting
if temperature > 30:
    print("🔥 Hot day — stay hydrated!")
elif temperature > 20:
    print("🌤️ Pleasant weather — enjoy the day!")
else:
    print("❄️ Cool — bring a jacket!")

if humidity > 70:
    print("💧 High humidity — might rain!")

# Converting back to string for display
report = "Temp: " + str(temperature) + "°C | Humidity: " + str(humidity) + "%"
print(f"\nWeather Report: {report}")

# The ValueError trap — safe conversion
raw_value = "5.5"
try:
    # int(raw_value) would crash!
    safe_value = int(float(raw_value))  # float first, then int
    print(f"\nSafe conversion of '{raw_value}': {safe_value}")
except ValueError:
    print(f"\nCould not convert '{raw_value}' to a number.")
```

## 🔍 How It Works

- `float(temp_string)` — converts the input string (e.g., `"23.5"`) to a float `23.5`
- `int(humidity_string)` — converts `"65"` to integer `65`; would crash on `"65.5"`
- `str(temperature)` — converts float `23.5` back to string `"23.5"` for concatenation
- `int(float("5.5"))` — two-step conversion: first to float `5.5`, then to int `5` (truncates, doesn't round)
- `bool()` — converts any value to `True` or `False` (see Truthy & Falsy lesson)
- The `try/except` block catches `ValueError` if the user enters non-numeric text

## ⚠️ Common Pitfall

Calling `int()` directly on a decimal string like `"5.5"` or `"3.14"` — this raises `ValueError`. Always go through `float()` first: `int(float("5.5"))` gives `5`. Also, casting `"abc"` to `int` or `float` will crash — validate with `.isdigit()` or use `try/except`.

## 🧠 Memory Aid

**"Cast from wide to narrow: string is the widest (holds anything), float holds decimals, int holds only whole numbers. Go string → float → int, never string → int directly."** Think of a funnel — pouring a wide container through a narrow opening requires a middle step.

## 🏃 Try It

Run the code file:
```bash
python code/01-07-type-casting.py
```
Then add a wind speed input and convert it to an integer for a "windy or calm" check.

## 🔗 Related

- [Data Types](03-data-types.md) — what you're casting from and to
- [Input & Output](05-input-output.md) — casting user input in practice

## ➡️ Next

→ [08 — Truthy & Falsy](08-truthy-falsy.md)
