"""08.19 3D object detection: point clouds, BEV, voxels."""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

np.random.seed(42)

n_objects = 4
n_points = 500

objects_3d = []
for i in range(n_objects):
    cx, cy = np.random.uniform(-10, 10, 2)
    cz = np.random.uniform(0, 0.5)
    w, l, h = np.random.uniform(1, 3, 3)
    theta = np.random.uniform(0, 2*np.pi)
    objects_3d.append({"center": [cx, cy, cz], "size": [w, l, h],
                       "angle": theta, "class": i % 3})

point_cloud = np.random.randn(n_points, 3) * 0.5
for obj in objects_3d:
    c = obj["center"]
    w, l, h = obj["size"]
    angle = obj["angle"]
    n_obj_pts = np.random.randint(30, 80)
    pts = np.random.randn(n_obj_pts, 3) * np.array([w/4, l/4, h/4])
    c_, s_ = np.cos(angle), np.sin(angle)
    rot = np.array([[c_, -s_, 0], [s_, c_, 0], [0, 0, 1]])
    pts = pts @ rot.T + c
    point_cloud = np.vstack([point_cloud, pts])

n_voxels = 20
voxel_grid = np.zeros((n_voxels, n_voxels, n_voxels))
pc_min, pc_max = point_cloud.min(axis=0), point_cloud.max(axis=0)
scale = n_voxels / (pc_max - pc_min + 1e-10)
for pt in point_cloud:
    idx = np.floor((pt - pc_min) * scale).astype(int)
    if np.all((idx >= 0) & (idx < n_voxels)):
        voxel_grid[tuple(idx)] += 1

bev_map = voxel_grid.max(axis=2)

fig = plt.figure(figsize=(14, 9))
gs = fig.add_gridspec(2, 3)
axes = [fig.add_subplot(gs[0, 0], projection="3d"),
        fig.add_subplot(gs[0, 1]),
        fig.add_subplot(gs[0, 2]),
        fig.add_subplot(gs[1, 0], projection="3d"),
        fig.add_subplot(gs[1, 1]),
        fig.add_subplot(gs[1, 2])]

ax = axes[0]
ax.scatter(point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2],
          c=point_cloud[:, 2], cmap="viridis", s=1, alpha=0.6)
for obj in objects_3d:
    c = obj["center"]
    ax.scatter(c[0], c[1], c[2], c="red", s=50)
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
ax.set_title(f"3D Point Cloud\n({len(point_cloud)} points, {n_objects} objects)")
ax.grid(True, alpha=0.3)

ax2 = axes[1]
ax2.imshow(bev_map, cmap="hot", origin="lower",
           extent=[pc_min[0], pc_max[0], pc_min[1], pc_max[1]])
for obj in objects_3d:
    c = obj["center"]
    ax2.plot(c[0], c[1], "co", ms=8)
    w, l, h = obj["size"]
    rect = plt.Rectangle((c[0]-w/2, c[1]-l/2), w, l, angle=np.degrees(obj["angle"]),
                         fill=False, color="cyan", lw=2)
    ax2.add_patch(rect)
ax2.set_xlabel("x"); ax2.set_ylabel("y")
ax2.set_title("Bird's Eye View (BEV)\n+ 3D bounding boxes")
ax2.grid(True, alpha=0.3)

ax3 = axes[2]
ax3.bar(range(n_objects), [obj["size"][0] for obj in objects_3d], alpha=0.7,
        label="Width")
ax3.bar(range(n_objects), [obj["size"][1] for obj in objects_3d], alpha=0.5,
        label="Length", bottom=[obj["size"][0] for obj in objects_3d])
ax3.set_xlabel("Object index")
ax3.set_ylabel("Size (m)")
ax3.set_title("3D Bounding Box Sizes")
ax3.legend()
ax3.grid(True, axis="y", alpha=0.3)

ax4 = axes[3]
zc = point_cloud[np.abs(point_cloud[:, 2]) < 0.5]
yc = point_cloud[np.abs(point_cloud[:, 1]) < 1]
ax4.scatter(point_cloud[:, 0], point_cloud[:, 2], c=point_cloud[:, 2],
           cmap="viridis", s=1, alpha=0.6)
ax4.set_xlabel("x"); ax4.set_ylabel("z")
ax4.set_title("Side View\n(x-z projection)")
ax4.grid(True, alpha=0.3)

ax5 = axes[4]
voxel_counts = voxel_grid[voxel_grid > 0]
ax5.hist(voxel_counts, bins=20, alpha=0.7)
ax5.set_xlabel("Points per voxel")
ax5.set_ylabel("Frequency")
ax5.set_title(f"Voxel Occupancy\n({n_voxels}³ grid)")
ax5.grid(True, alpha=0.3)

ax6 = axes[5]
classes = [obj["class"] for obj in objects_3d]
ax6.hist(classes, bins=range(4), alpha=0.7, rwidth=0.8)
ax6.set_xticks(range(3))
ax6.set_xlabel("Class")
ax6.set_ylabel("Count")
ax6.set_title("Object Class Distribution")
ax6.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/19-3d-object-detection.png")
plt.close()

print("=" * 60)
print("3D OBJECT DETECTION")
print("=" * 60)
print(f"\nPoint cloud: {len(point_cloud)} points")
print(f"  Bounds: x=[{pc_min[0]:.1f}, {pc_max[0]:.1f}], "
      f"y=[{pc_min[1]:.1f}, {pc_max[1]:.1f}]")

print(f"\nObjects ({n_objects}):")
for i, obj in enumerate(objects_3d):
    print(f"  Object {i}: center={np.round(obj['center'], 2)}, "
          f"size={np.round(obj['size'], 2)}, "
          f"class={obj['class']}")

print(f"\n3D detection approaches:")
print(f"  • Point-based: PointNet++, PointPillars")
print(f"    → Operate directly on point clouds")
print(f"  • Voxel-based: VoxelNet, SECOND")
print(f"    → 3D convolutions on voxel grid")
print(f"  • BEV-based: CenterPoint, BEVFormer")
print(f"    → Project to bird's eye view")
print(f"    → 2D detection pipeline")
print(f"  • Multi-modal: camera + LiDAR fusion")
