# ⚡ Advanced Querying
<!-- ⏱️ 20 min | 🔴 Advanced -->

**What You'll Learn:** Subqueries, window functions, CTEs, hybrid properties, custom expressions.

## Subqueries in ORM

```python
subq = session.query(
    Order.user_id,
    func.sum(Order.amount).label("total")
).group_by(Order.user_id).subquery()

users = session.query(User).join(subq, User.id == subq.c.user_id)\
    .filter(subq.c.total > 100).all()
```

## Window Functions

```python
stmt = select(
    Order.id,
    func.row_number().over(
        partition_by=Order.user_id,
        order_by=Order.created_at
    ).label("order_num")
)
```

## CTE (Common Table Expression)

```python
cte = session.query(
    Order.user_id,
    func.sum(Order.amount).label("total")
).group_by(Order.user_id).cte("order_totals")

results = session.query(User).join(cte, User.id == cte.c.user_id).all()
```

## Hybrid Properties

```python
from sqlalchemy.ext.hybrid import hybrid_property

class Product(Base):
    price: Mapped[float]
    tax_rate: Mapped[float] = mapped_column(Float, default=0.1)

    @hybrid_property
    def total_price(self):
        return self.price * (1 + self.tax_rate)
```

<!-- 🧠 Hybrid properties work at both the instance level and the query level (can be used in `.filter()`). -->

## Run the Code

```bash
python code/12-advanced-querying.py
```
