---
name: pytest-markdown-docs-validation
description: Validate Python code fences in markdown docs by executing them under pytest. Modal Labs' `pytest-markdown-docs` (primary), `mktestdocs` (alternative). Use when guaranteeing tutorial / README examples run end-to-end and never drift from the implementation.
---

# pytest-markdown-docs — Executable Doc Validation

`pytest-markdown-docs` (Modal Labs) executes every Python code fence in a markdown file as a pytest case. It's the de facto solution for "the doc examples must keep working" in Python projects.

For non-Python or simpler setups, `mktestdocs` is the alternative.

## When to use this skill

- The user writes Python tutorials, READMEs, or reference docs with executable code fences.
- The user wants CI to fail when a code example stops working.
- The user wants per-fence isolation (each fence runs in its own session OR shares state via fixtures).

## Setup

### Install

```bash
# Recommended — uv
uv add --dev pytest pytest-markdown-docs

# Or pip
pip install --dev pytest pytest-markdown-docs
```

### Configure pytest

`pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--markdown-docs"
markdown-docs-types = ["python", "python3", "pycon"]
```

Or `pytest.ini`:

```ini
[pytest]
addopts = --markdown-docs
markdown-docs-types = python python3 pycon
```

## Common recipes

### Recipe 1: Validate a single file

```bash
pytest --markdown-docs README.md
```

### Recipe 2: Validate the whole docs tree

```bash
pytest --markdown-docs docs/
```

### Recipe 3: Mix with normal test discovery

```bash
pytest --markdown-docs tests/ docs/ README.md
```

`pytest` runs both `tests/` and the markdown fences in one invocation.

### Recipe 4: Skip a fence

Add a comment directly before the fence:

````markdown
<!--pytest-codeblocks:skip-->
```python
# this fence won't be executed (illustrative pseudocode)
```
````

Or with metadata:

````markdown
```python
# pytest-markdown-docs: skip
my_pseudocode()
```
````

### Recipe 5: Share state across fences in one file

````markdown
```python
import datetime
now = datetime.datetime.now()
```

Now we can reference `now`:

```python
print(now.year)   # works — state persists per-file
```
````

By default, fences in a single file share state (run sequentially in one pytest session). Disable per-file with `--markdown-docs-isolation=session-per-file` flag.

### Recipe 6: Fixtures and parametrization

`conftest.py`:

```python
import pytest

@pytest.fixture(autouse=True)
def patch_env(monkeypatch):
    monkeypatch.setenv("ACME_API_KEY", "sk-test-fake")
```

Fixtures apply to markdown fences too — useful for mocking auth, network, time.

### Recipe 7: Expected-output assertions

For doctest-style fences (`pycon`):

````markdown
```pycon
>>> 1 + 2
3
>>> "hello".upper()
'HELLO'
```
````

`pytest-markdown-docs` runs these as doctest equivalents and asserts the output matches.

### Recipe 8: CI integration

```yaml
# .github/workflows/docs-test.yml
name: Docs Test
on:
  pull_request:
    paths: ['**/*.md', 'docs/**']
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --dev
      - run: uv run pytest --markdown-docs docs/ README.md
```

### Recipe 9: Validating type hints with mypy in docs

After fence execution passes, run mypy on extracted code (advanced):

```bash
# extract fences to a temp dir
uv run python -m pytest_markdown_docs --extract docs/ -o /tmp/extracted/
mypy /tmp/extracted/
```

## Alternative: mktestdocs

For simpler setups or non-pytest projects:

```bash
uv add --dev mktestdocs
```

```python
# tests/test_docs.py
from mktestdocs import check_md_file
import pathlib

@pytest.mark.parametrize("fpath", pathlib.Path("docs").glob("**/*.md"))
def test_docs(fpath):
    check_md_file(fpath=fpath, memory=True)
```

mktestdocs is a thinner library — you wire pytest yourself. Use it when `pytest-markdown-docs` is overkill.

## Anti-patterns the agent avoids

- **Hidden side effects:** fences that write to disk, call external APIs, or modify shared state without cleanup. Use `tmp_path` fixture + monkeypatched env vars.
- **Network calls without mocks:** every external HTTP/DB call must be mocked (`responses`, `pytest-httpx`, fixture).
- **Hardcoded paths:** `/Users/<name>/...` in docs — replace with `pathlib.Path.home()` or `tmp_path`.
- **Long-running fences:** if a fence sleeps or trains a model, mark it `skip` and run separately.

## Edge cases

- **Async code:** `pytest-asyncio` plays nice; mark fences that use `asyncio.run(...)` and they execute synchronously.
- **`importlib` and package layout:** if fences import the package under test, ensure `pip install -e .` ran first.
- **Jupyter notebooks (.ipynb):** pytest-markdown-docs is markdown only. For notebooks, use `nbval` or `papermill`.
- **Non-Python fences:** ignored by default; pair with language-specific runners if needed.

## Sources

- pytest-markdown-docs: https://github.com/modal-labs/pytest-markdown-docs
- mktestdocs: https://github.com/koaning/mktestdocs
- Modal Labs writeup: https://modal.com/blog/pytest-markdown-docs
