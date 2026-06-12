---
name: translator-quality-scoring
description: MQM 2.0 + DQF translator quality scoring. Error taxonomy, severity weights, per-1000-word rate, per-translator aggregation. Use when the user asks "score our translators", "MQM scorecard", "rank vendors by quality", or wants translator quality trended over time.
---

# Translator Quality Scoring (MQM 2.0 + DQF)

MQM 2.0 (Multidimensional Quality Metrics, 2024) is the 2026 standard scoring framework — error categories (accuracy / fluency / terminology / locale convention / style / design / veracity), severity weights (critical / major / minor / neutral), per-1000-word rate. Used by Lilt, Welocalize, Phrase.

DQF (Dynamic Quality Framework, TAUS) is the alternative; same shape, different category names. Convertible.

## When to use

- The user wants to score a translation batch.
- The user is comparing LSPs by quality.
- The user is tracking per-translator quality over time.
- The user needs a CI gate that blocks low-quality batches.
- The user is migrating from ad-hoc QA to MQM framework.

Trigger phrases: "MQM", "DQF", "translator quality", "scorecard", "rank translators", "QE", "quality estimation", "error taxonomy".

## Setup

```bash
# Lilt MQM scoring CLI (community-developed)
pip install mqm-tools                # if needed

# Otherwise: spreadsheet-based scoring
# Use Google Sheets / Excel / Notion table

# Reference: themqm.org provides offline scorecards
# Download from https://themqm.org/the-mqm-typology/
```

Auth/env: none required for the scoring framework itself. TMS API tokens to fetch batches covered by `tms-setup-crowdin-lokalise-phrase`.

## MQM 2.0 error taxonomy

### Top-level categories

- **Accuracy** — Mistranslation, Omission, Addition, Untranslated, Do-not-translate violation
- **Fluency** — Grammar, Spelling, Punctuation, Register, Style, Inconsistency
- **Terminology** — Wrong term, Inconsistent term, Forbidden term
- **Locale convention** — Number format, Date format, Currency format, Address format, Name order
- **Style** — Awkwardness, Unclear reference, Inconsistency
- **Design** — Length, Truncation, Whitespace
- **Veracity** — Brand voice deviation (custom — useful for marketing)

### Severity weights

| Severity | Weight | Definition |
|---|---|---|
| Critical | 10 | Renders content unusable / brand-damaging / legal risk |
| Major | 5 | Significantly impedes comprehension or task |
| Minor | 1 | Noticeable but doesn't impede |
| Neutral | 0 | Stylistic preference, no clear error |

### Score formula

```
MQM Score = (Σ severity weights × penalty_factor) / (translated_words / 1000)
```

Standard penalty_factor = 1. Custom industries adjust (pharma: 2; gaming: 0.5).

### Target thresholds

| Tier | Threshold (per 1000 words) | Content type |
|---|---|---|
| Premium | ≤ 5 | Legal, marketing, brand-critical |
| Standard | ≤ 15 | UI, support, docs |
| Functional | ≤ 30 | Internal, dev tooling |

## Common recipes

### Recipe 1: Scorecard CSV template

```csv
batch_id,translator,vendor,locale,domain,word_count,critical,major,minor,neutral,mqm_score,reviewer,review_date,notes
2026Q3-001,alice,TransPerfect,de-DE,ui,2400,0,3,8,2,9.6,john,2026-06-15,Strong technical
2026Q3-002,bob,Acclaro,fr-FR,marketing,1800,1,2,4,1,14.4,jane,2026-06-15,Slogan slightly off
2026Q3-003,carol,Andovar,ja-JP,legal,3200,0,0,2,0,0.6,sam,2026-06-15,Excellent
2026Q3-004,dave,Smartcat,ko-KR,ui,1500,2,8,15,3,40.7,jane,2026-06-15,Below standard threshold
```

### Recipe 2: Score a translated batch (manual)

```
1. Reviewer opens translated XLIFF in CAT (memoQ / Trados / Phrase TMS)
2. Per segment, mark errors with category + severity:
   - Wrong term (Terminology), Major → 5 points
   - Awkward phrasing (Style), Minor → 1 point
3. Sum severity × count
4. Divide by word count / 1000
5. Compare to threshold for content tier
```

### Recipe 3: Score via TMS QA APIs

```bash
# Crowdin QA findings
curl -L "https://api.crowdin.com/api/v2/projects/<PID>/qa-checks" \
  -H "Authorization: Bearer $CROWDIN_PERSONAL_TOKEN"

# Phrase QA report
curl 'https://api.phrase.com/v2/projects/<PID>/translations/verify' \
  -H "Authorization: token $PHRASE_TOKEN"

# Lokalise QA issues
lokalise2 qa-issue list --token $LOKALISE_API_TOKEN --project-id $PID
```

Map TMS QA findings → MQM categories:
```
TMS finding           → MQM category
'Untranslated'        → Accuracy: Untranslated (Major)
'Inconsistent term'   → Terminology: Inconsistent (Major)
'Spelling'            → Fluency: Spelling (Minor)
'Tag mismatch'        → Design: Whitespace/Format (Major)
'Glossary violation'  → Terminology: Wrong term (Major or Critical)
```

### Recipe 4: Per-translator aggregation

```python
import pandas as pd
df = pd.read_csv('mqm_scores.csv')

# Per-translator rolling 90-day average
df['review_date'] = pd.to_datetime(df['review_date'])
recent = df[df['review_date'] > df['review_date'].max() - pd.Timedelta(days=90)]

trend = recent.groupby('translator').agg(
    avg_mqm=('mqm_score', 'mean'),
    word_count=('word_count', 'sum'),
    batches=('batch_id', 'count'),
    critical_count=('critical', 'sum'),
    locales=('locale', 'nunique')
).sort_values('avg_mqm')

print(trend)
```

### Recipe 5: Per-domain aggregation

```python
domain = df.groupby(['translator', 'domain']).agg(
    avg_mqm=('mqm_score', 'mean'),
    sample_count=('batch_id', 'count')
)
print(domain)
```

Reveals: translator great at UI but weak on marketing → reassign or train.

### Recipe 6: Per-batch report (Markdown summary)

```python
def report(batch_id):
    row = df[df.batch_id == batch_id].iloc[0]
    threshold = {'legal': 5, 'marketing': 5, 'ui': 15, 'docs': 15, 'support': 30}[row.domain]
    verdict = 'PASS' if row.mqm_score <= threshold else 'FAIL'
    return f"""
# Batch {batch_id} — {verdict}

| Field | Value |
|---|---|
| Translator | {row.translator} |
| Vendor | {row.vendor} |
| Locale | {row.locale} |
| Domain | {row.domain} |
| Word count | {row.word_count:,} |
| Critical errors | {row.critical} |
| Major errors | {row.major} |
| Minor errors | {row.minor} |
| **MQM score** | {row.mqm_score:.1f} (threshold: {threshold}) |
| Reviewer | {row.reviewer} |
"""
```

### Recipe 7: CI gate — fail merge on MQM score

```yaml
# .github/workflows/translation-qa.yml
- name: Score MQM
  run: python score-mqm.py locales/de-2026q3.xlf > mqm.json
- name: Gate
  run: |
    score=$(jq '.score' mqm.json)
    domain=$(jq -r '.domain' mqm.json)
    threshold=$(jq -r ".$domain" thresholds.json)
    if (( $(echo "$score > $threshold" | bc -l) )); then
      echo "::error::MQM $score > $threshold for $domain"; exit 1
    fi
```

### Recipe 8: Multi-batch trend chart

```python
import matplotlib.pyplot as plt
weekly = df.groupby([pd.Grouper(key='review_date', freq='W'), 'translator']).agg(
    avg=('mqm_score', 'mean'),
    words=('word_count', 'sum')
).reset_index()

fig, ax = plt.subplots()
for translator in weekly.translator.unique():
    sub = weekly[weekly.translator == translator]
    ax.plot(sub.review_date, sub.avg, label=translator)
ax.axhline(15, color='red', linestyle='--', label='Standard threshold')
ax.set_xlabel('Week')
ax.set_ylabel('MQM score')
ax.legend()
plt.savefig('mqm-trend.png')
```

### Recipe 9: Custom Veracity category (brand voice)

For marketing batches, add a "Brand voice" category not in standard MQM:
```
veracity_score = 0
for segment in batch:
  if voice_mismatch:
    veracity_score += 5  # Major weight default
```

Include in total or report separately.

### Recipe 10: Inter-rater agreement

When 2 reviewers score same batch — measure agreement:
```python
from sklearn.metrics import cohen_kappa_score

# Score batch with 2 reviewers
r1 = [scores_reviewer1]   # array of error counts per segment
r2 = [scores_reviewer2]
kappa = cohen_kappa_score(r1, r2)
# κ > 0.6 = good agreement
# κ < 0.4 = re-calibrate reviewers
```

### Recipe 11: Translator scorecard delivery

```markdown
# Translator Quality Report — Q3 2026

## Alice (TransPerfect — de-DE)
- Word count: 24,500
- Avg MQM: 6.8 (target ≤15) ✓
- Critical: 0 | Major: 18 | Minor: 87
- Strongest: technical docs (3.2)
- Weakest: marketing copy (9.5)
- Action: keep on technical; pair with senior on marketing

## Bob (Acclaro — fr-FR)
- Word count: 18,000
- Avg MQM: 11.2 (target ≤5 for marketing) ✗
- Critical: 1 | Major: 12 | Minor: 65
- Pattern: slogan transcreation slightly off-brand
- Action: in-market reviewer cycle + brand voice training
```

### Recipe 12: DQF ↔ MQM crosswalk

DQF uses different terminology but same shape:
```
DQF Adequacy     ↔ MQM Accuracy
DQF Fluency      ↔ MQM Fluency
DQF Style        ↔ MQM Style
DQF Terminology  ↔ MQM Terminology
```

Convert DQF scores to MQM-equivalent for cross-vendor comparison.

### Recipe 13: Adaptive engine self-scoring

memoQ AGT, Lilt, ModernMT return confidence scores per segment:
```python
# Lilt API includes per-segment confidence
high_conf = [s for s in segments if s.confidence > 0.95]
med_conf = [s for s in segments if 0.85 < s.confidence <= 0.95]
low_conf = [s for s in segments if s.confidence <= 0.85]
print(f"High: {len(high_conf)} → auto-approve")
print(f"Med: {len(med_conf)} → spot-review 10%")
print(f"Low: {len(low_conf)} → full PE")
```

### Recipe 14: Sample size for stat-sig

Per-batch MQM is point-in-time; per-translator trend needs sample size:
```
Min for reliable trend:
- 4 batches OR 5000+ words for premium tier
- 6 batches OR 10000+ words for standard tier
```

Below sample size, treat MQM as advisory; not gate.

### Recipe 15: Reviewer calibration

```
Quarterly:
1. Reviewers all score same 500-word batch independently
2. Compare scores
3. Discuss discrepancies → recalibrate
4. Update internal QA guide with examples
```

Without calibration, reviewer-A's "Minor" = reviewer-B's "Major" → invalid trend.

## Examples

### Example 1: Score Q3 batches across 6 locales, identify underperformer

**Goal:** Trend MQM by translator + locale; find who needs intervention.

**Steps:**
1. Pull batch list from TMS (Crowdin / Phrase QA API, Recipe 3).
2. Reviewer scores each batch in CAT tool with MQM categories + severities.
3. Capture per Recipe 1 CSV.
4. Run per-translator aggregation (Recipe 4) — Bob's avg MQM 18.4 for ko-KR.
5. Drill into Bob's batches (Recipe 5) — pattern: terminology errors dominate.
6. Action: re-train Bob on termbase OR reassign ko-KR to alternate translator.

**Result:** ko-KR MQM target met in next quarter (avg 9.2).

### Example 2: CI gate prevents low-quality merge

**Goal:** PR contains translated `de-DE` batch; gate fails if MQM > 15 (UI tier).

**Steps:**
1. PR triggers Recipe 7 workflow.
2. Score script reads `de-DE.xlf` translated segments + Crowdin QA findings.
3. Computes MQM per Recipe 6 — score = 22.4.
4. UI threshold = 15 — gate fails.
5. PR comment: "MQM 22.4 > 15 — see issues: <breakdown>".
6. Vendor re-translates; PR re-runs; passes.

**Result:** Low-quality batches never reach main.

## Edge cases / gotchas

- **MQM is opinionated** — different reviewers score same batch differently. Run inter-rater agreement (Recipe 10) regularly.
- **Sample size matters** — single 500-word batch's MQM is noisy; trend over 5+ batches per translator.
- **Severity inflation** — reviewers tend to grade "Major" out of caution. Calibrate quarterly (Recipe 15).
- **Penalty factor adjustments** — pharma uses 2.0; gaming/casual uses 0.5. Document choice + lock per project.
- **Critical errors poison batch** — single critical = 10 points; on 1000-word batch = score 10 already. Use with caution.
- **Non-errors logged** — reviewers sometimes log preferences as Minor; corrupts trend. Train: "Is this WRONG, or just different from how I'd say it?"
- **DNT violations** — translating brand term ("CraftBot" → "Bastel-Bot") is automatically Critical. Hardcode in TMS QA.
- **Terminology score double-count** — same wrong term across 10 segments = 1 root cause but 10 errors. Decide policy: count once OR count each occurrence.
- **MT-only scoring** — adaptive engine self-scores ≠ human MQM. Don't confuse.
- **Translator sees scores** — share with translator, drives improvement. Hiding leads to repeated errors.
- **Customer-facing reports** — internal MQM may surface critical errors that legal would flag. Sanitize before sharing.
- **DQF deprecation** — TAUS DQF platform sunset in stages; MQM is the going-forward standard.
- **Cross-locale comparison** — MQM scores between locales aren't directly comparable (some languages tolerate more variation). Compare against per-locale target.
- **Time pressure ↔ quality tradeoff** — rush tier batches typically MQM +30-50%. Report rush vs standard separately.
- **Errors per segment not per word** — some MQM variants count per-segment; specify which.

## Sources

- MQM Typology: https://themqm.org/the-mqm-typology/
- MQM 2.0 spec: https://themqm.org/
- TAUS DQF: https://www.taus.net/qe-platform/dynamic-quality-framework
- ISO 5060 (Translation quality evaluation): https://www.iso.org/standard/72079.html
- Lilt MQM: https://lilt.com/blog/measuring-translation-quality
- Phrase TMS QA: https://support.phrase.com/hc/en-us/sections/4406022049820-Quality-Assurance
- MQM scorecard examples: https://www.qt21.eu/mqm-definition/
- Cohen's kappa (sklearn): https://scikit-learn.org/stable/modules/generated/sklearn.metrics.cohen_kappa_score.html
- Welocalize quality: https://www.welocalize.com/solutions/quality-management/
