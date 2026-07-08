"""Workflows — chains, groups, chords, chunks."""
from celery import Celery, chain, group, chord, chunks


print("=== Workflows ===\n")

app = Celery('demo', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True

@app.task
def add(x, y):
    result = x + y
    print(f"    add({x}, {y}) = {result}")
    return result

@app.task
def multiply(x, y):
    result = x * y
    print(f"    multiply({x}, {y}) = {result}")
    return result

@app.task
def sum_all(numbers):
    result = sum(numbers)
    print(f"    sum_all({numbers}) = {result}")
    return result

print("1. Chain (sequential):")
result = chain(add.s(1, 2), add.s(3), add.s(4))()
print(f"   [(1+2)→3, +3→6, +4→10] = {result.get()}\n")

print("2. Chain with pipe operator:")
result = (add.s(1, 2) | multiply.s(10))()
print(f"   [(1+2)=3, ×10=30] = {result.get()}\n")

print("3. Group (parallel):")
result = group(add.s(i, i) for i in range(5))()
print(f"   Results: {result.get()}\n")

print("4. Chord (group + callback):")
result = chord([add.s(i, i) for i in range(5)])(sum_all.s())
print(f"   Group: [0,2,4,6,8], Sum: {result.get()}\n")

print("5. Signature composition:")
step1 = add.s(5, 5)
step2 = multiply.s(2)
step3 = add.s(10)
result = (step1 | step2 | step3)()
print(f"   (5+5)=10, ×2=20, +10=30 → {result.get()}")
