# Lesson 08.20: Multi-Object Tracking

## Learning Objectives
- Understand tracking-by-detection paradigm
- Implement Deep SORT with Kalman filter + appearance features
- Apply FairMOT for joint detection and re-ID
- Evaluate with MOTA, IDF1, and HOTA metrics

## Tracking-by-Detection

### Pipeline
```
Video frames → Object detector → Association → Track management → Tracked objects
```

### Association
- **Hungarian algorithm**: Solve assignment between detections and tracks
- Cost matrix: IoU distance + appearance feature distance
- **Gated**: Only accept assignment if cost < threshold

### Track Management
- **Birth**: New track initialized for unassigned detections
- **Death**: Track terminated if unmatched for $T_{\text{lost}}$ frames
- **Confirmed vs tentative**: Track needs $N$ matches before output

## Deep SORT

### Kalman Filter
State: $\mathbf{x} = [cx, cy, r, h, \dot{cx}, \dot{cy}, \dot{r}, \dot{h}]$

- $cx, cy$: center coordinates
- $r$: aspect ratio
- $h$: height
- Velocities: $\dot{cx}, \dot{cy}, \dot{r}, \dot{h}$

**Prediction**: $\mathbf{x}_t = F \mathbf{x}_{t-1}$
**Update**: $\mathbf{x}_t = \mathbf{x}_t + K_t(z_t - H\mathbf{x}_t)$

### Appearance Feature
- **Re-ID network**: Wide ResNet trained on person re-ID datasets
- **Feature bank**: Store last $N$ frame features for each track
- **Cosine distance**: $d_{\text{app}}(i, j) = 1 - \text{cosine}(f_i, f_j)$

### Cascade Matching
Priority to tracks matched most recently:
```
for track in sort_by_last_update_time(ascending):
    matched = hungarian_match(track, unmatched_detections, max_age=30)
```

### Matching Cost
$$c_{ij} = \lambda \cdot d_{\text{app}}(i, j) + (1-\lambda) \cdot d_{\text{IoU}}(i, j)$$

## FairMOT

### Joint Detection + Re-ID
Single network with two heads:

```
Encoder (DLA-34) → [Detection head (for boxes) + Re-ID head (for features)]
```

### Center-Based Detection
- **Heatmap**: Predict object center (Gaussian)
- **Box size**: Predict width and height
- **Offset**: Sub-pixel center offset

### Re-ID Features
- Per-pixel re-ID features
- Only train re-ID at object center locations

### Loss
$$\mathcal{L} = \mathcal{L}_{\text{det}} + \lambda \mathcal{L}_{\text{id}}$$

- $\mathcal{L}_{\text{det}}$: Focal loss (heatmap) + L1 (box)
- $\mathcal{L}_{\text{id}}$: Cross-entropy (re-ID classification)

## Code: Simple Tracking Association

```python
import numpy as np
from scipy.optimize import linear_sum_assignment

class Track:
    def __init__(self, detection, track_id, feature):
        self.track_id = track_id
        self.bbox = detection  # [x1, y1, x2, y2]
        self.features = [feature]
        self.hits = 1
        self.time_since_update = 0

def associate_detections(detections, tracks, iou_threshold=0.3):
    if len(tracks) == 0:
        return [], list(range(len(detections))), []
    
    # IoU cost matrix
    cost_matrix = np.zeros((len(tracks), len(detections)))
    for i, track in enumerate(tracks):
        for j, det in enumerate(detections):
            cost_matrix[i, j] = 1 - compute_iou(track.bbox, det['bbox'])
    
    # Hungarian assignment
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    matched = []
    unmatched_det = list(range(len(detections)))
    unmatched_trk = list(range(len(tracks)))
    
    for i, j in zip(row_ind, col_ind):
        if cost_matrix[i, j] < 1 - iou_threshold:
            matched.append((i, j))
            unmatched_trk.remove(i)
            unmatched_det.remove(j)
    
    return matched, unmatched_det, unmatched_trk
```

## Evaluation Metrics

| Metric | Formula | Focus |
|--------|---------|-------|
| MOTA | $1 - \frac{FP + FN + IDSW}{GT}$ | Detection + association |
| IDF1 | $\frac{2 \cdot \text{IDTP}}{2 \cdot \text{IDTP} + \text{IDFP} + \text{IDFN}}$ | Identity preservation |
| HOTA | $\sqrt{\frac{\sum \text{TP} \cdot \text{Assoc}}{|TP| + |FN| + |FP|}}$ | Higher-order tracking |

### MOTA Limitations
- Biased toward detection quality
- ID switches weighted equally regardless of length

## Online vs Batch Tracking

| Type | Description | Example | Use Case |
|------|-------------|---------|----------|
| Online | Process frame by frame | Deep SORT, FairMOT | Real-time |
| Batch (offline) | Process entire video | MOTR, TrackFormer | Post-processing |
| Near-online | Small temporal window | QDTrack | Balanced |

## Practical Considerations
- **Re-ID feature quality**: Critical for identity preservation; train on diverse data
- **NMS threshold**: 0.4-0.5 for detection; lower = fewer but more confident detections
- **Kalman filter**: Assumes constant velocity; fails on sudden direction changes
- **Occlusion handling**: Use motion prediction for occluded frames
- **Track fragmentation**: Caused by missed detections; lower detection threshold helps

## References
- Bewley, Ge, Ott, Ramos, Upcroft, "Simple Online and Realtime Tracking (SORT)", ICIP 2016
- Wojke, Bewley, Paulus, "Simple Online and Realtime Tracking with a Deep Association Metric (Deep SORT)", ICIP 2017
- Zhang, Wang, et al., "FairMOT: On the Fairness of Detection and Re-Identification in Multiple Object Tracking", IJCV 2021
- Sun, Jiang, et al., "TransTrack: Multiple Object Tracking with Transformer", 2020
- Luiten, Osep, et al., "HOTA: A Higher Order Metric for Evaluating Multi-Object Tracking", IJCV 2021
