<!--
Source: https://fastapi.tiangolo.com/ · https://litestar.dev/ · https://robyn.tech/
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# FastAPI / Litestar / Robyn — Modern Async Web Frameworks

The 2026 SOTA async-Python web stack is multi-track:
- **FastAPI 0.115+** — greenfield default, Pydantic v2 + OpenAPI, by far the
  largest ecosystem.
- **Litestar** (formerly Starlite) — msgspec-based serialization, ~2x faster
  than FastAPI, multi-decorator API, ideal for service-internal APIs.
- **Robyn** — Rust-backed runtime, perf-critical (>50k req/s on commodity
  hardware), less mature ecosystem.
- **Django 5.x + Django Ninja** — when you need Django's admin/ORM/auth
  with FastAPI-style endpoints.

## When to use this skill

- Choosing a framework for a new service (decision tree below)
- Migrating from Flask / older Django
- Performance-tuning an existing FastAPI / Litestar app
- Adding OpenAPI / OAuth2 / WebSockets to an existing service
- Integrating Pydantic v2 / msgspec for fast validation
- Dropping `uvloop` into an existing app for an easy 20-40% boost

Do NOT use these for: pure CLI tools (use Typer/Click); deeply integrated
admin UIs (use Django proper); WebSocket-heavy / SSE-only (consider
Starlette directly).

## Decision tree

```
Need Django admin / ORM / auth?
├── YES → Django 5.x (+ Django Ninja for typed APIs)
└── NO
    Need >30k req/s on commodity hardware?
    ├── YES → Robyn
    └── NO
        Service-internal API with strict perf budget?
        ├── YES → Litestar
        └── NO → FastAPI (default)
```

For 95% of greenfield work: FastAPI. Switch only with a measured budget
violation.

## Setup

```bash
# FastAPI
uv add "fastapi[standard]" uvloop pydantic-settings

# Litestar
uv add "litestar[standard]" msgspec uvloop

# Robyn
uv add robyn

# Django + Ninja
uv add django django-ninja pydantic
```

## Common recipes — FastAPI

### Recipe F1 — Minimal app

```python
# src/my_app/main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="My App", version="0.1.0")

class CreateUser(BaseModel):
    email: str
    name: str

@app.post("/users")
async def create_user(payload: CreateUser):
    return {"email": payload.email, "name": payload.name}
```

```bash
uv run fastapi dev src/my_app/main.py        # hot-reload dev server
uv run fastapi run src/my_app/main.py        # production (uvicorn)
```

### Recipe F2 — Production server (uvicorn + uvloop + h11)

```bash
uv add uvicorn[standard] uvloop httptools
```

```python
# pyproject.toml — [project.scripts]
[project.scripts]
serve = "my_app.cli:serve"

# src/my_app/cli.py
import uvicorn
def serve():
    uvicorn.run(
        "my_app.main:app",
        host="0.0.0.0",
        port=8000,
        loop="uvloop",
        http="httptools",
        workers=4,
    )
```

### Recipe F3 — Settings via pydantic-settings

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")
    database_url: str
    redis_url: str
    secret_key: str

settings = Settings()                        # reads APP_DATABASE_URL, etc.
```

### Recipe F4 — Dependency injection

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        yield session

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_repo.get(db, user_id)
```

### Recipe F5 — OAuth2 / JWT

```python
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2 = OAuth2PasswordBearer(tokenUrl="token")

async def current_user(token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401)
```

### Recipe F6 — WebSocket

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def ws(socket: WebSocket):
    await socket.accept()
    while True:
        msg = await socket.receive_text()
        await socket.send_text(f"echo: {msg}")
```

## Common recipes — Litestar

### Recipe L1 — Minimal app

```python
# src/my_app/main.py
from litestar import Litestar, post
from msgspec import Struct

class CreateUser(Struct):
    email: str
    name: str

@post("/users")
async def create_user(data: CreateUser) -> dict:
    return {"email": data.email, "name": data.name}

app = Litestar(route_handlers=[create_user])
```

```bash
uv run litestar run --port 8000 --reload
```

### Recipe L2 — msgspec vs Pydantic (perf)

Litestar uses `msgspec.Struct` natively — 5-10x faster validation than
Pydantic v2 for the same shape:

```python
class Order(Struct):
    id: int
    items: list[str]
    total: float
```

For shared models with FastAPI, you can mix Pydantic + msgspec — Litestar
accepts both.

### Recipe L3 — Controller + DTO pattern

```python
from litestar import Controller, get, post

class UserController(Controller):
    path = "/users"

    @get("/{user_id:int}")
    async def get_user(self, user_id: int) -> UserDTO: ...

    @post("/")
    async def create_user(self, data: CreateUserDTO) -> UserDTO: ...
```

Class-based controllers with shared dependencies — feels cleaner than
FastAPI's APIRouter for medium apps.

## Common recipes — Robyn

### Recipe R1 — Minimal app

```python
# src/my_app/main.py
from robyn import Robyn

app = Robyn(__file__)

@app.get("/")
async def hello():
    return {"hello": "world"}

@app.post("/users")
async def create_user(request):
    body = request.json()
    return {"ok": True, "email": body["email"]}

if __name__ == "__main__":
    app.start(port=8000)
```

Robyn handles the request loop in Rust; the Python coroutines just process.
Result: >50k req/s on commodity hardware, ~2-3x FastAPI on simple endpoints.

### Recipe R2 — When NOT to choose Robyn

- Need OpenAPI auto-generation (manual in Robyn).
- Need Pydantic-deep validation (Robyn is simpler).
- Need wide middleware ecosystem (Robyn is younger).

Robyn is the choice when raw req/s matters more than framework features.

## Common recipes — Django + Ninja

```python
# api.py
from ninja import NinjaAPI, Schema

api = NinjaAPI()

class CreateUserSchema(Schema):
    email: str
    name: str

@api.post("/users")
def create_user(request, payload: CreateUserSchema):
    return {"email": payload.email}
```

Django Ninja gives FastAPI-style typed endpoints with Django's auth/ORM/admin
intact. Best of both worlds for content-heavy / admin-heavy apps.

## uvloop integration (universal speedup)

```python
# main.py
import uvloop
uvloop.install()                              # before any asyncio.run

# OR with uvicorn flag
# uvicorn main:app --loop uvloop
```

`uvloop` is a drop-in `asyncio.Loop` replacement (Cython + libuv).
Typical 20-40% throughput boost on I/O-bound endpoints. Zero code changes.

## Pydantic v2 essentials

```python
from pydantic import BaseModel, Field, computed_field, field_validator
from datetime import datetime

class Order(BaseModel):
    id: int
    items: list[str] = Field(min_length=1)
    total: float
    created: datetime

    @computed_field
    @property
    def item_count(self) -> int:
        return len(self.items)

    @field_validator("total")
    @classmethod
    def positive_total(cls, v: float) -> float:
        if v < 0:
            raise ValueError("total must be non-negative")
        return v
```

Pydantic v2 is Rust-backed (5-50x faster than v1). Use `model_construct(...)`
to skip validation for trusted internal data.

## Common patterns / pitfalls

- **Don't block in async handlers.** No `time.sleep`, no `requests.get`, no
  sync DB drivers. Use `asyncio.sleep`, `httpx.AsyncClient`, `asyncpg`.
- **CPU-bound work**: `await asyncio.to_thread(cpu_func, args)` or offload
  to Ray/dask for heavy.
- **Database**: SQLAlchemy 2.x async + asyncpg for Postgres
  (see `sqlalchemy-2x-async-postgres` skill).
- **Background tasks**: FastAPI's `BackgroundTasks` is fire-and-forget;
  for real work use `arq`, `taskiq`, or Celery 5+.
- **Tracing**: OpenTelemetry auto-instrumentation works with all four
  (see `opentelemetry-observability` skill).
- **Rate limiting**: `slowapi` for FastAPI, `litestar-rate-limit` for
  Litestar.

## Performance benchmarks (June 2026, synthetic)

| Framework | req/s (single worker, hello) | Notes |
|---|---|---|
| Django (sync) | 5k | sync, baseline |
| FastAPI + uvicorn | 18k | default |
| FastAPI + uvicorn + uvloop | 26k | drop-in |
| Litestar + uvicorn + uvloop | 35k | msgspec serialization |
| Robyn | 55k | Rust event loop |

Reality: 90% of services are DB-bound, not framework-bound. Pick the
framework with the ecosystem you need.

## Sources

- https://fastapi.tiangolo.com/ — FastAPI docs
- https://litestar.dev/ — Litestar docs
- https://robyn.tech/ — Robyn docs
- https://django-ninja.dev/ — Django Ninja
- https://docs.pydantic.dev/latest/ — Pydantic v2
- https://github.com/jcrist/msgspec — msgspec
- https://uvloop.readthedocs.io/ — uvloop
