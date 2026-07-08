# 29. PCA/SVD Pipeline: Eigenfaces, Compression, Denoising

## Introduction

This lesson builds an end-to-end pipeline using PCA/SVD for real-world computer vision tasks: eigenfaces (face recognition), image compression, and denoising.

## Eigenfaces

Eigenfaces are the principal components of a face image dataset. Each face is represented as a vector of pixel values. PCA finds the directions of最大 variance:

```python
def eigenfaces(face_images, k=50):
    mean_face = face_images.mean(axis=0)
    centered = face_images - mean_face
    U, s, Vt = np.linalg.svd(centered, full_matrices=False)
    return mean_face, Vt[:k], s[:k]
```

Each face can be represented by its k coefficients in the eigenface basis:

```python
def project_face(face, mean_face, eigenfaces):
    return eigenfaces @ (face - mean_face)
```

## Image Compression Pipeline

1. Convert image to grayscale
2. Compute SVD
3. Keep only top k singular values
4. Reconstruct from truncated SVD

```python
def compress_pipeline(img, k):
    U, s, Vt = np.linalg.svd(img, full_matrices=False)
    return U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :], s
```

## Denoising Pipeline

1. Compute SVD of noisy image
2. Threshold or truncate small singular values
3. Reconstruct

```python
def denoise_pipeline(img_noisy, threshold):
    U, s, Vt = np.linalg.svd(img_noisy, full_matrices=False)
    s_denoised = np.maximum(s - threshold, 0)
    return U @ np.diag(s_denoised) @ Vt
```

## End-to-End Pipeline

```python
def full_pipeline(dataset):
    # 1. Load and preprocess
    # 2. Compute PCA/SVD
    # 3. Train classifier in PCA space
    # 4. Evaluate on test set
    # 5. Visualize reconstructions
```

## What You'll Implement

- Eigenface computation from image dataset
- Face reconstruction at various compression levels
- Image compression with adjustable quality
- Denoising via singular value thresholding
- End-to-end pipeline with visualization
- Compare compression ratios and quality metrics
