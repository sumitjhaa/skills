"""
09.06 Multilingual NLP — SentencePiece-style tokenizer & embedding alignment
Built with only numpy, scipy, matplotlib.
"""
import numpy as np
from collections import Counter
import re


class MultilingualTokenizer:
    """Simple character + subword tokenizer for multiple scripts."""

    def __init__(self, vocab_size=500):
        self.vocab_size = vocab_size
        self.char_counts = Counter()
        self.vocab = {}

    def _extract_chars(self, text):
        return list(set(text.lower()))

    def fit(self, texts):
        chars = Counter()
        for t in texts:
            chars.update(list(t.lower()))
        # Keep top characters
        top = chars.most_common(self.vocab_size)
        self.vocab = {c: i for i, (c, _) in enumerate(top)}

    def encode(self, text):
        return [self.vocab.get(c, self.vocab.get('<unk>', 0)) for c in text.lower() if c in self.vocab]

    def decode(self, ids, idx2char=None):
        if idx2char is None:
            idx2char = {i: c for c, i in self.vocab.items()}
        return "".join(idx2char.get(i, '?') for i in ids)


def align_embeddings(src_embs, tgt_embs, num_iter=100):
    """Simple orthogonal Procrustes alignment between two embedding spaces."""
    # src_embs: (V1, d), tgt_embs: (V2, d)
    # Find rotation matrix W to align src to tgt
    U, _, Vt = np.linalg.svd(src_embs.T @ tgt_embs[:len(src_embs)], full_matrices=False)
    W = U @ Vt
    aligned = src_embs @ W
    return aligned, W


if __name__ == "__main__":
    tokenizer = MultilingualTokenizer(vocab_size=100)

    texts_en = ["hello world", "the cat sat", "natural language processing"]
    texts_zh = ["你好世界", "猫坐在地上", "自然语言处理"]
    texts_es = ["hola mundo", "el gato se sienta", "procesamiento del lenguaje"]

    tokenizer.fit(texts_en + texts_zh + texts_es)

    for text in texts_zh[:2]:
        ids = tokenizer.encode(text)
        print(f"'{text}' -> {ids}")

    # Embedding alignment simulation
    d = 8
    V_en, V_zh = 10, 10
    en_embs = np.random.randn(V_en, d)
    zh_embs = np.random.randn(V_zh, d)

    aligned_zh, W = align_embeddings(zh_embs[:V_en], en_embs)
    print(f"\nEmbedding alignment: src={en_embs.shape}, tgt={zh_embs.shape}")
    print(f"Aligned shape: {aligned_zh.shape}")
    print(f"Frobenius error: {np.linalg.norm(aligned_zh - en_embs):.4f}")
