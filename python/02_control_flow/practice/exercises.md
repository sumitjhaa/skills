# Practice Exercises — Control Flow

Solve each exercise, then check your answers in [solutions.py](solutions.py).

### Exercise 1: Squid Game Eligibility
Ask the user for their age and debt amount (in millions). If they're 18+ and debt > 10 million, print "Eligible for Squid Game." If they're under 18, print "Too young." Otherwise, print "Debt too low — not eligible."

**Hints:** `if`/`elif`/`else`, `and` operator, `int()`.

---

### Exercise 2: FizzBuzz
Print numbers 1 to 50. For multiples of 3 print "Fizz", for multiples of 5 print "Buzz", for multiples of both print "FizzBuzz". One line per number.

**Hints:** `for` loop, `range()`, modulo `%`, `if`/`elif`/`else`.

---

### Exercise 3: Sum Until Zero
Keep asking the user for numbers. Sum them up. Stop when the user enters 0. Print the total.

**Hints:** `while True`, `break`, `int()`.

---

### Exercise 4: Prime Checker
Ask the user for a number. Use a `for`/`else` loop to determine if it's prime. Print the result.

**Hints:** `for`/`else`, modulo, `range(2, int(n ** 0.5) + 1)` for efficiency.

---

### Exercise 5: Multiplication Table
Use nested loops to print a 10×10 multiplication table, right-aligned to 4 characters each.

**Hints:** Nested `for` loops, f-string formatting like `{i*j:4}`.

---

### Exercise 6: Password Validator
Keep asking for a password until it's at least 8 characters, contains a digit, and contains an uppercase letter. Print specific error messages for each failed check.

**Hints:** `while True`, `break`, `continue`, `any()`, `.isdigit()`, `.isupper()`.

---

### Exercise 7: Number Pyramid
Use nested loops to print this pattern:
```
    1
   1 2
  1 2 3
 1 2 3 4
1 2 3 4 5
```

**Hints:** Nested loops, `end=" "`, spaces for alignment.

---

### Exercise 8: HTTP Status Classifier
Use `match`/`case` to classify an HTTP status code:
- 1xx: "Informational"
- 2xx: "Success"
- 3xx: "Redirection"
- 4xx: "Client Error"
- 5xx: "Server Error"
- Other: "Unknown"

**Hints:** `match`/`case` with guards (`case _ if 100 <= code < 200:`).
