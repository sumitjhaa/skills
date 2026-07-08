"""08.15 3D pose and shape: SMPL, VIBE, mesh recovery."""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

np.random.seed(42)

n_vertices = 100
vertices = np.random.randn(n_vertices, 3) * 0.3
faces = np.random.randint(0, n_vertices, (50, 3))
joints_3d = np.random.randn(17, 3) * 0.5
joints_2d = joints_3d[:, :2] / (1 + joints_3d[:, 2:]) * 200 + 100

n_frames = 50
pose_seq = np.sin(np.linspace(0, 4*np.pi, n_frames))[:, None, None] * np.random.randn(1, 17, 3)
pose_seq = pose_seq.reshape(n_frames, -1)

camera_t = np.array([0, 0, 5])
focal = 500

reproj = joints_3d[:, :2] * focal / (joints_3d[:, 2:] + camera_t[2])
reproj += camera_t[:2]
reproj_error = np.mean(np.linalg.norm(reproj - joints_2d[:len(reproj)]))

fig = plt.figure(figsize=(14, 9))
gs = fig.add_gridspec(2, 3)
axes = [fig.add_subplot(gs[0, 0], projection="3d"),
        fig.add_subplot(gs[0, 1]),
        fig.add_subplot(gs[0, 2]),
        fig.add_subplot(gs[1, 0], projection="3d"),
        fig.add_subplot(gs[1, 1]),
        fig.add_subplot(gs[1, 2])]

skel_3d = [(0, 1), (0, 2), (1, 3), (2, 4), (5, 6), (5, 7), (7, 9),
           (6, 8), (8, 10), (5, 11), (6, 12), (11, 13), (13, 15),
           (12, 14), (14, 16)]

ax = axes[0]
ax.scatter(joints_3d[:, 0], joints_3d[:, 1], joints_3d[:, 2], c="blue", s=30)
for i, j in skel_3d[:min(len(skel_3d), len(joints_3d)-1)]:
    ax.plot([joints_3d[i, 0], joints_3d[j, 0]],
           [joints_3d[i, 1], joints_3d[j, 1]],
           [joints_3d[i, 2], joints_3d[j, 2]], "b-", lw=2)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_title("3D Pose (SMPL joints)")
ax.grid(True, alpha=0.3)

ax2 = axes[1]
ax2.scatter(joints_2d[:, 0], joints_2d[:, 1], c="red", s=30)
for i, j in skel_3d[:min(len(skel_3d), len(joints_3d)-1)]:
    ax2.plot([joints_2d[i, 0], joints_2d[j, 0]],
            [joints_2d[i, 1], joints_2d[j, 1]], "r-", lw=2)
ax2.set_xlim(0, 200); ax2.set_ylim(200, 0)
ax2.set_title("2D Projection\n(weak perspective)")
ax2.grid(True, alpha=0.3)
ax2.set_aspect("equal")

pose_var = np.var(pose_seq, axis=0)
ax3 = axes[2]
ax3.bar(range(len(pose_var)), pose_var, alpha=0.7)
ax3.set_xlabel("Pose parameter index")
ax3.set_ylabel("Variance")
ax3.set_title("Pose Parameter Variance\n(over 50 frames)")
ax3.grid(True, axis="y", alpha=0.3)

vert_mean = vertices.mean(axis=0)
vertices_centered = vertices - vert_mean
ax4 = axes[3]
ax4.scatter(vertices_centered[:, 0], vertices_centered[:, 1], vertices_centered[:, 2],
           c=vertices_centered[:, 2], cmap="coolwarm", s=5)
ax4.set_xlabel("x"); ax4.set_ylabel("y"); ax4.set_zlabel("z")
ax4.set_title("SMPL-like Mesh\n(100 vertices)")
ax4.grid(True, alpha=0.3)

ax5 = axes[4]
weak_persp = np.linspace(0.5, 2, 30)
reproj_errors = []
for s in weak_persp:
    r = joints_3d[:, :2] * s
    err = np.mean(np.linalg.norm(r - joints_2d[:len(joints_3d)], axis=1))
    reproj_errors.append(err)
ax5.plot(weak_persp, reproj_errors, "o-", lw=2)
ax5.set_xlabel("Scale factor")
ax5.set_ylabel("Reprojection error")
ax5.set_title("Optimal Camera Scale\nfor 2D→3D projection")
ax5.grid(True, alpha=0.3)

ax6 = axes[5]
n_params = [10, 20, 50, 100, 200, 500, 1000]
recon_err = [0.5 / np.sqrt(n) for n in n_params]
ax6.loglog(n_params, recon_err, "o-", lw=2)
ax6.loglog(n_params, 1/np.sqrt(n_params), "--", lw=2, label="O(1/√n)")
ax6.set_xlabel("Mesh vertices")
ax6.set_ylabel("Reconstruction error")
ax6.set_title("3D Mesh: Error vs\nVertex Count")
ax6.legend()
ax6.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/15-3d-pose-shape.png")
plt.close()

print("=" * 60)
print("3D POSE AND SHAPE")
print("=" * 60)
print(f"\n3D pose: {len(joints_3d)} joints")
print(f"  2D reprojection error: {reproj_error:.4f} px")
print(f"  Optimal scale: {weak_persp[np.argmin(reproj_errors)]:.4f}")

print(f"\nPose sequence ({n_frames} frames):")
print(f"  Mean pose variance: {np.mean(pose_var):.4f}")
print(f"  Top 3 most variable params: {np.argsort(pose_var)[-3:][::-1]}")

print(f"\nMesh: {n_vertices} vertices, {len(faces)} faces")
print(f"  Bounding box: [{vertices.min(axis=0)}, {vertices.max(axis=0)}]")

print(f"\nSMPL model parameters:")
print(f"  • Shape (β): 10 PCA coefficients (~身高, 体型)")
print(f"  • Pose (θ): 72 parameters (24 joints × 3)")
print(f"  • Translation (γ): 3 parameters")
print(f"  • Total: ~85 parameters → 6890 vertices")
print(f"\nKey methods:")
print(f"  • SMPL: Skinned Multi-Person Linear Model")
print(f"  • VIBE: video inference ( temporal context)")
print(f"  • HMR: human mesh recovery (regression)")
print(f"  • PIFu: pixel-aligned implicit function")
