<!--
Source: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html · https://magicstack.github.io/asyncpg/
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# SQLAlchemy 2.x Async + asyncpg (Postgres)

The 2026 SOTA Postgres stack from Python is SQLAlchemy 2.x async ORM/Core on
top of `asyncpg` (the fastest Postgres driver), with `alembic` for migrations
and optionally `SQLModel` (Pydantic + SQLAlchemy glue) for FastAPI integration.

## When to use this skill

- New Postgres-backed Python service
- Migrating from sync SQLAlchemy 1.4 to async 2.x
- Migrating from `psycopg2` / `databases` to asyncpg
- Adding migrations to a project using Alembic
- Integrating SQLAlchemy with FastAPI / Litestar
- "N+1 query" debugging
- Connection-pool tuning under load

Do NOT use SQLAlchemy when: raw asyncpg is plenty (analytics scripts, very
simple CRUD); you don't need migrations; you don't need cross-DB portability
(SQLAlchemy abstracts MySQL/SQLite/Postgres).

## Setup

```bash
uv add "sqlalchemy[asyncio]>=2.0" asyncpg "alembic>=1.13"
# Optional Pydantic glue
uv add sqlmodel
```

## Common recipes

### Recipe 1 — Engine + session factory

```python
# src/my_app/db.py
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine,
)

engine = create_async_engine(
    settings.database_url,                    # "postgresql+asyncpg://user:pw@host/db"
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,                       # checks connection liveness
    pool_recycle=3600,                        # recycle after 1h
    echo=settings.debug,                      # SQL logging
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,                    # IMPORTANT for FastAPI
)
```

### Recipe 2 — Declarative models (2.x style)

```python
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
```

Modern 2.x style uses `Mapped[T]` annotations + `mapped_column(...)` — both
runtime and static type checkers (mypy / pyrefly) understand it.

### Recipe 3 — Async query patterns

```python
from sqlalchemy import select

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def list_users(db: AsyncSession, limit: int = 50) -> list[User]:
    stmt = select(User).limit(limit).order_by(User.id)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def create_user(db: AsyncSession, email: str, name: str) -> User:
    user = User(email=email, name=name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
```

Always `await db.execute(stmt)` then `.scalar*` or `.scalars().all()`. NEVER
iterate the result without `scalars()` — you get raw rows otherwise.

### Recipe 4 — Eager-loading to avoid N+1

```python
from sqlalchemy.orm import selectinload, joinedload

# selectinload: separate SELECT per relationship — usually best for *-to-many
stmt = select(User).options(selectinload(User.orders))

# joinedload: single SELECT with JOIN — best for to-one / small to-many
stmt = select(Order).options(joinedload(Order.user))

# raiseload: fail loudly on accidental lazy-load
stmt = select(User).options(selectinload(User.orders).raiseload("*"))
```

Async sessions are LAZY by default — accessing `.orders` after the session
closes raises `MissingGreenlet`. Always eager-load relationships you need
post-session.

### Recipe 5 — Transactions

```python
async def transfer(db: AsyncSession, from_id: int, to_id: int, amount: int) -> None:
    async with db.begin():
        await db.execute(
            update(Account).where(Account.id == from_id).values(balance=Account.balance - amount)
        )
        await db.execute(
            update(Account).where(Account.id == to_id).values(balance=Account.balance + amount)
        )
    # auto-commits or rolls back on exception
```

`async with db.begin()` is the safe transaction pattern. Don't manually
`commit()`/`rollback()` unless you know you need savepoints.

### Recipe 6 — FastAPI dependency

```python
# src/my_app/deps.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        yield session

# In a route:
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404)
    return user
```

Session per request; auto-cleanup via the `yield` pattern. `expire_on_commit
=False` is critical or post-commit attribute access blows up.

### Recipe 7 — Alembic migrations

```bash
uvx alembic init -t async migrations
```

```python
# migrations/env.py — point at your Base.metadata
from my_app.db import Base
target_metadata = Base.metadata
```

```bash
uvx alembic revision --autogenerate -m "add users table"
uvx alembic upgrade head
uvx alembic downgrade -1                      # rollback one
uvx alembic history
uvx alembic current
```

For multi-env: pass `ALEMBIC_DATABASE_URL` env var, or use `-x url=...`.

### Recipe 8 — SQLModel (Pydantic + SQLAlchemy in one class)

```python
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    name: str
```

Use SQLModel when you want ONE class for both Pydantic API schema AND SQL
table. Less flexible than separate Pydantic DTOs + SQLAlchemy models, but
faster to write.

### Recipe 9 — Connection pool tuning

```python
engine = create_async_engine(
    url,
    pool_size=20,                             # connections kept open
    max_overflow=10,                          # burst over pool_size
    pool_timeout=30,                          # seconds to wait for a connection
    pool_recycle=3600,                        # seconds before refresh
    pool_pre_ping=True,                       # SELECT 1 before each checkout
)
```

Rule of thumb: `pool_size + max_overflow ≤ Postgres max_connections / workers`.
For 4 workers on a 100-conn Postgres: pool_size=20, max_overflow=5 (4 * 25 =
100).

### Recipe 10 — Diagnose slow queries

```python
engine = create_async_engine(url, echo="debug")
# OR enable query timing
from sqlalchemy import event
@event.listens_for(engine.sync_engine, "before_cursor_execute")
def log_slow_queries(conn, cursor, statement, *args, **kwargs):
    conn.info.setdefault("query_start_time", []).append(time.time())
@event.listens_for(engine.sync_engine, "after_cursor_execute")
def report_slow_queries(conn, cursor, statement, *args, **kwargs):
    elapsed = time.time() - conn.info["query_start_time"].pop()
    if elapsed > 0.1:                         # 100ms threshold
        logger.warning("slow query", elapsed=elapsed, sql=statement)
```

Pair with `py-spy` (CPU) and `EXPLAIN ANALYZE` (Postgres) for the full
picture.

## Performance numbers (June 2026 synthetic)

| Driver | tps (simple SELECT, single conn) |
|---|---|
| psycopg2 sync | 6k |
| psycopg3 sync | 9k |
| psycopg3 async | 12k |
| asyncpg | 22k |

For Postgres workloads, `asyncpg` is meaningfully faster. SQLAlchemy 2.x
adds ~10-20% overhead on top of raw driver throughput.

## Edge cases

- **`MissingGreenlet` errors**: accessing lazy-loaded attributes outside
  the session. Fix: eager-load OR access inside the session block.
- **`expire_on_commit=True` (default)**: re-fetches every attribute after
  commit — fine for scripts, broken for FastAPI. Set to False.
- **Connection leaks**: missing `async with session:` — sessions leaked,
  pool exhausted. Always use the context manager.
- **JSONB column**: `sqlalchemy.dialects.postgresql.JSONB` — type-safe in
  2.x. Combine with Pydantic for validation.
- **`SELECT FOR UPDATE`**: `select(User).with_for_update()` — Postgres-only;
  pair with explicit transactions.
- **Read replicas**: `async_sessionmaker(bind=engine_replica)` for a
  read-only session; use `bind=engine_write` for the writer.
- **Connection pre-ping cost**: `pool_pre_ping=True` adds a SELECT 1 per
  checkout. For very low-latency endpoints, prefer `pool_recycle` instead.
- **Migrations against testcontainers**: see `testcontainers-integration-
  testing` skill — run alembic upgrade against the container at fixture
  setup.

## Comparison

| ORM/driver | Notes |
|---|---|
| **SQLAlchemy 2.x async + asyncpg** | SOTA; widest ecosystem; recommended |
| Tortoise ORM | smaller; Django-like; less ecosystem |
| Piccolo ORM | modern; async-first; smaller community |
| Edgy / Saffier | newer; pydantic-native; nascent |
| raw asyncpg | fastest; no ORM; good for high-perf paths |
| psycopg3 | sync default; usable async |
| databases (encode/databases) | UNMAINTAINED — migrate away |
| GINO | UNMAINTAINED — migrate to SQLAlchemy 2.x async |

## Sources

- https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html — async docs
- https://docs.sqlalchemy.org/en/20/tutorial/ — 2.x tutorial
- https://magicstack.github.io/asyncpg/ — asyncpg docs
- https://alembic.sqlalchemy.org/ — Alembic
- https://sqlmodel.tiangolo.com/ — SQLModel
- https://www.postgresql.org/docs/ — Postgres docs
