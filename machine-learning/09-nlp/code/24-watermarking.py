"""
09.24 Watermarking — Red-Green List Statistical Watermark
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


class Watermarker:
    """
    Statistical watermark using red-green list split.
    """

    def __init__(self, vocab_size=1000, green_ratio=0.5, key=42):
        self.vocab_size = vocab_size
        self.green_ratio = green_ratio
        self.rng = np.random.RandomState(key)
        self.green_set = None

    def _partition(self, prefix_tokens=None):
        """Partition vocab into red and green lists."""
        if prefix_tokens is None:
            self.rng = np.random.RandomState(42)
        self.green_set = set(
            self.rng.choice(self.vocab_size, size=int(self.vocab_size * self.green_ratio), replace=False)
        )

    def generate_with_watermark(self, length=20):
        """Generate biased toward green tokens (simulated)."""
        tokens = []
        for _ in range(length):
            self._partition(tokens)
            logits = np.random.randn(self.vocab_size)
            # Bias toward green tokens
            for i in range(self.vocab_size):
                if i in self.green_set:
                    logits[i] += 2.0
            probs = np.exp(logits - logits.max())
            probs = probs / probs.sum()
            token = np.random.choice(self.vocab_size, p=probs)
            tokens.append(token)
        return tokens

    def detect(self, tokens):
        """Statistical test: count green tokens."""
        green_count = 0
        total = len(tokens)
        for t in tokens:
            self._partition()
            if t in self.green_set:
                green_count += 1
        expected_green = total * self.green_ratio
        z = (green_count - expected_green) / np.sqrt(total * self.green_ratio * (1 - self.green_ratio))
        return z, green_count / total


if __name__ == "__main__":
    watermarker = Watermarker(vocab_size=1000, green_ratio=0.5, key=42)

    # Generate watermarked text
    watermarked = watermarker.generate_with_watermark(length=50)
    z_score, green_prop = watermarker.detect(watermarked)
    print(f"Watermarked sequence: {len(watermarked)} tokens")
    print(f"Green token proportion: {green_prop:.3f} (expected 0.5)")
    print(f"Z-score: {z_score:.2f}")

    # Random (non-watermarked) text
    random_tokens = np.random.randint(0, 1000, size=50).tolist()
    z_random, green_random = watermarker.detect(random_tokens)
    print(f"\nRandom text green proportion: {green_random:.3f}")
    print(f"Z-score: {z_random:.2f}")

    # Detection
    threshold = 4.0
    print(f"\nWatermarked detected (z>{threshold}): {z_score > threshold}")
    print(f"Random detected (z>{threshold}):        {z_random > threshold}")
