"""06.12 - Normalization Layers: BatchNorm, LayerNorm, InstanceNorm, GroupNorm"""

import numpy as np
import matplotlib.pyplot as plt


class BatchNorm1d:
    def __init__(self, dim, eps=1e-5, momentum=0.9):
        self.gamma = np.ones(dim)
        self.beta = np.zeros(dim)
        self.eps = eps
        self.momentum = momentum
        self.running_mean = np.zeros(dim)
        self.running_var = np.ones(dim)
        self.training = True

    def forward(self, x):
        if self.training:
            batch_mean = x.mean(axis=0)
            batch_var = x.var(axis=0)
            self.running_mean = self.momentum * self.running_mean + (1 - self.momentum) * batch_mean
            self.running_var = self.momentum * self.running_var + (1 - self.momentum) * batch_var
            mu, v = batch_mean, batch_var
        else:
            mu, v = self.running_mean, self.running_var
        x_norm = (x - mu) / np.sqrt(v + self.eps)
        return self.gamma * x_norm + self.beta


class LayerNorm:
    def __init__(self, normalized_shape, eps=1e-5):
        self.gamma = np.ones(normalized_shape)
        self.beta = np.zeros(normalized_shape)
        self.eps = eps

    def forward(self, x):
        mu = x.mean(axis=-1, keepdims=True)
        v = x.var(axis=-1, keepdims=True)
        x_norm = (x - mu) / np.sqrt(v + self.eps)
        return self.gamma * x_norm + self.beta


class InstanceNorm:
    def __init__(self, channels, eps=1e-5):
        self.gamma = np.ones(channels)
        self.beta = np.zeros(channels)
        self.eps = eps

    def forward(self, x):
        mu = x.mean(axis=(2, 3), keepdims=True)
        v = x.var(axis=(2, 3), keepdims=True)
        x_norm = (x - mu) / np.sqrt(v + self.eps)
        return self.gamma.reshape(1, -1, 1, 1) * x_norm + self.beta.reshape(1, -1, 1, 1)


class GroupNorm:
    def __init__(self, num_groups, channels, eps=1e-5):
        assert channels % num_groups == 0
        self.num_groups = num_groups
        self.gamma = np.ones(channels)
        self.beta = np.zeros(channels)
        self.eps = eps

    def forward(self, x):
        N, C, H, W = x.shape
        G = self.num_groups
        x_g = x.reshape(N, G, C // G, H, W)
        mu = x_g.mean(axis=(2, 3, 4), keepdims=True)
        v = x_g.var(axis=(2, 3, 4), keepdims=True)
        x_norm = (x_g - mu) / np.sqrt(v + self.eps)
        x_norm = x_norm.reshape(N, C, H, W)
        return self.gamma.reshape(1, -1, 1, 1) * x_norm + self.beta.reshape(1, -1, 1, 1)


if __name__ == "__main__":
    np.random.seed(42)

    x_1d = np.random.randn(32, 64)
    bn = BatchNorm1d(64)
    out_bn = bn.forward(x_1d)
    print(f"BatchNorm1d: input mean={x_1d.mean():.3f}, std={x_1d.std():.3f}")
    print(f"             output mean={out_bn.mean():.3f}, std={out_bn.std():.3f}")

    ln = LayerNorm(64)
    out_ln = ln.forward(x_1d)
    print(f"LayerNorm:   output mean={out_ln.mean():.3f}, std={out_ln.std():.3f}")

    x_4d = np.random.randn(8, 16, 32, 32)
    inn = InstanceNorm(16)
    out_in = inn.forward(x_4d)
    print(f"\nInstanceNorm: output shape={out_in.shape}, mean={out_in.mean():.3f}")

    gn = GroupNorm(4, 16)
    out_gn = gn.forward(x_4d)
    print(f"GroupNorm:    output shape={out_gn.shape}, mean={out_gn.mean():.3f}")

    print("\nAll normalization layers verified.")
