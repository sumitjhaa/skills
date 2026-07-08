"""
07.28 Contrastive Learning: SimCLR-style with InfoNCE loss.
"""
import numpy as np
import matplotlib.pyplot as plt


class Encoder:
    def __init__(self, in_dim=8, out_dim=4):
        self.W1 = np.random.randn(in_dim, 32) * 0.1
        self.b1 = np.zeros(32)
        self.W2 = np.random.randn(32, out_dim) * 0.1
        self.b2 = np.zeros(out_dim)

    def forward(self, x):
        h = np.tanh(x @ self.W1 + self.b1)
        return h @ self.W2 + self.b2


class ProjectionHead:
    def __init__(self, in_dim=4, out_dim=4):
        self.W = np.random.randn(in_dim, out_dim) * 0.1
        self.b = np.zeros(out_dim)

    def forward(self, h):
        return h @ self.W + self.b


def info_nce_loss(z, temperature=0.5):
    """InfoNCE loss with batched negatives."""
    z = z / (np.linalg.norm(z, axis=-1, keepdims=True) + 1e-8)
    sim = z @ z.T
    pos_mask = np.eye(len(z), dtype=bool)
    pos_sim = sim[pos_mask].reshape(-1, 1)
    neg_sim = sim[~pos_mask].reshape(len(z), -1)
    logits = np.hstack([pos_sim, neg_sim]) / temperature
    labels = np.zeros(len(z), dtype=int)
    exp_logits = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
    probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)
    return -np.mean(np.log(probs[np.arange(len(z)), labels] + 1e-8))


class SimCLR:
    def __init__(self, in_dim=8, proj_dim=4):
        self.encoder = Encoder(in_dim, proj_dim)
        self.projector = ProjectionHead(proj_dim, proj_dim)

    def forward(self, x):
        h = self.encoder.forward(x)
        z = self.projector.forward(h)
        return z

    def augment(self, x):
        noise = np.random.randn(*x.shape) * 0.1
        return x + noise


if __name__ == "__main__":
    np.random.seed(42)
    model = SimCLR(in_dim=8, proj_dim=4)
    batch = 64
    x = np.random.randn(batch, 8)
    x_aug = model.augment(x)
    z = model.forward(np.vstack([x, x_aug]))
    loss = info_nce_loss(z, temperature=0.5)
    print(f"InfoNCE loss: {loss:.4f}")

    x_new = np.random.randn(100, 8)
    z_new = model.forward(x_new)

    plt.figure(figsize=(10, 4))
    plt.subplot(121)
    plt.scatter(z_new[:50, 0], z_new[:50, 1], alpha=0.5, label='Class 1')
    plt.scatter(z_new[50:, 0], z_new[50:, 1], alpha=0.5, label='Class 2')
    plt.legend()
    plt.title('Contrastive embeddings')
    plt.subplot(122)
    sim_matrix = z_new @ z_new.T
    plt.imshow(sim_matrix, cmap='RdBu', vmin=-1, vmax=1)
    plt.colorbar()
    plt.title('Similarity matrix')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/contrastive_learning.png')
    plt.close()
    print("Saved contrastive_learning.png")
