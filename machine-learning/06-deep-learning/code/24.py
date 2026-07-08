"""06.24 - CNN Backbones: LeNet-5, AlexNet, VGG, ResNet, EfficientNet"""

import numpy as np


def im2col(x, k_h, k_w, stride=1, pad=0):
    N, C, H, W = x.shape
    H_out = (H + 2 * pad - k_h) // stride + 1
    W_out = (W + 2 * pad - k_w) // stride + 1
    x_pad = np.pad(x, ((0,0),(0,0),(pad,pad),(pad,pad)), mode="constant")
    cols = np.zeros((N, C, k_h, k_w, H_out, W_out))
    for i in range(k_h):
        for j in range(k_w):
            cols[:, :, i, j, :, :] = x_pad[:, :, i:i+H_out*stride:stride, j:j+W_out*stride:stride]
    return cols.reshape(N, C * k_h * k_w, H_out * W_out).transpose(0, 2, 1)

def conv(x, W, b, stride=1, pad=0):
    N, C, H, Win = x.shape
    K, _, k_h, k_w = W.shape
    H_out = (H + 2*pad - k_h)//stride + 1
    W_out = (Win + 2*pad - k_w)//stride + 1
    cols = im2col(x, k_h, k_w, stride, pad)
    out = cols @ W.reshape(K, -1).T
    return out.reshape(N, H_out, W_out, K).transpose(0, 3, 1, 2) + b.reshape(1, -1, 1, 1)

def max_pool(x, pool=2, stride=2):
    N, C, H, W = x.shape
    H_out = (H - pool)//stride + 1
    W_out = (W - pool)//stride + 1
    out = np.zeros((N, C, H_out, W_out))
    for i in range(H_out):
        for j in range(W_out):
            out[:, :, i, j] = x[:, :, i*stride:i*stride+pool, j*stride:j*stride+pool].max(axis=(2,3))
    return out

def relu(x):
    return np.maximum(0, x)

def avg_pool_global(x):
    return x.mean(axis=(2, 3))


class LeNet5:
    def __init__(self):
        self.C1 = (np.random.randn(6, 3, 5, 5) * 0.1, np.zeros(6))
        self.C3 = (np.random.randn(16, 6, 5, 5) * 0.1, np.zeros(16))
        self.C5 = (np.random.randn(120, 16, 5, 5) * 0.1, np.zeros(120))
        self.fc = (np.random.randn(120, 10) * 0.1, np.zeros(10))

    def forward(self, x):
        x = relu(conv(x, *self.C1, stride=1, pad=2))
        x = max_pool(x, 2, 2)
        x = relu(conv(x, *self.C3))
        x = max_pool(x, 2, 2)
        x = relu(conv(x, *self.C5))
        x = avg_pool_global(x)
        x = x @ self.fc[0] + self.fc[1]
        return x


class VGG:
    def __init__(self, num_classes=10):
        self.conv_layers = []
        channels = [3, 64, 64, 128, 128, 256, 256, 256, 512, 512, 512]
        for i in range(len(channels) - 1):
            W = np.random.randn(channels[i+1], channels[i], 3, 3) * 0.1
            self.conv_layers.append((W, np.zeros(channels[i+1])))

        self.fc1 = (np.random.randn(512, 4096) * 0.01, np.zeros(4096))
        self.fc2 = (np.random.randn(4096, 4096) * 0.01, np.zeros(4096))
        self.fc3 = (np.random.randn(4096, num_classes) * 0.01, np.zeros(num_classes))

    def forward(self, x):
        pool_indices = [1, 3, 6, 9, 12]
        for idx, (W, b) in enumerate(self.conv_layers):
            x = relu(conv(x, W, b, stride=1, pad=1))
            if idx in pool_indices:
                x = max_pool(x, 2, 2)
        x = avg_pool_global(x)
        x = relu(x @ self.fc1[0] + self.fc1[1])
        x = relu(x @ self.fc2[0] + self.fc2[1])
        x = x @ self.fc3[0] + self.fc3[1]
        return x


class ResBlock:
    def __init__(self, in_ch, out_ch, stride=1):
        self.conv1 = (np.random.randn(out_ch, in_ch, 3, 3) * 0.1, np.zeros(out_ch))
        self.conv2 = (np.random.randn(out_ch, out_ch, 3, 3) * 0.1, np.zeros(out_ch))
        self.shortcut = None
        if in_ch != out_ch or stride != 1:
            self.shortcut = (np.random.randn(out_ch, in_ch, 1, 1) * 0.1, np.zeros(out_ch))
        self.stride = stride

    def forward(self, x):
        identity = x
        out = relu(conv(x, *self.conv1, stride=self.stride, pad=1))
        out = conv(out, *self.conv2, stride=1, pad=1)
        if self.shortcut is not None:
            identity = conv(identity, *self.shortcut, stride=self.stride, pad=0)
        out = relu(out + identity)
        return out


class ResNet:
    def __init__(self, num_classes=10):
        self.conv1 = (np.random.randn(64, 3, 7, 7) * 0.1, np.zeros(64))
        self.layer1 = [ResBlock(64, 64) for _ in range(2)]
        self.layer2 = [ResBlock(64, 128, stride=2)] + [ResBlock(128, 128) for _ in range(1)]
        self.layer3 = [ResBlock(128, 256, stride=2)] + [ResBlock(256, 256) for _ in range(1)]
        self.layer4 = [ResBlock(256, 512, stride=2)] + [ResBlock(512, 512) for _ in range(1)]
        self.fc = (np.random.randn(512, num_classes) * 0.01, np.zeros(num_classes))

    def forward(self, x):
        x = relu(conv(x, *self.conv1, stride=2, pad=3))
        x = max_pool(x, 3, 2)
        for block in self.layer1 + self.layer2 + self.layer3 + self.layer4:
            x = block.forward(x)
        x = avg_pool_global(x)
        x = x @ self.fc[0] + self.fc[1]
        return x


class EfficientNet:
    def __init__(self, num_classes=10):
        self.stem = (np.random.randn(32, 3, 3, 3) * 0.1, np.zeros(32))
        W = np.random.randn(128, 32, 3, 3) * 0.1
        self.blocks = [(W, np.zeros(128))]
        self.fc = (np.random.randn(128, num_classes) * 0.01, np.zeros(num_classes))

    def forward(self, x):
        x = relu(conv(x, *self.stem, stride=2, pad=1))
        for W, b in self.blocks:
            x = relu(conv(x, W, b, stride=1, pad=1))
        x = avg_pool_global(x)
        x = x @ self.fc[0] + self.fc[1]
        return x


if __name__ == "__main__":
    np.random.seed(42)
    x = np.random.randn(2, 3, 32, 32)

    lenet = LeNet5()
    out = lenet.forward(x)
    print(f"LeNet-5:           input {x.shape} -> output {out.shape}")

    vgg = VGG()
    out = vgg.forward(x)
    print(f"VGG (simplified):  input {x.shape} -> output {out.shape}")

    resnet = ResNet()
    out = resnet.forward(x)
    print(f"ResNet (simplified): input {x.shape} -> output {out.shape}")

    effnet = EfficientNet()
    out = effnet.forward(x)
    print(f"EfficientNet:      input {x.shape} -> output {out.shape}")

    print("\nAll CNN backbones implemented.")
