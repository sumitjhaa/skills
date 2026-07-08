"""08.20 Multi-object tracking: SORT, DeepSORT, MOT."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment
from scipy.spatial.distance import cdist

np.random.seed(42)

n_frames = 30
n_objects = 3
img_size = 200

true_tracks = {}
for obj_id in range(n_objects):
    cx, cy = np.random.randint(20, 180, 2)
    vx = np.random.uniform(-2, 2)
    vy = np.random.uniform(-2, 2)
    positions = [(cx, cy)]
    for f in range(1, n_frames):
        cx += vx + np.random.randn() * 1.5
        cy += vy + np.random.randn() * 1.5
        positions.append((cx, cy))
    true_tracks[obj_id] = np.array(positions)

detections = {}
for f in range(n_frames):
    dets = []
    for obj_id in range(n_objects):
        pos = true_tracks[obj_id][f]
        dets.append([pos[0] + np.random.randn() * 3,
                     pos[1] + np.random.randn() * 3,
                     np.random.uniform(0.7, 1.0)])
    detections[f] = np.array(dets)

def iou_2d(box1, box2):
    x1, y1, x2, y2 = box1
    x1p, y1p, x2p, y2p = box2
    xi1, yi1 = max(x1, x1p), max(y1, y1p)
    xi2, yi2 = min(x2, x2p), min(y2, y2p)
    inter = max(0, xi2 - xi1) * max(0, yi2 - yi1)
    area1 = (x2 - x1) * (y2 - y1)
    area2 = (x2p - x1p) * (y2p - y1p)
    return inter / (area1 + area2 - inter + 1e-10)

def kalman_predict(x, P, dt=1.0, motion_noise=1.0):
    F = np.array([[1, 0, dt, 0], [0, 1, 0, dt],
                  [0, 0, 1, 0], [0, 0, 0, 1]])
    Q = motion_noise * np.eye(4)
    x_pred = F @ x
    P_pred = F @ P @ F.T + Q
    return x_pred, P_pred

def kalman_update(x_pred, P_pred, z, measurement_noise=3.0):
    H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])
    R = measurement_noise * np.eye(2)
    y = z - H @ x_pred
    S = H @ P_pred @ H.T + R
    K = P_pred @ H.T @ np.linalg.inv(S)
    x_upd = x_pred + K @ y
    P_upd = (np.eye(4) - K @ H) @ P_pred
    return x_upd, P_upd

tracks = {}
track_states = {}
next_id = 0

for f in range(n_frames):
    dets = detections[f]
    if len(tracks) == 0:
        for d in dets:
            tracks[next_id] = np.array([d[0], d[1], 0, 0])
            track_states[next_id] = {"P": 10 * np.eye(4), "age": 0, "hits": 1, "misses": 0}
            next_id += 1
    else:
        track_ids = list(tracks.keys())
        track_pos = np.array([tracks[tid][:2] for tid in track_ids])
        det_pos = dets[:, :2]
        cost = cdist(track_pos, det_pos)
        row_idx, col_idx = linear_sum_assignment(cost)
        for t, d in zip(row_idx, col_idx):
            tid = track_ids[t]
            tracks[tid][:2] = dets[d, :2]
            track_states[tid]["age"] += 1
            track_states[tid]["hits"] += 1
            track_states[tid]["misses"] = 0
        unmatched_dets = set(range(len(dets))) - set(col_idx)
        for d in unmatched_dets:
            tracks[next_id] = np.array([dets[d, 0], dets[d, 1], 0, 0])
            track_states[next_id] = {"P": 10 * np.eye(4), "age": 0, "hits": 1, "misses": 0}
            next_id += 1

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

colors = plt.cm.tab10(np.linspace(0, 1, n_objects))
for obj_id in range(n_objects):
    pos = true_tracks[obj_id]
    axes[0, 0].plot(pos[:, 0], pos[:, 1], "o-", color=colors[obj_id], lw=2,
                   label=f"GT Track {obj_id}")
axes[0, 0].set_xlabel("x"); axes[0, 0].set_ylabel("y")
axes[0, 0].set_title("Ground Truth Trajectories")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].axis("equal")

for f in range(0, n_frames, 5):
    dets = detections[f]
    axes[0, 1].scatter(dets[:, 0], dets[:, 1], s=30, alpha=0.5,
                      c=range(len(dets)), cmap="Set1")
axes[0, 1].set_xlabel("x"); axes[0, 1].set_ylabel("y")
axes[0, 1].set_title(f"Detections Over Time\n({n_frames} frames)")
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].axis("equal")

max_track_id = max(tracks.keys()) + 1 if tracks else 0
axes[0, 2].bar(["Total tracks", "Active tracks"],
               [max_track_id, len(tracks)], alpha=0.7)
axes[0, 2].set_ylabel("Count")
axes[0, 2].set_title("Track Management")
axes[0, 2].grid(True, axis="y", alpha=0.3)

confidences = [dets[:, 2] for f, dets in detections.items()]
all_confs = np.concatenate(confidences)
axes[1, 0].hist(all_confs, bins=20, alpha=0.7)
axes[1, 0].axvline(0.5, color="r", ls="--", label="Threshold")
axes[1, 0].set_xlabel("Detection confidence")
axes[1, 0].set_ylabel("Count")
axes[1, 0].set_title("Detection Confidence Distribution")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

track_lengths = [track_states[tid]["hits"] for tid in tracks]
axes[1, 1].hist(track_lengths, bins=range(1, n_frames+2), alpha=0.7)
axes[1, 1].set_xlabel("Track length (frames)")
axes[1, 1].set_ylabel("Count")
axes[1, 1].set_title("Track Length Distribution")
axes[1, 1].grid(True, alpha=0.3)

n_dets_per_frame = [len(detections[f]) for f in range(n_frames)]
axes[1, 2].plot(range(n_frames), n_dets_per_frame, "o-", lw=2)
axes[1, 2].axhline(n_objects, color="r", ls="--", label=f"True objects ({n_objects})")
axes[1, 2].set_xlabel("Frame")
axes[1, 2].set_ylabel("Detections")
axes[1, 2].set_title("Detections per Frame\n(vs ground truth)")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/20-multi-object-tracking.png")
plt.close()

print("=" * 60)
print("MULTI-OBJECT TRACKING")
print("=" * 60)
print(f"\nSequence: {n_frames} frames, {n_objects} objects")
print(f"  Total detections: {sum(len(d) for d in detections.values())}")
print(f"  Tracks created: {max_track_id}")
print(f"  Active tracks at end: {len(tracks)}")

print(f"\nTrack stats:")
for tid in list(tracks.keys())[:n_objects]:
    state = track_states[tid]
    print(f"  Track {tid}: hits={state['hits']}, misses={state['misses']}, "
          f"age={state['age']}")

print(f"\nMOT Pipeline:")
print(f"  Detection → Kalman Filter → Data Association")
print(f"  • SORT: IoU + Kalman (simple, fast)")
print(f"  • DeepSORT: appearance features (ReID)")
print(f"  • ByteTrack: BYTE association (low-score detections)")
print(f"\nMetrics:")
print(f"  • MOTA: Multiple Object Tracking Accuracy")
print(f"  • IDF1: Identity F1 score")
print(f"  • HOTA: Higher Order Tracking Accuracy")
