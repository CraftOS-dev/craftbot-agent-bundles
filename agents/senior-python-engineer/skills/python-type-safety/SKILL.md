<!--
Source: https://github.com/wshobson/agents/blob/main/plugins/python-development/skills/python-type-safety/SKILL.md
Repo: wshobson/agents
-->
---
name: python-type-safety
description: Python type safety with type hints, generics, protocols, and strict type checking. Use when adding type annotations, implementing generic classes, defining structural interfaces, or configuring mypy/pyright.
---

# Python Type Safety

Leverage Python's type system to catch errors at static analysis time. Type annotations serve as enforced documentation that tooling validates automatically.

## When to Use This Skill

- Adding type hints to existing code
- Creating generic, reusable classes
- Defining structural interfaces with protocols
- Configuring mypy or pyright for strict checking
- Understanding type narrowing and guards
- Building type-safe APIs and libraries

## Core Concepts

### 1. Type Annotations
Declare expected types for function parameters, return values, and variables.

### 2. Generics
Write reusable code that preserves type information across different types.

### 3. Protocols
Define structural interfaces without inheritance (duck typing with type safety).

### 4. Type Narrowing
Use guards and conditionals to narrow types within code blocks.

## Quick Start

```python
def get_user(user_id: str) -> User | None:
    ...

user = get_user("123")
if user is None:
    raise UserNotFoundError("123")
print(user.name)  # Type checker knows user is User here
```

## Fundamental Patterns

### Pattern 1: Annotate All Public Signatures

```python
def get_user(user_id: str) -> User:
    ...

def process_batch(
    items: list[Item],
    max_workers: int = 4,
) -> BatchResult[ProcessedItem]:
    ...

class UserRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def find_by_id(self, user_id: str) -> User | None:
        ...

    async def find_by_email(self, email: str) -> User | None:
        ...

    async def save(self, user: User) -> User:
        ...
```

Use `mypy --strict` or `pyright` in CI to catch type errors early.

### Pattern 2: Modern Union Syntax

```python
# Preferred (Python 3.10+)
def find_user(user_id: str) -> User | None:
    ...

def parse_value(v: str) -> int | float | str:
    ...

# Older style (still valid, needed for 3.9)
from typing import Optional, Union

def find_user(user_id: str) -> Optional[User]:
    ...
```

### Pattern 3: Type Narrowing with Guards

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

### Pattern 4: Generic Classes

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

    @property
    def is_failure(self) -> bool:
        return self._error is not None

    def unwrap(self) -> T:
        if self._error is not None:
            raise self._error
        return self._value  # type: ignore[return-value]

    def unwrap_or(self, default: T) -> T:
        if self._error is not None:
            return default
        return self._value  # type: ignore[return-value]
```

## Best Practices Summary

1. Annotate all public APIs — functions, methods, class attributes
2. Use `T | None` — modern union syntax over `Optional[T]`
3. Run strict type checking — `mypy --strict` in CI
4. Use generics — preserve type info in reusable code
5. Define protocols — structural typing for interfaces
6. Narrow types — use guards to help the type checker
7. Bound type vars — restrict generics to meaningful types
8. Create type aliases — meaningful names for complex types
9. Minimize `Any` — use specific types or generics
10. Document with types — types are enforceable documentation
