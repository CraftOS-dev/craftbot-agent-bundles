<!--
Source: https://www.zaproxy.org/ · https://portswigger.net/burp · https://snyk.io/ · https://github.com/zaproxy/action-baseline
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Security Testing — OWASP ZAP + Burp Suite + Snyk / pip-audit / osv-scanner

The QA-side security toolchain layers automated DAST in CI (OWASP ZAP),
manual pentest (Burp Pro), and dependency CVE scanning (Snyk / pip-audit /
osv-scanner / npm audit). ZAP is the 2026 default for CI: free, Apache 2.0,
official GitHub Actions, SARIF output for GitHub Code Scanning.

## When to use

- New endpoint / new public surface area
- Pre-launch security gate
- Compliance (SOC 2 / PCI / GDPR) DAST evidence
- Dependency upgrade — verify no new CVE introduced
- Suspected vulnerability — manual deep-dive
- Trigger phrases: "security test", "DAST", "SAST", "ZAP", "Burp", "Snyk",
  "OWASP Top 10", "CVE", "pen test", "vulnerability scan", "SARIF"

Do NOT use for: replacing a real pentest before regulated audit; replacing
WAF / RASP. These are scanners, not silver bullets.

## Setup

```bash
# OWASP ZAP — Docker (default for CI)
docker pull zaproxy/zap-stable

# Or local install
brew install --cask zap

# Burp Suite Community (manual)
# Download from https://portswigger.net/burp/communitydownload

# Snyk CLI
npm i -g snyk
snyk auth

# Python dep audit
uvx pip-audit
uv add --dev pip-audit

# OSV multi-eco
brew install osv-scanner
# Or: go install github.com/google/osv-scanner/cmd/osv-scanner@latest

# Secrets detection
brew install gitleaks
brew install trufflehog
```

Auth: `SNYK_TOKEN`, `GITHUB_TOKEN` (for SARIF upload), `ZAP_API_KEY` (only
for API-driven runs).

## Common recipes

### Recipe 1 — ZAP baseline scan (CI default)

```bash
docker run --rm -v $PWD:/zap/wrk:rw \
  zaproxy/zap-stable zap-baseline.py \
    -t https://staging.example.com \
    -r zap-report.html \
    -J zap-report.json \
    -w zap-report.md \
    -d
```

`-d` debug; passive scan only (safe against staging).

### Recipe 2 — ZAP full scan (active + spider)

```bash
docker run --rm -v $PWD:/zap/wrk:rw \
  zaproxy/zap-stable zap-full-scan.py \
    -t https://staging.example.com \
    -r zap-report.html \
    --hook=/zap/wrk/hooks.py
```

`zap-full-scan.py` actively probes — only against staging / test envs.

### Recipe 3 — ZAP GitHub Action

```yaml
# .github/workflows/security.yml
on:
  pull_request:
  schedule: [{ cron: '0 5 * * *' }]   # nightly

jobs:
  zap-baseline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.13.0
        with:
          target: 'https://staging.example.com'
          rules_file_name: '.zap/rules.tsv'
          fail_action: true
          allow_issue_writing: false
      - name: Upload SARIF
        if: always()
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: report_sarif.json
```

### Recipe 4 — ZAP rules.tsv (suppress noisy rules)

```
# .zap/rules.tsv  — TAB-separated
10020	IGNORE	(X-Frame-Options) — already CSP-handled
10038	WARN	(CSP) — accepted risk in staging
10049	IGNORE	(Storable + Cacheable content) — by design
```

### Recipe 5 — ZAP authenticated scan

```python
# .zap/auth-hook.py
def zap_started(zap, target):
    zap.authentication.set_authentication_method(
        contextid=1,
        authmethodname="formBasedAuthentication",
        authmethodconfigparams="loginUrl=https://staging.example.com/login&"
                              "loginRequestData=email%3D%7B%25username%25%7D%26"
                              "password%3D%7B%25password%25%7D",
    )
    zap.users.new_user(contextid=1, name="loadtest")
    zap.users.set_authentication_credentials(
        contextid=1, userid=1,
        authcredentialsconfigparams="username=loadtest@example.com&password=Test1234!",
    )
    zap.users.set_user_enabled(contextid=1, userid=1, enabled=True)
```

```bash
docker run --rm -v $PWD/.zap:/zap/wrk:rw \
  zaproxy/zap-stable zap-baseline.py \
  -t https://staging.example.com \
  --hook=/zap/wrk/auth-hook.py
```

### Recipe 6 — Snyk dep + IaC scan

```bash
snyk test                          # deps
snyk code test                     # SAST
snyk iac test terraform/           # IaC
snyk container test myimage:tag    # container
snyk monitor                       # baseline + continuous

# SARIF for GitHub
snyk test --sarif > snyk.sarif
gh code-scanning upload-sarif --sarif snyk.sarif
```

### Recipe 7 — pip-audit (Python deps)

```bash
uvx pip-audit --fix --strict
uvx pip-audit --format=cyclonedx-json --output=sbom.json
uvx pip-audit --requirement=requirements.txt --vulnerability-service=pypi
```

```yaml
# .github/workflows/audit.yml
- run: uv pip install pip-audit
- run: uvx pip-audit --strict --format=json --output=pip-audit.json
- if: failure()
  uses: actions/upload-artifact@v4
  with: { name: pip-audit, path: pip-audit.json }
```

### Recipe 8 — osv-scanner (multi-eco)

```bash
osv-scanner -r .                          # repo scan
osv-scanner --lockfile=requirements.txt
osv-scanner --format=sarif --output=osv.sarif .

# GitHub Action
- uses: google/osv-scanner-action/osv-scanner-action@v1.6
  with: { scan-args: |- -r . }
```

### Recipe 9 — Secrets scan

```bash
gitleaks detect --source . --redact --verbose
gitleaks protect --staged             # pre-commit
trufflehog filesystem . --only-verified
trufflehog git https://github.com/org/repo --only-verified
```

```yaml
# Pre-commit
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks:
      - id: gitleaks
```

### Recipe 10 — Burp Suite for manual investigation

```text
# Burp Community workflow
1. Set browser proxy → localhost:8080
2. Install Burp CA cert
3. Browse target → all requests appear in Proxy → History
4. Right-click request → Send to Repeater → mutate + re-send
5. Right-click request → Send to Intruder → fuzz parameters
6. Burp Decoder for base64 / URL / hex
7. Burp Comparer for diffing responses
```

Burp Pro adds Active Scanner (paid). Burp Enterprise = CI DAST competitor to
ZAP.

### Recipe 11 — OWASP Top 10 checklist (manual review)

```markdown
- [ ] A01 Broken Access Control — IDOR via swap user IDs / object IDs
- [ ] A02 Cryptographic Failures — TLS 1.3+, no MD5/SHA1, KMS managed keys
- [ ] A03 Injection — parameterized queries, schema validation
- [ ] A04 Insecure Design — threat model present, abuse cases tested
- [ ] A05 Security Misconfig — security headers, no default creds, no debug
- [ ] A06 Vulnerable Components — dep CVE scan green
- [ ] A07 Auth Failures — MFA, lockout, secure session, no weak passwords
- [ ] A08 Software/Data Integrity Failures — SLSA L2+, signed artifacts
- [ ] A09 Logging Failures — auth events, access events, no PII in logs
- [ ] A10 SSRF — allowlist outbound URLs; deny internal RFC1918
```

### Recipe 12 — Security headers verification

```bash
curl -I https://staging.example.com | grep -i -E \
  '(strict-transport|content-security|x-frame|x-content-type|referrer-policy|permissions-policy)'

# Or
docker run --rm projectdiscovery/nuclei -u https://staging.example.com \
  -t http/misconfiguration/security-headers.yaml
```

### Recipe 13 — SARIF upload to GitHub Code Scanning

```yaml
- name: Upload ZAP SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: report_sarif.json
    category: zap
```

Surfaces findings in PR + Security tab.

### Recipe 14 — Container CVE scan (Trivy / Grype)

```bash
brew install trivy
trivy image myorg/app:1.42 --severity HIGH,CRITICAL --exit-code 1
trivy fs . --scanners vuln,secret,misconfig

brew install grype
grype docker:myorg/app:1.42 --fail-on high
```

## Examples

### Example 1: Stand up CI security gate from scratch

**Goal:** Block merge on high-severity dep CVE + ZAP high alert.

1. Add `.github/workflows/security.yml` (Recipe 3) — ZAP baseline.
2. Add Snyk / pip-audit job (Recipe 6 / 7) — fail on high.
3. Add gitleaks pre-commit (Recipe 9).
4. Wire SARIF upload (Recipe 13) → Security tab.
5. Add `.zap/rules.tsv` (Recipe 4) for known-accepted findings.
6. Test on a known vulnerable branch to verify gate fires.

### Example 2: Pre-launch deep security review

**Goal:** Review checkout flow for a paid feature launch.

1. Run ZAP full scan against staging (Recipe 2) — capture report.
2. Walk OWASP Top 10 checklist manually (Recipe 11).
3. Burp Pro Active Scanner on checkout endpoints (Recipe 10).
4. Inspect security headers (Recipe 12).
5. Container scan with Trivy (Recipe 14).
6. File findings in Jira with CVSS; triage S1/S2 before launch.

## Edge cases / gotchas

- **Never scan prod actively** — `zap-full-scan.py` and Burp Active Scanner
  send malicious payloads. Use baseline (passive) only on prod.
- **Out-of-scope IPs / domains** — set context properly in ZAP; otherwise
  you may scan a third-party CDN and trigger legal questions.
- **Auth scope** — authenticated scans expose more attack surface; required
  for IDOR / authz testing.
- **WAF blocking the scanner** — staging-only WAF bypass needed; otherwise
  signal noise. Allowlist the scanner IP.
- **CSP report-only** — scanner sees report-only as a finding; tune in
  `rules.tsv`.
- **Dep CVE false positives** — `--ignore` known-false in Snyk; document
  rationale in `.snyk` policy file.
- **CVE without patch** — accept risk in policy file with expiry date.
- **Container scanning by SBOM** — Trivy supports SBOM-only (no image pull);
  faster for CI.
- **`gh secret-scanning` GitHub feature** — enable in repo settings for
  push-protection; complements gitleaks at commit time.
- **OWASP Top 10 vs OWASP ASVS** — ASVS is the detailed verification
  standard; Top 10 is the executive summary. Use ASVS for code review.
- **Pentest vs DAST** — DAST is automated; pentest is humans with creativity.
  Use both. DAST in CI, pentest pre-launch.

## Sources

- [OWASP ZAP](https://www.zaproxy.org/)
- [ZAP GitHub Actions](https://github.com/zaproxy/action-baseline)
- [ZAP getting started](https://www.zaproxy.org/getting-started/)
- [Burp Suite](https://portswigger.net/burp)
- [Burp Suite Academy](https://portswigger.net/web-security)
- [Snyk docs](https://docs.snyk.io/)
- [pip-audit](https://pypi.org/project/pip-audit/)
- [osv-scanner](https://google.github.io/osv-scanner/)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- [trufflehog](https://github.com/trufflesecurity/trufflehog)
- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [Trivy](https://trivy.dev/)
- [SARIF spec](https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning)
