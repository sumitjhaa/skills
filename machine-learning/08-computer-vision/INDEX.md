# Phase 08 — Computer Vision

## 1. Phase Overview

| Field | Value |
|---|---|
| **Phase** | 08 — Computer Vision |
| **Lessons** | 31 |
| **Core topics** | Image processing, feature detection/descriptors, CNN backbones (classic, efficient, modern), vision transformers, self-supervised vision, object detection, instance/semantic/panoptic segmentation, depth estimation, human pose, 3D pose/shape, neural face models, neural rendering, point clouds, 3D object detection, multi-object tracking, video understanding, video generation, image-to-image, super-resolution, medical imaging, VQA/captioning, open-vocabulary, robustness, visual RL, multimodal generation, CV system |

## 2. Prerequisites

- **Prior phases:** [Phase 01](../01-linear-algebra/INDEX.md) (convolutions as linear ops, SVD for compression), [Phase 02](../02-calculus-optimization/INDEX.md) (gradient-based training), [Phase 06](../06-deep-learning/INDEX.md) (CNN backbones, transformers, augmentations, training pipeline)
- **Python frameworks:** [`../../python-frameworks/pytorch/`](../../python-frameworks/pytorch/) (reference), [`../../python-frameworks/numpy-pandas/`](../../python-frameworks/numpy-pandas/) (image preprocessing)

## 3. Lesson Table

| # | Title | What You'll Learn | Lesson | Code | Cross-References |
|---|---|---|---|---|---|
| 01 | Image Processing | Filtering, convolution, edges, morphology | [lesson](lessons/01-image-processing.md) | [code](code/01-image-processing.py) | Used in: Phase 04 (Fourier/wavelet) |
| 02 | Feature Detection | Harris, SIFT, SURF, FAST, ORB | [lesson](lessons/02-feature-detection.md) | [code](code/02-feature-detection.py) | Used in: Phase 11 (feature engineering) |
| 03 | Feature Descriptors | HOG, BRIEF, BRISK, LBP | [lesson](lessons/03-feature-descriptors.md) | [code](code/03-feature-descriptors.py) | Used in: Phase 05 (classical features) |
| 04 | CNN Backbones | AlexNet, VGG, ResNet, DenseNet | [lesson](lessons/04-cnn-backbones.md) | [code](code/04-cnn-backbones.py) | Used in: Phase 06 (CNN backbones) |
| 05 | Efficient Backbones | MobileNet, ShuffleNet, EfficientNet | [lesson](lessons/05-efficient-backbones.md) | [code](code/05-efficient-backbones.py) | Used in: Phase 11 (deployment) |
| 06 | Modern Backbones | ConvNeXt, ResNeXt, RegNet | [lesson](lessons/06-modern-backbones.md) | [code](code/06-modern-backbones.py) | Used in: Phase 12 (SOTA repro) |
| 07 | Vision Transformers | ViT, DeiT, Swin, cross-attention | [lesson](lessons/07-vision-transformers.md) | [code](code/07-vision-transformers.py) | Used in: Phase 06 (transformers) |
| 08 | Self-Supervised Vision | MAE, SimCLR, MoCo, DINO | [lesson](lessons/08-self-supervised-vision.md) | [code](code/08-self-supervised-vision.py) | Used in: Phase 07 (contrastive learning) |
| 09 | Object Detection | R-CNN, YOLO, SSD, DETR | [lesson](lessons/09-object-detection.md) | [code](code/09-object-detection.py) | Used in: Phase 09 (multi-modal) |
| 10 | Instance Segmentation | Mask R-CNN, SOLO, YOLACT | [lesson](lessons/10-instance-segmentation.md) | [code](code/10-instance-segmentation.py) | Used in: Phase 12 (medical imaging) |
| 11 | Semantic Segmentation | FCN, U-Net, DeepLab, SegFormer | [lesson](lessons/11-semantic-segmentation.md) | [code](code/11-semantic-segmentation.py) | Used in: Phase 09 (medical) |
| 12 | Panoptic Segmentation | Panoptic FPN, UPSNet | [lesson](lessons/12-panoptic-segmentation.md) | [code](code/12-panoptic-segmentation.py) | Used in: Phase 11 (autonomous driving) |
| 13 | Depth Estimation | Monocular, stereo, MiDaS | [lesson](lessons/13-depth-estimation.md) | [code](code/13-depth-estimation.py) | Used in: Phase 10 (robotics) |
| 14 | Human Pose | Keypoint detection, OpenPose | [lesson](lessons/14-human-pose.md) | [code](code/14-human-pose.py) | Used in: Phase 10 (imitation) |
| 15 | 3D Pose & Shape | SMPL, HMR, body models | [lesson](lessons/15-3d-pose-shape.md) | [code](code/15-3d-pose-shape.py) | Used in: Phase 04 (Lie groups) |
| 16 | Neural Face Models | Face reenactment, 3DMM, NeRF | [lesson](lessons/16-neural-face-models.md) | [code](code/16-neural-face-models.py) | Used in: Phase 07 (implicit neural) |
| 17 | Neural Rendering | NeRF, Gaussian splatting, radiance fields | [lesson](lessons/17-neural-rendering.md) | [code](code/17-neural-rendering.py) | Used in: Phase 07 (implicit neural) |
| 18 | Point Cloud | PointNet, PointNet++, PointMLP | [lesson](lessons/18-point-cloud.md) | [code](code/18-point-cloud.py) | Used in: Phase 07 (set functions) |
| 19 | 3D Object Detection | VoxelNet, PointPillars, F-PointNet | [lesson](lessons/19-3d-object-detection.md) | [code](code/19-3d-object-detection.py) | Used in: Phase 11 (autonomous driving) |
| 20 | Multi-Object Tracking | SORT, DeepSORT, MOT algorithms | [lesson](lessons/20-multi-object-tracking.md) | [code](code/20-multi-object-tracking.py) | Used in: Phase 10 (multi-agent) |
| 21 | Video Understanding | I3D, SlowFast, timesformer | [lesson](lessons/21-video-understanding.md) | [code](code/21-video-understanding.py) | Used in: Phase 09 (video LLMs) |
| 22 | Video Generation | Video diffusion, CogVideo, AnimateDiff | [lesson](lessons/22-video-generation.md) | [code](code/22-video-generation.py) | Used in: Phase 07 (diffusion) |
| 23 | Image-to-Image | Pix2Pix, CycleGAN, conditional diffusion | [lesson](lessons/23-image-to-image.md) | [code](code/23-image-to-image.py) | Used in: Phase 07 (GANs) |
| 24 | Super-Resolution | SRCNN, ESRGAN, SwinIR | [lesson](lessons/24-super-resolution.md) | [code](code/24-super-resolution.py) | Used in: Phase 07 (diffusion) |
| 25 | Medical Imaging | CT, MRI, segmentation, detection | [lesson](lessons/25-medical-imaging.md) | [code](code/25-medical-imaging.py) | Used in: Phase 12 (ML for science) |
| 26 | VQA & Captioning | Visual question answering, image captioning | [lesson](lessons/26-vqa-captioning.md) | [code](code/26-vqa-captioning.py) | Used in: Phase 09 (multimodal LLMs) |
| 27 | Open-Vocabulary | CLIP, GLIP, open-vocab detection | [lesson](lessons/27-open-vocabulary.md) | [code](code/27-open-vocabulary.py) | Used in: Phase 07 (contrastive) |
| 28 | Robustness | Adversarial examples, corruption, OOD | [lesson](lessons/28-robustness.md) | [code](code/28-robustness.py) | Used in: Phase 11 (model robustness) |
| 29 | Visual RL | RL with visual input, DQN, Dreamer | [lesson](lessons/29-visual-rl.md) | [code](code/29-visual-rl.py) | Used in: Phase 10 (deep RL) |
| 30 | Multimodal Generation | Text-to-image, text-to-video, DALL·E | [lesson](lessons/30-multimodal-generation.md) | [code](code/30-multimodal-generation.py) | Used in: Phase 09 (multimodal) |
| 31 | CV System | Full computer vision system design | [lesson](lessons/31-cv-system.md) | [code](code/31-cv-system.py) | Used in: Phase 11 (system design) |

## 4. Builds Toward

- **Phase 09** (multimodal models, video understanding, VQA/captioning)
- **Phase 10** (visual RL, robotics perception)
- **Phase 11** (model deployment, monitoring for vision systems)
- **Phase 12** (SOTA reproduction, novel contribution)

## 5. Quick Start

```bash
python3 code/01-image-processing.py
```
