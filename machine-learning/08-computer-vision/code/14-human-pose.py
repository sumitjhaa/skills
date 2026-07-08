"""08.14 Human pose estimation: top-down, bottom-up."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

n_joints = 17
skeleton = [(0, 1), (0, 2), (1, 3), (2, 4), (5, 6), (5, 7), (7, 9),
            (6, 8), (8, 10), (5, 11), (6, 12), (11, 13), (13, 15),
            (12, 14), (14, 16)]
joint_names = ["nose", "Leye", "Reye", "Lear", "Rear", "Lsho", "Rsho",
               "Lelb", "Relb", "Lwri", "Rwri", "Lhip", "Rhip",
               "Lkne", "Rkne", "Lank", "Rank"]

img_size = 200
true_pose = np.array([
    [100, 30], [85, 25], [115, 25], [75, 30], [125, 30],
    [70, 70], [130, 70], [55, 100], [145, 100], [40, 130], [160, 130],
    [75, 120], [125, 120], [70, 160], [130, 160], [65, 190], [135, 190]
], dtype=float)

pred_pose = true_pose + np.random.randn(n_joints, 2) * 5
pred_conf = np.random.uniform(0.6, 1.0, n_joints)

heatmap = np.zeros((img_size, img_size))
for j in range(n_joints):
    yy, xx = np.ogrid[:img_size, :img_size]
    heatmap += pred_conf[j] * np.exp(-((xx - pred_pose[j, 0])**2 +
                                       (yy - pred_pose[j, 1])**2) / (2 * 5**2))

pck_dist = np.linalg.norm(true_pose - pred_pose, axis=1)
pck_thresh = 10
pck = np.mean(pck_dist < pck_thresh)

oks_sigmas = np.array([0.026, 0.025, 0.025, 0.035, 0.035,
                      0.079, 0.079, 0.072, 0.072, 0.062, 0.062,
                      0.107, 0.107, 0.087, 0.087, 0.089, 0.089])
oks = np.exp(-pck_dist**2 / (2 * (oks_sigmas * img_size)**2))

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

bg = np.random.rand(img_size, img_size) * 0.3
axes[0, 0].imshow(bg, cmap="gray")
for (i, j) in skeleton:
    axes[0, 0].plot([true_pose[i, 0], true_pose[j, 0]],
                   [true_pose[i, 1], true_pose[j, 1]], "b-", lw=2, alpha=0.7)
axes[0, 0].scatter(true_pose[:, 0], true_pose[:, 1], c="blue", s=50, zorder=5)
axes[0, 0].set_title("Ground Truth Pose\n(17 keypoints)")
axes[0, 0].axis("off")

axes[0, 1].imshow(bg, cmap="gray")
for (i, j) in skeleton:
    if pred_conf[i] > 0.5 and pred_conf[j] > 0.5:
        axes[0, 1].plot([pred_pose[i, 0], pred_pose[j, 0]],
                       [pred_pose[i, 1], pred_pose[j, 1]], "r-", lw=2, alpha=0.7)
sc = axes[0, 1].scatter(pred_pose[:, 0], pred_pose[:, 1], c=pred_conf,
                        s=50, cmap="RdYlGn", vmin=0, vmax=1, zorder=5)
axes[0, 1].set_title(f"Predicted Pose\nPCK@{pck_thresh}={pck:.3f}")
axes[0, 1].axis("off")
plt.colorbar(sc, ax=axes[0, 1])

axes[0, 2].imshow(heatmap, cmap="hot")
axes[0, 2].scatter(true_pose[:, 0], true_pose[:, 1], c="cyan", s=20, alpha=0.7)
axes[0, 2].set_title("Heatmap Prediction")
axes[0, 2].axis("off")
plt.colorbar(axes[0, 2].images[0], ax=axes[0, 2])

axes[1, 0].bar(range(n_joints), pck_dist, color="steelblue", alpha=0.7)
axes[1, 0].axhline(pck_thresh, color="r", ls="--", label=f"Threshold={pck_thresh}")
axes[1, 0].set_xlabel("Joint index")
axes[1, 0].set_xticks(range(n_joints))
axes[1, 0].set_xticklabels(joint_names, rotation=45, fontsize=7)
axes[1, 0].set_ylabel("PCK distance (px)")
axes[1, 0].set_title(f"Per-Joint PCK Error\nPCK={pck:.3f}")
axes[1, 0].legend()
axes[1, 0].grid(True, axis="y", alpha=0.3)

axes[1, 1].bar(range(n_joints), oks, color="coral", alpha=0.7)
axes[1, 1].axhline(np.mean(oks), color="k", ls="--", label=f"mOKS={np.mean(oks):.3f}")
axes[1, 1].set_xlabel("Joint index")
axes[1, 1].set_xticks(range(n_joints))
axes[1, 1].set_xticklabels(joint_names, rotation=45, fontsize=7)
axes[1, 1].set_ylabel("OKS")
axes[1, 1].set_title("Object Keypoint Similarity")
axes[1, 1].legend()
axes[1, 1].grid(True, axis="y", alpha=0.3)

thresholds = np.linspace(0, 30, 50)
pck_curve = [np.mean(pck_dist < t) for t in thresholds]
axes[1, 2].plot(thresholds, pck_curve, "b-", lw=2)
axes[1, 2].axvline(pck_thresh, color="r", ls="--")
axes[1, 2].set_xlabel("Distance threshold (px)")
axes[1, 2].set_ylabel("PCK")
axes[1, 2].set_title("PCK Curve\nArea Under Curve")

plt.tight_layout()
plt.savefig("../../assets/phase08/14-human-pose.png")
plt.close()

print("=" * 60)
print("HUMAN POSE ESTIMATION")
print("=" * 60)
print(f"\nDataset: Single person, {n_joints} keypoints (COCO format)")
print(f"  PCK@{pck_thresh}: {pck:.4f}")
print(f"  mOKS: {np.mean(oks):.4f}")
print(f"  Average error: {np.mean(pck_dist):.2f} px")

print(f"\nPer-joint error (worst joints):")
worst_idx = np.argsort(pck_dist)[-3:][::-1]
for idx in worst_idx:
    print(f"  {joint_names[idx]}: {pck_dist[idx]:.2f} px, OKS={oks[idx]:.4f}")

print(f"\nApproaches:")
print(f"  • Top-down: detect person → estimate pose")
print(f"    → SimpleBaseline, HRNet, ViTPose")
print(f"    → Scales with #people (O(n))")
print(f"  • Bottom-up: detect all joints → associate")
print(f"    → OpenPose, Associative Embedding")
print(f"    → O(1) per image (constant)")
print(f"\nMetrics:")
print(f"  • PCK/PCKh: % of correct keypoints")
print(f"  • OKS: object keypoint similarity (COCO)")
print(f"  • AP: average precision (COCO evaluation)")
