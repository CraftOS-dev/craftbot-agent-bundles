<!--
Source: https://github.com/wshobson/agents/blob/main/plugins/python-development/skills/python-resource-management/SKILL.md
Repo: wshobson/agents
-->
---
name: python-resource-management
description: Python resource management with context managers, cleanup patterns, and streaming. Use when managing connections, file handles, implementing cleanup logic, or building streaming responses with accumulated state.
---

# Python Resource Management

Manage resources deterministically using context managers. Resources like database connections, file handles, and network sockets should be released reliably, even when exceptions occur.

## When to Use This Skill

- Managing database connections and connection pools
- Working with file handles and I/O
- Implementing custom context managers
- Building streaming responses with state
- Handling nested resource cleanup
- Creating async context managers

## Core Concepts

### 1. Context Managers
The `with` statement ensures resources are released automatically, even on exceptions.

### 2. Protocol Methods
`__enter__`/`__exit__` for sync, `__aenter__`/`__aexit__` for async resource management.

### 3. Unconditional Cleanup
`__exit__` always runs, regardless of whether an exception occurred.

### 4. Exception Handling
Return `True` from `__exit__` to suppress exceptions, `False` to propagate them.

## Quick Start

```python
from contextlib import contextmanager

@contextmanager
def managed_resource():
    resource = acquire_resource()
    try:
        yield resource
    finally:
        resource.cleanup()

with managed_resource() as r:
    r.do_work()
```

## Fundamental Patterns

### Pattern 1: Class-Based Context Manager

```python
class DatabaseConnection:
    def __init__(self, dsn: str) -> None:
        self._dsn = dsn
        self._conn: Connection | None = None

    def connect(self) -> None:
        self._conn = psycopg.connect(self._dsn)

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "DatabaseConnection":
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()
```

### Pattern 2: Async Context Manager

```python
class AsyncDatabasePool:
    def __init__(self, dsn: str, min_size: int = 1, max_size: int = 10) -> None:
        self._dsn = dsn
        self._min_size = min_size
        self._max_size = max_size
        self._pool: asyncpg.Pool | None = None

    async def __aenter__(self) -> "AsyncDatabasePool":
        self._pool = await asyncpg.create_pool(
            self._dsn, min_size=self._min_size, max_size=self._max_size,
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._pool is not None:
            await self._pool.close()

    async def execute(self, query: str, *args) -> list[dict]:
        async with self._pool.acquire() as conn:
            return await conn.fetch(query, *args)
```

### Pattern 3: @contextmanager Decorator

```python
from contextlib import contextmanager, asynccontextmanager
import time
import structlog

logger = structlog.get_logger()

@contextmanager
def timed_block(name: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        logger.info(f"{name} completed", duration_seconds=round(elapsed, 3))

@asynccontextmanager
async def database_transaction(conn: AsyncConnection):
    await conn.execute("BEGIN")
    try:
        yield conn
        await conn.execute("COMMIT")
    except Exception:
        await conn.execute("ROLLBACK")
        raise
```

### Pattern 4: Unconditional Resource Release

```python
class FileProcessor:
    def __init__(self, path: str) -> None:
        self._path = path
        self._file: IO | None = None
        self._temp_files: list[Path] = []

    def __enter__(self) -> "FileProcessor":
        self._file = open(self._path, "r")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._file is not None:
            self._file.close()
        for temp_file in self._temp_files:
            try:
                temp_file.unlink()
            except OSError:
                pass
```

## Best Practices Summary

1. Always use context managers — for any resource that needs cleanup
2. Clean up unconditionally — `__exit__` runs even on exception
3. Don't suppress unexpectedly — return `False` unless suppression is intentional
4. Use `@contextmanager` — for simple resource patterns
5. Implement both protocols — support `with` and manual management
6. Use ExitStack — for dynamic numbers of resources
7. Accumulate efficiently — list + join, not string concatenation
8. Track metrics — time-to-first-byte matters for streaming
9. Document behavior — especially exception suppression
10. Test cleanup paths — verify resources are released on errors
