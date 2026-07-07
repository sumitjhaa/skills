"""Engine & Connections: create_engine, connect, execute raw SQL."""
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///:memory:", echo=False)

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"))
    conn.commit()

with engine.connect() as conn:
    conn.execute(text("INSERT INTO users (name, email) VALUES (:name, :email)"),
                 [{"name": "Alice", "email": "alice@test.com"},
                  {"name": "Bob", "email": "bob@test.com"}])
    conn.commit()

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM users"))
    print("=== Engine & Connections ===\n")
    for row in result:
        print(f"  {row.id}: {row.name} ({row.email})")

print(f"\nEngine URL: {engine.url}")
print(f"Engine driver: {engine.driver}")
print(f"Table info: users table created and queried via raw SQL")
