"""
08.07 Vision Transformers — patch embedding + attention in numpy
Usage: python 07-vision-transformers.py
"""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

def softmax(x, axis=-1):
    e = np.exp(x - x.max(axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)

def layer_norm(x, eps=1e-5):
    mean = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return (x - mean) / np.sqrt(var + eps)

def mha(Q, K, V):
    d = Q.shape[-1]
    scores = Q @ K.transpose(0,2,1) / np.sqrt(d)
    attn = softmax(scores, axis=-1)
    return attn @ V, attn

# create dummy image and patch it
img = np.random.randn(1, 3, 32, 32)
patch_size = 8
n_patches = (32//8)**2  # 16
patch_dim = 3 * 8 * 8  # 192
patches = img.reshape(1, 3, 4, 8, 4, 8)
patches = patches.transpose(0,2,4,1,3,5).reshape(1, 16, 192)

# linear projection
E = np.random.randn(192, 64) * 0.02
pos_embed = np.random.randn(1, 17, 64) * 0.02  # 16 patches + cls
cls_token = np.random.randn(1, 1, 64) * 0.02

x = patches @ E  # (1,16,64)
x = np.concatenate([cls_token, x], axis=1)  # (1,17,64)
x = x + pos_embed
x = layer_norm(x)

# single attention head
W_q = np.random.randn(64, 64) * 0.02
W_k = np.random.randn(64, 64) * 0.02
W_v = np.random.randn(64, 64) * 0.02
Q = x @ W_q; K = x @ W_k; V = x @ W_v
out, attn = mha(Q, K, V)
x = x + out
x = layer_norm(x)

print(f"Patch sequence: {x.shape}")
print(f"Attention matrix: {attn.shape}")
print(f"CLS token output norm: {np.linalg.norm(x[0,0]):.4f}")

fig, axes = plt.subplots(1, 2, figsize=(8, 4))
axes[0].imshow(attn[0], cmap='viridis'); axes[0].set_title('Attention Weights')
axes[1].bar(range(x.shape[1]), np.linalg.norm(x[0], axis=1)); axes[1].set_title('Token Norms')
plt.tight_layout(); plt.savefig('../../assets/phase08/07_vision_transformers.png', dpi=100)
print("Saved 07_vision_transformers.png")
