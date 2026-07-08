# 🏗️ Dataset & DataLoader
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Use `Dataset` and `DataLoader` for batching and shuffling.

## Dataset Class

```python
from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]
```

## DataLoader

```python
from torch.utils.data import DataLoader

dataset = MyDataset(X, y)
loader = DataLoader(dataset, batch_size=32, shuffle=True)

for X_batch, y_batch in loader:
    # training step
    pass
```

## Key Parameters

```python
DataLoader(dataset,
    batch_size=32,    # samples per batch
    shuffle=True,     # randomize order
    num_workers=2,    # parallel loading
    drop_last=True)   # drop incomplete batch
```

<!-- 🤔 Always shuffle training data. Never shuffle validation/test data. -->

## Run the Code

```bash
python code/13-dataset-dataloader.py
```
