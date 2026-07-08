"""06.30 - Loss Symmetries: Label smoothing, margin, contrastive, triplet"""

import numpy as np
import matplotlib.pyplot as plt


def softmax(x, axis=-1):
    e_x = np.exp(x - x.max(axis=axis, keepdims=True))
    return e_x / e_x.sum(axis=axis, keepdims=True)


def label_smoothing(labels, num_classes, epsilon=0.1):
    smooth = np.full((len(labels), num_classes), epsilon / num_classes)
    smooth[np.arange(len(labels)), labels] = 1 - epsilon
    return smooth


def smoothed_cross_entropy(logits, smooth_labels):
    log_probs = np.log(softmax(logits) + 1e-12)
    return -np.mean(np.sum(smooth_labels * log_probs, axis=1))


def multi_margin_loss(scores, labels, margin=1.0):
    batch_size, num_classes = scores.shape
    correct_scores = scores[np.arange(batch_size), labels]
    margins = np.maximum(0, scores - correct_scores[:, None] + margin)
    margins[np.arange(batch_size), labels] = 0
    return np.mean(margins.sum(axis=1))


def contrastive_loss(distances, labels, margin=1.0):
    similar = labels
    dissimilar = 1 - labels
    loss = similar * distances ** 2 + dissimilar * np.maximum(0, margin - distances) ** 2
    return np.mean(loss)


def triplet_loss(anchor, positive, negative, margin=1.0):
    d_pos = np.linalg.norm(anchor - positive, axis=1)
    d_neg = np.linalg.norm(anchor - negative, axis=1)
    loss = np.maximum(0, d_pos - d_neg + margin)
    return np.mean(loss)


def hard_triplet_mining(embeddings, labels, margin=1.0):
    batch_size = len(embeddings)
    losses = []
    for i in range(batch_size):
        pos_mask = labels == labels[i]
        neg_mask = ~pos_mask
        pos_mask[i] = False
        if not pos_mask.any() or not neg_mask.any():
            continue
        anchor = embeddings[i]
        hardest_pos_idx = np.argmax(np.linalg.norm(embeddings[pos_mask] - anchor, axis=1))
        hardest_neg_idx = np.argmin(np.linalg.norm(embeddings[neg_mask] - anchor, axis=1))
        pos_idx = np.where(pos_mask)[0][hardest_pos_idx]
        neg_idx = np.where(neg_mask)[0][hardest_neg_idx]
        loss = max(0, np.linalg.norm(anchor - embeddings[pos_idx]) -
                   np.linalg.norm(anchor - embeddings[neg_idx]) + margin)
        losses.append(loss)
    return np.mean(losses) if losses else 0.0


def info_nce_loss(embeddings, temperature=0.1):
    batch_size = len(embeddings)
    sim = embeddings @ embeddings.T / temperature
    labels = np.arange(batch_size)
    pos_mask = np.eye(batch_size, dtype=bool)
    neg_mask = ~pos_mask
    exp_sim = np.exp(sim - sim.max(axis=1, keepdims=True))
    pos = exp_sim[pos_mask]
    neg_sum = exp_sim @ (1.0 - np.eye(batch_size, dtype=float))
    loss = -np.mean(np.log(pos / (pos + neg_sum) + 1e-12))
    return loss


if __name__ == "__main__":
    np.random.seed(42)
    batch_size, num_classes = 8, 10

    logits = np.random.randn(batch_size, num_classes)
    labels = np.random.randint(0, num_classes, batch_size)

    smooth_labels = label_smoothing(labels, num_classes, epsilon=0.1)
    ce = smoothed_cross_entropy(logits, smooth_labels)
    raw_ce = -np.mean(np.log(softmax(logits)[np.arange(batch_size), labels] + 1e-12))
    print(f"Raw cross-entropy:        {raw_ce:.4f}")
    print(f"Smoothed cross-entropy:   {ce:.4f}")

    margin = multi_margin_loss(logits, labels, margin=1.0)
    print(f"Multi-margin loss:        {margin:.4f}")

    embeddings = np.random.randn(batch_size, 16)
    embed_labels = np.array([0, 0, 0, 1, 1, 1, 2, 2])
    distances = np.linalg.norm(embeddings[:4] - embeddings[4:8], axis=1)
    pair_labels = np.array([0, 0, 0, 1])
    cl = contrastive_loss(distances[:4], pair_labels, margin=1.0)
    print(f"Contrastive loss:         {cl:.4f}")

    tl = triplet_loss(embeddings[0:1], embeddings[1:2], embeddings[3:4], margin=1.0)
    print(f"Triplet loss:             {tl:.4f}")

    ht = hard_triplet_mining(embeddings, embed_labels, margin=1.0)
    print(f"Hard triplet mining:      {ht:.4f}")

    nce = info_nce_loss(embeddings, temperature=0.1)
    print(f"InfoNCE loss:             {nce:.4f}")

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    smooth_levels = np.linspace(0, 0.5, 20)
    for ax, fn, title in [
        (axes[0, 0], lambda e: smoothed_cross_entropy(logits, label_smoothing(labels, num_classes, e)),
         "Label Smoothing Sensitivity"),
        (axes[0, 1], lambda m: multi_margin_loss(logits, labels, m), "Margin Sensitivity"),
        (axes[0, 2], lambda t: info_nce_loss(embeddings, t), "InfoNCE Temperature"),
    ]:
        vals = [fn(s) for s in smooth_levels]
        ax.plot(smooth_levels, vals)
        ax.set_xlabel("Parameter")
        ax.set_title(title)
        ax.grid(True, alpha=0.3)

    axes[1, 0].axis("off"); axes[1, 1].axis("off"); axes[1, 2].axis("off")
    plt.tight_layout()
    plt.savefig("../../assets/phase06/loss_symmetries.png")
    plt.close()
    print("\nAll loss symmetry techniques implemented.")
