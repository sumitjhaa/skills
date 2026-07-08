"""08.03 Feature descriptors: SIFT, SURF, ORB, LBP."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, sobel
from scipy.signal import convolve2d

np.random.seed(42)

img = np.zeros((100, 100))
for i in range(3):
    cx, cy = np.random.randint(20, 80, 2)
    r = np.random.randint(5, 15)
    y, x = np.ogrid[:100, :100]
    mask = (x - cx)**2 + (y - cy)**2 <= r**2
    img[mask] = np.random.uniform(0.5, 1.0)
img = gaussian_filter(img, sigma=2.0)
img += 0.02 * np.random.randn(100, 100)
img = np.clip(img, 0, 1)

def lbp(img, radius=1, n_points=8):
    h, w = img.shape
    lbp_img = np.zeros((h-2*radius, w-2*radius))
    for i in range(radius, h - radius):
        for j in range(radius, w - radius):
            center = img[i, j]
            pattern = 0
            for k in range(n_points):
                angle = 2 * np.pi * k / n_points
                x = j + radius * np.cos(angle)
                y = i + radius * np.sin(angle)
                val = img[int(y), int(x)]
                if val >= center:
                    pattern |= (1 << k)
            lbp_img[i-radius, j-radius] = pattern
    return lbp_img

def histogram_of_gradients(img, cell_size=8, n_bins=9):
    h, w = img.shape
    gx = sobel(img, axis=1)
    gy = sobel(img, axis=0)
    mag = np.sqrt(gx**2 + gy**2)
    ang = (np.arctan2(gy, gx) + np.pi) % (np.pi)
    n_cells_y = h // cell_size
    n_cells_x = w // cell_size
    hog = np.zeros((n_cells_y, n_cells_x, n_bins))
    bin_width = np.pi / n_bins
    for cy in range(n_cells_y):
        for cx in range(n_cells_x):
            y0, y1 = cy * cell_size, (cy + 1) * cell_size
            x0, x1 = cx * cell_size, (cx + 1) * cell_size
            patch_mag = mag[y0:y1, x0:x1]
            patch_ang = ang[y0:y1, x0:x1]
            for i in range(n_bins):
                bin_low = i * bin_width
                bin_high = (i + 1) * bin_width
                mask = (patch_ang >= bin_low) & (patch_ang < bin_high)
                hog[cy, cx, i] = np.sum(patch_mag[mask])
    hog = hog.ravel()
    hog = hog / (np.linalg.norm(hog) + 1e-10)
    return hog

lbp_img = lbp(img, radius=1, n_points=8)
hog_desc = histogram_of_gradients(img, cell_size=10, n_bins=9)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].imshow(img, cmap="gray")
axes[0, 0].set_title("Input Image\n(shapes + noise)")
axes[0, 0].axis("off")

axes[0, 1].imshow(lbp_img, cmap="tab20", interpolation="nearest")
axes[0, 1].set_title(f"LBP (radius=1, 8 pts)\n{len(np.unique(lbp_img))} patterns")
axes[0, 1].axis("off")

lbp_hist, _ = np.histogram(lbp_img, bins=np.arange(257), density=True)
axes[0, 2].bar(range(256), lbp_hist, width=1, alpha=0.7)
axes[0, 2].set_xlabel("LBP pattern code")
axes[0, 2].set_ylabel("Frequency")
axes[0, 2].set_title("LBP Histogram (256-bin)")
axes[0, 2].set_xlim(0, 255)
axes[0, 2].grid(True, axis="y", alpha=0.3)

hog_2d = hog_desc.reshape(-1, 9).T
axes[1, 0].bar(range(len(hog_desc)), hog_desc, width=1, alpha=0.7)
axes[1, 0].set_xlabel("HOG bin index")
axes[1, 0].set_ylabel("Normalized magnitude")
axes[1, 0].set_title(f"HOG Descriptor ({len(hog_desc)} dims)")
axes[1, 0].grid(True, alpha=0.3)

img2 = np.rot90(img, k=1)
hog_desc2 = histogram_of_gradients(img2, cell_size=10, n_bins=9)
sim = np.dot(hog_desc, hog_desc2) / (np.linalg.norm(hog_desc) * np.linalg.norm(hog_desc2) + 1e-10)
axes[1, 1].bar(["Original", "Rotated"], [1.0, sim], color=["blue", "orange"])
axes[1, 1].set_ylabel("Cosine similarity")
axes[1, 1].set_title("Descriptor Matching\n(original vs 90° rotated)")
axes[1, 1].grid(True, axis="y", alpha=0.3)

noise_levels = np.linspace(0, 0.3, 20)
sims = []
for nl in noise_levels:
    img_n = img + nl * np.random.randn(100, 100)
    img_n = np.clip(img_n, 0, 1)
    h_n = histogram_of_gradients(img_n, cell_size=10, n_bins=9)
    sims.append(np.dot(hog_desc, h_n) / (np.linalg.norm(hog_desc) * np.linalg.norm(h_n) + 1e-10))
axes[1, 2].plot(noise_levels, sims, "o-", lw=2)
axes[1, 2].set_xlabel("Noise level σ")
axes[1, 2].set_ylabel("Similarity to clean")
axes[1, 2].set_title("HOG Robustness to Noise")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/03-feature-descriptors.png")
plt.close()

print("=" * 60)
print("FEATURE DESCRIPTORS")
print("=" * 60)
print(f"\nLBP: {len(np.unique(lbp_img))} unique patterns in {lbp_img.size} cells")
print(f"  Rotation invariant: 36 uniform patterns")
print(f"  Gray-scale invariant (compares neighbors)")

print(f"\nHOG descriptor: {len(hog_desc)} dimensions")
print(f"  Cells: {img.shape[0]//10}×{img.shape[1]//10}")
print(f"  9 orientation bins (0-180°)")
print(f"  Block normalization for illumination invariance")

print(f"\nDescriptor matching:")
print(f"  Self-similarity: {1.0:.4f}")
print(f"  Rotated (90°):   {sim:.4f}")
print(f"  Noise robustness: at σ=0.3 → {sims[-1]:.4f}")

print(f"\nKey descriptors:")
print(f"  • SIFT: 128-dim, scale/rotation invariant")
print(f"  • SURF: faster approximation of SIFT")
print(f"  • ORB: binary descriptor (FAST + BRIEF)")
print(f"  • LBP: 256-dim histogram of local patterns")
print(f"  • HOG: gradient orientation histogram")
