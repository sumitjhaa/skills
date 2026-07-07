# 🔢 NumPy & Pandas Deep-Dive

NumPy provides fast numerical arrays. Pandas adds DataFrames for data analysis. Together they're the foundation of the Python data stack.

## Structure

```
numpy-pandas/
├── lessons/       # 30 markdown lessons
├── code/          # 30 runnable Python files
├── practice/      # 3 exercise sets
└── README.md      # this file
```

## Progress

### Phase 01 — NumPy Foundations ✅
| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 01 | [Arrays](lessons/01-arrays.md) | [01-arrays.py](code/01-arrays.py) | Creation, shapes, dtypes |
| 02 | [Operations](lessons/02-operations.md) | [02-operations.py](code/02-operations.py) | Vectorized arithmetic, ufuncs |
| 03 | [Indexing](lessons/03-indexing.md) | [03-indexing.py](code/03-indexing.py) | Slicing, fancy indexing, masks |
| 04 | [Broadcasting](lessons/04-broadcasting.md) | [04-broadcasting.py](code/04-broadcasting.py) | Shape compatibility, newaxis |
| 05 | [Linear Algebra](lessons/05-linear-algebra.md) | [05-linear-algebra.py](code/05-linear-algebra.py) | Matrix ops, solve, eig, SVD |
| 06 | [Random](lessons/06-random.md) | [06-random.py](code/06-random.py) | Generators, distributions |
| 07 | [Aggregations](lessons/07-aggregations.md) | [07-aggregations.py](code/07-aggregations.py) | Sum, mean, std, axis |
| 08 | [Manipulation](lessons/08-manipulation.md) | [08-manipulation.py](code/08-manipulation.py) | Reshape, concat, split |
| 09 | [File I/O](lessons/09-file-io.md) | [09-file-io.py](code/09-file-io.py) | Save/load text, binary, compressed |
| 10 | [Integration: Data Pipeline](lessons/10-integration-data-pipeline.md) | [10-integration-data-pipeline.py](code/10-integration-data-pipeline.py) | End-to-end NumPy pipeline |

### Phase 02 — Pandas Basics ✅
| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 11 | [Series & DataFrames](lessons/11-series-dataframe.md) | [11-series-dataframe.py](code/11-series-dataframe.py) | Creation, attributes, dtypes |
| 12 | [Reading & Writing](lessons/12-reading-writing.md) | [12-reading-writing.py](code/12-reading-writing.py) | CSV, Excel, JSON, Parquet |
| 13 | [Indexing & Selection](lessons/13-indexing-selection.md) | [13-indexing-selection.py](code/13-indexing-selection.py) | loc, iloc, boolean masks |
| 14 | [Data Cleaning](lessons/14-data-cleaning.md) | [14-data-cleaning.py](code/14-data-cleaning.py) | Missing values, duplicates, types |
| 15 | [Group Operations](lessons/15-group-operations.md) | [15-group-operations.py](code/15-group-operations.py) | groupby, agg, transform |
| 16 | [Merge & Join](lessons/16-merge-join.md) | [16-merge-join.py](code/16-merge-join.py) | Merges, concat, join types |
| 17 | [Apply & Transform](lessons/17-apply-transform.md) | [17-apply-transform.py](code/17-apply-transform.py) | apply, map, vectorized ops |
| 18 | [Time Series](lessons/18-time-series.md) | [18-time-series.py](code/18-time-series.py) | Datetime, resample, rolling |
| 19 | [Visualization](lessons/19-visualization.md) | [19-visualization.py](code/19-visualization.py) | Line, bar, hist, box plots |
| 20 | [Integration: EDA](lessons/20-integration-eda.md) | [20-integration-eda.py](code/20-integration-eda.py) | Exploratory data analysis |

### Phase 03 — Advanced Analysis ✅
| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 21 | [MultiIndex](lessons/21-multiindex.md) | [21-multiindex.py](code/21-multiindex.py) | Hierarchical indexing |
| 22 | [Advanced GroupBy](lessons/22-advanced-groupby.md) | [22-advanced-groupby.py](code/22-advanced-groupby.py) | Custom agg, multiple keys |
| 23 | [Pivot & Crosstab](lessons/23-pivot-crosstab.md) | [23-pivot-crosstab.py](code/23-pivot-crosstab.py) | pivot_table, crosstab |
| 24 | [Rolling Windows](lessons/24-rolling-windows.md) | [24-rolling-windows.py](code/24-rolling-windows.py) | Rolling, expanding, EWMA |
| 25 | [String Operations](lessons/25-string-operations.md) | [25-string-operations.py](code/25-string-operations.py) | Vectorized str, regex |
| 26 | [Categorical Data](lessons/26-categorical.md) | [26-categorical.py](code/26-categorical.py) | Category dtype, memory |
| 27 | [Missing Data](lessons/27-missing-data.md) | [27-missing-data.py](code/27-missing-data.py) | Imputation, interpolation |
| 28 | [Performance](lessons/28-performance.md) | [28-performance.py](code/28-performance.py) | Vectorization, query, eval |
| 29 | [Large Datasets](lessons/29-large-datasets.md) | [29-large-datasets.py](code/29-large-datasets.py) | Memory, chunking, downcast |
| 30 | [Integration: Analytics](lessons/30-integration-analytics.md) | [30-integration-analytics.py](code/30-integration-analytics.py) | Customer analytics project |

## Practice
- [Phase 01 Exercises](practice/phase01-exercises.md)
- [Phase 02 Exercises](practice/phase02-exercises.md)
- [Phase 03 Exercises](practice/phase03-exercises.md)

## Quick Start

```bash
pip install numpy pandas matplotlib
python code/01-arrays.py
```
