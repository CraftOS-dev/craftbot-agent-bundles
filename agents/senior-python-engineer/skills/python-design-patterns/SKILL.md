<!--
Source: https://github.com/wshobson/agents/blob/main/plugins/python-development/skills/python-design-patterns/SKILL.md
Repo: wshobson/agents
-->
---
name: python-design-patterns
description: Python design patterns including KISS, Separation of Concerns, Single Responsibility, and composition over inheritance.
---

# Python Design Patterns

Write maintainable Python code using fundamental design principles. These patterns help you build systems that are easy to understand, test, and modify.

## When to Use This Skill

- Designing new components or services
- Refactoring complex or tangled code
- Deciding whether to create an abstraction
- Choosing between inheritance and composition
- Evaluating code complexity and coupling
- Planning modular architectures

## Core Concepts

### 1. KISS (Keep It Simple)
Choose the simplest solution that works. Complexity must be justified by concrete requirements.

### 2. Single Responsibility (SRP)
Each unit should have one reason to change. Separate concerns into focused components.

### 3. Composition Over Inheritance
Build behavior by combining objects, not extending classes.

### 4. Rule of Three
Wait until you have three instances before abstracting. Duplication is often better than premature abstraction.

## Quick Start

```python
# Simple beats clever
FORMATTERS = {"json": JsonFormatter, "csv": CsvFormatter}

def get_formatter(name: str) -> Formatter:
    return FORMATTERS[name]()
```

## Best Practices Summary

1. Keep it simple — choose the simplest solution that works
2. Single responsibility — each unit has one reason to change
3. Separate concerns — distinct layers with clear purposes
4. Compose, don't inherit — combine objects for flexibility
5. Rule of three — wait before abstracting
6. Keep functions small — 20-50 lines, one purpose
7. Inject dependencies — constructor injection for testability
8. Delete before abstracting — remove dead code, then consider patterns
9. Test each layer — isolated tests for each concern
10. Explicit over clever — readable code beats elegant code

## Troubleshooting

**A class is growing and seems to have multiple responsibilities, but splitting it feels wrong.**
Apply the "reason to change" test: list every change that could require editing this class. If the list has items from different domains (e.g., HTTP parsing AND business rules AND formatting), split it.

**Injecting all dependencies through the constructor is producing constructors with 7+ parameters.**
This is a sign of too many responsibilities in one class, not a problem with dependency injection. Split the class first.

**Composition is producing deeply nested wrapper objects that are hard to trace.**
Keep composition shallow (2-3 levels). Consider a Protocol-based approach or simple function composition.

**The rule of three says not to abstract yet, but duplication is causing bugs when one copy is updated but not the other.**
Duplication that diverges in dangerous ways should be abstracted sooner. If copies are already diverging incorrectly, extract immediately.

**A service layer is importing from the API layer, breaking the dependency direction.**
Layering violation. The service layer must not import from handlers. Introduce a shared types/models layer that both import from. (API → Service → Repository.)
