# 🏗️ Hyperparameter Optimization
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Search for optimal hyperparameters.

## Grid Search

```python
for lr in [0.1, 0.01, 0.001]:
    for hidden in [32, 64, 128]:
        model = train_model(lr, hidden)
        score = evaluate(model)
```

## Random Search (better)

```python
for _ in range(20):
    lr = 10 ** random.uniform(-4, -1)
    hidden = random.choice([32, 64, 128])
    model = train_model(lr, hidden)
    score = evaluate(model)
```

## Optuna (recommended)

```python
import optuna

def objective(trial):
    lr = trial.suggest_float('lr', 1e-4, 1e-1, log=True)
    hidden = trial.suggest_int('hidden', 16, 128)
    model = train_model(lr, hidden)
    return evaluate(model)

study = optuna.create_study()
study.optimize(objective, n_trials=50)
```

<!-- 🤔 Random search is better than grid search. Optuna is better than both. -->

## Run the Code

```bash
python code/37-hyperparameter-opt.py
```
