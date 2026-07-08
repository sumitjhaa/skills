"""08.23 Image-to-image translation: Pix2Pix, CycleGAN, diffusion."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

np.random.seed(42)

img_size = 64
n_pairs = 3

source_imgs = []
target_imgs = []
for i in range(n_pairs):
    source = np.random.rand(img_size, img_size)
    source = gaussian_filter(source, sigma=3)
    target = np.sin(source * 4 * np.pi) * 0.5 + 0.5
    source_imgs.append(source)
    target_imgs.append(target)

def cycle_consistency(x, G, F):
    return np.mean((F(G(x)) - x)**2)

def identity_loss(x, G, threshold=0.5):
    return np.mean((G(x) - x)**2) * threshold

G_source = lambda x: np.sin(x * 3 * np.pi) * 0.3 + 0.5 + x * 0.3
F_target = lambda y: np.cos(y * 2 * np.pi) * 0.2 + 0.5 + y * 0.3

cycle_losses = [cycle_consistency(s, G_source, F_target) for s in source_imgs]
identity_losses = [identity_loss(s, G_source) for s in source_imgs]

source_flat = np.array(source_imgs).reshape(n_pairs, -1)
target_flat = np.array(target_imgs).reshape(n_pairs, -1)

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

for i in range(n_pairs):
    axes[0, 0].imshow(source_imgs[i], cmap="gray")
axes[0, 0].set_title("Source Domain A\n(Input)")
axes[0, 0].axis("off")

for i in range(n_pairs):
    axes[0, 1].imshow(target_imgs[i], cmap="gray")
axes[0, 1].set_title("Target Domain B\n(Ground Truth)")
axes[0, 1].axis("off")

translated = [G_source(s) for s in source_imgs]
for i in range(n_pairs):
    axes[0, 2].imshow(translated[i], cmap="gray")
axes[0, 2].set_title("Translated A→B\n(G(A))")
axes[0, 2].axis("off")

cycle_back = [F_target(G_source(s)) for s in source_imgs]
for i in range(n_pairs):
    axes[1, 0].imshow(cycle_back[i], cmap="gray")
axes[1, 0].set_title("Cycle: A→B→A\n(F(G(A)))")
axes[1, 0].axis("off")

axes[1, 1].bar(range(n_pairs), cycle_losses, alpha=0.7, label="Cycle loss")
axes[1, 1].bar(range(n_pairs), identity_losses, alpha=0.5, label="Identity loss")
axes[1, 1].set_xlabel("Image pair")
axes[1, 1].set_ylabel("Loss")
axes[1, 1].set_title("CycleGAN Loss Components")
axes[1, 1].legend()
axes[1, 1].grid(True, axis="y", alpha=0.3)

steps = np.arange(1, 50)
g_loss = 1 / steps + 0.1 * np.random.randn(49)
d_loss = np.exp(-steps / 20) + 0.1 * np.random.randn(49)
g_loss = np.maximum(g_loss, 0)
d_loss = np.maximum(d_loss, 0)
axes[1, 2].plot(steps, g_loss, "r-", lw=2, label="Generator loss")
axes[1, 2].plot(steps, d_loss, "b-", lw=2, label="Discriminator loss")
axes[1, 2].set_xlabel("Training step")
axes[1, 2].set_ylabel("Loss")
axes[1, 2].set_title("GAN Training Dynamics")
axes[1, 2].legend()
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/23-image-to-image.png")
plt.close()

print("=" * 60)
print("IMAGE-TO-IMAGE TRANSLATION")
print("=" * 60)
print(f"\nPaired translation ({n_pairs} image pairs):")
print(f"  Cycle consistency losses: {np.round(cycle_losses, 4)}")
print(f"  Identity losses: {np.round(identity_losses, 4)}")
print(f"  Mean cycle loss: {np.mean(cycle_losses):.4f}")

corr_source = np.corrcoef(source_flat[0], source_flat[1])[0, 1]
corr_cycle = np.corrcoef(cycle_back[0].ravel(), source_imgs[0].ravel())[0, 1]
print(f"  Cycle consistency correlation: {corr_cycle:.4f}")

print(f"\nImage translation approaches:")
print(f"  • Pix2Pix: conditional GAN (paired data)")
print(f"    → U-Net generator + PatchGAN discriminator")
print(f"    → L1 + adversarial loss")
print(f"  • CycleGAN: unpaired translation")
print(f"    → Cycle consistency loss: G(F(x)) ≈ x")
print(f"    → Identity loss: G(x) ≈ x when x is in B")
print(f"  • Palette: diffusion-based (multi-task)")
print(f"  • InstructPix2Pix: instruction-guided editing")
print(f"\nLosses:")
print(f"  • Adversarial: L_GAN = log(D(y)) + log(1 - D(G(x)))")
print(f"  • Cycle: L_cyc = ||F(G(x)) - x||₁")
print(f"  • Identity: L_id = ||G(y) - y||₁")
