"""
08.18 Point Cloud — PointNet-style feature extraction + ICP in numpy
Usage: python 18-point-cloud.py
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

np.random.seed(0)

# synthetic point clouds
n_pts = 100
# source: random points on a sphere
theta = np.random.uniform(0, 2*np.pi, n_pts)
phi = np.arccos(np.random.uniform(-1, 1, n_pts))
src = np.stack([np.sin(phi)*np.cos(theta),
                np.sin(phi)*np.sin(theta),
                np.cos(phi)], axis=1)
# target: rotated + translated
R_gt = np.array([[np.cos(0.5), -np.sin(0.5), 0],
                 [np.sin(0.5), np.cos(0.5), 0],
                 [0, 0, 1]])
t_gt = np.array([0.3, 0.1, 0])
tgt = src @ R_gt.T + t_gt

# simple ICP (1 iteration)
def icp(src, tgt, n_iter=5):
    R = np.eye(3); t = np.zeros(3)
    src_curr = src.copy()
    for _ in range(n_iter):
        # nearest neighbour association
        dists = np.linalg.norm(src_curr[:, None] - tgt[None], axis=2)
        matches = dists.argmin(axis=1)
        # compute optimal rigid transform (closed form)
        mu_s = src_curr.mean(axis=0)
        mu_t = tgt[matches].mean(axis=0)
        H = (src_curr - mu_s).T @ (tgt[matches] - mu_t)
        U, _, Vt = np.linalg.svd(H)
        R_step = Vt.T @ U.T
        if np.linalg.det(R_step) < 0:
            Vt[-1] *= -1
            R_step = Vt.T @ U.T
        t_step = mu_t - R_step @ mu_s
        src_curr = src_curr @ R_step.T + t_step
        R = R_step @ R
        t = t_step + R_step @ t
    return R, t, src_curr

R_est, t_est, src_aligned = icp(src, tgt, n_iter=5)
print(f"Estimated R (first row): {R_est[0].round(3)}")
print(f"GT R (first row):        {R_gt[0].round(3)}")
print(f"Translation error: {np.linalg.norm(t_est - t_gt):.4f}")

fig = plt.figure(figsize=(12, 4))
ax1 = fig.add_subplot(131, projection='3d')
ax1.scatter(src[:,0], src[:,1], src[:,2], c='r', s=5, label='Source')
ax1.scatter(tgt[:,0], tgt[:,1], tgt[:,2], c='b', s=5, label='Target')
ax1.legend(); ax1.set_title('Before ICP')

ax2 = fig.add_subplot(132, projection='3d')
ax2.scatter(src_aligned[:,0], src_aligned[:,1], src_aligned[:,2], c='g', s=5, label='Aligned')
ax2.scatter(tgt[:,0], tgt[:,1], tgt[:,2], c='b', s=5, label='Target')
ax2.legend(); ax2.set_title('After ICP')

ax3 = fig.add_subplot(133)
errors = np.linalg.norm(src_aligned - tgt[icp(src, tgt, 5)[2].argmin(axis=1)], axis=1)
ax3.hist(errors, bins=20)
ax3.set_title('Alignment Errors')

for ax in [ax1, ax2]: ax.view_init(elev=20, azim=30)
plt.tight_layout(); plt.savefig('../../assets/phase08/18_point_cloud.png', dpi=100)
print("Saved 18_point_cloud.png")
