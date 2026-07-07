"""Solutions for Phase 04 practice exercises."""
import functools
import time
from functools import reduce, singledispatch, wraps


def ex1_compound_interest(principal=2000, rate=0.08, years=15):
    def calculate_growth(p, r, y):
        return p * (1 + r) ** y
    result = calculate_growth(principal, rate, years)
    print(f"1. ${principal} at {rate*100}% for {years}y: ${result:.2f}")
    return result


def ex2_discount_calculator():
    def apply_discount(price, *, discount_percent=10, **coupons):
        total_discount = discount_percent + sum(coupons.values())
        return round(price * (1 - total_discount / 100), 2)
    print(f"2. $100 with 10% + VIP10: ${apply_discount(100, coupon_VIP10=10)}")
    return apply_discount


def ex3_counter_factory():
    def make_counter(start=0):
        count = start
        def inc(step=1):
            nonlocal count; count += step; return count
        def dec(step=1):
            nonlocal count; count -= step; return count
        def reset():
            nonlocal count; count = start; return count
        def value():
            return count
        return {"inc": inc, "dec": dec, "reset": reset, "value": value}
    c = make_counter(10)
    assert c["inc"]() == 11
    assert c["dec"]() == 10
    assert c["reset"]() == 10
    print("3. Counter: OK")
    return c


def ex4_product_filter():
    products = [
        {"name": "A", "price": 100, "rating": 4.5},
        {"name": "B", "price": 250, "rating": 4.2},
        {"name": "C", "price": 50, "rating": 3.8},
        {"name": "D", "price": 150, "rating": 4.1},
    ]
    filtered = list(filter(lambda p: p["price"] < 200 and p["rating"] >= 4.0, products))
    names = [p["name"] for p in filtered]
    assert names == ["A", "D"]
    print(f"4. Filtered: {names}")
    return filtered


def ex5_recursive_dir_size():
    def total_size(tree):
        if isinstance(tree, dict):
            return sum(total_size(v) for v in tree.values())
        return tree
    tree = {"docs": {"a": 100, "b": 200}, "pics": 300}
    assert total_size(tree) == 600
    print("5. Dir size: OK")


def ex6_read_chunks():
    from io import StringIO
    def read_chunks(buf, chunk_size=10):
        while chunk := buf.read(chunk_size):
            yield chunk
    buf = StringIO("Hello World! This is a test.")
    chunks = list(read_chunks(buf, 5))
    assert chunks == ["Hello", " Worl", "d! Th", "is is", " a te", "st."]
    print(f"6. Chunks: {chunks}")


def ex7_cache_ttl():
    def cache_ttl(seconds=30):
        def decorator(func):
            cache = {}
            @wraps(func)
            def wrapper(*args, **kwargs):
                key = (args, tuple(sorted(kwargs.items())))
                now = time.time()
                if key in cache and now - cache[key][0] < seconds:
                    return cache[key][1]
                result = func(*args, **kwargs)
                cache[key] = (now, result)
                return result
            return wrapper
        return decorator
    call_count = 0
    @cache_ttl(seconds=2)
    def get_data(x):
        nonlocal call_count; call_count += 1; return x * 2
    assert get_data(5) == 10 and call_count == 1
    assert get_data(5) == 10 and call_count == 1
    print("7. Cache TTL: OK")


def ex8_singledispatch():
    @singledispatch
    def report(data):
        return f"Unknown: {data}"
    @report.register(dict)
    def _(data):
        return "\n".join(f"{k}: {v}" for k, v in data.items())
    @report.register(list)
    def _(data):
        return "\n".join(f"{i}. {v}" for i, v in enumerate(data, 1))
    assert report({"a": 1, "b": 2}) == "a: 1\nb: 2"
    assert report(["x", "y"]) == "1. x\n2. y"
    print("8. SingleDispatch: OK")


def ex9_safe_pipeline():
    def safe_pipeline(*funcs):
        def applied(x):
            for f in funcs:
                try:
                    x = f(x)
                except Exception as e:
                    return {"error": str(e), "step": f.__name__}
            return x
        return applied
    def double(x):
        return x * 2
    def fail(x):
        raise ValueError("boom")
    pipe = safe_pipeline(double, fail, double)
    result = pipe(5)
    assert result == {"error": "boom", "step": "fail"}
    print("9. Safe pipeline: OK")


def ex10_text_pipeline():
    def pipe(*funcs):
        def applied(x):
            for f in funcs:
                x = f(x)
            return x
        return applied
    def clean(text):
        return text.lower().replace(",", "").replace(".", "")
    def tokenize(text):
        return text.split()
    def remove_stopwords(tokens):
        stops = {"the", "a", "an", "is", "are", "was", "were"}
        return [t for t in tokens if t not in stops]
    def freq(tokens):
        counts = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
        return counts
    pipeline = pipe(clean, tokenize, remove_stopwords, freq)
    result = pipeline("The cat and the dog were running. A cat ran fast.")
    assert result.get("cat") == 2
    assert "the" not in result
    print(f"10. Text pipeline: {result}")


if __name__ == "__main__":
    print("=== Phase 04 Solutions ===\n")
    ex1_compound_interest()
    ex2_discount_calculator()
    ex3_counter_factory()
    ex4_product_filter()
    ex5_recursive_dir_size()
    ex6_read_chunks()
    ex7_cache_ttl()
    ex8_singledispatch()
    ex9_safe_pipeline()
    ex10_text_pipeline()
    print("\nAll solutions passed!")
