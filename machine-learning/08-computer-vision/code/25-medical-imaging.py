"""08.25 Medical imaging: segmentation, detection, registration."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, affine_transform, binary_erosion, binary_dilation

np.random.seed(42)

img_size = 128
n_organs = 3

ct_scan = np.random.randn(img_size, img_size) * 50 + 100
ct_scan = gaussian_filter(ct_scan, sigma=2)

organ_masks = np.zeros((n_organs, img_size, img_size))
for i in range(n_organs):
    cx = np.random.randint(30, img_size - 30)
    cy = np.random.randint(30, img_size - 30)
    rx = np.random.randint(10, 25)
    ry = np.random.randint(10, 25)
    angle = np.random.uniform(0, np.pi)
    yy, xx = np.ogrid[:img_size, :img_size]
    mask = ((xx - cx) * np.cos(angle) + (yy - cy) * np.sin(angle))**2 / rx**2 + \
           ((-(xx - cx) * np.sin(angle) + (yy - cy) * np.cos(angle))**2) / ry**2 <= 1
    organ_masks[i] = mask
    intens = np.random.uniform(50, 200)
    ct_scan[mask] += intens + np.random.randn(np.sum(mask)) * 20

seg_pred = np.zeros((n_organs, img_size, img_size))
for i in range(n_organs):
    seg_pred[i] = gaussian_filter(organ_masks[i].astype(float), sigma=3) > 0.4

dice_scores = []
for i in range(n_organs):
    intersection = np.sum(seg_pred[i] * organ_masks[i])
    union = np.sum(seg_pred[i]) + np.sum(organ_masks[i])
    dice_scores.append(2 * intersection / (union + 1e-10) if union > 0 else 0)

tumor = np.zeros((img_size, img_size))
tumor[50:60, 40:55] = 1
tumor = gaussian_filter(tumor, sigma=1) > 0.3

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].imshow(ct_scan, cmap="gray")
axes[0, 0].set_title("CT Scan\n(with synthetic organs)")
axes[0, 0].axis("off")
plt.colorbar(axes[0, 0].images[0], ax=axes[0, 0])

seg_rgb = np.zeros((img_size, img_size, 3))
colors = plt.cm.Set2(np.linspace(0, 1, n_organs))
for i in range(n_organs):
    for c in range(3):
        seg_rgb[:, :, c] += organ_masks[i] * colors[i, c]
axes[0, 1].imshow(np.clip(seg_rgb, 0, 1))
axes[0, 1].set_title("Ground Truth\nOrgan Segmentation")
axes[0, 1].axis("off")

pred_rgb = np.zeros((img_size, img_size, 3))
for i in range(n_organs):
    for c in range(3):
        pred_rgb[:, :, c] += seg_pred[i] * colors[i, c]
axes[0, 2].imshow(np.clip(pred_rgb, 0, 1))
axes[0, 2].set_title(f"Predicted Segmentation\n(Dice mean={np.mean(dice_scores):.3f})")
axes[0, 2].axis("off")

axes[1, 0].bar(range(n_organs), dice_scores, color=colors, alpha=0.7)
axes[1, 0].axhline(np.mean(dice_scores), color="k", ls="--",
                   label=f"Mean={np.mean(dice_scores):.3f}")
axes[1, 0].set_xlabel("Organ")
axes[1, 0].set_ylabel("Dice coefficient")
axes[1, 0].set_title("Segmentation Quality\nper Organ")
axes[1, 0].legend()
axes[1, 0].grid(True, axis="y", alpha=0.3)

tumor_rgb = np.zeros((img_size, img_size, 3))
tumor_rgb[:, :, 0] = ct_scan / ct_scan.max() * 0.5
tumor_rgb[:, :, 1] = tumor * 0.8
axes[1, 1].imshow(np.clip(tumor_rgb * 1.5, 0, 1))
axes[1, 1].set_title(f"Tumor Detection\n({int(np.sum(tumor))} px tumor)")
axes[1, 1].axis("off")

img_moved = affine_transform(ct_scan, np.array([[1, 0.1], [0.1, 1]]), offset=[-5, 3])
diff = ct_scan - img_moved
axes[1, 2].imshow(diff, cmap="RdBu", vmin=-50, vmax=50)
axes[1, 2].set_title(f"Registration: Before-After\n"
                     f"RMSE={np.sqrt(np.mean(diff**2)):.1f} HU")
axes[1, 2].axis("off")
plt.colorbar(axes[1, 2].images[0], ax=axes[1, 2])

plt.tight_layout()
plt.savefig("../../assets/phase08/25-medical-imaging.png")
plt.close()

print("=" * 60)
print("MEDICAL IMAGING")
print("=" * 60)
print(f"\nCT scan: {img_size}×{img_size}, {n_organs} organs")
print(f"  Intensity range: [{ct_scan.min():.0f}, {ct_scan.max():.0f}] HU")
print(f"  Organ Dice scores: {np.round(dice_scores, 4)}")
print(f"  Mean Dice: {np.mean(dice_scores):.4f}")

print(f"\nTumor detection:")
tumor_area = np.sum(tumor)
print(f"  Tumor area: {tumor_area} px ({tumor_area/img_size**2*100:.2f}%)")

print(f"\nRegistration:")
registration_rmse = np.sqrt(np.mean(diff**2))
print(f"  RMSE: {registration_rmse:.2f} HU")

print(f"\nMedical imaging tasks:")
print(f"  • Segmentation: organ/tumor delineation")
print(f"    → U-Net, nnU-Net, TransUNet")
print(f"  • Detection: lesions, nodules, abnormalities")
print(f"    → RetinaNet, DETR for medical")
print(f"  • Registration: align multi-modal/multi-time")
print(f"    → Rigid, affine, deformable (VoxelMorph)")
print(f"  • Classification: disease diagnosis")
print(f"    → CheXNet, COVID-Net")
