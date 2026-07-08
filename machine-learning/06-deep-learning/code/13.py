"""06.13 - Regularization: L1/L2, Dropout, DropConnect, Stochastic Depth"""

import numpy as np
import matplotlib.pyplot as plt


def l1_penalty(params, lam=0.01):
    return lam * sum(np.sum(np.abs(p)) for p in params)

def l2_penalty(params, lam=0.01):
    return 0.5 * lam * sum(np.sum(p ** 2) for p in params)


class Dropout:
    def __init__(self, rate=0.5):
        self.rate = rate
        self.mask = None
        self.training = True

    def forward(self, x):
        if not self.training:
            return x
        self.mask = np.random.binomial(1, 1 - self.rate, x.shape) / (1 - self.rate)
        return x * self.mask

    def backward(self, dout):
        return dout * self.mask if self.training else dout


class DropConnect:
    def __init__(self, rate=0.5):
        self.rate = rate
        self.mask = None

    def apply(self, W):
        self.mask = np.random.binomial(1, 1 - self.rate, W.shape) / (1 - self.rate)
        return W * self.mask


class StochasticDepth:
    def __init__(self, prob=0.5):
        self.prob = prob
        self.active = True

    def forward(self, x, layer_output):
        if not self.active or np.random.random() > self.prob:
            return layer_output
        return x


if __name__ == "__main__":
    np.random.seed(42)

    weights = [np.random.randn(10, 20), np.random.randn(20, 5)]
    print(f"L1 penalty: {l1_penalty(weights, lam=0.01):.4f}")
    print(f"L2 penalty: {l2_penalty(weights, lam=0.01):.4f}")

    x = np.random.randn(4, 8)
    dropout = Dropout(rate=0.5)
    out_train = dropout.forward(x)
    dropout.training = False
    out_eval = dropout.forward(x)
    print(f"\nDropout - training: {np.count_nonzero(out_train)}/{x.size} nonzero "
          f"(expected ~{int(x.size * 0.5)})")
    print(f"Dropout - eval:     {np.count_nonzero(out_eval)}/{x.size} nonzero (all should remain)")

    dc = DropConnect(rate=0.3)
    W = np.random.randn(16, 32)
    W_dropped = dc.apply(W)
    print(f"\nDropConnect: {np.count_nonzero(W_dropped)}/{W.size} nonzero "
          f"(expected ~{int(W.size * 0.7)})")

    sd = StochasticDepth(prob=0.8)
    skip_in = np.array([1.0])
    block_out = np.array([2.0])
    results = [sd.forward(skip_in, block_out) for _ in range(1000)]
    kept = sum(1 for r in results if r[0] == 2.0)
    skipped_ratio = 1 - kept / 1000
    print(f"StochasticDepth: skipped {skipped_ratio:.1%} (expected ~20%)")

    print("\nAll regularization techniques implemented.")
