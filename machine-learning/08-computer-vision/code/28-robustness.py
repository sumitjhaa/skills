"""
08.28 Robustness — FGSM adversarial attack in numpy
Usage: python 28-robustness.py
"""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

# simple binary classifier
np.random.seed(0)
W = np.random.randn(64, 64) * 0.1
b = np.zeros(64)
W_out = np.random.randn(64, 2) * 0.1
b_out = np.zeros(2)

def forward(x):
    h = np.maximum(0, x @ W + b)
    logits = h @ W_out + b_out
    return logits

def softmax(x):
    e = np.exp(x - x.max())
    return e / e.sum()

def loss(x, y):
    logits = forward(x)
    p = softmax(logits)
    return -np.log(p[y] + 1e-10), logits

# a single image
x = np.random.randn(64, 64)
y_true = 0

# FGSM attack
eps = 0.5
_, logits = loss(x, y_true)
# gradient of cross-entropy w.r.t. input
p = softmax(logits)
dy = p.copy()
dy[y_true] -= 1  # dL/dlogits
dh = dy @ W_out.T  # dL/dh
dh = dh * (x @ W + b > 0)  # relu gradient
dx = dh @ W.T  # dL/dx
x_adv = x + eps * np.sign(dx)
x_adv = np.clip(x_adv, -3, 3)

_, logits_clean = loss(x, y_true)
_, logits_adv = loss(x_adv, y_true)
p_clean = softmax(logits_clean)
p_adv = softmax(logits_adv)
print(f"Clean confidence: {p_clean[y_true]:.3f}")
print(f"Adversarial confidence: {p_adv[y_true]:.3f}")

fig, axes = plt.subplots(1, 3, figsize=(10, 3))
axes[0].imshow(x, cmap='gray'); axes[0].set_title('Clean')
axes[1].imshow(x_adv, cmap='gray'); axes[1].set_title(f'Adversarial (eps={eps})')
axes[2].imshow(x_adv - x, cmap='seismic', vmin=-eps, vmax=eps); axes[2].set_title('Perturbation')
for ax in axes: ax.axis('off')
plt.tight_layout(); plt.savefig('../../assets/phase08/28_robustness.png', dpi=100)
print("Saved 28_robustness.png")
