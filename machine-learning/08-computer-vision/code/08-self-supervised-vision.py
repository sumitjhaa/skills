"""08.08 Self-supervised vision: SimCLR, MAE, DINO."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

np.random.seed(42)

def simclr_loss(z_i, z_j, temperature=0.5, n_negatives=100):
    n = len(z_i)
    pos_sim = np.sum(z_i * z_j) / temperature
    neg_sim = 0
    for k in range(n_negatives):
        idx = np.random.randint(n)
        neg_sim += np.sum(z_i * np.roll(z_j, idx + 1)) / temperature
    return -np.log(np.exp(pos_sim) / (np.exp(pos_sim) + np.exp(neg_sim / n_negatives)))

def mae_loss(x, x_recon, mask_ratio=0.75):
    n = len(x.ravel())
    n_masked = int(n * mask_ratio)
    masked_idx = np.random.choice(n, n_masked, replace=False)
    mse = np.mean((x.ravel()[masked_idx] - x_recon.ravel()[masked_idx])**2)
    return mse

n_dims = 128
z_i = np.random.randn(n_dims)
z_j = z_i + 0.1 * np.random.randn(n_dims)
z_i = z_i / np.linalg.norm(z_i)
z_j = z_j / np.linalg.norm(z_j)
sim = np.dot(z_i, z_j)

img_flat = np.sin(np.linspace(0, 4*np.pi, 256))
recon_flat = img_flat + 0.2 * np.random.randn(256)

temperatures = np.logspace(-1, 1, 20)
losses_sim = []
for t in temperatures:
    z_i_n = z_i / np.linalg.norm(z_i)
    z_j_n = z_j / np.linalg.norm(z_j)
    pos = np.exp(np.dot(z_i_n, z_j_n) / t)
    neg = 0
    for _ in range(50):
        z_k = np.random.randn(n_dims)
        z_k = z_k / np.linalg.norm(z_k)
        neg += np.exp(np.dot(z_i_n, z_k) / t)
    losses_sim.append(-np.log(pos / (pos + neg)))

fig, axes = plt.subplots(2, 3, figsize=(14, 9))

axes[0, 0].plot(temperatures, losses_sim, "o-", lw=2)
axes[0, 0].axvline(0.5, color="r", ls="--", label="τ=0.5")
axes[0, 0].set_xlabel("Temperature τ")
axes[0, 0].set_ylabel("NT-Xent loss")
axes[0, 0].set_xscale("log")
axes[0, 0].set_title("SimCLR: Contrastive Loss vs τ\n"
                     "Low τ → hard negative emphasis")
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

mask_ratios = np.linspace(0.1, 0.9, 20)
losses_mae = []
for mr in mask_ratios:
    losses_mae.append(mae_loss(img_flat, recon_flat, mask_ratio=mr))
axes[0, 1].plot(mask_ratios, losses_mae, "o-", lw=2)
axes[0, 1].axvline(0.75, color="r", ls="--", label="75% mask (MAE)")
axes[0, 1].set_xlabel("Mask ratio")
axes[0, 1].set_ylabel("Reconstruction loss (MSE)")
axes[0, 1].set_title("MAE: Loss vs Mask Ratio")
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

batch_sizes = [32, 64, 128, 256, 512, 1024]
losses_bs = []
for bs in batch_sizes:
    z_batch = np.random.randn(bs, 64)
    z_batch = z_batch / np.linalg.norm(z_batch, axis=1, keepdims=True)
    pos_sim = np.mean(np.sum(z_batch * z_batch[::-1], axis=1))
    loss_bs = -np.log(np.exp(pos_sim / 0.5) / (np.exp(pos_sim / 0.5) + bs * np.exp(0.1 / 0.5)))
    losses_bs.append(loss_bs)
axes[0, 2].plot(batch_sizes, losses_bs, "o-", lw=2)
axes[0, 2].set_xlabel("Batch size")
axes[0, 2].set_ylabel("Contrastive loss")
axes[0, 2].set_title("SimCLR: Loss vs Batch Size\n(larger batch → more negatives)")
axes[0, 2].grid(True, alpha=0.3)

aug_strengths = np.linspace(0, 1, 20)
sims = []
for a in aug_strengths:
    z1 = np.random.randn(128)
    z2 = z1 + a * np.random.randn(128)
    z1 /= np.linalg.norm(z1)
    z2 /= np.linalg.norm(z2)
    sims.append(np.dot(z1, z2))
axes[1, 0].plot(aug_strengths, sims, "o-", lw=2)
axes[1, 0].set_xlabel("Augmentation strength")
axes[1, 0].set_ylabel("Positive pair similarity")
axes[1, 0].set_title("Augmentation Design\n(positive pairs should be similar)")
axes[1, 0].grid(True, alpha=0.3)

repr_dims = [16, 32, 64, 128, 256, 512]
alignments, uniformities = [], []
for d in repr_dims:
    pos = np.random.randn(1000, d)
    pos = pos / np.linalg.norm(pos, axis=1, keepdims=True)
    pos_sim = np.mean([np.dot(pos[i], pos[i+1]) for i in range(0, 999, 2)])
    neg = np.random.randn(1000, d)
    neg = neg / np.linalg.norm(neg, axis=1, keepdims=True)
    neg_sim = np.mean([np.dot(neg[i], neg[j])
                      for i in range(100) for j in range(i+1, 100)])
    alignments.append(pos_sim)
    uniformities.append(neg_sim)
axes[1, 1].plot(repr_dims, alignments, "o-", lw=2, label="Alignment")
axes[1, 1].plot(repr_dims, uniformities, "s-", lw=2, label="Uniformity")
axes[1, 1].set_xlabel("Representation dimension")
axes[1, 1].set_ylabel("Metric")
axes[1, 1].set_title("Alignment & Uniformity\n(contrastive learning)")
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

n_negatives_range = [1, 5, 10, 50, 100, 500, 1000]
loss_neg = []
for n_neg in n_negatives_range:
    pos_s = np.dot(z_i, z_j) / 0.5
    neg_s_total = 0
    for _ in range(n_neg):
        z_k = np.random.randn(n_dims)
        z_k /= np.linalg.norm(z_k)
        neg_s_total += np.exp(np.dot(z_i, z_k) / 0.5)
    loss_neg.append(-np.log(np.exp(pos_s) / (np.exp(pos_s) + neg_s_total)))
axes[1, 2].plot(n_negatives_range, loss_neg, "o-", lw=2)
axes[1, 2].set_xlabel("Number of negatives")
axes[1, 2].set_ylabel("Contrastive loss")
axes[1, 2].set_xscale("log")
axes[1, 2].set_title("Effect of Negative Samples")
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("../../assets/phase08/08-self-supervised-vision.png")
plt.close()

print("=" * 60)
print("SELF-SUPERVISED VISION")
print("=" * 60)
print(f"\nSimCLR characteristics:")
print(f"  Positive pair similarity: {sim:.4f}")
print(f"  Optimal temp τ: ~0.5 (InfoNCE bound)")
print(f"  Batch size: larger batches → more negatives")

print(f"\nMAE (Masked Autoencoder):")
print(f"  Mask ratio: 75% (removes most patches)")
print(f"  Asymmetric encoder-decoder design")
print(f"  Decoder only processes visible patches")

print(f"\nKey methods:")
print(f"  • SimCLR: contrastive learning (augment + match)")
print(f"  • MAE: masked image modeling (BERT for vision)")
print(f"  • DINO: self-distillation w/ momentum encoder")
print(f"  • BYOL: no negatives, only positive pairs")
print(f"\nProperties of good representations:")
print(f"  • Alignment: positive pairs should be close")
print(f"  • Uniformity: distribution on hypersphere")
