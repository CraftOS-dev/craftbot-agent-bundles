<!--
Source: https://www.meddicc.com/ + https://www.gong.io/blog/meddpicc/
MEDDIC + MEDDPICC qualification execution + 0-3 scoring rubric (June 2026).
-->
# MEDDIC + MEDDPICC Qualification — SKILL

MEDDIC (Metrics / Economic buyer / Decision criteria / Decision process / Identify pain / Champion) is the gold-standard qualification framework for complex B2B > $25K ACV. MEDDPICC adds **P**aper process + **C**ompetition for enterprise > $100K. This skill is how the agent runs the framework: defines each field, scores 0-3, rolls up to forecast bucket, and surfaces the next missing field as the agent's next-best-action.

## When to use

- **Any deal > $25K ACV with multiple stakeholders** — default to MEDDIC.
- **Enterprise deal > $100K ACV** — upgrade to MEDDPICC (adds Paper + Competition).
- **Post-discovery-call MEDDIC fill** — extract from transcript via `gong-chorus-call-intelligence` recipe 10, then PATCH to CRM.
- **Forecast roll-up** — sum scores, bucket into Commit / Best Case / Pipeline.
- **Trigger phrases**: "score this deal", "MEDDIC for account X", "what's missing on this opp", "forecast roll-up", "qualify in or out", "MEDDPICC review".

Do NOT use this skill for: **transactional / SMB < $25K ACV** (use `bant-spin-challenger-frameworks` — BANT is faster); **inbound MQL qualification** (BANT or HubSpot's GPCT); **pure discovery prep** (use SPIN from `bant-spin-challenger-frameworks`).

## Setup

```bash
# CRM custom fields must exist. One-time setup per portal/org.
# HubSpot example — create via api-gateway
export MATON_API_KEY="<key>"

for field in meddic_metrics meddic_economic_buyer meddic_decision_criteria \
             meddic_decision_process meddic_identify_pain meddic_champion \
             meddpicc_paper_process meddpicc_competition meddic_score; do
  curl -X POST "https://gateway.maton.ai/hubspot/crm/v3/properties/deals" \
    -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
    -d "{\"name\":\"$field\",\"label\":\"$field\",\"type\":\"string\",\"fieldType\":\"textarea\",\"groupName\":\"dealinformation\"}"
done

# Salesforce — use Object Manager → Opportunity → New Field; or Metadata API.
```

No external API keys needed beyond CRM. The framework lives entirely in: (1) CRM custom fields, (2) the scoring rubric, (3) the agent's reasoning over discovery / call data.

## Common recipes

### Recipe 1: MEDDIC field definitions (canonical reference)

| Letter | Field | Definition | Validation source |
|---|---|---|---|
| M | Metrics | Measurable business outcome the buyer will own (e.g., "reduce CAC 20% in 6 months"). Dollar or % preferred. | Buyer-stated in call; documented in CRM |
| E | Economic buyer | Named individual with budget authority — NOT influencer, NOT champion (unless champion = decision-maker). | Title + name; confirmed via org chart / Sales Nav |
| D | Decision criteria | Explicit criteria the buying committee will evaluate on (technical, business, vendor stability, security, ROI). | Buyer-stated; ideally documented in a procurement RFP |
| D | Decision process | Step-by-step path from current state to signed contract (demo → security → procurement → legal → exec sign). | Champion-walked-through; mapped on a MAP |
| I | Identify pain | Specific business pain felt by named people. Quantified where possible. | Quoted from buyer in discovery; same pain echoed by 2+ stakeholders |
| C | Champion | Named individual actively advocating internally. Must have evidence of advocacy (intro to EB, internal slide, quote). | Documented advocacy moment in CRM activity log |

### Recipe 2: Scoring rubric (0-3 per field)

```
0 = Empty / unknown
1 = Hypothesis — agent or AE has a guess but buyer hasn't confirmed
2 = Validated by prospect (stated in call or email) but not documented with evidence in CRM
3 = Validated by prospect AND documented with evidence (quoted, attached, or linked) in CRM
```

Roll-up:
- **MEDDIC (6 fields, max 18)**: ≥ 14 = Commit-bucket eligible. 10-13 = Best Case. < 10 = Pipeline only.
- **MEDDPICC (8 fields, max 24)**: ≥ 19 = Commit. 14-18 = Best Case. < 14 = Pipeline.

### Recipe 3: Auto-fill MEDDIC from a Gong transcript (LLM extraction)

```python
# Reuse gong-chorus-call-intelligence recipe 10
# After extraction, write back to HubSpot deal:
import requests, os
meddic = {  # output from Recipe 10 of gong skill
    "metrics": "Reduce CAC by 20% in 6 months", "metrics_score": 2,
    "economic_buyer": "Sarah Lee, VP Sales", "economic_buyer_score": 2,
    "decision_criteria": "SOC 2, ROI > 3x, < 30d onboarding", "decision_criteria_score": 3,
    "decision_process": "demo → security → procurement → exec", "decision_process_score": 2,
    "identify_pain": "Outbound 2% reply, lost $1.2M last year", "identify_pain_score": 3,
    "champion": "AE Director Jaime Cruz", "champion_score": 2,
}
total = sum(v for k, v in meddic.items() if k.endswith("_score"))

requests.patch(
    f"https://gateway.maton.ai/hubspot/crm/v3/objects/deals/{DEAL_ID}",
    headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"},
    json={"properties":{
        "meddic_metrics":meddic["metrics"],
        "meddic_economic_buyer":meddic["economic_buyer"],
        "meddic_decision_criteria":meddic["decision_criteria"],
        "meddic_decision_process":meddic["decision_process"],
        "meddic_identify_pain":meddic["identify_pain"],
        "meddic_champion":meddic["champion"],
        "meddic_score":str(total),
    }}
)
```

### Recipe 4: MEDDPICC additional fields

```
P = Paper process — Vendor onboarding + security review + MSA timeline. Maps to realism of close date.
C = Competition — Named competitors in the deal + their position. "No competition" is a red flag (buyer hasn't decided to buy at all).
```

Scoring identical to MEDDIC (0-3). Add to the same property batch.

### Recipe 5: Roll-up forecast bucket from score

```python
def bucket(score, framework="meddic"):
    if framework == "meddic":
        if score >= 14: return "commit"
        if score >= 10: return "best_case"
        return "pipeline"
    if framework == "meddpicc":
        if score >= 19: return "commit"
        if score >= 14: return "best_case"
        return "pipeline"
```

Pair with `clari-forecasting-commit-accuracy` skill recipes for full forecast doc.

### Recipe 6: Identify the next missing field (NBA hook)

```python
PRIORITY_ORDER = ["champion", "identify_pain", "economic_buyer", "metrics",
                  "decision_criteria", "decision_process", "competition", "paper_process"]

def next_meddic_gap(deal_record):
    """Return the highest-priority field with score < 2."""
    for field in PRIORITY_ORDER:
        score = int(deal_record.get(f"meddic_{field}_score", 0) or deal_record.get(f"meddpicc_{field}_score", 0) or 0)
        if score < 2:
            return field
    return None
```

The agent surfaces the field with the literal question to ask in the next call.

### Recipe 7: Discovery question bank by MEDDIC field

```yaml
# Use during discovery call prep
metrics:
  - "What does success look like in 12 months — measurably?"
  - "If we solved this, what business metric moves and by how much?"
economic_buyer:
  - "Who else needs to weigh in on a decision like this?"
  - "If we move forward, who signs the contract on your side?"
decision_criteria:
  - "What criteria will your team use to evaluate?"
  - "If you brought this to <EB title>, what would they ask?"
decision_process:
  - "Walk me through how a purchase like this happens at <company>."
  - "What are the stages — discovery, evaluation, security, legal, sign-off?"
identify_pain:
  - "What's the cost of not solving this for another 6 months?"
  - "Who feels this pain most? Can you name them?"
champion:
  - "If we did this, who internally would be excited?"
  - "Who would you partner with to drive this initiative?"
competition (MEDDPICC):
  - "Who else are you looking at?"
  - "What's their pitch / what attracted you?"
paper_process (MEDDPICC):
  - "How long does procurement / security typically take?"
  - "Do you have a preferred MSA template, or do you use ours?"
```

### Recipe 8: Quality check — flag fake MEDDIC

Common patterns that masquerade as score-3 but should be 1 or 2:

```python
RED_FLAGS = {
    "metrics": ["improve productivity", "save time", "be more efficient"],  # vague
    "economic_buyer": ["the team", "leadership", "we"],                       # not a name
    "champion": ["everyone's excited", "they all liked it"],                  # no individual
    "identify_pain": ["nice to have", "would be cool"],                       # not pain
    "decision_process": ["soon", "in a few weeks"],                           # not a process
    "decision_criteria": ["price and value", "the best solution"],            # not real criteria
}

def downgrade_if_vague(field, value):
    flags = RED_FLAGS.get(field, [])
    if any(flag in (value or "").lower() for flag in flags):
        return 1   # downgrade to hypothesis
    return None
```

### Recipe 9: SDR ↔ AE handoff with MEDDIC starter

```yaml
# Minimum MEDDIC fill required for SDR → AE handoff
# (AE rejects handoff if any field below missing)
required_at_handoff:
  metrics: score >= 1 (hypothesis OK)
  economic_buyer: score >= 1 (title at minimum)
  identify_pain: score >= 2 (must be prospect-stated)
  champion: score >= 1 (candidate identified)
optional_at_handoff:
  decision_criteria, decision_process, competition, paper_process
```

If handoff doesn't meet bar → AE returns to SDR with rejection reason (per role.md SLA: 4 business hours).

### Recipe 10: Multi-stakeholder MEDDIC (enterprise)

For deals with > 3 stakeholders, MEDDIC fields are *per-stakeholder-perspective*:

```python
# Store as JSON in a custom property
meddic_per_stakeholder = {
    "champion_jaime": {
        "metrics": "20% CAC reduction",
        "decision_criteria": ["SOC 2", "ROI", "UX"],
    },
    "eb_sarah": {
        "metrics": "Hit Q4 number",
        "decision_criteria": ["payback < 12mo", "vendor stability"],
    },
    "technical_evaluator_alex": {
        "metrics": "API latency p99 < 200ms",
        "decision_criteria": ["SSO", "audit log", "data residency"],
    },
}
```

When buying committees split on criteria, your proposal must address each lens.

## Examples

### Example 1: Post-discovery MEDDIC fill

**Goal:** 30 minutes after a discovery call ends, the deal record has MEDDIC scored and the next-step task is created.

**Steps:**
1. Gong webhook fires on call-end → 10-min delay → pull transcript via `gong-chorus-call-intelligence` recipe 2.
2. Recipe 3 (LLM extraction) extracts each field + score.
3. Recipe 8 downgrades vague fields.
4. PATCH deal in HubSpot (Recipe 3 here writes `meddic_*` properties + `meddic_score`).
5. Recipe 6 identifies the highest-priority gap (e.g., `economic_buyer` still score 0).
6. Create a HubSpot task on the AE: "Identify EB before next call — ask champion ‘who signs?’"

**Result:** Deal record fully scored with no manual entry; next-step queued.

### Example 2: Friday forecast review

**Goal:** Friday 5pm, generate a forecast doc grouping all open deals by MEDDIC-derived bucket.

**Steps:**
1. Pull all open deals: `hubspot-sales-mcp` recipe 1 with `properties=[..., meddic_score, meddpicc_score]`.
2. Recipe 5 — bucket each deal.
3. For Commit bucket: list with amount + close date + EB name. Flag any deal where `meddic_score >= 14` but `champion_score < 2` (over-rated risk).
4. For Best Case: list with single-line "NBA: <field gap>".
5. For Pipeline: count only — no detail.
6. Render to Notion via `notion-mcp` + Slack DM the AE + manager.

**Result:** Disciplined three-bucket forecast every Friday; commit accuracy measured by Monday's diff.

## Edge cases / gotchas

- **"Champion" ≠ "nice person on the call".** A champion takes risk for you internally — sets up meetings, sends docs around, defends you in committee. Without an *advocacy moment* in the CRM activity log, champion = hypothesis (score 1 max).
- **EB inflation** — AEs love to mark a Director as the EB. If the deal > $100K, EB is usually VP/C-level. Mismatched EB = late-stage "I need to run this by my boss" surprise.
- **"No competition" is a red flag**, not a green light — it usually means the buyer hasn't decided whether to buy *at all*. Mark Competition score = 0 and ask "What's the alternative if we don't move forward?"
- **Metrics without quantification = score 1.** "Save time" is hypothesis; "save 15 hours/week per team of 10" is validated.
- **Decision process drift**: buyer's stated process changes mid-cycle ("now legal needs to review"). Treat each surprise as -1 from `decision_process_score`; trigger a MAP refresh.
- **Champion silence > 7 days drops score by 1.** Silence usually means: (a) lost internally, (b) busy with something else, (c) you're not the priority. NBA: send ammunition + check-in.
- **MEDDIC is not BANT.** Don't conflate — Budget lives nowhere in MEDDIC (it's implied in Metrics + Decision Criteria). If you need explicit budget, use BANT for that field or add a custom `budget` field.
- **MEDDPICC's Paper process is often underweighted.** Enterprise deals stall 30-60 days in legal / procurement; a P score of 0-1 means your close date is unrealistic.
- **Don't fake-score to hit Commit.** Manager review will catch it; commit accuracy will tank next quarter. Honest 9/18 with a clear NBA is better than fake 14/18.
- **Re-score on every meaningful event** — new stakeholder identified, EB confirmed, pricing shared, competitor disclosed. Stale MEDDIC = stale forecast.
- **Across CRM-handoff**: MEDDIC fields must be *deal-level*, not contact-level. If you put them on contacts, multiple deals with same contact will overwrite each other.

## Sources

- MEDDICC methodology (official): https://www.meddicc.com/
- Gong's MEDDPICC primer (2024): https://www.gong.io/blog/meddpicc/
- "How to actually run MEDDIC" — Sam Jacobs: https://blog.salesblazer.com/meddic
- Force Management MEDDIC playbook: https://www.forcemanagement.com/blog/meddic-sales-process
- 2026 MEDDIC + AI: extracting fields from call data: https://www.gong.io/blog/meddic-ai/
- HubSpot custom property setup for MEDDIC: https://knowledge.hubspot.com/properties/create-and-edit-properties
