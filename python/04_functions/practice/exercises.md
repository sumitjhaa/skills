# Practice Exercises — Functions (Phase 04)

## 1. 🟢 Compound Interest Calculator
Write a function `calculate_growth(principal, rate, years)` that returns the final amount using `A = P(1+r)^t`. Use it to find what $2000 becomes at 8% over 15 years.
> 💡 Hint: `def calculate_growth(principal, rate, years): return ...`

## 2. 🟢 Flexible Discount Calculator
Write `apply_discount(price, *, discount_percent=10, **coupons)` where `discount_percent` is keyword-only. Coupons can add extra discounts (e.g., `VIP10=10`). Return the final price.
> 💡 Hint: `**coupons` gives you a dict; sum `coupons.values()` for extra discount.

## 3. 🟡 Counter Factory with Reset
Write `make_counter(start=0)` returning a dict of closures: `inc()`, `dec()`, `reset()`, `value()`. Use `nonlocal`.
> 💡 Hint: Store `count` in enclosing scope; `reset()` sets it back to `start`.

## 4. 🟡 Product Filter Pipeline
Given `products = [{"name": "A", "price": 100, "rating": 4.5}, ...]`, use `filter` + `lambda` to find products under $200 with rating ≥ 4.0.
> 💡 Hint: Chain two `filter` calls or use `and` in one lambda.

## 5. 🟡 Recursive Directory Size
Write `total_size(tree)` that sums all values in a nested dict where leaves are integers. `{"docs": {"a": 100, "b": 200}, "pics": 300}` → 600.
> 💡 Hint: Use `isinstance(v, dict)` to check for nesting.

## 6. 🟡 Generator: Read Large File Chunks
Write `read_chunks(filepath, chunk_size=1024)` that yields chunks of a file. Test it with a StringIO buffer.
> 💡 Hint: Use `f.read(chunk_size)` in a loop until it returns empty string.

## 7. 🔴 Decorator: Cache with TTL
Write `@cache_ttl(seconds=30)` that caches results but expires them after `seconds`. Use `time.time()`.
> 💡 Hint: Store `(timestamp, result)` pairs in a dict.

## 8. 🔴 Functools: Single-Dispatch Formatter
Use `@singledispatch` to create a `report(data)` function that formats `dict` items as "key: value", `list` items as numbered lines.
> 💡 Hint: Register handlers with `@report.register(type)`.

## 9. 🔴 Error-Proof Pipeline
Write `safe_pipeline(*funcs)` that catches exceptions and returns `{"error": str(e), "step": func.__name__}` on failure.
> 💡 Hint: Wrap each `f(x)` call in try/except inside the pipeline loop.

## 10. 🔴 Function Composition: Text Processor
Build a text pipeline: `clean(text)` → `tokenize(text)` → `remove_stopwords(tokens)` → `freq(tokens)`. Use `pipe()`.
> 💡 Hint: `clean` strips/punctuation, `remove_stopwords` filters common words like "the" "a".
