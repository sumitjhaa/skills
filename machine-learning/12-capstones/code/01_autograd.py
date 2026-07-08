"""
12.01: Autograd from Scratch + Neural Net
A reverse-mode automatic differentiation engine ("PyTorch-lite")
that trains a multi-layer perceptron on MNIST.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import softmax, log_softmax
from typing import List, Optional, Set, Tuple


# ─────────────────────────────────────────────
# Tensor class
# ─────────────────────────────────────────────

class Tensor:
    def __init__(self, data: np.ndarray, requires_grad: bool = False,
                 _children: Tuple = ()):
        self.data = np.asarray(data, dtype=np.float64)
        self.requires_grad = requires_grad
        self.grad: Optional[np.ndarray] = np.zeros_like(self.data) if requires_grad else None
        self._backward = lambda: None
        self._prev: Set['Tensor'] = set(_children)

    @staticmethod
    def _ensure_tensor(x):
        if isinstance(x, Tensor):
            return x
        return Tensor(x)

    def __add__(self, other):
        other = Tensor._ensure_tensor(other)
        out = Tensor(self.data + other.data,
                     requires_grad=self.requires_grad or other.requires_grad,
                     _children=(self, other))
        if out.requires_grad:
            def _backward():
                if self.requires_grad:
                    self.grad += out.grad
                if other.requires_grad:
                    other.grad += out.grad
            out._backward = _backward
        return out

    def __mul__(self, other):
        other = Tensor._ensure_tensor(other)
        out = Tensor(self.data * other.data,
                     requires_grad=self.requires_grad or other.requires_grad,
                     _children=(self, other))
        if out.requires_grad:
            def _backward():
                if self.requires_grad:
                    self.grad += out.grad * other.data
                if other.requires_grad:
                    other.grad += out.grad * self.data
            out._backward = _backward
        return out

    def __sub__(self, other):
        return self + (-other)

    def __neg__(self):
        return self * Tensor(np.array(-1.0))

    def __truediv__(self, other):
        return self * (other ** -1)

    def __pow__(self, power):
        assert isinstance(power, (int, float)), "pow only supports scalar exponents"
        out = Tensor(self.data ** power,
                     requires_grad=self.requires_grad,
                     _children=(self,))
        if out.requires_grad:
            def _backward():
                self.grad += out.grad * (power * (self.data ** (power - 1)))
            out._backward = _backward
        return out

    def __matmul__(self, other):
        other = Tensor._ensure_tensor(other)
        out = Tensor(self.data @ other.data,
                     requires_grad=self.requires_grad or other.requires_grad,
                     _children=(self, other))
        if out.requires_grad:
            def _backward():
                if self.requires_grad:
                    self.grad += out.grad @ other.data.T
                if other.requires_grad:
                    other.grad += self.data.T @ out.grad
            out._backward = _backward
        return out

    def exp(self):
        out = Tensor(np.exp(self.data),
                     requires_grad=self.requires_grad,
                     _children=(self,))
        if out.requires_grad:
            def _backward():
                self.grad += out.grad * out.data
            out._backward = _backward
        return out

    def log(self):
        out = Tensor(np.log(self.data),
                     requires_grad=self.requires_grad,
                     _children=(self,))
        if out.requires_grad:
            def _backward():
                self.grad += out.grad / self.data
            out._backward = _backward
        return out

    def sum(self):
        out = Tensor(np.array(self.data.sum()),
                     requires_grad=self.requires_grad,
                     _children=(self,))
        if out.requires_grad:
            def _backward():
                self.grad += out.grad * np.ones_like(self.data)
            out._backward = _backward
        return out

    def mean(self):
        out = Tensor(np.array(self.data.mean()),
                     requires_grad=self.requires_grad,
                     _children=(self,))
        if out.requires_grad:
            def _backward():
                self.grad += out.grad * np.ones_like(self.data) / self.data.size
            out._backward = _backward
        return out

    def reshape(self, *shape):
        out = Tensor(self.data.reshape(shape),
                     requires_grad=self.requires_grad,
                     _children=(self,))
        if out.requires_grad:
            def _backward():
                self.grad += out.grad.reshape(self.data.shape)
            out._backward = _backward
        return out

    def relu(self):
        out = Tensor(np.maximum(0, self.data),
                     requires_grad=self.requires_grad,
                     _children=(self,))
        if out.requires_grad:
            def _backward():
                self.grad += out.grad * (self.data > 0).astype(np.float64)
            out._backward = _backward
        return out

    def __repr__(self):
        return f"Tensor(data={self.data.shape}, grad={'req' if self.requires_grad else 'none'})"

    # ── Topological sort and backward ──

    def backward(self):
        if self.grad is None:
            return
        self.grad = np.ones_like(self.data)
        topo = []
        visited = set()

        def _build(v):
            if v not in visited:
                visited.add(v)
                for p in v._prev:
                    _build(p)
                topo.append(v)
        _build(self)

        for v in reversed(topo):
            v._backward()


# ─────────────────────────────────────────────
# Modules
# ─────────────────────────────────────────────

class Module:
    def parameters(self) -> List[Tensor]:
        return []

    def zero_grad(self):
        for p in self.parameters():
            if p.grad is not None:
                p.grad.fill(0)


class Linear(Module):
    def __init__(self, in_features: int, out_features: int):
        scale = np.sqrt(2.0 / in_features)
        self.W = Tensor(
            np.random.randn(in_features, out_features).astype(np.float64) * scale,
            requires_grad=True,
        )
        self.b = Tensor(
            np.zeros(out_features, dtype=np.float64),
            requires_grad=True,
        )

    def forward(self, x: Tensor) -> Tensor:
        return x @ self.W + self.b

    def parameters(self) -> List[Tensor]:
        return [self.W, self.b]


class ReLU(Module):
    def forward(self, x: Tensor) -> Tensor:
        return x.relu()


class Sequential(Module):
    def __init__(self, *layers):
        self.layers = layers

    def forward(self, x: Tensor) -> Tensor:
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def parameters(self) -> List[Tensor]:
        params = []
        for layer in self.layers:
            params.extend(layer.parameters())
        return params


# ─────────────────────────────────────────────
# Loss functions
# ─────────────────────────────────────────────

class MSELoss:
    def forward(self, pred: Tensor, target: Tensor) -> Tensor:
        diff = pred - target
        return (diff ** 2).mean()


class CrossEntropyLoss:
    def forward(self, logits: Tensor, targets: np.ndarray) -> Tensor:
        """
        logits: (B, C) Tensor
        targets: (B,) int array of class indices
        """
        B, C = logits.data.shape
        # stabilized log-softmax
        logits_stable = logits.data - logits.data.max(axis=1, keepdims=True)
        log_probs = logits_stable - np.log(np.sum(np.exp(logits_stable), axis=1, keepdims=True))
        loss_val = -log_probs[np.arange(B), targets].mean()
        # Create a Tensor for the loss
        loss = Tensor(np.array(loss_val), requires_grad=True)

        # Store for backward
        probs = np.exp(log_probs)
        d_logits = probs.copy()
        d_logits[np.arange(B), targets] -= 1
        d_logits /= B

        def _backward():
            logits.grad += d_logits * loss.grad
        loss._backward = _backward
        loss._prev = {logits}
        return loss


# ─────────────────────────────────────────────
# Optimizers
# ─────────────────────────────────────────────

class SGD:
    def __init__(self, params: List[Tensor], lr: float = 0.01):
        self.params = params
        self.lr = lr

    def step(self):
        for p in self.params:
            if p.requires_grad and p.grad is not None:
                p.data -= self.lr * p.grad

    def zero_grad(self):
        for p in self.params:
            if p.grad is not None:
                p.grad.fill(0)


class Adam:
    def __init__(self, params: List[Tensor], lr: float = 1e-3,
                 betas: Tuple[float, float] = (0.9, 0.999), eps: float = 1e-8):
        self.params = params
        self.lr = lr
        self.b1, self.b2 = betas
        self.eps = eps
        self.t = 0
        self.m = [np.zeros_like(p.data) for p in params]
        self.v = [np.zeros_like(p.data) for p in params]

    def step(self):
        self.t += 1
        for i, p in enumerate(self.params):
            if not p.requires_grad or p.grad is None:
                continue
            g = p.grad
            self.m[i] = self.b1 * self.m[i] + (1 - self.b1) * g
            self.v[i] = self.b2 * self.v[i] + (1 - self.b2) * (g ** 2)
            m_hat = self.m[i] / (1 - self.b1 ** self.t)
            v_hat = self.v[i] / (1 - self.b2 ** self.t)
            p.data -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

    def zero_grad(self):
        for p in self.params:
            if p.grad is not None:
                p.grad.fill(0)


# ─────────────────────────────────────────────
# Data loading (MNIST simulation)
# ─────────────────────────────────────────────

def load_mnist_simulation(n_samples: int = 2000):
    """Generate synthetic MNIST-like data: 8x8 images with digits."""
    from sklearn.datasets import load_digits
    digits = load_digits()
    X = digits.images[:n_samples]  # (n, 8, 8)
    y = digits.target[:n_samples]
    # Normalize to [0, 1]
    X = X.reshape(n_samples, -1).astype(np.float64) / 16.0
    return X, y


def one_hot(y: np.ndarray, num_classes: int = 10) -> np.ndarray:
    return np.eye(num_classes)[y]


# ─────────────────────────────────────────────
# Training
# ─────────────────────────────────────────────

def train():
    np.random.seed(42)
    X, y = load_mnist_simulation(1500)
    X_val, y_val = load_mnist_simulation(200)
    X_val, y_val = X_val[1500:], y_val[1500:]

    B, D = X.shape
    num_classes = 10

    model = Sequential(
        Linear(D, 64),
        ReLU(),
        Linear(64, 32),
        ReLU(),
        Linear(32, num_classes),
    )
    loss_fn = CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=1e-3)

    batch_size = 64
    epochs = 30
    losses = []
    accs = []

    for epoch in range(epochs):
        # Shuffle
        perm = np.random.permutation(B)
        X_shuf, y_shuf = X[perm], y[perm]
        epoch_loss = 0.0
        n_batches = 0

        for i in range(0, B, batch_size):
            X_batch = X_shuf[i:i + batch_size]
            y_batch = y_shuf[i:i + batch_size]

            # Forward
            logits = model.forward(Tensor(X_batch))
            loss = loss_fn.forward(logits, y_batch)

            # Backward
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            epoch_loss += loss.data.item()
            n_batches += 1

        # Validation accuracy
        logits_val = model.forward(Tensor(X_val))
        preds = np.argmax(logits_val.data, axis=1)
        acc = (preds == y_val).mean()

        avg_loss = epoch_loss / n_batches
        losses.append(avg_loss)
        accs.append(acc)
        if (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch+1:2d}/{epochs} | Loss: {avg_loss:.4f} | Val Acc: {acc:.4f}")

    # Final accuracy on full training set
    logits_train = model.forward(Tensor(X))
    preds_train = np.argmax(logits_train.data, axis=1)
    train_acc = (preds_train == y).mean()
    print(f"\nFinal Train Acc: {train_acc:.4f} | Final Val Acc: {accs[-1]:.4f}")

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    ax1.plot(losses, 'b-', linewidth=2)
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('Training Loss')
    ax1.grid(alpha=0.3)

    ax2.plot(accs, 'g-', linewidth=2)
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Validation Accuracy')
    ax2.set_title('Validation Accuracy')
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig('../../assets/phase12/01_autograd_results.png', dpi=150)
    plt.close()
    print("Saved 01_autograd_results.png")

    # Gradient checking
    print("\n--- Gradient Check ---")
    x_check = Tensor(np.random.randn(4, D) * 0.1, requires_grad=True)
    out = model.forward(x_check)
    loss_check = out.sum()
    loss_check.backward()

    # Finite difference check
    eps = 1e-6
    idx = (0, 0)
    x_check.data[idx] += eps
    out_plus = model.forward(Tensor(x_check.data)).sum().data.item()
    x_check.data[idx] -= 2 * eps
    out_minus = model.forward(Tensor(x_check.data)).sum().data.item()
    x_check.data[idx] += eps
    fd_grad = (out_plus - out_minus) / (2 * eps)
    auto_grad = x_check.grad[idx]
    rel_err = abs(fd_grad - auto_grad) / (abs(fd_grad) + abs(auto_grad) + 1e-8)
    print(f"Finite difference grad: {fd_grad:.6f}")
    print(f"Autograd grad:         {auto_grad:.6f}")
    print(f"Relative error:        {rel_err:.6e}")
    print(f"Gradient check {'PASSED' if rel_err < 1e-4 else 'FAILED'}")

    return model, losses, accs


if __name__ == '__main__':
    model, losses, accs = train()
