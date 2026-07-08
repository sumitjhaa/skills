"""08.16 Neural face models: 3DMM, FaceGAN, style-based."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

np.random.seed(42)

n_landmarks = 68
shape_mean = np.random.randn(n_landmarks, 2) * 0.5
shape_pca = np.random.randn(n_landmarks * 2, 10)
shape_coeffs = np.random.randn(10) * 0.5
shape = shape_mean + (shape_pca @ shape_coeffs).reshape(n_landmarks, 2) * 0.1

expr_basis = np.random.randn(n_landmarks * 2, 5)
expr_coeffs = np.random.randn(5) * 0.3
expression = (expr_basis @ expr_coeffs).reshape(n_landmarks, 2) * 0.05

final_shape = shape + expression
final_shape[:, 1] *= -1

n_latent = 512
w_latent = np.random.randn(n_latent)
style_mixing = np.random.randn(8, n_latent)

img_size = 64
face_img = gaussian_filter(np.random.randn(img_size, img_size), sigma=2)
face_img = (face_img - face_img.min()) / (face_img.max() - face_img.min())

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

mean_face = (shape_mean - shape_mean.min(axis=0)) / (shape_mean.max(axis=0) - shape_mean.min(axis=0))
axes[0, 0].scatter(mean_face[:, 0], mean_face[:, 1], c="gray", s=10, alpha=0.5)
axes[0, 0].set_title("3DMM: Mean Face Shape\n(68 landmarks)")
axes[0, 0].axis("equal")
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].scatter(shape[:, 0], shape[:, 1], c="blue", s=20, alpha=0.7,
                  label="Identity")
for i in range(0, n_landmarks, 10):
    axes[0, 1].annotate(str(i), (shape[i, 0], shape[i, 1]), fontsize=6)
axes[0, 1].scatter(final_shape[:, 0], final_shape[:, 1], c="red", s=20, alpha=0.5,
                  label="+ Expression")
axes[0, 1].set_title("Identity + Expression\nVariation")
axes[0, 1].legend()
axes[0, 1].axis("equal")
axes[0, 1].grid(True, alpha=0.3)

im = axes[0, 2].imshow(shape_pca.reshape(n_landmarks, 2, 10)[:, :, 0], cmap="coolwarm")
axes[0, 2].set_title("First PCA Component\n(identity variation)")
plt.colorbar(im, ax=axes[0, 2])

latent_dims = np.arange(1, 11)
explained_var = 1 / latent_dims**2
explained_var /= explained_var.sum()
axes[1, 0].bar(latent_dims, explained_var, alpha=0.7)
axes[1, 0].plot(latent_dims, np.cumsum(explained_var), "ro-", lw=2, label="Cumulative")
axes[1, 0].set_xlabel("PCA component")
axes[1, 0].set_ylabel("Variance explained")
axes[1, 0].set_title("3DMM: PCA Variance\n(identity space)")
axes[1, 0].legend()
axes[1, 0].grid(True, axis="y", alpha=0.3)

truncation_psi = np.linspace(0, 1, 20)
truncation_effect = truncation_psi * 0.5 + 0.5
axes[1, 1].plot(truncation_psi, truncation_effect, "o-", lw=2)
axes[1, 1].axvline(0.7, color="r", ls="--", label="ψ=0.7 (StyleGAN2)")
axes[1, 1].set_xlabel("Truncation ψ")
axes[1, 1].set_ylabel("Feature magnitude")
axes[1, 1].set_title("StyleGAN: Truncation Trick\n(trade-off fidelity vs diversity)")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

axes[1, 2].imshow(face_img, cmap="gray")
axes[1, 2].scatter(final_shape[:, 0] * img_size / 4 + img_size/2,
                   final_shape[:, 1] * img_size / 4 + img_size/2,
                   c="red", s=5, alpha=0.7)
axes[1, 2].set_title("Facial Landmarks\non Generated Face")
axes[1, 2].axis("off")

plt.tight_layout()
plt.savefig("../../assets/phase08/16-neural-face-models.png")
plt.close()

print("=" * 60)
print("NEURAL FACE MODELS")
print("=" * 60)
print(f"\n3D Morphable Model (3DMM):")
print(f"  Shape: {n_landmarks} landmarks × 2D")
print(f"  Identity PCA dims: {shape_pca.shape[1]}")
print(f"  Expression dims: {expr_basis.shape[1]}")
print(f"  Total params: {shape_pca.shape[1] + expr_basis.shape[1]}")

print(f"\nPCA variance explained:")
for i in range(5):
    print(f"  PC{i+1}: {explained_var[i]*100:.1f}%")

print(f"\nFace generation approaches:")
print(f"  • 3DMM: PCA-based face model")
print(f"    → Identity + expression + texture")
print(f"  • StyleGAN: style-based generator")
print(f"    → W-space latent (512-dim)")
print(f"    → Style mixing for local control")
print(f"    → Truncation trick (ψ=0.7)")
print(f"  • Face reenactment: expression transfer")
print(f"  • NeRFace: NeRF for faces")
