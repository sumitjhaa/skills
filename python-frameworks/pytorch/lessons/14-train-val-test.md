# 🏗️ Train/Validation/Test Split
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Split data into training, validation, and test sets.

## Manual Split

```python
n = len(X)
train_end = int(0.7 * n)
val_end = int(0.85 * n)

X_train, X_val, X_test = X[:train_end], X[train_end:val_end], X[val_end:]
y_train, y_val, y_test = y[:train_end], y[train_end:val_end], y[val_end:]
```

## With DataLoader

```python
train_dataset = TensorDataset(X_train, y_train)
val_dataset   = TensorDataset(X_val, y_val)
test_dataset  = TensorDataset(X_test, y_test)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader   = DataLoader(val_dataset,   batch_size=32)
test_loader  = DataLoader(test_dataset,  batch_size=32)
```

## Why Three Sets?

- **Training:** update weights
- **Validation:** tune hyperparams, early stopping
- **Test:** final unbiased evaluation

<!-- 🤔 Never use test data for decisions like early stopping or hyperparameter tuning. -->

## Run the Code

```bash
python code/14-train-val-test.py
```
