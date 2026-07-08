"""Full AutoML Pipeline (prototype) from scratch."""
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score

class AutoMLPipeline:
    def __init__(self, n_trials=20):
        self.n_trials = n_trials
        self.best_pipeline = None
        self.best_score = -1

    def _get_models(self):
        from sklearn.linear_model import LogisticRegression
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.svm import SVC
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.neighbors import KNeighborsClassifier
        return {
            'lr': LogisticRegression(max_iter=200),
            'dt': DecisionTreeClassifier(),
            'svm': SVC(gamma='scale', max_iter=200),
            'rf': RandomForestClassifier(),
            'knn': KNeighborsClassifier()
        }

    def _get_preprocessors(self):
        from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
        return [('none', None), ('standard', StandardScaler()), ('minmax', MinMaxScaler()), ('robust', RobustScaler())]

    def fit(self, X, y):
        models = self._get_models()
        preps = self._get_preprocessors()
        results = []

        for _ in range(self.n_trials):
            model_name = np.random.choice(list(models.keys()))
            prep_name, prep = preps[np.random.randint(len(preps))]

            if prep:
                X_processed = prep.fit_transform(X)
            else:
                X_processed = X

            model = models[model_name]
            score = cross_val_score(model, X_processed, y, cv=3, scoring='accuracy').mean()

            results.append((prep_name, model_name, score, prep, model))
            if score > self.best_score:
                self.best_score = score
                self.best_prep_ = prep
                self.best_model_ = model.__class__(**model.get_params()) if hasattr(model, 'get_params') else model

        print("AutoML results (top 5):")
        results.sort(key=lambda r: r[2], reverse=True)
        for prep, model, score, _, _ in results[:5]:
            print(f"  {prep} + {model}: {score:.4f}")

        if self.best_prep_:
            X_best = self.best_prep_.fit_transform(X)
        else:
            X_best = X
        self.best_model_.fit(X_best, y)
        return self

    def predict(self, X):
        if self.best_prep_:
            X = self.best_prep_.transform(X)
        return self.best_model_.predict(X)

if __name__ == "__main__":
    X, y = make_classification(n_samples=300, n_features=10, random_state=42)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    aml = AutoMLPipeline(n_trials=15)
    aml.fit(X_tr, y_tr)
    preds = aml.predict(X_te)
    print(f"\nAutoML test accuracy: {accuracy_score(y_te, preds):.4f}")
