"""Streaming paginated API results and infinite sequences."""
import random


def paginated_results(data: list, page_size: int = 3):
    for i in range(0, len(data), page_size):
        yield {"page": i // page_size + 1, "results": data[i:i + page_size]}


def infinite_counter(start: int = 0, step: int = 1):
    while True:
        yield start
        start += step


def read_sensor_data(samples: int):
    for _ in range(samples):
        yield round(random.uniform(20.0, 30.0), 1)


def fibonacci(limit: int):
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b


squares = (x ** 2 for x in range(10))
print("Squares:", list(squares))

users = [f"user_{i}" for i in range(10)]
for page in paginated_results(users, 3):
    print(f"Page {page['page']}: {page['results']}")

counter = infinite_counter()
print("First 5 IDs:", [next(counter) for _ in range(5)])

print("Sensor:", list(read_sensor_data(3)))
print("Fibonacci <=100:", list(fibonacci(100)))
