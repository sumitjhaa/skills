"""08.02 Feature detection: Harris, SIFT, corner detection."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import sobel, gaussian_filter

np.random.seed(42)

img = np.zeros((100, 100))
img[30:70, 30:70] = 1.0
img[50:55, 20:80] = 0.5
img[20:80, 50:55] = 0.3
img = gaussian_filter(img, sigma=1.5)
img += 0.05 * np.random.randn(100, 100)

Ix = sobel(img, axis=1)
Iy = sobel(img, axis=0)

sigma = 2.0
window = 5
offset = window // 2
R = np.zeros_like(img)
for y in range(offset, img.shape[0] - offset):
    for x in range(offset, img.shape[1] - offset):
        patch = img[y-offset:y+offset+1, x-offset:x+offset+1]
        Sxx = np.sum(Ix[y-offset:y+offset+1, x-offset:x+offset+1]**2)
        Syy = np.sum(Iy[y-offset:y+offset+1, x-offset:x+offset+1]**2)
        Sxy = np.sum(Ix[y-offset:y+offset+1, x-offset:x+offset+1] *
                     Iy[y-offset:y+offset+1, x-offset:x+offset+1])
        det = Sxx * Syy - Sxy**2
        trace = Sxx + Syy
        R[y, x] = det - 0.04 * trace**2

threshold = 0.1 * R.max()
corners = np.argwhere(R > threshold)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].imshow(img, cmap="gray")
axes[0, 0].set_title("Synthetic Image\n(square + bars)")
axes[0, 0].axis("off")
plt.colorbar(axes[0, 0].images[0], ax=axes[0, 0])

mag = np.sqrt(Ix**2 + Iy**2)
axes[0, 1].imshow(mag, cmap="hot")
axes[0, 1].set_title("Gradient Magnitude")
axes[0, 1].axis("off")
plt.colorbar(axes[0, 1].images[0], ax=axes[0, 1])

axes[0, 2].imshow(R, cmap="hot")
axes[0, 2].set_title("Harris Corner Response R")
axes[0, 2].axis("off")
plt.colorbar(axes[0, 2].images[0], ax=axes[0, 2])

axes[1, 0].imshow(img, cmap="gray")
for y, x in corners[::max(1, len(corners)//30)]:
    axes[1, 0].plot(x, y, "ro", ms=4)
axes[1, 0].set_title(f"Detected Corners ({len(corners)})")
axes[1, 0].axis("off")

orient = np.arctan2(Iy, Ix)
axes[1, 1].imshow(orient, cmap="hsv")
axes[1, 1].set_title("Gradient Orientation")
axes[1, 1].axis("off")
plt.colorbar(axes[1, 1].images[0], ax=axes[1, 1])

hist_bins = np.linspace(-np.pi, np.pi, 20)
hist_orient = np.histogram(orient[mag > mag.mean()], bins=hist_bins)[0]
axes[1, 2].bar(hist_bins[:-1], hist_orient, width=np.pi/10, alpha=0.7)
axes[1, 2].set_xlabel("Orientation (rad)")
axes[1, 2].set_ylabel("Count")
axes[1, 2].set_title("Dominant Orientations")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/02-feature-detection.png")
plt.close()

print("=" * 60)
print("FEATURE DETECTION")
print("=" * 60)
print(f"\nImage: {img.shape[0]}×{img.shape[1]}")
print(f"  Corners detected: {len(corners)}")
print(f"  Threshold: {threshold:.4f}")
print(f"  R range: [{R.min():.4f}, {R.max():.4f}]")

R_sorted = np.sort(R.ravel())[::-1]
top_corners = np.sum(R_sorted > 0.5 * R_sorted[0])
print(f"  Top 50% response: ~{top_corners} corners")

print(f"\nHarris corner detector:")
print(f"  R = det(M) - α·tr(M)² (α=0.04)")
print(f"  M = [[Ix², IxIy], [IxIy, Iy²]] (structure tensor)")
print(f"  R > 0 → corner, R < 0 → edge, |R| small → flat")
print(f"\nKey properties:")
print(f"  • Rotation invariant (uses gradient magnitude)")
print(f"  • Not scale invariant (requires fixed window)")
print(f"  • SIFT/ORB extend with scale-space pyramid)")
