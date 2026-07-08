# 06.01 Computational Graphs

A computational graph is a directed acyclic graph (DAG) where nodes represent operations or variables, and edges represent data dependencies.

## DAG Construction

Every arithmetic expression decomposes into a DAG:

```
z = (a + b) * c

   a   b
    \ /
     +     c
      \   /
        *
        |
        z
```

Leaf nodes are inputs/parameters. Internal nodes are operations. Edges carry intermediate values.

## Topological Ordering

For correct forward (and later backward) evaluation, vertices must be visited in topological order — every parent before its children. Kahn's algorithm or DFS-based ordering works.

## Node Types

- **Leaf**: no children, stores a value, optionally a gradient
- **Unary**: one parent (neg, exp, log, sin, etc.)
- **Binary**: two parents (add, mul, sub, div)
- **Vararg**: many parents (sum, mean, concat)

## Key Properties

- Each node stores `data` (forward value) and later `grad` (accumulated gradient)
- The graph is built implicitly during forward execution (eager mode) or explicitly via a tape
- Cycles are forbidden — recurrence must be unrolled

## Why DAGs Matter

- Enable automatic differentiation via chain rule traversal
- Separate computation from gradient logic
- Allow graph optimizations: fusion, pruning, constant folding
- Foundation for every modern deep learning framework

## References

- Rumelhart, Hinton, Williams (1986). Learning representations by back-propagating errors.
- Autograd / Chainer / TF / PyTorch lineage.
