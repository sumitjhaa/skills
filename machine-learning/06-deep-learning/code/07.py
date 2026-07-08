"""06.07 - Activations: All activation functions and their derivatives"""

import numpy as np
import matplotlib.pyplot as plt


def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -100, 100)))

def sigmoid_prime(x):
    s = sigmoid(x)
    return s * (1 - s)

def tanh(x):
    return np.tanh(x)

def tanh_prime(x):
    return 1 - np.tanh(x) ** 2

def relu(x):
    return np.maximum(0, x)

def relu_prime(x):
    return (x > 0).astype(float)

def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

def leaky_relu_prime(x, alpha=0.01):
    return np.where(x > 0, 1.0, alpha)

def elu(x, alpha=1.0):
    return np.where(x > 0, x, alpha * (np.exp(x) - 1))

def elu_prime(x, alpha=1.0):
    return np.where(x > 0, 1.0, alpha * np.exp(x))

def swish(x, beta=1.0):
    return x * sigmoid(beta * x)

def swish_prime(x, beta=1.0):
    s = sigmoid(beta * x)
    return s + x * beta * s * (1 - s)

def gelu(x):
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))

def gelu_prime(x):
    c = np.sqrt(2 / np.pi)
    inner = c * (x + 0.044715 * x ** 3)
    t = np.tanh(inner)
    sech2 = 1 - t ** 2
    d_inner = c * (1 + 3 * 0.044715 * x ** 2)
    return 0.5 * (1 + t) + 0.5 * x * sech2 * d_inner


if __name__ == "__main__":
    x = np.linspace(-5, 5, 100)
    activations = {
        "Sigmoid": (sigmoid, sigmoid_prime),
        "Tanh": (tanh, tanh_prime),
        "ReLU": (relu, relu_prime),
        "Leaky ReLU": (leaky_relu, leaky_relu_prime),
        "ELU": (elu, elu_prime),
        "Swish": (swish, swish_prime),
        "GELU": (gelu, gelu_prime),
    }

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()
    for idx, (name, (f, f_prime)) in enumerate(activations.items()):
        ax = axes[idx]
        ax.plot(x, f(x), label=name, linewidth=2)
        ax.plot(x, f_prime(x), "--", label="Derivative", linewidth=2)
        ax.axhline(0, color="gray", alpha=0.3)
        ax.axvline(0, color="gray", alpha=0.3)
        ax.legend()
        ax.set_title(name)
        ax.grid(True, alpha=0.3)

    axes[7].axis("off")
    plt.tight_layout()
    plt.savefig("../../assets/phase06/activations.png")
    plt.close()

    test_x = np.array([-2.0, -0.5, 0.0, 0.5, 2.0])
    for name, (f, f_prime) in activations.items():
        vals = f(test_x)
        derivs = f_prime(test_x)
        print(f"{name:12s}: f(-2)={vals[0]:.3f}, f'(0)={derivs[2]:.3f}, f(2)={vals[4]:.3f}")
    print("\nAll activation functions implemented and plotted.")
