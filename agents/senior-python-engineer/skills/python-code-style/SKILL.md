<!--
Source: https://github.com/wshobson/agents/blob/main/plugins/python-development/skills/python-code-style/SKILL.md
Repo: wshobson/agents
-->
# Python Code Style & Documentation

Consistent code style and clear documentation make codebases maintainable and collaborative. This skill covers modern Python tooling, naming conventions, and documentation standards.

## When to Use This Skill

- Setting up linting and formatting for a new project
- Writing or reviewing docstrings
- Establishing team coding standards
- Configuring ruff, mypy, or pyright
- Reviewing code for style consistency
- Creating project documentation

## Core Concepts

### 1. Automated Formatting
Let tools handle formatting debates. Configure once, enforce automatically.

### 2. Consistent Naming
Follow PEP 8 conventions with meaningful, descriptive names.

### 3. Documentation as Code
Docstrings should be maintained alongside the code they describe.

### 4. Type Annotations
Modern Python code should include type hints for all public APIs.

## Quick Start

```bash
pip install ruff mypy
```

```toml
[tool.ruff]
line-length = 120
target-version = "py312"

[tool.mypy]
strict = true
```

## Fundamental Patterns

### Pattern 1: Modern Python Tooling (ruff)

Use `ruff` as an all-in-one linter and formatter. It replaces flake8, isort, and black with a single fast tool.

```toml
[tool.ruff]
line-length = 120
target-version = "py312"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "SIM"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

```bash
ruff check --fix .
ruff format .
```

### Pattern 2: Type Checking (mypy strict)

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

### Pattern 3: Naming Conventions

- Files/modules: `user_repository.py`, `order_processing.py`, `http_client.py` (snake_case)
- Classes: `UserRepository`, `HTTPClientFactory` (PascalCase, acronyms stay uppercase)
- Functions/variables: `get_user_by_email`, `retry_count` (snake_case)
- Constants: `MAX_RETRY_ATTEMPTS`, `DEFAULT_TIMEOUT_SECONDS` (SCREAMING_SNAKE_CASE)

### Pattern 4: Import Organization

```python
# Standard library
import os
from collections.abc import Callable
from typing import Any

# Third-party packages
import httpx
from pydantic import BaseModel
from sqlalchemy import Column

# Local imports
from myproject.models import User
from myproject.services import UserService
```

Use absolute imports exclusively.

### Pattern 5: Google-Style Docstrings

```python
def process_batch(
    items: list[Item],
    max_workers: int = 4,
    on_progress: Callable[[int, int], None] | None = None,
) -> BatchResult:
    """Process items concurrently using a worker pool.

    Args:
        items: The items to process. Must not be empty.
        max_workers: Maximum concurrent workers. Defaults to 4.
        on_progress: Optional callback receiving (completed, total) counts.

    Returns:
        BatchResult containing succeeded items and any failures.

    Raises:
        ValueError: If items is empty.
        ProcessingError: If the batch cannot be processed.
    """
    ...
```

### Pattern 6: Line Length and Formatting

120 characters for modern displays. Break method chains, format long strings as f-string sequences.

## Best Practices Summary

1. Use ruff — single tool for lint + format
2. Enable strict mypy — catch type errors before runtime
3. 120 character lines
4. Descriptive names — clarity over brevity
5. Absolute imports
6. Google-style docstrings
7. Document public APIs
8. Keep docs updated
9. Automate in CI
10. Target Python 3.10+ (3.12+ for new projects)
