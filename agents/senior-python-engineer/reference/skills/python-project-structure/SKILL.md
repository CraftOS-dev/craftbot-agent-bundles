<!--
Source: https://github.com/wshobson/agents/blob/main/plugins/python-development/skills/python-project-structure/SKILL.md
Repo: wshobson/agents
-->
# Python Project Structure & Module Architecture

Design well-organized Python projects with clear module boundaries, explicit public interfaces, and maintainable directory structures.

## When to Use This Skill

- Starting a new Python project from scratch
- Reorganizing an existing codebase for clarity
- Defining module public APIs with `__all__`
- Deciding between flat and nested directory structures
- Determining test file placement strategies
- Creating reusable library packages

## Core Concepts

### 1. Module Cohesion
Group related code that changes together. A module should have a single, clear purpose.

### 2. Explicit Interfaces
Define what's public with `__all__`. Everything not listed is an internal implementation detail.

### 3. Flat Hierarchies
Prefer shallow directory structures. Add depth only for genuine sub-domains.

### 4. Consistent Conventions
Apply naming and organization patterns uniformly across the project.

## Quick Start

```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── services/
│       ├── models/
│       └── api/
├── tests/
├── pyproject.toml
└── README.md
```

## Fundamental Patterns

### Pattern 1: One Concept Per File

```python
# Good: Focused files
# user_service.py - User business logic
# user_repository.py - User data access
# user_models.py - User data structures

# Avoid: Kitchen sink files
# user.py - Contains service, repository, models, utilities...
```

Consider splitting when a file:
- Handles multiple unrelated responsibilities
- Grows beyond 300-500 lines
- Contains classes that change for different reasons

### Pattern 2: Explicit Public APIs with `__all__`

```python
# mypackage/services/__init__.py
from .user_service import UserService
from .order_service import OrderService
from .exceptions import ServiceError, ValidationError

__all__ = [
    "UserService",
    "OrderService",
    "ServiceError",
    "ValidationError",
]
```

### Pattern 3: Flat Directory Structure

```
# Preferred
project/
├── api/
│   ├── routes.py
│   └── middleware.py
├── services/
│   ├── user_service.py
│   └── order_service.py
├── models/
│   ├── user.py
│   └── order.py
└── utils/
    └── validation.py

# Avoid: Deep nesting
project/core/internal/services/impl/user/
```

### Pattern 4: Test File Organization

**Option A: Colocated Tests** — tests live next to code they verify.

```
src/
├── user_service.py
├── test_user_service.py
├── order_service.py
└── test_order_service.py
```

**Option B: Parallel Test Directory** — standard for larger projects.

```
src/
├── services/
│   ├── user_service.py
│   └── order_service.py
tests/
├── services/
│   ├── test_user_service.py
│   └── test_order_service.py
```

## Advanced Patterns

### Pattern 5: Package Initialization

```python
# mypackage/__init__.py
"""MyPackage - A library for doing useful things."""

from .core import MainClass, HelperClass
from .exceptions import PackageError, ConfigError
from .config import Settings

__all__ = [
    "MainClass",
    "HelperClass",
    "PackageError",
    "ConfigError",
    "Settings",
]

__version__ = "1.0.0"
```

### Pattern 6: Layered Architecture

```
myapp/
├── api/           # HTTP handlers, request/response
│   ├── routes/
│   └── middleware/
├── services/      # Business logic
├── repositories/  # Data access
├── models/        # Domain entities
├── schemas/       # API schemas (Pydantic)
└── config/        # Configuration
```

Each layer should only depend on layers below it, never above.

### Pattern 7: Domain-Driven Structure

```
ecommerce/
├── users/
│   ├── models.py
│   ├── services.py
│   ├── repository.py
│   └── api.py
├── orders/
│   ├── models.py
│   ├── services.py
│   ├── repository.py
│   └── api.py
└── shared/
    ├── database.py
    └── exceptions.py
```

## File and Module Naming

- Use `snake_case` for all file and module names: `user_repository.py`
- Avoid abbreviations: `user_repository.py` not `usr_repo.py`
- Match class names to file names: `UserService` in `user_service.py`

### Import Style

```python
# Preferred: Absolute imports
from myproject.services import UserService
from myproject.models import User

# Avoid: Relative imports
from ..services import UserService
from . import models
```

## Best Practices Summary

1. Keep files focused — one concept per file, consider splitting at 300-500 lines
2. Define `__all__` explicitly — make public interfaces clear
3. Prefer flat structures — add depth only for genuine sub-domains
4. Use absolute imports — more reliable and clearer
5. Be consistent — apply patterns uniformly across the project
6. Match names to content — file names should describe their purpose
7. Separate concerns — keep layers distinct and dependencies flowing one direction
8. Document your structure — include a README explaining the organization
