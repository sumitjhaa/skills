# 📝 Core: CRUD Operations
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** Insert, Select, Update, Delete using SQLAlchemy Core expression language.

## Insert

```python
from sqlalchemy import insert

stmt = insert(products).values([
    {"name": "Laptop", "price": 999.99, "category": "electronics"},
    {"name": "Mouse", "price": 29.99},
])
with engine.connect() as conn:
    conn.execute(stmt)
    conn.commit()
```

## Select

```python
from sqlalchemy import select

# All rows
stmt = select(products)
result = conn.execute(stmt)

# With filter
stmt = select(products).where(products.c.category == "electronics")

# Access columns via .c
for row in result:
    print(row.name, row.price)
```

## Update

```python
from sqlalchemy import update

stmt = update(products).where(products.c.name == "Mouse").values(price=24.99)
conn.execute(stmt)
conn.commit()
```

## Delete

```python
from sqlalchemy import delete

stmt = delete(products).where(products.c.name == "Chair")
conn.execute(stmt)
conn.commit()
```

## Column Access

Use `table.c.column_name` to reference columns in expressions.

```python
select(products).where(products.c.price > 50)
update(products).where(products.c.id == 1).values(price=19.99)
```

<!-- 🧠 Core expressions compile to parameterized SQL — safe from injection. -->

## Run the Code

```bash
python code/03-core-crud.py
```
