<!--
Source: https://github.com/Instagram/LibCST · https://libcst.readthedocs.io/
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# libcst — Tree-Aware Codemods

`libcst` (Meta/Instagram) is a Concrete Syntax Tree library that PRESERVES
whitespace, comments, and formatting through edits — making it the right
tool for mass codebase rewrites. Used at Instagram for codemods across
~20M LOC and forms the engine behind `pyre`, `usort`, `Bowler`, and many
internal Meta refactoring pipelines.

This is the 2026 SOTA for any tree-aware refactor more sophisticated than
`ruff --fix` can do. Pair with `using-git-worktrees` to keep refactors
isolated.

## When to use this skill

- Rename a symbol with API-level awareness (not just text-replace)
- Migrate a deprecated API call site-by-site
- Bulk-add type annotations from a stub
- Mechanical refactors across many files where formatting MUST be preserved
- Custom lint rules that need tree inspection
- Transpiling old syntax to new (where `ruff --select=UP` isn't enough)

Do NOT use libcst when: `ruff --select=UP,SIM,RUF --fix` handles it (faster);
`rope` does it (rope is better for one-off rename in an IDE-like flow); a
regex really would suffice.

## Setup

```bash
uv add --dev libcst
# Initialize a project to host your codemods
uv run python -m libcst.tool initialize .
# Creates libcst.codemod.yaml with default config
```

## Common recipes

### Recipe 1 — Anatomy of a Codemod

```python
# src/my_codemods/rename_logger.py
"""Rename `from logging import getLogger as gL` to `gl`."""
import libcst as cst
from libcst.codemod import VisitorBasedCodemodCommand
from libcst.codemod.visitors import AddImportsVisitor

class RenameLoggerCommand(VisitorBasedCodemodCommand):
    DESCRIPTION = "Rename `gL` import alias to `gl`."

    def leave_ImportAlias(
        self,
        original_node: cst.ImportAlias,
        updated_node: cst.ImportAlias,
    ) -> cst.ImportAlias:
        if (
            isinstance(original_node.asname, cst.AsName)
            and isinstance(original_node.asname.name, cst.Name)
            and original_node.asname.name.value == "gL"
        ):
            return updated_node.with_changes(
                asname=cst.AsName(name=cst.Name("gl"))
            )
        return updated_node

    def leave_Name(
        self, original_node: cst.Name, updated_node: cst.Name
    ) -> cst.Name:
        if original_node.value == "gL":
            return updated_node.with_changes(value="gl")
        return updated_node
```

Run it:

```bash
python -m libcst.tool codemod my_codemods.rename_logger.RenameLoggerCommand src/
```

LibCST traverses every `.py` file under `src/`, applies the visitor, writes
modified files in place. Whitespace and comments are preserved.

### Recipe 2 — Rename a symbol globally

```python
class RenameSymbolCommand(VisitorBasedCodemodCommand):
    DESCRIPTION = "Rename Foo → Bar everywhere."

    def __init__(self, context, old: str, new: str) -> None:
        super().__init__(context)
        self.old = old
        self.new = new

    def leave_Name(self, original_node, updated_node):
        if original_node.value == self.old:
            return updated_node.with_changes(value=self.new)
        return updated_node

    def leave_Attribute(self, original_node, updated_node):
        # Handle `pkg.Foo` access
        if (
            isinstance(updated_node.attr, cst.Name)
            and updated_node.attr.value == self.old
        ):
            return updated_node.with_changes(
                attr=cst.Name(self.new)
            )
        return updated_node
```

```bash
python -m libcst.tool codemod \
    my_codemods.rename_symbol.RenameSymbolCommand \
    --old=Foo --new=Bar \
    src/
```

### Recipe 3 — Deprecation cleanup (Instagram pattern)

```python
class RemoveDeprecatedKwarg(VisitorBasedCodemodCommand):
    """Remove `legacy=True` kwarg from `client.fetch()` calls."""

    def leave_Call(self, original_node, updated_node):
        # Match calls to client.fetch
        if not self._is_target_call(updated_node):
            return updated_node
        new_args = tuple(
            arg for arg in updated_node.args
            if not (
                isinstance(arg.keyword, cst.Name)
                and arg.keyword.value == "legacy"
            )
        )
        return updated_node.with_changes(args=new_args)

    def _is_target_call(self, node: cst.Call) -> bool:
        func = node.func
        return (
            isinstance(func, cst.Attribute)
            and isinstance(func.attr, cst.Name)
            and func.attr.value == "fetch"
        )
```

### Recipe 4 — API migration (e.g., `requests.get` → `httpx.get`)

```python
from libcst.codemod.visitors import AddImportsVisitor, RemoveImportsVisitor

class RequestsToHttpx(VisitorBasedCodemodCommand):
    def leave_Call(self, original_node, updated_node):
        if not self._is_requests_call(updated_node):
            return updated_node
        AddImportsVisitor.add_needed_import(self.context, "httpx")
        RemoveImportsVisitor.remove_unused_import(
            self.context, "requests", obj="get"
        )
        return updated_node.with_changes(
            func=cst.Attribute(
                value=cst.Name("httpx"),
                attr=updated_node.func.attr,
            ),
        )

    def _is_requests_call(self, node: cst.Call) -> bool:
        return (
            isinstance(node.func, cst.Attribute)
            and isinstance(node.func.value, cst.Name)
            and node.func.value.value == "requests"
            and node.func.attr.value in {"get", "post", "put", "delete"}
        )
```

`AddImportsVisitor` and `RemoveImportsVisitor` handle import hygiene
automatically — libcst's killer feature for migrations.

### Recipe 5 — Bulk add type annotations from a stub

```python
import libcst as cst
from libcst.codemod.visitors import ApplyTypeAnnotationsVisitor

# Given my_module.pyi alongside my_module.py
visitor = ApplyTypeAnnotationsVisitor(
    context=context,
    annotations=cst.parse_module(stub_text),
)
new_module = visitor.transform_module(cst.parse_module(src_text))
```

This is how `pyre infer` adds types — leverage it for projects migrating
from untyped to fully typed.

### Recipe 6 — Run interactively

```bash
python -m libcst.tool codemod \
    my_codemods.rename_symbol.RenameSymbolCommand \
    --old=Foo --new=Bar \
    --jobs=8 \
    src/
```

`--jobs` parallelises the codemod across CPU cores. For 10k+ file repos,
this is the difference between minutes and seconds.

### Recipe 7 — Dry-run / preview

```bash
# Use git to preview
git stash
python -m libcst.tool codemod my_codemods.X src/
git diff > codemod.diff
git stash pop                 # discard codemod
# Review codemod.diff, decide whether to apply
```

LibCST doesn't ship `--dry-run` natively, but git makes this trivial.

### Recipe 8 — CI-side codemod (gate / autofix)

Run codemods inside pre-commit or CI to enforce migrations. Combine with a
worktree (`using-git-worktrees` skill) so the codemod commits land on a
dedicated branch.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: rename-old-api
        name: Rename old API
        entry: python -m libcst.tool codemod my_codemods.X
        language: system
        types: [python]
```

## Patterns from Instagram-scale codemods

These come from public Instagram engineering posts:

1. **One codemod, one concern.** Don't chain semantically distinct changes
   in a single codemod. Each codemod = one commit = one PR.
2. **Tests first.** Each codemod ships with a `test_codemod_X.py` that uses
   `CodemodTest` to assert `BEFORE → AFTER` on representative inputs.
3. **Idempotent.** Running the codemod twice should be a no-op.
4. **Reversible when possible.** Authoring a `Reverse<X>Command` for risky
   migrations is cheap insurance.
5. **Land in batches.** For 1000+ file changes, split by directory or
   ownership rather than one giant PR.
6. **Verify via CI, not eyeball.** Diff is too large to review line-by-line;
   trust the test suite + the codemod's own unit tests.

## Edge cases

- **Comments inside expressions**: LibCST keeps them but they can land in
  surprising spots after edits. Eyeball-review samples of the output.
- **`__init__.py` re-exports**: rename codemods must also update `__all__`
  lists. Add a separate visitor for `__all__` literals.
- **String references**: if `"Foo"` is used as a literal string (e.g.,
  pydantic discriminators, dynamic imports), libcst won't catch it. Combine
  with a `Grep` pass for literals.
- **Multi-line decorators**: edits preserve indentation, but inserting/
  removing decorators can break syntax. Test thoroughly.
- **Pyi stubs**: codemods don't auto-sync `.pyi` files. Either edit both or
  rely on stubgen post-codemod.
- **Whitespace-sensitive corners**: f-string internals, triple-quoted
  docstrings — usually fine but always test.

## Comparison

| Tool | When to use |
|---|---|
| `ruff --select=UP --fix` | mechanical syntax modernization (3.10+ idioms) — fastest |
| `libcst` | bespoke tree-aware migrations, API renames, type stub merge — most powerful |
| `rope` | IDE-style single rename, extract method — interactive |
| `Bowler` | DEPRECATED — use libcst directly |
| `lib2to3` | DEPRECATED (removed in 3.13) — use libcst |
| `ast` + `ast.unparse` | quick scripts, but DOESN'T preserve formatting — avoid for mass refactors |

## Sources

- https://github.com/Instagram/LibCST — source
- https://libcst.readthedocs.io/ — full docs
- https://libcst.readthedocs.io/en/latest/codemods.html — codemod tutorial
- https://libcst.readthedocs.io/en/latest/codemods_tutorial.html — step-by-step
- https://instagram-engineering.com/static-analysis-at-scale-an-instagram-story-8f498ab71a0c — Instagram codemod history
- https://github.com/Instagram/LibCST/tree/main/libcst/codemod/commands — pre-built codemods
