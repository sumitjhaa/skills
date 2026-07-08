"""08.11 Semantic segmentation: FCN, DeepLab, U-Net."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, binary_dilation, label

np.random.seed(42)

img_size = 128
n_classes = 5

img = np.zeros((img_size, img_size, 3))
seg = np.zeros((img_size, img_size), dtype=int)

for i in range(n_classes):
    cx, cy = np.random.randint(20, img_size-20, 2)
    r = np.random.randint(15, 35)
    yy, xx = np.ogrid[:img_size, :img_size]
    mask = (xx - cx)**2 + (yy - cy)**2 <= r**2
    seg[mask] = i
    img[mask] = np.random.uniform(0.3, 0.9, 3)

seg = gaussian_filter(seg.astype(float), sigma=3)
seg = np.round(seg).astype(int) % n_classes

img += 0.05 * np.random.randn(*img.shape)
img = np.clip(img, 0, 1)

pred = seg + np.random.randint(-1, 2, seg.shape)
pred = np.clip(pred, 0, n_classes - 1)

pixel_acc = np.mean(pred == seg)
iou_per_class = []
for c in range(n_classes):
    intersection = np.sum((pred == c) & (seg == c))
    union = np.sum((pred == c) | (seg == c))
    iou_per_class.append(intersection / union if union > 0 else 0)
miou = np.mean(iou_per_class)

confusion = np.zeros((n_classes, n_classes), dtype=int)
for i in range(n_classes):
    for j in range(n_classes):
        confusion[i, j] = np.sum((seg == i) & (pred == j))

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].imshow(img)
axes[0, 0].set_title("Input Image")
axes[0, 0].axis("off")

seg_rgb = np.zeros((*seg.shape, 3))
colors = plt.cm.tab10(np.linspace(0, 1, n_classes))
for c in range(n_classes):
    for ch in range(3):
        seg_rgb[:, :, ch] += (seg == c) * colors[c, ch]
axes[0, 1].imshow(seg_rgb)
axes[0, 1].set_title("Ground Truth\n(Semantic Segmentation)")
axes[0, 1].axis("off")

pred_rgb = np.zeros((*pred.shape, 3))
for c in range(n_classes):
    for ch in range(3):
        pred_rgb[:, :, ch] += (pred == c) * colors[c, ch]
axes[0, 2].imshow(pred_rgb)
axes[0, 2].set_title(f"Prediction\n(pixel acc={pixel_acc:.3f})")
axes[0, 2].axis("off")

axes[1, 0].imshow(confusion, cmap="Blues", interpolation="nearest")
for i in range(n_classes):
    for j in range(n_classes):
        axes[1, 0].text(j, i, str(confusion[i, j]), ha="center", va="center", fontsize=8)
axes[1, 0].set_xlabel("Predicted class")
axes[1, 0].set_ylabel("True class")
axes[1, 0].set_title("Confusion Matrix")
plt.colorbar(axes[1, 0].images[0], ax=axes[1, 0])

axes[1, 1].bar(range(n_classes), iou_per_class, color=colors, alpha=0.7)
axes[1, 1].axhline(miou, color="r", ls="--", label=f"mIoU={miou:.3f}")
axes[1, 1].set_xlabel("Class")
axes[1, 1].set_ylabel("IoU")
axes[1, 1].set_title("Per-class IoU")
axes[1, 1].legend()
axes[1, 1].grid(True, axis="y", alpha=0.3)

n_noise = np.linspace(0, 0.5, 20)
miou_noise = []
for n in n_noise:
    p_noisy = seg + np.random.randint(-2, 3, seg.shape)
    p_noisy = np.clip(p_noisy, 0, n_classes - 1)
    ious = []
    for c in range(n_classes):
        i = np.sum((p_noisy == c) & (seg == c))
        u = np.sum((p_noisy == c) | (seg == c))
        ious.append(i / u if u > 0 else 0)
    miou_noise.append(np.mean(ious))
axes[1, 2].plot(n_noise, miou_noise, "o-", lw=2)
axes[1, 2].set_xlabel("Noise level")
axes[1, 2].set_ylabel("mIoU")
axes[1, 2].set_title("Segmentation Robustness")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/11-semantic-segmentation.png")
plt.close()

print("=" * 60)
print("SEMANTIC SEGMENTATION")
print("=" * 60)
print(f"\nImage: {img_size}×{img_size}, {n_classes} classes")
print(f"  Pixel accuracy: {pixel_acc:.4f}")
print(f"  Mean IoU: {miou:.4f}")
print(f"  Per-class IoU: {np.round(iou_per_class, 4)}")

print(f"\nConfusion matrix (rows=true, cols=pred):")
print(confusion)

print(f"\nKey architectures:")
print(f"  • FCN: fully convolutional, skip connections")
print(f"  • U-Net: encoder-decoder w/ skip connections")
print(f"    → Medical imaging (few labels)")
print(f"    → Symmetric encoder-decoder")
print(f"  • DeepLab: atrous convolution + ASPP")
print(f"    → Atrous Spatial Pyramid Pooling")
print(f"    → Dilated conv for larger receptive field")
print(f"  • SegFormer: transformer-based segmentation")
print(f"  • Mask2Former: universal architecture (semantic+instance+panoptic)")
