<!--
Source: https://github.com/wshobson/agents/blob/main/plugins/python-development/skills/python-anti-patterns/SKILL.md
Repo: wshobson/agents
-->
# Python Anti-Patterns Checklist

A reference checklist of common mistakes and anti-patterns in Python code. Review this before finalizing implementations to catch issues early.

## When to Use This Skill

- Reviewing code before merge
- Debugging mysterious issues
- Teaching or learning Python best practices
- Establishing team coding standards
- Refactoring legacy code

## Infrastructure Anti-Patterns

### Scattered Timeout/Retry Logic

```python
# BAD
def fetch_user(user_id):
    try:
        return requests.get(url, timeout=30)
    except Timeout:
        logger.warning("Timeout fetching user")
        return None
```

```python
# GOOD: Centralized retry logic
@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def http_get(url: str) -> Response:
    return requests.get(url, timeout=30)
```

### Double Retry

```python
# BAD: Retrying at multiple layers
@retry(max_attempts=3)
def call_service():
    return client.request()  # Client also has retry configured!
```

Retry at one layer only.

### Hard-Coded Configuration

```python
# BAD
DB_HOST = "prod-db.example.com"
API_KEY = "sk-12345"
```

```python
# GOOD
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str = Field(alias="DB_HOST")
    api_key: str = Field(alias="API_KEY")
```

## Architecture Anti-Patterns

### Exposed Internal Types

```python
# BAD
@app.get("/users/{id}")
def get_user(id: str) -> UserModel:  # SQLAlchemy model leaks
    return db.query(UserModel).get(id)
```

```python
# GOOD: Use DTOs
@app.get("/users/{id}")
def get_user(id: str) -> UserResponse:
    user = db.query(UserModel).get(id)
    return UserResponse.from_orm(user)
```

### Mixed I/O and Business Logic

```python
# BAD: SQL inside business logic
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

## Error Handling Anti-Patterns

### Bare Exception Handling

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

### Ignored Partial Failures

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

### Missing Input Validation

```python
# BAD
def create_user(data: dict):
    return User(**data)
```

```python
# GOOD
def create_user(data: dict) -> User:
    validated = CreateUserInput.model_validate(data)
    return User.from_input(validated)
```

## Resource Anti-Patterns

### Unclosed Resources

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

### Blocking in Async

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

## Type Safety Anti-Patterns

### Missing Type Hints

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

### Untyped Collections

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

## Testing Anti-Patterns

### Only Testing Happy Paths

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

### Over-Mocking

Use integration tests for critical paths. Mock only external services.

## Quick Review Checklist

- [ ] No scattered timeout/retry logic (centralized)
- [ ] No double retry (app + infrastructure)
- [ ] No hard-coded configuration or secrets
- [ ] No exposed internal types (ORM models, protobufs)
- [ ] No mixed I/O and business logic
- [ ] No bare `except Exception: pass`
- [ ] No ignored partial failures in batches
- [ ] No missing input validation
- [ ] No unclosed resources (using context managers)
- [ ] No blocking calls in async code
- [ ] All public functions have type hints
- [ ] Collections have type parameters
- [ ] Error paths are tested
- [ ] Edge cases are covered

## Common Fixes Summary

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
