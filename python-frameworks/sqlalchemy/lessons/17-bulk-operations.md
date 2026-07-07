# 📦 Bulk Operations
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Batch inserts, bulk updates, performance comparison.

## Bulk Insert

### Legacy (ORM per-row):
```python
for item in items:
    session.add(Product(**item))
session.commit()  # Slow for many rows
```

### Bulk Insert (Core):
```python
conn.execute(insert(Product.__table__), items)
conn.commit()
```

### Bulk Insert (ORM 2.0):
```python
session.add_all([Product(**item) for item in items])
session.commit()
```

### Bulk via `bulk_insert_mappings`:
```python
session.bulk_insert_mappings(Product, items)
session.commit()
```

## Bulk Update

```python
# ORM approach
session.query(Product).filter(Product.price == 0)\
    .update({"price": 1.99}, synchronize_session="fetch")
session.commit()
```

## When to Use Bulk

| Operation | Rows | Approach |
|-----------|------|----------|
| Insert 1000+ | Bulk | `bulk_insert_mappings` or Core |
| Update many | Bulk `update()` | Avoids loading objects |
| Read many | ORM queries | Better for business logic |

<!-- 🤔 Bulk operations skip the identity map — objects in session aren't updated. -->

## Run the Code

```bash
python code/17-bulk-operations.py
```
