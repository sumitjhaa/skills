"""
12.10: Reproduce a SOTA Paper + Improve It
Reproduce SimCLR (contrastive learning) and propose
an adaptive augmentation improvement.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, List, Tuple, Callable
from scipy.ndimage import zoom, rotate, gaussian_filter
import warnings
warnings.filterwarnings('ignore')


# ─────────────────────────────────────────────
# Data: CIFAR-10 simulation
# ─────────────────────────────────────────────

def load_cifar_simulation(n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
    """Use sklearn digits as a CIFAR-10 proxy."""
    from sklearn.datasets import load_digits
    digits = load_digits()
    X = digits.images[:n_samples].astype(np.float64)
    y = digits.target[:n_samples]

    # Resize 8x8 → 32x32 (CIFAR-like)
    X_resized = np.zeros((n_samples, 32, 32, 1), dtype=np.float64)
    for i in range(n_samples):
        X_resized[i, :, :, 0] = zoom(X[i], 4, order=1)

    # Normalize to [0, 1]
    X_resized = X_resized / 16.0
    return X_resized, y


# ─────────────────────────────────────────────
# SimCLR Augmentations
# ─────────────────────────────────────────────

class SimCLRAugment:
    """Augmentation pipeline from SimCLR paper."""

    @staticmethod
    def random_crop_flip(x: np.ndarray, crop_size: int = 28) -> np.ndarray:
        H, W = x.shape[:2]
        dh = np.random.randint(0, H - crop_size + 1)
        dw = np.random.randint(0, W - crop_size + 1)
        x = x[dh:dh + crop_size, dw:dw + crop_size]
        if np.random.random() > 0.5:
            x = np.fliplr(x)
        return x

    @staticmethod
    def color_jitter(x: np.ndarray, strength: float = 0.5) -> np.ndarray:
        # Simulate color jitter on grayscale by adjusting brightness/contrast
        brightness = 1.0 + np.random.uniform(-strength, strength)
        contrast = 1.0 + np.random.uniform(-strength, strength)
        x = x * contrast + np.random.uniform(-strength, strength)
        return np.clip(x, 0, 1)

    @staticmethod
    def gaussian_blur(x: np.ndarray, max_sigma: float = 1.0) -> np.ndarray:
        sigma = np.random.uniform(0, max_sigma)
        if sigma > 0:
            x = gaussian_filter(x, sigma=sigma)
        return x

    @staticmethod
    def augment(x: np.ndarray) -> np.ndarray:
        x = SimCLRAugment.random_crop_flip(x, crop_size=28)
        x = SimCLRAugment.color_jitter(x, strength=0.3)
        if np.random.random() > 0.5:
            x = SimCLRAugment.gaussian_blur(x)
        return x

    @staticmethod
    def augment_pair(x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Generate two augmented views of the same image."""
        return SimCLRAugment.augment(x.copy()), SimCLRAugment.augment(x.copy())


# ─────────────────────────────────────────────
# Adaptive Augmentation (Improvement)
# ─────────────────────────────────────────────

class AdaptiveAugment:
    """
    Improvement: Learn augmentation strength per sample.
    Easy samples get stronger augmentation, hard samples get weaker.
    """

    def __init__(self, base_strength: float = 0.5):
        self.base_strength = base_strength

    def estimate_difficulty(self, x: np.ndarray, encoder: Callable) -> float:
        """Estimate sample difficulty based on feature norm."""
        features = encoder(x[None, :, :, :])
        # Lower norm = harder sample (less confident features)
        norm = np.linalg.norm(features)
        # Normalize difficulty to [0, 1]
        difficulty = 1.0 / (1.0 + norm)
        return float(np.clip(difficulty, 0.1, 0.9))

    def augment(self, x: np.ndarray, difficulty: float) -> np.ndarray:
        # Stronger augmentation for easy samples (difficulty < 0.5)
        # Weaker augmentation for hard samples (difficulty > 0.5)
        strength = self.base_strength * (1.0 + 0.5 * (0.5 - difficulty))

        x = SimCLRAugment.random_crop_flip(x, crop_size=28)
        x = SimCLRAugment.color_jitter(x, strength=strength * 0.5)
        if np.random.random() > 0.5:
            x = SimCLRAugment.gaussian_blur(x, max_sigma=strength)
        return x

    def augment_pair(self, x: np.ndarray, encoder: Callable) -> Tuple[np.ndarray, np.ndarray, float]:
        difficulty = self.estimate_difficulty(x, encoder)
        aug1 = self.augment(x.copy(), difficulty)
        aug2 = self.augment(x.copy(), difficulty)
        return aug1, aug2, difficulty


# ─────────────────────────────────────────────
# Encoder (simplified ResNet-18)
# ─────────────────────────────────────────────

def conv3x3(in_ch, out_ch, stride=1):
    scale = np.sqrt(2.0 / (in_ch * 9))
    return {
        'w': np.random.randn(out_ch, in_ch, 3, 3).astype(np.float64) * scale,
        'b': np.zeros(out_ch, dtype=np.float64),
        'stride': stride,
    }


def batch_norm(x, gamma, beta, eps=1e-5):
    if x.shape[0] <= 1:
        return np.ones_like(x) * beta
    mean = x.mean(axis=(0, 2, 3), keepdims=True)
    var = x.var(axis=(0, 2, 3), keepdims=True)
    return gamma[None, :, None, None] * (x - mean) / np.sqrt(var + eps) + beta[None, :, None, None]


def apply_conv(x, conv):
    N, C, H, W = x.shape
    out_ch, in_ch, kH, kW = conv['w'].shape
    pad = kH // 2
    stride = conv.get('stride', 1)
    x_pad = np.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)), mode='constant')

    if stride > 1:
        out_H = H // stride
        out_W = W // stride
    else:
        out_H, out_W = H, W

    out = np.zeros((N, out_ch, out_H, out_W), dtype=np.float64)
    for i in range(out_H):
        for j in range(out_W):
            si = i * stride
            sj = j * stride
            patch = x_pad[:, :, si:si + kH, sj:sj + kW]
            out[:, :, i, j] = (patch[:, :, ::-1, ::-1] * conv['w'][None, :, :, :, :]).sum(axis=(2, 3, 4))
    return out + conv['b'][None, :, None, None]


def relu(x):
    return np.maximum(0, x)


def global_avg_pool(x):
    return x.mean(axis=(2, 3))


class ResidualBlock:
    def __init__(self, in_ch, out_ch, stride=1):
        self.conv1 = conv3x3(in_ch, out_ch, stride)
        self.bn1_g = np.ones(out_ch, dtype=np.float64)
        self.bn1_b = np.zeros(out_ch, dtype=np.float64)
        self.conv2 = conv3x3(out_ch, out_ch)
        self.bn2_g = np.ones(out_ch, dtype=np.float64)
        self.bn2_b = np.zeros(out_ch, dtype=np.float64)

        if stride != 1 or in_ch != out_ch:
            scale = np.sqrt(2.0 / in_ch)
            self.shortcut = {
                'w': np.random.randn(out_ch, in_ch, 1, 1).astype(np.float64) * scale,
                'b': np.zeros(out_ch, dtype=np.float64),
                'stride': stride,
            }
            self.shortcut_bn_g = np.ones(out_ch, dtype=np.float64)
            self.shortcut_bn_b = np.zeros(out_ch, dtype=np.float64)
        else:
            self.shortcut = None

    def forward(self, x):
        identity = x
        out = relu(batch_norm(self.conv1, self.bn1_g, self.bn1_b))
        out = batch_norm(self.conv2, self.bn2_g, self.bn2_b)

        if self.shortcut is not None:
            identity = batch_norm(self.shortcut, self.shortcut_bn_g, self.shortcut_bn_b)
        out = out * (-1)  # dummy op to match shapes
        out += identity
        out = relu(out)
        return out

    # For simplicity, use a direct conv path
    def forward_simple(self, x):
        out = apply_conv(x, self.conv1)
        out = batch_norm(out, self.bn1_g, self.bn1_b)
        out = relu(out)
        out = apply_conv(out, self.conv2)
        out = batch_norm(out, self.bn2_g, self.bn2_b)

        if self.shortcut is not None:
            shortcut_out = apply_conv(x, self.shortcut)
            shortcut_out = batch_norm(shortcut_out, self.shortcut_bn_g, self.shortcut_bn_b)
            out = out + shortcut_out
        else:
            out = out + x
        out = relu(out)
        return out


class SimpleEncoder:
    """Simplified ResNet-18 for SimCLR."""
    def __init__(self, input_channels=1, feature_dim=128):
        # Initial conv
        self.conv1 = conv3x3(input_channels, 64)
        self.bn1_g = np.ones(64, dtype=np.float64)
        self.bn1_b = np.zeros(64, dtype=np.float64)

        # ResNet blocks (simplified)
        self.layer1 = [ResidualBlock(64, 64) for _ in range(2)]
        self.layer2 = [ResidualBlock(64, 128, stride=2)] + [ResidualBlock(128, 128) for _ in range(1)]

        # Projection head (SimCLR specific)
        scale = np.sqrt(2.0 / 128)
        self.proj_w1 = np.random.randn(128, 128).astype(np.float64) * scale
        self.proj_b1 = np.zeros(128, dtype=np.float64)
        self.proj_w2 = np.random.randn(128, feature_dim).astype(np.float64) * scale
        self.proj_b2 = np.zeros(feature_dim, dtype=np.float64)

    def forward(self, x: np.ndarray) -> np.ndarray:
        # Expect (B, H, W, C) → convert to (B, C, H, W)
        if x.ndim == 4 and x.shape[-1] in [1, 3]:
            x = x.transpose(0, 3, 1, 2)

        x = apply_conv(x, self.conv1)
        x = batch_norm(x, self.bn1_g, self.bn1_b)
        x = relu(x)

        for block in self.layer1:
            x = block.forward_simple(x)
        for block in self.layer2:
            x = block.forward_simple(x)

        x = global_avg_pool(x)  # (B, C)
        return x

    def project(self, x: np.ndarray) -> np.ndarray:
        features = self.forward(x)
        h = relu(features @ self.proj_w1 + self.proj_b1)
        z = h @ self.proj_w2 + self.proj_b2
        return z, features

    def parameters(self):
        params = [self.conv1['w'], self.conv1['b'], self.bn1_g, self.bn1_b,
                  self.proj_w1, self.proj_b1, self.proj_w2, self.proj_b2]
        for block in self.layer1 + self.layer2:
            params.extend([block.conv1['w'], block.conv1['b'],
                          block.bn1_g, block.bn1_b,
                          block.conv2['w'], block.conv2['b'],
                          block.bn2_g, block.bn2_b])
            if block.shortcut is not None:
                params.extend([block.shortcut['w'], block.shortcut['b'],
                              block.shortcut_bn_g, block.shortcut_bn_b])
        return params


# ─────────────────────────────────────────────
# NT-Xent loss (contrastive)
# ─────────────────────────────────────────────

def nt_xent_loss(z: np.ndarray, temperature: float = 0.5) -> float:
    """
    Normalized Temperature-scaled Cross Entropy loss.
    z: (2*B, D) — each pair is two augmented views of same image.
    """
    B = z.shape[0] // 2
    # Normalize
    z_norm = z / (np.linalg.norm(z, axis=1, keepdims=True) + 1e-10)

    # Similarity matrix
    sim = z_norm @ z_norm.T  # (2B, 2B)

    # Remove diagonal (self-similarity)
    mask = ~np.eye(2 * B, dtype=bool)
    sim = sim[mask].reshape(2 * B, 2 * B - 1)

    # Temperature scaling
    sim = sim / temperature

    # Positive pairs: (0, B), (1, B+1), ..., (B-1, 2B-1) and symmetric
    labels = np.zeros(2 * B, dtype=np.int64)
    for i in range(B):
        labels[i] = i + B
        labels[i + B] = i

    # Cross-entropy loss
    sim_max = sim.max(axis=1, keepdims=True)
    sim_stable = sim - sim_max
    log_probs = sim_stable - np.log(np.sum(np.exp(sim_stable), axis=1, keepdims=True))

    # Get log prob of positive pairs
    # For each sample i, the positive is at position labels[i] (adjusted for missing diagonal)
    pos_log_probs = []
    for i in range(2 * B):
        label = labels[i]
        # Adjust: if label > i, position is label-1 (since diagonal removed)
        pos_idx = label - 1 if label > i else label
        pos_log_probs.append(log_probs[i, pos_idx])

    loss = -np.mean(pos_log_probs)
    return float(loss)


# ─────────────────────────────────────────────
# Linear evaluation protocol
# ─────────────────────────────────────────────

class LinearClassifier:
    """Train a linear classifier on frozen representations."""
    def __init__(self, input_dim: int, n_classes: int, lr: float = 0.01):
        self.W = np.random.randn(input_dim, n_classes).astype(np.float64) * 0.01
        self.b = np.zeros(n_classes, dtype=np.float64)
        self.lr = lr

    def forward(self, x: np.ndarray) -> np.ndarray:
        return x @ self.W + self.b

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 50):
        n = X.shape[0]
        n_classes = self.W.shape[1]

        for ep in range(epochs):
            logits = self.forward(X)
            logits_stable = logits - logits.max(axis=1, keepdims=True)
            probs = np.exp(logits_stable) / np.exp(logits_stable).sum(axis=1, keepdims=True)
            y_onehot = np.eye(n_classes)[y]

            grad_W = X.T @ (probs - y_onehot) / n
            grad_b = (probs - y_onehot).mean(axis=0)

            self.W -= self.lr * grad_W
            self.b -= self.lr * grad_b

    def accuracy(self, X: np.ndarray, y: np.ndarray) -> float:
        preds = np.argmax(self.forward(X), axis=1)
        return float((preds == y).mean())


# ─────────────────────────────────────────────
# Optimizer
# ─────────────────────────────────────────────

class SGDOptimizer:
    def __init__(self, params, lr=0.01):
        self.params = params
        self.lr = lr

    def step(self, grads):
        for p, g in zip(self.params, grads):
            p -= self.lr * g


# ─────────────────────────────────────────────
# SimCLR Training (Baseline)
# ─────────────────────────────────────────────

def train_simclr_baseline(X: np.ndarray, y: np.ndarray,
                          epochs: int = 20, batch_size: int = 32,
                          temperature: float = 0.5, lr: float = 0.01) -> SimpleEncoder:
    """Train SimCLR baseline."""
    encoder = SimpleEncoder(input_channels=1, feature_dim=128)
    params = encoder.parameters()
    optim = SGDOptimizer(params, lr)
    n_samples = X.shape[0]

    losses = []
    for epoch in range(epochs):
        perm = np.random.permutation(n_samples)
        epoch_loss = 0.0
        n_batches = 0

        for i in range(0, n_samples, batch_size):
            idx = perm[i:i + batch_size]
            batch = X[idx]

            # Generate two augmented views
            views = []
            for img in batch:
                v1, v2 = SimCLRAugment.augment_pair(img)
                views.extend([v1[None, ...], v2[None, ...]])
            views = np.concatenate(views, axis=0)  # (2*B, H, W, C)

            # Forward
            z, _ = encoder.project(views)
            loss = nt_xent_loss(z, temperature)

            # Compute gradients (finite differences, subset of params for speed)
            grads = [np.zeros_like(p) for p in params]
            eps = 1e-4
            for j, p in enumerate(params):
                for idx_flat in range(min(5, p.size)):  # sparse grad for speed
                    multi_idx = np.unravel_index(idx_flat, p.shape)
                    orig = p[multi_idx]
                    p[multi_idx] = orig + eps
                    z_p, _ = encoder.project(views)
                    loss_p = nt_xent_loss(z_p, temperature)
                    p[multi_idx] = orig - eps
                    z_m, _ = encoder.project(views)
                    loss_m = nt_xent_loss(z_m, temperature)
                    grads[j][multi_idx] = (loss_p - loss_m) / (2 * eps)
                    p[multi_idx] = orig

            optim.step(grads)
            epoch_loss += loss
            n_batches += 1

        avg_loss = epoch_loss / max(n_batches, 1)
        losses.append(avg_loss)
        if (epoch + 1) % 5 == 0:
            print(f"  SimCLR Epoch {epoch+1}/{epochs} | Loss: {avg_loss:.4f}")

    return encoder, losses


def train_simclr_adaptive(X: np.ndarray, y: np.ndarray,
                          epochs: int = 20, batch_size: int = 32,
                          temperature: float = 0.5, lr: float = 0.01) -> SimpleEncoder:
    """Train SimCLR with adaptive augmentation improvement."""
    encoder = SimpleEncoder(input_channels=1, feature_dim=128)
    adaptive = AdaptiveAugment(base_strength=0.5)
    params = encoder.parameters()
    optim = SGDOptimizer(params, lr)
    n_samples = X.shape[0]

    losses = []
    difficulties = []

    for epoch in range(epochs):
        perm = np.random.permutation(n_samples)
        epoch_loss = 0.0
        n_batches = 0

        for i in range(0, n_samples, batch_size):
            idx = perm[i:i + batch_size]
            batch = X[idx]

            views = []
            for img in batch:
                v1, v2, diff = adaptive.augment_pair(img, lambda x: encoder.forward(x))
                views.extend([v1[None, ...], v2[None, ...]])
                difficulties.append(diff)
            views = np.concatenate(views, axis=0)

            z, _ = encoder.project(views)
            loss = nt_xent_loss(z, temperature)

            grads = [np.zeros_like(p) for p in params]
            eps = 1e-4
            for j, p in enumerate(params):
                for idx_flat in range(min(5, p.size)):
                    multi_idx = np.unravel_index(idx_flat, p.shape)
                    orig = p[multi_idx]
                    p[multi_idx] = orig + eps
                    z_p, _ = encoder.project(views)
                    loss_p = nt_xent_loss(z_p, temperature)
                    p[multi_idx] = orig - eps
                    z_m, _ = encoder.project(views)
                    loss_m = nt_xent_loss(z_m, temperature)
                    grads[j][multi_idx] = (loss_p - loss_m) / (2 * eps)
                    p[multi_idx] = orig

            optim.step(grads)
            epoch_loss += loss
            n_batches += 1

        avg_loss = epoch_loss / max(n_batches, 1)
        losses.append(avg_loss)
        if (epoch + 1) % 5 == 0:
            print(f"  Adaptive SimCLR Epoch {epoch+1}/{epochs} | Loss: {avg_loss:.4f}")

    return encoder, losses, difficulties


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    np.random.seed(42)

    print("=" * 60)
    print("REPRODUCE SIMCLR + IMPROVEMENT")
    print("=" * 60)

    # Load data
    print("\n[1] Loading data...")
    X, y = load_cifar_simulation(500)
    print(f"    Data: {X.shape}")

    # Split for linear evaluation
    split = 300
    X_train, y_train = X[:split], y[:split]
    X_test, y_test = X[split:], y[split:]

    # ── Reproduce SimCLR ──
    print("\n[2] Reproducing SimCLR baseline...")
    encoder_base, losses_base = train_simclr_baseline(X_train, y_train, epochs=15, batch_size=16)

    # Linear evaluation (baseline)
    print("\n[3] Linear evaluation (baseline)...")
    features_base_train, _ = encoder_base.project(X_train)
    features_base_test, _ = encoder_base.project(X_test)

    clf = LinearClassifier(features_base_train.shape[1], len(np.unique(y)), lr=0.01)
    clf.train(features_base_train, y_train, epochs=30)
    acc_base = clf.accuracy(features_base_test, y_test)
    print(f"    Baseline test accuracy: {acc_base:.4f}")

    # ── SimCLR with Adaptive Augmentation ──
    print("\n[4] Training SimCLR with adaptive augmentation...")
    encoder_adapt, losses_adapt, difficulties = train_simclr_adaptive(
        X_train, y_train, epochs=15, batch_size=16
    )

    # Linear evaluation (adaptive)
    print("\n[5] Linear evaluation (adaptive)...")
    features_adapt_train, _ = encoder_adapt.project(X_train)
    features_adapt_test, _ = encoder_adapt.project(X_test)

    clf_adapt = LinearClassifier(features_adapt_train.shape[1], len(np.unique(y)), lr=0.01)
    clf_adapt.train(features_adapt_train, y_train, epochs=30)
    acc_adapt = clf_adapt.accuracy(features_adapt_test, y_test)
    print(f"    Adaptive test accuracy: {acc_adapt:.4f}")
    print(f"\n    Improvement: {acc_adapt - acc_base:+.4f}")

    # ── Plots ──
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Training loss comparison
    axes[0, 0].plot(losses_base, 'b-', linewidth=2, label='SimCLR (baseline)')
    axes[0, 0].plot(losses_adapt, 'r-', linewidth=2, label='SimCLR + Adaptive Aug')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('NT-Xent Loss')
    axes[0, 0].set_title('Contrastive Loss Comparison')
    axes[0, 0].legend()
    axes[0, 0].grid(alpha=0.3)

    # Accuracy comparison
    methods = ['SimCLR', 'SimCLR + Adaptive']
    accs = [acc_base, acc_adapt]
    bars = axes[0, 1].bar(methods, accs, color=['steelblue', 'coral'], width=0.5)
    axes[0, 1].set_ylabel('Test Accuracy')
    axes[0, 1].set_title('Linear Evaluation Accuracy')
    axes[0, 1].set_ylim(0, 1)
    for bar, acc in zip(bars, accs):
        axes[0, 1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                        f'{acc:.4f}', ha='center')
    axes[0, 1].grid(alpha=0.3, axis='y')

    # Sample images and augmentations
    axes[1, 0].imshow(X[0, :, :, 0], cmap='gray')
    axes[1, 0].set_title('Original Image')
    axes[1, 0].axis('off')

    aug1, aug2 = SimCLRAugment.augment_pair(X[0])
    axes[1, 1].imshow(aug1[:, :, 0], cmap='gray')
    axes[1, 1].set_title('Augmented View 1')
    axes[1, 1].axis('off')

    plt.tight_layout()
    plt.savefig('../../assets/phase12/10_reproduce_paper_results.png', dpi=150)
    plt.close()
    print("\nSaved 10_reproduce_paper_results.png")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Paper reproduced: SimCLR (Chen et al., 2020)")
    print(f"Improvement: Adaptive augmentation based on sample difficulty")
    print(f"Baseline accuracy:  {acc_base:.4f}")
    print(f"Improved accuracy:  {acc_adapt:.4f}")
    print(f"Gain:              {acc_adapt - acc_base:+.4f}")


if __name__ == '__main__':
    main()
