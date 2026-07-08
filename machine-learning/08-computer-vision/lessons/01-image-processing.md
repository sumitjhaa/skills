# Lesson 08.01: Image Processing

## Learning Objectives
- Understand convolution, filtering, and their properties
- Implement Gaussian, Sobel, and median filtering
- Apply histogram equalization for contrast enhancement
- Choose appropriate color spaces for different tasks

## Convolution
A convolution applies a kernel $K$ over an image $I$:

$$(I * K)(x,y) = \sum_{i=-a}^{a}\sum_{j=-b}^{b} I(x-i, y-j) \, K(i,j)$$

### Properties
- **Linear**: $I * (K_1 + K_2) = (I * K_1) + (I * K_2)$
- **Commutative**: $I * K = K * I$
- **Associative**: $(I * K_1) * K_2 = I * (K_1 * K_2)$
- **Differentiation**: $\frac{\partial}{\partial x}(I * K) = I * \frac{\partial K}{\partial x}$

### Common Kernels
| Operation | Kernel | Effect |
|-----------|--------|--------|
| Identity | $\begin{bmatrix}0&0&0\\0&1&0\\0&0&0\end{bmatrix}$ | No change |
| Box blur | $\frac{1}{9}\begin{bmatrix}1&1&1\\1&1&1\\1&1&1\end{bmatrix}$ | Average |
| Gaussian | $G(x,y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}$ | Smooth |
| Sobel X | $\begin{bmatrix}-1&0&1\\-2&0&2\\-1&0&1\end{bmatrix}$ | Vertical edges |
| Sobel Y | $\begin{bmatrix}-1&-2&-1\\0&0&0\\1&2&1\end{bmatrix}$ | Horizontal edges |
| Laplacian | $\begin{bmatrix}0&1&0\\1&-4&1\\0&1&0\end{bmatrix}$ | Edge detection |

## Filtering

### Low-Pass (Blur)
Attenuates high frequencies. Gaussian blur radius controlled by $\sigma$:
- Small $\sigma$: subtle blur
- Large $\sigma$: strong blur (removes fine details)

### High-Pass (Edge Enhancement)
Amplifies high frequencies. Magnitude: $|G| = \sqrt{G_x^2 + G_y^2}$.

### Median Filter
Non-linear filter replacing pixel with median of neighbors:
- Excellent for salt-and-pepper noise
- Preserves edges better than Gaussian blur

### Bilateral Filter
$$\text{BF}[I]_p = \frac{1}{W_p} \sum_{q \in S} G_{\sigma_s}(\|p-q\|) G_{\sigma_r}(|I_p - I_q|) I_q$$

- $\sigma_s$: spatial sigma
- $\sigma_r$: range (intensity) sigma
- **Edge-preserving smoothing**

## Histogram Equalization

Maps pixel intensities so output histogram is approximately uniform:

$$T(i) = \lfloor (L-1) \cdot \text{CDF}(i) \rfloor$$
$$\text{CDF}(i) = \sum_{j=0}^{i} p(j)$$

- $p(j)$: probability of intensity $j$
- $L$: number of intensity levels (e.g., 256)
- **Effect**: Enhances contrast, especially for underexposed images

### Adaptive Histogram Equalization (AHE)
Apply equalization locally in tiles. **CLAHE (Contrast Limited AHE)**: Clip histogram to limit noise amplification.

## Color Spaces

| Space | Components | Use Case |
|-------|-----------|----------|
| RGB | Red, Green, Blue | Display, cameras |
| HSV | Hue, Saturation, Value | Color-based segmentation |
| LAB | Luminance, a (green-red), b (blue-yellow) | Perceptually uniform |
| YUV | Luma + Chroma | Video compression |
| Grayscale | Single intensity | Shape analysis, efficiency |

### Conversion: RGB to Grayscale
$$Y = 0.299 R + 0.587 G + 0.114 B$$

## Code: Image Filtering

```python
import numpy as np
from scipy import ndimage
from skimage import exposure, color

def gaussian_filter(image, sigma=1.0):
    return ndimage.gaussian_filter(image, sigma)

def sobel_edges(image):
    grad_x = ndimage.sobel(image, axis=1)
    grad_y = ndimage.sobel(image, axis=0)
    return np.sqrt(grad_x**2 + grad_y**2)

def median_filter(image, size=3):
    return ndimage.median_filter(image, size=size)

def histogram_equalization(image):
    return exposure.equalize_hist(image)
```

## Applications
- **Preprocessing**: Noise removal, contrast enhancement for ML input
- **Feature extraction**: Edge detection, corner detection
- **Segmentation**: Thresholding in appropriate color space
- **Image restoration**: Deblurring, denoising, inpainting
- **Data augmentation**: Random brightness/contrast/hue shifts

## References
- Gonzalez & Woods, "Digital Image Processing", 4th ed.
- Szeliski, "Computer Vision: Algorithms and Applications", 2nd ed.
- Bradski & Kaehler, "Learning OpenCV"
- Paris et al., "Bilateral Filtering: Theory and Applications", Foundations and Trends in Computer Graphics and Vision, 2009
- Zuiderveld, "Contrast Limited Adaptive Histogram Equalization", Graphics Gems IV, 1994
