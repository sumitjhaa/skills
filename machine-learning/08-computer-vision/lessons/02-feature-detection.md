# Lesson 08.02: Feature Detection

## Learning Objectives
- Understand Harris corner detector mathematics
- Implement FAST corner detection
- Apply ORB with orientation and scale invariance
- Use SuperPoint for learned feature detection

## Harris Corner Detector

### Second Moment Matrix
$$M = \sum_{x,y} w(x,y) \begin{bmatrix} I_x^2 & I_x I_y \\ I_x I_y & I_y^2 \end{bmatrix}$$

- $I_x, I_y$: image gradients
- $w(x,y)$: Gaussian window

### Corner Response
$$R = \det(M) - \alpha \cdot \text{tr}(M)^2$$

- $\alpha = 0.04-0.06$
- $R > 0$: corner
- $R \approx 0$: flat region
- $R < 0$: edge

### Properties
- Rotation invariant
- Not scale invariant
- Requires threshold tuning

## FAST (Features from Accelerated Segment Test)

### Algorithm
Compare pixel $p$ with 16 pixels on Bresenham circle of radius 3:

1. If $n$ contiguous pixels (typically 9-12) are all brighter than $p + t$ OR all darker than $p - t$, then $p$ is a corner
2. ID3 decision tree for efficient classification
3. Non-maximum suppression to remove adjacent detections

### Performance
- Extremely fast ($\mu$s per detection)
- **Machine learning approach**: Train decision tree on synthetic data
- Not scale or rotation invariant (ORB adds these)

## ORB (Oriented FAST and Rotated BRIEF)

### Orientation (Intensity Centroid)
$$m_{pq} = \sum_{x,y} x^p y^q I(x,y)$$
$$\theta = \text{atan2}(m_{01}, m_{10})$$

- **Centroid**: $C = (m_{10}/m_{00}, m_{01}/m_{00})$
- Orientation = vector from corner to centroid

### rBRIEF Descriptor
Binary descriptor: 256 pairwise intensity comparisons in a $31 \times 31$ patch:

$$\tau(p; x, y) = \begin{cases} 1 & p(x) < p(y) \\ 0 & \text{otherwise} \end{cases}$$

- **Steer BRIEF**: Rotate patch by $\theta$ before computing
- **Variance and correlation**: Learn good bit locations

### Scale Pyramid
Build image pyramid (scale factor $1.2$), detect FAST at each level. Assign level as keypoint scale.

## SuperPoint (Learning-Based)

### Architecture
Fully convolutional encoder-decoder:
1. **Shared encoder**: VGG-style (conv + pooling) $\to$ feature map
2. **Interest point decoder**: $65 \times H/8 \times W/8$ → softmax → reshape
3. **Descriptor decoder**: $256 \times H/8 \times W/8$ → bi-linear interpolation

### Training
- **Synthetic data**: Rendered shapes with known corners
- **Homographic adaptation**: Apply random homographies during training
- **Self-supervised**: Generate pseudo-labels on real images via homographic warping

## Feature Detector Comparison

| Detector | Repeatability | Speed | Scale | Rotation | Learned |
|----------|--------------|-------|-------|----------|---------|
| Harris | Moderate | Fast | No | Yes | No |
| FAST | Moderate | Very fast | No | No | No |
| ORB | Good | Fast | Pyramid | Yes | No |
| SIFT | Excellent | Slow | DoG | Yes | No |
| SuperPoint | Excellent | GPU | Yes (implicit) | Yes | Yes |

## Code: Harris Corner Detection

```python
import numpy as np
from scipy import ndimage

def harris_corners(image, k=0.04, threshold=1e-5):
    I_x = ndimage.sobel(image, axis=1)
    I_y = ndimage.sobel(image, axis=0)
    
    I_xx = ndimage.gaussian_filter(I_x**2, sigma=2)
    I_yy = ndimage.gaussian_filter(I_y**2, sigma=2)
    I_xy = ndimage.gaussian_filter(I_x * I_y, sigma=2)
    
    det = I_xx * I_yy - I_xy**2
    trace = I_xx + I_yy
    R = det - k * trace**2
    
    # Non-maximum suppression
    R_max = ndimage.maximum_filter(R, size=7)
    corners = (R == R_max) & (R > threshold * R.max())
    return np.argwhere(corners)
```

## Applications
- **Image matching**: Feature detection + matching for panorama stitching
- **Visual odometry**: Track features across frames for camera pose
- **AR/VR**: Detect known planar targets for augmentation
- **SfM (Structure from Motion)**: SIFT/SuperPoint for 3D reconstruction

## References
- Harris & Stephens, "A Combined Corner and Edge Detector", 1988
- Rosten & Drummond, "Machine Learning for High-Speed Corner Detection", ECCV 2006
- Rublee, Rabaud, Konolige, Bradski, "ORB: an efficient alternative to SIFT or SURF", ICCV 2011
- DeTone, Malisiewicz, Rabinovich, "SuperPoint: Self-Supervised Interest Point Detection and Description", CVPR Workshop 2018
- Lowe, "Distinctive Image Features from Scale-Invariant Keypoints", IJCV 2004
