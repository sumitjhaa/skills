"""08.30 Multimodal generation: text-to-image, DALL-E, Stable Diffusion."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

np.random.seed(42)

img_size = 64
n_steps = 50

text_embed = np.random.randn(77, 768)
noise = np.random.randn(img_size, img_size, 3)

def diffusion_step(x_t, t, text_cond):
    alpha = np.exp(-0.02 * t)
    noise_pred = 0.1 * x_t + 0.5 * np.mean(text_cond) * np.ones_like(x_t)
    x_next = (1 / np.sqrt(alpha)) * (x_t - (1 - alpha) / np.sqrt(1 - alpha) * noise_pred)
    x_next += np.sqrt(1 - alpha) * np.random.randn(*x_t.shape) * 0.1
    return x_next

generated = noise.copy()
for t in range(n_steps, 0, -1):
    generated = diffusion_step(generated, t / n_steps, text_embed)
generated = (generated - generated.min()) / (generated.max() - generated.min())

latent = np.random.randn(4, img_size // 8, img_size // 8)
decoded = gaussian_filter(np.random.randn(img_size, img_size, 3), sigma=1)
decoded = (decoded - decoded.min()) / (decoded.max() - decoded.min())

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

n_show = 10
t_steps = np.linspace(0, n_steps, n_show, dtype=int)[::-1]
for i, t in enumerate(t_steps):
    if i < 5:
        ax = axes[0, 0] if i < 3 else axes[0, 1]
    noise_vis = gaussian_filter(np.random.randn(img_size, img_size), sigma=max(1, t//10))
    noise_vis = (noise_vis - noise_vis.min()) / (noise_vis.max() - noise_vis.min())
axes[0, 0].imshow(noise_vis, cmap="gray")
axes[0, 0].set_title("Diffusion Process\n(noise → image)")
axes[0, 0].axis("off")
axes[0, 1].axis("off")

axes[0, 2].imshow(generated)
axes[0, 2].set_title("Generated Image\n(text-to-image)")
axes[0, 2].axis("off")

for i in range(4):
    ax = axes[1, 0] if i < 2 else axes[1, 0]
    latent_vis = gaussian_filter(latent[i], sigma=1)
    pass
axes[1, 0].imshow(gaussian_filter(latent[0], sigma=1), cmap="gray")
axes[1, 0].set_title("Latent (VAE encoding)\n4×8×8")
axes[1, 0].axis("off")

axes[1, 1].imshow(decoded)
axes[1, 1].set_title("Decoded Image\n(VAE decoder)")
axes[1, 1].axis("off")

classifier_free_scale = np.linspace(0, 10, 30)
fid_scores = 30 - 5 * np.log(classifier_free_scale + 1) + np.random.randn(30) * 1
fid_scores = np.maximum(fid_scores, 5)
axes[1, 2].plot(classifier_free_scale, fid_scores, "o-", lw=2)
axes[1, 2].axvline(7.5, color="r", ls="--", label="CFG=7.5 (optimal)")
axes[1, 2].set_xlabel("Classifier-free guidance scale")
axes[1, 2].set_ylabel("FID (lower is better)")
axes[1, 2].set_title("CFG Scale vs Image Quality")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/30-multimodal-generation.png")
plt.close()

print("=" * 60)
print("MULTIMODAL GENERATION")
print("=" * 60)
print(f"\nText-to-image generation ({img_size}×{img_size})")
print(f"  Text embedding: {text_embed.shape}")
print(f"  Diffusion steps: {n_steps}")
print(f"  Final image range: [{generated.min():.3f}, {generated.max():.3f}]")

print(f"\nKey components:")
print(f"  • Text encoder: CLIP/GPT (77 tokens, 768-dim)")
print(f"  • VAE: compress to latent space")
print(f"    → 64²×3 → 8²×4 (64× compression)")
print(f"  • UNet: denoising in latent space")
print(f"  • Scheduler: noise schedule (DDPM, DDIM)")

print(f"\nKey models:")
print(f"  • DALL-E 2: CLIP prior + diffusion decoder")
print(f"  • Stable Diffusion: latent diffusion")
print(f"    → 512² generation on consumer GPUs")
print(f"    → Cross-attention for text conditioning")
print(f"  • Imagen: text-to-image in pixel space")
print(f"    → Cascade of diffusion models")
print(f"  • DALL-E 3: text-to-image (improved captioning)")

print(f"\nClassifier-free guidance (CFG):")
print(f"  ε_CFG = ε_cond + s·(ε_cond - ε_uncond)")
print(f"  s=7.5 is typical best quality")
print(f"  Optimial FID at s={classifier_free_scale[np.argmin(fid_scores)]:.1f}")
