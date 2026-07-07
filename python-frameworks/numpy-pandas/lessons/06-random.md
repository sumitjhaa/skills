# 🎲 Random Numbers
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Generate random numbers, set seeds, sample from distributions.

## Basic Random

```python
rng = np.random.default_rng(seed=42)

rng.random(5)            # Uniform [0, 1) — 5 values
rng.integers(0, 10, 5)   # Random integers 0-9
rng.normal(0, 1, (3, 3)) # Normal(mean=0, std=1)
```

## Distributions

```python
rng.uniform(0, 10, 5)        # Uniform
rng.normal(0, 1, 1000)       # Normal/Gaussian
rng.binomial(10, 0.5, 5)     # Binomial
rng.poisson(3, 5)            # Poisson
rng.exponential(1, 5)        # Exponential
```

## Shuffle & Choice

```python
arr = np.arange(10)
rng.shuffle(arr)          # In-place shuffle

rng.choice(arr, 3)        # Random sample
rng.choice(arr, 5, replace=False)  # Without replacement
```

## Seeding

```python
rng = np.random.default_rng(42)  # Reproducible results
```

<!-- 🤔 Use `default_rng()` instead of the old `np.random.seed()` — it's the modern NumPy 1.17+ API. -->

## Run the Code

```bash
python code/06-random.py
```
