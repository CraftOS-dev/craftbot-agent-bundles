<!--
Sources: Klue Insider deal-app https://klue.com/insider
         Crayon Sales App https://www.crayon.co/
         Klue × Salesforce playbook https://klue.com/blog/the-salesforce-and-klue-playbook
         Klue topics CI tools 2026 https://klue.com/topics/competitive-intelligence-tools-b2b-software
Companion playbook: role.md → "Hot-deals CI playbook"
-->

# Hot-deals CI (deal-level micro-battlecard)

For active opportunities where competitor flag is set in CRM, generate a deal-specific micro-battlecard: this account's intent signals (Bombora / G2 / 6sense), this competitor's recent wins/losses in this segment, this contact's LinkedIn history with competitor (current/former employee? deal history?), this account's tech stack (BuiltWith / Wappalyzer), this account's recent press / hiring signals. 6-8 bullets max. Deliver to Salesforce + Slack DM to AE within minutes of competitor field set.

## When to use

- "Generate deal-level CI for opportunity X"
- Salesforce opportunity `Competitor__c` set or changed
- AE asks for pre-call brief
- Late-stage deal at risk; flash-brief request
- Surge / intent signal on an account
- Daily new-deal trigger

## When NOT to use

- General battlecard refresh → use `battlecard-authoring-maintenance`
- Multi-competitor compset monitoring → use `continuous-competitor-monitoring-klue-kompyte-crayon`
- Kill-sheet content authoring → use `kill-sheet-objection-rebuttals`

## Setup

```bash
# Salesforce webhook source
export SF_USERNAME="..."
export SF_PASSWORD="..."
export SF_SECURITY_TOKEN="..."

# Klue Insider (deal-app)
export KLUE_API_KEY="..."

# Intent
export BOMBORA_API_KEY="..."
export G2_BUYER_INTENT_API_KEY="..."
export SIXSENSE_API_KEY="..."
export ZOOMINFO_API_KEY="..."

# Tech-stack
export BUILTWITH_API_KEY="..."

# LinkedIn skill (default in bundle)
# Slack
export SLACK_BOT_TOKEN="..."
```

MCPs in `agent.yaml`: `salesforce-api`, `linkedin`, `slack-mcp`, `firecrawl-mcp`, `cli-anything`.

## Common recipes

### Recipe 1: Salesforce Apex / Process Builder trigger

```apex
trigger OpportunityCompetitorSet on Opportunity (after update) {
    for (Opportunity opp : Trigger.new) {
        Opportunity old = Trigger.oldMap.get(opp.Id);
        if (opp.Competitor__c != null && opp.Competitor__c != old.Competitor__c) {
            CIWebhook.send(opp.Id, opp.Competitor__c, opp.AccountId, opp.OwnerId);
        }
    }
}
```

### Recipe 2: Webhook handler — kick deal-level CI pipeline

```python
from flask import Flask, request
app = Flask(__name__)

@app.post("/hot-deals-trigger")
def trigger():
    p = request.json
    opportunity_id = p["opportunity_id"]
    competitor     = p["competitor"]
    account_id     = p["account_id"]
    ae_user_id     = p["ae_user_id"]
    micro_bc = build_micro_battlecard(opportunity_id, competitor, account_id, ae_user_id)
    push_to_salesforce(opportunity_id, micro_bc)
    dm_ae(ae_user_id, micro_bc)
    return "ok"
```

### Recipe 3: Build micro-battlecard (6-8 bullets)

```python
def build_micro_battlecard(opp_id, competitor, account_id, ae_user_id):
    bullets = []
    # Intent
    intent = fetch_intent(account_id, competitor)
    if intent["surge_score"] >= 60:
        bullets.append(f"INTENT: {intent['source']} surge {intent['surge_score']} on {competitor} category (L7D).")
    # Recent comp wins/losses in segment
    recent = fetch_recent_deals(competitor, segment=fetch_segment(account_id))
    bullets.append(f"DEAL HISTORY vs {competitor}: {recent['wins']} wins / {recent['losses']} losses last 90 days in {recent['segment']}.")
    # Contact LinkedIn history with competitor
    li = check_linkedin_history(account_id, competitor)
    if li["former_competitor_employee"]:
        bullets.append(f"CHAMPION RISK: contact {li['contact_name']} is *former {competitor}* employee — likely champion or detractor.")
    # Account tech stack
    stack = fetch_builtwith(fetch_account_domain(account_id))
    overlap = stack_overlap(stack, our_product=True)
    if overlap["score"] >= 0.7:
        bullets.append(f"STACK FIT: {overlap['score']*100:.0f}% overlap with our integrations. Lead with: {', '.join(overlap['shared'])}.")
    # Recent press / hiring
    press = recent_press(account_id, since_days=30)
    if press:
        bullets.append(f"ACCOUNT SIGNAL: {press[0]['headline']} ({press[0]['date']}).")
    # Top likely objection + rebuttal
    obj = top_objection_for_segment(competitor, account_id)
    bullets.append(f'LIKELY OBJECTION: "{obj["text"]}" → {obj["rebuttal"]}')
    # Pricing leverage
    bullets.append(f"PRICING LEVERAGE: typical discount needed {est_discount(competitor, account_id)}% to win.")
    return bullets[:8]
```

### Recipe 4: Intent fetch (multi-source)

```python
def fetch_intent(account_id, competitor):
    domain = fetch_account_domain(account_id)
    sources = []
    # Bombora
    b = bombora_company_surge(domain, topic=competitor)
    sources.append({"source":"bombora","score":b["surge_score"]})
    # G2
    g = g2_buyer_intent(domain, competitor=competitor)
    sources.append({"source":"g2","score":g["score"]})
    # 6sense
    six = sixsense_account(domain, topic=competitor)
    sources.append({"source":"6sense","score":six["score"]})
    # fused
    return max(sources, key=lambda x: x["score"]) | {"competitor": competitor}
```

### Recipe 5: LinkedIn contact-history check

```python
def check_linkedin_history(account_id, competitor):
    contact = primary_contact(account_id)
    li_profile = linkedin_skill.get_profile_public(contact["linkedin_url"])
    for job in li_profile["experience"]:
        if competitor.lower() in job["company"].lower():
            return {
                "contact_name": contact["name"],
                "former_competitor_employee": True,
                "tenure": job["years"],
                "title": job["title"],
            }
    return {"contact_name": contact["name"], "former_competitor_employee": False}
```

### Recipe 6: Recent comp wins/losses in segment

```python
def fetch_recent_deals(competitor, segment):
    sf_query = f"""
    SELECT Id, StageName, Amount FROM Opportunity
    WHERE Competitor__c = '{competitor}'
      AND Account.Segment__c = '{segment}'
      AND CloseDate >= LAST_N_DAYS:90
    """
    deals = sf.query_all(sf_query)["records"]
    return {
        "wins":   sum(1 for d in deals if d["StageName"] == "Closed Won"),
        "losses": sum(1 for d in deals if d["StageName"] == "Closed Lost"),
        "segment": segment,
    }
```

### Recipe 7: Account tech-stack BuiltWith

```python
def fetch_builtwith(domain):
    r = requests.get(f"https://api.builtwith.com/v21/api.json?KEY={BW_KEY}&LOOKUP={domain}")
    techs = [t for path in r.json()["Results"][0]["Result"]["Paths"]
                for t in path["Technologies"]]
    return {t["Name"]: t["Tag"] for t in techs}
```

### Recipe 8: Salesforce activity insert (micro-battlecard attached)

```python
def push_to_salesforce(opp_id, micro_bc):
    body = "\n".join(f"• {b}" for b in micro_bc)
    sf.Task.create({
        "Subject": "Deal-level CI brief",
        "Description": body,
        "WhatId": opp_id,
        "Status": "Completed",
        "TaskSubtype": "Other",
    })
```

### Recipe 9: Slack DM AE

```python
def dm_ae(ae_user_id, micro_bc):
    text = "*Deal-level CI brief*\n" + "\n".join(f"• {b}" for b in micro_bc)
    requests.post("https://slack.com/api/chat.postMessage",
                  headers={"Authorization":f"Bearer {SLACK_BOT_TOKEN}"},
                  json={"channel":f"@{ae_user_id}", "text":text})
```

### Recipe 10: Klue Insider native deal-app

If licensed, Klue Insider does much of this natively:

```bash
# Klue Insider auto-attaches deal-level battlecard to opportunity
curl -X POST "$KLUE_API_BASE/insider/deals" \
  -H "Authorization: Bearer $KLUE_API_KEY" \
  -d '{
    "opportunity_id": "'"$OPP_ID"'",
    "competitor_id": "'"$COMP"'",
    "include_intent": true,
    "include_account_signal": true
  }'
```

### Recipe 11: Crayon Sales App equivalent

Crayon Sales App has a similar deal-level surface; configure via Salesforce app settings.

### Recipe 12: Deal outcome → CI program metrics

```python
def track_outcome(opp_id):
    # When deal closes, log: CI used (Y/N), stage where used, outcome
    sf.Opportunity.update(opp_id, {
        "CI_Used__c": True,
        "CI_Influence__c": ae_self_report(opp_id),
    })
```

Feeds `ci-program-metrics-adoption-rate` Recipe 6 (CI-influenced revenue).

### Recipe 13: Refresh trigger (re-pull intent every 7d while deal open)

```python
def refresh_intent(opp_id):
    opp = sf.Opportunity.get(opp_id)
    if opp["StageName"] not in ["Closed Won","Closed Lost"]:
        new_intent = fetch_intent(opp["AccountId"], opp["Competitor__c"])
        if new_intent["score"] > opp["Last_Intent_Score__c"] + 10:
            dm_ae(opp["OwnerId"], [f"INTENT UPDATE: score now {new_intent['score']} (+{new_intent['score'] - opp['Last_Intent_Score__c']})"])
        sf.Opportunity.update(opp_id, {"Last_Intent_Score__c": new_intent["score"]})
```

## Examples

### Example 1: End-to-end hot-deal trigger

**Goal:** AE marks `Competitor__c = "Acme Corp"` on an opportunity → micro-battlecard DM in <60s.

**Steps:**
1. Recipe 1 → Apex trigger fires.
2. Recipe 2 → webhook handler runs Recipe 3.
3. Recipes 4-7 → assemble signals.
4. Recipe 8 → SF activity insert (attaches to opp record).
5. Recipe 9 → Slack DM to AE.

**Result:** AE gets brief in DM before first call.

### Example 2: Former-competitor-employee champion detection

**Goal:** Detect when account contact is former competitor employee — likely champion or detractor.

**Steps:**
1. Recipe 5 → LinkedIn check on primary contact.
2. Found: contact was Acme Director of Sales for 3 years until 2024.
3. Micro-battlecard bullet flags this; AE adjusts approach (probably champion, lead with "what frustrated you about Acme").

### Example 3: Intent-surge alert + recheck

**Goal:** During a 60-day sales cycle, detect intent surge and re-DM the AE.

**Steps:**
1. Recipe 13 → daily refresh check.
2. Intent score jumps from 45 to 78.
3. DM: "INTENT UPDATE: Acme surge on account 78 (+33). Likely doing parallel eval. Suggest moving to commitment step."

### Example 4: Self-build (no Klue Insider) — full pipeline

**Goal:** All Recipes 1-9 + 13 without paid Klue.

**Steps:**
1. Recipe 1 → SF Apex.
2. Recipe 2 → run on Lambda / Cloud Run.
3. Skip Recipe 10/11 (Klue/Crayon native).
4. Recipe 8 + 9 → SF activity + Slack DM as canonical surfaces.

## Edge cases / gotchas

- **Competitor field volatility** — reps flip flag multiple times; debounce 5 min before kicking pipeline.
- **Multi-competitor deals** — `Competitor__c` is single-select usually; for multi-pick, run pipeline per competitor with deduped DM.
- **Intent data lag** — Bombora weekly; G2 near-real-time; surge score at trigger may already be stale.
- **LinkedIn skill rate limits** — public-profile fetch capped; cache 30d.
- **BuiltWith cost** — 1 call per hot-deal trigger; if 100 hot deals/day, that's 100 calls. Cache 7d per domain.
- **AE DM fatigue** — limit 1 DM per opp per 7 days unless intent-jump per Recipe 13.
- **Wrong account-to-domain mapping** — Salesforce `Website` field unreliable; have a fallback resolver.
- **SCIP compliance on LinkedIn** — public-view only; never DM the contact for CI under fake pretense (`ethical-public-source-methodology` Recipe 2 hard no).
- **No intent data licensed** — drop Recipe 4; pipeline still works on Recipes 5-7.
- **Privacy / GDPR** — EU accounts may opt out of intent; respect.
- **Apex CPU limits** — trigger should fire webhook to external compute; don't compute the brief in Apex.
- **Slack bot scope** — `chat:write` + DM scope; admin to install.
- **Outcome attribution** — Recipe 12 self-reported; biased. Pair with battlecard-opened-in-window.
- **PROACTIVE.md** — trigger-based, not cron-based; document trigger config.
- **Provenance footer in DM** — for each bullet, cite source in compact form (`L7D Bombora; G2 review #12345; LI profile`).

## Sources

- Klue Insider — https://klue.com/insider
- Klue × Salesforce playbook — https://klue.com/blog/the-salesforce-and-klue-playbook
- Klue topics CI tools 2026 — https://klue.com/topics/competitive-intelligence-tools-b2b-software
- Crayon Sales App — https://www.crayon.co/
- Salesforce Apex Trigger reference — https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/apex_triggers.htm
- role.md → "Hot-deals CI playbook"

## Related skills

- `intent-data-bombora-g2-zoominfo` — intent fetch source
- `competitor-tech-stack-builtwith-wappalyzer` — account stack pull
- `competitor-hiring-intel-linkedin-sales-nav` — contact LinkedIn history
- `ci-delivery-slack-crm-klue-insider` — SF activity + Slack DM delivery
- `ci-program-metrics-adoption-rate` — outcome tracking flows here
- `battlecard-authoring-maintenance` — micro-battlecard sources from canonical battlecard
