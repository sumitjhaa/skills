"""
09.26 Code LLMs — Fill-in-the-Middle Training Loop
Built with only numpy, scipy, matplotlib.
"""
import numpy as np


class CodeDataset:
    """Simple code dataset for FIM training."""

    def __init__(self, vocab_size=50, max_len=20):
        self.vocab_size = vocab_size
        self.max_len = max_len

    def generate_sample(self):
        """Generate a synthetic code snippet."""
        length = np.random.randint(5, self.max_len)
        tokens = np.random.randint(0, self.vocab_size, size=length).tolist()
        return tokens

    def prepare_fim(self, tokens):
        """
        Fill-in-the-Middle: split into prefix, middle, suffix.
        Returns: (prefix + sentinel + suffix + sentinel + middle) tokens.
        """
        n = len(tokens)
        split1 = n // 3
        split2 = 2 * n // 3
        prefix = tokens[:split1]
        middle = tokens[split1:split2]
        suffix = tokens[split2:]

        sentinel = self.vocab_size - 1
        fim_tokens = prefix + [sentinel] + suffix + [sentinel] + middle
        return fim_tokens


class SimpleCodeModel:
    """Simple model for code FIM training."""

    def __init__(self, vocab_size=50, d_model=16):
        self.emb = np.random.randn(vocab_size, d_model) * 0.02
        self.W = np.random.randn(d_model, vocab_size) * 0.02

    def forward(self, tokens):
        x = self.emb[tokens]
        logits = x @ self.W
        return logits

    def loss(self, logits, targets):
        log_probs = logits - np.log(np.sum(np.exp(logits), axis=-1, keepdims=True))
        return -np.mean(log_probs[np.arange(len(targets)), targets])


if __name__ == "__main__":
    dataset = CodeDataset(vocab_size=50, max_len=20)
    model = SimpleCodeModel(vocab_size=50, d_model=16)

    tokens = dataset.generate_sample()
    fim_tokens = dataset.prepare_fim(tokens)

    # Predict the middle part
    prefix_len = len(fim_tokens) - len(tokens) // 3
    input_tokens = fim_tokens[:prefix_len]
    target_tokens = fim_tokens[prefix_len:]

    logits = model.forward(input_tokens)
    l = model.loss(logits, target_tokens)

    print(f"Original tokens:   {tokens}")
    print(f"FIM format length: {len(fim_tokens)}")
    print(f"Input length:      {len(input_tokens)}")
    print(f"Target length:     {len(target_tokens)}")
    print(f"Loss:              {l:.4f}")
    print("FIM training teaches model to infill code.")
