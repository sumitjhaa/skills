"""
08.09 Object Detection — anchor-based proposal + IoU in numpy
Usage: python 09-object-detection.py
"""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

def iou(box1, box2):
    """box: [x1, y1, x2, y2]"""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    inter = max(0, x2-x1) * max(0, y2-y1)
    area1 = (box1[2]-box1[0]) * (box1[3]-box1[1])
    area2 = (box2[2]-box2[0]) * (box2[3]-box2[1])
    union = area1 + area2 - inter
    return inter / (union + 1e-10)

def nms(boxes, scores, iou_thresh=0.5):
    """Non-maximum suppression"""
    idxs = scores.argsort()[::-1]
    keep = []
    while len(idxs) > 0:
        i = idxs[0]
        keep.append(i)
        rest = idxs[1:]
        suppress = []
        for j in rest:
            if iou(boxes[i], boxes[j]) > iou_thresh:
                suppress.append(j)
        idxs = np.array([j for j in rest if j not in suppress])
    return keep

# simulate ground truth + proposals
gt = np.array([30, 30, 70, 70])
proposals = np.random.randn(20, 4) * 10 + np.array([50, 50, 50, 50])
proposals = np.clip(proposals, 0, 100).astype(int)
# score each proposal by IoU with GT
scores = np.array([iou(gt, p) for p in proposals])
scores += np.random.randn(20) * 0.05
scores = np.clip(scores, 0, 1)

print(f"GT box: {gt}")
print(f"Proposals: {len(proposals)}")
print(f"Best IoU: {scores.max():.3f}")

kept = nms(proposals, scores, 0.5)
print(f"After NMS: {len(kept)} proposals kept")

fig, ax = plt.subplots(1, 1, figsize=(5, 5))
ax.add_patch(plt.Rectangle((gt[0],gt[1]), gt[2]-gt[0], gt[3]-gt[1],
                           fill=False, edgecolor='g', linewidth=3, label='GT'))
for i, p in enumerate(proposals):
    color = 'r' if scores[i] < 0.3 else 'orange'
    ax.add_patch(plt.Rectangle((p[0],p[1]), p[2]-p[0], p[3]-p[1],
                               fill=False, edgecolor=color, linewidth=0.5))
for i in kept:
    p = proposals[i]
    ax.add_patch(plt.Rectangle((p[0],p[1]), p[2]-p[0], p[3]-p[1],
                               fill=False, edgecolor='b', linewidth=1.5))
ax.set_xlim(0, 100); ax.set_ylim(100, 0)
ax.legend(); ax.set_title(f'Detections (NMS): {len(kept)}')
plt.tight_layout(); plt.savefig('../../assets/phase08/09_object_detection.png', dpi=100)
print("Saved 09_object_detection.png")
