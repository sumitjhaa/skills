# 🔗 Core: Joins & Subqueries
<!-- ⏱️ 20 min | 🟡 Intermediate -->

**What You'll Learn:** INNER JOIN, LEFT JOIN, aggregations, subqueries, GROUP BY.

## Joining Tables

```python
from sqlalchemy import join

j = users.join(orders, users.c.id == orders.c.user_id)
stmt = select(users.c.name, orders.c.product).select_from(j)
```

## LEFT JOIN

```python
j = users.outerjoin(orders, users.c.id == orders.c.user_id)
stmt = select(users.c.name, func.sum(orders.c.amount))
```

## Aggregations

```python
from sqlalchemy import func

stmt = select(
    users.c.name,
    func.sum(orders.c.amount).label("total")
).select_from(j).group_by(users.c.name)
```

## Subqueries

```python
subq = select(
    orders.c.user_id,
    func.sum(orders.c.amount).label("total")
).group_by(orders.c.user_id).subquery()

stmt = select(users.c.name, subq.c.total).join(subq, users.c.id == subq.c.user_id)
```

## Aliases

```python
from sqlalchemy import alias

managers = employees.alias("managers")
stmt = select(employees, managers).join(managers, employees.c.manager_id == managers.c.id)
```

<!-- 🤔 `.subquery()` wraps a SELECT as a FROM-clause. Access its columns with `.c`. -->

## Run the Code

```bash
python code/04-core-joins-subqueries.py
```
