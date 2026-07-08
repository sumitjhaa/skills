"""
Mock ML Testing — demonstrates data tests, model tests (invariance,
directional), and infrastructure tests using pytest-style assertions.
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification


# ---------------------------------------------------------------------------
# Data Tests
# ---------------------------------------------------------------------------

def test_no_nulls(df: np.ndarray) -> bool:
    assert not np.any(np.isnan(df)), "Data contains NaN values"
    return True


def test_feature_range(df: np.ndarray, mins: list[float], maxs: list[float]) -> bool:
    for col_idx in range(df.shape[1]):
        col = df[:, col_idx]
        assert col.min() >= mins[col_idx] - 1e-6, f"Feature {col_idx} below min"
        assert col.max() <= maxs[col_idx] + 1e-6, f"Feature {col_idx} above max"
    return True


def test_train_test_split(X_train: np.ndarray, X_test: np.ndarray) -> bool:
    """Check no overlap between train and test."""
    train_set = set(map(tuple, X_train[:100]))  # sample for speed
    test_set = set(map(tuple, X_test[:100]))
    overlap = train_set & test_set
    assert len(overlap) == 0, f"Found {len(overlap)} overlapping rows"
    return True


# ---------------------------------------------------------------------------
# Model Tests
# ---------------------------------------------------------------------------

def test_model_invariance(model, X: np.ndarray, epsilon: float = 1e-4) -> bool:
    """Small input perturbations should not meaningfully change output."""
    preds_original = model.predict_proba(X[:10])
    noisy = X[:10] + np.random.normal(0, epsilon, X[:10].shape)
    preds_noisy = model.predict_proba(noisy)
    diff = np.abs(preds_original - preds_noisy).max()
    assert diff < 0.01, f"Model not invariant: max diff = {diff:.6f}"
    return True


def test_directional_effect(model, feature_idx: int = 0, direction: str = "positive") -> bool:
    """Increasing a feature should move prediction in expected direction."""
    base = np.zeros((10, model.coef_.shape[1]))
    base[:, feature_idx] = 0.0
    pred_low = model.predict_proba(base)[:, 1]

    base[:, feature_idx] = 10.0
    pred_high = model.predict_proba(base)[:, 1]

    if direction == "positive":
        assert (pred_high > pred_low).all(), f"Feature {feature_idx} should have positive effect"
    else:
        assert (pred_high < pred_low).all(), f"Feature {feature_idx} should have negative effect"
    return True


def test_performance_floor(model, X_test: np.ndarray, y_test: np.ndarray, min_accuracy: float = 0.70) -> bool:
    preds = model.predict(X_test)
    acc = (preds == y_test).mean()
    assert acc >= min_accuracy, f"Accuracy {acc:.3f} < floor {min_accuracy}"
    return True


# ---------------------------------------------------------------------------
# Infrastructure Tests
# ---------------------------------------------------------------------------

def test_model_serialization(model) -> bool:
    """Model can be pickled and loaded."""
    import io
    import pickle
    buf = io.BytesIO()
    pickle.dump(model, buf)
    buf.seek(0)
    loaded = pickle.load(buf)
    assert loaded is not None
    return True


def test_inference_time(model, X: np.ndarray, max_ms: float = 10.0) -> bool:
    import time
    t0 = time.perf_counter()
    model.predict(X[:32])
    elapsed_ms = (time.perf_counter() - t0) * 1000
    assert elapsed_ms < max_ms, f"Inference took {elapsed_ms:.2f}ms > {max_ms}ms"
    return True


if __name__ == "__main__":
    print("=== ML Testing Suite ===\n")

    # Create synthetic dataset
    X, y = make_classification(n_samples=1000, n_features=10, random_state=42)
    X_train, X_test = X[:800], X[800:]
    y_train, y_test = y[:800], y[800:]

    # Train a simple model
    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)

    # Run tests
    tests = [
        ("test_no_nulls (train)", lambda: test_no_nulls(X_train)),
        ("test_no_nulls (test)", lambda: test_no_nulls(X_test)),
        ("test_feature_range", lambda: test_feature_range(X_train, [-5]*10, [5]*10)),
        ("test_train_test_split", lambda: test_train_test_split(X_train, X_test)),
        ("test_model_invariance", lambda: test_model_invariance(model, X_test)),
        ("test_directional_effect", lambda: test_directional_effect(model, 0, "positive")),
        ("test_performance_floor", lambda: test_performance_floor(model, X_test, y_test, 0.70)),
        ("test_model_serialization", lambda: test_model_serialization(model)),
        ("test_inference_time", lambda: test_inference_time(model, X_test, 10.0)),
    ]

    passed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  ✓ {name}")
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {name}: {e}")
        except Exception as e:
            print(f"  ✗ {name}: unexpected error: {e}")

    print(f"\n{passed}/{len(tests)} tests passed")
    assert passed == len(tests), "Some tests failed"
