"""08.22 Video generation: prediction, interpolation, synthesis."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

n_frames = 16
img_size = 32

video = np.zeros((n_frames, img_size, img_size))
cx, cy = img_size // 2, img_size // 8
for f in range(n_frames):
    cy += 2
    r = 4 + f // 4
    yy, xx = np.ogrid[:img_size, :img_size]
    video[f] = np.exp(-((xx - cx)**2 + (yy - cy)**2) / (2 * r**2))
video += 0.05 * np.random.randn(*video.shape)

pred_future = np.zeros((4, img_size, img_size))
for f in range(4):
    cy_f = cy + 2 * (f + 1)
    yy, xx = np.ogrid[:img_size, :img_size]
    pred_future[f] = np.exp(-((xx - cx)**2 + (yy - cy_f)**2) / (2 * (4 + (n_frames + f) // 4)**2))

pred_interp = np.zeros((n_frames * 2 - 1, img_size, img_size))
for f in range(n_frames * 2 - 1):
    t = f / (2 * (n_frames - 1))
    cy_t = img_size // 8 + 2 * t * (img_size * 3 // 4)
    yy, xx = np.ogrid[:img_size, :img_size]
    pred_interp[f] = np.exp(-((xx - cx)**2 + (yy - cy_t)**2) / (2 * 6**2))

gt_vs_future = np.mean((pred_future - video[-4:])**2)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

frame_idx = [0, 4, 8, 12]
for i, idx in enumerate(frame_idx):
    axes[0, 0].imshow(video[idx], cmap="gray")
axes[0, 0].set_title("Input Video\n(frames 0, 4, 8, 12)")
axes[0, 0].axis("off")

for i in range(4):
    axes[0, 1].imshow(pred_future[i], cmap="gray")
axes[0, 1].set_title("Future Prediction\n(next 4 frames)")
axes[0, 1].axis("off")

for i in range(0, 4, 1):
    target_ax = axes[0, 2]
    target_ax.imshow(pred_interp[i * (len(pred_interp)//4)], cmap="gray")
axes[0, 2].set_title("Interpolation")
axes[0, 2].axis("off")

n_pixels = img_size * img_size
flat_video = video.reshape(n_frames, -1)
U, s, Vt = np.linalg.svd(flat_video, full_matrices=False)
recon_dims = [1, 2, 3, 5, 10, 16]
recon_errors = []
for k in recon_dims:
    recon = U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :]
    recon_errors.append(np.mean((recon - flat_video)**2))
axes[1, 0].plot(recon_dims, recon_errors, "o-", lw=2)
axes[1, 0].set_xlabel("SVD components (k)")
axes[1, 0].set_ylabel("MSE")
axes[1, 0].set_title(f"Video SVD Reconstruction\n"
                     f"variance explained: {s[:3].sum()/s.sum()*100:.1f}%")
axes[1, 0].grid(True, alpha=0.3)

ts = np.linspace(0, 1, 100)
flow_x = -5 * np.sin(2 * np.pi * ts)
flow_y = 10 * np.ones(100)
axes[1, 1].plot(ts, flow_x, "b-", lw=2, label="vx")
axes[1, 1].plot(ts, flow_y, "r-", lw=2, label="vy")
axes[1, 1].set_xlabel("Time")
axes[1, 1].set_ylabel("Velocity (px/frame)")
axes[1, 1].set_title("Motion Trajectory\nfor Video Prediction")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

n_params = [1, 2, 5, 10, 20, 50]
mvae_params = [p * 1000 * 4 + 1000 * p for p in n_params]
gan_params = [p * 1000 * 4 * 3 for p in n_params]
axes[1, 2].loglog(n_params, mvae_params, "o-", lw=2, label="Video VAE")
axes[1, 2].loglog(n_params, gan_params, "s-", lw=2, label="Video GAN")
axes[1, 2].set_xlabel("Latent dimension")
axes[1, 2].set_ylabel("Model parameters")
axes[1, 2].set_title("Model Complexity\nVAE vs GAN")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/22-video-generation.png")
plt.close()

print("=" * 60)
print("VIDEO GENERATION")
print("=" * 60)
print(f"\nVideo: {n_frames} frames, {img_size}×{img_size}")
print(f"  Future prediction MSE: {gt_vs_future:.4f}")
print(f"  SVD top 3 singular values: {np.round(s[:3], 2)}")
print(f"  Low-rank approx (k=3) explains {s[:3].sum()/s.sum()*100:.1f}% variance")

print(f"\nVideo generation tasks:")
print(f"  • Future prediction: given past → predict future, {gt_vs_future:.4f} MSE")
print(f"  • Interpolation: generate intermediate frames")
print(f"  • Video synthesis: generate entire video from noise")
print(f"  • Conditional generation: text/class → video")

print(f"\nKey methods:")
print(f"  • Video diffusion: VDMs (Video Diffusion Models)")
print(f"    → Denoising in space-time")
print(f"  • MoCoGAN: motion + content disentanglement")
print(f"  • DVD-GAN: dual discriminator (spatial + temporal)")
print(f"  • CogVideo: transformer-based (text-to-video)")
print(f"  • Sora: large-scale video diffusion (OpenAI)")
