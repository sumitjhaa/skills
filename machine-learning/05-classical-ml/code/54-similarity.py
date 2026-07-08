"""Similarity / Distance Measures from scratch."""
import numpy as np

def euclidean(x, y):
    return np.sqrt(np.sum((x - y)**2))

def manhattan(x, y):
    return np.sum(np.abs(x - y))

def cosine(x, y):
    return 1 - x @ y / (np.linalg.norm(x) * np.linalg.norm(y) + 1e-10)

def mahalanobis(x, y, cov_inv):
    diff = x - y
    return np.sqrt(diff @ cov_inv @ diff)

def dtw(x, y):
    n, m = len(x), len(y)
    D = np.full((n+1, m+1), np.inf)
    D[0, 0] = 0
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = (x[i-1] - y[j-1])**2
            D[i, j] = cost + min(D[i-1, j], D[i, j-1], D[i-1, j-1])
    return np.sqrt(D[n, m])

def levenshtein(a, b):
    n, m = len(a), len(b)
    D = np.zeros((n+1, m+1))
    for i in range(n+1): D[i, 0] = i
    for j in range(m+1): D[0, j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = 0 if a[i-1] == b[j-1] else 1
            D[i, j] = min(D[i-1, j] + 1, D[i, j-1] + 1, D[i-1, j-1] + cost)
    return D[n, m]

def kernel_alignment(K1, K2):
    num = np.sum(K1 * K2)
    den = np.sqrt(np.sum(K1**2) * np.sum(K2**2))
    return num / den

if __name__ == "__main__":
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([4.0, 5.0, 6.0])

    print(f"Euclidean: {euclidean(x, y):.4f}")
    print(f"Manhattan: {manhattan(x, y):.4f}")
    print(f"Cosine: {cosine(x, y):.4f}")

    cov = np.eye(3)
    cov_inv = np.linalg.inv(cov)
    print(f"Mahalanobis (I): {mahalanobis(x, y, cov_inv):.4f} (same as Euclidean)")

    ts_x = np.sin(np.linspace(0, np.pi, 10))
    ts_y = np.sin(np.linspace(0, np.pi, 15) + 0.5)
    print(f"DTW: {dtw(ts_x, ts_y):.4f}")

    print(f"Levenshtein('kitten', 'sitting'): {levenshtein('kitten', 'sitting')}")

    K1 = np.array([[1, 0.5], [0.5, 1]])
    K2 = np.array([[1, 0.8], [0.8, 1]])
    print(f"Kernel alignment: {kernel_alignment(K1, K2):.4f}")
