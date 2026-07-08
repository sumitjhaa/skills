"""
09.02 Tokenization — BPE Tokenizer from scratch
Built with only numpy, scipy, matplotlib.
"""
import re
from collections import defaultdict


def get_stats(vocab):
    """Count frequency of adjacent symbol pairs."""
    pairs = defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i + 1]] += freq
    return pairs


def merge_vocab(pair, vocab):
    """Replace all occurrences of pair in vocabulary with merged symbol."""
    new_vocab = {}
    bigram = " ".join(pair)
    replacement = "".join(pair)
    for word, freq in vocab.items():
        new_word = word.replace(bigram, replacement)
        new_vocab[new_word] = freq
    return new_vocab


class BPETokenizer:
    """Byte-Pair Encoding tokenizer trained from scratch."""

    def __init__(self, num_merges=100):
        self.num_merges = num_merges
        self.merges = {}
        self.vocab = None

    def _get_word_vocab(self, corpus):
        """Split words into characters and count frequencies."""
        vocab = {}
        for sentence in corpus:
            for word in sentence.strip().split():
                word = " ".join(list(word)) + " </w>"
                vocab[word] = vocab.get(word, 0) + 1
        return vocab

    def fit(self, corpus):
        vocab = self._get_word_vocab(corpus)
        merges = {}
        for i in range(self.num_merges):
            pairs = get_stats(vocab)
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            merges[best] = i
            vocab = merge_vocab(best, vocab)
        self.merges = merges
        self.vocab = vocab
        return self

    def encode(self, text):
        word = " ".join(list(text)) + " </w>"
        while True:
            pairs = get_stats({word: 1})
            if not pairs:
                break
            # Apply learned merges in order
            mergeable = {p: self.merges.get(p, float("inf")) for p in pairs}
            min_rank = min(mergeable.values())
            if min_rank == float("inf"):
                break
            best = min(pairs, key=lambda p: self.merges.get(p, float("inf")))
            word = word.replace(" ".join(best), "".join(best))
        return word.split()


if __name__ == "__main__":
    corpus = [
        "the cat sat on the mat",
        "the bat flew over the cat",
        "a cat and a bat sat on the mat",
        "the data is categorical",
    ]
    tokenizer = BPETokenizer(num_merges=20)
    tokenizer.fit(corpus)

    test = "categorical data"
    tokens = tokenizer.encode(test)
    print(f"Input: {test}")
    print(f"Tokens: {tokens}")
    print(f"Merges learned: {len(tokenizer.merges)}")
