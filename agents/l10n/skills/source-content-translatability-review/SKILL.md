---
name: source-content-translatability-review
description: Pre-translation source review — idioms, concat strings, ambiguous pronouns, hardcoded units, brand voice. Vale L10n style pack, Acrolinx, Textio readability scoring. Use when the user asks "is this source ready to translate", "audit our copy", "Vale L10n rules", "Acrolinx setup", or wants to reduce downstream localization cost.
---

# Source Content Translatability Review

Pre-translation source review reduces downstream localization cost 20-40%. Idioms cost 3x word-rate (transcreation); concat strings cost +15% time per round; ambiguous pronouns trigger translator queries that delay delivery 1-3 days each. Catching issues at the source — before TMS upload — is the highest-leverage L10n investment.

Stack: **Vale** for plain-text + Markdown rules (open source, runs in CI), **Acrolinx** for enterprise content governance with translatability score (paid, SOC 2), **Textio** for inclusive-language + readability scoring on marketing copy.

## When to use

- Writer drafts new help-center article; agent reviews before sending to TMS.
- Reviewing UI strings catalog before first translation push.
- Onboarding a new product team to localization; need a writing checklist.
- Cost overruns on translation projects; need to fix upstream.
- Translator complaints about ambiguity, idioms, broken segments.
- Marketing content needs translatability score before campaign launch.

Trigger phrases: "translatability", "Vale L10n", "Acrolinx", "translatable source", "idiom check", "concat string", "source review", "Textio score", "pre-translation gate".

## Setup

```bash
# Vale (open source, primary tool)
brew install vale                           # macOS
choco install vale                          # Windows
# OR release tarball: https://github.com/errata-ai/vale/releases
vale --version                              # 3.x or later

# Vale L10n style pack (community)
vale sync                                   # downloads styles defined in .vale.ini
# Or manually:
git clone https://github.com/errata-ai/Microsoft .vale/styles/Microsoft
git clone https://github.com/errata-ai/proselint .vale/styles/proselint
git clone https://github.com/errata-ai/Google .vale/styles/Google

# Acrolinx (enterprise, paid)
# Server: SaaS or on-prem; user provisioned via Acrolinx admin console
# Editor plug-ins: Word, Outlook, Chrome, Figma, VS Code
# CLI:
npm i -g @acrolinx/cli
acrolinx --version

# Textio (marketing copy, paid)
# Web UI + Chrome extension + API
# https://textio.com/

# readability score (free CLI fallback)
pipx install readability                    # textstat-based
```

Auth/env:
- Acrolinx: `ACROLINX_TOKEN`, `ACROLINX_URL` (your tenant)
- Textio: `TEXTIO_API_KEY`
- Vale: no auth

## Translatability rubric (pre-translation checklist)

| Category | Issue | Cost impact |
|---|---|---|
| **Idioms** | `hit it out of the park`, `low-hanging fruit`, `boil the ocean` | +200% on that string (transcreation rate) |
| **Concatenated strings** | `"You have " + count + " items"` | +15% per round (split + re-stitch) |
| **Ambiguous pronouns** | `it`, `they` with multiple antecedents | +1 query round per ambiguity (1-3 day delay) |
| **Hardcoded units** | mph, °F, feet, gallons | +1 dev round (per-locale logic) |
| **Hardcoded date format** | `03/04/25` (ambiguous April 3 vs March 4) | wrong dates in 1+ locales |
| **Embedded HTML/markup** | `Click <a href="x">here</a>` | tag damage; +1 QA round |
| **Cultural references** | sports teams, holidays, food | requires transcreation |
| **Abbreviations** | `OOO`, `ETA`, `EOD` | translator queries; sometimes untranslatable |
| **Metaphors** | `circle back`, `move the needle` | requires creative equivalents |
| **Gendered nouns** | `the doctor → he`, `nurse → she` | gender-neutral rewrite + ICU select |
| **String length limits** | "fits in 30 chars en" → 50+ chars de/fi | UI truncation |
| **Brand voice violations** | inconsistent tone | per-locale style drift |

**Cumulative: bad source → +20-40% total localization cost.**

## Common recipes

### Recipe 1: Initialize Vale with L10n style pack

```bash
# .vale.ini
StylesPath = .vale/styles
MinAlertLevel = suggestion

Packages = Microsoft, proselint, Google, L10n

[*.{md,mdx,txt}]
BasedOnStyles = Microsoft, proselint, L10n

[locales/*.json]
BasedOnStyles = L10n

[src/**/*.{ts,tsx,js,jsx}]
BasedOnStyles = L10n
```

```bash
vale sync         # downloads Microsoft + proselint
mkdir -p .vale/styles/L10n
```

### Recipe 2: Custom Vale L10n style pack

```yaml
# .vale/styles/L10n/Idioms.yml
extends: existence
message: "'%s' is an idiom — replace for translatability."
level: error
ignorecase: true
tokens:
  - hit it out of the park
  - low-hanging fruit
  - circle back
  - boil the ocean
  - touch base
  - move the needle
  - drink the kool-aid
  - bite the bullet
  - drop the ball
  - on the same page
  - reinvent the wheel
  - take it offline
```

```yaml
# .vale/styles/L10n/Concat.yml — string concatenation in source
extends: existence
message: "Concatenation '%s' breaks translation. Use ICU MessageFormat."
level: error
tokens:
  - '"\s*\+\s*\{?\w+\}?\s*\+\s*"'
  - '`\$\{\w+\}\s+\w+\s+\{?'

# .vale/styles/L10n/HardcodedUnits.yml — non-locale-aware units
# tokens: '\d+\s*(mph|°[FC]|feet|ft|miles|mi|gallons|gal|inches|lbs|oz)'

# .vale/styles/L10n/AmbiguousDate.yml — ambiguous DD/MM vs MM/DD
# tokens: '\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'

# .vale/styles/L10n/CulturalRef.yml — US-only references (level: suggestion)
# tokens: super bowl, thanksgiving, fourth of july, black friday, homecoming, tailgate, happy hour

# .vale/styles/L10n/Abbreviations.yml — flag for expansion
# tokens: '\b(OOO|ETA|EOD|EOW|ASAP|FYI|IIRC)\b'

# .vale/styles/L10n/EmbeddedHTML.yml — segment-breaking markup
# tokens: '<[a-z]+[^>]*>', '</[a-z]+>'
```

### Recipe 3: Run Vale in CI

```yaml
# .github/workflows/source-review.yml
name: Source content review
on: [pull_request]
jobs:
  vale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: errata-ai/vale-action@reviewdog
        with:
          version: 3.4.0
          reporter: github-pr-review
          files: 'docs/ src/components/ locales/en.json'
          fail_on_error: true
```

### Recipe 4: Vale JSON output for programmatic gate

```bash
vale --output=JSON --no-exit docs/ > vale-report.json

# Aggregate
python -c "
import json, sys
report = json.load(open('vale-report.json'))
errors = sum(1 for issues in report.values() for i in issues if i['Severity'] == 'error')
warns = sum(1 for issues in report.values() for i in issues if i['Severity'] == 'warning')
print(f'Errors: {errors}, Warnings: {warns}')
sys.exit(1 if errors > 0 else 0)
"
```

### Recipe 5: Acrolinx integration

```bash
# Acrolinx CLI scoring
acrolinx login --url https://yourtenant.acrolinx.cloud --token $ACROLINX_TOKEN

acrolinx check \
  --file docs/getting-started.md \
  --guidance-profile en-marketing \
  --report-type=brief

# Output:
# Acrolinx Score:    78
# Clarity:           82
# Tone:              80
# Inclusive Language:75
# Translatability:   82
# Terminology:       90
```

```bash
# Batch with CI gate
acrolinx check docs/**/*.md \
  --score-threshold 75 \
  --translatability-threshold 80 \
  --report-format json \
  --output report.json
```

### Recipe 6: Acrolinx custom rules + Textio scoring

```json
// Acrolinx guidance profile snippet
{ "rules": {
  "long_sentences":      { "max_words": 25 },
  "passive_voice":       { "max_percent": 15 },
  "noun_chains":         { "max_consecutive": 3 },
  "ambiguous_referents": { "enabled": true },
  "embedded_markup":     { "enabled": true, "severity": "error" },
  "non_breaking_terms":  { "list": "do-not-translate.txt" },
  "forbidden_idioms":    { "list": "idioms-en.txt" } }}
```

```bash
# Textio (marketing copy + inclusivity + readability)
textio score --file campaigns/launch-q3.md \
  --tone marketing --inclusivity-check --readability-grade 8
# → Score 92 / Tone Marketing—Confident / Inclusivity clean / Translatability high
```

### Recipe 8: Readability score (free fallback)

```python
# textstat — Flesch-Kincaid grade, Gunning Fog, sentence length
from textstat import textstat
text = open('docs/page.md').read()
print({
  'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),  # target ≤ 8
  'gunning_fog':          textstat.gunning_fog(text),
  'avg_sentence_length':  textstat.avg_sentence_length(text),   # target ≤ 20
})
```

Translatable English: FK grade 6-8, avg sentence ≤ 20 words. CLI: `readability --metric=flesch_kincaid_grade docs/page.md`.

### Recipe 9: Translatability score for a UI catalog (en.json)

```python
import json, re
from pathlib import Path

ISSUES = {
  'concat': re.compile(r'["\']\s*\+\s*\{|\$\{[^}]+\}\s+[a-z]+'),
  'embedded_html': re.compile(r'<[a-z]+[^>]*>'),
  'hardcoded_unit': re.compile(r'\d+\s*(mph|°[FC]|feet|miles|gallons|inches|lbs)'),
  'idiom': re.compile(r'\b(circle back|low-hanging fruit|boil the ocean|touch base)\b', re.I),
  'ambiguous_date': re.compile(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b'),
  'abbrev': re.compile(r'\b(OOO|ETA|EOD|ASAP|FYI|IIRC)\b'),
  'concat_format': re.compile(r'%(s|d|\d+\$s)'),       # printf-style instead of ICU
}

catalog = json.loads(Path('locales/en.json').read_text())
report = {key: [] for key in ISSUES}
total = 0
for k, v in catalog.items():
  if not isinstance(v, str): continue
  total += 1
  for issue, pat in ISSUES.items():
    if pat.search(v):
      report[issue].append((k, v))

print(f'Total strings: {total}')
for issue, hits in report.items():
  print(f'  {issue}: {len(hits)}')

flagged = sum(len(h) for h in report.values())
score = 100 * (1 - flagged / max(total, 1))
print(f'Translatability score: {score:.1f}%')
```

### Recipe 10: Pre-commit hook

```yaml
# .pre-commit-config.yaml
repos:
  - { repo: https://github.com/errata-ai/vale, rev: v3.4.0,
      hooks: [{ id: vale, args: [--config=.vale.ini, --minAlertLevel=error], files: '\.(md|mdx|json)$' }] }
```

### Recipe 11: Pre-translation report (per-file)

```bash
# Run Vale + readability + custom heuristics → one report
for f in docs/**/*.md; do
  echo "=== $f ==="
  vale --output=line --no-exit "$f"
  readability --metric=flesch_kincaid_grade "$f"
done > pre-translation-report.txt
```

### Recipe 12: Hand-off to technical-writer for rewrite

```
SUMMARY for technical-writer:
File: docs/api-quickstart.md
Vale errors: 3 idioms, 2 hardcoded units, 1 ambiguous date
Acrolinx translatability score: 67/100 (target ≥ 80)
Readability: FK grade 11 (target ≤ 8)
Top fixes:
1. Line 12: "circle back" → "follow up"
2. Line 23: "5 mph" → "{speed, number, ::measure-unit/length-meter-per-second}"
3. Line 41: passive voice cluster (3 sentences)
4. Line 67: sentence length 38 words → split
```

### Recipe 13: Brand voice + DNT + inclusive language (combined)

```yaml
# .vale/styles/L10n/BrandVoice.yml — enforce approved terminology
extends: substitution
level: warning
ignorecase: true
swap: { customer: user, end-user: user, user-friendly: easy to use }

# .vale/styles/L10n/DoNotTranslate.yml — brand terms TMS must skip
# extends: existence; level: suggestion
# tokens: YourBrand, YourBrand Cloud, YourBrand Pro

# .vale/styles/L10n/Inclusivity.yml — inclusive language gate
# extends: substitution; level: error
# swap: { blacklist: blocklist, whitelist: allowlist, master: main, slave: replica,
#         guys: folks, manpower: workforce, manhours: person-hours, chairman: chair }
```

DNT list must also be uploaded to Crowdin/Lokalise/Phrase glossary marked do-not-translate.

### Recipe 14: TMS gate via webhook

```yaml
# .github/workflows/pre-tms-push.yml — block Crowdin push if score < 80
on: { push: { paths: ['locales/en.json'] } }
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: vale --minAlertLevel=error locales/en.json
      - run: |
          score=$(python scripts/translatability_score.py locales/en.json --score-only)
          (( $(echo "$score < 80" | bc -l) )) && exit 1 || true
      - if: success()
        uses: crowdin/github-action@v2
```

## Examples

### Example 1: New help-center article fails pre-translation gate

**Goal:** Writer submits `docs/getting-started.md`; CI must catch translatability issues before reviewer sees it.

**Steps:**
1. PR opened → GitHub Action runs Vale + Acrolinx (Recipes 3, 5).
2. Vale errors:
   - Line 12: `"circle back"` (idiom)
   - Line 23: `"5 mph"` (hardcoded unit)
   - Line 41: `"03/04/25"` (ambiguous date)
3. Acrolinx translatability score: 67 (threshold 80).
4. Reviewdog posts inline comments on PR.
5. Writer rewrites:
   - "circle back" → "follow up"
   - "5 mph" → "8 km/h (5 mph)" or "{speed, number, ::measure-unit/length-meter-per-second}"
   - "03/04/25" → "March 4, 2025"
6. Re-run gate passes (score 85, no errors).
7. Merge → Crowdin sync triggers.

**Result:** Source content reaches translators clean; no clarifying queries; on-time delivery.

### Example 2: UI catalog audit before initial Crowdin push

**Goal:** 1,200-string `locales/en.json` going to Crowdin first time; minimize cost.

**Steps:**
1. Run Recipe 9 (translatability_score.py) → finds 47 concat strings, 8 embedded HTML, 15 hardcoded units, 22 abbreviations, 3 idioms.
2. Calculate cost projection: 47 concat × 15% time = +7 days; 22 abbrev × 1 query each = +22 queries.
3. Prioritize: fix concat (Recipe in `icu-messageformat-pluralization`), expand abbreviations, replace hardcoded units with ICU skeletons.
4. Re-run audit: 0 concat, 0 idioms, 5 remaining abbreviations are domain-standard (API, URL, SDK) — mark DNT.
5. Push DNT list to Crowdin: `crowdin glossary upload do-not-translate.csv`.
6. Translatability score 92/100 → push to Crowdin.

**Result:** Initial translation project completes 25% faster, 18% cheaper than baseline estimate.

## Edge cases / gotchas

- **Vale JSON keys vs values** — `existence` checks raw text; use scope filter or accept that key names get linted.
- **Acrolinx false positives on jargon** — add `API`, `SDK`, `JWT` to termbase as approved.
- **Textio is inclusivity + tone** — pair with Vale for i18n-specific (concat, hardcoded units).
- **Flesch-Kincaid is English-only** — for JA/ZH source use jReadability / 中文可读性.
- **Vale skips Markdown code blocks** — configure scope per file glob for JSON/MDX.
- **Concat detection false positives** — `path + '/file.txt'` is fine; scope to user-facing strings.
- **Idiom lists are subjective** — review with content lead before escalating to `error`.
- **Brand voice per geo** — US vs UK spellings; separate `.vale/styles/L10n-en-US/`, `L10n-en-GB/`.
- **DNT must sync to TMS** — Vale DNT list also uploaded to Crowdin/Lokalise/Phrase glossary.
- **Acrolinx on-prem** — enterprise tier; 4-6 week deployment.
- **Rule priority** — start as `warning`; escalate to `error` as team adopts.
- **MDX with `extends: existence`** — embedded HTML may not match; use remark-lint for MDX.
- **Reviewdog** — Markdown by default; configure `files:` for JSON/code.
- **Score thresholds are opinion** — 80 for technical docs, 90 for marketing.
- **Cultural refs at `suggestion`** — `Super Bowl` may be intentional in US copy; don't block.

## Sources

- Vale: https://vale.sh/  + styles explorer https://vale.sh/explorer/
- Vale Microsoft / Google / proselint packs: https://github.com/errata-ai/Microsoft  https://github.com/errata-ai/Google  https://github.com/errata-ai/proselint
- vale-action (CI): https://github.com/errata-ai/vale-action
- Acrolinx Platform + Translatability: https://www.acrolinx.com/platform/  https://www.acrolinx.com/products/acrolinx-platform/translatability/
- Acrolinx CLI: https://docs.acrolinx.com/coreplatform/latest/en/cli
- Textio (inclusivity + tone): https://textio.com/  https://textio.com/products/inclusive-language
- textstat (readability): https://github.com/textstat/textstat
- Flesch-Kincaid: https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
- W3C inclusive design: https://www.w3.org/International/articles/inclusive-design/
- plainlanguage.gov: https://www.plainlanguage.gov/guidelines/
- Phrase translation-friendly content: https://phrase.com/blog/posts/translation-friendly-content/
- SimpleLocalize i18n guide: https://simplelocalize.io/blog/posts/internationalization-guide-software-localization/
