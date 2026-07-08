# 08.21 Video Understanding

## Learning Objectives
- Understand 3D CNNs for spatio-temporal feature learning
- Implement two-stream and SlowFast architectures
- Apply VideoMAE for self-supervised video representation
- Evaluate on action recognition benchmarks (Kinetics, UCF101)

## Video Classification

### 3D CNNs
Extend 2D convolution to 3D (spatio-temporal):

$$(f * g)(x,y,t) = \sum_{i=-k}^{k} \sum_{j=-k}^{k} \sum_{l=-k}^{k} f(i,j,l) \cdot g(x+i, y+j, t+l)$$

**C3D**: 3D Conv → 3D Pool → ... → FC → class. 3×3×3 kernels. ~2× parameters of 2D Conv.

### I3D (Inflated 3D)
Inflate 2D ConvNet (Inception) to 3D: $3\times3$ kernels become $3\times3\times3$. Bootstraps from ImageNet pretrained weights (inflated + averaged).

## Two-Stream Networks

### Spatial Stream
Single RGB frame → 2D ConvNet → spatial features

### Temporal Stream
Optical flow (stack of 10 consecutive flow fields) → 2D ConvNet → motion features

### Fusion
Late fusion (average softmax scores) or early fusion (concatenate features before classifier).

## TSN (Temporal Segment Networks)

### Sparse Sampling
Divide video into $K$ segments, sample 1 frame/segment:

$$F(T_1, \dots, T_K) = H(G(\text{CNN}(T_1), \dots, \text{CNN}(T_K)))$$

- $G$: consensus function (max, avg, attention)
- $H$: classifier

### Advantage
Processes 8-16 frames (not all 100+), enabling longer temporal coverage.

## SlowFast

### Architecture
Two parallel pathways with different frame rates:

| Pathway | Frame Rate | Channels | Temporal Stride |
|---------|-----------|----------|----------------|
| Slow | $\tau$ | $C$ | 16 |
| Fast | $\tau/\alpha$ | $C/\beta$ ($\beta=8$) | 2 |

### Lateral Connections
Fast pathway features fused into slow pathway via convolution:

$$F_{\text{slow}} = F_{\text{slow}} + \text{Conv}_{1\times1\times1}(\text{Downsample}(F_{\text{fast}}))$$

## VideoMAE

### Tube Masking
Mask entire spatio-temporal tubes (not random patches):

$$M_{t,h,w} = \begin{cases} 0 & \text{if in tube} \\ 1 & \text{otherwise} \end{cases}$$

### Encoder-Decoder
- **Encoder**: Only visible tubes (75% masked)
- **Decoder**: All tubes (visible + mask tokens), reconstruct pixel values

### Pretraining Data Efficiency
VideoMAE achieves strong results with 10% Kinetics-400 pretraining data.

## Temporal Action Localisation

### Boundary-Matching Network
1. Generate temporal proposals (start, end, confidence)
2. Refine boundaries with regression
3. Score each proposal for action class

### ActionFormer
Transformer encoder over temporal features. Each position predicts action probability + boundary offsets.

## Code: VideoMAE Tube Masking

```python
import torch

def tube_mask(x, mask_ratio=0.75, tube_size=2):
    """x: (B, T, H, W, C)"""
    B, T, H, W, C = x.shape
    num_patches = T * H * W
    num_masked = int(num_patches * mask_ratio)
    
    # Group patches into tubes (temporal blocks)
    T_tubes = T // tube_size
    num_tubes = T_tubes * H * W
    tube_patches = x.reshape(B, T_tubes, tube_size, H, W, C)
    
    # Mask entire tubes
    noise = torch.rand(B, num_tubes, device=x.device)
    ids_shuffle = torch.argsort(noise, dim=1)
    ids_keep = ids_shuffle[:, :num_tubes - num_masked // tube_size]
    
    mask = torch.zeros(B, num_tubes, device=x.device)
    mask.scatter_(1, ids_keep, 1)
    mask = mask.reshape(B, T_tubes, 1, H, W).expand(-1, -1, tube_size, -1, -1)
    return mask.reshape(B, T, H, W)
```

## Dataset Benchmarks

| Dataset | Classes | Videos | Task | SOTA |
|---------|---------|--------|------|------|
| Kinetics-400 | 400 | 300K | Action recognition | 88.9% (VideoMAE) |
| Kinetics-700 | 700 | 650K | Action recognition | 80.8% (SlowFast) |
| UCF101 | 101 | 13K | Action recognition | 98.5% (I3D) |
| ActivityNet | 200 | 28K | Temporal localisation | 36.1% mAP (ActionFormer) |
| AVA | 80 | 430 | Spatio-temporal detection | 40.0% mAP (SlowFast) |

## Practical Considerations
- **Frames vs clips**: Train on short clips (< 64 frames), test with dense sampling
- **Optical flow**: Precomputed flow is expensive; use motion vectors or RGB difference
- **Temporal resolution**: Higher FPS benefits motion-heavy actions
- **Memory**: 3D Conv uses 5× memory of 2D; use gradient checkpointing

## References
- Tran, Bourdev, Fergus, Torresani, Paluri, "C3D: Generic Features for Video Analysis", 2014
- Carreira & Zisserman, "Quo Vadis, Action Recognition? A New Model and the Kinetics Dataset", CVPR 2017
- Wang, Xiong, Wang, Qiao, Lin, Tang, Van Gool, "Temporal Segment Networks: Towards Good Practices for Deep Action Recognition", ECCV 2016
- Feichtenhofer, Fan, Malik, He, "SlowFast Networks for Video Recognition", ICCV 2019
- Tong, Song, Wang, Wang, "VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training", NeurIPS 2022
