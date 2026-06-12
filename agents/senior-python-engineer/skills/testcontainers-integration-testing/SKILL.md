<!--
Source: https://github.com/testcontainers/testcontainers-python · https://testcontainers-python.readthedocs.io/
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# testcontainers — Real-Backend Integration Testing

`testcontainers-python` spins up real Postgres / Redis / Kafka / RabbitMQ /
Mongo / Elasticsearch containers on demand for each test session — giving
you actual-backend integration tests instead of brittle mocks. The 2026
SOTA for replacing repository / queue / cache mocks with the real thing.

Pair with `pyfakefs` for filesystem isolation when needed.

## When to use this skill

- Integration tests that hit a database — drop psycopg/asyncpg mocks
- Queue tests that need real broker semantics (Kafka, RabbitMQ)
- Cache invalidation tests — Redis behaviour can't be mocked accurately
- Migration tests — run Alembic upgrade/downgrade against a real Postgres
- "It works against sqlite but breaks on Postgres" investigations
- Service-to-service contract tests
- Replacing handwritten Docker setup in test fixtures

Do NOT use testcontainers for: pure unit tests (still mock dependencies);
contract tests against external APIs (use `respx`/`vcrpy`); environments
where Docker is unavailable (CI without Docker-in-Docker).

## Setup

```bash
uv add --dev "testcontainers[postgresql]" pytest-asyncio asyncpg
# Optional extras
uv add --dev "testcontainers[redis,kafka,mongodb,elasticsearch]"
```

Requires Docker (or Podman with `DOCKER_HOST=unix:///var/run/podman/podman.sock`).
On macOS, Docker Desktop / Colima / OrbStack all work.

## Common recipes

### Recipe 1 — Postgres session fixture

```python
# tests/conftest.py
import asyncio
import asyncpg
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_url():
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg.get_connection_url()

@pytest.fixture
async def db(postgres_url):
    conn = await asyncpg.connect(postgres_url)
    try:
        yield conn
    finally:
        await conn.close()
```

```python
# tests/test_users.py
import pytest
from my_app.users import create_user, get_user

@pytest.mark.asyncio
async def test_create_user_returns_user(db):
    await db.execute(open("schema.sql").read())
    user = await create_user(db, email="alice@example.com")
    fetched = await get_user(db, user.id)
    assert fetched.email == "alice@example.com"
```

The container starts ONCE per test session (`scope="session"`), is shared
across tests, and cleans up automatically.

### Recipe 2 — Run Alembic migrations against the container

```python
@pytest.fixture(scope="session")
def postgres_url():
    with PostgresContainer("postgres:16-alpine") as pg:
        url = pg.get_connection_url()
        # Run real migrations against the real DB
        import subprocess
        subprocess.run(
            ["uv", "run", "alembic", "upgrade", "head"],
            env={**os.environ, "DATABASE_URL": url},
            check=True,
        )
        yield url
```

This catches migration bugs that mocks would never expose.

### Recipe 3 — Redis cache test

```python
from testcontainers.redis import RedisContainer
import redis.asyncio as aioredis

@pytest.fixture(scope="session")
def redis_url():
    with RedisContainer("redis:7-alpine") as r:
        yield f"redis://{r.get_container_host_ip()}:{r.get_exposed_port(6379)}"

@pytest.mark.asyncio
async def test_cache_set_get(redis_url):
    client = aioredis.from_url(redis_url)
    await client.set("k", "v", ex=10)
    assert await client.get("k") == b"v"
```

### Recipe 4 — Kafka producer/consumer

```python
from testcontainers.kafka import KafkaContainer

@pytest.fixture(scope="session")
def kafka_bootstrap():
    with KafkaContainer() as kafka:
        yield kafka.get_bootstrap_server()

def test_publish_consume(kafka_bootstrap):
    from confluent_kafka import Producer, Consumer
    p = Producer({"bootstrap.servers": kafka_bootstrap})
    p.produce("topic", b"hello")
    p.flush()
    c = Consumer({
        "bootstrap.servers": kafka_bootstrap,
        "group.id": "g1",
        "auto.offset.reset": "earliest",
    })
    c.subscribe(["topic"])
    msg = c.poll(timeout=5)
    assert msg.value() == b"hello"
```

### Recipe 5 — Per-test isolation via transactions

For Postgres, run each test inside a SAVEPOINT and roll back:

```python
@pytest.fixture
async def db(postgres_url):
    conn = await asyncpg.connect(postgres_url)
    tr = conn.transaction()
    await tr.start()
    try:
        yield conn
    finally:
        await tr.rollback()
        await conn.close()
```

Container starts once; each test runs in its own transaction; rollback at
end gives perfect isolation. This is the recommended pattern.

### Recipe 6 — pyfakefs for filesystem tests

```python
def test_writes_config_file(fs):                # fs is the pyfakefs fixture
    fs.create_file("/etc/myapp/conf.yaml", contents="key: value")
    config = load_config("/etc/myapp/conf.yaml")
    assert config.key == "value"
```

```bash
uv add --dev pyfakefs
```

Filesystem fake; no real disk writes. Faster than tempdirs, equally isolated.

### Recipe 7 — Multi-service test (Postgres + Redis + your service)

```python
@pytest.fixture(scope="session")
def services():
    with PostgresContainer("postgres:16-alpine") as pg, \
         RedisContainer("redis:7-alpine") as r:
        yield {
            "postgres_url": pg.get_connection_url(),
            "redis_url": f"redis://localhost:{r.get_exposed_port(6379)}",
        }

@pytest.fixture
async def app(services):
    from my_app import create_app
    return create_app(
        database_url=services["postgres_url"],
        redis_url=services["redis_url"],
    )
```

### Recipe 8 — Custom image (your own service)

```python
from testcontainers.core.container import DockerContainer

@pytest.fixture(scope="session")
def my_service():
    with DockerContainer("my-registry/my-service:test").with_exposed_ports(8080) as c:
        c.start()
        url = f"http://localhost:{c.get_exposed_port(8080)}"
        yield url
```

Useful for contract tests against your own service binary.

### Recipe 9 — CI gotchas

```yaml
# GitHub Actions
- uses: actions/checkout@v4
- uses: astral-sh/setup-uv@v3
- run: uv sync --frozen
# Docker is available by default on ubuntu-latest runners
- run: uv run pytest tests/integration/
```

For self-hosted runners without Docker, switch to Docker-in-Docker via
sysbox or use a service-container approach.

## Common patterns

### Slow startup → use session scope + savepoints

Container start is 1-3 seconds. Reuse via `scope="session"` and isolate
tests with savepoints. Never `scope="function"` for containers.

### Schema setup

Use Alembic migrations as the schema source. Tests should not maintain a
separate `schema.sql`.

### Seed data

Use a `fixture` that inserts before yield and deletes after. Keep seed data
minimal — one row per concept, not "realistic load."

### Wait for ready

`testcontainers` includes wait-strategies for each backend. If a test
flakes at container startup, increase the wait timeout:

```python
PostgresContainer("postgres:16-alpine").with_kwargs(
    wait_for_logs=("database system is ready", 30)
)
```

## Edge cases

- **Docker unavailable**: testcontainers will raise at startup. CI options:
  Docker-in-Docker, service containers (GH Actions), or skip the integration
  test marker.
- **Slow CI runners**: cache the Docker image via the registry; testcontainers
  pulls fresh otherwise. Set `TESTCONTAINERS_RYUK_DISABLED=true` if you don't
  need the auto-cleanup container.
- **Port conflicts**: testcontainers picks a random host port; access via
  `container.get_exposed_port(internal_port)`. Don't hard-code.
- **Network bridges in CI**: when CI workers are themselves containers,
  use `host.docker.internal` or `--network=host`.
- **Volumes**: pass `volumes={"/host/path": "/container/path"}` to share
  files. Rare for unit-level tests.
- **Resource cleanup**: `with` block guarantees cleanup; `pytest` session
  teardown also runs. If you see leftover containers (e.g., after Ctrl-C),
  `docker container prune` clears them.

## Comparison with mocks

| Approach | Speed | Fidelity | Setup cost |
|---|---|---|---|
| Mock (`Mock()` / `unittest.mock`) | <1ms | LOW — tests pass even when prod fails | Low |
| In-memory DB (sqlite) | 10ms | MEDIUM — diverges from Postgres on JSONB, FOR UPDATE, COPY | Low |
| **testcontainers** | 1-3s startup + 10ms per test | HIGH — same engine as prod | Medium |
| Stage environment | 100ms-2s per test | HIGH | High (separate ops) |

In practice: unit tests stay mocked; integration tests use testcontainers.

## Sources

- https://github.com/testcontainers/testcontainers-python — source
- https://testcontainers-python.readthedocs.io/ — full docs
- https://testcontainers.com/ — multi-language project home
- https://github.com/pytest-dev/pyfakefs — pyfakefs source
- https://docs.docker.com/desktop/ — Docker Desktop
