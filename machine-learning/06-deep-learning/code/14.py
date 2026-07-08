"""06.14 - Augmentation: Flip, rotate, crop, noise, color jitter, mixup, cutout"""

import numpy as np
import matplotlib.pyplot as plt


def random_horizontal_flip(x, p=0.5):
    if np.random.random() < p:
        return x[:, :, ::-1]
    return x

def random_rotation(x, max_angle=15):
    angle = np.random.uniform(-max_angle, max_angle)
    rad = np.deg2rad(angle)
    c, s = np.cos(rad), np.sin(rad)
    H, W = x.shape[1:]
    cx, cy = W / 2, H / 2
    y, x_coords = np.meshgrid(np.arange(H), np.arange(W), indexing="ij")
    ox = (x_coords - cx) * c - (y - cy) * s + cx
    oy = (x_coords - cx) * s + (y - cy) * c + cy
    ox = np.clip(ox, 0, W - 1).astype(int)
    oy = np.clip(oy, 0, H - 1).astype(int)
    out = np.zeros_like(x)
    for c in range(x.shape[0]):
        out[c] = x[c, oy, ox]
    return out

def random_crop(x, padding=4):
    C, H, W = x.shape
    x_pad = np.pad(x, ((0, 0), (padding, padding), (padding, padding)), mode="reflect")
    top = np.random.randint(0, 2 * padding + 1)
    left = np.random.randint(0, 2 * padding + 1)
    return x_pad[:, top:top + H, left:left + W]

def add_gaussian_noise(x, std=0.05):
    noise = np.random.randn(*x.shape) * std
    return np.clip(x + noise, 0, 1)

def color_jitter(x, brightness=0.2, contrast=0.2):
    x_out = x.copy()
    b_factor = 1 + np.random.uniform(-brightness, brightness)
    c_factor = 1 + np.random.uniform(-contrast, contrast)
    x_out = x_out * c_factor
    x_out = x_out + b_factor * np.mean(x_out)
    return np.clip(x_out, 0, 1)

def mixup(x1, x2, y1, y2, alpha=1.0):
    lam = np.random.beta(alpha, alpha)
    x = lam * x1 + (1 - lam) * x2
    y = lam * y1 + (1 - lam) * y2
    return x, y

def cutout(x, size=16):
    C, H, W = x.shape
    top = np.random.randint(0, H - size + 1) if H > size else 0
    left = np.random.randint(0, W - size + 1) if W > size else 0
    x_out = x.copy()
    x_out[:, top:top + size, left:left + size] = 0
    return x_out


if __name__ == "__main__":
    np.random.seed(42)

    img = np.random.rand(3, 32, 32)

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    transforms = [
        ("Original", img),
        ("Horizontal Flip", random_horizontal_flip(img)),
        ("Rotation", random_rotation(img, 30)),
        ("Random Crop", random_crop(img, 4)),
        ("Gaussian Noise", add_gaussian_noise(img, 0.1)),
        ("Color Jitter", color_jitter(img)),
        ("Cutout", cutout(img, 8)),
    ]

    for idx, (name, aug_img) in enumerate(transforms):
        ax = axes[idx // 4][idx % 4]
        ax.imshow(np.transpose(aug_img, (1, 2, 0)))
        ax.set_title(name)
        ax.axis("off")

    x1, x2 = np.random.rand(3, 32, 32), np.random.rand(3, 32, 32)
    y1, y2 = np.array([1, 0, 0]), np.array([0, 1, 0])
    mixed_x, mixed_y = mixup(x1, x2, y1, y2, alpha=1.0)
    axes[1, 3].imshow(np.transpose(mixed_x, (1, 2, 0)))
    axes[1, 3].set_title(f"Mixup (λ={mixed_y[0]:.2f})")
    axes[1, 3].axis("off")

    plt.tight_layout()
    plt.savefig("../../assets/phase06/augmentation.png")
    plt.close()
    print(f"Original shape: {img.shape}")
    print(f"Mixup label: {mixed_y}")
    print("All augmentations implemented and plotted.")
