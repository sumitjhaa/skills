# 🎯 Operators
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** Use arithmetic, comparison, and logical operators to perform calculations and make comparisons.

> 💡 **TL;DR — The whole point:** Operators are the math and logic tools (`+`, `-`, `*`, `/`, `==`, `>`, `and`, `or`, `not`) that let you calculate values and compare them.

## 🔗 Why This Matters
Data Types (Lesson 03) taught you what values exist. Operators let you *do things* with those values — scale a recipe by 3, compare ingredient portions, or check if you have enough flour. Without operators, your variables just sit there doing nothing.

## The Concept

Operators are symbols that perform operations on values. Like a chef adjusting a recipe:

**Arithmetic operators** adjust quantities: `+` (add), `-` (subtract), `*` (multiply), `/` (divide), `//` (floor division — how many whole portions?), `%` (modulo — what's left over?), `**` (exponentiation — scale up dramatically).

**Comparison operators** compare amounts: `==` (equal to?), `!=` (not equal?), `<`, `>`, `<=`, `>=`.

**Logical operators** combine conditions: `and` (both true?), `or` (at least one true?), `not` (reverse the truth).

Python supports **chained comparisons** — write `0 < x < 10` instead of `x > 0 and x < 10`. Logical operators use **short-circuit evaluation**: if the first operand decides the result, the second never runs.

## Code Example

```python
"""Recipe scaling — adjusting ingredient quantities with operators"""

# Original recipe (serves 4)
original_flour = 2.0       # cups
original_sugar = 1.5       # cups
original_eggs = 3
original_butter = 0.5      # cups

# Scale to serve 6 people
scale_factor = 6 / 4

# Arithmetic operators
flour_needed = original_flour * scale_factor
sugar_needed = original_sugar * scale_factor
eggs_needed = original_eggs * scale_factor
butter_needed = original_butter * scale_factor

print(f"To serve 6, you need:")
print(f"  Flour: {flour_needed} cups")
print(f"  Sugar: {sugar_needed} cups")
print(f"  Eggs: {eggs_needed} (can't buy partial eggs!)")
print(f"  Butter: {butter_needed} cups")

# Floor division and modulo — splitting eggs into dozens
total_eggs_needed = 15
dozens = total_eggs_needed // 12
loose_eggs = total_eggs_needed % 12
print(f"\n{total_eggs_needed} eggs = {dozens} dozen + {loose_eggs} loose")

# Comparison operators
print(f"\nNeed more than 2 cups flour? {flour_needed > 2.0}")
print(f"Exact sugar amount? {sugar_needed == 2.25}")

# Logical operators — can I make this recipe?
has_flour = flour_needed <= 5.0    # I have 5 cups of flour
has_sugar = sugar_needed <= 2.0     # I have 2 cups of sugar
can_bake = has_flour and has_sugar
print(f"\nHave enough flour? {has_flour}")
print(f"Have enough sugar? {has_sugar}")
print(f"Can I bake? {can_bake}")

# Short-circuit demonstration
def check_pantry(item):
    print(f"  (Checking {item}...)")
    return True

print(f"\nShort-circuit: Need eggs OR check pantry?")
result = True or check_pantry("milk")  # check_pantry never runs!
print(f"  Result: {result} (milk was never checked!)")
```

## 🔍 How It Works

- `*` multiplies quantities by the scale factor — `2.0 * 1.5 = 3.0` cups flour
- `/` divides — `6 / 4 = 1.5`, the scaling factor
- `//` floor division — `15 // 12 = 1` (how many full dozens)
- `%` modulo — `15 % 12 = 3` (leftover eggs after making dozens)
- `flour_needed > 2.0` — comparison returns `True` or `False`
- `has_flour and has_sugar` — logical AND: both must be `True`
- `True or check_pantry("milk")` — short-circuit: since first operand is `True`, Python never calls `check_pantry()`
- Chained comparison: `0 < x < 10` works like `x > 0 and x < 10`

## ⚠️ Common Pitfall

Using `=` instead of `==` in comparisons: `if flour_needed = 3.0` assigns instead of comparing, causing a syntax error or subtle bug. Also, remember that `/` always returns a float even if the division is exact (`4/2 = 2.0`), and `==` for floats can be unreliable due to precision — compare `abs(a - b) < 0.0001` instead.

## 🧠 Memory Aid

**"PEMDAS — Please Excuse My Dear Aunt Sally"** (Parentheses, Exponents, Multiplication/Division, Addition/Subtraction). Operator precedence follows standard math. When in doubt, add parentheses: `(a + b) * c` is clearer than `a + b * c`.

## 🏃 Try It

Run the code file:
```bash
python code/01-04-operators.py
```
Then change the recipe to serve 12 and add a check for `butter` availability.

## 🔗 Related

- [Type Casting](07-type-casting.md) — operators often involve type conversion
- [Truthy & Falsy](08-truthy-falsy.md) — how operators interact with truthiness

## ➡️ Next

→ [05 — Input & Output](05-input-output.md)
