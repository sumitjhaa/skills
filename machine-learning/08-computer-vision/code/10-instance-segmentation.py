"""08.10 Instance segmentation: Mask R-CNN, SOLO, YOLACT."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import label, center_of_mass

np.random.seed(42)

n_objects = 5
img_size = 100
img = np.zeros((img_size, img_size))
masks = np.zeros((n_objects, img_size, img_size))
boxes = np.zeros((n_objects, 4))
for i in range(n_objects):
    cx, cy = np.random.randint(15, 85, 2)
    w, h = np.random.randint(10, 30, 2)
    x1, x2 = max(0, cx - w//2), min(img_size, cx + w//2)
    y1, y2 = max(0, cy - h//2), min(img_size, cy + h//2)
    masks[i, y1:y2, x1:x2] = 1.0
    boxes[i] = [x1, y1, x2, y2]
    if i % 2 == 0:
        r = min(w, h) // 2
        y, x = np.ogrid[:img_size, :img_size]
        circle = (x - cx)**2 + (y - cy)**2 <= r**2
        masks[i] = circle
    img += masks[i] * np.random.uniform(0.5, 1.0)
img = np.clip(img, 0, 1)
img += 0.02 * np.random.randn(img_size, img_size)

scores = np.sort(np.random.rand(n_objects))[::-1]

nms_mask = np.zeros((img_size, img_size))
for i in range(n_objects):
    nms_mask[masks[i] > 0] = i + 1

iou_matrix = np.zeros((n_objects, n_objects))
for i in range(n_objects):
    for j in range(n_objects):
        intersection = np.sum(masks[i] * masks[j])
        union = np.sum(np.clip(masks[i] + masks[j], 0, 1))
        iou_matrix[i, j] = intersection / union if union > 0 else 0

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].imshow(img, cmap="gray")
axes[0, 0].set_title("Input Image\n(5 objects with masks)")
axes[0, 0].axis("off")

mask_overlay = np.zeros((*img.shape, 3))
colors = plt.cm.tab10(np.linspace(0, 1, n_objects))
for i in range(n_objects):
    for c in range(3):
        mask_overlay[:, :, c] += masks[i] * colors[i, c] * 0.5
mask_overlay = np.clip(mask_overlay, 0, 1)
axes[0, 1].imshow(mask_overlay)
axes[0, 1].set_title("Ground Truth Masks\n(+ bounding boxes)")
axes[0, 1].axis("off")
for i in range(n_objects):
    x1, y1, x2, y2 = boxes[i]
    axes[0, 1].plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1],
                   color=colors[i], lw=1.5)

axes[0, 2].imshow(iou_matrix, cmap="Blues", vmin=0, vmax=1)
for i in range(n_objects):
    for j in range(n_objects):
        axes[0, 2].text(j, i, f"{iou_matrix[i, j]:.2f}", ha="center", va="center",
                       fontsize=8)
axes[0, 2].set_xlabel("Predicted mask index")
axes[0, 2].set_ylabel("Ground truth index")
axes[0, 2].set_title("IoU Matrix\n(mask matching)")
plt.colorbar(axes[0, 2].images[0], ax=axes[0, 2])

axes[1, 0].bar(range(n_objects), scores, color=colors, alpha=0.7)
axes[1, 0].axhline(0.5, color="r", ls="--", label="Threshold=0.5")
axes[1, 0].set_xlabel("Object index")
axes[1, 0].set_ylabel("Confidence score")
axes[1, 0].set_title("Detection Scores\n(NMS threshold)")
axes[1, 0].legend()
axes[1, 0].grid(True, axis="y", alpha=0.3)

mask_sizes = [np.sum(m > 0) for m in masks]
axes[1, 1].bar(range(n_objects), mask_sizes, color=colors, alpha=0.7)
axes[1, 1].set_xlabel("Object index")
axes[1, 1].set_ylabel("Pixel count")
axes[1, 1].set_title("Mask Sizes")
axes[1, 1].grid(True, axis="y", alpha=0.3)

precision = []
recall = []
for t in np.linspace(0, 1, 30):
    tp = np.sum(scores >= t)
    fp = max(0, n_objects - tp)
    fn = max(0, n_objects - tp)
    precision.append(tp / (tp + fp) if tp + fp > 0 else 0)
    recall.append(tp / (tp + fn) if tp + fn > 0 else 0)
axes[1, 2].plot(recall, precision, "o-", lw=2)
axes[1, 2].set_xlabel("Recall")
axes[1, 2].set_ylabel("Precision")
axes[1, 2].set_title("Precision-Recall Curve\n(mAP estimation)")
axes[1, 2].grid(True, alpha=0.3)
ap = np.sum(precision) * (recall[1] - recall[0])
axes[1, 2].set_title(f"PR Curve (mAP ≈ {ap:.3f})")

plt.tight_layout()
plt.savefig("../../assets/phase08/10-instance-segmentation.png")
plt.close()

print("=" * 60)
print("INSTANCE SEGMENTATION")
print("=" * 60)
print(f"\nDataset: {n_objects} objects on {img_size}×{img_size} image")
print(f"  Mask sizes: {mask_sizes}")
average_iou = np.mean([iou_matrix[i, i] for i in range(n_objects)])
print(f"  Average self-IoU: {average_iou:.4f}")

print(f"\nmAP estimation: {ap:.4f}")
print(f"  Detection scores: {np.round(scores, 3)}")
print(f"  IoU threshold typically 0.5 for mAP@0.5")

print(f"\nInstance Segmentation approaches:")
print(f"  • Mask R-CNN: Faster R-CNN + mask head")
print(f"    → Two-stage (detect then segment)")
print(f"    → RoIAlign for pixel-perfect masks")
print(f"  • SOLO: Fully convolutional, no bounding boxes")
print(f"    → Divide image into grids, predict masks")
print(f"  • YOLACT: Real-time (30+ FPS)")
print(f"    → Prototype masks + linear combination")
print(f"    → Parallel: classification + mask coefficients")
print(f"  • Panoptic FPN: instance + semantic together")
