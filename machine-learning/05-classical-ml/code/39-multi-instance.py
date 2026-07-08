"""Multi-Instance Learning from scratch."""
import numpy as np

class MISVM:
    def __init__(self, C=1.0):
        self.C = C
        self.w = None
        self.b = 0

    def fit(self, bags, y_bag):
        n_bags = len(bags)
        X_all = np.vstack(bags)
        n_all = len(X_all)
        self.w = np.zeros(X_all.shape[1])

        bag_to_inst = []
        for i, bag in enumerate(bags):
            for _ in bag:
                bag_to_inst.append(i)

        for iteration in range(20):
            y_inst = np.zeros(n_all)
            for i, bag in enumerate(bags):
                if y_bag[i] == 1:
                    scores = bag @ self.w + self.b
                    best = np.argmax(scores)
                    y_inst[bag_to_inst == i] = -1
                    inst_idx = np.where(np.array(bag_to_inst) == i)[0]
                    y_inst[inst_idx[best]] = 1
                else:
                    y_inst[bag_to_inst == i] = -1

            grad = self.w.copy()
            for i in range(n_all):
                margin = 1 - y_inst[i] * (X_all[i] @ self.w + self.b)
                if margin > 0:
                    grad -= self.C * y_inst[i] * X_all[i]
            self.w -= 0.01 * grad / n_all

    def predict(self, bags):
        preds = []
        for bag in bags:
            scores = bag @ self.w + self.b
            preds.append(1 if np.max(scores) > 0 else 0)
        return np.array(preds)

if __name__ == "__main__":
    np.random.seed(42)

    pos_bags = []
    for _ in range(20):
        bag = np.random.randn(np.random.randint(3, 8), 5)
        bag[np.random.randint(len(bag))] += np.array([2, 2, 2, 2, 2])
        pos_bags.append(bag)

    neg_bags = [np.random.randn(np.random.randint(3, 8), 5) for _ in range(20)]

    bags = pos_bags + neg_bags
    y_bag = np.array([1]*20 + [0]*20)

    mi_svm = MISVM(C=1.0)
    mi_svm.fit(bags, y_bag)

    preds = mi_svm.predict(bags)
    acc = np.mean(preds == y_bag)
    print(f"MI-SVM bag accuracy: {acc:.4f}")
