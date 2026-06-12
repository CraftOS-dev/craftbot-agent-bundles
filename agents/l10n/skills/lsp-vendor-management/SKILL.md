---
name: lsp-vendor-management
description: LSP (Language Service Provider) selection + RFP + MQM scorecard + per-locale rate sheets. Acclaro / TransPerfect / Welocalize / Smartcat / Lilt / Unbabel. Use when the user asks "pick an LSP", "RFP for translation vendor", "negotiate per-word rate", "score our LSP".
---

# LSP Vendor Management

Major 2026 LSPs: **TransPerfect** (global enterprise), **RWS** (Trados parent), **Welocalize** (gaming + life sciences), **Acclaro** (marketing transcreation), **Andovar** (Asian markets), **Smartcat marketplace** (direct translator hire), **Lilt** (tech + adaptive MT + human), **Unbabel** (AI + human, support content).

Vendor selection by domain expertise + per-word price + quality scoring (MQM) + SLA. Dispatch via TMS connector (Crowdin / Phrase / Lokalise all integrate LSP supply).

## When to use

- The user is choosing an LSP for a new project.
- The user wants an RFP brief drafted.
- The user is comparing LSP quotes per language pair.
- The user wants to score current LSP performance (MQM-based).
- The user needs vendor handoff format (XLIFF package, brief, TM/TB).

Trigger phrases: "LSP", "language service provider", "RFP translation", "translation vendor", "per word rate", "MQM scorecard", "TransPerfect", "Acclaro", "Welocalize".

## Setup

```bash
# Smartcat (marketplace + LSP routing)
# Sign up: https://www.smartcat.com/ — get API key

# Lilt enterprise
# Contract via https://lilt.com/

# TransPerfect / RWS / Welocalize / Acclaro — sales contact

# Phrase TMS LSP routing (any TMS-routed LSP)
npm i -g @phrase/cli
```

Auth/env:
- `SMARTCAT_API_KEY` — `https://www.smartcat.com/api`
- `LILT_API_KEY` — enterprise contract

## LSP comparison (2026)

| LSP | Strength | Per-word range (EN→EU) | Domains |
|---|---|---|---|
| TransPerfect | Global enterprise scale | $0.12-0.25 | All |
| RWS (Trados ecosystem) | Established LSP supply chain | $0.10-0.22 | Legal, technical, life sciences |
| Welocalize | Gaming, life sciences | $0.12-0.30 | Gaming, pharma, eDiscovery |
| Acclaro | Marketing transcreation | $0.15-0.40 | Marketing, brand |
| Andovar | Asian market specialization | $0.10-0.30 | JP/KR/CN/TH/VN/ID |
| Smartcat marketplace | Direct hire + DIY contract | $0.06-0.15 | Generalist |
| Lilt | Tech + adaptive MT + human | $0.12-0.25 | Tech, SaaS, support |
| Unbabel | AI + human, support content | $0.08-0.15 | Support, CX |

CJK pricing ~30-50% higher than European pairs.

## Common recipes

### Recipe 1: RFP brief format

```markdown
# Translation Services RFP — <company>

## Scope
- Languages: EN → DE, FR, ES, IT, JA, KO, AR, PT-BR, ZH-Hans-CN, ZH-Hant-TW (10 locales)
- Annual volume: ~1.2M source words (UI 40%, docs 30%, marketing 15%, support 15%)
- Domains: SaaS (data analytics) — technical + UI heavy
- Continuous localization model (weekly drops, not big-bang)

## Required capabilities
- TMS integration: Crowdin connector required
- CAT tool: vendor's choice; we provide TM + TBX
- ICU MessageFormat literate translators
- MQM 2.0 quality reporting per batch
- Per-locale dedicated linguist (no rotation without notice)

## Quality expectations
- MQM premium tier (≤ 5 points / 1000 words) on marketing
- MQM standard tier (≤ 15 points / 1000 words) on UI + docs
- Turnaround: standard tier 5 business days; rush tier 2 business days (50% surcharge)

## Pricing model
- Per source word; leverage discount applied per TMS report
  - 101% in-context: 10% rate
  - 100% exact: 20% rate
  - 95-99% fuzzy: 40% rate
  - 75-94% fuzzy: 60% rate
  - 50-74% partial: 90% rate
  - New segment: 100% rate

## Required RFP response
- Per-locale rate card (above tiers)
- MQM scorecard sample from existing client
- 3 sample translations (provided source attached)
- Linguist CVs for assigned per-locale leads
- Onboarding timeline + KPIs for first 90 days
- SOC 2 / ISO 17100 / ISO 27001 attestation

## Selection criteria (weighted)
- Quality (sample + references): 40%
- Price: 25%
- Turnaround SLA: 15%
- TMS integration depth: 10%
- Domain expertise: 10%
```

### Recipe 2: Per-locale rate sheet template

```csv
locale,new_per_word,fuzzy_95-99,fuzzy_75-94,partial_50-74,exact_100,context_101,rush_surcharge
de-DE,0.13,0.052,0.078,0.117,0.026,0.013,50%
fr-FR,0.12,0.048,0.072,0.108,0.024,0.012,50%
ja-JP,0.18,0.072,0.108,0.162,0.036,0.018,50%
ko-KR,0.17,0.068,0.102,0.153,0.034,0.017,50%
ar,0.14,0.056,0.084,0.126,0.028,0.014,50%
zh-Hans-CN,0.16,0.064,0.096,0.144,0.032,0.016,50%
pt-BR,0.10,0.040,0.060,0.090,0.020,0.010,50%
```

### Recipe 3: Dispatch via TMS LSP routing (Crowdin / Phrase)

```bash
# Crowdin — assign translation to vendor org
crowdin organization-tasks add --vendor-id <VENDOR_ID> \
  --files locales/en.json --languages de,fr,ja

# Phrase TMS — assign job to vendor user
curl -X PATCH 'https://cloud.memsource.com/web/api2/v1/projects/<PID>/jobs/<JID>' \
  -H "Authorization: ApiToken $PHRASE_TMS_TOKEN" \
  -d '{"providers":[{"id":"<VENDOR_USER_ID>","type":"VENDOR"}]}'
```

### Recipe 4: Smartcat marketplace direct dispatch

```bash
curl -X POST 'https://smartcat.com/api/integration/v2/project' \
  -H "Authorization: Basic $SMARTCAT_API_KEY" \
  -d '{
    "name": "release-2026-Q3",
    "sourceLanguage": "en",
    "targetLanguages": ["de", "fr", "ja"],
    "workflowStages": ["translation", "editing", "proofreading"],
    "deadline": "2026-07-15T00:00:00Z"
  }'
```

Smartcat auto-finds translators matching specialization + rate; marketplace bid model.

### Recipe 5: Vendor handoff package

Include:
1. `source.xliff` — XLIFF 2.0 with all segments + metadata + IDs
2. `tm-domain.tmx` — reference TM (read-only for vendor)
3. `termbase.tbx` — locked termbase
4. `brief.md` — domain notes + brand voice
5. `style-guide-<locale>.md` — per-locale tone reference
6. `glossary-forbidden.csv` — DNT + forbidden terms
7. `reference-screenshots/` — UI context

Zip + email or attach in TMS task.

### Recipe 6: Vendor scoring spreadsheet (MQM)

```csv
vendor,locale,batch_id,word_count,critical_errors,major_errors,minor_errors,mqm_score,sla_met,notes
TransPerfect,de-DE,2026-06-batch1,12000,0,3,12,3.5,yes,Strong technical
Acclaro,fr-FR,2026-06-batch1,8000,1,5,18,8.2,yes,Marketing transcreation excellent
Welocalize,ja-JP,2026-06-batch1,9500,0,2,8,2.6,yes,Strong domain expertise
Smartcat,ko-KR,2026-06-batch1,4500,2,8,22,16.4,no,Translator rotation issue
```

MQM score = `(critical×10 + major×5 + minor×1) × 1000 / word_count`.

Targets:
- Premium (legal, marketing): ≤ 5 points / 1000
- Standard (UI, support, docs): ≤ 15 points / 1000
- Functional (internal, dev tooling): ≤ 30 points / 1000

### Recipe 7: SLA tracking dashboard

```python
import pandas as pd
df = pd.read_csv('vendor-scorecards.csv')
trend = df.groupby(['vendor', 'locale']).agg(
    avg_mqm=('mqm_score', 'mean'),
    sla_pct=('sla_met', lambda x: (x == 'yes').mean() * 100),
    word_count=('word_count', 'sum'),
    batches=('batch_id', 'nunique')
).sort_values(['avg_mqm', 'sla_pct'])
print(trend)
```

### Recipe 8: Quarterly vendor review template

```markdown
# Vendor Review Q3 2026 — <Vendor Name>

## Volume
- Words translated: 287,000
- Locales: de-DE, fr-FR, ja-JP, ko-KR, ar
- Batches: 12

## Quality (MQM 2.0)
- de-DE: 4.2 (premium target ≤5 — PASS)
- fr-FR: 6.1 (standard target ≤15 — PASS)
- ja-JP: 3.8 (premium target ≤5 — PASS)
- ko-KR: 8.5 (premium target ≤5 — FAIL)
- ar: 11.2 (standard target ≤15 — PASS, borderline)

## SLA
- Standard tier: 11/12 batches on time (92%)
- Rush tier: 4/4 batches on time (100%)

## Issues
- 2 critical errors in marketing copy (slogan mistranslation)
- ko-KR linguist rotation without notice — caused drift

## Action
- Replace ko-KR linguist or transfer ko-KR to alternate vendor
- Add backtranslation gate to marketing copy
- Renew contract for 4 locales; ko-KR up for re-bid
```

### Recipe 9: Termbase + TM handoff to vendor (read-only)

```bash
# Export TM/TB from TMS
crowdin tm download --id <TM_ID> --format tmx -o handoff/tm-ui.tmx
crowdin glossary download --id <GL_ID> --format tbx -o handoff/brand.tbx

# Zip
zip handoff-2026-Q3.zip handoff/*

# Send to vendor with read-only access in TMS:
crowdin organization-tasks add --vendor-id <VID> --task-type translate \
  --files <FILE_ID> --tm-id <TM_ID> --read-only-tm
```

### Recipe 10: Translator preferences (per locale)

```yaml
# vendor-preferences.yml
de-DE:
  primary: TransPerfect (linguist: A. Mueller, since 2024)
  backup: Welocalize (linguist: B. Schmidt)
  formality: Sie (formal address)
  style: confident, slightly playful
fr-FR:
  primary: Acclaro (linguist: C. Dubois)
  formality: vous (formal)
  style: elegant, slightly indirect
ja-JP:
  primary: Andovar (linguist: 田中)
  formality: です/ます
  style: warm, respectful
```

Provide to each new vendor onboarding pack.

### Recipe 11: Backtranslation gate (high-stakes copy)

```
1. Vendor delivers DE translation of marketing hero
2. Independent translator (different vendor) back-translates DE → EN literally
3. Compare back-translation to source — discrepancies flagged
4. Reviewer (marketing lead) approves or requests revision
```

Common for regulated industries (pharma, finance) + brand-critical copy.

### Recipe 12: Onboarding checklist for new vendor

```markdown
- [ ] NDA signed
- [ ] DPA (Data Processing Agreement) signed — GDPR-relevant
- [ ] TMS access provisioned (Crowdin/Phrase/Lokalise org-level)
- [ ] TM + TBX delivered (read-only)
- [ ] Brand voice guide + locale-specific style guides
- [ ] Glossary (forbidden + preferred terms)
- [ ] Sample brief — translator returns 100-word test
- [ ] MQM scorecard format reviewed
- [ ] Escalation contact list
- [ ] First batch in dry-run (low-stakes content)
- [ ] First-batch MQM review meeting
- [ ] 90-day KPIs defined
```

## Examples

### Example 1: Pick LSP for 10-locale SaaS expansion

**Goal:** Annual $200k translation budget; need MQM ≤10 across 10 locales.

**Steps:**
1. Issue RFP (Recipe 1) to 4 LSPs: TransPerfect, Welocalize, Acclaro, Smartcat.
2. Score responses on quality (40%) / price (25%) / SLA (15%) / TMS (10%) / domain (10%).
3. Sample translations: 300 words per LSP per priority locale (de, ja, ar).
4. In-market reviewer scores samples MQM.
5. Final selection: TransPerfect for de/fr/es/it (EU strength); Andovar for ja/ko/zh; Acclaro for marketing batches.
6. Onboard (Recipe 12) — 90-day pilot before full commit.

**Result:** Multi-vendor model; risk-distributed; per-locale specialists.

### Example 2: Replace underperforming LSP for ko-KR

**Goal:** Current LSP MQM 18.4 for ko-KR (target ≤15); customer complaints.

**Steps:**
1. Pull current LSP MQM trend (Recipe 7) — confirms 8-week deterioration.
2. Send replacement RFP to Andovar + Welocalize for ko-KR only.
3. Run 500-word test batch with both alternates.
4. In-market reviewer ranks.
5. Onboard winner (Andovar) per Recipe 12.
6. Transition existing TM + TBX from old to new vendor (Recipe 9).
7. Track new vendor's MQM weekly for 90 days.

**Result:** ko-KR MQM improves to 5.5 within 6 weeks; customer complaints stop.

## Edge cases / gotchas

- **Don't trust LSP's self-reported MQM** — run independent QA via Xbench / Checkmate (see `locale-qa-linguistic-functional` skill).
- **Per-word price hides total cost** — leverage discount + minimum job fees + project management + rush surcharges = effective rate often 30-50% above headline.
- **Linguist rotation = quality drift** — require vendor to disclose linguist changes; lock leads via contract.
- **TMS connector limitations** — Crowdin's vendor marketplace doesn't expose all LSPs; some require direct contract.
- **NDA + DPA required for any vendor** — GDPR exposure; never ship customer-data containing strings to LSP without DPA.
- **CJK rate premium** — JA/KO/ZH typically 30-50% above EU rates; budget appropriately.
- **Minimum job fees** — many LSPs have $50-100 minimums; small batches are inefficient.
- **Translation memory ownership** — clarify in contract; default: client owns TM; vendor cannot reuse for other clients.
- **Terminology drift across LSPs** — if multi-LSP, share termbase + run weekly cross-vendor terminology audits.
- **Rush job stress** — quality drops on rush tier; reserve for genuine emergencies.
- **Single-vendor lock-in** — multi-vendor reduces risk but increases coordination cost. Worth it above $100k/year spend.
- **SOC 2 / ISO 17100** — enterprise procurement requires these; verify cert dates.
- **Domain mismatch** — Acclaro is great for marketing, weak on technical docs. Match vendor to domain.
- **Time zone for rush** — assigning ja-JP work to a US vendor on Friday EST = Monday delivery (no JA linguists Saturday).
- **In-market vs near-shore** — true in-country linguist = +$0.02-0.05/word vs offshore.

## Sources

- MQM framework: https://themqm.org/
- DQF (TAUS): https://www.taus.net/qe-platform/dynamic-quality-framework
- TransPerfect: https://www.transperfect.com/
- RWS / Trados: https://www.rws.com/
- Welocalize: https://www.welocalize.com/
- Acclaro: https://www.acclaro.com/
- Andovar: https://www.andovar.com/
- Smartcat marketplace: https://www.smartcat.com/
- Lilt: https://lilt.com/
- Unbabel: https://unbabel.com/
- LSP comparison 2026: https://intlpull.com/blog/top-10-localization-tools-tms-comparison-2026
- Smartcat API: https://developers.smartcat.com/
- ISO 17100 translation services: https://www.iso.org/standard/59149.html
- ISO 18587 PEMT: https://www.iso.org/standard/62970.html
