# 🏷️ Marks
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** skip, skipif, xfail, custom marks, running by mark.

## Skip

```python
@pytest.mark.skip(reason="Not implemented yet")
def test_feature():
    ...

@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires 3.10+")
def test_new_syntax():
    ...
```

## Expected Failure

```python
@pytest.mark.xfail(reason="Known bug #123")
def test_bug():
    assert 1 / 0  # Expected to fail

@pytest.mark.xfail(strict=True)  # Fails if unexpectedly passes
def test_regression():
    ...
```

## Custom Marks

```python
@pytest.mark.slow
def test_heavy_computation():
    ...

@pytest.mark.api
def test_external_service():
    ...
```

Register in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "api: tests that call external APIs",
]
```

## Running by Mark

```bash
pytest -m slow                    # Run slow tests
pytest -m "not slow"              # Skip slow tests
pytest -m "api or slow"           # Union
pytest -m "api and not slow"      # Intersection
```

<!-- 🤔 Use `-m` to organize CI pipelines: unit vs integration vs smoke tests. -->

## Run the Code

```bash
pytest code/05-marks.py -v
```
