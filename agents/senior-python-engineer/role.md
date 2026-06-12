# Senior Python Engineer — deep reference

This section appends to `AGENT.md`. It is **not** in the agent's default context. Grep it when the SOUL.md summary isn't enough.

Headings are kept search-friendly: "Code review playbook", "Antipattern catalog", "Performance investigation playbook", "Debugging procedure", "Refactoring procedures", "Testing reference patterns", etc.

For provenance of any section, see `SOURCES.md` in this bundle.

---

## Capability reference

Pure factual reference — what tools, frameworks, and language features exist in the Python ecosystem. SOUL.md does not carry these (they don't drive decisions); grep here when the user asks "what should I use for X?" or you need to name a specific tool.

### Python development verification checklist

- Type hints for all function signatures and class attributes
- PEP 8 compliance with `ruff` (replaces black + isort + flake8 + pyupgrade + pydocstyle + bandit-lite + autoflake; see `ruff-lint-format-all-in-one` skill)
- Comprehensive docstrings (Google style)
- Test coverage exceeding 90% with pytest
- Error handling with custom exceptions
- Async/await for I/O-bound operations
- Performance profiling for critical paths
- Security scanning with bandit

### Pythonic patterns and idioms

- List / dict / set comprehensions over loops
- Generator expressions for memory efficiency
- Context managers for resource handling
- Decorators for cross-cutting concerns
- Properties for computed attributes
- Dataclasses for data structures
- Protocols for structural typing
- Pattern matching for complex conditionals

### Type system features

- Complete type annotations for public APIs
- Generic types with `TypeVar` and `ParamSpec`
- Protocol definitions for duck typing
- Type aliases for complex types
- Literal types for constants
- `TypedDict` for structured dicts
- Union types — prefer `T | None` (Python 3.10+) over `Optional[T]`
- Mypy strict mode compliance
- Type narrowing with guards

### Async and concurrent programming capabilities

- AsyncIO for I/O-bound concurrency
- Proper async context managers (`__aenter__` / `__aexit__`)
- `concurrent.futures` for CPU-bound tasks
- Multiprocessing for parallel execution
- Thread safety with locks and queues
- Async generators and comprehensions
- Task groups and exception handling
- Performance monitoring for async code

### Web framework expertise

- FastAPI for modern async APIs
- Django for full-stack applications
- Flask for lightweight services
- SQLAlchemy for database ORM
- Pydantic for data validation
- Celery for task queues
- Redis for caching
- WebSocket support

### Testing methodology

**Tools:**
- pytest as the test runner
- pytest-cov for coverage
- pytest-asyncio for async tests
- Hypothesis for property-based testing
- freezegun for time mocking
- pytest-benchmark for performance

**Test structure (AAA):** Arrange → Act → Assert. Each test independent, no shared state, cleans up after itself.

**Test naming convention:** `test_<unit>_<scenario>_<expected_outcome>`. Examples:
- `test_create_user_with_valid_data_returns_user`
- `test_create_user_with_duplicate_email_raises_conflict`
- `test_get_user_with_unknown_id_returns_none`

Bad names to flag in review: `test_1`, `test_user`, `test_function`.

**Test types coverage:**
- **Unit Tests**: Isolated function/method tests, mocking dependencies, edge cases, error paths
- **Integration Tests**: API endpoint tests, database integration, service-to-service communication, middleware chains
- **E2E Tests**: Critical user journeys, happy paths, error scenarios, browser/API-level flows
- **TDD Support**: Red-green-refactor cycle, failing test first
- **Coverage Analysis**: Identify untested paths, coverage gap analysis

### Package management

- LEGACY: Poetry or `uv` for dependency management. **SOTA 2026: `uv` (Astral, Rust) — 10-100x faster than pip/poetry, single binary, replaces pip+poetry+pyenv+pip-tools+virtualenv+pipx. See `uv-uvx-modern-toolchain` skill.**
- Virtual environments with `venv`
- Requirements pinning with `pip-tools`
- Semantic versioning compliance
- Package distribution to PyPI
- Private package repositories
- Docker containerization
- Dependency vulnerability scanning

**Modern packaging standards:** PEPs 517/518/621/660. Single `pyproject.toml` for build, dependencies, metadata, and tool config. Prefer `src/` layout over flat — prevents accidental imports from the dev directory and improves test isolation.

### Security best practices reference

- Input validation and sanitization
- SQL injection prevention
- Secret management with env vars (never hardcode)
- Cryptography library usage
- OWASP compliance
- Authentication and authorization
- Rate limiting implementation
- Security headers for web apps
- Encryption for sensitive data
- API key management and rotation
- Audit logging for sensitive operations

### Debugging techniques

- Breakpoint debugging
- Log analysis
- Binary search (git bisect or manual)
- Divide and conquer
- Rubber duck debugging
- Time travel debugging (rr, pdb's time-travel features)
- Differential debugging (compare working vs broken)
- Statistical debugging

### Common bug patterns to suspect first

- Off-by-one errors
- `None` / null pointer exceptions
- Resource leaks
- Race conditions
- Integer overflows (rare in Python but possible in C extensions)
- Type mismatches
- Logic errors
- Configuration issues

### Behavioral traits

- Follows PEP 8 and modern Python idioms consistently
- Prioritizes code readability and maintainability
- Uses type hints throughout
- Implements comprehensive error handling with custom exceptions
- Writes extensive tests with high coverage (>90%)
- Leverages Python's standard library before external dependencies
- Focuses on performance optimization when needed
- Documents code thoroughly with docstrings and examples
- Stays current with latest Python releases and ecosystem changes
- Emphasizes security and best practices in production code

### Response approach (full)

1. Analyze requirements for modern Python best practices
2. Suggest current tools and patterns from the 2024/2025 ecosystem
3. Provide production-ready code with proper error handling and type hints
4. Include comprehensive tests with pytest and appropriate fixtures
5. Consider performance implications and suggest optimizations
6. Document security considerations and best practices
7. Recommend modern tooling for development workflow
8. Include deployment strategies when applicable

### Example interactions this agent handles

- "Help me migrate from pip to uv for package management"
- "Optimize this Python code for better async performance"
- "Design a FastAPI application with proper error handling and validation"
- "Set up a modern Python project with ruff, mypy, and pytest"
- "Implement a high-performance data processing pipeline"
- "Create a production-ready Dockerfile for a Python application"
- "Design a scalable background task system with Celery"
- "Implement modern authentication patterns in FastAPI"
- "Review this PR — focus on security and performance"
- "I'm seeing a `RecursionError` only under load — help me find the cause"

---

## Antipattern catalog

Full BAD/GOOD code pairs for every anti-pattern in the SOUL.md checklist. Use these when reviewing code or when the user asks "what's wrong with this pattern?"

### Scattered timeout/retry logic

```python
# BAD
def fetch_user(user_id):
    try:
        return requests.get(url, timeout=30)
    except Timeout:
        logger.warning("Timeout fetching user")
        return None

def fetch_orders(user_id):
    try:
        return requests.get(url, timeout=30)
    except Timeout:
        logger.warning("Timeout fetching orders")
        return None
```

```python
# GOOD: Centralized retry logic
@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def http_get(url: str) -> Response:
    return requests.get(url, timeout=30)
```

### Double retry

```python
# BAD: Retrying at multiple layers
@retry(max_attempts=3)  # Application retry
def call_service():
    return client.request()  # Client also has retry configured!
```

Retry at one layer only. Know your infrastructure's retry behavior.

### Hard-coded configuration

```python
# BAD
DB_HOST = "prod-db.example.com"
API_KEY = "sk-12345"

def connect():
    return psycopg.connect(f"host={DB_HOST}...")
```

```python
# GOOD
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str = Field(alias="DB_HOST")
    api_key: str = Field(alias="API_KEY")

settings = Settings()
```

### Exposed internal types

```python
# BAD: Leaking ORM model to API
@app.get("/users/{id}")
def get_user(id: str) -> UserModel:
    return db.query(UserModel).get(id)
```

```python
# GOOD: Use DTOs
@app.get("/users/{id}")
def get_user(id: str) -> UserResponse:
    user = db.query(UserModel).get(id)
    return UserResponse.from_orm(user)
```

### Mixed I/O and business logic

```python
# BAD: SQL embedded in business logic
def calculate_discount(user_id: str) -> float:
    user = db.query("SELECT * FROM users WHERE id = ?", user_id)
    orders = db.query("SELECT * FROM orders WHERE user_id = ?", user_id)
    if len(orders) > 10:
        return 0.15
    return 0.0
```

```python
# GOOD: Repository pattern, pure business logic
def calculate_discount(user: User, orders: list[Order]) -> float:
    if len(orders) > 10:
        return 0.15
    return 0.0
```

### Bare exception handling

```python
# BAD
try:
    process()
except Exception:
    pass
```

```python
# GOOD
try:
    process()
except ConnectionError as e:
    logger.warning("Connection failed, will retry", error=str(e))
    raise
except ValueError as e:
    logger.error("Invalid input", error=str(e))
    raise BadRequestError(str(e))
```

### Ignored partial failures

```python
# BAD: Stops on first error
def process_batch(items):
    results = []
    for item in items:
        result = process(item)
        results.append(result)
    return results
```

```python
# GOOD: Capture both successes and failures
def process_batch(items) -> BatchResult:
    succeeded = {}
    failed = {}
    for idx, item in enumerate(items):
        try:
            succeeded[idx] = process(item)
        except Exception as e:
            failed[idx] = e
    return BatchResult(succeeded, failed)
```

### Missing input validation

```python
# BAD
def create_user(data: dict):
    return User(**data)  # Crashes deep in code on bad input
```

```python
# GOOD
def create_user(data: dict) -> User:
    validated = CreateUserInput.model_validate(data)
    return User.from_input(validated)
```

### Unclosed resources

```python
# BAD
def read_file(path):
    f = open(path)
    return f.read()
```

```python
# GOOD
def read_file(path):
    with open(path) as f:
        return f.read()
```

### Blocking in async

```python
# BAD
async def fetch_data():
    time.sleep(1)
    response = requests.get(url)
```

```python
# GOOD
async def fetch_data():
    await asyncio.sleep(1)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
```

### Missing type hints

```python
# BAD
def process(data):
    return data["value"] * 2
```

```python
# GOOD
def process(data: dict[str, int]) -> int:
    return data["value"] * 2
```

### Untyped collections

```python
# BAD
def get_users() -> list:
    ...
```

```python
# GOOD
def get_users() -> list[User]:
    ...
```

### Only testing happy paths

```python
# BAD
def test_create_user():
    user = service.create_user(valid_data)
    assert user.id is not None
```

```python
# GOOD
def test_create_user_success():
    user = service.create_user(valid_data)
    assert user.id is not None

def test_create_user_invalid_email():
    with pytest.raises(ValueError, match="Invalid email"):
        service.create_user(invalid_email_data)

def test_create_user_duplicate_email():
    service.create_user(valid_data)
    with pytest.raises(ConflictError):
        service.create_user(valid_data)
```

### Over-mocking

```python
# BAD
def test_user_service():
    mock_repo = Mock()
    mock_cache = Mock()
    mock_logger = Mock()
    mock_metrics = Mock()
    # Test doesn't verify real behavior
```

Use integration tests for critical paths. Mock only external services.

### Common fixes summary

| Anti-Pattern | Fix |
|-------------|-----|
| Scattered retry logic | Centralized decorators |
| Hard-coded config | Environment variables + pydantic-settings |
| Exposed ORM models | DTO/response schemas |
| Mixed I/O + logic | Repository pattern |
| Bare except | Catch specific exceptions |
| Batch stops on error | Return BatchResult with successes/failures |
| No validation | Validate at boundaries with Pydantic |
| Unclosed resources | Context managers |
| Blocking in async | Async-native libraries |
| Missing types | Type annotations on all public APIs |
| Only happy path tests | Test errors and edge cases |

---

## Code review playbook

### Review preparation

- Change scope analysis
- Standard identification
- Context gathering
- Tool configuration
- History review
- Related issues
- Team preferences
- Priority setting

### Context evaluation

- Review pull request
- Understand changes
- Check related issues
- Review history
- Identify patterns
- Set focus areas
- Configure tools
- Plan approach

### Implementation phase — conduct thorough code review

- Analyze systematically
- Check security first
- Verify correctness
- Assess performance
- Review maintainability
- Validate tests
- Check documentation
- Provide feedback

### Review patterns

- Start with high-level
- Focus on critical issues
- Provide specific examples
- Suggest improvements
- Acknowledge good practices
- Be constructive
- Prioritize feedback
- Follow up consistently

### Review categories — what to look at

- Security vulnerabilities
- Performance bottlenecks
- Memory leaks
- Race conditions
- Error handling
- Input validation
- Access control
- Data integrity

### Best practices enforcement

- Clean code principles
- SOLID compliance
- DRY adherence
- KISS philosophy
- YAGNI principle
- Defensive programming
- Fail-fast approach
- Documentation standards

### Constructive feedback shape

- Specific examples
- Clear explanations
- Alternative solutions
- Learning resources
- Positive reinforcement
- Priority indication
- Action items
- Follow-up plans

---

## Debugging procedure

### Issue analysis — gather information

Analysis priorities:
- Symptom documentation
- Error collection
- Environment details
- Reproduction steps
- Timeline construction
- Impact assessment
- Change correlation
- Pattern identification

Information gathering:
- Collect error logs
- Review stack traces
- Check system state
- Analyze recent changes
- Interview stakeholders
- Review documentation
- Check known issues
- Set up environment

### Apply systematic debugging

Implementation approach:
1. Reproduce issue
2. Form hypotheses
3. Design experiments
4. Collect evidence
5. Analyze results
6. Isolate cause
7. Develop fix
8. Validate solution

Debugging patterns:
- Start with reproduction
- Simplify the problem
- Check assumptions
- Use scientific method
- Document findings
- Verify fixes
- Consider side effects
- Share knowledge

### Resolution checklist

- Root cause identified
- Fix implemented
- Solution tested
- Side effects verified
- Performance validated
- Documentation complete
- Knowledge shared
- Prevention planned

### Error analysis techniques

- Stack trace interpretation
- Core dump analysis
- Memory dump examination
- Log correlation
- Error pattern detection
- Exception analysis
- Crash report investigation
- Performance profiling

### Memory debugging — what to look for

- Memory leaks
- Buffer overflows (in C extensions)
- Use-after-free (in C extensions)
- Memory corruption
- Heap analysis
- Stack analysis
- Reference tracking (cycles)

### Concurrency debugging

- Race conditions
- Deadlocks
- Livelocks
- Thread safety
- Synchronization bugs
- Timing issues
- Resource contention
- Lock ordering

### Production debugging — non-intrusive techniques

- **SOTA 2026 stack — see `## SOTA tool reference (June 2026)` section below for deep dives:**
- Live stack snapshot: `uvx py-spy dump --pid <PID>` (no code change, no install pollution) — see `py-spy-cpu-profiling` skill.
- Live live top: `uvx py-spy top --pid <PID>` — current hot frames, updated every second.
- Live memory leak hunt: `uvx memray attach <PID>` (Linux, requires CAP_SYS_PTRACE), or arrange to start the service under `memray run` — see `memray-memory-profiling` skill. `memray --native --leaks` is the killer combo.
- Distributed tracing: OpenTelemetry Python SDK + Honeycomb/Datadog/Sentry/Grafana Tempo — see `opentelemetry-observability` skill.
- Continuous profiling: Sentry Profiling / Pyroscope / Datadog Continuous Profiler — sample CPU+memory continuously in prod with low overhead.
- Sampling methods (py-spy is sampling-based; lower fidelity per-line, higher fidelity prod-safe vs cProfile).
- Log aggregation (ELK, Loki) — pair with OTel log correlation (`LoggingInstrumentor` injects trace_id into every log).
- Metrics correlation — OTel histograms / counters / gauges via `meter.create_*`.
- Canary analysis — wire OTel resource attribute `deployment.canary=true` to slice.
- A/B test debugging — use trace tags / span attributes per experiment arm.

### Postmortem process

- Timeline creation
- Root cause analysis
- Impact assessment
- Action items
- Process improvements
- Knowledge sharing
- Monitoring additions
- Prevention strategies

---

## Performance investigation playbook

### Step 1 — establish baseline

Comprehensive measurement and profiling. Without a baseline, "improvement" is unmeasurable.

Ask the user (or assume the most useful answer):
- **What's the budget?** Latency (p50 / p99), memory ceiling, throughput.
- **What's the observed value?** "It's slow" is not a measurement.
- **What's the input?** Real data shape, not a synthetic minimal example.

### Step 2 — pick the tool

| Symptom | Tool (legacy → SOTA 2026) |
|---|---|
| Don't know where time goes | LEGACY: `cProfile` for cold profile, then `py-spy` for live sampling. **SOTA 2026: `uvx py-spy record -o flame.svg --format speedscope -- python script.py` (no code change, attach to PID) — see `py-spy-cpu-profiling` skill.** cProfile still fine when you need EXACT deterministic call counts, not sampling. |
| Looks like memory growth | LEGACY: `tracemalloc` for snapshot, `memory_profiler` for per-line. **SOTA 2026: `uvx memray run --native python script.py && uvx memray flamegraph` — captures native C-extension allocs via LD_PRELOAD that tracemalloc misses. See `memray-memory-profiling` skill.** `tracemalloc` still OK for stdlib-only contexts. `memory_profiler` is fully superseded — do not reach for it. |
| Async event loop slow | LEGACY: `asyncio.run(... debug=True)` + `aiomonitor`. **SOTA 2026: `uvx viztracer --log_async python script.py` then open `result.json` in Perfetto UI — see `viztracer-asyncio-timeline` skill.** Perfetto timeline shows exactly when each task ran/awaited. |
| Suspect GIL contention | `py-spy dump --pid <PID>` for a one-shot stack snapshot, `py-spy top --pid <PID>` for live view. **Also: `uvx scalene script.py` shows CPU split between Python and native — see `scalene-ai-optimization` skill.** |
| Combined CPU + memory + GPU in one shot | **SOTA 2026: `uvx scalene --html --outfile profile.html script.py` — unified CPU/memory/GPU profile with AI optimization suggestions on hot lines. See `scalene-ai-optimization` skill.** |
| I/O-bound vs CPU-bound unclear | compare wall vs CPU time (`time` command, `perf`); cross-check with `py-spy record --idle` (idle threads visible). |

### Step 3 — order of typical wins

1. **Algorithmic change** (O(n²) → O(n log n)) — almost always the largest win.
2. **Avoid per-iteration overhead** — hoist invariants out of the loop, replace per-iteration `.append()` with a list comprehension if it fits.
3. **Batch I/O** — one query for 1000 rows beats 1000 queries for 1 row. Same for file reads, HTTP calls.
4. **Caching** (`functools.lru_cache`, external Redis) for repeated computations.
5. **Built-in functions** (C-implemented) over hand-rolled.
6. **NumPy vectorization** for numerical work.
7. **Cython / Numba** for hot paths.
8. **Async I/O** — only if genuinely I/O-bound.
9. **Multiprocessing** — only if work is large enough to amortize pickle / fork cost.

### Step 4 — observability stack

- **OpenTelemetry**: Distributed tracing, metrics collection, correlation across services
- **APM platforms**: DataDog APM, New Relic, Dynatrace, AppDynamics, Honeycomb, Jaeger
- **Metrics & monitoring**: Prometheus, Grafana, InfluxDB, custom metrics, SLI/SLO tracking
- **Real User Monitoring (RUM)**: User experience tracking, Core Web Vitals
- **Synthetic monitoring**: Uptime monitoring, API testing, user journey simulation
- **Log correlation**: Structured logging, distributed log tracing, error correlation

### Step 5 — load testing

- Tools: k6, JMeter, Gatling, Locust, Artillery
- API testing: REST API testing, GraphQL performance testing, WebSocket testing
- Browser testing: Puppeteer, Playwright, Selenium WebDriver performance testing
- Chaos engineering: Netflix Chaos Monkey, Gremlin, failure injection testing
- Performance budgets: Budget tracking, CI/CD integration, regression detection
- Scalability testing: Auto-scaling validation, capacity planning, breaking point analysis

### Step 6 — caching architecture

- **Application caching**: In-memory caching, object caching, computed value caching
- **Distributed caching**: Redis, Memcached, Hazelcast
- **Database caching**: Query result caching, connection pooling, buffer pool optimization
- **CDN optimization**: CloudFlare, AWS CloudFront, Azure CDN, GCP CDN
- **Browser caching**: HTTP cache headers, service workers
- **API caching**: Response caching, conditional requests, cache invalidation

### Step 7 — verify

Re-run the same benchmark. If the change isn't measurable, undo it — speculative optimization is technical debt with no return.

---

## Refactoring procedures

### A class is growing and seems to have multiple responsibilities, but splitting it feels wrong

Apply the "reason to change" test: list every change that could require editing this class. If the list has items from different domains (e.g., HTTP parsing AND business rules AND formatting), split it. If all changes stem from the same domain concern, the class may be appropriately sized.

### Injecting all dependencies through the constructor is producing constructors with 7+ parameters

This is a sign of too many responsibilities in one class, not a problem with dependency injection. Split the class into smaller units first, then each constructor naturally becomes smaller.

### Composition is producing deeply nested wrapper objects that are hard to trace

Keep the composition shallow (2-3 levels). If wrapping is the only mechanism, consider whether a Protocol-based approach or simple function composition would be cleaner than a chain of decorator objects.

### The rule of three says not to abstract yet, but the duplication is causing bugs when one copy is updated but not the other

Duplication that diverges in dangerous ways should be abstracted sooner. The rule of three is a heuristic, not a law. If the copies are already diverging incorrectly, extract immediately and add a test that exercises the shared behavior.

### A service layer is importing from the API layer, breaking the dependency direction

Layering violation. The service layer must not import from handlers. Introduce a shared types/models layer that both can import from, keeping the dependency arrow pointing downward (API → Service → Repository).

### Renaming something used widely

1. Add the new name as an alias for the old. Both work.
2. Update call sites in batches, one PR each. Keep tests green.
3. When the old name has zero call sites, remove it.

This avoids the "one giant rename PR" that's impossible to review.

### Converting sync to async

- Make sure the code is actually I/O-bound. CPU-bound code does not benefit from async.
- Convert from the bottom up: low-level functions first, then their callers.
- `asyncio.run` only at the top. Don't sprinkle event loops through the code.
- Watch for accidentally serial code (`await` in a loop where `asyncio.gather` would parallelize).

---

## Testing reference patterns

### Testing retry behavior

```python
from unittest.mock import Mock

def test_retries_on_transient_error():
    client = Mock()
    client.request.side_effect = [
        ConnectionError("Failed"),
        ConnectionError("Failed"),
        {"status": "ok"},
    ]
    service = ServiceWithRetry(client, max_retries=3)
    result = service.fetch()
    assert result == {"status": "ok"}
    assert client.request.call_count == 3

def test_gives_up_after_max_retries():
    client = Mock()
    client.request.side_effect = ConnectionError("Failed")
    service = ServiceWithRetry(client, max_retries=3)
    with pytest.raises(ConnectionError):
        service.fetch()
    assert client.request.call_count == 3

def test_does_not_retry_on_permanent_error():
    client = Mock()
    client.request.side_effect = ValueError("Invalid input")
    service = ServiceWithRetry(client, max_retries=3)
    with pytest.raises(ValueError):
        service.fetch()
    assert client.request.call_count == 1
```

### Mocking time with freezegun

```python
from freezegun import freeze_time
from datetime import datetime

@freeze_time("2026-01-15 10:00:00")
def test_token_expiry():
    token = create_token(expires_in_seconds=3600)
    assert token.expires_at == datetime(2026, 1, 15, 11, 0, 0)

def test_with_time_travel():
    with freeze_time("2026-01-01") as frozen_time:
        item = create_item()
        assert item.created_at == datetime(2026, 1, 1)
        frozen_time.move_to("2026-01-15")
        assert item.age_days == 14
```

### Test markers

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    import time
    time.sleep(2)

@pytest.mark.integration
def test_database_integration():
    pass

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(os.name == "nt", reason="Unix only test")
def test_unix_specific():
    pass

@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug():
    assert False
```

```bash
pytest -m slow          # Run only slow tests
pytest -m "not slow"    # Skip slow tests
pytest -m integration   # Run integration tests
```

### Coverage reporting

```bash
pip install pytest-cov

pytest --cov=myapp tests/
pytest --cov=myapp --cov-report=html tests/
pytest --cov=myapp --cov-fail-under=80 tests/
pytest --cov=myapp --cov-report=term-missing tests/
```

---

## Async patterns deep reference

### Basic async/await

```python
import asyncio

async def fetch_data(url: str) -> dict:
    await asyncio.sleep(1)
    return {"url": url, "data": "result"}

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())
```

### Concurrent execution with gather()

```python
async def fetch_user(user_id: int) -> dict:
    await asyncio.sleep(0.5)
    return {"id": user_id, "name": f"User {user_id}"}

async def fetch_all_users(user_ids: List[int]) -> List[dict]:
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)
```

### Task creation and management

```python
async def main():
    task1 = asyncio.create_task(background_task("Task 1", 2))
    task2 = asyncio.create_task(background_task("Task 2", 1))
    print("Main: doing other work")
    await asyncio.sleep(0.5)
    result1 = await task1
    result2 = await task2
```

### Error handling

```python
async def process_items(item_ids: List[int]):
    tasks = [safe_operation(iid) for iid in item_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    successful = [r for r in results if r is not None and not isinstance(r, Exception)]
    failed = [r for r in results if isinstance(r, Exception)]
    return successful
```

### Timeout handling

```python
async def with_timeout():
    try:
        result = await asyncio.wait_for(slow_operation(5), timeout=2.0)
    except asyncio.TimeoutError:
        print("Operation timed out")
```

### Cancellation handling

```python
async def cancelable_task():
    try:
        while True:
            await asyncio.sleep(1)
            print("Working...")
    except asyncio.CancelledError:
        print("Task cancelled, cleaning up...")
        # Perform cleanup
        raise  # Re-raise to propagate cancellation
```

---

## Pydantic validation patterns

```python
from pydantic import BaseModel, Field, field_validator

class CreateUserInput(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v.lower()

    @field_validator("name")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        return v.strip().title()

# Usage at API boundary
try:
    user_input = CreateUserInput(
        email="user@example.com",
        name="john doe",
        age=25,
    )
except ValidationError as e:
    print(e.errors())  # Structured error info
```

---

## Resource management deep examples

### Class-based context manager

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

### Async context manager

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

### @contextmanager + @asynccontextmanager decorators

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

---

## Type system deep examples

### Generic Result class

```python
from typing import TypeVar, Generic

T = TypeVar("T")
E = TypeVar("E", bound=Exception)

class Result(Generic[T, E]):
    def __init__(
        self,
        value: T | None = None,
        error: E | None = None,
    ) -> None:
        if (value is None) == (error is None):
            raise ValueError("Exactly one of value or error must be set")
        self._value = value
        self._error = error

    @property
    def is_success(self) -> bool:
        return self._error is None

    def unwrap(self) -> T:
        if self._error is not None:
            raise self._error
        return self._value  # type: ignore[return-value]

    def unwrap_or(self, default: T) -> T:
        if self._error is not None:
            return default
        return self._value  # type: ignore[return-value]

# Usage preserves types
def parse_config(path: str) -> Result[Config, ConfigError]:
    try:
        return Result(value=Config.from_file(path))
    except ConfigError as e:
        return Result(error=e)
```

### Type narrowing with guards

```python
def process_user(user_id: str) -> UserData:
    user = find_user(user_id)
    if user is None:
        raise UserNotFoundError(f"User {user_id} not found")
    # Type checker knows user is User here
    return UserData(name=user.name, email=user.email)

def process_items(items: list[Item | None]) -> list[ProcessedItem]:
    valid_items = [item for item in items if item is not None]
    return [process(item) for item in valid_items]
```

---

## SOTA tool reference (June 2026)

Grep-friendly per-tool reference. Each tool gets ~10-30 lines naming the
verb, the source, the canonical command(s), and the bundled skill pack
that deep-dives. Run any tool via `cli-anything` skill + `uvx`/`uv run`.

### uv — universal Python verb

Replaces pip + poetry + pyenv + pip-tools + virtualenv + pipx.

- `uv init --package my-pkg` — new src/-layout project
- `uv add <pkg>` / `uv add --dev <pkg>` / `uv remove <pkg>`
- `uv sync` (install) / `uv sync --frozen` (CI) / `uv lock --upgrade`
- `uv run <cmd>` — run inside the project venv
- `uv python install 3.12` / `uv python pin 3.12` — interpreter management
- `uv export --format requirements-txt` — legacy compat

Source: https://docs.astral.sh/uv/ · Skill: `uv-uvx-modern-toolchain`

### uvx — ephemeral tool runner

Like `pipx run` but instant. Default agent verb for any CLI tool not added
as a dep.

- `uvx ruff check .` / `uvx mypy --strict src/` / `uvx pytest`
- `uvx py-spy record -- python script.py`
- `uvx memray run script.py`
- `uvx scalene script.py` / `uvx pyinstrument script.py`
- `uvx pre-commit install` / `uvx cz commit` / `uvx bandit -r src/`

Source: https://docs.astral.sh/uv/guides/tools/ · Skill: `uv-uvx-modern-toolchain`

### ruff — lint + format in one binary

Replaces black + isort + flake8 + pyupgrade + pydocstyle + bandit-lite +
pylint-lite + autoflake + eradicate. 900+ rules. Rust.

- `uvx ruff check --select=ALL --fix .`
- `uvx ruff format .` (black-equivalent)
- `uvx ruff check --select=UP,SIM,RUF,B --fix .` (pyupgrade pass)
- `uvx ruff check --select=S .` (bandit-lite security subset)
- Pre-commit: `astral-sh/ruff-pre-commit` hook

Source: https://docs.astral.sh/ruff/ · Skill: `ruff-lint-format-all-in-one`

### pyrefly — Meta's Rust type checker (v1.0 stable May 2026)

10-50x faster than mypy, 90%+ typing-spec conformance. Successor to Pyre.

- `uv add --dev pyrefly && uv run pyrefly check src/`
- `uv run pyrefly check --watch src/` (dev loop)
- `uv run pyrefly infer src/` (generate stubs)
- Strict mode: `[tool.pyrefly] errors = ["all"]`

Source: https://github.com/facebook/pyrefly · Skill: `pyrefly-meta-type-checker`

### ty — Astral's type checker (beta, 1.0 in 2026)

Sibling to uv + ruff. Worth tracking; not yet default.

- `uvx ty check src/`

Source: https://docs.astral.sh/ty/

### mypy — mature default

Still the broadest plugin ecosystem (django-stubs, sqlalchemy-stubs,
pydantic-mypy). Use when you need plugins.

- `uvx mypy --strict src/`

Source: https://mypy.readthedocs.io/

### pyright — Microsoft, Pylance engine

Embedded in VSCode via Pylance. Fast. Good complement to ruff in IDE.

- `uvx pyright src/`

Source: https://github.com/microsoft/pyright

### py-spy — sampling profiler, no code change

Attach to ANY Python process by PID. Production-safe. Replaces cProfile
for "where is time going?"

- `uvx py-spy record -o flame.svg --format speedscope -- python script.py`
- `uvx py-spy record -o flame.svg --pid <PID> --duration 60`
- `uvx py-spy top --pid <PID>` (live)
- `uvx py-spy dump --pid <PID>` (stack snapshot for hangs)
- `--native` for C-extension stacks, `--idle` to include sleeping threads

Source: https://github.com/benfred/py-spy · Skill: `py-spy-cpu-profiling`

### memray — memory profiler (Bloomberg)

Replaces `memory_profiler` entirely. Tracks NATIVE C-extension allocs via
LD_PRELOAD. Live mode, leak mode, native mode.

- `uvx memray run --native -o cap.bin python script.py`
- `uvx memray flamegraph cap.bin`
- `uvx memray run --live python script.py` (TUI)
- `uvx memray run --leaks` for leak detection
- pytest integration: `uv add --dev pytest-memray && pytest --memray`

Source: https://github.com/bloomberg/memray · Skill: `memray-memory-profiling`

### scalene — unified CPU + GPU + memory + AI suggestions

Plasma Group. UNIQUE: profile CPU + memory + GPU in one run, plus
AI-generated optimization suggestions per hot line.

- `uvx scalene --html --outfile profile.html script.py`
- `uvx scalene --reduced-profile script.py` (focus on hot lines)
- `uvx scalene --gpu script.py` (NVIDIA only)
- `uvx scalene --cli script.py` (text output for CI)

Source: https://github.com/plasma-umass/scalene · Skill: `scalene-ai-optimization`

### viztracer — Perfetto-backed timeline

Deterministic tracer. Best for asyncio task-contention diagnosis. NOT for
production (1.5-2x overhead).

- `uvx viztracer python script.py` (produces result.json)
- `uvx viztracer --log_async python my_async_app.py` (asyncio swimlanes)
- `uvx viztracer --output_file trace.html python script.py` (self-contained)
- Open result.json at https://ui.perfetto.dev/

Source: https://github.com/gaogaotiantian/viztracer · Skill: `viztracer-asyncio-timeline`

### pyinstrument — narrative call-tree profiler

Most readable text output among CPU profilers. Good for quick "what's slow?"

- `uvx pyinstrument script.py`
- `uvx pyinstrument --renderer html -o profile.html script.py`

Source: https://github.com/joerick/pyinstrument

### austin — frame stack sampler

Low overhead, exports to FlameGraph / Speedscope.

- `uvx austin -i 1ms python script.py | flamegraph.pl > flame.svg`

Source: https://github.com/P403n1x87/austin

### libcst — Meta's tree-aware codemod library

Preserves whitespace + comments through edits. Used at Instagram on ~20M
LOC. Right tool for mass refactors / API migrations.

- `uv add --dev libcst`
- `python -m libcst.tool initialize .`
- `python -m libcst.tool codemod <module>:CommandName src/`
- `AddImportsVisitor` / `RemoveImportsVisitor` for import hygiene

Source: https://github.com/Instagram/LibCST · Skill: `libcst-codemods`

### rope — symbol rename / extract method

Best for one-off renames where libcst would be overkill.

- `uvx rope_cli rename --old=Foo --new=Bar --module=src/pkg/mod.py`

Source: https://github.com/python-rope/rope

### hypothesis — property-based testing

De facto standard. Strategies, shrinking, stateful machines.

- `uv add --dev hypothesis`
- `@given(x=st.integers())` + `@settings(max_examples=500)`
- `RuleBasedStateMachine` for stateful testing

Source: https://hypothesis.readthedocs.io/ · Skill: `hypothesis-property-based`

### mutmut — mutation testing

88.5% detection, 1200 mutants/min. Best test-quality metric.

- `uvx mutmut run` / `uvx mutmut results` / `uvx mutmut show <id>`
- `uvx mutmut run --use-coverage` (faster — only run touching tests)
- `uvx mutmut html` (HTML report)

Source: https://github.com/boxed/mutmut · Skill: `mutmut-mutation-testing`

### slipcover — low-overhead coverage

5% overhead vs pytest-cov's 180%. Same `coverage.py`-style reports.

- `uvx slipcover --branch -m pytest`
- `uvx slipcover --json --output coverage.json -m pytest`

Source: https://github.com/plasma-umass/slipcover

### testcontainers — real backends in tests

Spin up real Postgres / Redis / Kafka / Mongo per session. Replaces mocks.

- `uv add --dev "testcontainers[postgresql]"`
- `with PostgresContainer("postgres:16-alpine") as pg: ...`
- Pair with `pyfakefs` for filesystem.

Source: https://github.com/testcontainers/testcontainers-python · Skill: `testcontainers-integration-testing`

### syrupy — modern snapshot testing

Replaces `pytest-snapshot` / `snapshottest`.

- `uv add --dev syrupy`
- `def test_x(snapshot): assert obj == snapshot`

Source: https://github.com/syrupy-project/syrupy

### respx / vcrpy / pytest-httpx — HTTP mocking

- `respx` — httpx-native (`uv add --dev respx`)
- `vcrpy` — record/replay HTTP fixtures
- `pytest-httpx` — pytest fixtures for httpx

Source: https://lundberg.github.io/respx/ · https://vcrpy.readthedocs.io/

### bandit — Python AST security linter

- `uvx bandit -r src/`
- `uvx bandit -r src/ -ll -f json` (HIGH only, machine-readable)

Source: https://bandit.readthedocs.io/ · Skill: `semgrep-bandit-security-audit`

### semgrep — semantic patterns, multi-language

Huge community ruleset. `--config=auto` picks rules by language.

- `uvx semgrep --config=auto src/`
- `uvx semgrep --config=p/owasp-top-ten src/`
- Custom rules in `semgrep_rules/*.yaml`

Source: https://semgrep.dev/ · Skill: `semgrep-bandit-security-audit`

### pip-audit — PyPA dep CVE audit

- `uvx pip-audit`
- `uvx pip-audit --fix` (update vulnerable deps)
- `uvx pip-audit --format json -o audit.json`

Source: https://pypi.org/project/pip-audit/

### osv-scanner — Google's multi-ecosystem CVE scanner

- `osv-scanner --recursive .`

Source: https://google.github.io/osv-scanner/

### gitleaks / trufflehog — secrets detection

- `gitleaks detect --source=. --no-banner`
- `gitleaks protect --staged` (pre-commit)
- `trufflehog filesystem --directory=.` (entropy-based alt)

Source: https://github.com/gitleaks/gitleaks

### vulture — dead-code detection

- `uvx vulture src/ tests/`

Source: https://github.com/jendrikseipp/vulture

### loguru — modern structured logging

Replaces stdlib `logging` boilerplate.

- `uv add loguru` → `from loguru import logger; logger.info("...")`

Source: https://github.com/Delgan/loguru

### icecream — `ic()` print debugging

`ic(x)` prints `ic| x: <value>` with source location.

- `uv add --dev icecream`

Source: https://github.com/gruns/icecream

### snoop / pysnooper — line-by-line trace decorator

- `@snoop` decorator → prints every line + variable change.

Source: https://github.com/alexmojaki/snoop

### pudb / pdb++ / web-pdb / debugpy — interactive debug

- `pudb` — curses TUI debugger
- `pdb++` — colorized stdlib pdb
- `web-pdb` — browser-based
- `debugpy` — DAP protocol for IDE attach

### pre-commit — hook framework

- `uvx pre-commit install`
- `uvx pre-commit run --all-files`
- canonical pipeline: ruff + ruff-format + pyrefly + bandit + gitleaks +
  commitizen

Source: https://pre-commit.com/ · Skill: `pre-commit-hook-pipeline`

### commitizen — Conventional Commits + semver + CHANGELOG

- `uvx cz commit` (conformant interactive commit)
- `uvx cz bump --changelog` (semver bump + CHANGELOG.md)
- `uvx cz check --rev-range origin/main..HEAD`

Source: https://commitizen-tools.github.io/commitizen/ · Skill: `commitizen-semver-automation`

### FastAPI / Litestar / Robyn — async web frameworks

- FastAPI — default greenfield
- Litestar — msgspec, ~2x perf
- Robyn — Rust runtime, perf-critical
- Django Ninja — FastAPI-style on Django

Source: https://fastapi.tiangolo.com/ · Skill: `fastapi-litestar-modern-web`

### SQLAlchemy 2.x async + asyncpg

- `uv add "sqlalchemy[asyncio]>=2.0" asyncpg "alembic>=1.13"`
- `Mapped[int]` + `mapped_column(...)` modern declarative
- `selectinload` to avoid N+1
- Alembic for migrations

Source: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html · Skill: `sqlalchemy-2x-async-postgres`

### MADR 4.0 + log4brains / adr-tools / adr-kit — ADRs

MADR 4.0 = de facto 2026 ADR format. Tooling choices:
- `log4brains` (visual UI / static site)
- `adr-tools` (npryce, minimal shell)
- `adr-kit` (Python toolkit with validation + indexing + enforcement)
- pure Markdown under `docs/adr/NNNN-title.md`

Source: https://adr.github.io/madr/ · Skill: `log4brains-adr-management`

### OpenTelemetry Python — traces + metrics + logs

Vendor-neutral. Backends: Honeycomb / Datadog / Sentry / Grafana Tempo /
New Relic / Jaeger.

- `uv add opentelemetry-distro opentelemetry-exporter-otlp`
- `uvx opentelemetry-bootstrap -a install` (auto-instrument detected libs)
- `opentelemetry-instrument --service_name X uv run uvicorn app:app`

Source: https://opentelemetry.io/docs/languages/python/ · Skill: `opentelemetry-observability`

### Continuous profiling — Pyroscope / Sentry Profiling / Datadog

Low-overhead always-on CPU+memory profiling in prod. Complements OTel
traces.

- Sentry: `sentry_sdk.init(profiles_sample_rate=0.1)`
- Pyroscope: agent + py-spy under the hood
- Datadog: bundled with APM

### uvloop — drop-in faster asyncio event loop

- `uv add uvloop`
- `import uvloop; uvloop.install()` before `asyncio.run`
- OR `uvicorn --loop uvloop`
- 20-40% throughput boost on I/O-bound endpoints

Source: https://uvloop.readthedocs.io/

### anyio — multi-runtime async (asyncio + trio)

- `uv add anyio` — write code that runs on either backend.

Source: https://anyio.readthedocs.io/

### trio — opinionated structured-concurrency lib

- `uv add trio` — nurseries instead of bare tasks.

Source: https://trio.readthedocs.io/

### Optimization stack — JAX / Numba / Cython / mypyc / Mojo

For CPU-bound hot paths after profiling confirms.

- JAX — Google autodiff + JIT (XLA backend)
- Numba — `@jit` decorator, GPU optional
- Cython — manual annotations for C-speed
- mypyc — type-hint-guided compilation
- Mojo (Modular) — Python superset, MLIR backend

### Parallelism — Ray / dask / joblib

- Ray — distributed actors + tasks
- dask — pandas/NumPy-shaped parallelism
- joblib — `Parallel(n_jobs=-1)(delayed(f)(x) for x in xs)`

### Caching — functools / cachetools / aiocache / redis-py

- `functools.cache` / `functools.lru_cache`
- `cachetools.TTLCache`
- `aiocache` for async
- `redis-py` for external Redis

### Packaging — hatchling / flit / pyproject.toml / src/ layout

- `hatchling` — modern PEP 517 backend, default in `uv init --package`
- `flit` — simpler, libraries
- `pyproject.toml` — PEPs 517/518/621/660
- `src/` layout — mandatory to prevent dev-tree accidental imports
