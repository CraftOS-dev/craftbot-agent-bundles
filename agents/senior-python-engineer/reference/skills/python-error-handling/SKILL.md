<!--
Source: https://github.com/wshobson/agents/blob/main/plugins/python-development/skills/python-error-handling/SKILL.md
Repo: wshobson/agents
-->
---
name: python-error-handling
description: Python error handling patterns including input validation, exception hierarchies, and partial failure handling. Use when implementing validation logic, designing exception strategies, handling batch processing failures, or building robust APIs.
---

# Python Error Handling

Build robust Python applications with proper input validation, meaningful exceptions, and graceful failure handling.

## When to Use This Skill

- Validating user input and API parameters
- Designing exception hierarchies for applications
- Handling partial failures in batch operations
- Converting external data to domain types
- Building user-friendly error messages
- Implementing fail-fast validation patterns

## Core Concepts

### 1. Fail Fast
Validate inputs early, before expensive operations. Report all validation errors at once when possible.

### 2. Meaningful Exceptions
Use appropriate exception types with context. Messages should explain what failed, why, and how to fix it.

### 3. Partial Failures
In batch operations, don't let one failure abort everything. Track successes and failures separately.

### 4. Preserve Context
Chain exceptions to maintain the full error trail for debugging.

## Quick Start

```python
def fetch_page(url: str, page_size: int) -> Page:
    if not url:
        raise ValueError("'url' is required")
    if not 1 <= page_size <= 100:
        raise ValueError(f"'page_size' must be 1-100, got {page_size}")
    # Now safe to proceed...
```

## Fundamental Patterns

### Pattern 1: Early Input Validation

```python
def process_order(
    order_id: str,
    quantity: int,
    discount_percent: float,
) -> OrderResult:
    if not order_id:
        raise ValueError("'order_id' is required")
    if quantity <= 0:
        raise ValueError(f"'quantity' must be positive, got {quantity}")
    if not 0 <= discount_percent <= 100:
        raise ValueError(
            f"'discount_percent' must be 0-100, got {discount_percent}"
        )
    return _process_validated_order(order_id, quantity, discount_percent)
```

### Pattern 2: Convert to Domain Types Early

```python
from enum import Enum

class OutputFormat(Enum):
    JSON = "json"
    CSV = "csv"
    PARQUET = "parquet"

def parse_output_format(value: str) -> OutputFormat:
    try:
        return OutputFormat(value.lower())
    except ValueError:
        valid_formats = [f.value for f in OutputFormat]
        raise ValueError(
            f"Invalid format '{value}'. "
            f"Valid options: {', '.join(valid_formats)}"
        )
```

### Pattern 3: Pydantic for Complex Validation

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
```

### Pattern 4: Map Errors to Standard Exceptions

| Failure Type | Exception | Example |
|--------------|-----------|---------|
| Invalid input | `ValueError` | Bad parameter values |
| Wrong type | `TypeError` | Expected string, got int |
| Missing item | `KeyError` | Dict key not found |
| Operational failure | `RuntimeError` | Service unavailable |
| Timeout | `TimeoutError` | Operation took too long |
| File not found | `FileNotFoundError` | Path doesn't exist |
| Permission denied | `PermissionError` | Access forbidden |

```python
# Good: Specific exception with context
raise ValueError(f"'page_size' must be 1-100, got {page_size}")

# Avoid: Generic exception, no context
raise Exception("Invalid parameter")
```

## Best Practices Summary

1. Validate early — check inputs before expensive operations
2. Use specific exceptions — `ValueError`, `TypeError`, not generic `Exception`
3. Include context — messages should explain what, why, and how to fix
4. Convert types at boundaries — parse strings to enums/domain types early
5. Chain exceptions — use `raise ... from e` to preserve debug info
6. Handle partial failures — don't abort batches on single item errors
7. Use Pydantic — for complex input validation with structured errors
8. Document failure modes — docstrings should list possible exceptions
9. Log with context — include IDs, counts, and other debugging info
10. Test error paths — verify exceptions are raised correctly
