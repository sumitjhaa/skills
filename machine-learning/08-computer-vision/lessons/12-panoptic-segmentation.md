# Lesson 08.12: Panoptic Segmentation

## Learning Objectives
- Understand panoptic segmentation: semantic + instance unified
- Implement Panoptic FPN combining Mask R-CNN + semantic head
- Apply mask transformer architectures (Panoptic SegFormer, Mask2Former)
- Evaluate using Panoptic Quality (PQ) metric

## Task Definition
Assign to each pixel $(i,j)$:
- **Semantic label**: $l_{ij} \in \{1, \dots, L\}$
- **Instance ID**: $z_{ij} \in \{0, 1, \dots\}$ (0 for stuff)

### Stuff vs Things
| Category | Examples | Instance ID |
|----------|----------|-------------|
| Things | People, cars, animals | Unique per object |
| Stuff | Sky, road, grass, wall | 0 (all same) |

## Panoptic FPN

### Architecture
```
Image → Backbone → FPN → [Mask R-CNN head (things) + Semantic FPN head (stuff)]
→ Fusion → Panoptic output
```

### Fusion Algorithm
```
For each pixel:
  if Mask R-CNN confidence > threshold:
    assign thing class + instance ID
  else:
    assign stuff class from semantic head
Resolve overlaps: stuff regions take priority for unconfident things
```

## Panoptic SegFormer

### Mask Transformer
Query-based architecture:
1. **Transformer decoder**: Learns $N$ queries predicting binary masks + class probabilities
2. **Mask prediction**: Each query outputs attention map over image features
3. **Class prediction**: Softmax over $C+1$ classes (1 for "no object")

### Overlap Resolution
- Masks can overlap (multiple queries activate same region)
- Heuristic: Assign pixel to query with highest confidence score
- OR: Learn mask-wise non-overlap constraint

## Mask2Former

### Masked Attention
$$\text{MaskedAttention}(Q, K, V) = \text{softmax}(\log M + QK^\top / \sqrt{d}) V$$

- $M$: predicted mask from previous decoder layer
- Zero attention to regions outside predicted mask
- **Advantage**: Each query focuses on its own region (no interference)

### Architecture
```
Image → Backbone → Pixel decoder → Transformer decoder (with masked attention) → per-pixel + per-query classification
```

### Unified Architecture
Single architecture for semantic, instance, and panoptic segmentation:
- Semantic: Each query predicts class + mask; merge all masks
- Instance: Each query = one instance
- Panoptic: Combine (things = instance, stuff = merge semantic queries)

## Code: Panoptic Fusion

```python
import torch
import torch.nn.functional as F

def panoptic_fusion(mask_rcnn_outputs, semantic_outputs, num_things=80, 
                    thing_score_thresh=0.5):
    """Simple panoptic fusion logic"""
    B, H, W = semantic_outputs.shape
    panoptic = torch.zeros(B, H, W, dtype=torch.long)
    next_id = 1
    
    for b in range(B):
        # Process things (instance) first
        thing_masks = mask_rcnn_outputs[b]['masks']  # (N, H, W)
        thing_scores = mask_rcnn_outputs[b]['scores']
        thing_classes = mask_rcnn_outputs[b]['labels']
        
        for i in range(len(thing_scores)):
            if thing_scores[i] > thing_score_thresh:
                cls_id = thing_classes[i]  # 0..num_things-1
                mask = thing_masks[i] > 0.5
                # Assign unique instance ID
                panoptic[b][mask] = cls_id * 1000 + next_id
                next_id += 1
        
        # Fill stuff regions (semantic)
        stuff_mask = (panoptic[b] == 0)
        panoptic[b][stuff_mask] = semantic_outputs[b][stuff_mask] + num_things * 1000
    
    return panoptic
```

## Metrics

### Panoptic Quality (PQ)
$$\text{PQ} = \frac{\sum_{(p,g) \in TP} \text{IoU}(p,g)}{|TP| + \frac{1}{2}|FP| + \frac{1}{2}|FN|}$$

- **Segmentation Quality (SQ)**: $\frac{\sum_{(p,g)} \text{IoU}(p,g)}{|TP|}$ — mask quality
- **Recognition Quality (RQ)**: $\frac{|TP|}{|TP| + \frac{1}{2}|FP| + \frac{1}{2}|FN|}$ — detection quality
- $\text{PQ} = \text{SQ} \times \text{RQ}$

### Matching
- Predicted segment matched to GT segment if IoU > 0.5
- One-to-one matching (greedy)

## Panoptic Segmentation Results

| Method | Backbone | PQ | PQ_Th | PQ_St |
|--------|----------|-----|-------|-------|
| Panoptic FPN | ResNet-50 | 40.9 | 46.9 | 34.8 |
| Panoptic-DeepLab | ResNet-50 | 41.4 | 45.1 | 37.5 |
| Panoptic SegFormer | Swin-B | 50.0 | 56.6 | 43.3 |
| Mask2Former | Swin-B | 51.9 | 58.2 | 45.5 |
| Mask2Former | Swin-L | 57.8 | 65.5 | 50.0 |

## Practical Considerations
- **Threshold tuning**: Thing score threshold balances precision/recall for things
- **Overlapping instances**: Mask transformer may assign overlapping masks — resolve via NMS or learned merging
- **Class balancing**: Stuff is typically easier (texture-based) than things (shape-based)
- **Efficient inference**: Mask2Former uses masked attention for faster convergence and decoding

## References
- Kirillov, He, Girshick, Rother, Dollar, "Panoptic Segmentation", CVPR 2019
- Kirillov, Girshick, He, Dollar, "Panoptic Feature Pyramid Networks", CVPR 2019
- Li, Xu, et al., "Panoptic SegFormer", CVPR 2022
- Cheng, Schwing, Kirillov, "Per-Pixel Classification is Not All You Need for Semantic Segmentation (MaskFormer)", NeurIPS 2021
- Cheng, Misra, Schwing, Kirillov, Girdhar, "Masked-attention Mask Transformer for Universal Image Segmentation (Mask2Former)", CVPR 2022
