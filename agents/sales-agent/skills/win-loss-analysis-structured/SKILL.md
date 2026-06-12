<!--
Source: https://www.gong.io/blog/win-loss-analysis/ + internal post-mortem templates
Structured win/loss post-mortems with tag rollup (June 2026).
-->
# Win/Loss Analysis (Structured) — SKILL

Every closed-won AND closed-lost deal gets a 5-section post-mortem: trigger event, our diagnosis quality, decision-criteria match, competitor (if lost), what to repeat / what to change. Tag each post-mortem with structured fields (industry, deal size, cycle days, primary competitor, lost reason) so quarterly rollup queries surface trends — not anecdotes.

## When to use

- **Every closed-won deal** — 30-day window from close.
- **Every closed-lost deal** — same window; especially urgent for >$50K losses.
- **Quarterly rollup** — aggregate tagged post-mortems to surface patterns: "we lost 4 of 7 deals to <competitor> on price in segment X".
- **Pre-renewal review** — if an existing customer is churning, run win/loss-style post-mortem on the relationship.
- **Trigger phrases**: "post-mortem this deal", "win/loss review", "why did we lose X", "quarterly W/L rollup", "tag this lost deal", "what's our W/L trend".

Do NOT use this skill for: **mid-deal coaching** (use `deal-coaching-next-best-action`); **fresh discovery prep** (use `account-research-deep`); **commission disputes** (handoff to `finance-controller`).

## Setup

```bash
export MATON_API_KEY="<key>"           # CRM access
export NOTION_TOKEN="<key>"            # Win/Loss DB lives in Notion
export GONG_ACCESS_KEY="<key>"         # for sentiment + objection mining

# Notion DB schema (create once)
# Properties:
#   - Deal name (title)
#   - Outcome (select: Won / Lost)
#   - ACV (number)
#   - Cycle days (number)
#   - Industry (select)
#   - Deal size tier (select: SMB / Mid / Enterprise)
#   - Primary competitor (select)
#   - Lost reason (multi-select: pricing / feature_gap / no_decision / chose_competitor / timing / champion_lost)
#   - Won reason (multi-select: pricing / feature_win / champion_advocacy / proof / timing / relationship)
#   - Trigger event (text)
#   - Our diagnosis quality (select: accurate / partial / wrong)
#   - What to repeat / change (rich text)
#   - Closed date (date)
```

## Common recipes

### Recipe 1: 5-section post-mortem template (canonical)

```markdown
# Post-Mortem — [Account Name] · [Won / Lost] · [Close Date]

## Deal context
- ACV: $___
- Cycle days from first touch to close: ___
- Primary competitor: ___ (or "no competition")
- Industry / size / vertical: ___

## 1. Trigger event (what initiated the deal)
[Plain-text — what made them buy / not buy at this moment]

## 2. Our diagnosis quality
- Pain we identified: ___
- Was that the real pain? [Yes / Partially / No]
- What we missed: ___

## 3. Decision criteria match
- Their stated criteria: ___
- Our score on each criterion (as THEY evaluated us, not us): ___

## 4. Competitor (if lost)
- Who: ___
- Why they won: [pricing / feature / relationship / brand / timing / other]
- What we'd need to change to win next time: ___

## 5. What to repeat (won) / what to change (lost)
1. ___
2. ___
3. ___

## Structured tags
- Industry: ___
- Deal size tier: SMB / Mid / Enterprise
- Cycle band: < 30d / 30-90d / 90-180d / > 180d
- Primary competitor: ___
- Lost reason: [pricing / feature gap / no decision / chose competitor / timing / champion lost]
- Won reason: [pricing / feature win / champion advocacy / proof / timing / relationship]
```

### Recipe 2: Pull deal + linked calls + emails (data prep)

```bash
# Get the deal
curl "https://gateway.maton.ai/hubspot/crm/v3/objects/deals/<deal-id>?associations=contacts,companies,notes,emails,calls,tasks&properties=dealname,amount,closedate,createdate,dealstage,meddic_score,meddpicc_competition,closed_lost_reason,won_reason" \
  -H "Authorization: Bearer $MATON_API_KEY" > deal.json

# Get the associated Gong calls
curl -X POST "https://gateway.maton.ai/gong/v2/calls/extensive" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{"filter":{"crmAccountId":"<account-id>"}}' > calls.json
```

### Recipe 3: Extract trigger event from call transcripts (LLM)

```python
# Look at the FIRST discovery call (or first inbound contact)
# What did the buyer say prompted them to engage?
import anthropic, os
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

first_call_transcript = open("/tmp/first-call.txt").read()
prompt = f"""From this first sales discovery call transcript, identify the TRIGGER EVENT — what specifically prompted the buyer to evaluate vendors at this moment? 

Common trigger types:
- internal_pain_threshold (existing approach broke at scale)
- leadership_change (new VP/CXO mandated change)
- funding_event (new capital → tooling refresh)
- competitor_failure (their existing vendor failed)
- mandate_from_above (board/exec directive)
- compliance_deadline (regulatory or audit requirement)
- contract_expiration (forced renegotiation)
- m_a_event (acquisition or merger)

Return JSON: {{trigger_type: <category>, trigger_summary: <verbatim quote or paraphrase>, confidence: 0-3}}

Transcript:
{first_call_transcript}
"""

resp = client.messages.create(model="claude-sonnet-4-5", max_tokens=500, messages=[{"role":"user","content":prompt}])
trigger = json.loads(resp.content[0].text)
```

### Recipe 4: Extract competitor (if lost)

```python
# Search all call transcripts + email replies for competitor mentions
import re
COMPETITORS = ["VendorA","VendorB","VendorC","Status Quo"]
def detect_competitor(corpus):
    counts = {c: len(re.findall(rf"\b{c}\b", corpus, re.I)) for c in COMPETITORS}
    return max(counts, key=counts.get) if max(counts.values()) > 0 else None
```

For lost deals, follow up with a buyer interview: "Mind sharing — who did you go with?" Even 50% buyer-interview rate gives much cleaner competitor data than transcript-mining alone.

### Recipe 5: Categorize lost reason (LLM + buyer interview)

```python
LOST_REASONS = [
    "pricing",          # too expensive vs alternatives
    "feature_gap",      # missing specific capability
    "no_decision",      # buyer chose to do nothing
    "chose_competitor", # picked another vendor
    "timing",           # not now; revisit later
    "champion_lost",    # internal champion left or lost authority
    "budget_pulled",    # funding evaporated
    "process_failure",  # we mis-handled a step (RFP, security review)
]

prompt = f"""Based on the deal history (last 5 emails + last call transcript) categorize the primary lost reason from: {LOST_REASONS}. Return JSON with primary_reason + secondary_reason (or null) + 1-line evidence_quote."""
```

### Recipe 6: Categorize won reason

```python
WON_REASONS = [
    "pricing",              # we were cheaper / better ROI
    "feature_win",          # specific capability won it
    "champion_advocacy",    # internal champion drove it home
    "proof",                # case study / reference call sealed it
    "timing",               # we showed up at the right moment
    "relationship",         # AE relationship overcame parity
    "incumbent_failure",    # competitor lost trust
]
```

### Recipe 7: Buyer interview script (3-question minimum)

```markdown
# Win/Loss Buyer Interview Script (10 min)

Hi [Name] — thanks for taking 10 min. We're trying to learn, not pitch.

## Question 1 (open)
"Looking back at the eval, what was the single biggest factor in your decision?"

## Question 2 (us vs alternative)
"What did [winner] do well that we either didn't do or didn't do as well?"

## Question 3 (if lost — recommendation)
"If you were advising us on how to improve, what one thing would you tell us?"

## Optional Question 4 (signal-quality)
"What was the trigger that made you start evaluating?"

[Record + transcribe via Fathom; structured fields populated post-call]
```

### Recipe 8: Write post-mortem to Notion DB

```bash
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent":{"database_id":"<winloss-db-id>"},
    "properties":{
      "Deal name":{"title":[{"text":{"content":"Acme — Lost Q3"}}]},
      "Outcome":{"select":{"name":"Lost"}},
      "ACV":{"number":85000},
      "Cycle days":{"number":78},
      "Industry":{"select":{"name":"SaaS"}},
      "Deal size tier":{"select":{"name":"Mid"}},
      "Primary competitor":{"select":{"name":"VendorA"}},
      "Lost reason":{"multi_select":[{"name":"pricing"},{"name":"chose_competitor"}]},
      "Closed date":{"date":{"start":"2026-06-02"}}
    },
    "children":[
      {"object":"block","type":"heading_2","heading_2":{"rich_text":[{"text":{"content":"Trigger event"}}]}},
      {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"text":{"content":"VP Sales hired in Feb, mandate to fix outbound; reply rate had collapsed to 1%."}}]}}
    ]
  }'
```

### Recipe 9: Quarterly rollup query

```sql
-- Run against Notion DB exported to postgresql, or against HubSpot deals
SELECT
    industry,
    deal_size_tier,
    primary_competitor,
    COUNT(*) FILTER (WHERE outcome='Won') AS won,
    COUNT(*) FILTER (WHERE outcome='Lost') AS lost,
    ROUND(100.0 * COUNT(*) FILTER (WHERE outcome='Won') / NULLIF(COUNT(*),0), 1) AS win_rate,
    AVG(acv) FILTER (WHERE outcome='Won') AS avg_acv_won,
    AVG(cycle_days) AS avg_cycle_days,
    STRING_AGG(DISTINCT lost_reason::text, ', ') FILTER (WHERE outcome='Lost') AS lost_reasons
FROM win_loss
WHERE closed_date >= '2026-04-01' AND closed_date < '2026-07-01'
GROUP BY industry, deal_size_tier, primary_competitor
ORDER BY won DESC, lost DESC;
```

### Recipe 10: Pattern-detection alerts

```python
# Fire alert if pattern emerges in a single quarter
# Example: lost 3+ deals to same competitor on same lost-reason
ALERT_PATTERNS = [
    {"name":"competitor_streak","query":"SELECT primary_competitor, COUNT(*) FROM win_loss WHERE outcome='Lost' AND closed_date >= NOW()-INTERVAL '90d' GROUP BY primary_competitor HAVING COUNT(*) >= 3"},
    {"name":"pricing_loss_streak","query":"SELECT industry, COUNT(*) FROM win_loss WHERE outcome='Lost' AND 'pricing' = ANY(lost_reasons) AND closed_date >= NOW()-INTERVAL '60d' GROUP BY industry HAVING COUNT(*) >= 3"},
    {"name":"no_decision_streak","query":"SELECT COUNT(*) FROM win_loss WHERE outcome='Lost' AND 'no_decision' = ANY(lost_reasons) AND closed_date >= NOW()-INTERVAL '90d' HAVING COUNT(*) >= 5"},
]
```

Wire to Slack via `slack-mcp` — leadership ping when pattern detected.

### Recipe 11: 30-day SLA enforcement

```python
# Cron: find deals closed in last 35 days without a post-mortem
import datetime, requests
cutoff = (datetime.date.today() - datetime.timedelta(days=35)).isoformat()
closed_deals = requests.post(
    "https://gateway.maton.ai/hubspot/crm/v3/objects/deals/search",
    headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"},
    json={"filterGroups":[{"filters":[
        {"propertyName":"closedate","operator":"GTE","value":cutoff},
        {"propertyName":"closedate","operator":"LT","value":datetime.date.today().isoformat()},
        {"propertyName":"dealstage","operator":"IN","values":["closedwon","closedlost"]}
    ]}],"properties":["dealname","closedate","postmortem_completed"],"limit":100},
).json()

for deal in closed_deals["results"]:
    if deal["properties"].get("postmortem_completed") != "true":
        # Slack the owner: "Post-mortem overdue for <deal>"
        pass
```

## Examples

### Example 1: Lost-deal post-mortem within 7 days of close

**Goal:** A $120K deal closed lost yesterday; produce structured post-mortem + leadership-ready summary.

**Steps:**
1. Recipe 2 — pull deal + calls + emails.
2. Recipe 3 — extract trigger event from first call.
3. Recipe 4 — detect competitor; cross-check with `meddpicc_competition` CRM field.
4. Recipe 5 — categorize lost reason (LLM extraction).
5. Schedule a buyer interview (Recipe 7) within 7 days of loss.
6. After buyer interview, refine lost reason; update Notion record.
7. Recipe 8 — write to Notion DB with full tags.
8. Slack the team channel with 3-sentence summary + tag.

**Result:** Within 7 days the loss is structured, tagged, and contributes to quarterly rollup.

### Example 2: Quarterly W/L rollup (board prep)

**Goal:** Board meeting next week; need W/L trends for Q2.

**Steps:**
1. Recipe 9 — run rollup query against Q2 closed deals.
2. Generate charts (win rate by segment, lost reasons by competitor, cycle days trend).
3. Recipe 10 — flag the 2-3 patterns that need leadership attention.
4. Render to `pptx` via `pptx` default skill or `notion-mcp` page.
5. Annotate with 1-2 "what we're changing because of this" recommendations.

**Result:** Board sees pattern, not anecdote; sales-leadership has concrete improvement actions.

## Edge cases / gotchas

- **Buyer interviews drive >2x more accurate lost-reasons.** AE-reported lost reasons are biased ("they went cheap"). Buyer-stated reasons unearth real product gaps.
- **AEs hate doing post-mortems on losses.** Make it the manager's job to gather data + interview the buyer; AE provides timeline + their POV separately.
- **30-day SLA is real.** Beyond 30 days, memory fades + buyer becomes harder to reach. Recipe 11 enforces.
- **Tagging discipline** — if "lost reason" is a freeform field, rollups are useless. Multi-select with controlled vocab (Recipe 5) is the only way to make trend analysis work.
- **"No decision" is the most under-categorized lost reason.** AEs report it as "competitor" because admitting they failed to qualify is harder. Cross-check: if there's no competitor named in any call or email, lost_reason should default to "no_decision".
- **Won post-mortems matter more than people think.** "We won, so what's there to learn?" misses the point — *why* we won is more replicable than *why* we lost. Force won post-mortems too.
- **Competitor detection on transcripts is noisy.** "We've heard about Vendor X" ≠ "we are evaluating Vendor X". Confirm via the MEDDPICC competition field or buyer interview.
- **Cycle band binning matters.** "78 days" vs "30-90d band" — the band is what surfaces in rollup. Pick bins (<30 / 30-90 / 90-180 / >180) at the start; never re-bin retroactively.
- **Manager bias**: managers writing post-mortems on their own deals soften the criticism. Use peer review (different AE/manager) for losses > $100K.
- **Privacy on buyer interviews**: ask permission to record; offer anonymized summary if they're hesitant. Some buyers won't agree if their name will be quoted in your CRM.
- **Quarterly rollup needs >= 20 closed deals to be statistically useful.** Below that, you're reading patterns into noise.
- **Action items must close the loop.** Each pattern (Recipe 10) should produce a specific change: battlecard update, pricing experiment, ICP refinement. Without the loop, post-mortems become busywork.

## Sources

- Gong win/loss research: https://www.gong.io/blog/win-loss-analysis/
- "How to run a buyer interview" — Cluedin: https://www.cluedin.com/customer-research
- Win/Loss program implementation (Klue): https://klue.com/blog/win-loss-program
- Force Management lost-reason taxonomy: https://www.forcemanagement.com/blog/lost-reason
- Sales post-mortem 2026 playbook: https://www.gong.io/blog/sales-post-mortem/
- Notion DB schema for win/loss (community template): https://www.notion.so/templates/win-loss-database
