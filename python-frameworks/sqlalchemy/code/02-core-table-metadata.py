"""Core: Table & Metadata — define tables with MetaData, create/drop."""
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean, Text

engine = create_engine("sqlite:///:memory:", echo=False)
metadata = MetaData()

authors = Table(
    "authors", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("bio", Text),
)

books = Table(
    "books", metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(200), nullable=False),
    Column("price", Float, default=0.0),
    Column("author_id", Integer),
    Column("in_stock", Boolean, default=True),
)

metadata.create_all(engine)

print("=== Core: Table & Metadata ===\n")
print(f"Tables created: {list(metadata.tables.keys())}")
for name, table in metadata.tables.items():
    cols = [(c.name, str(c.type), "PK" if c.primary_key else "") for c in table.columns]
    print(f"\n  {name}:")
    for col_name, col_type, pk in cols:
        print(f"    {col_name:12s} {col_type:20s} {pk}")

metadata.drop_all(engine)
print(f"\nTables after drop: {list(metadata.tables.keys())}")
print("Tables defined, created, and dropped successfully.")
