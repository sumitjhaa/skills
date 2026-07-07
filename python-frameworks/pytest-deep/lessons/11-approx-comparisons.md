# 📐 Approx & Comparisons
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Float comparison with `approx`, custom tolerances.

## The Float Problem

```python
assert 0.1 + 0.2 == 0.3  # ❌ False! Floating point error
```

## Using approx

```python
from pytest import approx

assert 0.1 + 0.2 == approx(0.3)  # ✅ True
```

## Custom Tolerance

```python
assert value == approx(100, rel=0.01)   # Within 1% relative
assert value == approx(100, abs=0.5)    # Within 0.5 absolute
assert value == approx(100, rel=0.05, abs=1.0)  # Both
```

## Collections

```python
assert [0.1 + 0.2, 1.0 / 3.0] == approx([0.3, 0.33333])
assert {"a": 0.1 + 0.2} == approx({"a": 0.3})
```

## Default Tolerances

| Type | Default |
|------|---------|
| `rel` | 1e-6 |
| `abs` | 1e-12 |

<!-- 🤔 Always use `approx` for float comparisons. Never use `==`. -->

## Run the Code

```bash
pytest code/11-approx-comparisons.py -v
```
