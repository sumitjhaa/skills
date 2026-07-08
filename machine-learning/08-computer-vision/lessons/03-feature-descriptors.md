# Lesson 08.03: Feature Descriptors

## Learning Objectives
- Understand SIFT descriptor construction
- Implement SIFT/SURF/ORB matching pipeline
- Apply nearest-neighbor matching with RANSAC verification
- Compare learned vs hand-crafted descriptors

## SIFT (Scale-Invariant Feature Transform)

### Pipeline
1. **Scale-space extrema**: Difference-of-Gaussians (DoG) across scales ($\sigma = 1.6$, $3$ octaves)
2. **Keypoint localization**: Fit 3D quadratic to refine (x, y, scale); discard low contrast ($|D(\hat{x})| < 0.03$) and edge responses ($\text{tr}(H)^2 / \det(H) > 12.1$)
3. **Orientation assignment**: 36-bin gradient histogram over keypoint neighborhood
4. **Descriptor**: $4 \times 4$ grid of 8-bin orientation histograms → 128-D vector

### DoG Scale Space
$$D(x, y, \sigma) = (G(x, y, k\sigma) - G(x, y, \sigma)) * I(x, y)$$

- Detect local extrema in $3 \times 3 \times 3$ neighborhood (spatial + scale)

### Descriptor Normalization
1. Rotate to canonical orientation (rotation invariance)
2. Weight by Gaussian ($\sigma = \text{window size / 2}$)
3. Normalize to unit length, clip values $> 0.2$, re-normalize

## SURF (Speeded-Up Robust Features)

### Key Advantages
- **Integral images**: Box filter approximations (computes Haar-like features in constant time)
- **Hessian-based detector**: $\det(H) = D_{xx}D_{yy} - (0.9 D_{xy})^2$
- **64-D descriptor**: Sum of Haar wavelet responses in $4 \times 4$ subregions
- **U-SURF**: Upright SURF (no rotation invariance) for faster matching

## Descriptor Comparison

| Descriptor | Dimension | Scale Inv. | Rot. Inv. | Speed | Matching Accuracy |
|------------|-----------|------------|-----------|-------|------------------|
| SIFT | 128 | Yes | Yes | Slow | Excellent |
| SURF | 64/128 | Yes | Yes | Fast | Very good |
| ORB | 32 (binary) | Pyramid | Yes | Very fast | Good |
| BRIEF | 256 (binary) | No | No | Fast | Good |
| BRISK | 64 (binary) | Yes | Yes | Fast | Good |
| SuperPoint | 256 | Implicit | Yes | GPU | Excellent |
| D2-Net | 512 | Implicit | Yes | GPU | Excellent |

## Feature Matching

### Nearest-Neighbor Distance Ratio (NNDR)
$$\text{ratio} = \frac{d_1}{d_2} < \tau$$

- $d_1$: distance to nearest neighbor
- $d_2$: distance to second nearest neighbor
- $\tau \approx 0.6-0.8$
- Filters ambiguous matches (where two features look similar)

### RANSAC (Random Sample Consensus)
Geometric verification to remove outliers:
1. Randomly sample $k$ matches (4 for homography, 8 for fundamental matrix)
2. Fit model
3. Count inliers (points within $\varepsilon$ pixels of model)
4. Repeat N times, keep model with most inliers

## Code: SIFT Matching with RANSAC

```python
import cv2
import numpy as np

def sift_match(img1, img2, ratio_thresh=0.75, ransac_thresh=5.0):
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)
    
    # FLANN matcher
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    matcher = cv2.FlannBasedMatcher(index_params, {})
    matches = matcher.knnMatch(des1, des2, k=2)
    
    # Lowe's ratio test
    good = []
    for m, n in matches:
        if m.distance < ratio_thresh * n.distance:
            good.append(m)
    
    # RANSAC homography
    if len(good) >= 4:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, ransac_thresh)
        inliers = mask.ravel().tolist()
    else:
        H, inliers = None, None
    
    return kp1, kp2, good, H, inliers
```

## Evaluation Metrics
- **Repeatability**: Fraction of features detected in both images under viewpoint change
- **Matching score**: Ratio of correct matches to total features
- **Precision/Recall**: Trade-off in matching threshold
- **Tracking length**: How long features persist in video sequence

## Applications
- **Panorama stitching**: SIFT matching + homography warping (AutoStitch, Microsoft ICE)
- **Visual localization**: Match against database of geo-tagged images
- **3D reconstruction**: SfM pipeline (COLMAP) using SIFT/SuperPoint features
- **Object recognition**: Find known objects via feature matching
- **Image retrieval**: Bag of Visual Words (BoVW) using descriptor clustering

## References
- Lowe, "Distinctive Image Features from Scale-Invariant Keypoints", IJCV 2004
- Bay, Tuytelaars, Van Gool, "SURF: Speeded Up Robust Features", ECCV 2006
- Rublee, Rabaud, Konolige, Bradski, "ORB: an efficient alternative to SIFT or SURF", ICCV 2011
- Fischler & Bolles, "Random Sample Consensus: A Paradigm for Model Fitting with Applications to Image Analysis and Automated Cartography", Comm. ACM 1981
- DeTone, Malisiewicz, Rabinovich, "SuperPoint: Self-Supervised Interest Point Detection and Description", CVPR Workshop 2018
