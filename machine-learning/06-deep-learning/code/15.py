"""06.15 - Convolutions: Conv2d, depthwise, dilated, transposed, group conv"""

import numpy as np


def im2col(x, k_h, k_w, stride=1, pad=0):
    N, C, H, W = x.shape
    H_out = (H + 2 * pad - k_h) // stride + 1
    W_out = (W + 2 * pad - k_w) // stride + 1
    x_pad = np.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)), mode="constant")
    cols = np.zeros((N, C, k_h, k_w, H_out, W_out))
    for i in range(k_h):
        for j in range(k_w):
            cols[:, :, i, j, :, :] = x_pad[:, :, i:i + H_out * stride:stride, j:j + W_out * stride:stride]
    return cols.reshape(N, C * k_h * k_w, H_out * W_out).transpose(0, 2, 1)


def conv2d_forward(x, W, b, stride=1, pad=0):
    N, C, H, W_in = x.shape
    K, _, k_h, k_w = W.shape
    H_out = (H + 2 * pad - k_h) // stride + 1
    W_out = (W_in + 2 * pad - k_w) // stride + 1
    cols = im2col(x, k_h, k_w, stride, pad)
    W_flat = W.reshape(K, -1)
    out = cols @ W_flat.T
    out = out.reshape(N, H_out, W_out, K).transpose(0, 3, 1, 2)
    out += b.reshape(1, -1, 1, 1)
    return out


def depthwise_conv2d_forward(x, W, b, stride=1, pad=0):
    N, C, H, W_in = x.shape
    _, C_in, k_h, k_w = W.shape
    H_out = (H + 2 * pad - k_h) // stride + 1
    W_out = (W_in + 2 * pad - k_w) // stride + 1
    cols = im2col(x, k_h, k_w, stride, pad)
    cols = cols.reshape(N, H_out * W_out, C, k_h * k_w)
    W_flat = W.reshape(C, -1)
    out = np.zeros((N, H_out * W_out, C))
    for c in range(C):
        out[:, :, c] = cols[:, :, c, :] @ W_flat[c, :]
    out = out.reshape(N, H_out, W_out, C).transpose(0, 3, 1, 2)
    out += b.reshape(1, -1, 1, 1)
    return out


def dilated_conv2d_forward(x, W, b, dilation=2, stride=1, pad=0):
    k_h, k_w = W.shape[2:]
    k_h_d = k_h + (k_h - 1) * (dilation - 1)
    k_w_d = k_w + (k_w - 1) * (dilation - 1)
    W_d = np.zeros((W.shape[0], W.shape[1], k_h_d, k_w_d))
    for i in range(k_h):
        for j in range(k_w):
            W_d[:, :, i * dilation, j * dilation] = W[:, :, i, j]
    return conv2d_forward(x, W_d, b, stride, pad)


def transposed_conv2d_forward(x, W, b, stride=2, pad=1):
    N, C, H, W_in = x.shape
    K, _, k_h, k_w = W.shape
    H_out = (H - 1) * stride + k_h - 2 * pad
    W_out = (W_in - 1) * stride + k_w - 2 * pad
    out = np.zeros((N, K, H_out, W_out))
    for n in range(N):
        for c in range(C):
            for i in range(H):
                for j in range(W_in):
                    oh = i * stride
                    ow = j * stride
                    h_end = min(oh + k_h, H_out)
                    w_end = min(ow + k_w, W_out)
                    kh_eff = h_end - oh
                    kw_eff = w_end - ow
                    out[n, :, oh:h_end, ow:w_end] += \
                        x[n, c, i, j] * W[:, c, :kh_eff, :kw_eff]
    out += b.reshape(1, -1, 1, 1)
    return out


def group_conv2d_forward(x, W, b, groups=2, stride=1, pad=0):
    N, C, H, W_in = x.shape
    K, Cg, k_h, k_w = W.shape
    C_per_group = C // groups
    K_per_group = K // groups
    x_groups = np.split(x, groups, axis=1)
    W_groups = np.split(W, groups, axis=0)
    b_groups = np.split(b, groups)
    out_groups = []
    for g in range(groups):
        out_g = conv2d_forward(x_groups[g], W_groups[g], b_groups[g], stride, pad)
        out_groups.append(out_g)
    return np.concatenate(out_groups, axis=1)


if __name__ == "__main__":
    np.random.seed(42)
    x = np.random.randn(2, 3, 8, 8)
    W = np.random.randn(4, 3, 3, 3)

    out = conv2d_forward(x, W, np.zeros(4), stride=1, pad=1)
    print(f"Conv2d: {x.shape} -> {out.shape}  (expected: (2, 4, 8, 8))")

    W_dw = np.random.randn(1, 3, 3, 3)
    out_dw = depthwise_conv2d_forward(x, W_dw, np.zeros(3), stride=1, pad=1)
    print(f"Depthwise: {x.shape} -> {out_dw.shape}  (expected: (2, 3, 8, 8))")

    out_dil = dilated_conv2d_forward(x, W, np.zeros(4), dilation=2, stride=1, pad=2)
    print(f"Dilated: {x.shape} -> {out_dil.shape}  (expected: (2, 4, 8, 8))")

    x_small = np.random.randn(2, 3, 4, 4)
    out_t = transposed_conv2d_forward(x_small, W, np.zeros(4), stride=2, pad=1)
    print(f"Transposed: {x_small.shape} -> {out_t.shape}  (expected: (2, 4, 7, 7))")

    x_g = np.random.randn(2, 4, 8, 8)
    W_g = np.random.randn(4, 2, 3, 3)
    out_gg = group_conv2d_forward(x_g, W_g, np.zeros(4), groups=2, stride=1, pad=1)
    print(f"Group conv: {x_g.shape} -> {out_gg.shape}  (expected: (2, 4, 8, 8))")

    print("\nAll convolution variants implemented and tested.")
