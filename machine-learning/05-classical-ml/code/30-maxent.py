"""Maximum Entropy (MaxEnt) classifier from scratch via GIS with L2 regularization."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class MaxEnt:
    def __init__(self, max_iter=100, lr=0.01, reg=0.0):
        self.max_iter = max_iter
        self.lr = lr
        self.reg = reg

    def fit(self, X, y):
        n, d = X.shape
        self.classes_ = np.unique(y)
        K = len(self.classes_)
        self.w = np.zeros((K, d))
        self.loss_history = []

        for iteration in range(self.max_iter):
            probs = self.predict_proba(X)
            y_onehot = np.zeros((n, K))
            y_onehot[np.arange(n), np.searchsorted(self.classes_, y)] = 1

            grad = X.T @ (y_onehot - probs) / n - self.reg * self.w.T
            self.w += self.lr * grad.T

            loss = -np.mean(np.log(probs[np.arange(n), np.searchsorted(self.classes_, y)] + 1e-15))
            loss += 0.5 * self.reg * np.sum(self.w**2)
            self.loss_history.append(loss)

            if np.linalg.norm(grad) < 1e-5:
                print(f"  MaxEnt converged in {iteration + 1} iterations")
                break

    def predict_proba(self, X):
        scores = X @ self.w.T
        scores = scores - scores.max(axis=1, keepdims=True)
        exp_scores = np.exp(scores)
        return exp_scores / exp_scores.sum(axis=1, keepdims=True)

    def predict(self, X):
        return self.classes_[np.argmax(self.predict_proba(X), axis=1)]

def compare_datasets():
    configs = [
        ("Binary (easy)", 500, 10, 2, 8, 0.0),
        ("Binary (noisy)", 500, 10, 2, 3, 0.5),
        ("Multi-class", 500, 10, 4, 6, 0.1),
    ]
    for name, n, d, k, inf, flip in configs:
        X, y = make_classification(n_samples=n, n_features=d, n_classes=k,
                                   n_informative=inf, flip_y=flip, random_state=42)
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
        me = MaxEnt(max_iter=300, lr=0.01, reg=0.01)
        me.fit(X_tr, y_tr)
        acc = accuracy_score(y_te, me.predict(X_te))
        from sklearn.linear_model import LogisticRegression
        lr = LogisticRegression(max_iter=300).fit(X_tr, y_tr)
        sk_acc = accuracy_score(y_te, lr.predict(X_te))
        print(f"  {name}: MaxEnt={acc:.4f}, sklearn LR={sk_acc:.4f}")

if __name__ == "__main__":
    np.random.seed(42)
    print("=== MaxEnt Classifier ===")

    X, y = make_classification(n_samples=500, n_features=10, n_classes=3,
                               n_informative=5, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    # Without regularization
    me0 = MaxEnt(max_iter=200, lr=0.01, reg=0.0)
    me0.fit(X_tr, y_tr)
    acc0 = accuracy_score(y_te, me0.predict(X_te))

    # With regularization
    me1 = MaxEnt(max_iter=200, lr=0.01, reg=0.1)
    me1.fit(X_tr, y_tr)
    acc1 = accuracy_score(y_te, me1.predict(X_te))

    print(f"  MaxEnt (no reg):  {acc0:.4f}")
    print(f"  MaxEnt (L2=0.1): {acc1:.4f}")

    from sklearn.linear_model import LogisticRegression
    sk = LogisticRegression(max_iter=200, C=10.0).fit(X_tr, y_tr)
    print(f"  sklearn LR:       {accuracy_score(y_te, sk.predict(X_te)):.4f}")

    compare_datasets()

    # Convergence plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for reg, c in zip([0.0, 0.01, 0.1], ['C0', 'C1', 'C2']):
        me = MaxEnt(max_iter=200, lr=0.01, reg=reg)
        me.fit(X_tr, y_tr)
        axes[0].plot(me.loss_history, c=c, label=f'reg={reg}')
    axes[0].set_xlabel("Iteration")
    axes[0].set_ylabel("Loss")
    axes[0].set_title("MaxEnt Convergence")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Weight comparison
    axes[1].plot(me0.w.ravel(), 'o-', alpha=0.5, label='no reg')
    axes[1].plot(me1.w.ravel(), 's-', alpha=0.5, label='L2=0.1')
    axes[1].set_xlabel("Weight index")
    axes[1].set_ylabel("Weight value")
    axes[1].set_title("MaxEnt Weights")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("../../assets/phase05/30-maxent.png")
    plt.close()
    print("\nFigure saved to 30-maxent.png")

    # Edge case: single class
    print("\n=== Edge Cases ===")
    X1 = np.random.randn(50, 3)
    y1 = np.zeros(50, dtype=int)
    try:
        me_edge = MaxEnt(max_iter=50)
        me_edge.fit(X1, y1)
        print(f"  Single class: OK (probas shape={me_edge.predict_proba(X1[:2]).shape})")
    except Exception as e:
        print(f"  Single class error: {e}")

    # Edge case: small data
    X2 = np.array([[0, 0], [1, 1], [2, 0], [3, 1]])
    y2 = np.array([0, 0, 1, 1])
    me_small = MaxEnt(max_iter=100, lr=0.01)
    me_small.fit(X2, y2)
    print(f"  Small data acc: {accuracy_score(y2, me_small.predict(X2)):.4f}")
