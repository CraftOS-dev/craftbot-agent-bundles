---
name: open-source-license-mit-apache-gpl-agpl
description: Audit open-source license compliance — permissive (MIT, BSD, Apache 2.0), weak copyleft (MPL 2.0, LGPL), strong copyleft (GPL v2/v3), network copyleft (AGPL), source-available (SSPL, Elastic, BUSL). Run OSS Review Toolkit (ORT) / Syft / FOSSA / Snyk for SBOM + license scanning. Output is an obligation memo + SBOM with the consult-an-attorney disclaimer.
---

# OSS License Compliance — MIT / Apache / GPL / AGPL + SBOM

## When to use

User says:

- "Check OSS license obligations"
- "MIT vs Apache vs GPL vs AGPL"
- "Can I use [AGPL'd library] in my closed SaaS?"
- "Run an SBOM"
- "OSS Review Toolkit / ORT setup"
- "License compliance for [product]"
- "M&A IP diligence — OSS scan"
- "SPDX identifier"
- "Apache NOTICE file"
- "GPL distribution obligation"

Companion skills:
- `contract-review-msa-nda-employment` — for OSS licensing-IN contracts.

## Setup

```bash
# OSS Review Toolkit (ORT) — most comprehensive multi-ecosystem scanner (2026)
# https://github.com/oss-review-toolkit/ort
docker pull oss-review-toolkit/ort
# Or build from source
# Or via Homebrew (limited): brew install ort

# Syft — multi-ecosystem SBOM generator (Anchore)
brew install syft       # or: curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh

# Grype — vulnerability scanner (Anchore)
brew install grype

# License Checker (npm)
npm install -g license-checker

# pip-licenses (Python)
pip install pip-licenses

# FOSSA (commercial — free for OSS)
# https://fossa.com/

# Snyk (commercial)
# https://snyk.io/
npm install -g snyk

# SPDX License List
# https://spdx.org/licenses/

# OSI License Index
# https://opensource.org/licenses

# Python helpers
pip install spdx-tools requests pandas
```

## Common recipes

### Recipe 1: License obligation matrix (when must I do what?)
| License | Type | Attribution? | Disclose source on distribution? | Disclose source on network use (SaaS)? | Patent grant? | Sub-license? |
|---|---|---|---|---|---|---|
| MIT | Permissive | Yes | No | No | No (implicit) | Yes |
| BSD-2-Clause | Permissive | Yes | No | No | No | Yes |
| BSD-3-Clause | Permissive | Yes | No | No | No | Yes |
| Apache 2.0 | Permissive | Yes + NOTICE file | No | No | Yes (explicit) | Yes |
| MPL 2.0 | Weak copyleft | Yes | File-level copyleft (modified files) | No | Yes | Yes |
| LGPL 2.1 / 3.0 | Library copyleft | Yes | Library code; linking allowed (LGPL) | No | LGPL 3.0: yes | Yes |
| GPL v2 | Copyleft | Yes | Whole work, on distribution | No (GPL = distribution copyleft only) | Yes (v2 implicit) | Yes (under GPL) |
| GPL v3 | Copyleft | Yes | Whole work, on distribution | No | Yes (explicit + anti-Tivoization) | Yes (under GPL) |
| AGPL v3 | Network copyleft | Yes | Whole work, on distribution + on SaaS use | YES | Yes | Yes (under AGPL) |
| SSPL v1 | Source-available (not OSI-approved) | Yes | Whole stack including all service infrastructure | YES | Yes | Restrictive |
| Elastic License 2.0 | Source-available (not OSS) | Yes | — | — | — | Restrictive |
| BUSL 1.1 | Time-delayed OSS | Yes | After change date (typically 4 years) → typically Apache 2.0 | — | — | Restrictive |
| CC0 | Public domain dedication | No | No | No | No | N/A |

### Recipe 2: OSS Review Toolkit (ORT) — comprehensive scan
```bash
# Install via Docker
docker run --rm \
  -v "$PWD":/data \
  oss-review-toolkit/ort:latest \
  analyze -i /data -o /data/ort-results/

docker run --rm \
  -v "$PWD":/data \
  oss-review-toolkit/ort:latest \
  scan -i /data/ort-results/analyzer-result.yml -o /data/ort-results/

docker run --rm \
  -v "$PWD":/data \
  oss-review-toolkit/ort:latest \
  evaluate \
  -i /data/ort-results/scan-result.yml \
  --rules-file /data/.ort/evaluator.rules.kts \
  -o /data/ort-results/

docker run --rm \
  -v "$PWD":/data \
  oss-review-toolkit/ort:latest \
  report \
  -i /data/ort-results/evaluation-result.yml \
  -o /data/ort-results/reports/ \
  -f WebApp,StaticHtml,SPDX_JSON,CycloneDX_JSON,Excel
```
ORT analyzes manifest files (package.json, requirements.txt, go.mod, pom.xml, Cargo.toml, etc.), scans for declared + actual licenses, evaluates against policies, and reports.

### Recipe 3: Syft + Grype — SBOM + vulnerability
```bash
# Generate SPDX SBOM
syft . -o spdx-json=sbom.spdx.json
syft . -o cyclonedx-json=sbom.cyclonedx.json
syft . -o syft-json=sbom.json
syft . -o table   # human-readable

# Scan SBOM for vulnerabilities
grype sbom:sbom.spdx.json
grype dir:.        # scan directory directly
```

### Recipe 4: npm license-checker
```bash
license-checker --production --json > licenses.json
license-checker --production --csv --out licenses.csv
license-checker --failOn "AGPL;SSPL;GPL"   # fail on copyleft
```

### Recipe 5: pip-licenses (Python)
```bash
pip-licenses --format=json --output-file=licenses.json
pip-licenses --format=markdown
pip-licenses --fail-on "GPL;AGPL;SSPL"
```

### Recipe 6: SPDX identifier — single source of truth
```text
Every license has an SPDX identifier:
- MIT
- Apache-2.0
- BSD-2-Clause / BSD-3-Clause
- GPL-2.0-only / GPL-2.0-or-later / GPL-3.0-only / GPL-3.0-or-later
- AGPL-3.0-only / AGPL-3.0-or-later
- LGPL-2.1-only / LGPL-2.1-or-later / LGPL-3.0-only
- MPL-2.0
- ISC
- CC0-1.0
- Unlicense
- WTFPL
- BUSL-1.1
- SSPL-1.0
- Elastic-2.0

Add to your code:
// SPDX-License-Identifier: MIT
// Copyright 2026 Your Company
```

### Recipe 7: Apache 2.0 NOTICE file requirement
```text
Apache 2.0 §4(d) requires retention of NOTICE files when redistributing.

Example NOTICE:
```
Your Application
Copyright 2026 Your Company

This product includes software developed by:
- Apache HttpClient
  Copyright 2015 The Apache Software Foundation
  Apache 2.0 license; see LICENSE-Apache-2.0
- jackson-databind
  Copyright 2009-2025 FasterXML
  Apache 2.0 license

Notices for full text: https://github.com/your-company/your-app/blob/main/NOTICES.md
```

### Recipe 8: AGPL "network use" trigger
```text
AGPL §13:
"If you modify the [AGPL'd] Program, your modified version must prominently offer all users interacting with it remotely through a computer network (if your version supports such interaction) an opportunity to receive the Corresponding Source of your version..."

Practical impact:
- Using AGPL'd library in a closed-source SaaS → triggers source disclosure obligation
- "Corresponding Source" = your modified library + the program that uses it (in many readings)
- Often misunderstood: scope of "Corresponding Source" is contested but cautious reading = your entire SaaS stack

Solution paths:
- Don't use AGPL libraries in closed SaaS
- Negotiate dual license (commercial) with copyright holder
- Self-host on-prem (no network interaction by external users)
```

### Recipe 9: License compatibility matrix (what can I combine?)
```text
Combining licenses:
- MIT + Apache 2.0: ✓ (use as Apache 2.0 + MIT NOTICE)
- MIT + GPL: ✓ (combined work under GPL)
- Apache 2.0 + GPL v3: ✓ (combined work under GPL v3)
- Apache 2.0 + GPL v2: ✗ (Apache 2.0 patent clause incompatible with GPL v2)
- GPL v2 + GPL v3: ✓ (if either license allows "or later")
- BSD-3 + Apache 2.0: ✓ (combined under Apache 2.0)
- MIT + AGPL: ✓ (combined under AGPL)
- Commercial + GPL: ✗ in linked product (combined work must be GPL)
- Commercial + LGPL: ✓ (use as library only; dynamic linking ok)
- Commercial + AGPL: ✗ in SaaS (triggers source disclosure)
- SSPL + Anything closed source: ✗ in SaaS (triggers stack disclosure)

When in doubt: GPL/AGPL/SSPL = avoid in closed code unless dual-licensed.
```

### Recipe 10: SBOM (Software Bill of Materials)
```text
SBOM = inventory of all software components + licenses + versions.

Required by:
- US Executive Order 14028 (federal procurement)
- EU Cyber Resilience Act (2024)
- Common enterprise customer ask
- M&A IP diligence

Formats:
- SPDX (Linux Foundation)
- CycloneDX (OWASP)
- SWID (ISO/IEC 19770-2)

Tooling:
- Syft (multi-ecosystem)
- Anchore Engine
- CycloneDX maven/npm/pip plugins
- ORT
```

### Recipe 11: Source-available vs OSS — the modern boundary
```text
OSI-approved OSS (truly open):
- MIT, BSD, Apache, GPL, AGPL, MPL, LGPL, EPL, etc.

Source-available (NOT OSS):
- SSPL (MongoDB) — production-use disclosure trigger
- BUSL (Hashicorp 2023, MariaDB) — time-delayed OSS
- Elastic License 2.0 — restrictive
- Fair Source — restricted use cases
- PolyForm — restricted use cases
- RSAL — Redis Source Available License

These are NOT free / open in OSI sense:
- May restrict commercial use
- May trigger disclosure
- May expire / convert

Treat differently from OSS in due diligence + obligation tracking.
```

### Recipe 12: M&A IP diligence — OSS scan
```bash
# Standard M&A diligence checklist:
# 1. Generate SBOM
syft . -o spdx-json=sbom.spdx.json

# 2. Identify all licenses
ort analyze -i . -o ort-results/
ort scan -i ort-results/analyzer-result.yml -o ort-results/

# 3. Flag risky licenses
# 4. Identify NOTICE / attribution gaps
# 5. Confirm AGPL / SSPL / BUSL absence in closed-source product
# 6. Verify all licenses are OSI-approved (or commercial)

# Output: License Compliance Memo
```

### Recipe 13: License compliance memo skeleton
```markdown
# OSS License Compliance Memo — <Product>

**Date:** 2026-06-09
**Reviewed by:** Legal Counsel (AI agent)

## SBOM summary
- Total dependencies: <N>
- Direct: <X> / Transitive: <Y>
- License count: <N> distinct
- SPDX SBOM: attached (sbom.spdx.json)

## License distribution
| License | Count | Permissive / Copyleft / Restrictive |
|---|---|---|
| MIT | 423 | Permissive |
| Apache-2.0 | 187 | Permissive |
| BSD-3-Clause | 56 | Permissive |
| ISC | 32 | Permissive |
| GPL-2.0 | 1 | Copyleft (FLAG) |
| AGPL-3.0 | 0 | — |
| SSPL | 0 | — |
| Unknown | 4 | (FLAG) |

## Findings + flags

### FLAG 1: GPL-2.0 dependency
- Package: <name> v<version>
- Issue: Distributing closed-source product with GPL'd library triggers copyleft
- Recommendation: Replace OR isolate via process boundary OR dual-license OR negotiate commercial

### FLAG 2: Unknown licenses
- 4 packages without detected license
- Action: Manual review of each; remove or replace

### FLAG 3: Apache NOTICE compliance
- 187 Apache-licensed packages
- Action: Generate consolidated NOTICE file

## Obligations summary
- Attribution: All MIT + BSD + Apache + GPL packages → consolidated LICENSE / NOTICE file
- NOTICE file: Required for Apache (§4(d)) and many MIT variants
- Source disclosure: None required (no GPL/AGPL in production code path — verified after FLAG 1 remediation)
- Patent: Apache 2.0 + GPL v3 + AGPL all provide patent grants

## Remediation actions
| Action | Priority | Owner | Deadline |
|---|---|---|---|
| Replace GPL-2.0 dependency | HIGH | Eng | 2026-06-25 |
| Audit + license 4 unknown packages | HIGH | Eng | 2026-06-25 |
| Generate NOTICE file (auto from ORT) | MED | Eng | 2026-07-01 |
| Set up CI license check (license-checker --failOn GPL) | MED | DevOps | 2026-07-15 |
| Document OSS policy | LOW | Legal | 2026-08-01 |

---
**Disclaimer:** This is informational guidance from an AI agent. Always consult a licensed attorney before relying on this license analysis for compliance, M&A diligence, or product release decisions.
```

### Recipe 14: CI/CD license enforcement
```yaml
# .github/workflows/license-check.yml
name: License Check
on: [pull_request]

jobs:
  oss-license:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npx license-checker --production --failOn "GPL;AGPL;SSPL;BUSL;Elastic-2.0"
      
      - name: SBOM
        run: |
          curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
          syft . -o spdx-json=sbom.spdx.json
      
      - uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.spdx.json
```

## Examples

### Example 1: SaaS startup OSS scan before launch
**Goal:** Verify no AGPL / SSPL / BUSL dependencies in production.
**Steps:**
1. Recipe 2 ORT scan.
2. Recipe 3 Syft SBOM.
3. Recipe 13 produce compliance memo.
4. Remediate FLAGs (Recipe 14 CI enforcement).
5. Add disclaimer; route to licensed attorney for sign-off.

**Result:** Compliant launch with documented SBOM.

### Example 2: M&A diligence — acquirer reviewing target's OSS
**Goal:** Identify any AGPL / SSPL / GPL contamination in target's closed-source product.
**Steps:**
1. Recipe 12 M&A diligence scan.
2. Generate SBOM.
3. ORT scan with policy evaluator.
4. Flag any copyleft / restrictive.
5. Memo to acquirer's lawyers.

**Result:** Diligence finding informs purchase price + indemnity.

## Edge cases / gotchas

- **License detection misses.** ORT / Syft / license-checker may miss non-standard headers. Manual review for "Unknown" entries.
- **Transitive dependencies dominate.** A small project may have 1000+ transitive deps; one AGPL-licensed transitive can taint the whole tree.
- **GPL "distribution" trigger.** Distributing GPL'd code (even with closed code) triggers copyleft. SaaS deployment is NOT distribution under GPL — but it IS under AGPL.
- **AGPL §13 ambiguity.** Scope of "Corresponding Source" is contested. Conservative reading: must release source of your modified version (at minimum), plus possibly more.
- **SSPL §13 is broader than AGPL.** Triggers disclosure of "Service Source Code" including infrastructure. Stricter than AGPL.
- **Linking interpretation (GPL/LGPL).** Static linking + dynamic linking can be treated differently. FSF interpretation is strict; LGPL permits dynamic linking with closed code.
- **Apache 2.0 patent termination clause.** §3 terminates patent license if licensee sues licensor for patent infringement. Be aware in M&A.
- **NOTICE file enforcement.** Apache 2.0 §4(d) violations are licensable; in practice rarely litigated for solo NOTICE failures but enterprise customers will flag.
- **Multi-license / "OR-later"** can be confusing. GPL-2.0-or-later means recipient can choose v2 OR v3. Document the chosen version.
- **License compatibility issues.** Apache 2.0 + GPL v2 is incompatible (patent clause). Be careful when combining permissive + GPL v2 in same project.
- **BUSL change date.** BUSL terms expire to permissive (typically Apache 2.0) after change date (4 years typical). Track which version of dependency you're using.
- **Elastic License 2.0 restrictions.** Cannot offer the software as a managed service (compete with Elastic). Carefully read.
- **CC0 + non-US.** CC0 may not be a valid public domain dedication in all jurisdictions (e.g., Germany doesn't recognize PD dedication). Use cautiously.
- **No-license code on GitHub.** No license = full copyright reserved. Cannot use without permission. Unlike Stack Overflow (which auto-licenses CC BY-SA 4.0), GitHub repos default to no rights granted.
- **Confidential code leakage.** OSS scan may upload code to cloud service for analysis. Use offline tools (ORT, Syft) for sensitive code.
- **CycloneDX vs SPDX format.** Both valid; pick one based on customer + regulatory requirement.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney before relying on this license analysis for compliance, M&A diligence, product release decisions, or binding business commitments.**

## Sources

- [SPDX License List](https://spdx.org/licenses/) — canonical license identifiers.
- [OSI License Index](https://opensource.org/licenses) — OSI-approved licenses.
- [OSS Review Toolkit (ORT)](https://github.com/oss-review-toolkit/ort) — multi-ecosystem scanner.
- [Syft (Anchore)](https://github.com/anchore/syft) — SBOM generator.
- [Grype (Anchore)](https://github.com/anchore/grype) — vulnerability scanner.
- [FOSSA](https://fossa.com/) — commercial OSS license + vulnerability scanning.
- [Snyk](https://snyk.io/) — security + license platform.
- [SPDX Spec](https://spdx.dev/) — SBOM spec.
- [CycloneDX Spec](https://cyclonedx.org/) — alternative SBOM spec.
- [GNU GPL FAQ](https://www.gnu.org/licenses/gpl-faq.html) — FSF interpretation.
- [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) — Apache 2.0 + FAQ.
- [Choose a License (GitHub)](https://choosealicense.com/) — license picker guide.
- [TLDRLegal](https://www.tldrlegal.com/) — plain-English license summaries.
- [US Executive Order 14028](https://www.whitehouse.gov/briefing-room/presidential-actions/2021/05/12/executive-order-on-improving-the-nations-cybersecurity/) — SBOM federal procurement mandate.
- Sister skill: `contract-review-msa-nda-employment`.
