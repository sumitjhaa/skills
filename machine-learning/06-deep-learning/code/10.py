"""06.10 - Optimizer Zoo: SGD, Momentum, NAG, AdaGrad, RMSprop, Adam, AdamW"""

import numpy as np
import matplotlib.pyplot as plt


class SGD:
    def __init__(self, lr=0.01):
        self.lr = lr

    def step(self, params, grads):
        return [p - self.lr * g for p, g in zip(params, grads)]


class Momentum:
    def __init__(self, lr=0.01, beta=0.9):
        self.lr = lr
        self.beta = beta
        self.v = None

    def step(self, params, grads):
        if self.v is None:
            self.v = [np.zeros_like(p) for p in params]
        updates = []
        for i, (p, g) in enumerate(zip(params, grads)):
            self.v[i] = self.beta * self.v[i] + g
            updates.append(p - self.lr * self.v[i])
        return updates


class NAG:
    def __init__(self, lr=0.01, beta=0.9):
        self.lr = lr
        self.beta = beta
        self.v = None

    def step(self, params, grads):
        if self.v is None:
            self.v = [np.zeros_like(p) for p in params]
        updates = []
        for i, (p, g) in enumerate(zip(params, grads)):
            self.v[i] = self.beta * self.v[i] + g
            updates.append(p - self.lr * (self.beta * self.v[i] + g))
        return updates


class AdaGrad:
    def __init__(self, lr=0.01, eps=1e-8):
        self.lr = lr
        self.eps = eps
        self.G = None

    def step(self, params, grads):
        if self.G is None:
            self.G = [np.zeros_like(p) for p in params]
        updates = []
        for i, (p, g) in enumerate(zip(params, grads)):
            self.G[i] += g ** 2
            updates.append(p - self.lr * g / (np.sqrt(self.G[i]) + self.eps))
        return updates


class RMSprop:
    def __init__(self, lr=0.001, beta=0.9, eps=1e-8):
        self.lr = lr
        self.beta = beta
        self.eps = eps
        self.v = None

    def step(self, params, grads):
        if self.v is None:
            self.v = [np.zeros_like(p) for p in params]
        updates = []
        for i, (p, g) in enumerate(zip(params, grads)):
            self.v[i] = self.beta * self.v[i] + (1 - self.beta) * g ** 2
            updates.append(p - self.lr * g / (np.sqrt(self.v[i]) + self.eps))
        return updates


class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m = None
        self.v = None
        self.t = 0

    def step(self, params, grads):
        if self.m is None:
            self.m = [np.zeros_like(p) for p in params]
            self.v = [np.zeros_like(p) for p in params]
        self.t += 1
        updates = []
        for i, (p, g) in enumerate(zip(params, grads)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * g ** 2
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)
            updates.append(p - self.lr * m_hat / (np.sqrt(v_hat) + self.eps))
        return updates


class AdamW:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8, weight_decay=0.01):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.weight_decay = weight_decay
        self.m = None
        self.v = None
        self.t = 0

    def step(self, params, grads):
        if self.m is None:
            self.m = [np.zeros_like(p) for p in params]
            self.v = [np.zeros_like(p) for p in params]
        self.t += 1
        updates = []
        for i, (p, g) in enumerate(zip(params, grads)):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * g ** 2
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)
            decay = self.lr * self.weight_decay * p
            updates.append(p - self.lr * m_hat / (np.sqrt(v_hat) + self.eps) - decay)
        return updates


def quadratic_optimization(opt_fn, n_steps=50):
    x = np.array([3.0, -2.0])
    history = [x.copy()]
    for _ in range(n_steps):
        grad = np.array([2 * x[0], 4 * x[1]])
        opt = opt_fn
        if hasattr(opt, 'step'):
            x = np.array(opt.step([x], [grad])[0])
        history.append(x.copy())
    return np.array(history)


if __name__ == "__main__":
    optimizers = [
        ("SGD", SGD(lr=0.1)),
        ("Momentum", Momentum(lr=0.1, beta=0.9)),
        ("NAG", NAG(lr=0.1, beta=0.9)),
        ("AdaGrad", AdaGrad(lr=0.5)),
        ("RMSprop", RMSprop(lr=0.1)),
        ("Adam", Adam(lr=0.1)),
        ("AdamW", AdamW(lr=0.1, weight_decay=0.01)),
    ]

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()
    x_opt = np.array([0.0, 0.0])

    for idx, (name, opt) in enumerate(optimizers):
        x = np.array([3.0, -2.0])
        history = [x.copy()]
        for step in range(50):
            grad = np.array([2 * x[0], 4 * x[1]])
            x = np.array(opt.step([x], [grad])[0])
            history.append(x.copy())
        history = np.array(history)
        dists = np.linalg.norm(history - x_opt, axis=1)
        axes[idx].plot(dists, linewidth=2)
        axes[idx].set_title(f"{name}\nFinal dist: {dists[-1]:.4f}")
        axes[idx].set_xlabel("Step")
        axes[idx].set_ylabel("Distance to optimum")
        axes[idx].set_yscale("log")
        axes[idx].grid(True, alpha=0.3)

        print(f"{name:12s}: final distance = {dists[-1]:.6f}")

    axes[7].axis("off")
    plt.tight_layout()
    plt.savefig("../../assets/phase06/optimizers.png")
    plt.close()
    print("\nAll optimizers implemented and tested on quadratic minimization.")
