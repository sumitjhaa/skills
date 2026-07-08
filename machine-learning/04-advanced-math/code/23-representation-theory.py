"""04.23 Representation theory: characters and Fourier on finite groups."""
import numpy as np

# Regular representation of Z_3
def cyclic_group_regular_rep(n=3):
    """Regular representation of Z_n as permutation matrices."""
    reps = {}
    for k in range(n):
        P = np.zeros((n, n))
        for i in range(n):
            P[i, (i + k) % n] = 1
        reps[k] = P
    return reps

Z3 = cyclic_group_regular_rep(3)
for k, v in Z3.items():
    print(f"g={k}:\n{v}\n")

# Characters of Z_3 (1D irreps)
def cyclic_characters(n=3):
    chars = {}
    omega = np.exp(2j * np.pi / n)
    for k in range(n):
        chars[k] = np.array([omega**(k * j) for j in range(n)])
    return chars

chars = cyclic_characters(3)
print("Characters of Z_3:")
for k, v in chars.items():
    print(f"  chi_{k} = {np.round(v, 4)}")

# Orthogonality of characters
for i in range(3):
    for j in range(3):
        inner = np.sum(chars[i] * np.conj(chars[j])) / 3
        if i == j:
            print(f"<chi_{i}, chi_{j}> = {inner:.1f} (should be 1)")
        else:
            print(f"<chi_{i}, chi_{j}> = {inner:.4f} (should be 0)")

# Fourier transform on Z_3
def ft_cyclic(f):
    n = len(f)
    chars = cyclic_characters(n)
    f_hat = np.array([np.sum(f * np.conj(chars[k])) for k in range(n)]) / np.sqrt(n)
    return f_hat

f = np.array([1.0, 2.0, 1.0])
f_hat = ft_cyclic(f)
print(f"\nFunction f = {f}")
print(f"Fourier coefficients: {np.round(f_hat, 4)}")

# Inverse Fourier
def ift_cyclic(f_hat):
    n = len(f_hat)
    chars = cyclic_characters(n)
    f = np.array([np.sum(f_hat * chars[k]) for k in range(n)]) / np.sqrt(n)
    return f

f_recon = ift_cyclic(f_hat)
print(f"Reconstructed f: {np.round(f_recon, 4)}")
