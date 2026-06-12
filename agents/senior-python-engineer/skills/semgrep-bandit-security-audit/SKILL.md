<!--
Source: https://semgrep.dev/ · https://bandit.readthedocs.io/ · https://github.com/pyupio/safety
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# semgrep + bandit — Security Auditing Stack

The 2026 SOTA Python security audit combines `bandit` (Python-specific AST
patterns), `semgrep` (semantic patterns across languages with a huge
community ruleset), `pip-audit` / `osv-scanner` (vulnerable dependencies),
and `gitleaks` (committed secrets). Each catches a different class of
vulnerabilities — run all four.

## When to use this skill

- New project security baseline
- Adding security CI gate to existing repo
- Quarterly security audit of an existing codebase
- Reviewing a security-critical PR (auth, payments, crypto, deserialization)
- Compliance work (PCI, HIPAA, SOC 2 — these tools generate evidence)
- Pre-deployment / pre-release security check

Do NOT use these as a substitute for: pen-testing (semgrep finds known
patterns; pen-test finds zero-days); runtime security (use WAF, RASP);
secret rotation (use a secrets manager).

## Setup

```bash
uv add --dev bandit semgrep
# OR ephemeral
uvx bandit -r src/
uvx semgrep --config=auto src/
uvx pip-audit
gitleaks detect --source=. --no-banner
```

## Common recipes

### Recipe 1 — Bandit baseline

```toml
# pyproject.toml
[tool.bandit]
exclude_dirs = ["tests", ".venv", "build"]
skips = ["B101"]              # asserts in tests are fine
severity = "low"              # report low+

[tool.bandit.assert_used]
skips = ["**/test_*.py", "**/tests/**"]
```

```bash
uvx bandit -r src/                           # report
uvx bandit -r src/ -ll                       # only HIGH severity
uvx bandit -r src/ -f json -o bandit.json    # CI-machine-readable
```

Common bandit findings:
- `B102` exec_used
- `B105`/`B107`/`B108` hardcoded passwords / tmp files
- `B201` flask_debug_true
- `B301`-`B324` insecure deserialization (pickle, marshal, shelve)
- `B501`-`B502` requests with verify=False
- `B602`-`B608` shell=True / SQL injection

Each finding: file:line + severity + confidence + remediation hint.

### Recipe 2 — Semgrep auto-scan

```bash
uvx semgrep --config=auto src/               # uses semgrep registry default ruleset
uvx semgrep --config=p/python src/           # Python pack
uvx semgrep --config=p/security-audit src/   # security pack
uvx semgrep --config=p/owasp-top-ten src/    # OWASP
uvx semgrep --config=p/secrets src/          # secrets in code
```

Semgrep ruleset library: https://semgrep.dev/explore — thousands of curated
rules. The `auto` config picks rules based on language detection.

### Recipe 3 — Semgrep custom rule

```yaml
# semgrep_rules/no_eval_on_user_input.yaml
rules:
  - id: no-eval-on-user-input
    pattern: eval($USER_INPUT)
    message: "eval() on user-controlled input is RCE."
    severity: ERROR
    languages: [python]
```

```bash
uvx semgrep --config=semgrep_rules/ src/
```

Custom rules let you encode project-specific security invariants (e.g.,
"never call raw_sql with untrusted input").

### Recipe 4 — Dependency audit (pip-audit)

```bash
uvx pip-audit                                # against current env
uvx pip-audit -r requirements.txt            # against a lockfile
uvx pip-audit --format json -o audit.json   # CI-machine-readable
uvx pip-audit --fix                          # update vulnerable deps
```

`pip-audit` is PyPA-maintained; queries the OSV database. For broader
ecosystem coverage, use `osv-scanner`:

```bash
osv-scanner --recursive .                    # scan all manifests + lockfiles
```

### Recipe 5 — Secret scanning (gitleaks)

```bash
gitleaks detect --source=. --no-banner       # scan working tree
gitleaks detect --source=. --no-banner --redact
gitleaks protect --staged --no-banner        # pre-commit check
```

```yaml
# .gitleaks.toml
[allowlist]
files = ["**/fixtures/test_data.json"]
regexes = ["EXAMPLE_KEY"]
```

Pre-commit hook (see `pre-commit-hook-pipeline` skill) catches secrets
before they're committed. `trufflehog` is an alternative with more entropy-
based detection.

### Recipe 6 — Full security pipeline (CI)

```yaml
# GitHub Actions — security.yml
name: Security
on: [pull_request, push]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --frozen

      - name: bandit
        run: uv run bandit -r src/ -ll -f sarif -o bandit.sarif

      - name: semgrep
        run: uvx semgrep --config=auto --sarif --output=semgrep.sarif src/

      - name: pip-audit
        run: uvx pip-audit --format json -o pip-audit.json
        continue-on-error: false

      - name: gitleaks
        uses: gitleaks/gitleaks-action@v2
        env: { GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} }

      - uses: github/codeql-action/upload-sarif@v3
        with: { sarif_file: bandit.sarif }
```

SARIF output is read natively by GitHub's Security tab — findings appear
inline on PRs.

### Recipe 7 — Severity-driven gate

```bash
# Fail build if any HIGH severity findings
uvx bandit -r src/ -ll -f json -o bandit.json
test "$(jq '.results | map(select(.issue_severity == "HIGH")) | length' bandit.json)" -eq 0
```

Calibrate thresholds: HIGH always blocks; MEDIUM blocks unless tagged
`security-exception`; LOW reports without blocking.

### Recipe 8 — False-positive management

For bandit:

```python
import subprocess
subprocess.run(["echo", "hello"], shell=True)  # nosec B602 — controlled input
```

For semgrep:

```python
sql = f"SELECT * FROM t WHERE id = {id}"  # nosemgrep: tainted-sql
```

Use sparingly. Document WHY the suppression is safe in the same line (`#
nosec B602 — input is controlled, not user-facing`). Suppressions
without explanations should fail review.

### Recipe 9 — Common CWE coverage

| CWE | Caught by |
|---|---|
| CWE-78 (OS command injection) | bandit B602/B603 + semgrep |
| CWE-89 (SQL injection) | bandit B608 + semgrep |
| CWE-94 (code injection / eval) | bandit B102 + semgrep |
| CWE-200 (information exposure) | semgrep custom rules |
| CWE-295 (cert validation) | bandit B501 |
| CWE-327 (broken crypto) | bandit B303-B324 |
| CWE-400 (DoS / unbounded resource) | semgrep |
| CWE-502 (deserialization) | bandit B301 (pickle), B305 (marshal), B324 (shelve) |
| CWE-798 (hardcoded credentials) | bandit B105/B107/B108 + gitleaks |
| Known-CVE deps | pip-audit / osv-scanner |

## Edge cases

- **Tests get flagged**: bandit flags `assert` (B101) in tests. Add tests
  to `[tool.bandit] exclude_dirs` or skip B101 globally.
- **Semgrep network access**: `--config=auto` fetches rulesets at run time.
  In air-gapped CI, pre-download rules and pass `--config=./rules/`.
- **pip-audit false positives**: occasional CVEs are flagged for affected-only
  versions of a dep you don't actually use that way. Use `--vulnerability-service
  osv` for OSV-only, or vendor-specific allowlists.
- **Gitleaks history scan**: by default scans only the working tree.
  `--log-opts="--all"` scans full git history (slower; recommended once per
  repo on first adoption).
- **SARIF size limits**: GitHub limits SARIF uploads to 10 MB per file.
  Filter by severity before upload.
- **License + funding**: semgrep's cloud product is paid; the CLI is open
  source (LGPL). Self-hosted is free.

## Comparison

| Tool | Layer | Strength | Weakness |
|---|---|---|---|
| **bandit** | AST patterns | Python-specific, fast | Limited semantic understanding |
| **semgrep** | semantic patterns | huge community ruleset, multi-lang | slower; needs ruleset curation |
| **CodeQL** | full semantic analysis | most precise | very slow, needs GitHub |
| **Snyk Code / SonarQube** | commercial DASTs | rich UI | paid, vendor lock-in |
| **pip-audit** | dep CVEs | PyPA-official | only Python deps |
| **osv-scanner** | dep CVEs | multi-ecosystem | newer tool |
| **gitleaks** | secret patterns | fast, low FP | static patterns only |
| **trufflehog** | secret patterns | entropy detection | more FPs than gitleaks |

Recommended stack: bandit + semgrep (auto config) + pip-audit + gitleaks.
Add CodeQL for repos with high-security stakes — it's slower but catches
more semantic issues.

## Sources

- https://bandit.readthedocs.io/ — bandit docs
- https://semgrep.dev/ — semgrep registry + docs
- https://semgrep.dev/p/bandit — bandit-equivalent semgrep pack
- https://pypi.org/project/pip-audit/ — pip-audit
- https://google.github.io/osv-scanner/ — osv-scanner
- https://github.com/gitleaks/gitleaks — gitleaks
- https://owasp.org/Top10/ — OWASP Top 10
- https://cwe.mitre.org/ — CWE catalog
