# Phase 08 Exercises — Computer Vision

## Exercise 1: Implement Image Convolution

**Theory:** Explain the difference between correlation and convolution. How does zero-padding versus same-padding affect the output spatial dimensions? What is the computational complexity of a 2D convolution with a k×k kernel on an H×W image?

**Coding:** Write a function that performs 2D convolution on a grayscale image with a given kernel (without using `scipy.ndimage.convolve` or similar). Demonstrate it on an 8×8 image with a 3×3 edge-detection kernel.

## Exercise 2: Harris Corner Detector

**Theory:** Derive the second-moment matrix (auto-correlation matrix) for corner detection. Why does the Harris corner response function R = det(M) - k·tr(M)² distinguish corners, edges, and flat regions?

**Coding:** Implement the Harris corner detector step-by-step: compute gradients, second-moment matrix, corner response, and non-maximum suppression. Run on a synthetic image with known corners and report the number of detected corners.

## Exercise 3: SIFT-like Descriptor

**Theory:** Explain why SIFT descriptors are designed to be rotation-invariant and scale-invariant. Why is the descriptor built from gradient histograms rather than raw pixel values?

**Coding:** Implement a simplified SIFT descriptor: compute gradient magnitude and orientation, build a 4×4 grid of 8-bin histograms, and normalise the resulting 128-D vector. Compare two patches by Euclidean distance.

## Exercise 4: Forward Pass of a ConvNet

**Theory:** Explain the receptive field concept in CNNs. How does stacking multiple 3×3 convolutions compare to using a single 7×7 convolution in terms of parameters and effective receptive field?

**Coding:** Implement forward pass of a 2-layer ConvNet (conv → ReLU → pool → conv → ReLU → pool → flattened → FC → softmax) using numpy. Execute on a random 32×32×3 input and show the output shape at each layer.

## Exercise 5: Vision Transformer Patch Embedding

**Theory:** Explain why Vision Transformers split images into patches rather than processing pixels directly. What is the computational complexity of self-attention with patch size P on a H×W image?

**Coding:** Implement the patch embedding layer of a ViT: split a 224×224×3 image into 16×16 patches, linearly project each to 768 dims, add a learnable class token and positional embeddings. Show the resulting tensor shape (1, 197, 768).

## Exercise 6: Non-Maximum Suppression

**Theory:** Explain why NMS is necessary in object detection pipelines. What is the IoU threshold trade-off: too high leads to false positives, too low leads to false negatives?

**Coding:** Implement NMS given a list of bounding boxes (x1, y1, x2, y2) and scores. Use IoU threshold of 0.5. Test with 10 overlapping proposals and show how many survive.

## Exercise 7: Mask IoU Calculation

**Theory:** Define the Intersection-over-Union metric for segmentation. Why is IoU preferred over pixel accuracy when evaluating segmentation models on imbalanced data?

**Coding:** Implement a function that computes the Intersection-over-Union between two binary masks. Generate two overlapping circles of radius 10 at different centres, compute their IoU, and display the masks side by side.

## Exercise 8: Block Matching for Stereo Disparity

**Theory:** Explain the epipolar constraint in stereo vision. Why does block matching search only along the same row (after rectification)? What causes errors in textureless or repetitive regions?

**Coding:** Implement a simple block-matching stereo algorithm: for each pixel in the left image, find the best-matching block in the right image along the same row and return the disparity map. Use a 5×5 block and max disparity of 20. Evaluate on synthetic shifted patterns.

## Exercise 9: PointNet-style Feature Extraction

**Theory:** Explain why PointNet needs a symmetric function (max-pooling) to achieve permutation invariance. What information is lost by global max-pooling, and how do later architectures (PointNet++, Point Transformer) address this?

**Coding:** Implement a permutation-invariant function that processes a set of 3D points: apply an MLP (linear → ReLU → linear) to each point independently, then global max-pool across points. Show that the output is invariant to point order by shuffling rows.

## Exercise 10: Kalman Filter for Object Tracking

**Theory:** Derive the predict and update steps of the Kalman filter. What is the relationship between the Kalman gain and the relative uncertainty of the process vs. measurement noise?

**Coding:** Implement a 2D Kalman filter (state: x, y, vx, vy). Simulate a moving point with noisy observations over 20 time steps. Plot the true trajectory, noisy observations, and filtered estimates.

## Exercise 11: Contrastive (NT-Xent) Loss

**Theory:** Derive the NT-Xent loss and explain its temperature parameter τ. How does a low temperature encourage sharper separation of representations?

**Coding:** Implement the NT-Xent loss used in SimCLR. Given a batch of 4 images with 2 augmentations each (8 embeddings), compute the loss. Verify that identical embeddings yield near-zero loss and random embeddings yield loss ~log(N).

## Exercise 12: FGSM Adversarial Attack

**Theory:** Explain why the Fast Gradient Sign Method is a white-box attack. What is the relationship between the perturbation magnitude ε and the success rate of the attack? How do adversarial training and gradient masking defend against such attacks?

**Coding:** Implement the Fast Gradient Sign Method to attack a simple binary classifier. Given an input image, compute the gradient of the loss w.r.t. the input, add a perturbation of ε=0.3, and show the original and adversarial examples along with their predicted class probabilities.

## Exercise 13: Semantic Segmentation with FCN

**Theory:** Explain how fully convolutional networks replace fully connected layers to produce spatial output maps. What is the role of skip connections in FCN-8s compared to FCN-32s?

**Coding:** Implement a simple FCN with a 3-layer encoder and 3-layer decoder with skip connections. Train on a synthetic 2D segmentation dataset (coloured shapes on a background). Report pixel accuracy and IoU.

## Exercise 14: Depthwise Separable Convolution

**Theory:** Derive the FLOPs reduction from standard convolution to depthwise separable convolution. For a k×k kernel with C_in input and C_out output channels, what is the ratio of parameters?

**Coding:** Implement depthwise separable convolution from scratch using numpy. Verify that the output shape matches a standard Conv2d with the same configuration. Compare runtime for various channel sizes.
