# 🧱 Defining Functions
<!-- ⏱️ 10 min read | 🟢 Easy | 🧠 Core -->

**What You'll Learn:** How to define reusable functions with `def`, `return`, docstrings, and type hints.

> 💡 **TL;DR — The whole point:** A function packages code so you can run it again with different inputs.

## 🔗 Why This Matters
Remember writing the same calculation over and over? Functions let you write it once and call it by name — like setting up a formula in a spreadsheet.

## The Concept
A function is a named block of reusable code. You feed it inputs (parameters), it does work, and optionally returns a result. Functions are **first-class citizens** in Python — you can assign them to variables, pass them as arguments, and return them from other functions.

Think of a function like an ATM: you insert a card (parameter), it processes (function body), and gives you cash (return value). Well-defined, predictable, reusable.

## Code Example

```python
"""Financial calculator — compound interest and loan payment functions."""


def compound_interest(principal: float, rate: float, years: int) -> float:
    """Calculate compound interest: A = P(1 + r)^t."""
    return principal * (1 + rate) ** years


def monthly_loan_payment(principal: float, annual_rate: float, months: int) -> float:
    """Calculate fixed monthly payment for a loan."""
    monthly_rate = annual_rate / 12
    if monthly_rate == 0:
        return principal / months
    payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    return round(payment, 2)


# Functions are first-class — assign to a variable
calc = compound_interest
print(calc(1000, 0.05, 10))          # 1628.89
print(monthly_loan_payment(30000, 0.06, 60))  # 579.98
print(compound_interest.__doc__)      # Calculate compound interest...
```

## 🔍 How It Works
- `def` creates a function object and binds it to a name
- `return` sends a value back to the caller and exits the function
- A function without `return` implicitly returns `None`
- Type hints (`name: str`, `-> str`) are documentation — not enforced at runtime
- Functions are objects: you can print them, pass them, inspect their `__doc__`

## ⚠️ Common Pitfall
Forgetting `return`. If you write `def f(x): x * 2` without `return`, the function returns `None`. Always check you have a `return` statement if you expect a value.

## 🧠 Memory Aid
**"def → return"** — every `def` should be paired with a `return` (or be a void function). Think **DRY**: Don't Repeat Yourself.

## 🏃 Try It
Write a function `investment_growth(principal, rate, years)` that returns the final value using compound interest. Test it with $5000 at 7% for 30 years.

## 🔗 Related
- [Parameters & Arguments →](./02-parameters.md)

## ➡️ Next
[Parameters & Arguments](./02-parameters.md)
