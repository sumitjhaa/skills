import numpy as np
import matplotlib.pyplot as plt
import time


class COOMatrix:
    """Coordinate format sparse matrix."""
    def __init__(self, rows, cols, vals, shape):
        self.rows = np.array(rows)
        self.cols = np.array(cols)
        self.vals = np.array(vals)
        self.shape = shape

    def matvec(self, x):
        m, n = self.shape
        y = np.zeros(m)
        for idx in range(len(self.vals)):
            y[self.rows[idx]] += self.vals[idx] * x[self.cols[idx]]
        return y

    def to_dense(self):
        m, n = self.shape
        A = np.zeros((m, n))
        for idx in range(len(self.vals)):
            A[self.rows[idx], self.cols[idx]] = self.vals[idx]
        return A


class CSRMatrix:
    """Compressed Sparse Row format."""
    def __init__(self, values, col_indices, row_ptr, shape):
        self.values = np.array(values)
        self.col_indices = np.array(col_indices)
        self.row_ptr = np.array(row_ptr)
        self.shape = shape

    def matvec(self, x):
        m, n = self.shape
        y = np.zeros(m)
        for i in range(m):
            row_sum = 0.0
            for j in range(self.row_ptr[i], self.row_ptr[i + 1]):
                row_sum += self.values[j] * x[self.col_indices[j]]
            y[i] = row_sum
        return y

    def to_dense(self):
        m, n = self.shape
        A = np.zeros((m, n))
        for i in range(m):
            for j in range(self.row_ptr[i], self.row_ptr[i + 1]):
                A[i, self.col_indices[j]] = self.values[j]
        return A


class CSCMatrix:
    """Compressed Sparse Column format."""
    def __init__(self, values, row_indices, col_ptr, shape):
        self.values = np.array(values)
        self.row_indices = np.array(row_indices)
        self.col_ptr = np.array(col_ptr)
        self.shape = shape

    def matvec(self, x):
        m, n = self.shape
        y = np.zeros(m)
        for j in range(n):
            for idx in range(self.col_ptr[j], self.col_ptr[j + 1]):
                y[self.row_indices[idx]] += self.values[idx] * x[j]
        return y


def coo_to_csr(coo):
    """Convert COO to CSR."""
    m, n = coo.shape
    idx = np.lexsort((coo.cols, coo.rows))
    values = coo.vals[idx]
    col_indices = coo.cols[idx]
    row_ptr = np.zeros(m + 1, dtype=int)
    for i in range(len(values)):
        row_ptr[coo.rows[idx[i]] + 1] += 1
    row_ptr = np.cumsum(row_ptr)
    return CSRMatrix(values, col_indices, row_ptr, (m, n))


def coo_to_csc(coo):
    """Convert COO to CSC."""
    m, n = coo.shape
    idx = np.lexsort((coo.rows, coo.cols))
    values = coo.vals[idx]
    row_indices = coo.rows[idx]
    col_ptr = np.zeros(n + 1, dtype=int)
    for i in range(len(values)):
        col_ptr[coo.cols[idx[i]] + 1] += 1
    col_ptr = np.cumsum(col_ptr)
    return CSCMatrix(values, row_indices, col_ptr, (m, n))


class ELLMatrix:
    """ELLPACK format."""
    def __init__(self, data, col_indices, shape):
        self.data = data
        self.col_indices = col_indices
        self.shape = shape

    def matvec(self, x):
        m, n = self.shape
        n_cols = self.data.shape[1]
        y = np.zeros(m)
        for i in range(m):
            s = 0.0
            for j in range(n_cols):
                if self.col_indices[i, j] >= 0:
                    s += self.data[i, j] * x[self.col_indices[i, j]]
            y[i] = s
        return y


def dense_to_csr(A):
    """Convert dense matrix to CSR."""
    m, n = A.shape
    values = []
    col_indices = []
    row_ptr = [0]
    for i in range(m):
        for j in range(n):
            if abs(A[i, j]) > 1e-14:
                values.append(A[i, j])
                col_indices.append(j)
        row_ptr.append(len(values))
    return CSRMatrix(values, col_indices, row_ptr, (m, n))


def benchmark():
    """Benchmark sparse matvec vs dense."""
    sizes = [100, 500, 1000, 2000]
    densities = [0.01, 0.05, 0.1]

    fig, axes = plt.subplots(1, len(densities), figsize=(15, 5))

    for d_idx, density in enumerate(densities):
        dense_times = []
        csr_times = []

        for n in sizes:
            A_dense = np.random.randn(n, n)
            mask = np.random.rand(n, n) > density
            A_dense[mask] = 0
            A_sparse = dense_to_csr(A_dense)
            x = np.random.randn(n)

            t0 = time.perf_counter()
            for _ in range(10):
                y1 = A_dense @ x
            t_dense = (time.perf_counter() - t0) / 10
            dense_times.append(t_dense)

            t0 = time.perf_counter()
            for _ in range(10):
                y2 = A_sparse.matvec(x)
            t_csr = (time.perf_counter() - t0) / 10
            csr_times.append(t_csr)

            print(f"n={n}, density={density}: dense={t_dense*1000:.3f}ms, "
                  f"csr={t_csr*1000:.3f}ms")

        axes[d_idx].plot(sizes, dense_times, 'o-', label='Dense')
        axes[d_idx].plot(sizes, csr_times, 's-', label='CSR')
        axes[d_idx].set_xlabel('n')
        axes[d_idx].set_ylabel('Time (s)')
        axes[d_idx].set_title(f'Density = {density}')
        axes[d_idx].legend()
        axes[d_idx].grid(True, alpha=0.3)

    plt.suptitle('Sparse Matvec Benchmark')
    plt.tight_layout()
    plt.show()


def main():
    print("=" * 60)
    print("SPARSE MATRICES - CSR, CSC, COO, ELL")
    print("=" * 60)

    np.random.seed(42)

    print("\n--- COO Format ---")
    rows = [0, 1, 2, 0, 2]
    cols = [0, 2, 1, 3, 3]
    vals = [1.0, 2.0, 3.0, 4.0, 5.0]
    coo = COOMatrix(rows, cols, vals, (3, 4))

    A_dense = coo.to_dense()
    print(f"COO to dense:\n{A_dense}")

    print("\n--- CSR Format ---")
    csr = coo_to_csr(coo)
    print(f"Values: {csr.values}")
    print(f"Col indices: {csr.col_indices}")
    print(f"Row pointer: {csr.row_ptr}")
    print(f"CSR to dense:\n{csr.to_dense()}")

    print("\n--- CSC Format ---")
    csc = coo_to_csc(coo)
    x = np.array([1.0, 2.0, 3.0, 4.0])
    y_csr = csr.matvec(x)
    y_csc = csc.matvec(x)
    y_dense = A_dense @ x
    print(f"x = {x}")
    print(f"CSR matvec: {y_csr}")
    print(f"CSC matvec: {y_csc}")
    print(f"Dense matvec: {y_dense}")
    print(f"CSR match: {np.allclose(y_csr, y_dense)}")
    print(f"CSC match: {np.allclose(y_csc, y_dense)}")

    print("\n--- ELLPACK Format ---")
    A_test = np.array([[1, 0, 2],
                       [0, 3, 0],
                       [4, 0, 5]], dtype=float)
    n_cols_ell = 2
    data_ell = np.zeros((3, n_cols_ell))
    col_indices_ell = np.full((3, n_cols_ell), -1)
    for i in range(3):
        non_zero_cols = np.where(A_test[i] != 0)[0]
        for j, c in enumerate(non_zero_cols[:n_cols_ell]):
            data_ell[i, j] = A_test[i, c]
            col_indices_ell[i, j] = c

    ell = ELLMatrix(data_ell, col_indices_ell, (3, 3))
    x_ell = np.array([1, 2, 3])
    print(f"ELL data:\n{data_ell}")
    print(f"ELL col indices:\n{col_indices_ell}")
    print(f"ELL matvec: {ell.matvec(x_ell)}")
    print(f"Dense matvec: {A_test @ x_ell}")

    print("\n--- Sparse Matrix from Dense ---")
    n = 10
    A_rand = np.random.randn(n, n)
    A_rand[np.abs(A_rand) < 0.7] = 0
    csr_from_dense = dense_to_csr(A_rand)
    print(f"Dense non-zeros: {np.count_nonzero(A_rand)} / {n*n}")
    print(f"CSR values count: {len(csr_from_dense.values)}")

    x_test = np.random.randn(n)
    y1 = A_rand @ x_test
    y2 = csr_from_dense.matvec(x_test)
    print(f"Matvec match: {np.allclose(y1, y2)}")

    print("\n--- Benchmark ---")
    benchmark()

    print("\n--- Laplacian Matrix (Sparse Structure) ---")
    n_grid = 5
    n_nodes = n_grid * n_grid
    rows_lapl, cols_lapl, vals_lapl = [], [], []
    for i in range(n_grid):
        for j in range(n_grid):
            node = i * n_grid + j
            rows_lapl.append(node); cols_lapl.append(node); vals_lapl.append(4)
            if i > 0:
                rows_lapl.append(node); cols_lapl.append(node - n_grid); vals_lapl.append(-1)
            if i < n_grid - 1:
                rows_lapl.append(node); cols_lapl.append(node + n_grid); vals_lapl.append(-1)
            if j > 0:
                rows_lapl.append(node); cols_lapl.append(node - 1); vals_lapl.append(-1)
            if j < n_grid - 1:
                rows_lapl.append(node); cols_lapl.append(node + 1); vals_lapl.append(-1)

    csr_lapl = coo_to_csr(COOMatrix(rows_lapl, cols_lapl, vals_lapl, (n_nodes, n_nodes)))
    print(f"Laplacian nodes: {n_nodes}, non-zeros: {len(csr_lapl.values)}")
    print(f"Density: {len(csr_lapl.values) / (n_nodes * n_nodes) * 100:.2f}%")


if __name__ == "__main__":
    main()
