import numpy as np
import matplotlib.pyplot as plt
import time


def matmul_naive(A, B):
    """Naive O(n^3) matrix multiplication."""
    m, n = A.shape
    n2, p = B.shape
    if n != n2:
        raise ValueError(f"Incompatible shapes: {A.shape}, {B.shape}")
    C = np.zeros((m, p))
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i, j] += A[i, k] * B[k, j]
    return C


def matmul_naive_ikj(A, B):
    """Naive with i-k-j loop order for better cache behavior."""
    m, n = A.shape
    n2, p = B.shape
    C = np.zeros((m, p))
    for i in range(m):
        for k in range(n):
            aik = A[i, k]
            for j in range(p):
                C[i, j] += aik * B[k, j]
    return C


def matmul_tiled(A, B, tile_size=32):
    """Tiled/blocked matrix multiplication."""
    m, n = A.shape
    n2, p = B.shape
    C = np.zeros((m, p))
    for i in range(0, m, tile_size):
        for j in range(0, p, tile_size):
            for k in range(0, n, tile_size):
                i_end = min(i + tile_size, m)
                j_end = min(j + tile_size, p)
                k_end = min(k + tile_size, n)
                C[i:i_end, j:j_end] += A[i:i_end, k:k_end] @ B[k:k_end, j:j_end]
    return C


def strassen(A, B, crossover=64):
    """Strassen's algorithm with crossover to naive for small matrices."""
    n = A.shape[0]
    if n <= crossover:
        return A @ B

    mid = n // 2
    A11 = A[:mid, :mid]
    A12 = A[:mid, mid:]
    A21 = A[mid:, :mid]
    A22 = A[mid:, mid:]
    B11 = B[:mid, :mid]
    B12 = B[:mid, mid:]
    B21 = B[mid:, :mid]
    B22 = B[mid:, mid:]

    M1 = strassen(A11 + A22, B11 + B22, crossover)
    M2 = strassen(A21 + A22, B11, crossover)
    M3 = strassen(A11, B12 - B22, crossover)
    M4 = strassen(A22, B21 - B11, crossover)
    M5 = strassen(A11 + A12, B22, crossover)
    M6 = strassen(A21 - A11, B11 + B12, crossover)
    M7 = strassen(A12 - A22, B21 + B22, crossover)

    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    C = np.empty((n, n))
    C[:mid, :mid] = C11
    C[:mid, mid:] = C12
    C[mid:, :mid] = C21
    C[mid:, mid:] = C22
    return C


def matmul_cache_oblivious(A, B, threshold=32):
    """Cache-oblivious matrix multiplication using recursive splitting."""
    m, n = A.shape
    n2, p = B.shape

    if m <= threshold or n <= threshold or p <= threshold:
        return A @ B

    if m >= max(n, p):
        mid = m // 2
        return np.vstack([
            matmul_cache_oblivious(A[:mid], B, threshold),
            matmul_cache_oblivious(A[mid:], B, threshold)
        ])
    elif n >= max(m, p):
        mid = n // 2
        left = matmul_cache_oblivious(A[:, :mid], B[:mid], threshold)
        right = matmul_cache_oblivious(A[:, mid:], B[mid:], threshold)
        return left + right
    else:
        mid = p // 2
        return np.hstack([
            matmul_cache_oblivious(A, B[:, :mid], threshold),
            matmul_cache_oblivious(A, B[:, mid:], threshold)
        ])


def benchmark():
    """Benchmark different multiplication algorithms."""
    sizes = [32, 64, 96, 128, 192, 256]
    results = {'naive': [], 'ikj': [], 'tiled': [], 'blas': []}

    print(f"{'Size':<8} {'Naive':<12} {'IKJ':<12} {'Tiled':<12} {'BLAS':<12}")
    print("-" * 56)

    for n in sizes:
        A = np.random.randn(n, n)
        B = np.random.randn(n, n)

        t0 = time.perf_counter()
        _ = matmul_naive(A, B)
        t_naive = time.perf_counter() - t0
        results['naive'].append(t_naive)

        t0 = time.perf_counter()
        _ = matmul_naive_ikj(A, B)
        t_ikj = time.perf_counter() - t0
        results['ikj'].append(t_ikj)

        t0 = time.perf_counter()
        _ = matmul_tiled(A, B)
        t_tiled = time.perf_counter() - t0
        results['tiled'].append(t_tiled)

        t0 = time.perf_counter()
        _ = A @ B
        t_blas = time.perf_counter() - t0
        results['blas'].append(t_blas)

        print(f"{n:<8} {t_naive:<12.4f} {t_ikj:<12.4f} {t_tiled:<12.4f} {t_blas:<12.4f}")

    return sizes, results


def main():
    print("=" * 60)
    print("MATRIX MULTIPLICATION ALGORITHMS")
    print("=" * 60)

    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    B = np.array([[5.0, 6.0], [7.0, 8.0]])

    print(f"\nA =\n{A}")
    print(f"\nB =\n{B}")

    C_naive = matmul_naive(A, B)
    C_blas = A @ B
    print(f"\nNaive multiply:\n{C_naive}")
    print(f"BLAS multiply:\n{C_blas}")
    print(f"Match: {np.allclose(C_naive, C_blas)}")

    C_ikj = matmul_naive_ikj(A, B)
    print(f"IKJ loop order match: {np.allclose(C_ikj, C_blas)}")

    print("\n--- Strassen Validation ---")
    for n in [4, 8, 16, 32, 64]:
        A = np.random.randn(n, n)
        B = np.random.randn(n, n)
        C_strassen = strassen(A, B)
        C_ref = A @ B
        err = np.linalg.norm(C_strassen - C_ref) / np.linalg.norm(C_ref)
        print(f"n={n}: relative error = {err:.2e}")

    print("\n--- Cache Oblivious Validation ---")
    for n in [16, 32, 64]:
        A = np.random.randn(n, n)
        B = np.random.randn(n, n)
        C_co = matmul_cache_oblivious(A, B)
        C_ref = A @ B
        err = np.linalg.norm(C_co - C_ref) / np.linalg.norm(C_ref)
        print(f"n={n}: relative error = {err:.2e}")

    print("\n--- Tiled Validation ---")
    for n in [32, 64, 128]:
        A = np.random.randn(n, n)
        B = np.random.randn(n, n)
        C_tiled = matmul_tiled(A, B)
        C_ref = A @ B
        err = np.linalg.norm(C_tiled - C_ref) / np.linalg.norm(C_ref)
        print(f"n={n}: relative error = {err:.2e}")

    print("\n--- Benchmark ---")
    sizes, results = benchmark()

    fig, ax = plt.subplots(figsize=(10, 6))
    for label, data in results.items():
        ax.plot(sizes, data, 'o-', label=label)
    ax.set_xlabel('Matrix size (n)')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Matrix Multiplication Performance Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    naive_times = np.array(results['naive'])
    for label in ['blas', 'tiled']:
        speedup = naive_times / np.array(results[label])
        ax2.plot(sizes, speedup, 'o-', label=f'Speedup vs naive ({label})')
    ax2.set_xlabel('Matrix size (n)')
    ax2.set_ylabel('Speedup')
    ax2.set_title('Speedup vs Naive O(n³)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.show()


if __name__ == "__main__":
    main()
