"""
08.17 Neural Rendering — NeRF-like volume rendering with numpy
Usage: python 17-neural-rendering.py
"""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

def positional_encoding(x, L=6):
    enc = [x]
    for i in range(L):
        enc.extend([np.sin(2**i * np.pi * x), np.cos(2**i * np.pi * x)])
    return np.concatenate(enc)

# dummy MLP: maps (x,y,z,theta,phi) -> (r,g,b,sigma) learned via random weights
np.random.seed(0)
in_dim = 3 + 2 + 2*6*3  # xyz + viewdir + enc
W1 = np.random.randn(in_dim, 128) * 0.1; b1 = np.zeros(128)
W2 = np.random.randn(128, 128) * 0.1; b2 = np.zeros(128)
W_rgb = np.random.randn(128, 3) * 0.1; b_rgb = np.zeros(3)
W_sigma = np.random.randn(128, 1) * 0.1; b_sigma = np.zeros(1)

def relu(x): return np.maximum(0, x)
def sigmoid(x): return 1/(1+np.exp(-x))

def mlp(x, d):
    h = relu(x @ W1 + b1)
    h = relu(h @ W2 + b2)
    rgb = sigmoid(h @ W_rgb + b_rgb)
    sigma = relu(h @ W_sigma + b_sigma)
    return rgb, sigma

# ray marching
H, W = 32, 32
origin = np.array([0, 0, -2])
focal = 1.0

image = np.zeros((H, W, 3))
for i in range(H):
    for j in range(W):
        dir = np.array([(j-W/2)/focal, (i-H/2)/focal, 1])
        dir = dir / np.linalg.norm(dir)
        # sample along ray
        t_vals = np.linspace(0, 4, 32)
        rgb_acc = np.zeros(3)
        alpha_acc = 1.0
        for t in t_vals:
            pt = origin + t * dir
            enc_pt = np.concatenate([pt, dir])
            for L in range(1, 7):
                enc_pt = np.concatenate([enc_pt,
                    np.sin(2**L * np.pi * pt), np.cos(2**L * np.pi * pt)])
            rgb, sigma = mlp(enc_pt[:in_dim], dir)
            alpha = 1 - np.exp(-sigma[0] * 0.1)
            rgb_acc += alpha_acc * alpha * rgb[0]
            alpha_acc *= 1 - alpha
        image[i, j] = np.clip(rgb_acc, 0, 1)

plt.imshow(image); plt.title('NeRF-like Volume Render')
plt.axis('off')
plt.savefig('../../assets/phase08/17_neural_rendering.png', dpi=100)
print("Saved 17_neural_rendering.png")
