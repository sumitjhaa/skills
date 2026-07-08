"""06.25 - Skip Connections: Residual, dense, highway connections"""

import numpy as np


def relu(x):
    return np.maximum(0, x)


class ResidualBlock:
    def __init__(self, dim):
        self.W1 = np.random.randn(dim, dim) * 0.01
        self.b1 = np.zeros(dim)
        self.W2 = np.random.randn(dim, dim) * 0.01
        self.b2 = np.zeros(dim)

    def forward(self, x):
        out = relu(x @ self.W1 + self.b1)
        out = out @ self.W2 + self.b2
        return relu(out + x)


class DenseBlock:
    def __init__(self, growth_rate):
        self.growth_rate = growth_rate
        self.W = np.random.randn(64, growth_rate) * 0.01
        self.b = np.zeros(growth_rate)

    def forward(self, x):
        out = relu(x @ self.W + self.b)
        return np.concatenate([x, out], axis=-1)


class HighwayBlock:
    def __init__(self, dim):
        self.W = np.random.randn(dim, dim) * 0.01
        self.b = np.zeros(dim)
        self.W_T = np.random.randn(dim, dim) * 0.01
        self.b_T = np.zeros(dim)

    def forward(self, x):
        H = relu(x @ self.W + self.b)
        T = 1 / (1 + np.exp(-(x @ self.W_T + self.b_T)))
        C = 1 - T
        return H * T + x * C


class UNetBlock:
    def __init__(self, in_ch, out_ch):
        self.W = np.random.randn(in_ch, out_ch) * 0.1
        self.b = np.zeros(out_ch)

    def forward(self, x):
        return relu(x @ self.W + self.b)


class UNet:
    def __init__(self):
        self.enc1 = UNetBlock(64, 128)
        self.enc2 = UNetBlock(128, 256)
        self.bottleneck = UNetBlock(256, 512)
        self.dec2 = UNetBlock(512 + 256, 128)
        self.dec1 = UNetBlock(128 + 128, 64)

    def forward(self, x):
        e1 = self.enc1.forward(x)
        e2 = self.enc2.forward(e1)
        b = self.bottleneck.forward(e2)
        d2 = self.dec2.forward(np.concatenate([b, e2], axis=-1))
        d1 = self.dec1.forward(np.concatenate([d2, e1], axis=-1))
        return d1


if __name__ == "__main__":
    np.random.seed(42)

    res_block = ResidualBlock(32)
    x = np.random.randn(4, 32)
    out_res = res_block.forward(x)
    print(f"Residual block: input {x.shape}, output {out_res.shape}")
    print(f"  Output equals input shape: {out_res.shape == x.shape}")

    dense = DenseBlock(growth_rate=16)
    x = np.random.randn(4, 64)
    out_dense = dense.forward(x)
    print(f"\nDense block:    input (4,64), output {out_dense.shape}  (expected: (4,80))")

    highway = HighwayBlock(32)
    x = np.random.randn(4, 32)
    out_hw = highway.forward(x)
    print(f"\nHighway block:  input {x.shape}, output {out_hw.shape}")

    unet = UNet()
    x_unet = np.random.randn(4, 64)
    out_unet = unet.forward(x_unet)
    print(f"\nU-Net:          input {x_unet.shape}, output {out_unet.shape}  (expected: (4,64))")

    x_orig_res = np.random.randn(4, 32)
    out_res2 = res_block.forward(x_orig_res)
    residual_effect = np.linalg.norm(out_res2 - x_orig_res) > np.linalg.norm(x_orig_res) * 0.5
    print(f"\nResidual output differs from input: {residual_effect}")
    print("All skip connection architectures implemented.")
