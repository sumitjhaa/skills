# 🏗️ Tensor Operations
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Index, slice, reshape, and broadcast tensors.

## Indexing & Slicing

```python
t = torch.randn(4, 4)
t[0]          # first row
t[:, 1]       # second column
t[1:3, 1:3]   # 2x2 submatrix
t[t > 0]      # boolean indexing
```

## Reshaping

```python
t = torch.randn(2, 3, 4)
t.view(6, 4)      # reshape (contiguous)
t.reshape(6, 4)   # reshape (may copy)
t.flatten()       # to 1D
t.squeeze()       # remove dims of size 1
t.unsqueeze(0)    # add dim at position 0
t.transpose(0, 1) # swap dims
t.permute(2, 0, 1) # arbitrary reorder
```

## Broadcasting

```python
a = torch.randn(3, 1)
b = torch.randn(3, 4)
c = a + b  # a broadcasts to (3, 4)
```

## Math Operations

```python
torch.add(a, b)
torch.mul(a, b)
torch.matmul(a, b)  # or a @ b
torch.sum(a), torch.mean(a)
```

<!-- 🤔 Broadcasting follows the same rules as NumPy. -->

## Run the Code

```bash
python code/02-tensor-operations.py
```
