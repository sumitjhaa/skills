# 🏗️ Workflows — Chains, Groups, Chords
<!-- ⏱️ 20 min | 🔶 Intermediate -->

**What You'll Learn:** Compose tasks into pipelines.

## Chain (sequential)

```python
from celery import chain

# t1 → t2 → t3
result = chain(add.s(1, 2), add.s(3), add.s(4))()
# Same as:
result = (add.s(1, 2) | add.s(3) | add.s(4))()
# add(1,2) → 3 → add(3,3) → 6 → add(6,4) → 10
```

## Group (parallel)

```python
from celery import group

# All tasks run in parallel
result = group(add.s(i, i) for i in range(5))()
result.get()  # [0, 2, 4, 6, 8]
```

## Chord (group + callback)

```python
from celery import chord

# Run group, then callback with results
result = chord(
    [add.s(i, i) for i in range(5)],
    body=summarize.s()
)()
```

## Chunk (process in batches)

```python
from celery import chunks

tasks = chunks(add.s(i, i) for i in range(1000))(10)  # 10 batches of 100
```

<!-- 🤔 Use chain for sequential pipelines, group for parallel fan-out, chord for map-reduce. -->

## Run the Code

```bash
python code/09-workflows.py
```
