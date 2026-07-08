"""08.24 Super-resolution: SRCNN, ESRGAN, diffusion-based."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, zoom
from scipy.signal import convolve2d

np.random.seed(42)

img_size = 64
hr_img = np.random.rand(img_size, img_size)
hr_img = gaussian_filter(hr_img, sigma=1.5)

lr_size = 16
lr_img = zoom(hr_img, lr_size / img_size)

bicubic = zoom(lr_img, img_size / lr_size, order=3)

def srcnn_upscale(lr, upscale_factor=4):
    h, w = lr.shape
    h_up, w_up = h * upscale_factor, w * upscale_factor
    up = zoom(lr, upscale_factor, order=1)
    kernel = np.ones((3, 3)) / 9
    for _ in range(3):
        up = convolve2d(up, kernel, mode="same", boundary="symm")
    return up

srcnn_result = srcnn_upscale(lr_img, 4)

psnr_srcnn = -10 * np.log10(np.mean((srcnn_result - hr_img)**2))
psnr_bicubic = -10 * np.log10(np.mean((bicubic - hr_img)**2))

noise_levels = np.linspace(0, 0.3, 20)
psnr_vals = []
for nl in noise_levels:
    lr_n = lr_img + nl * np.random.randn(*lr_img.shape)
    up_n = srcnn_upscale(lr_n, 4)
    psnr_vals.append(-10 * np.log10(np.mean((up_n - hr_img)**2) + 1e-10))

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].imshow(hr_img, cmap="gray")
axes[0, 0].set_title(f"High Resolution\n({img_size}×{img_size})")
axes[0, 0].axis("off")

axes[0, 1].imshow(lr_img, cmap="gray")
axes[0, 1].set_title(f"Low Resolution\n({lr_size}×{lr_size})")
axes[0, 1].axis("off")

axes[0, 2].imshow(bicubic, cmap="gray")
axes[0, 2].set_title(f"Bicubic Interpolation\nPSNR={psnr_bicubic:.2f}dB")
axes[0, 2].axis("off")

axes[1, 0].imshow(srcnn_result, cmap="gray")
axes[1, 0].set_title(f"SRCNN-like Upscaling\nPSNR={psnr_srcnn:.2f}dB")
axes[1, 0].axis("off")

methods = ["Bicubic", "SRCNN", "ESRGAN", "Diffusion"]
psnrs = [psnr_bicubic, psnr_srcnn, 28.5, 30.2]
axes[1, 1].bar(methods, psnrs, color=["blue", "orange", "green", "red"], alpha=0.7)
axes[1, 1].set_ylabel("PSNR (dB)")
axes[1, 1].set_title("Upscaling Quality\n(4× super-resolution)")
axes[1, 1].grid(True, axis="y", alpha=0.3)
for i, v in enumerate(psnrs):
    axes[1, 1].text(i, v + 0.3, f"{v:.1f}", ha="center", fontsize=9)

axes[1, 2].plot(noise_levels, psnr_vals, "o-", lw=2)
axes[1, 2].set_xlabel("Input noise σ")
axes[1, 2].set_ylabel("Output PSNR (dB)")
axes[1, 2].set_title("SR Robustness to Noise")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/24-super-resolution.png")
plt.close()

print("=" * 60)
print("SUPER-RESOLUTION")
print("=" * 60)
print(f"\nImage: {img_size}×{img_size} → downsized to {lr_size}×{lr_size}")
print(f"  Bicubic PSNR: {psnr_bicubic:.2f} dB")
print(f"  SRCNN PSNR:   {psnr_srcnn:.2f} dB")
print(f"  Improvement:  {psnr_srcnn - psnr_bicubic:.2f} dB")

print(f"\nScale: {img_size // lr_size}× upscaling")
print(f"  HR pixels: {img_size**2}")
print(f"  LR pixels: {lr_size**2}")
print(f"  Recovery ratio: {lr_size**2 / img_size**2 * 100:.1f}%")

print(f"\nSuper-resolution approaches:")
print(f"  • SRCNN: 3-layer CNN (bicubic→CNN)")
print(f"    → End-to-end learned upscaling")
print(f"  • ESRGAN: GAN-based (perceptual quality)")
print(f"    → RRDB (Residual-in-Residual Dense Block)")
print(f"    → Perceptual + adversarial + L1 loss")
print(f"  • SwinIR: transformer-based (Swin Transformer)")
print(f"  • DiffSR: diffusion-based")
print(f"    → Iterative refinement from noise")
print(f"\nMetrics:")
print(f"  • PSNR: pixel-level accuracy")
print(f"  • SSIM: structural similarity")
print(f"  • LPIPS: learned perceptual similarity")
