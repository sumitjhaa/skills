"""
08.04 CNN Backbones — simple ConvNet from scratch with numpy
Usage: python 04-cnn-backbones.py
"""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

# conv2d forward
def conv2d(x, w, b, stride=1, pad=0):
    N, C, H, W = x.shape
    K, C, Hk, Wk = w.shape
    H_out = (H + 2*pad - Hk) // stride + 1
    W_out = (W + 2*pad - Wk) // stride + 1
    x_pad = np.pad(x, ((0,0),(0,0),(pad,pad),(pad,pad)), mode='constant')
    out = np.zeros((N, K, H_out, W_out))
    for n in range(N):
        for k in range(K):
            for i in range(H_out):
                for j in range(W_out):
                    hs, ws = i*stride, j*stride
                    out[n,k,i,j] = np.sum(x_pad[n,:,hs:hs+Hk,ws:ws+Wk] * w[k]) + b[k]
    return out

# max pool
def maxpool2d(x, pool=2, stride=2):
    N, C, H, W = x.shape
    H_out = (H - pool) // stride + 1
    W_out = (W - pool) // stride + 1
    out = np.zeros((N, C, H_out, W_out))
    for n in range(N):
        for c in range(C):
            for i in range(H_out):
                for j in range(W_out):
                    hs, ws = i*stride, j*stride
                    out[n,c,i,j] = np.max(x[n,c,hs:hs+pool,ws:ws+pool])
    return out

# relu
def relu(x):
    return np.maximum(0, x)

# create a tiny image batch
x = np.random.randn(2, 1, 16, 16)  # N,C,H,W

# simulate a simple backbone: conv-pool-conv-pool-GAP
w1 = np.random.randn(4, 1, 3, 3) * 0.1; b1 = np.zeros(4)
x1 = relu(conv2d(x, w1, b1, pad=1))     # (2,4,16,16)
x2 = maxpool2d(x1, pool=2, stride=2)     # (2,4,8,8)
w2 = np.random.randn(8, 4, 3, 3) * 0.1; b2 = np.zeros(8)
x3 = relu(conv2d(x2, w2, b2, pad=1))     # (2,8,8,8)
x4 = maxpool2d(x3, pool=2, stride=2)     # (2,8,4,4)
# global average pooling
gap = x4.mean(axis=(2,3))                # (2,8)
print(f"Input shape:  {x.shape}")
print(f"After conv1:  {x1.shape}")
print(f"After pool1:  {x2.shape}")
print(f"After conv2:  {x3.shape}")
print(f"After pool2:  {x4.shape}")
print(f"After GAP:    {gap.shape}")

# visualise first feature maps
fig, axes = plt.subplots(2, 4, figsize=(10, 5))
for i in range(4):
    axes[0, i].imshow(x1[0, i], cmap='gray')
    axes[0, i].set_title(f'Conv1 FM {i}')
    axes[1, i].imshow(x3[0, i], cmap='gray')
    axes[1, i].set_title(f'Conv2 FM {i}')
for ax in axes.flat: ax.axis('off')
plt.tight_layout(); plt.savefig('../../assets/phase08/04_cnn_backbones.png', dpi=100)
print("Saved 04_cnn_backbones.png")
