"""Rule Learning (CN2-style) from scratch."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class Rule:
    def __init__(self, conditions=None, prediction=None):
        self.conditions = conditions or []
        self.prediction = prediction

    def covers(self, x):
        return all(x[f] == v for f, v in self.conditions)

    def __str__(self):
        conds = ' AND '.join(f'x{f}=={v}' for f, v in self.conditions)
        return f"IF {conds} THEN {self.prediction}"

class CN2:
    def __init__(self, beam_width=5, min_cover=5):
        self.beam_width = beam_width
        self.min_cover = min_cover
        self.rule_list = []

    def fit(self, X, y):
        classes = np.unique(y)
        remaining_X, remaining_y = X.copy(), y.copy()

        for cls in classes:
            while True:
                best_rule = self._find_best_rule(remaining_X, remaining_y, cls)
                if best_rule is None: break
                covered = [i for i in range(len(remaining_X)) if best_rule.covers(remaining_X[i])]
                if len(covered) < self.min_cover: break
                self.rule_list.append(best_rule)
                remaining_X = np.delete(remaining_X, covered, axis=0)
                remaining_y = np.delete(remaining_y, covered, axis=0)
                if len(remaining_X) < self.min_cover: break

        self.default_class = np.bincount(remaining_y.astype(int)).argmax() if len(remaining_y) > 0 else classes[0]

    def _find_best_rule(self, X, y, target_class):
        best_rule = None
        best_score = -1
        beam = [Rule()]

        for _ in range(5):
            new_beam = []
            for rule in beam:
                used_features = set(f for f, _ in rule.conditions)
                for f in range(X.shape[1]):
                    if f in used_features: continue
                    for v in np.unique(X[:, f]):
                        new_rule = Rule(rule.conditions + [(f, v)])

                        covered = [i for i in range(len(X)) if new_rule.covers(X[i])]
                        if len(covered) < self.min_cover: continue

                        n_correct = sum(y[covered] == target_class)
                        score = (n_correct + 1) / (len(covered) + len(np.unique(y)))
                        if score > best_score:
                            best_score = score
                            best_rule = new_rule
                        new_beam.append(new_rule)

            if not new_beam: break
            new_beam.sort(key=lambda r: (sum(y[[i for i in range(len(X)) if r.covers(X[i])]] == target_class) + 1)
                           / (len([i for i in range(len(X)) if r.covers(X[i])]) + len(np.unique(y))), reverse=True)
            beam = new_beam[:self.beam_width]

        return best_rule

    def predict(self, X):
        preds = []
        for x in X:
            predicted = False
            for rule in self.rule_list:
                if rule.covers(x):
                    preds.append(rule.prediction)
                    predicted = True; break
            if not predicted:
                preds.append(self.default_class)
        return np.array(preds)

if __name__ == "__main__":
    X, y = make_classification(n_samples=300, n_features=5, n_informative=3, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    X_tr_disc = (X_tr > X_tr.mean(axis=0)).astype(int)
    X_te_disc = (X_te > X_tr.mean(axis=0)).astype(int)

    cn2 = CN2(beam_width=5, min_cover=5)
    cn2.fit(X_tr_disc, y_tr)
    print("Learned rules:")
    for r in cn2.rule_list:
        print(f"  {r}")
    print(f"Default class: {cn2.default_class}")

    preds = cn2.predict(X_te_disc)
    print(f"CN2 Accuracy: {accuracy_score(y_te, preds):.4f}")
