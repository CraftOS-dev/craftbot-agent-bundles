<!--
Source: https://huthwaiteinternational.com/insights/spin-selling + https://www.challengerinc.com/the-challenger-sale/
BANT + SPIN + Challenger + GPCT — alt qualification frameworks (June 2026).
-->
# BANT + SPIN + Challenger Qualification Frameworks — SKILL

The non-MEDDIC qualification frameworks. **BANT** for transactional / SMB / inbound — faster than MEDDIC. **SPIN** for discovery-call structure — works alongside any other framework. **Challenger** for commercial-conversation framing when buyer is shopping competitors. **GPCT** (HubSpot's variant) for inbound. Pick ONE per deal; don't mix-and-match incoherently.

## When to use

- **Transactional / SMB / inbound MQL** with single decision-maker → **BANT** (4 fields).
- **Any discovery call** (regardless of larger framework) → **SPIN** as the question-structure layer.
- **Commercial conversation stalled** or buyer shopping multiple vendors → **Challenger** (teach / tailor / take control).
- **HubSpot-native inbound** → **GPCT** (Goals / Plans / Challenges / Timeline) — easier fit with HubSpot's lifecycle stages.
- **Trigger phrases**: "BANT this lead", "give me SPIN questions for X", "build a discovery script", "Challenger approach for this deal", "GPCT for inbound", "qualify quickly".

Do NOT use this skill for: **complex B2B > $25K with multi-stakeholder** (use `meddic-meddpicc-qualification` — MEDDIC is the right tool); **non-sales discovery** (e.g., customer-success QBRs — different question patterns).

## Setup

```bash
# CRM custom fields per framework — one-time setup. Example: HubSpot for BANT
export MATON_API_KEY="<key>"

for field in bant_budget bant_authority bant_need bant_timeline bant_score; do
  curl -X POST "https://gateway.maton.ai/hubspot/crm/v3/properties/deals" \
    -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
    -d "{\"name\":\"$field\",\"label\":\"$field\",\"type\":\"string\",\"fieldType\":\"textarea\",\"groupName\":\"dealinformation\"}"
done

# For GPCT (HubSpot-native) — same pattern with gpct_goals, gpct_plans, gpct_challenges, gpct_timeline
```

No external API keys — frameworks live in CRM fields + the agent's reasoning.

## Common recipes

### Recipe 1: BANT scoring rubric

```
B = Budget: confirmed $ amount + fiscal-year alignment
A = Authority: named decision-maker has agreed to evaluate
N = Need: specific pain articulated by prospect (not vendor-suggested)
T = Timeline: trigger event + target purchase date

Each field: yes / partial / no
- All 4 = qualified → progress to demo / proposal
- 3 = qualified-with-risk → progress + flag missing field
- 2 or fewer = nurture, not active opp
```

### Recipe 2: BANT discovery questions

```yaml
budget:
  - "Has budget been allocated for this, or is this an exploratory conversation?"
  - "What range have you scoped — five figures, six, or seven?"
  - "What's the budget cycle here — annual / quarterly / project-based?"
authority:
  - "Who else needs to be involved in a decision like this?"
  - "If we agree this is the right path, what's the approval process?"
need:
  - "What's prompting this conversation now vs 6 months ago?"
  - "What happens if you don't solve this in the next 6 months?"
timeline:
  - "When are you hoping to have this implemented?"
  - "What's the trigger date — fiscal year, project deadline, something else?"
```

### Recipe 3: SPIN question bank (discovery-call structure)

5-7 questions per discovery call, mixing four types:

```yaml
situation (1-2 Qs, establish baseline):
  - "Walk me through your current [process / setup / team structure]."
  - "How are you handling [problem area] today?"
  - "What does your stack look like for [function]?"

problem (2-3 Qs, surface pain):
  - "Where does that process break down?"
  - "What costs you the most time / money / customer trust?"
  - "What's not working about [current approach]?"

implication (2-3 Qs, magnify pain):
  - "If that persists for another 6 months, what's the downstream impact?"
  - "Who else feels that pain — sales, marketing, product?"
  - "What does this cost you in [missed revenue / churn / team morale]?"

need-payoff (1-2 Qs, buyer articulates value):
  - "If we solved [specific pain], what would that be worth to your team?"
  - "How would your day look different if [problem] went away?"
  - "What would success look like in 12 months?"
```

**Anti-pattern**: asking all Situation questions — buyers feel interrogated, not understood. Aim for 1-2 S, 2-3 P, 2-3 I, 1-2 NP.

### Recipe 4: SPIN call structure (30-min discovery)

```
0-3 min: rapport + agenda confirm
3-7 min: 1-2 Situation Qs (warm up)
7-15 min: 2-3 Problem Qs (find pain)
15-22 min: 2-3 Implication Qs (magnify pain)
22-26 min: 1-2 Need-payoff Qs (buyer says the value)
26-30 min: hypothesis + agreed next step
```

The buyer should articulate value (NP answer) before you ever pitch — Rackham's foundational insight.

### Recipe 5: Challenger commercial conversation (teach / tailor / take control)

```yaml
teach:
  goal: bring an insight the buyer didn't have
  not: "our features are great"
  is: "here's a counter-intuitive truth about your industry / role"
  example: "Most heads of growth measure CAC, but the metric that actually predicts churn at your stage is..."

tailor:
  goal: make the teach specific to their company / team / industry / stage
  not: generic industry trends
  is: "for a Series B SaaS at your headcount, this specifically means..."

take_control:
  goal: hold the line on price, scope, timeline
  not: "let me check with my manager"
  is: "based on what you've shared, here's what I'd recommend — and here's why discounting hurts your outcome"
```

Use when: buyer stated wrong criteria, commercial conversation stalled, or buyer is shopping multiple vendors.

### Recipe 6: Challenger conversation flow

```
1. "The Warmer": establish credibility (1 min — case study, data point)
2. "The Reframe": deliver the teach (5 min — insight that flips their assumption)
3. "Rational Drowning": data showing the cost of status quo (3 min)
4. "Emotional Impact": who specifically pays the cost (3 min)
5. "A New Way": the alternative path (5 min)
6. "Your Solution": positioned as the proof of the new way (5 min)
```

### Recipe 7: GPCT (HubSpot's inbound qualification)

```
G = Goals: what is the company / team trying to achieve in 12 months?
P = Plans: what's their current plan to hit those goals?
C = Challenges: what's getting in the way?
T = Timeline: when do they need a solution in place?

Plus (BA/C&I):
BA = Budget + Authority
C&I = Consequences + Implications (i.e., SPIN's I + NP)
```

GPCT inverts the order from BANT — goals first (forward-looking) before budget (backward-looking). Fits inbound MQLs who arrive curious, not ready-to-buy.

### Recipe 8: GPCT discovery questions

```yaml
goals:
  - "What's the biggest goal your team is working toward this year?"
  - "How is success measured for you personally?"
plans:
  - "What's the current plan to hit that?"
  - "What have you tried so far?"
challenges:
  - "Where is that plan getting stuck?"
  - "What's the biggest obstacle right now?"
timeline:
  - "When do you need to have something in place to hit your timeline?"
budget_authority:
  - "How is budget allocated for initiatives like this?"
  - "Who else gets involved in a decision like this?"
consequences_implications:
  - "What happens if this goal isn't hit?"
  - "What's the cost of staying with the current approach?"
```

### Recipe 9: Choose the right framework (decision tree)

```python
def pick_framework(deal):
    acv = deal.get("amount", 0)
    stakeholders = deal.get("num_stakeholders", 1)
    source = deal.get("lead_source", "")

    if acv >= 100_000: return "meddpicc"  # see meddic-meddpicc-qualification skill
    if acv >= 25_000 and stakeholders >= 2: return "meddic"
    if source in ("inbound", "freemium_signup", "webinar"): return "gpct"
    if deal.get("competitor_named") and deal.get("stalled_at_proposal"): return "challenger"
    # All discovery calls use SPIN as the question-structure layer regardless
    return "bant"
```

### Recipe 10: BANT → MEDDIC upgrade trigger

If a deal starts as BANT-qualified but expands in scope:

```python
# Triggers to upgrade BANT → MEDDIC
UPGRADE_TRIGGERS = [
    lambda d: d["amount"] > 25_000,
    lambda d: d.get("num_stakeholders", 1) >= 3,
    lambda d: d.get("close_date_pushed_count", 0) >= 1,  # cycle elongating
    lambda d: "security review" in d.get("notes", "").lower(),
    lambda d: "procurement" in d.get("notes", "").lower(),
]

if any(t(deal) for t in UPGRADE_TRIGGERS):
    # Upgrade framework; populate MEDDIC fields from BANT + transcript
    pass
```

### Recipe 11: GPCT → MEDDIC handoff (inbound → AE)

When a GPCT-qualified inbound lead becomes a real opp:

```
GPCT.Goals       → MEDDIC.Metrics (quantify the goal)
GPCT.Plans       → MEDDIC.Decision criteria (what they value)
GPCT.Challenges  → MEDDIC.Identify pain
GPCT.Timeline    → MEDDIC.Decision process (when + how)
GPCT.BA          → MEDDIC.Economic buyer (+ Authority)
GPCT.C&I         → MEDDIC.Identify pain (deeper)
```

Champion is the one field GPCT doesn't directly cover — the AE must explicitly identify a champion in the post-handoff discovery.

### Recipe 12: Field-fill from Gong transcript (BANT)

```python
# Same pattern as MEDDIC fill; different prompt
PROMPT = """From this call transcript, extract BANT fields. Return JSON with:
- budget: dollar range stated by prospect, or null
- budget_confidence: 0 (none) / 1 (hinted) / 2 (stated) / 3 (confirmed allocated)
- authority: name + title of decision-maker, or null
- authority_confidence: 0-3
- need: specific pain articulated by prospect (verbatim if possible)
- need_confidence: 0-3
- timeline: target purchase date or trigger event
- timeline_confidence: 0-3
"""
```

Pipe through the same flow as `gong-chorus-call-intelligence` recipe 10.

## Examples

### Example 1: Inbound MQL → GPCT-qualified → AE handoff

**Goal:** Inbound lead from a webinar signup → SDR runs GPCT discovery → hands off to AE.

**Steps:**
1. MQL enters HubSpot; SDR books discovery call via `calendly-api`.
2. SDR runs GPCT discovery (Recipe 8). Captures Goals/Plans/Challenges/Timeline + BA + C&I.
3. At handoff: if Goals + Challenges + Timeline + BA all answered, route to AE; otherwise nurture.
4. SDR populates `gpct_*` fields on contact (or new deal). Recipe 11 maps to MEDDIC fields the AE will own.
5. AE accepts within 4 hr (per role.md SLA) or returns with reason.

**Result:** Inbound funnel measured + handed off cleanly; AE gets a deal with MEDDIC pre-filled to score-1/2.

### Example 2: SPIN-structured discovery for a mid-market opp

**Goal:** 30-min discovery call with a VP Sales at a 200-person SaaS. Output: MEDDIC scored to >= 12/18.

**Steps:**
1. Pre-call: `account-research-deep` to surface triggers + tech stack.
2. Pre-call: build 5-7 SPIN questions (Recipe 3), weighted 1 S, 3 P, 2 I, 1 NP.
3. Conduct call per Recipe 4 structure.
4. Recipe 12 + `gong-chorus-call-intelligence` recipe 10 extract MEDDIC + BANT from transcript.
5. PATCH deal in CRM. Identify next gap via MEDDIC NBA recipe.

**Result:** Discovery call yields a scored opp + a clear next-step, all in 60 min (30 call + 30 follow-up).

### Example 3: Challenger pivot when buyer is shopping

**Goal:** Deal stalled in proposal stage; buyer comparing 3 vendors. Re-engage with Challenger.

**Steps:**
1. Diagnose: pull Gong calls for buyer's stated criteria. Are those criteria correlated with their *actual* pain? If not, criteria are misframed.
2. Build a 1-slide Reframe: counter-intuitive insight (Recipe 5/6).
3. Book a 30-min "alignment" call with champion + EB.
4. Run Recipe 6 flow: warmer → reframe → rational drowning → emotional impact → new way → your solution.
5. End with a recommended path + close date. Don't capitulate on price unless buyer reciprocates.

**Result:** Re-anchored conversation on the *right* criteria; price defended; close date confirmed or deal lost cleanly.

## Edge cases / gotchas

- **BANT is shallow on purpose** — don't try to make it MEDDIC. If you find yourself adding fields, switch to MEDDIC.
- **"Budget" is the most-faked BANT field.** Buyers say "yes we have budget" to keep you on the call. Treat anything without a $-range as score-1 hypothesis.
- **SPIN's "Implication" is the hardest** to actually ask — feels presumptuous. Practice the framing: "if X persisted, what's the downstream impact?" not "you're going to lose money if you don't fix this".
- **Challenger ≠ "be aggressive".** Take Control means holding the line on price + scope, not being rude. Buyers respect AEs who don't capitulate; they don't respect ones who lecture.
- **GPCT requires a Goals-articulate buyer.** Inbound MQLs from low-intent channels (popups, ebook downloads) often can't articulate goals — fall back to BANT or qualify them out.
- **Mixing frameworks mid-deal confuses the team.** Pick one at deal-creation and stick with it; upgrade BANT→MEDDIC explicitly (Recipe 10), don't drift.
- **"Need" without quantification = nurture, not qualified.** "We want to improve outbound" is curious; "We're losing $1.2M/yr because reply rate is 1.5%" is need.
- **Timeline drift kills BANT.** If the buyer pushes timeline twice, the T was never real — re-qualify or move to nurture.
- **Challenger assumes credibility.** Don't deliver a Reframe to a buyer who doesn't trust you yet (i.e., first call). Use after 1-2 prior touches.
- **SPIN works best in 30-45 min discovery calls.** In 15-min calls there isn't time for the full I + NP arc — compress to 1 P + 1 I + agreed next step.
- **GPCT's BA + C&I tags-on** are easy to skip; without them you've got a curious lead, not a qualified opp.

## Sources

- SPIN Selling — Neil Rackham (Huthwaite): https://huthwaiteinternational.com/insights/spin-selling
- The Challenger Sale — Dixon + Adamson (Gartner/CEB): https://www.challengerinc.com/the-challenger-sale/
- BANT framework primer (HubSpot): https://blog.hubspot.com/sales/bant
- GPCT (HubSpot variant): https://blog.hubspot.com/sales/gpct-sales-process
- "When BANT fails — MEDDIC vs BANT" (2024): https://www.salesforce.com/blog/bant-vs-meddic/
- 2026 sales qualification framework comparison: https://www.gong.io/blog/sales-qualification-frameworks/
