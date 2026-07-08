"""
08.01 Image Processing — convolution, filtering, histogram equalisation
Usage: python 01-image-processing.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage, signal

np.random.seed(0)

# create a synthetic image
img = np.zeros((64, 64))
img[16:48, 16:48] = 1.0
img += np.random.randn(64, 64) * 0.1
img = np.clip(img, 0, 1)

# gaussian kernel
def gaussian_kernel(size=5, sigma=1.0):
    ax = np.linspace(-(size-1)/2, (size-1)/2, size)
    x, y = np.meshgrid(ax, ax)
    k = np.exp(-(x**2 + y**2) / (2*sigma**2))
    return k / k.sum()

kernel = gaussian_kernel(5, 1.0)
blurred = ndimage.convolve(img, kernel)

# sobel edge detection
sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
sobel_y = sobel_x.T
edges_x = ndimage.convolve(img, sobel_x)
edges_y = ndimage.convolve(img, sobel_y)
edges = np.hypot(edges_x, edges_y)

# histogram equalisation
def hist_eq(img, bins=256):
    hist, _ = np.histogram(img.flatten(), bins=bins, range=(0, 1))
    cdf = hist.cumsum()
    cdf_norm = cdf / cdf[-1]
    eq = np.interp(img.flatten(), np.linspace(0, 1, bins), cdf_norm)
    return eq.reshape(img.shape)

img_low = img * 0.2 + 0.05  # low contrast
eq = hist_eq(img_low)

# median filter (salt & pepper)
noisy = img.copy()
mask = np.random.rand(*img.shape) < 0.05
noisy[mask] = 1.0 - noisy[mask]
median = ndimage.median_filter(noisy, size=3)

fig, axes = plt.subplots(2, 4, figsize=(12, 6))
axes[0, 0].imshow(img, cmap='gray'); axes[0, 0].set_title('Original')
axes[0, 1].imshow(blurred, cmap='gray'); axes[0, 1].set_title('Gaussian Blur')
axes[0, 2].imshow(edges, cmap='gray'); axes[0, 2].set_title('Sobel Edges')
axes[0, 3].imshow(img_low, cmap='gray'); axes[0, 3].set_title('Low Contrast')
axes[1, 0].imshow(eq, cmap='gray'); axes[1, 0].set_title('Histogram Eq')
axes[1, 1].imshow(noisy, cmap='gray'); axes[1, 1].set_title('Salt & Pepper')
axes[1, 2].imshow(median, cmap='gray'); axes[1, 2].set_title('Median Filter')
for ax in axes.flat: ax.axis('off')
plt.tight_layout(); plt.savefig('../../assets/phase08/01_image_processing.png', dpi=100)
print("Saved 01_image_processing.png")
