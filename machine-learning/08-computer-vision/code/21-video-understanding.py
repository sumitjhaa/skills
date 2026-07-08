"""08.21 Video understanding: action recognition, temporal modeling."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

np.random.seed(42)

n_frames = 64
n_classes = 5
n_channels = 3

video = np.random.randn(n_frames, 56, 56, n_channels) * 0.1
action_pattern = np.sin(np.linspace(0, 4*np.pi, n_frames))
for c in range(n_channels):
    video[:, :, :, c] += action_pattern[:, None, None] * 0.3 * np.random.randn(56, 56)

class_scores = np.random.randn(n_frames, n_classes)
class_scores = np.exp(class_scores) / np.exp(class_scores).sum(axis=1, keepdims=True)

temporal_features = np.random.randn(n_frames, 128)
kernel_size = 9
temporal_kernel = np.exp(-np.linspace(-2, 2, kernel_size)**2)
temporal_kernel /= temporal_kernel.sum()
smoothed = np.convolve(np.mean(class_scores[:, 0]), temporal_kernel, mode="same")

optical_flow = np.random.randn(n_frames - 1, 56, 56, 2)
flow_mag = np.sqrt(optical_flow[:, :, :, 0]**2 + optical_flow[:, :, :, 1]**2)

Ts = np.linspace(1, 32, 50, dtype=int)
temporal_similarity = []
for T in Ts:
    if T < n_frames:
        sim = np.mean([np.dot(temporal_features[t], temporal_features[t+T])
                      for t in range(n_frames - T)])
        temporal_similarity.append(sim)
    else:
        temporal_similarity.append(0)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

frame_indices = np.linspace(0, n_frames-1, 8, dtype=int)
for i, idx in enumerate(frame_indices):
    ax = axes[0, 0] if i < 4 else axes[0, 1]
    target_ax = axes[0, 0] if i < 4 else axes[0, 1]
    row, col = i // 2, i % 2
    if i < 4:
        axes[0, 0].imshow(video[idx, :, :, 0], cmap="gray")
    else:
        axes[0, 1].imshow(video[idx, :, :, 0], cmap="gray")
axes[0, 0].set_title("Frames 0-3")
axes[0, 0].axis("off")
axes[0, 1].set_title("Frames 4-7")
axes[0, 1].axis("off")

axes[0, 2].plot(range(n_frames), class_scores[:, :3], lw=2)
axes[0, 2].set_xlabel("Frame")
axes[0, 2].set_ylabel("Class probability")
axes[0, 2].set_title("Per-Frame Class Scores\n(top 3 classes)")
axes[0, 2].legend([f"Class {i}" for i in range(3)])
axes[0, 2].grid(True, alpha=0.3)

axes[1, 0].plot(range(n_frames), np.mean(video, axis=(1, 2, 3)), "b-", lw=2,
               label="Frame mean intensity")
axes[1, 0].plot(range(n_frames), action_pattern, "r--", lw=2, label="Action pattern")
axes[1, 0].set_xlabel("Frame")
axes[1, 0].set_ylabel("Intensity")
axes[1, 0].set_title("Temporal Signal Pattern")
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].plot(range(n_frames-1), flow_mag.mean(axis=(1, 2)), "g-", lw=2)
axes[1, 1].set_xlabel("Frame")
axes[1, 1].set_ylabel("Mean flow magnitude")
axes[1, 1].set_title("Optical Flow Magnitude")
axes[1, 1].grid(True, alpha=0.3)

axes[1, 2].plot(Ts[:len(temporal_similarity)], temporal_similarity, "o-", lw=2)
axes[1, 2].set_xlabel("Temporal offset T")
axes[1, 2].set_ylabel("Avg feature similarity")
axes[1, 2].set_title("Temporal Self-Similarity\n(feature coherence)")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/21-video-understanding.png")
plt.close()

print("=" * 60)
print("VIDEO UNDERSTANDING")
print("=" * 60)
print(f"\nVideo: {n_frames}frames, 56×56×{n_channels}, {n_classes} classes")
print(f"  Mean frame intensity: {np.mean(video):.4f}")
print(f"  Mean optical flow: {np.mean(flow_mag):.4f}")

pred_class = np.argmax(class_scores.mean(axis=0))
print(f"  Predicted class (average): {pred_class}")
print(f"  Class distribution: {np.round(class_scores.mean(axis=0), 3)}")

print(f"\nTemporal coherence:")
print(f"  Max self-similarity at T={Ts[np.argmax(temporal_similarity)]}")

print(f"\nVideo understanding approaches:")
print(f"  • 3D CNNs: C3D, I3D, SlowFast")
print(f"    → 3D convolutions (spatio-temporal)")
print(f"  • Two-stream: RGB + optical flow")
print(f"  • TimeSformer: divided space-time attention")
print(f"  • VideoMAE: masked video modeling")
print(f"  • Action recognition: Kinetics, AVA")
print(f"\nKey challenges:")
print(f"  • Temporal scale variation")
print(f"  • Long-range dependencies (transformers)")
print(f"  • Computational cost (O(T·H·W))")
