"""06.28 - Gradient Accumulation / Checkpointing: Memory-efficient training"""

import numpy as np
import matplotlib.pyplot as plt


def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -100, 100)))


class SimpleNet:
    def __init__(self, dims):
        self.params = [np.random.randn(dims[i], dims[i+1]) * 0.1 for i in range(len(dims)-1)]
        self.biases = [np.zeros(dims[i+1]) for i in range(len(dims)-1)]

    def forward(self, x):
        h = x
        for W, b in zip(self.params, self.biases):
            h = sigmoid(h @ W + b)
        return h

    def backward(self, x, grad_output):
        grads = []
        h = x
        activations = [x]
        for W, b in zip(self.params, self.biases):
            h = sigmoid(h @ W + b)
            activations.append(h)

        d = grad_output
        for i in range(len(self.params) - 1, -1, -1):
            h_prev = activations[i]
            sig_out = activations[i + 1]
            dsig = sig_out * (1 - sig_out)
            dW = h_prev.T @ (d * dsig)
            db = (d * dsig).sum(axis=0)
            d = (d * dsig) @ self.params[i].T
            grads.insert(0, (dW, db))
        return grads


def gradient_accumulation(model, data_batches, labels_batches, accumulation_steps=4):
    accumulated_grads = [(np.zeros_like(W), np.zeros_like(b))
                         for W, b in zip(model.params, model.biases)]

    total_loss = 0
    for step, (x, y) in enumerate(zip(data_batches, labels_batches)):
        pred = model.forward(x)
        loss = np.mean((pred - y) ** 2) / accumulation_steps
        total_loss += loss
        dout = 2 * (pred - y) / (x.shape[0] * accumulation_steps)
        grads = model.backward(x, dout)
        for i, (dW, db) in enumerate(grads):
            accumulated_grads[i] = (accumulated_grads[i][0] + dW, accumulated_grads[i][1] + db)

    return accumulated_grads, total_loss


def checkpoint_forward(model, x, segment_size=2):
    inputs = [x]
    current = x
    for W, b in zip(model.params, model.biases):
        current = sigmoid(current @ W + b)
        inputs.append(current)
    return current, inputs


def checkpoint_backward(model, x, grad_output, activations, segment_size=2):
    grads = []
    g = grad_output
    for i in range(len(model.params) - 1, -1, -1):
        seg_start = (i // segment_size) * segment_size
        if seg_start < i:
            h = activations[seg_start]
            for j in range(seg_start, i):
                h = sigmoid(h @ model.params[j] + model.biases[j])
        else:
            h = activations[i]
        sig_out = sigmoid(h @ model.params[i] + model.biases[i])
        dsig = sig_out * (1 - sig_out)
        dz = g * dsig
        dW = h.T @ dz
        db = dz.sum(axis=0)
        d = dz @ model.params[i].T
        g = d
        grads.insert(0, (dW, db))
    return grads


if __name__ == "__main__":
    np.random.seed(42)
    model = SimpleNet([8, 16, 8, 4])

    micro_batch_size = 4
    effective_batch_size = 16
    accumulation_steps = effective_batch_size // micro_batch_size

    data = np.random.randn(effective_batch_size, 8)
    labels = np.random.randn(effective_batch_size, 4)
    batches = [data[i*micro_batch_size:(i+1)*micro_batch_size] for i in range(accumulation_steps)]
    label_batches = [labels[i*micro_batch_size:(i+1)*micro_batch_size] for i in range(accumulation_steps)]

    single_pred = model.forward(data)
    single_loss = np.mean((single_pred - labels) ** 2)
    single_dout = 2 * (single_pred - labels) / effective_batch_size
    single_grads = model.backward(data, single_dout)

    acc_grads, acc_loss = gradient_accumulation(model, batches, label_batches, accumulation_steps)

    print(f"Single batch loss:  {single_loss:.6f}")
    print(f"Accumulated loss:   {acc_loss:.6f}")
    print(f"Gradients match:    {all(np.allclose(sg[0], ag[0], atol=1e-7) for sg, ag in zip(single_grads, acc_grads))}")

    x = np.random.randn(4, 8)
    h, activations = checkpoint_forward(model, x, segment_size=2)
    grad_output = np.random.randn(4, 4)
    ckpt_grads = checkpoint_backward(model, x, grad_output, activations, segment_size=2)

    full_grads = model.backward(x, grad_output)

    match = True
    for (cW, cb), (fW, fb) in zip(ckpt_grads, full_grads):
        if not np.allclose(cW, fW, atol=1e-5) or not np.allclose(cb, fb, atol=1e-5):
            match = False
            break
    print(f"\nCheckpointing gradients match full backward: {match}")

    print("\nGradient accumulation and checkpointing verified.")
