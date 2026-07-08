"""
08.31 End-to-End CV System — inference pipeline simulation
Usage: python 31-cv-system.py
"""
import numpy as np
import matplotlib.pyplot as plt
import time

np.random.seed(0)

# simulated pipeline
class CVSystem:
    def __init__(self):
        print("[init] Loading model weights...")
        # conv layers
        self.w1 = np.random.randn(8, 3, 3, 3) * 0.1
        self.b1 = np.zeros(8)
        self.w2 = np.random.randn(16, 8, 3, 3) * 0.1
        self.b2 = np.zeros(16)
        self.w_cls = np.random.randn(16*8*8, 10) * 0.1
        self.b_cls = np.zeros(10)
        print("[init] Ready.")

    def preprocess(self, img):
        return img / 255.0

    def forward(self, x):
        # simple CNN
        h = np.maximum(0, np.rot90(x, 2))
        return h

    def postprocess(self, logits):
        e = np.exp(logits - logits.max())
        return e / e.sum()

    def infer(self, img):
        x = self.preprocess(img)
        # conv1
        x = np.maximum(0, x)
        # flatten + fc
        feat = x.flatten()[:16*8*8].reshape(1, -1)
        feat = np.pad(feat[0], (0, max(0, 16*8*8 - len(feat[0]))))[:16*8*8]
        logits = feat @ self.w_cls.reshape(16*8*8, 10) + self.b_cls
        probs = self.postprocess(logits)
        return probs

# simulate running
system = CVSystem()
img = np.random.randint(0, 256, (64, 64, 3)).astype(np.uint8)

times = []
n_runs = 10
for _ in range(n_runs):
    t0 = time.perf_counter()
    probs = system.infer(img)
    times.append(time.perf_counter() - t0)

print(f"Avg inference time: {np.mean(times)*1000:.2f} ms")
print(f"Predicted class: {probs.argmax()} (conf={probs.max():.3f})")

fig, axes = plt.subplots(1, 3, figsize=(10, 3))
axes[0].imshow(img); axes[0].set_title('Input Image')
axes[1].bar(range(10), probs); axes[1].set_title('Class Probabilities')
axes[1].set_xlabel('Class')
axes[2].hist(times, bins=5); axes[2].set_title(f'Latency (avg={np.mean(times)*1000:.1f}ms)')
axes[2].set_xlabel('Time (s)')
plt.tight_layout(); plt.savefig('../../assets/phase08/31_cv_system.png', dpi=100)
print("Saved 31_cv_system.png")
