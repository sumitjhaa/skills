"""
08.13 Depth Estimation — synthetic disparity from stereo pair
Usage: python 13-depth-estimation.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

np.random.seed(0)

# synthetic depth map (ground truth)
depth_gt = np.zeros((64, 64))
depth_gt[10:30, 10:30] = 0.5
depth_gt[35:50, 35:50] = 0.8
depth_gt = ndimage.gaussian_filter(depth_gt, sigma=2)

# stereo: shift creates disparity
disparity = 20 * depth_gt + 2  # pixels
left = np.random.randn(64, 64) * 0.05
for y in range(64):
    for x in range(64):
        left[y, x] += 0.5 + 0.5 * np.sin(x/5)
left = np.clip(left, 0, 1)

right = np.zeros_like(left)
for y in range(64):
    for x in range(64):
        d = int(round(disparity[y, x]))
        src_x = x - d
        if 0 <= src_x < 64:
            right[y, x] = left[y, src_x]

# simple block matching to estimate disparity
def block_match(left, right, block=5, max_d=30):
    h, w = left.shape
    disp = np.zeros((h, w))
    for y in range(h):
        for x in range(w):
            best_d = 0
            best_sad = float('inf')
            y0, y1 = max(0, y-block//2), min(h, y+block//2+1)
            for d in range(max_d):
                x0_l, x1_l = max(0, x-block//2), min(w, x+block//2+1)
                x0_r, x1_r = max(0, x-d-block//2), min(w, x-d+block//2+1)
                if x0_r >= x1_r: continue
                patch_l = left[y0:y1, x0_l:x1_l]
                patch_r = right[y0:y1, x0_r:x1_r]
                min_h = min(patch_l.shape[0], patch_r.shape[0])
                min_w_p = min(patch_l.shape[1], patch_r.shape[1])
                sad = np.sum(np.abs(patch_l[:min_h, :min_w_p] - patch_r[:min_h, :min_w_p]))
                if sad < best_sad:
                    best_sad = sad
                    best_d = d
            disp[y, x] = best_d
    return disp

disp_est = block_match(left, right)

depth_est = np.where(disp_est > 1, 1.0 / disp_est, 0)

fig, axes = plt.subplots(2, 3, figsize=(10, 6))
axes[0,0].imshow(left, cmap='gray'); axes[0,0].set_title('Left View')
axes[0,1].imshow(right, cmap='gray'); axes[0,1].set_title('Right View')
axes[0,2].imshow(disparity, cmap='plasma'); axes[0,2].set_title('GT Disparity')
axes[1,0].imshow(disp_est, cmap='plasma'); axes[1,0].set_title('Estimated Disparity')
axes[1,1].imshow(depth_gt, cmap='plasma'); axes[1,1].set_title('GT Depth')
axes[1,2].imshow(depth_est, cmap='plasma'); axes[1,2].set_title('Estimated Depth')
for ax in axes.flat: ax.axis('off')
plt.tight_layout(); plt.savefig('../../assets/phase08/13_depth_estimation.png', dpi=100)
print("Saved 13_depth_estimation.png")
