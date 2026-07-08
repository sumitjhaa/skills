"""Calling tasks — delay, apply_async, signatures, countdown."""
from celery import Celery


print("=== Calling Tasks ===\n")

app = Celery('demo', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True

@app.task
def add(x, y):
    return x + y

@app.task
def greet(name):
    return f"Hello, {name}!"

print("1. delay()")
r1 = add.delay(2, 3)
print(f"   add.delay(2, 3) = {r1.get()}")

print("\n2. apply_async()")
r2 = add.apply_async(args=(10, 20), countdown=5)
print(f"   add.apply_async(args=(10,20), countdown=5) = {r2.get()}")

print("\n3. Signature objects")
sig = add.s(5, 5)
r3 = sig.delay()
print(f"   add.s(5,5).delay() = {r3.get()}")

print("\n4. Partial signatures")
add_10 = add.s(10)
r4 = add_10.delay(20)
print(f"   add.s(10).delay(20) = {r4.get()}")

r5 = add_10.delay(30)
print(f"   add.s(10).delay(30) = {r5.get()}")

print("\n5. Method mapping:")
print("   .delay(*args)           → simple async call")
print("   .apply_async(kwargs)    → full control")
print("   .s(*args)               → signature (partial)")
