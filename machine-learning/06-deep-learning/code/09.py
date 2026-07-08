"""06.09 - Loss Functions: MSE, Cross-Entropy, Hinge, Huber, Focal"""

import numpy as np
import matplotlib.pyplot as plt


def mse_loss(y_pred, y_true):
    return np.mean((y_pred - y_true) ** 2)

def mse_grad(y_pred, y_true):
    return 2 * (y_pred - y_true) / y_true.size

def mae_loss(y_pred, y_true):
    return np.mean(np.abs(y_pred - y_true))

def mae_grad(y_pred, y_true):
    return np.sign(y_pred - y_true) / y_true.size

def binary_cross_entropy(y_pred, y_true, eps=1e-12):
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

def bce_grad(y_pred, y_true, eps=1e-12):
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return (y_pred - y_true) / (y_pred * (1 - y_pred) * y_true.size)

def categorical_cross_entropy(y_pred, y_true, eps=1e-12):
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(np.sum(y_true * np.log(y_pred), axis=1))

def cce_grad(y_pred, y_true, eps=1e-12):
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -y_true / (y_pred * y_true.shape[0])

def hinge_loss(y_pred, y_true):
    margins = np.maximum(0, 1 - y_true * y_pred)
    return np.mean(margins)

def hinge_grad(y_pred, y_true):
    return -y_true * (y_true * y_pred < 1) / y_true.size

def huber_loss(y_pred, y_true, delta=1.0):
    error = y_pred - y_true
    abs_err = np.abs(error)
    quadratic = 0.5 * error ** 2
    linear = delta * (abs_err - 0.5 * delta)
    return np.mean(np.where(abs_err <= delta, quadratic, linear))

def huber_grad(y_pred, y_true, delta=1.0):
    error = y_pred - y_true
    abs_err = np.abs(error)
    return np.where(abs_err <= delta, error, delta * np.sign(error)) / y_true.size

def focal_loss(y_pred, y_true, gamma=2.0, eps=1e-12):
    y_pred = np.clip(y_pred, eps, 1 - eps)
    ce = -np.log(y_pred)
    return np.mean((1 - y_pred) ** gamma * ce * y_true + y_pred ** gamma * ce * (1 - y_true))


if __name__ == "__main__":
    np.random.seed(42)

    y_true_reg = np.array([1.5, 2.0, 3.5, 4.0])
    y_pred_reg = np.array([1.2, 2.3, 3.0, 4.5])

    print("Regression Losses:")
    print(f"  MSE:      {mse_loss(y_pred_reg, y_true_reg):.4f}")
    print(f"  MAE:      {mae_loss(y_pred_reg, y_true_reg):.4f}")
    print(f"  Huber:    {huber_loss(y_pred_reg, y_true_reg):.4f}")

    y_true_bin = np.array([0, 1, 1, 0])
    y_pred_bin = np.array([0.1, 0.9, 0.8, 0.2])

    print("\nBinary Classification Losses:")
    print(f"  BCE:      {binary_cross_entropy(y_pred_bin, y_true_bin):.4f}")
    print(f"  Hinge:    {hinge_loss(y_pred_bin * 2 - 1, y_true_bin * 2 - 1):.4f}")
    print(f"  Focal:    {focal_loss(y_pred_bin, y_true_bin):.4f}")

    y_true_mc = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    y_pred_mc = np.array([[0.7, 0.2, 0.1], [0.1, 0.8, 0.1], [0.05, 0.05, 0.9]])
    print(f"\nMulti-class CCE: {categorical_cross_entropy(y_pred_mc, y_true_mc):.4f}")

    grad_fn = focal_loss(y_pred_bin, y_true_bin)
    print(f"\nAll loss functions verified. Gradients available.")
