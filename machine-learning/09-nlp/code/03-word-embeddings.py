"""
09.03 Word Embeddings — Skip-gram Word2Vec with Negative Sampling
Built with only numpy, scipy, matplotlib.
"""
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt


class SkipGramWord2Vec:
    """Word2Vec Skip-gram with negative sampling."""

    def __init__(self, vocab_size, embedding_dim=50, lr=0.01):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.lr = lr
        # Center word embeddings (target)
        self.W_in = np.random.randn(vocab_size, embedding_dim) * 0.01
        # Context word embeddings (output)
        self.W_out = np.random.randn(vocab_size, embedding_dim) * 0.01

    def _sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-np.clip(x, -20, 20)))

    def train_step(self, center_idx, context_idx, negative_idxs):
        """Single training step for one center-context pair."""
        center_emb = self.W_in[center_idx]  # (d,)
        # Positive sample
        pos_out_emb = self.W_out[context_idx]
        pos_score = np.dot(center_emb, pos_out_emb)
        pos_pred = self._sigmoid(pos_score)
        pos_grad_out = (pos_pred - 1) * center_emb
        pos_grad_in = (pos_pred - 1) * pos_out_emb

        grad_in = pos_grad_in.copy()
        self.W_out[context_idx] -= self.lr * pos_grad_out

        # Negative samples
        for neg_idx in negative_idxs:
            neg_out_emb = self.W_out[neg_idx]
            neg_score = np.dot(center_emb, neg_out_emb)
            neg_pred = self._sigmoid(neg_score)
            neg_grad_out = neg_pred * center_emb
            neg_grad_in = neg_pred * neg_out_emb
            grad_in += neg_grad_in
            self.W_out[neg_idx] -= self.lr * neg_grad_out

        self.W_in[center_idx] -= self.lr * grad_in

    def get_embedding(self, word_idx):
        return self.W_in[word_idx]


def build_vocab(sentences, min_count=1):
    word_counts = Counter()
    for sent in sentences:
        word_counts.update(sent.lower().split())
    word_counts = {w: c for w, c in word_counts.items() if c >= min_count}
    word2idx = {w: i for i, (w, _) in enumerate(word_counts.items())}
    idx2word = {i: w for w, i in word2idx.items()}
    return word2idx, idx2word


def generate_training_data(sentences, word2idx, window=2):
    pairs = []
    for sent in sentences:
        tokens = sent.lower().split()
        indices = [word2idx[t] for t in tokens if t in word2idx]
        for i, center in enumerate(indices):
            start = max(0, i - window)
            end = min(len(indices), i + window + 1)
            for j in range(start, end):
                if j != i:
                    pairs.append((center, indices[j]))
    return pairs


def negative_sampling(center_idx, vocab_size, num_neg=5, power=0.75):
    """Simple uniform negative sampling (unigram distribution^0.75)."""
    # Simplified: uniform for demonstration
    negs = []
    while len(negs) < num_neg:
        idx = np.random.randint(0, vocab_size)
        if idx != center_idx:
            negs.append(idx)
    return negs


if __name__ == "__main__":
    sentences = [
        "the cat sat on the mat",
        "the dog sat on the log",
        "cats and dogs are pets",
        "the mat is on the floor",
        "the log is near the tree",
        "a pet is a good companion",
        "the tree has green leaves",
        "leaves fall from the tree",
    ]
    word2idx, idx2word = build_vocab(sentences)
    vocab_size = len(word2idx)
    pairs = generate_training_data(sentences, word2idx, window=2)

    model = SkipGramWord2Vec(vocab_size, embedding_dim=10, lr=0.05)
    epochs = 100

    for epoch in range(epochs):
        np.random.shuffle(pairs)
        total_loss = 0.0
        for center, context in pairs:
            negs = negative_sampling(center, vocab_size, num_neg=3)
            model.train_step(center, context, negs)

    # Plot embeddings
    embeds = np.array([model.get_embedding(i) for i in range(vocab_size)])
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(embeds[:, 0], embeds[:, 1], alpha=0.7)
    for i, word in idx2word.items():
        ax.annotate(word, (embeds[i, 0], embeds[i, 1]), fontsize=8)
    ax.set_title("Word2Vec Skip-gram Embeddings (first 2 dims)")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("../../assets/phase09/03-word-embeddings.png")
    print(f"Trained {len(pairs)} pairs over {epochs} epochs. Embeddings saved.")
