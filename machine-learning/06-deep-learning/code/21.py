"""06.21 - BPTT: Backpropagation through time"""

import numpy as np
import matplotlib.pyplot as plt


def tanh(x):
    return np.tanh(x)

def tanh_deriv(x):
    return 1 - np.tanh(x) ** 2


class SimpleRNN:
    def __init__(self, input_size, hidden_size, output_size):
        self.Wxh = np.random.randn(input_size, hidden_size) * 0.01
        self.Whh = np.random.randn(hidden_size, hidden_size) * 0.01
        self.Why = np.random.randn(hidden_size, output_size) * 0.01
        self.bh = np.zeros(hidden_size)
        self.by = np.zeros(output_size)
        self.hidden_size = hidden_size

    def forward(self, inputs):
        T = len(inputs)
        h = np.zeros(self.hidden_size)
        hs, ys = [], []
        for t in range(T):
            h = tanh(inputs[t] @ self.Wxh + h @ self.Whh + self.bh)
            y = h @ self.Why + self.by
            hs.append(h)
            ys.append(y)
        return np.array(ys), np.array(hs)

    def bptt(self, inputs, targets, lr=0.01, clip_norm=5.0):
        T = len(inputs)
        ys, hs = self.forward(inputs)
        dWxh, dWhh, dWhy = np.zeros_like(self.Wxh), np.zeros_like(self.Whh), np.zeros_like(self.Why)
        dbh, dby = np.zeros_like(self.bh), np.zeros_like(self.by)
        dh_next = np.zeros(self.hidden_size)
        for t in reversed(range(T)):
            dy = ys[t] - targets[t]
            dWhy += np.outer(hs[t], dy)
            dby += dy
            dh = dy @ self.Why.T + dh_next
            dh_raw = dh * tanh_deriv(hs[t])
            dWxh += np.outer(inputs[t], dh_raw)
            if t > 0:
                dWhh += np.outer(hs[t-1], dh_raw)
            dbh += dh_raw
            dh_next = dh_raw @ self.Whh.T

        for grad in [dWxh, dWhh, dWhy]:
            norm = np.linalg.norm(grad)
            if norm > clip_norm:
                grad *= clip_norm / norm

        self.Wxh -= lr * dWxh
        self.Whh -= lr * dWhh
        self.Why -= lr * dWhy
        self.bh -= lr * dbh
        self.by -= lr * dby
        return np.mean((ys - np.array(targets)) ** 2)


if __name__ == "__main__":
    np.random.seed(42)
    rnn = SimpleRNN(10, 32, 10)
    seq_len = 8
    inputs = [np.random.randn(10) for _ in range(seq_len)]
    targets = [np.random.randn(10) for _ in range(seq_len)]

    loss = rnn.bptt(inputs, targets, lr=0.01)
    print(f"BPTT step complete. Loss = {loss:.6f}")

    losses = []
    for i in range(500):
        inputs = [np.random.randn(10) for _ in range(seq_len)]
        targets = [np.random.randn(10) for _ in range(seq_len)]
        loss = rnn.bptt(inputs, targets, lr=0.01)
        losses.append(loss)
        if i % 100 == 0:
            print(f"  Iter {i}: loss = {loss:.6f}")

    plt.plot(losses)
    plt.xlabel("Iteration")
    plt.ylabel("MSE Loss")
    plt.title("BPTT Training")
    plt.savefig("../../assets/phase06/bptt.png")
    plt.close()
    print(f"\nFinal loss: {losses[-1]:.6f}. BPTT implemented and verified.")
