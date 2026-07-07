# 🗄️ SQLAlchemy Deep-Dive

SQLAlchemy is Python's most powerful and mature ORM/database toolkit. This deep-dive covers Core, ORM, migrations, performance, async, testing, and production patterns.

## Structure

```
sqlalchemy/
├── lessons/          # 20 markdown lessons
├── code/             # 20 runnable Python files
├── practice/         # 2 exercise sets
└── README.md         # this file
```

## Phases

| Phase | Topic | Lessons | Status |
|-------|-------|---------|--------|
| 01 | Core & ORM Foundations | 10 | ✅ Complete |
| 02 | Advanced & Production | 10 | ✅ Complete |

## Phase 01 — Core & ORM Foundations (lessons 01–10)

| # | Lesson | Code | What You'll Learn |
|---|--------|------|-------------------|
| 01 | Engine & Connections | ✅ | `create_engine`, `connect()`, raw SQL, params |
| 02 | Core: Table & Metadata | ✅ | `MetaData`, `Table`, `Column`, types, constraints |
| 03 | Core: CRUD Operations | ✅ | `insert/select/update/delete` with Core |
| 04 | Core: Joins & Subqueries | ✅ | JOIN, LEFT JOIN, GROUP BY, subqueries |
| 05 | ORM: Declarative Models | ✅ | `Mapped`, `mapped_column`, `DeclarativeBase` |
| 06 | ORM: Session & CRUD | ✅ | `Session`, `sessionmaker`, add/get/filter/delete |
| 07 | ORM: Querying | ✅ | Filter, order, join, aggregate |
| 08 | ORM: Relationships | ✅ | One-to-many, `back_populates`, cascade |
| 09 | ORM: Many-to-Many | ✅ | Association tables, `secondary` |
| 10 | Integration: Library | ✅ | Library management system |

## Phase 02 — Advanced & Production (lessons 11–20)

| # | Lesson | Code | What You'll Learn |
|---|--------|------|-------------------|
| 11 | Alembic Migrations | ✅ | Schema versioning, upgrade/downgrade |
| 12 | Advanced Querying | ✅ | Subqueries, window functions, CTEs |
| 13 | Inheritance Patterns | ✅ | STI, JTI, polymorphic queries |
| 14 | Events & Hooks | ✅ | Mapper/session/connection events |
| 15 | Async & Concurrency | ✅ | `AsyncSession`, async engine |
| 16 | Performance: N+1 | ✅ | Eager loading, profiling |
| 17 | Bulk Operations | ✅ | Batch inserts, bulk updates |
| 18 | Testing | ✅ | Fixtures, rollback strategy |
| 19 | Production Patterns | ✅ | Pooling, logging, retry |
| 20 | Integration: E-commerce | ✅ | Full e-commerce backend |

## Prerequisites

- Python 3.10+
- Basic SQL knowledge
- `pip install sqlalchemy aiosqlite`

## Quick Start

```bash
# Run any code file
python code/01-engine-connections.py

# Run tests
python -m pytest code/18-testing.py -v

# Run async demo
python code/15-async-concurrency.py
```

## Key SQLAlchemy 2.0 Features Used

- `Mapped[]` / `mapped_column()` — new 2.0 declarative style
- `session.execute(select(...))` — 2.0 query style
- `DeclarativeBase` — new base class
- `create_async_engine` — async support
