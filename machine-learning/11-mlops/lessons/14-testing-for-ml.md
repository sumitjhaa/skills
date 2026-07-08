# 11.14 Testing for ML

## Objective
Apply software testing principles to ML data, models, and infrastructure.

## Types of ML Tests

### 1. Data Tests
- Schema validation (column types, null %, allowed values).
- Distribution tests (train vs. test — KS test, mean, std).
- Freshness tests (timestamp not in future).

```python
def test_no_nulls(df):
    assert df.isnull().sum().sum() == 0

def test_target_range(df):
    assert df["label"].between(0, 1).all()
```

### 2. Model Tests
- **Invariance** — small input perturbations → same prediction.
- **Directional** — increasing a feature should move prediction in expected direction.
- **Performance floor** — accuracy > baseline on held-out test set.

```python
def test_model_invariance(model, X):
    noisy = X + np.random.normal(0, 1e-4, X.shape)
    np.testing.assert_allclose(model(X), model(noisy), rtol=1e-3)
```

### 3. Infrastructure Tests
- Model can be loaded and run inference.
- Serving endpoint returns correct status code.
- Batch inference time under threshold.

### 4. Integration Tests
- Feature engineering produces expected output columns.
- Training pipeline runs end-to-end on a tiny subset.

## Test Automation (CI)
```yaml
# .github/workflows/ml-tests.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: python -m pytest tests/data/
      - run: python -m pytest tests/model/
      - run: python -m pytest tests/integration/
```

## Best Practices
1. Test on data slices (by region, by segment) — not just global metrics.
2. Use `pytest` fixtures for model and data setup.
3. Fail CI fast — run data tests before model tests.
4. Maintain a golden test dataset (never modified).
