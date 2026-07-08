# 🏗️ Calling Tasks
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Different ways to call tasks.

## Calling Methods

```python
# Synchronous (direct call, no queue)
result = add(1, 2)

# Async with delay()
result = add.delay(1, 2)

# Async with apply_async (more options)
result = add.apply_async(
    args=(1, 2),
    countdown=10,         # execute in 10s
    queue='high_priority',
    priority=5,
    expires=3600,         # expire after 1 hour
)
```

## Signature Objects

```python
# Create a callable signature
sig = add.s(1, 2)
sig.delay()               # same as add.delay(1, 2)

# Partial arguments
add_s = add.s(10)         # one arg bound
add_s.delay(5)            # calls add(10, 5) → 15
```

<!-- 🤔 Use `apply_async` for production (control over timing, queue, routing). Use `delay` for quick scripts. -->

## Run the Code

```bash
python code/05-calling-tasks.py
```
