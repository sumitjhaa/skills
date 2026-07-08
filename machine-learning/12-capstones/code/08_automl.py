"""
12.08: AutoML System
End-to-end automated machine learning with data profiling,
feature engineering, model selection, HPO, and ensemble.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Optional, Callable, Tuple, Any
from sklearn.datasets import load_breast_cancer, load_iris, load_digits
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import accuracy_score
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')


# ─────────────────────────────────────────────
# Data Profiler
# ─────────────────────────────────────────────

class DataProfiler:
    """Profile a dataset to extract meta-features."""
    def __init__(self):
        self.meta_features = {}

    def profile(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> Dict:
        n_rows, n_cols = X.shape
        self.meta_features = {
            'n_rows': n_rows,
            'n_cols': n_cols,
            'n_missing': int(np.isnan(X).sum()),
            'missing_ratio': float(np.isnan(X).sum() / X.size),
            'n_unique_vals': [len(np.unique(X[:, c])) for c in range(n_cols)],
            'mean_corr': None,
        }

        # Column type detection
        col_types = []
        for c in range(n_cols):
            col = X[:, c]
            unique_vals = len(np.unique(col[~np.isnan(col)]))
            if unique_vals <= 10:
                col_types.append('categorical')
            else:
                col_types.append('numeric')
        self.meta_features['col_types'] = col_types
        self.meta_features['n_categorical'] = col_types.count('categorical')
        self.meta_features['n_numeric'] = col_types.count('numeric')

        if y is not None:
            self.meta_features['n_classes'] = len(np.unique(y))
            self.meta_features['class_balance'] = np.bincount(y.astype(int)) / len(y)

        # Feature correlations
        X_clean = np.nan_to_num(X, 0)
        if n_cols > 1:
            corr = np.corrcoef(X_clean.T)
            triu = np.triu(corr, k=1)
            self.meta_features['mean_abs_corr'] = float(np.abs(triu).mean())
        else:
            self.meta_features['mean_abs_corr'] = 0.0

        return self.meta_features

    def report(self) -> str:
        lines = ["Data Profile:"]
        for k, v in self.meta_features.items():
            lines.append(f"  {k}: {v}")
        return '\n'.join(lines)


# ─────────────────────────────────────────────
# Feature Engineering Pipeline
# ─────────────────────────────────────────────

class FeatureEngineer:
    """Automated feature engineering."""
    def __init__(self):
        self.scaler_mean = None
        self.scaler_std = None
        self.encoders = {}

    def fit_transform(self, X: np.ndarray, col_types: List[str]) -> np.ndarray:
        X_out = X.copy().astype(np.float64)
        n_rows, n_cols = X.shape

        # Handle missing values
        for c in range(n_cols):
            mask = np.isnan(X_out[:, c])
            if mask.any():
                if col_types[c] == 'numeric':
                    X_out[mask, c] = np.nanmean(X_out[:, c])
                else:
                    X_out[mask, c] = 0

        # Scale numeric columns
        self.scaler_mean = np.zeros(n_cols)
        self.scaler_std = np.ones(n_cols)
        for c in range(n_cols):
            if col_types[c] == 'numeric':
                self.scaler_mean[c] = X_out[:, c].mean()
                self.scaler_std[c] = X_out[:, c].std() + 1e-8
                X_out[:, c] = (X_out[:, c] - self.scaler_mean[c]) / self.scaler_std[c]

        # Encode categorical (simple integer encoding)
        for c in range(n_cols):
            if col_types[c] == 'categorical':
                unique = np.unique(X_out[:, c])
                mapping = {v: i for i, v in enumerate(unique)}
                self.encoders[c] = mapping
                X_out[:, c] = np.array([mapping.get(v, -1) for v in X_out[:, c]])

        # Add polynomial features for numeric columns
        numeric_cols = [c for c in range(n_cols) if col_types[c] == 'numeric']
        if len(numeric_cols) >= 2:
            for i in range(min(3, len(numeric_cols))):
                c1 = numeric_cols[i]
                for j in range(i + 1, min(3, len(numeric_cols))):
                    c2 = numeric_cols[j]
                    X_out = np.column_stack([X_out, X_out[:, c1] * X_out[:, c2]])

        # Add squared terms
        for c in numeric_cols[:5]:
            X_out = np.column_stack([X_out, X_out[:, c] ** 2])

        return X_out


# ─────────────────────────────────────────────
# Model Pool
# ─────────────────────────────────────────────

class SimpleLogisticRegression(BaseEstimator, ClassifierMixin):
    """Simple logistic regression with SGD."""
    def __init__(self, lr=0.01, epochs=100, reg=0.001):
        self.lr = lr
        self.epochs = epochs
        self.reg = reg
        self.W = None
        self.b = None

    def fit(self, X, y):
        n, d = X.shape
        n_classes = len(np.unique(y))
        if n_classes > 2:
            self.multi = True
            self.W = np.random.randn(d, n_classes).astype(np.float64) * 0.01
            self.b = np.zeros(n_classes, dtype=np.float64)
        else:
            self.multi = False
            y_bin = (y == 1).astype(np.float64) * 2 - 1
            self.W = np.random.randn(d).astype(np.float64) * 0.01
            self.b = 0.0

        for ep in range(self.epochs):
            if self.multi:
                logits = X @ self.W + self.b
                logits_stable = logits - logits.max(axis=1, keepdims=True)
                probs = np.exp(logits_stable) / np.exp(logits_stable).sum(axis=1, keepdims=True)
                y_onehot = np.eye(n_classes)[y]
                grad_W = X.T @ (probs - y_onehot) / n + self.reg * self.W
                grad_b = (probs - y_onehot).mean(axis=0) + self.reg * self.b
            else:
                logits = X @ self.W + self.b
                probs = 1 / (1 + np.exp(-logits * y_bin))
                loss = -np.log(probs + 1e-15).mean() + self.reg * (self.W ** 2).sum()
                sig = 1 / (1 + np.exp(-logits))
                grad_W = X.T @ ((sig - (y_bin > 0).astype(float)) * y_bin) / n + 2 * self.reg * self.W
                grad_b = ((sig - (y_bin > 0).astype(float)) * y_bin).mean() + 2 * self.reg * self.b

            self.W -= self.lr * grad_W
            self.b -= self.lr * grad_b
        return self

    def predict(self, X):
        if self.multi:
            logits = X @ self.W + self.b
            return np.argmax(logits, axis=1)
        logits = X @ self.W + self.b
        return (logits > 0).astype(int)

    def predict_proba(self, X):
        if self.multi:
            logits = X @ self.W + self.b
            logits_stable = logits - logits.max(axis=1, keepdims=True)
            probs = np.exp(logits_stable) / np.exp(logits_stable).sum(axis=1, keepdims=True)
            return probs
        logits = X @ self.W + self.b
        prob_pos = 1 / (1 + np.exp(-logits))
        return np.column_stack([1 - prob_pos, prob_pos])


class SimpleRandomForest(BaseEstimator, ClassifierMixin):
    """Simplified random forest."""
    def __init__(self, n_trees=20, max_depth=5, max_features='sqrt'):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.max_features = max_features
        self.trees = []

    class _DecisionTree:
        def __init__(self, max_depth, max_features):
            self.max_depth = max_depth
            self.max_features = max_features
            self.tree = None

        def _gini(self, y):
            if len(y) == 0:
                return 0
            _, counts = np.unique(y, return_counts=True)
            probs = counts / len(y)
            return 1 - (probs ** 2).sum()

        def _best_split(self, X, y, n_features):
            best_gain = 0
            best_idx, best_thresh = None, None
            current_gini = self._gini(y)
            for idx in np.random.choice(X.shape[1], n_features, replace=False):
                col = X[:, idx]
                thresholds = np.percentile(col, np.linspace(10, 90, 9))
                for thresh in thresholds:
                    left = y[col <= thresh]
                    right = y[col > thresh]
                    if len(left) == 0 or len(right) == 0:
                        continue
                    gain = current_gini - (len(left) * self._gini(left) + len(right) * self._gini(right)) / len(y)
                    if gain > best_gain:
                        best_gain = gain
                        best_idx = idx
                        best_thresh = thresh
            return best_idx, best_thresh

        def _build(self, X, y, depth=0):
            if depth >= self.max_depth or len(np.unique(y)) == 1 or len(y) < 5:
                counts = np.bincount(y.astype(int))
                return {'type': 'leaf', 'pred': np.argmax(counts), 'counts': counts}

            n_features = max(1, int(np.sqrt(X.shape[1])))
            idx, thresh = self._best_split(X, y, n_features)
            if idx is None:
                counts = np.bincount(y.astype(int))
                return {'type': 'leaf', 'pred': np.argmax(counts), 'counts': counts}

            left_mask = X[:, idx] <= thresh
            right_mask = ~left_mask
            left = self._build(X[left_mask], y[left_mask], depth + 1)
            right = self._build(X[right_mask], y[right_mask], depth + 1)
            return {'type': 'node', 'idx': idx, 'thresh': thresh, 'left': left, 'right': right}

        def fit(self, X, y):
            self.n_features_ = max(1, int(np.sqrt(X.shape[1])))
            self.tree = self._build(X, y)

        def predict_row(self, row, node):
            if node['type'] == 'leaf':
                return node['pred']
            if row[node['idx']] <= node['thresh']:
                return self.predict_row(row, node['left'])
            return self.predict_row(row, node['right'])

        def predict(self, X):
            return np.array([self.predict_row(row, self.tree) for row in X])

    def fit(self, X, y):
        self.trees = []
        n_samples = X.shape[0]
        for _ in range(self.n_trees):
            idx = np.random.choice(n_samples, n_samples, replace=True)
            X_boot = X[idx]
            y_boot = y[idx]
            tree = self._DecisionTree(self.max_depth, self.max_features)
            tree.fit(X_boot, y_boot)
            self.trees.append(tree)
        return self

    def predict(self, X):
        preds = np.array([t.predict(X) for t in self.trees])
        return np.array([np.bincount(preds[:, i]).argmax() for i in range(len(X))])


# ─────────────────────────────────────────────
# Configuration Space
# ─────────────────────────────────────────────

class ConfigSpace:
    def __init__(self):
        self.params = {}

    def add_int(self, name: str, low: int, high: int):
        self.params[name] = {'type': 'int', 'low': low, 'high': high}

    def add_float(self, name: str, low: float, high: float):
        self.params[name] = {'type': 'float', 'low': low, 'high': high}

    def add_categorical(self, name: str, choices: List):
        self.params[name] = {'type': 'categorical', 'choices': choices}

    def sample(self) -> Dict:
        config = {}
        for name, spec in self.params.items():
            if spec['type'] == 'int':
                config[name] = np.random.randint(spec['low'], spec['high'] + 1)
            elif spec['type'] == 'float':
                config[name] = np.random.uniform(spec['low'], spec['high'])
            elif spec['type'] == 'categorical':
                config[name] = np.random.choice(spec['choices'])
        return config

    def get_neighbors(self, config: Dict, radius: float = 0.1) -> Dict:
        new_config = {}
        for name, spec in self.params.items():
            if spec['type'] == 'int':
                delta = np.random.randint(-max(1, int((spec['high'] - spec['low']) * radius)),
                                          max(1, int((spec['high'] - spec['low']) * radius)) + 1)
                new_config[name] = np.clip(config[name] + delta, spec['low'], spec['high'])
            elif spec['type'] == 'float':
                delta = np.random.uniform(-(spec['high'] - spec['low']) * radius,
                                          (spec['high'] - spec['low']) * radius)
                new_config[name] = np.clip(config[name] + delta, spec['low'], spec['high'])
            elif spec['type'] == 'categorical':
                if np.random.random() < 0.5:
                    new_config[name] = np.random.choice(spec['choices'])
                else:
                    new_config[name] = config[name]
        return new_config


# ─────────────────────────────────────────────
# Hyperparameter Optimization
# ─────────────────────────────────────────────

class GPRegressor:
    """Gaussian Process surrogate model (simplified)."""
    def __init__(self, length_scale=1.0, noise=0.01):
        self.length_scale = length_scale
        self.noise = noise
        self.X_train = None
        self.y_train = None

    def _rbf_kernel(self, x1, x2):
        dist2 = np.sum((x1[:, None] - x2[None, :]) ** 2, axis=-1)
        return np.exp(-0.5 * dist2 / self.length_scale ** 2)

    def fit(self, X, y):
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def predict(self, X):
        X = np.array(X)
        K = self._rbf_kernel(self.X_train, self.X_train) + self.noise * np.eye(len(self.X_train))
        K_s = self._rbf_kernel(self.X_train, X)
        K_ss = self._rbf_kernel(X, X) + self.noise

        K_inv = np.linalg.inv(K)
        mu = K_s.T @ K_inv @ self.y_train
        sigma = K_ss - K_s.T @ K_inv @ K_s
        sigma = np.maximum(np.diag(sigma), 0)
        return mu, np.sqrt(sigma)

    def expected_improvement(self, X, best_y):
        mu, sigma = self.predict(X)
        with np.errstate(divide='warn'):
            imp = mu - best_y
            Z = imp / (sigma + 1e-10)
            ei = imp * (0.5 * (1 + np.math.erf(Z / np.sqrt(2)))) + \
                 sigma * np.exp(-Z ** 2 / 2) / np.sqrt(2 * np.pi)
        return ei


class BayesianOptimizer:
    """Bayesian optimization with GP surrogate."""
    def __init__(self, config_space: ConfigSpace, objective: Callable,
                 n_init: int = 10, n_iter: int = 30):
        self.config_space = config_space
        self.objective = objective
        self.n_init = n_init
        self.n_iter = n_iter
        self.trials = []
        self.gp = GPRegressor()

    def _config_to_vector(self, config):
        vec = []
        for name, spec in self.config_space.params.items():
            val = config[name]
            if spec['type'] == 'categorical':
                choices = spec['choices']
                vec.extend([1.0 if val == c else 0.0 for c in choices])
            else:
                vec.append((val - spec['low']) / (spec['high'] - spec['low'] + 1e-10))
        return np.array(vec)

    def optimize(self) -> Tuple[Dict, float]:
        # Initial random trials
        for _ in range(self.n_init):
            config = self.config_space.sample()
            score = self.objective(config)
            self.trials.append((config, score))

        best_config, best_score = max(self.trials, key=lambda t: t[1])

        for it in range(self.n_iter):
            X_train = np.array([self._config_to_vector(t[0]) for t in self.trials])
            y_train = np.array([t[1] for t in self.trials])
            self.gp.fit(X_train, y_train)

            best_candidate = None
            best_ei = -np.inf
            for _ in range(100):
                candidate = self.config_space.sample()
                x = self._config_to_vector(candidate)
                ei = self.gp.expected_improvement(x.reshape(1, -1), best_score)
                if ei > best_ei:
                    best_ei = ei
                    best_candidate = candidate

            score = self.objective(best_candidate)
            self.trials.append((best_candidate, score))

            if score > best_score:
                best_config, best_score = best_candidate, score

            if (it + 1) % 10 == 0:
                print(f"    BO Iter {it+1}/{self.n_iter} | Best: {best_score:.4f} | EI: {best_ei:.4f}")

        return best_config, best_score


# ─────────────────────────────────────────────
# Model Builder
# ─────────────────────────────────────────────

def build_model(model_type: str, config: Dict) -> BaseEstimator:
    if model_type == 'logistic':
        return SimpleLogisticRegression(
            lr=config.get('lr', 0.01),
            epochs=config.get('epochs', 100),
            reg=config.get('reg', 0.001),
        )
    elif model_type == 'random_forest':
        return SimpleRandomForest(
            n_trees=config.get('n_trees', 20),
            max_depth=config.get('max_depth', 5),
            max_features='sqrt',
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")


# ─────────────────────────────────────────────
# AutoML Pipeline
# ─────────────────────────────────────────────

class AutoML:
    """End-to-end AutoML system."""
    def __init__(self, time_budget: int = 60):
        self.time_budget = time_budget
        self.profiler = DataProfiler()
        self.engineer = FeatureEngineer()
        self.best_model = None
        self.best_config = None
        self.best_score = -np.inf
        self.leaderboard = []
        self.models_pool = {}

    def _score_model(self, model_type: str, config: Dict,
                     X: np.ndarray, y: np.ndarray) -> float:
        try:
            model = build_model(model_type, config)
            cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
            scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
            return float(scores.mean())
        except Exception as e:
            return -1.0

    def fit(self, X: np.ndarray, y: np.ndarray):
        print("[AutoML] Profiling data...")
        meta = self.profiler.profile(X, y)

        print("[AutoML] Engineering features...")
        X_feat = self.engineer.fit_transform(X, meta['col_types'])
        print(f"        {X.shape[1]} → {X_feat.shape[1]} features")

        # Model selection phase: try each model type with default params
        print("[AutoML] Model selection phase...")
        defaults = {
            'logistic': {'lr': 0.01, 'epochs': 100, 'reg': 0.001},
            'random_forest': {'n_trees': 20, 'max_depth': 5},
        }

        for model_type in ['logistic', 'random_forest']:
            score = self._score_model(model_type, defaults[model_type], X_feat, y)
            print(f"        {model_type}: {score:.4f}")
            self.leaderboard.append({
                'model_type': model_type,
                'config': defaults[model_type],
                'score': score,
            })

        # HPO for best model type
        best_type = max(self.leaderboard, key=lambda x: x['score'])['model_type']
        print(f"[AutoML] Optimizing {best_type}...")

        cs = ConfigSpace()
        if best_type == 'logistic':
            cs.add_float('lr', 1e-4, 1e-1)
            cs.add_int('epochs', 50, 500)
            cs.add_float('reg', 1e-5, 1e-1)
        else:
            cs.add_int('n_trees', 10, 100)
            cs.add_int('max_depth', 2, 10)

        objective = lambda c: self._score_model(best_type, c, X_feat, y)
        bo = BayesianOptimizer(cs, objective, n_init=5, n_iter=15)
        best_config, best_score = bo.optimize()

        self.best_config = {'model_type': best_type, **best_config}
        self.best_score = best_score
        self.best_model = build_model(best_type, best_config)
        self.best_model.fit(X_feat, y)

        # Add BO trials to leaderboard
        for config, score in bo.trials:
            self.leaderboard.append({
                'model_type': best_type,
                'config': config,
                'score': score,
            })

        self.leaderboard = sorted(self.leaderboard, key=lambda x: x['score'], reverse=True)

        print(f"\n[AutoML] Best: {self.best_config['model_type']} "
              f"with score {self.best_score:.4f}")
        if best_type == 'logistic':
            print(f"         lr={self.best_config.get('lr', 'N/A'):.4f}, "
                  f"epochs={self.best_config.get('epochs', 'N/A')}, "
                  f"reg={self.best_config.get('reg', 'N/A'):.6f}")

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        meta = self.profiler.profile(X)
        X_feat = self.engineer.fit_transform(X, meta['col_types'])
        return self.best_model.predict(X_feat)

    def leaderboard_table(self, n: int = 10) -> str:
        lines = [f"{'Rank':<6}{'Model':<20}{'Score':<10}",
                 '-' * 36]
        for i, entry in enumerate(self.leaderboard[:n]):
            lines.append(f"{i+1:<6}{entry['model_type']:<20}{entry['score']:<10.4f}")
        return '\n'.join(lines)

    def feature_importance(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Simple permutation feature importance."""
        meta = self.profiler.profile(X, y)
        X_feat = self.engineer.fit_transform(X, meta['col_types'])
        baseline = accuracy_score(y, self.best_model.predict(X_feat))
        importances = []

        for c in range(X_feat.shape[1]):
            X_perm = X_feat.copy()
            np.random.shuffle(X_perm[:, c])
            perm_score = accuracy_score(y, self.best_model.predict(X_perm))
            importances.append(baseline - perm_score)

        return np.array(importances)


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    np.random.seed(42)

    print("=" * 60)
    print("AUTOML SYSTEM")
    print("=" * 60)

    # Load datasets
    datasets = {
        'Breast Cancer': load_breast_cancer(),
        'Iris': load_iris(),
        'Digits (binary)': load_digits(n_class=2),
    }

    all_results = {}

    for name, data in datasets.items():
        print(f"\n{'─' * 40}")
        print(f"Dataset: {name}")
        print(f"{'─' * 40}")

        X, y = data.data[:200], data.target[:200]

        # AutoML
        automl = AutoML(time_budget=30)
        automl.fit(X, y)

        print(f"\n  Leaderboard:")
        print(automl.leaderboard_table(5))

        # Feature importance
        importances = automl.feature_importance(X, y)
        top_k = min(5, len(importances))
        top_idx = np.argsort(importances)[-top_k:][::-1]
        print(f"\n  Top {top_k} features by importance:")
        for idx in top_idx:
            print(f"    Feature {idx}: {importances[idx]:.4f}")

        all_results[name] = {
            'best_score': automl.best_score,
            'best_config': automl.best_config,
        }

    # Summary plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Performance by dataset
    names = list(all_results.keys())
    scores = [all_results[n]['best_score'] for n in names]
    axes[0].bar(names, scores, color=['steelblue', 'seagreen', 'coral'])
    axes[0].set_ylabel('Best CV Accuracy')
    axes[0].set_title('AutoML Performance by Dataset')
    axes[0].set_ylim(0.5, 1.0)
    for i, v in enumerate(scores):
        axes[0].text(i, v + 0.01, f'{v:.3f}', ha='center')
    axes[0].grid(alpha=0.3, axis='y')

    # Feature importance distribution
    automl_final = AutoML()
    X_all, y_all = load_breast_cancer()['data'][:200], load_breast_cancer()['target'][:200]
    automl_final.fit(X_all, y_all)
    imp = automl_final.feature_importance(X_all, y_all)
    axes[1].hist(imp[imp > 0], bins=20, color='steelblue', edgecolor='black', alpha=0.7)
    axes[1].set_xlabel('Importance')
    axes[1].set_ylabel('Count')
    axes[1].set_title('Feature Importance Distribution')
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('../../assets/phase12/08_automl_results.png', dpi=150)
    plt.close()
    print("\nSaved 08_automl_results.png")


if __name__ == '__main__':
    main()
