<!--
Source: https://www.gong.io/blog/deal-coaching/ + MEDDPICC framework
Per-opportunity deal coaching + next-best-action (June 2026 SOTA).
-->
# Deal Coaching + Next-Best-Action — SKILL

For each open deal, compute 7 signals and surface the **single highest-value next action** with literal execution copy. Not "here's what you could do" — one explicit action with a deadline, a recipient, and an escalation trigger if the action fails. Drives weekly 1:1 coaching, pipeline reviews, and self-service AE prompts.

## When to use

- **Weekly 1:1 coaching prep** — generate an NBA report per AE's open pipeline.
- **Pipeline review** — flag slip-risk deals with the next move pre-written.
- **Mid-cycle deal stuck** — diagnose stall + produce the right unstick play.
- **Negotiation prep** — BATNA + ZOPA + concession ladder pulled from closed-won comps.
- **Trigger phrases**: "what's next on deal X", "why is this stuck", "coach me on this opp", "deal review", "stalled deal", "negotiation prep for X", "best next move".

Do NOT use this skill for: **broad pipeline review without per-deal depth** (use `pipeline-hygiene-stage-criteria`); **post-close analysis** (use `win-loss-analysis-structured`); **fresh discovery** (use SPIN from `bant-spin-challenger-frameworks`).

## Setup

```bash
export MATON_API_KEY="<key>"   # CRM access via api-gateway
# Optional
export GONG_ACCESS_KEY="<key>" # for sentiment + activity signal
```

No skill-specific external API keys beyond CRM + Gong (covered by `hubspot-sales-mcp` and `gong-chorus-call-intelligence`).

## Common recipes

### Recipe 1: The 7 NBA signals (canonical list)

```yaml
1. meddic_completeness:
    rule: meddic_score < 14 (out of 18)
    nba: "Close criteria gaps — ask champion the discovery question for the lowest-scoring field"
2. age_in_stage:
    rule: days_in_current_stage > 1.5 × median_days_for_stage
    nba: "Diagnose stall — call champion this week to confirm process is still moving"
3. multi_thread_depth:
    rule: stakeholders_engaged < 3 for deal > $50K, OR < 4 for deal > $150K
    nba: "Multi-thread to EB — request champion intro + send content gift to silent stakeholder"
4. last_meaningful_activity:
    rule: prospect_initiated_touch > 14 days ago
    nba: "Reactivation outreach with new angle — case study + value-anchored question"
5. sentiment_trajectory:
    rule: gong_sentiment over 3 most recent calls = declining
    nba: "Direct conversation about deal status — ask explicitly: 'are we still on track?'"
6. champion_silence:
    rule: champion non-responsive > 7 days (across email + LinkedIn + phone)
    nba: "Send ammunition (1-pager / ROI calc / case study) + ‘checking in — does this help you internally?’"
7. decision_date_drift:
    rule: close_date pushed 2+ times
    nba: "Mutual action plan with signed close-date commitment, or qualify out"
```

### Recipe 2: Compute all 7 signals (deal pull → score)

```python
import requests, os, datetime
from statistics import median

def compute_signals(deal, history, gong_calls):
    today = datetime.date.today()
    signals = []

    # 1. MEDDIC
    if int(deal.get("meddic_score", 0) or 0) < 14:
        signals.append(("meddic_completeness", 18 - int(deal.get("meddic_score", 0) or 0)))

    # 2. Age-in-stage
    days_in_stage = (today - datetime.date.fromisoformat(deal["hs_entered_current_stage_date"])).days
    stage_median = STAGE_MEDIAN.get(deal["dealstage"], 30)
    if days_in_stage > 1.5 * stage_median:
        signals.append(("age_in_stage", days_in_stage))

    # 3. Multi-thread
    n_stakeholders = len(deal.get("associated_contacts", []))
    if deal.get("amount", 0) > 150_000 and n_stakeholders < 4:
        signals.append(("multi_thread_depth", n_stakeholders))
    elif deal.get("amount", 0) > 50_000 and n_stakeholders < 3:
        signals.append(("multi_thread_depth", n_stakeholders))

    # 4. Last meaningful activity
    last_inbound = deal.get("hs_last_inbound_activity_date")
    if last_inbound:
        days_since = (today - datetime.date.fromisoformat(last_inbound)).days
        if days_since > 14:
            signals.append(("last_meaningful_activity", days_since))

    # 5. Sentiment trajectory
    if gong_calls and len(gong_calls) >= 3:
        sentiments = [c["sentiment_score"] for c in gong_calls[-3:]]
        if sentiments[0] > sentiments[1] > sentiments[2]:
            signals.append(("sentiment_trajectory", sentiments[-1] - sentiments[0]))

    # 6. Champion silence
    champion_email = deal.get("meddic_champion_email")
    if champion_email:
        last_reply = deal.get(f"contact_{champion_email}_last_reply_date")
        if last_reply:
            days_silent = (today - datetime.date.fromisoformat(last_reply)).days
            if days_silent > 7:
                signals.append(("champion_silence", days_silent))

    # 7. Close-date drift
    if deal.get("close_date_pushed_count", 0) >= 2:
        signals.append(("decision_date_drift", deal["close_date_pushed_count"]))

    return signals
```

### Recipe 3: Pick the SINGLE highest-value NBA

```python
PRIORITY_RANKING = [
    "champion_silence",       # highest — fix relationship before anything else
    "sentiment_trajectory",   # ditto, slightly lower
    "meddic_completeness",    # criteria gaps fixed = forecast confidence
    "multi_thread_depth",     # critical for big deals
    "decision_date_drift",    # need MAP discipline
    "age_in_stage",           # the symptom; usually one of above is the cause
    "last_meaningful_activity",
]

def pick_nba(signals):
    """Return the single highest-priority signal."""
    signals_dict = {name: severity for name, severity in signals}
    for sig in PRIORITY_RANKING:
        if sig in signals_dict:
            return sig
    return None
```

ONE action per deal per week. Multiple NBAs = no NBA — AE picks the easy one and ignores the hard one.

### Recipe 4: Generate literal copy per NBA

Per-signal template (channel + body / ask + deadline + escalation):

```yaml
champion_silence:
  channel: email + LinkedIn
  subject: "Quick one — {first_name}"
  body: |
    Hi {first_name}, knowing it's been a busy week. Sending {asset} that's helped teams in your spot.
    Two things to flag inside: {point_1}; {point_2}. Happy to tailor for {eb_name} if useful internally.
    If now's not the right time, totally understood — want to be useful, not noisy.
  deadline_days: 2
  escalation: "no reply by Friday → manager + AE joint call to discuss deal status"

meddic_completeness:
  channel: next call
  ask: "Confirm {weakest_field_name}. Question to ask champion: {weakest_field_question}."
  deadline_days: 7
  escalation: "unanswered after 2 attempts → nurture stage"

multi_thread_depth:
  channel: email to champion + LinkedIn to silent stakeholders
  body: |
    Hi {champion_first_name}, for {eb_name} to feel confident I'd like to bring them in — even 10 min.
    Open to introducing me, or want me to draft a 1-pager for you to forward?
  deadline_days: 5
  escalation: "EB unengaged by Day 21 → qualify-out risk increases"

sentiment_trajectory:
  channel: phone (not email)
  ask: |
    15 min with champion. Open: "Want to make sure we're still aligned. Honest read on where this stands?"
    Listen for hesitation; surface real concern.
  deadline_days: 3
  escalation: "can't get on phone → manager joint-pitch"

decision_date_drift:
  channel: in-person / video meeting
  ask: |
    Bring draft MAP with proposed dates. Open: "Here's what I've heard about how this closes. Help me sharpen it."
    Get champion to commit dates in writing.
  deadline_days: 7
  escalation: "MAP refused → no-decision; move to nurture"

age_in_stage:
  channel: call champion
  ask: "Open: 'We've been at {stage} for {days} days — what's the actual blocker?'"
  deadline_days: 5
  escalation: "unblocked-but-not-progressing → downgrade commit → best-case"

last_meaningful_activity:
  channel: email with new angle
  body: "{first_name} — haven't bothered you in weeks. Saw {trigger_event}, thought of you. {one_sentence_reason}. Worth 15 min?"
  deadline_days: 3
  escalation: "silent 2+ more weeks → mark dormant"
```

### Recipe 5: End-to-end NBA report for one AE

```python
# Compose Recipes 2, 3, 4 against all open deals owned by one AE
import json, requests, os

def ae_nba_report(ae_user_id):
    deals = requests.post(
        "https://gateway.maton.ai/hubspot/crm/v3/objects/deals/search",
        headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"},
        json={"filterGroups":[{"filters":[
            {"propertyName":"hubspot_owner_id","operator":"EQ","value":ae_user_id},
            {"propertyName":"dealstage","operator":"NOT_IN","values":["closedwon","closedlost"]}
        ]}],"properties":["dealname","amount","dealstage","closedate","meddic_score","close_date_pushed_count"],"limit":100},
    ).json()["results"]

    report = []
    for deal in deals:
        history = deal_history(deal["id"])
        gong_calls = gong_calls_for_deal(deal["id"])
        signals = compute_signals(deal, history, gong_calls)
        nba_key = pick_nba(signals)
        if nba_key:
            template = NBA_TEMPLATES[nba_key]
            report.append({
                "deal": deal["properties"]["dealname"],
                "amount": deal["properties"]["amount"],
                "nba": nba_key,
                "action": template,
                "signals_count": len(signals),
            })
    return sorted(report, key=lambda x: -float(x["amount"] or 0))
```

### Recipe 6: Negotiation prep (BATNA + ZOPA + concession ladder)

```python
# Pull closed-won comparables, compute price corridor + concession ladder
def negotiation_brief(deal):
    comps = closed_won_comparables(deal, lookback_quarters=4)  # same vertical + size
    prices = [c["amount"] / c["seats"] for c in comps]
    p25, p50, p75 = quantile(prices, 0.25), quantile(prices, 0.50), quantile(prices, 0.75)

    return {
        "anchor_price": p75,
        "target_price": p50,
        "floor_price": p25,
        "deal_specific_floor": max(p25, deal["minimum_acceptable"]),
        "concession_ladder": [
            {"ask":"10% discount","give":"multi-year (3yr) commit","get":"cash up-front"},
            {"ask":"15% discount","give":"reference call","get":"case study rights"},
            {"ask":"20% discount","give":"logo + co-marketing","get":"quarterly exec QBR"},
            {"ask":">20% discount","escalate":"finance-controller agent"},
        ],
        "batna": "Walk away — pipeline coverage shows replacement opportunity in 30 days",
        "zopa_upper": p75 * 1.1,    # what they'll pay if held firm
        "zopa_lower": p25 * 0.95,   # below this we'd rather lose
    }
```

### Recipe 7: Stalled-deal triage flowchart

```yaml
# Run this when a deal is in stage > 1.5x median
diagnose:
  q1: "Is champion still responsive?"
    yes:
      q2: "Is EB engaged?"
        yes:
          q3: "Is there a competing priority?"
            yes: "Wait + agree on revisit date; move to nurture stage"
            no: "Push on close — MAP refresh with dates"
        no: "Multi-thread NBA — content gift to EB via champion"
    no:
      q4: "Did champion go silent or did they leave?"
        silent: "Champion-silence NBA (Recipe 4)"
        left: "Champion-mover signal — restart at new co + find new champion at current co"
```

### Recipe 8: Slip-risk score (composite NBA priority)

```python
def slip_risk_score(deal, signals):
    """0-100, higher = more likely to slip past close date."""
    base = 0
    for name, severity in signals:
        base += {
            "champion_silence": 25,
            "sentiment_trajectory": 25,
            "meddic_completeness": 20,
            "multi_thread_depth": 15,
            "decision_date_drift": 25,
            "age_in_stage": 10,
            "last_meaningful_activity": 10,
        }.get(name, 0)

    # Cap and add deal-size weighting
    return min(base, 100)
```

### Recipe 9: Render NBA report to Notion + Slack

After `ae_nba_report()`, fold each item into Markdown: `### {deal} (${amount})\n**NBA**: {nba}\n**Action**: {ask or body[:200]}\n**Deadline**: {days}d\n**Escalation**: {escalation}`. Write via `notion-mcp`; Slack DM AE with top-3.

### Recipe 10: Weekly cadence

```yaml
monday_8am: Generate per-AE NBA report
monday_9am 1:1: Manager reviews top-3 NBAs with each AE
midweek: AE executes
friday_5pm: Friday forecast roll-up references NBA-completion status
```

## Examples

### Example 1: Monday 1:1 prep for one AE with 12 open deals

**Goal:** Manager has a 15-min coaching agenda for one AE.

**Steps:** Recipe 5 against AE's open pipeline → 12 deals scored, 7 with NBA fired → rank by deal size + Recipe 8 slip-risk → top-3: $150K (champion_silence), $80K (meddic_completeness), $60K (multi_thread_depth) → Recipe 9 renders to Notion 1:1 doc → manager reviews; AE commits to all three by Friday.

**Result:** 1:1 focused on outcomes (this email, this call) not "let's review the pipeline".

### Example 2: Negotiation prep before a pricing call

**Goal:** AE has pricing call tomorrow on $120K deal; need brief.

**Steps:** Recipe 6 pulls closed-won comps (same size + vertical) → anchor p75, target p50, floor p25 → concession ladder rendered as 1-page doc → BATNA assessed → brief delivered to AE 12 hours pre-call via `notion-mcp` + Slack.

**Result:** AE walks in anchored on data; defends price; doesn't capitulate.

## Edge cases / gotchas

- **One NBA per deal per week — strictly.** Multiple NBAs = no NBA; AEs cherry-pick the easy one.
- **Signal priority order matters more than weights.** `champion_silence` beats `age_in_stage` because age-in-stage usually *is* champion-silence wearing a costume.
- **NBA copy is literal, not "you should consider".** Provide the exact email body / call open. Friction is the enemy of execution.
- **Deadline + escalation are non-negotiable fields.** No deadline = the NBA dies; no escalation = AE has no off-ramp when stuck.
- **MEDDIC < 14 with "Commit" forecast = self-deception.** Most common manager-coaching call: re-score honestly first, then re-bucket.
- **Sentiment from Gong is noisy on short calls** (< 15 min). Require >= 20 min of call duration before trusting sentiment.
- **Champion silence on email ≠ silence everywhere.** Check LinkedIn DMs + phone before declaring silent.
- **Decision-date drift twice** = the original date was wishful. Don't keep pushing — call it: MAP-or-nurture.
- **NBA report fatigue**: cap at top-5 per AE; rest go to a "watch" list, not the prioritized doc.
- **Quarterly re-calibration**: if "champion silence" NBAs led to recovery in only 20% of cases, the play needs work — don't keep recommending broken plays.
- **"Best NBA" is sometimes "qualify-out".** Mark a deal lost cleanly so AE focuses on real pipeline.

## Sources

- Gong deal coaching research: https://www.gong.io/blog/deal-coaching/
- Gong "Why deals slip" data: https://www.gong.io/labs/why-deals-slip/
- Multi-threading deals (Gong): https://www.gong.io/blog/multi-threading/
- Mutual Action Plan template (Force Management): https://www.forcemanagement.com/map
- Negotiation playbook (Chris Voss "Never Split the Difference"): https://www.blackswanltd.com/the-edge/
- 2026 AI-assisted deal coaching landscape: https://www.gong.io/blog/ai-deal-coach/
- MEDDIC + NBA pattern: https://www.meddicc.com/blog/meddic-deal-coaching
