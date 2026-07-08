"""06.32 - Full Training Pipeline: End-to-end training with all components"""

import numpy as np
import time


def softmax(x):
    e_x = np.exp(x - x.max(axis=1, keepdims=True))
    return e_x / e_x.sum(axis=1, keepdims=True)

def cross_entropy(logits, labels):
    probs = softmax(logits)
    return -np.mean(np.log(probs[np.arange(len(labels)), labels] + 1e-12))


class LayerNorm:
    def __init__(self, dim):
        self.gamma = np.ones(dim)
        self.beta = np.zeros(dim)

    def forward(self, x):
        mu = x.mean(axis=1, keepdims=True)
        v = x.var(axis=1, keepdims=True)
        return self.gamma * (x - mu) / np.sqrt(v + 1e-5) + self.beta


class SimpleCNN:
    def __init__(self, use_bn=True, dropout_rate=0.0, label_smoothing=0.0):
        self.conv1 = (np.random.randn(16, 3, 3, 3) * 0.1, np.zeros(16))
        self.conv2 = (np.random.randn(32, 16, 3, 3) * 0.1, np.zeros(32))
        self.fc1 = (np.random.randn(32 * 8 * 8, 128) * 0.01, np.zeros(128))
        self.fc2 = (np.random.randn(128, 10) * 0.01, np.zeros(10))
        self.use_bn = use_bn
        self.dropout_rate = dropout_rate
        self.label_smoothing = label_smoothing
        if use_bn:
            self.bn1 = LayerNorm(16)
            self.bn2 = LayerNorm(32)

    def forward(self, x):
        x = np.maximum(0, self._conv2d(x, *self.conv1, pad=1))
        if self.use_bn:
            x = self.bn1.forward(x.transpose(0, 2, 3, 1)).transpose(0, 3, 1, 2)
        x = self._max_pool(x, 2, 2)
        x = np.maximum(0, self._conv2d(x, *self.conv2, pad=1))
        if self.use_bn:
            x = self.bn2.forward(x.transpose(0, 2, 3, 1)).transpose(0, 3, 1, 2)
        x = self._max_pool(x, 2, 2)
        x = x.reshape(x.shape[0], -1)
        x = np.maximum(0, x @ self.fc1[0] + self.fc1[1])
        if self.dropout_rate > 0:
            mask = np.random.binomial(1, 1 - self.dropout_rate, x.shape) / (1 - self.dropout_rate)
            x = x * mask
        x = x @ self.fc2[0] + self.fc2[1]
        return x

    def _conv2d(self, x, W, b, stride=1, pad=0):
        N, C, H, Win = x.shape
        K, _, k_h, k_w = W.shape
        H_out = (H + 2*pad - k_h)//stride + 1
        W_out = (Win + 2*pad - k_w)//stride + 1
        x_pad = np.pad(x, ((0,0),(0,0),(pad,pad),(pad,pad)), mode="constant")
        cols = np.zeros((N, C, k_h, k_w, H_out, W_out))
        for i in range(k_h):
            for j in range(k_w):
                cols[:, :, i, j, :, :] = x_pad[:, :, i:i+H_out*stride:stride, j:j+W_out*stride:stride]
        cols = cols.reshape(N, C*k_h*k_w, H_out*W_out).transpose(0, 2, 1)
        out = cols @ W.reshape(K, -1).T
        return out.reshape(N, H_out, W_out, K).transpose(0, 3, 1, 2) + b.reshape(1, -1, 1, 1)

    def _max_pool(self, x, pool=2, stride=2):
        N, C, H, W = x.shape
        H_out = (H - pool)//stride + 1
        W_out = (W - pool)//stride + 1
        out = np.zeros((N, C, H_out, W_out))
        for i in range(H_out):
            for j in range(W_out):
                out[:, :, i, j] = x[:, :, i*stride:i*stride+pool, j*stride:j*stride+pool].max(axis=(2,3))
        return out


class StepLR:
    def __init__(self, initial_lr, step_size=30, gamma=0.5):
        self.lr = initial_lr
        self.step_size = step_size
        self.gamma = gamma

    def step(self, epoch):
        self.lr = self.lr * self.gamma ** (epoch // self.step_size)
        return self.lr


class Adam:
    def __init__(self, params, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8, weight_decay=0.0):
        self.params = params
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.weight_decay = weight_decay
        self.m = [np.zeros_like(p) for p in params]
        self.v = [np.zeros_like(p) for p in params]
        self.t = 0

    def step(self, grads):
        self.t += 1
        updates = []
        for i, (p, g) in enumerate(zip(self.params, grads)):
            if self.weight_decay > 0:
                g = g + self.weight_decay * p
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * g
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * g ** 2
            m_hat = self.m[i] / (1 - self.beta1 ** self.t)
            v_hat = self.v[i] / (1 - self.beta2 ** self.t)
            updates.append(p - self.lr * m_hat / (np.sqrt(v_hat) + self.eps))
        return updates


def compute_gradients_numerical(model, x, y, eps=1e-5):
    params = [model.conv1[0], model.conv1[1], model.conv2[0], model.conv2[1],
              model.fc1[0], model.fc1[1], model.fc2[0], model.fc2[1]]
    grads = []
    original = [p.copy() for p in params]
    logits = model.forward(x)
    base_loss = cross_entropy(logits, y)
    for pi, p in enumerate(params):
        g = np.zeros_like(p)
        it = np.nditer(p, flags=["multi_index"])
        while not it.finished:
            idx = it.multi_index
            old = p[idx]
            p[idx] = old + eps
            loss_p = cross_entropy(model.forward(x), y)
            p[idx] = old - eps
            loss_m = cross_entropy(model.forward(x), y)
            g[idx] = (loss_p - loss_m) / (2 * eps)
            p[idx] = old
            it.iternext()
        grads.append(g)
    for pi, p in enumerate(params):
        p[:] = original[pi]
    return grads


if __name__ == "__main__":
    np.random.seed(42)

    print("=" * 60)
    print("06.32 - Full Training Pipeline")
    print("=" * 60)

    x_train = np.random.randn(200, 3, 32, 32) * 0.5
    y_train = np.random.randint(0, 10, 200)
    x_val = np.random.randn(50, 3, 32, 32) * 0.5
    y_val = np.random.randint(0, 10, 50)

    config = {"use_bn": True, "dropout": 0.1, "label_smoothing": 0.1, "lr": 0.01}
    model = SimpleCNN(use_bn=config["use_bn"], dropout_rate=config["dropout"],
                      label_smoothing=config["label_smoothing"])

    params = [model.conv1[0], model.conv1[1], model.conv2[0], model.conv2[1],
              model.fc1[0], model.fc1[1], model.fc2[0], model.fc2[1]]
    optimizer = Adam(params, lr=config["lr"], weight_decay=1e-4)
    scheduler = StepLR(config["lr"], step_size=20, gamma=0.5)
    clip_norm = 5.0

    history = {"train_loss": [], "val_acc": [], "lr": []}

    for epoch in range(10):
        epoch_loss = 0
        for batch_start in range(0, len(x_train), 32):
            batch_end = batch_start + 32
            x_batch = x_train[batch_start:batch_end]
            y_batch = y_train[batch_start:batch_end]

            logits = model.forward(x_batch)
            loss = cross_entropy(logits, y_batch)
            epoch_loss += loss

            probs = softmax(logits)
            dout = probs.copy()
            dout[np.arange(len(y_batch)), y_batch] -= 1
            dout /= len(y_batch)

            # compute numerical gradients for trainable params
            grads = compute_gradients_numerical(model, x_batch, y_batch)

            # gradient clipping
            total_norm = np.sqrt(sum(np.sum(g ** 2) for g in grads))
            if total_norm > clip_norm:
                for g in grads:
                    g *= clip_norm / (total_norm + 1e-6)

            updated = optimizer.step(grads)
            model.conv1 = (updated[0], updated[1])
            model.conv2 = (updated[2], updated[3])
            model.fc1 = (updated[4], updated[5])
            model.fc2 = (updated[6], updated[7])

        scheduler.step(epoch)
        current_lr = scheduler.lr

        val_logits = model.forward(x_val)
        val_preds = np.argmax(softmax(val_logits), axis=1)
        val_acc = np.mean(val_preds == y_val)

        history["train_loss"].append(epoch_loss / (len(x_train) // 32))
        history["val_acc"].append(val_acc)
        history["lr"].append(current_lr)

        print(f"Epoch {epoch+1:2d}: loss={history['train_loss'][-1]:.4f}, "
              f"val_acc={val_acc*100:.1f}%, lr={current_lr:.6f}")

    print("\n" + "=" * 60)
    print(f"Training complete. Final validation accuracy: {history['val_acc'][-1]*100:.1f}%")
    print(f"Best validation accuracy: {max(history['val_acc'])*100:.1f}%")
    print("Full training pipeline verified.")
