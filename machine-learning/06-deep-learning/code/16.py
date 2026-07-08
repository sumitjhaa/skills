"""06.16 - Pooling: Max, Average, Global, Adaptive, ROI"""

import numpy as np


def max_pool2d(x, pool_size=2, stride=2):
    N, C, H, W = x.shape
    H_out = (H - pool_size) // stride + 1
    W_out = (W - pool_size) // stride + 1
    out = np.zeros((N, C, H_out, W_out))
    for i in range(H_out):
        for j in range(W_out):
            h_start, w_start = i * stride, j * stride
            out[:, :, i, j] = x[:, :, h_start:h_start + pool_size, w_start:w_start + pool_size].max(axis=(2, 3))
    return out


def avg_pool2d(x, pool_size=2, stride=2):
    N, C, H, W = x.shape
    H_out = (H - pool_size) // stride + 1
    W_out = (W - pool_size) // stride + 1
    out = np.zeros((N, C, H_out, W_out))
    for i in range(H_out):
        for j in range(W_out):
            h_start, w_start = i * stride, j * stride
            out[:, :, i, j] = x[:, :, h_start:h_start + pool_size, w_start:w_start + pool_size].mean(axis=(2, 3))
    return out


def global_avg_pool2d(x):
    return x.mean(axis=(2, 3))


def adaptive_pool2d(x, output_size):
    N, C, H, W = x.shape
    out = np.zeros((N, C, output_size[0], output_size[1]))
    for i in range(output_size[0]):
        for j in range(output_size[1]):
            h_start = int(i * H / output_size[0])
            h_end = int((i + 1) * H / output_size[0])
            w_start = int(j * W / output_size[1])
            w_end = int((j + 1) * W / output_size[1])
            out[:, :, i, j] = x[:, :, h_start:h_end, w_start:w_end].mean(axis=(2, 3))
    return out


def roi_pool2d(x, rois, pool_size=2, spatial_scale=1.0):
    N, C, H, W = x.shape
    num_rois = rois.shape[0]
    out = np.zeros((num_rois, C, pool_size, pool_size))
    for i in range(num_rois):
        batch_idx = int(rois[i, 0])
        x1 = int(rois[i, 1] * spatial_scale)
        y1 = int(rois[i, 2] * spatial_scale)
        x2 = int(rois[i, 3] * spatial_scale)
        y2 = int(rois[i, 4] * spatial_scale)
        x1, y1, x2, y2 = max(0, x1), max(0, y1), min(W, x2), min(H, y2)
        if x2 <= x1 or y2 <= y1:
            continue
        region = x[batch_idx, :, y1:y2, x1:x2]
        rh, rw = region.shape[1], region.shape[2]
        for pi in range(pool_size):
            for pj in range(pool_size):
                h_start = int(pi * rh / pool_size)
                h_end = int((pi + 1) * rh / pool_size)
                w_start = int(pj * rw / pool_size)
                w_end = int((pj + 1) * rw / pool_size)
                out[i, :, pi, pj] = region[:, h_start:h_end, w_start:w_end].max(axis=(1, 2))
    return out


if __name__ == "__main__":
    np.random.seed(42)
    x = np.random.randn(2, 3, 8, 8)

    out_max = max_pool2d(x, pool_size=2, stride=2)
    print(f"MaxPool:    {x.shape} -> {out_max.shape}")

    out_avg = avg_pool2d(x, pool_size=2, stride=2)
    print(f"AvgPool:    {x.shape} -> {out_avg.shape}")

    out_gap = global_avg_pool2d(x)
    print(f"GlobalAvg:  {x.shape} -> {out_gap.shape}")

    out_adp = adaptive_pool2d(x, (3, 3))
    print(f"Adaptive:   {x.shape} -> {out_adp.shape}")

    rois = np.array([[0, 1, 1, 5, 5], [1, 2, 2, 6, 6]])
    out_roi = roi_pool2d(x, rois, pool_size=2)
    print(f"ROI Pool:   {x.shape} with {rois.shape[0]} ROIs -> {out_roi.shape}")

    print("\nAll pooling operations implemented and tested.")
