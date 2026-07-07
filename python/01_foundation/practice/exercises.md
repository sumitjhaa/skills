# Practice Exercises — Phase 01: Foundation

Work through these exercises to reinforce everything you've learned. Try each one on your own before peeking at [solutions.py](solutions.py).

---

### 1. Cricket Scorecard

Write a program that stores a batsman's name, runs scored, balls faced, and whether they're out. Calculate the strike rate: `(runs / balls) * 100`. Print a formatted scorecard.

```
Batsman: Virat Kohli
Runs: 82
Balls: 53
Strike Rate: 154.72
Out: Yes
```

**Hints:** Variables, arithmetic operators, f-strings.

---

### 2. Pizza Order Calculator

Ask the user for the number of pizzas and the slices per pizza. Calculate total slices. If there are 8 people, how many slices per person (floor division) and how many leftover (modulo)?

```
Number of pizzas: 3
Slices per pizza: 8
Total slices: 24
Slices per person (8 people): 3
Leftover slices: 0
```

**Hints:** `input()`, `int()`, `//`, `%`.

---

### 3. Character Creation (RPG)

Ask the user for their character name, class, and starting level. Display a formatted character sheet using f-strings.

```
=== CHARACTER SHEET ===
Name: Thrain
Class: Dwarf Warrior
Level: 3
HP: 75
Mana: 25
```

**Hints:** `input()`, f-strings, variables, `sep=` and `end=` in print.

---

### 4. Temperature Alert

Ask for a temperature in Celsius. Convert to Fahrenheit (`F = C * 9/5 + 32`). If the temperature is above 30°C, print "Heat warning!". If below 5°C, print "Freeze warning!". Otherwise, print "Temperature normal."

**Hints:** `float()`, comparison operators, truthy/falsy from conditions.

---

### 5. Type Identification

Create one variable of each type: `int`, `float`, `str`, `bool`. Print each value and its type using `type()`. Then use `bool()` on each and print whether it's truthy or falsy.

```
Value: 42 → Type: int → Truthy
Value: 0.0 → Type: float → Falsy
Value: hello → Type: str → Truthy
Value: False → Type: bool → Falsy
```

**Hints:** `type()`, `bool()`, f-strings.

---

### 6. Grade Calculator

Ask for three test scores (as integers or floats). Calculate the average. Print each score, the average, and whether the student passed (average >= 60) or failed.

```
Test 1: 78
Test 2: 85
Test 3: 92
Average: 85.0
Status: Passed
```

**Hints:** `float()`, arithmetic operators, `if`/`else`.

---

### 7. Swap & Compare

Ask for two numbers. Print them before swapping, swap them using Python's swap syntax, print after. Then print whether the first number is now greater than the second.

```
Enter a: 15
Enter b: 7
Before: a=15, b=7
After: a=7, b=15
a > b? False
```

**Hints:** Multiple assignment, comparison operators.

---

### 8. Menu Price Calculator

A restaurant menu: Burger = $8.50, Fries = $3.00, Drink = $2.50. Ask the user how many of each they want. Calculate the subtotal, tax (8%), and total. Use f-strings with `:.2f` for currency formatting.

```
How many burgers? 2
How many fries? 1
How many drinks? 3
Subtotal: $27.50
Tax (8%): $2.20
Total: $29.70
```

**Hints:** Variables, arithmetic, f-string formatting `:.2f`, type casting.
