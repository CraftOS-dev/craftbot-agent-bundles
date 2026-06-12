<!--
Source: https://www.gong.io/blog/sales-battlecards/ + internal templates
Sales enablement: battlecards, ROI calculators, case studies (June 2026 SOTA).
-->
# Sales Enablement — Battlecards + ROI Calculators + Case Studies — SKILL

Build and maintain the materials AEs actually use mid-deal: competitor battlecards (positioning + traps + proof), ROI calculators (input → output economic model), case studies (customer story with diagnosis + outcome + metric), and demo-prep packages. Battlecards in `pptx`/Notion; ROI in `xlsx` / Google Sheets formula model; case studies in `docx`/`pdf`.

## When to use

- **Buyer named a competitor** → pull or update battlecard.
- **Pricing pushback** → output an ROI calculator with their inputs.
- **Demo prep** → assemble feature→pain mapping + objection rehearsal.
- **Case study request** — buyer wants proof from a similar customer.
- **Quarterly enablement refresh** — battlecards from objection-mining (Gong); pricing comps update.
- **Trigger phrases**: "battlecard for competitor X", "ROI calc for this deal", "case study like Y", "demo prep for X", "competitive intel", "proof points for vertical Z".

Do NOT use this skill for: **brand-new content authoring** (use `marketing-agent` for content production); **internal training programs** (Mindtickle / Highspot — out of scope); **sales coaching** (use `gong-chorus-call-intelligence` + `deal-coaching-next-best-action`).

## Setup

```bash
export MATON_API_KEY="<key>"     # for CRM closed-won pulls
export GONG_ACCESS_KEY="<key>"   # for objection mining
export NOTION_TOKEN="<key>"      # battlecard + case-study library
export GOOGLE_SHEETS_TOKEN="<token>"   # ROI calc rendering
# pptx, xlsx, docx, pdf default skills handle file generation
```

One-time: build a Notion DB schema for battlecards and one for case studies. ROI calc template as a Google Sheet (one tab per pricing model).

## Common recipes

### Recipe 1: Battlecard template (per role.md)

```markdown
# Battlecard — [Us] vs [Competitor]

## Positioning (30 sec)
- Their pitch: ___
- Our counter-pitch: ___
- Unique to us: ___
- Unique to them: ___

## Where they win
- ___
- ___

## Where we win
- ___
- ___

## Traps to set (questions to ask that surface their weakness)
1. "Ask them about [feature/capability they don't have well]."
2. "Ask them about [pricing model gap]."
3. "Ask them about [support / migration concern]."

## Talk tracks
- "When prospects compare us to [X], here's what we say..."
- "If they say 'we already use X' — respond: ___"

## Proof points
- Customer case: ___ (link to case study)
- Independent analyst: ___ (link to Forrester/Gartner)
- Metric: ___ (number + source)

## Pricing intel
- Their list: ___
- Their typical discount: ___
- Their contract terms: ___

## Owner: [Product Marketing] | Last updated: [Date]
```

### Recipe 2: Battlecard data sourcing (where each section comes from)

```yaml
positioning:
  source:
    - Their public website + pricing page (via playwright-mcp)
    - Recent G2 / Capterra reviews comparing both products
    - Crunchbase / press releases for funding / leadership
where_they_win + where_we_win:
  source:
    - Gong call transcripts where competitor was named (gong-chorus-call-intelligence Recipe 11)
    - Win/loss post-mortems where this competitor appeared (win-loss-analysis-structured Recipe 9)
    - Lost-deal interviews
traps_to_set:
  source:
    - Their docs / changelog for gaps
    - User complaints on G2 / Reddit / their public Slack
    - Their pricing page for hidden costs
talk_tracks:
  source:
    - AE-shared playbooks (Notion library)
    - Manager-approved scripts
proof_points:
  source:
    - Closed-won deals in same vertical (CRM query)
    - Customer references list (Notion DB)
pricing_intel:
  source:
    - Win/loss interviews (what they offered)
    - Public pricing pages (often partial)
    - LinkedIn discussions / Reddit threads
```

### Recipe 3: Generate battlecard from objection mining (Gong + CRM)

```python
import requests, os
COMPETITOR = "VendorX"

# Step 1: pull last 90 days of calls where competitor mentioned (gong recipe 11)
calls = pull_calls_with_competitor(COMPETITOR, days=90)

# Step 2: pull won + lost deals where competitor was in MEDDPICC competition field
deals = query_deals_competition(COMPETITOR)
wins = [d for d in deals if d["outcome"] == "won"]
losses = [d for d in deals if d["outcome"] == "lost"]

# Step 3: extract patterns
where_we_win = top_reasons([d["won_reason"] for d in wins])
where_they_win = top_reasons([d["lost_reason"] for d in losses])

# Step 4: LLM-summarize objections from call snippets into talk tracks
talk_tracks = llm_summarize_objections(calls, COMPETITOR)

# Step 5: render battlecard markdown (Recipe 1 template)
md = render_battlecard(COMPETITOR, where_we_win, where_they_win, talk_tracks)

# Step 6: push to Notion battlecard DB
notion_upsert_battlecard(COMPETITOR, md, last_updated=today)
```

### Recipe 4: ROI calculator inputs + outputs (canonical structure)

```yaml
inputs:
  - current_spend_annual: "$ on existing solution / process"
  - users_or_seats: integer
  - hours_per_user_per_week_on_current: float
  - loaded_labor_cost_per_hour: "$ (default $75)"
  - estimated_efficiency_gain_pct: "% (default 20-30%, conservative)"
  - one_time_switching_cost: "$ (default $0)"
  - our_annual_price: "$ from proposal"
  - contract_length_years: integer (default 1)

outputs:
  annual_labor_savings: "users × hours_per_week × 52 × $/hr × efficiency_pct"
  software_cost_delta_annual: "our_annual_price - current_spend_annual"
  net_annual_savings: "annual_labor_savings + software_cost_delta_annual - (switching_cost / contract_years)"
  payback_period_months: "switching_cost / (net_annual_savings / 12)"
  three_year_roi_pct: "(3 * net_annual_savings - switching_cost) / switching_cost × 100"

interpretation:
  payback_under_6_months: "great — easy CFO sell"
  payback_6_to_12_months: "good — typical SaaS ROI"
  payback_12_to_24_months: "OK — needs strategic justification"
  payback_over_24_months: "hard sell — re-examine assumptions"
```

### Recipe 5: Render ROI calc to Google Sheets

```python
import gspread
gc = gspread.service_account()
sh = gc.copy("<template-sheet-id>", title=f"ROI — {account_name}")

ws = sh.worksheet("Inputs")
ws.update("B2", [[current_spend], [users], [hours_per_week], [labor_cost], [efficiency_pct], [switching_cost], [our_price], [contract_years]])

# Outputs tab uses Sheets formulas; just share the URL with buyer
print(f"Share with buyer: {sh.url}")
```

The Google Sheet's `Outputs` tab uses live formulas — buyer can edit inputs and see results instantly. More credible than a static PDF.

### Recipe 6: Render ROI calc to xlsx (offline / email-attachable)

```python
import openpyxl
wb = openpyxl.load_workbook("/templates/roi-template.xlsx")
ws_inputs = wb["Inputs"]
ws_inputs["B2"] = current_spend
ws_inputs["B3"] = users
# ... fill remaining inputs

# Outputs tab uses formulas; openpyxl recalculates on open
wb.save(f"/tmp/ROI-{account_name}.xlsx")
```

### Recipe 7: Case study generation (CRM closed-won → docx)

```python
# Pull a closed-won deal + linked calls + buyer interview
# Render to a templated docx
DEAL_ID = "<id>"
deal = get_deal(DEAL_ID)
buyer_interview = get_buyer_interview(DEAL_ID)  # post-close interview, if done
metrics = get_deal_outcome_metrics(DEAL_ID)     # e.g., "reduced CAC 22%"

case_study = render_template("/templates/case-study.docx", {
    "customer_name": deal["company"],
    "industry": deal["industry"],
    "size": deal["employees_at_close"],
    "challenge": deal["meddic_identify_pain"],
    "criteria": deal["meddic_decision_criteria"],
    "implementation_weeks": metrics["implementation_weeks"],
    "outcome_metric_1": metrics["metric_1"],
    "outcome_metric_2": metrics["metric_2"],
    "champion_quote": buyer_interview.get("quote", ""),
    "champion_name": deal["meddic_champion"],
    "champion_title": deal["meddic_champion_title"],
})
# save as /case-studies/{slug}-{date}.docx
```

### Recipe 8: Case study template (skeleton)

```markdown
# Case Study — [Customer]
## Overview — [Industry] · [Size] · Implemented in [N] weeks · Outcome: [headline metric]
## Challenge — pre-state pain + quantified cost of inaction
## Why us — decision criteria + the differentiator that sealed it
## Implementation — week-by-week milestones
## Results — 2-3 baseline→outcome metrics
## Champion quote — verbatim from buyer interview + name + title
## What's next — expansion plan / continued partnership
```

### Recipe 9: Demo prep package (per role.md template)

```markdown
# Demo Prep — [Account] × [Date]
## Discovery recap — pain + stakeholders attending + MEDDIC gaps to close
## Demo storyline (3 acts, 25 min):
  Act 1 (5m): "Here's what we heard you're trying to solve."
  Act 2 (15m): "Here's how we'd solve it — 3 features tied to your pain."
  Act 3 (5m): "Here's how we'd roll this out at [Account] — proposed MAP."
## Feature → pain mapping table (Feature | Pain | Proof point)
## Objection rehearsal (top-5 + responses)
## Battlecard (if competitor named — strength / differentiation / trap)
## Agreed next step
```

Generated by composing data from `account-research-deep` + most-recent Gong discovery transcript.

### Recipe 10: Battlecard freshness check (quarterly)

```python
# Flag stale battlecards
import datetime
def is_stale_battlecard(battlecard, max_age_days=90):
    last_updated = battlecard.get("last_updated")
    if not last_updated: return True
    return (datetime.date.today() - datetime.date.fromisoformat(last_updated)).days > max_age_days

stale = [b for b in all_battlecards() if is_stale_battlecard(b)]
# Slack the product-marketing owner to refresh
```

### Recipe 11: Render battlecard to pptx (for AE quick-reference)

```python
from pptx import Presentation
from pptx.util import Inches, Pt
prs = Presentation("/templates/battlecard.pptx")

slide = prs.slides[0]
slide.shapes.title.text = f"Us vs {competitor}"
# Populate text placeholders by name from battlecard data
populate_placeholder(slide, "positioning_them", battlecard["their_pitch"])
populate_placeholder(slide, "positioning_us", battlecard["our_counter_pitch"])
populate_placeholder(slide, "we_win", "\n".join(f"• {x}" for x in battlecard["where_we_win"]))
populate_placeholder(slide, "they_win", "\n".join(f"• {x}" for x in battlecard["where_they_win"]))
populate_placeholder(slide, "traps", "\n".join(battlecard["traps"]))

prs.save(f"/tmp/battlecard-{competitor}.pptx")
```

### Recipe 12: Quarterly enablement audit (output → action items)

```yaml
audit_quarterly:
  - List all competitors named in last 90 days (from Gong + MEDDPICC field)
  - For each: check battlecard exists + last_updated < 90 days
  - For competitors without battlecard: create stub + assign owner
  - For stale battlecards: trigger refresh task to product marketing
  - List all closed-won deals in last 90 days without a case study (and ACV > $50K)
  - Trigger case-study draft from each (Recipe 7)
  - Check ROI-calc template usage: how many proposals attached a calc? Below 50% = enablement gap
```

## Examples

### Example 1: Buyer named competitor → AE gets fresh battlecard in 5 min

**Goal:** AE on call hears buyer say "we're also looking at VendorX". By end of call, AE has the battlecard.

**Steps:**
1. AE Slack DM: `/battlecard VendorX`.
2. Agent looks up Notion battlecard DB for VendorX.
3. If exists and fresh (< 90 days): return pptx/Notion link in Slack reply.
4. If stale: refresh via Recipe 3 (Gong objection mining + CRM win/loss); update Notion; return link.
5. If missing entirely: stub with positioning placeholders + flag product-marketing.

**Result:** AE never goes into the next call without the latest competitor intel.

### Example 2: Pricing pushback → ROI calc same-day

**Goal:** Buyer said "too expensive" Tuesday; AE wants ROI calc by EOD.

**Steps:** AE provides users + current spend → Recipe 5 copies template Google Sheet, populates inputs, computes annual savings + payback live → share read-only link with buyer + 2-slide summary deck → follow-up email anchors on the math.

**Result:** Buyer engages with the math instead of dismissing it.

### Example 3: Demo prep auto-package

**Goal:** Demo tomorrow with [account]; AE needs prep doc.

**Steps:** `account-research-deep` brief pulled overnight → Recipe 9 renders prep doc combining discovery transcript (Gong) + battlecard + feature→pain mapping + objection rehearsal → auto-DM AE morning-of with Notion link.

**Result:** AE walks into the demo prepared, not improvising.

## Edge cases / gotchas

- **Battlecards rot fast.** A competitor's new feature 6 weeks ago can flip "where they lose" → "where they win". Quarterly refresh isn't enough for fast-moving categories.
- **AE-generated battlecards drift to AE-favorable framing.** Product marketing owns the canonical version; AEs annotate but don't edit the master.
- **ROI calc inputs are buyer-controlled** when shared as a live Sheet. Anchor conservative defaults in the template with notes on why.
- **ROI "labor savings" overstated** — buyers rarely fire FTEs whose time you saved. Present savings in *capacity terms* ("frees 12 hrs/wk for higher-value work") not pure dollars.
- **Case study consent**: buyer must approve metrics + their name + logo. Default to anonymized; named only with written consent.
- **Cross-customer proof points need data**: "Customer X saved 22%" needs the underlying calc + buyer permission to cite. Vague claims destroy credibility.
- **Battlecard DB schema discipline**: free-form rich-text doesn't roll up. Structured fields (their_pitch / our_counter / where_we_win / etc.) enable cross-competitor comparison.
- **Demo prep auto-generation can mis-quote** call transcripts (LLM hallucination). Always include link to original transcript so AE can verify.
- **Stale enablement = lost deals.** If the same objection keeps surfacing in lost deals and the battlecard didn't help, the battlecard is wrong.

## Sources

- Gong sales battlecards guide: https://www.gong.io/blog/sales-battlecards/
- Klue battlecard examples + management: https://klue.com/blog/sales-battlecards
- ROI calculator framework (PriceIntelligently): https://www.priceintelligently.com/blog/roi-calculator
- Case study structure (Animalz): https://www.animalz.co/blog/case-studies/
- "Build a battlecard from win/loss" — Klue: https://klue.com/blog/win-loss-battlecards
- Demo prep template (Sales Hacker): https://www.saleshacker.com/sales-demo-template/
- 2026 sales enablement landscape: https://www.gong.io/blog/sales-enablement-stack/
