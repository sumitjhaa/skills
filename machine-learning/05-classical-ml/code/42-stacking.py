"""Stacking / Blending from scratch with CV stacking for classification and regression."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score, r2_score

class StackingClassifier:
    def __init__(self, base_models, meta_model, n_folds=5):
        self.base_models = base_models
        self.meta_model = meta_model
        self.n_folds = n_folds

    def fit(self, X, y):
        kf = KFold(n_splits=self.n_folds, shuffle=True, random_state=42)
        meta_features = np.zeros((X.shape[0], len(self.base_models)))

        for i, model in enumerate(self.base_models):
            for train_idx, val_idx in kf.split(X):
                model_clone = model.__class__(**model.get_params()) if hasattr(model, 'get_params') else model.__class__()
                if hasattr(model, 'fit'):
                    model_clone.fit(X[train_idx], y[train_idx])
                    meta_features[val_idx, i] = model_clone.predict_proba(X[val_idx])[:, 1]
            model.fit(X, y)

        self.meta_model.fit(meta_features, y)
        return self

    def predict(self, X):
        meta = self._get_meta_features(X)
        return self.meta_model.predict(meta)

    def predict_proba(self, X):
        meta = self._get_meta_features(X)
        return self.meta_model.predict_proba(meta) if hasattr(self.meta_model, 'predict_proba') else None

    def _get_meta_features(self, X):
        meta = np.zeros((X.shape[0], len(self.base_models)))
        for i, model in enumerate(self.base_models):
            meta[:, i] = model.predict_proba(X)[:, 1]
        return meta

class StackingRegressor:
    def __init__(self, base_models, meta_model, n_folds=5):
        self.base_models = base_models
        self.meta_model = meta_model
        self.n_folds = n_folds

    def fit(self, X, y):
        kf = KFold(n_splits=self.n_folds, shuffle=True, random_state=42)
        meta_features = np.zeros((X.shape[0], len(self.base_models)))

        for i, model in enumerate(self.base_models):
            for train_idx, val_idx in kf.split(X):
                model_clone = model.__class__(**model.get_params()) if hasattr(model, 'get_params') else model.__class__()
                model_clone.fit(X[train_idx], y[train_idx])
                meta_features[val_idx, i] = model_clone.predict(X[val_idx])
            model.fit(X, y)

        self.meta_model.fit(meta_features, y)
        return self

    def predict(self, X):
        meta = np.zeros((X.shape[0], len(self.base_models)))
        for i, model in enumerate(self.base_models):
            meta[:, i] = model.predict(X)
        return self.meta_model.predict(meta)

if __name__ == "__main__":
    np.random.seed(42)
    from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
    from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
    from sklearn.svm import SVC, SVR
    from sklearn.ensemble import RandomForestClassifier

    print("=== Stacking Classifier ===")
    X, y = make_classification(n_samples=500, n_features=10, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    base_models = [
        LogisticRegression(max_iter=200),
        DecisionTreeClassifier(max_depth=5),
        LogisticRegression(max_iter=200, C=10.0),
    ]
    meta_model = LogisticRegression(max_iter=200)

    stack = StackingClassifier(base_models, meta_model)
    stack.fit(X_tr, y_tr)
    stack_acc = accuracy_score(y_te, stack.predict(X_te))

    print(f"  Stacking Accuracy: {stack_acc:.4f}")
    print(f"  Individual model accuracies:")
    individual_accs = []
    for m in base_models:
        m.fit(X_tr, y_tr)
        acc = accuracy_score(y_te, m.predict(X_te))
        individual_accs.append(acc)
        print(f"    {type(m).__name__}: {acc:.4f}")

    # Compare with majority voting
    voting_preds = np.array([m.predict(X_te) for m in base_models])
    voting_acc = accuracy_score(y_te, np.round(voting_preds.mean(axis=0)).astype(int))
    print(f"  Majority voting: {voting_acc:.4f}")
    print(f"  Stacking improvement over best base: {stack_acc - max(individual_accs):.4f}")

    print("\n=== Stacking Regressor ===")
    X_r, y_r = make_regression(n_samples=300, n_features=10, noise=0.3, random_state=42)
    Xr_tr, Xr_te, yr_tr, yr_te = train_test_split(X_r, y_r, test_size=0.2, random_state=42)

    base_regs = [
        LinearRegression(),
        DecisionTreeRegressor(max_depth=5),
        Ridge(alpha=1.0),
    ]
    meta_reg = LinearRegression()
    stack_reg = StackingRegressor(base_regs, meta_reg)
    stack_reg.fit(Xr_tr, yr_tr)
    stack_r2 = r2_score(yr_te, stack_reg.predict(Xr_te))

    print(f"  Stacking R²: {stack_r2:.4f}")
    for m in base_regs:
        m.fit(Xr_tr, yr_tr)
        r2 = r2_score(yr_te, m.predict(Xr_te))
        print(f"    {type(m).__name__}: R²={r2:.4f}")

    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Classifier comparison
    labels = [type(m).__name__ for m in base_models] + ['Voting', 'Stacking']
    accs = individual_accs + [voting_acc, stack_acc]
    colors = ['C0', 'C1', 'C2', 'C3', 'C4']
    axes[0].bar(labels, accs, color=colors)
    axes[0].set_ylabel("Accuracy")
    axes[0].set_title("Classifier Performance")
    axes[0].set_xticklabels(labels, rotation=20, ha='right')
    axes[0].grid(True, axis='y', alpha=0.3)

    # Regressor comparison
    labels_r = [type(m).__name__ for m in base_regs] + ['Stacking']
    r2s = [r2_score(yr_te, m.predict(Xr_te)) for m in base_regs] + [stack_r2]
    axes[1].bar(labels_r, r2s, color=['C0', 'C1', 'C2', 'C4'])
    axes[1].set_ylabel("R² Score")
    axes[1].set_title("Regressor Performance")
    axes[1].grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig("../../assets/phase05/42-stacking.png")
    plt.close()
    print("\nFigure saved to 42-stacking.png")

    # Edge case: different n_folds
    for nf in [2, 3, 5, 10]:
        s = StackingClassifier(base_models, LogisticRegression(max_iter=200), n_folds=nf)
        s.fit(X_tr, y_tr)
        acc = accuracy_score(y_te, s.predict(X_te))
        print(f"  n_folds={nf}: stacking acc={acc:.4f}")

    # Edge case: single base model
    single_stack = StackingClassifier([LogisticRegression(max_iter=200)], LogisticRegression(max_iter=200))
    single_stack.fit(X_tr, y_tr)
    single_acc = accuracy_score(y_te, single_stack.predict(X_te))
    print(f"  Single base model stacking: {single_acc:.4f}")
