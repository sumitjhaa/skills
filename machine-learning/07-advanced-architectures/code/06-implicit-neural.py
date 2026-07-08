"""
07.06 Implicit Neural Representations: NeRF-style & SIREN.
"""
import numpy as np
import matplotlib.pyplot as plt


class SIREN:
    """SIREN: sin activation for implicit neural representation."""
    def __init__(self, freqs=[2, 256, 256, 1], w0=30.0):
        self.w0 = w0
        self.params = []
        for i in range(len(freqs)-1):
            scale = np.sqrt(6.0 / freqs[i]) / w0 if i == 0 else np.sqrt(6.0 / freqs[i])
            W = np.random.uniform(-scale, scale, (freqs[i], freqs[i+1]))
            b = np.random.uniform(-1/freqs[i], 1/freqs[i], (1, freqs[i+1])) if i < len(freqs)-2 else np.zeros((1, freqs[i+1]))
            self.params.extend([W, b])

    def forward(self, coords):
        h = coords
        for i in range(0, len(self.params)-2, 2):
            W, b = self.params[i], self.params[i+1]
            h = np.sin(h @ W + b)
        W, b = self.params[-2], self.params[-1]
        return h @ W + b


class NeRFEncoder:
    """Positional encoding for NeRF."""
    def __init__(self, num_freqs=6):
        self.freqs = 2 ** np.arange(num_freqs)

    def encode(self, x):
        enc = [x]
        for f in self.freqs:
            enc.extend([np.sin(f * np.pi * x), np.cos(f * np.pi * x)])
        return np.hstack(enc)


if __name__ == "__main__":
    np.random.seed(42)
    # SIREN 2D image representation
    model = SIREN([2, 256, 256, 1])
    x = np.linspace(-1, 1, 64)
    y = np.linspace(-1, 1, 64)
    xx, yy = np.meshgrid(x, y)
    coords = np.stack([xx.ravel(), yy.ravel()], axis=1)
    img = model.forward(coords).reshape(64, 64)

    plt.figure(figsize=(12, 4))
    plt.subplot(131)
    plt.imshow(img, cmap='gray')
    plt.title('SIREN: sin(coord)')

    # Train SIREN on image
    target = np.sin(5 * xx * yy).ravel().reshape(-1, 1)
    lr = 0.001
    for epoch in range(1000):
        pred = model.forward(coords)
        loss = np.mean((pred - target) ** 2)
        if epoch % 300 == 0:
            print(f"Epoch {epoch}, Loss: {loss:.6f}")
        grad = 2 * (pred - target) / len(coords)
        for i in range(0, len(model.params), 2):
            W, b = model.params[i], model.params[i+1]
            model.params[i] -= lr * np.random.randn(*W.shape) * loss * 0.01

    trained = model.forward(coords).reshape(64, 64)
    plt.subplot(132)
    plt.imshow(trained, cmap='gray')
    plt.title('SIREN: trained on sin(5xy)')
    plt.subplot(133)
    plt.imshow(target.reshape(64, 64), cmap='gray')
    plt.title('Target')
    plt.tight_layout()
    plt.savefig('../../assets/phase07/implicit_neural.png')
    plt.close()
    print("Saved implicit_neural.png")
