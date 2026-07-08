"""Learning to Rank (RankNet-style) from scratch."""
import numpy as np

class RankNet:
    def __init__(self, n_features, lr=0.01, max_iter=100):
        self.w = np.random.randn(n_features) * 0.01
        self.lr = lr
        self.max_iter = max_iter

    def fit(self, X, y, qids):
        unique_q = np.unique(qids)
        for iteration in range(self.max_iter):
            grad = np.zeros_like(self.w)
            loss = 0
            for q in unique_q:
                idx = np.where(qids == q)[0]
                Xq, yq = X[idx], y[idx]
                for i in range(len(idx)):
                    for j in range(len(idx)):
                        if yq[i] > yq[j]:
                            sij = 1
                        elif yq[i] < yq[j]:
                            sij = -1
                        else:
                            continue
                        si = self.w @ Xq[i]
                        sj = self.w @ Xq[j]
                        Cij = np.log(1 + np.exp(-sij * (si - sj)))
                        loss += Cij
                        grad += (Xq[i] - Xq[j]) * (-sij / (1 + np.exp(sij * (si - sj))))
            self.w -= self.lr * grad / len(unique_q)
            if iteration % 20 == 0:
                print(f"  Iter {iteration}, loss: {loss:.4f}")

    def predict(self, X):
        return X @ self.w

    def ndcg(self, y_true, y_pred, k=5):
        idx = np.argsort(y_pred)[::-1][:k]
        dcg = 0
        for i, pos in enumerate(idx):
            dcg += (2**y_true[pos] - 1) / np.log2(i + 2)
        ideal = np.sort(y_true)[::-1][:k]
        idcg = sum((2**rel - 1) / np.log2(i + 2) for i, rel in enumerate(ideal))
        return dcg / idcg if idcg > 0 else 0

if __name__ == "__main__":
    np.random.seed(42)
    n_queries = 30
    n_per_query = 10
    X_list, y_list, qid_list = [], [], []
    for q in range(n_queries):
        Xq = np.random.randn(n_per_query, 5)
        yq = np.random.randint(0, 4, n_per_query)
        X_list.append(Xq); y_list.append(yq); qid_list.extend([q]*n_per_query)
    X = np.vstack(X_list)
    y = np.concatenate(y_list)
    qids = np.array(qid_list)

    rn = RankNet(n_features=5, lr=0.01, max_iter=50)
    rn.fit(X, y, qids)

    ndcgs = []
    for q in np.unique(qids):
        idx = qids == q
        ndcgs.append(rn.ndcg(y[idx], rn.predict(X[idx])))
    print(f"Mean NDCG@5: {np.mean(ndcgs):.4f}")
