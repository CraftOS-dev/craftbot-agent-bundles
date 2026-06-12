<!--
Source: https://www.gong.io/blog/multi-threading/ + Challenger Customer methodology
Multi-threading enterprise deals (June 2026 SOTA).
-->
# Multi-Threading Enterprise Deals — SKILL

Single-threaded deals die when the one person you know goes silent or leaves. Multi-threading maps the buying committee — economic buyer, champion, technical evaluator, end-user voice, executive sponsor, blockers — then engages each with the right outreach. Targets: 4+ stakeholders engaged for deal > $50K, 5-7 for > $150K.

## When to use

- **Deal > $50K** with only 1-2 stakeholders engaged.
- **Champion silent > 7 days** — broaden so the deal isn't dependent on one node.
- **EB hasn't been brought into a single meeting** by Discovery → Evaluation transition.
- **Enterprise deal > $150K** — must have 5-7 stakeholders + executive sponsor on both sides.
- **Trigger phrases**: "multi-thread this deal", "who else should I engage", "champion is silent", "EB hasn't shown up", "expand the buying committee", "stakeholder map for X".

Do NOT use this skill for: **SMB deals < $25K** with single decision-maker (over-engineered); **post-close expansion** (use `expansion-upsell-renewal-playbook`); **broad ABM coordination** (defer to `marketing-agent` for paid ABM tactics).

## Setup

```bash
export MATON_API_KEY="<key>"   # CRM + Apollo + LinkedIn data
export LI_AT_COOKIE="<cookie>" # for Sales Nav scraping
export NOTION_TOKEN="<key>"    # stakeholder maps live here
```

Required CRM custom fields per deal:
- `stakeholder_count_engaged` (number)
- `stakeholder_map_notion_url` (URL)
- `executive_sponsor_us` (text — our exec who's involved)
- `executive_sponsor_them` (text — their exec we've engaged)

## Common recipes

### Recipe 1: Stakeholder map template (canonical per role.md)

```markdown
# Stakeholder Map — [Account]

| Stakeholder | Title | Role in eval | Last engaged | Engagement depth | Influence | Sentiment |
|---|---|---|---|---|---|---|
| Name 1 | VP Eng | Champion | 2026-06-02 | 5 touches / 2 meetings | High | Positive |
| Name 2 | CTO | Economic buyer | 2026-05-15 | 1 touch / 0 meetings | Critical | Unknown |
| Name 3 | Dir Platform | Technical evaluator | 2026-05-28 | 3 touches / 1 meeting | Medium | Neutral |
| Name 4 | CFO | Approver | Not engaged | 0 | Critical (price) | Unknown |
| Name 5 | Sr Eng | End-user voice | 2026-05-20 | 2 touches | Low | Positive |
| Name 6 | VP Security | Blocker (procurement gate) | Not engaged | 0 | High (gate) | Unknown |

## Engagement targets by deal size
- Deal < $25K: 1 stakeholder sufficient (champion = decision-maker)
- Deal $25-50K: 2-3 stakeholders engaged
- Deal $50-150K: 4+ stakeholders, including EB confirmed
- Deal > $150K: 5-7 stakeholders, exec sponsor on both sides

## Multi-thread tactics
- LinkedIn "thanks for connecting" message to silent stakeholders
- Content gift ungated to silent EB (industry report, ROI study)
- Champion-driven intro request to peer stakeholders
- Joint AE + champion-led meeting to bring EB in
- Executive sponsor outreach (your CEO/CRO to their counterpart)
```

### Recipe 2: Discover the buying committee (Apollo + LinkedIn)

```bash
# Pull all people at the company with relevant titles
curl -X POST "https://gateway.maton.ai/apollo/api/v1/mixed_people/search" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "organization_ids":["<apollo-org-id>"],
    "person_titles":["VP Sales","CRO","CTO","CFO","VP Marketing","Head of Sales","Director of Sales","VP Engineering","Director of Product","VP Operations","COO","Head of RevOps","CISO","VP Security"],
    "per_page":50
  }' > committee_candidates.json
```

Cross-reference candidates against existing CRM contacts to find: (a) already engaged, (b) candidate but not engaged, (c) net-new role we should add.

### Recipe 3: Role assignment for each candidate

```python
ROLES = {
    "champion": "person advocating internally; has shown enthusiasm",
    "economic_buyer": "person with budget authority; usually VP+ for $50K-200K, C-suite for $200K+",
    "technical_evaluator": "person evaluating the product technically",
    "end_user_voice": "person who will use the product daily",
    "executive_sponsor_them": "their exec (CEO/CRO/CFO depending on category) sponsoring the initiative",
    "blocker": "person whose approval is required AND could block (Security / Procurement / Legal)",
    "approver": "person whose sign-off is required for budget",
}

def assign_role(person, deal_context):
    """Heuristics — refine with each call."""
    title = person["title"].lower()
    if "ceo" in title or "founder" in title: return "executive_sponsor_them" if deal_context["acv"] > 250_000 else "approver"
    if "cfo" in title: return "approver"
    if "ciso" in title or "vp security" in title: return "blocker"
    if "head of" in title or "vp" in title or "director" in title:
        return "economic_buyer" if "sales" in title or "revenue" in title or "marketing" in title else "technical_evaluator"
    if "manager" in title or "lead" in title:
        return "champion"  # often where champions hide
    return "end_user_voice"
```

### Recipe 4: Engagement-depth scoring

```python
def engagement_depth(person, deal_id):
    """Score 0-5 based on touches + meetings."""
    touches = count_touches(person["email"], deal_id, days=60)   # emails + LI + calls
    meetings = count_meetings(person["email"], deal_id, days=60)
    advocacy = has_advocacy_evidence(person["email"], deal_id)   # forwarded our content, asked Qs internally

    score = 0
    if touches >= 1: score += 1
    if touches >= 3: score += 1
    if meetings >= 1: score += 1
    if meetings >= 2: score += 1
    if advocacy: score += 1
    return score
```

`0` = silent, `5` = engaged-champion. Target: every role with influence "Critical" or "High" should be ≥ 2 by Evaluation stage.

### Recipe 5: Gap report — who's missing + who's silent

```python
def stakeholder_gaps(deal):
    smap = get_stakeholder_map(deal["id"])
    gaps = []

    # Missing role
    if not any(s["role"] == "economic_buyer" for s in smap):
        gaps.append({"type":"missing_role","role":"economic_buyer","priority":"high"})
    if deal["amount"] > 150_000 and not any(s["role"] == "executive_sponsor_them" for s in smap):
        gaps.append({"type":"missing_role","role":"executive_sponsor","priority":"high"})

    # Silent stakeholders (last_engaged > 14d)
    for s in smap:
        if s["influence"] in ("critical","high") and engagement_depth(s, deal["id"]) < 2:
            gaps.append({"type":"silent","stakeholder":s["name"],"priority":"high"})
    return gaps
```

### Recipe 6: Multi-thread tactics by stakeholder type

```yaml
silent_eb:
  - "champion-driven intro request: 'Sarah, would you be open to introducing me to <EB Name>? Even 10 min — I'd like to make sure they have what they need to feel confident'"
  - "ungated content gift via LinkedIn: send industry report or ROI study"
  - "joint AE + champion meeting where EB is invited"
  - "executive sponsor outreach: your CEO/CRO emails their counterpart"
silent_technical_evaluator:
  - "demo session focused on their stack"
  - "tech-deep-dive doc shared by champion"
  - "office hours with our CTO / Head of Eng"
silent_end_user_voice:
  - "include them in the technical demo"
  - "send a 5-min product walkthrough video"
  - "ask champion: 'who else on the team should weigh in?'"
silent_blocker_security_procurement:
  - "pre-emptively share security overview (SOC 2, ISO 27001, pen test summary)"
  - "ask champion: 'who's leading the security review? Mind connecting me directly?'"
  - "InfoSec questionnaire sent same-day on request"
silent_approver_cfo:
  - "share ROI calc + reference customer with similar size"
  - "champion-driven intro to financial conversation"
  - "concession ladder pre-built (deal-coaching-next-best-action Recipe 6)"
```

### Recipe 7: Champion-driven intro request (email script)

```markdown
Subject: One quick favor

Hi [Champion First Name],

For us to make [EB First Name] feel really confident on this, I'd love to bring them into the next 15 min — just to share the lens we've heard from peers at similar [vertical] companies.

Two options:
1. I can join your next 1:1 with them (5-10 min appearance).
2. You forward a 1-pager — I'll prep one tailored to [EB's likely concern].

Which is easier? If neither, totally open to ideas.

Thanks,
[AE]
```

### Recipe 8: Executive-sponsor outreach (peer-level)

```markdown
# When sales-agent's owner needs their CEO/CRO to engage their CEO/CRO
Subject: Quick word — [Our company] × [Their company]

Hi [Their CEO/CRO First Name],

We've been working with [Champion Name] at [their company] on [initiative]. Wanted to introduce myself directly given how much potential we see together.

If helpful, would love 15 min to share what we've seen with similar [vertical / stage] companies on [topic]. Happy to come prepared.

Calendar: [link]

Best,
[Our CEO/CRO Name]
```

Triggered when: deal > $150K AND EB hasn't responded to AE/champion outreach in 14 days.

### Recipe 9: Stakeholder map maintenance (weekly)

```python
# Every Monday, refresh the map for each active deal > $50K
for deal in active_enterprise_deals():
    smap = get_stakeholder_map(deal["id"])
    for s in smap:
        s["engagement_depth"] = engagement_depth(s, deal["id"])
        s["last_engaged"] = last_activity_for(s["email"], deal["id"])
        s["sentiment"] = latest_sentiment_for(s["email"], deal["id"])  # from Gong

    # Re-render to Notion + post gaps to Slack
    notion_update_stakeholder_map(deal["id"], smap)
    gaps = stakeholder_gaps(deal)
    if gaps:
        slack_dm(deal["owner_id"], f"{deal['name']} — multi-thread gaps:\n" + "\n".join(f"• {g['type']}: {g.get('role',g.get('stakeholder'))}" for g in gaps))
```

### Recipe 10: Content gift selection (per stakeholder role)

```yaml
eb_content:
  - "Industry report: Forrester / Gartner relevant to their function"
  - "ROI study: 1-pager with conservative-input ROI calc"
  - "Customer story: same-size + same-vertical case"
technical_evaluator_content:
  - "Technical whitepaper or architecture doc"
  - "Public docs / changelog / API reference"
  - "Video walkthrough of integration"
cfo_content:
  - "Payback analysis"
  - "Pricing comparison vs status quo + alternatives"
  - "Reference call recording from CFO-peer customer"
ciso_content:
  - "SOC 2 / ISO 27001 / pen test summary"
  - "Data flow + sub-processor list"
  - "DPA template"
```

### Recipe 11: Sales Nav org chart enrichment

```bash
# Sales Nav has a /org-chart/ view but no API. Scrape via brightdata-mcp or playwright-mcp.
mcp tool brightdata.scrape_url \
  --url "https://www.linkedin.com/sales/people/<companyId>/organizational-chart" \
  --renderJs true \
  --cookies '[{"name":"li_at","value":"'$LI_AT_COOKIE'"}]'
```

Use to identify the reporting line above your champion — that's usually your EB or one step from it.

### Recipe 12: Track multi-thread KPIs

```yaml
per_deal:
  - stakeholder_count_engaged (target: 4+ for $50K+, 5-7 for $150K+)
  - eb_engaged (boolean — has EB been in at least 1 meeting?)
  - executive_sponsor_engaged_them (for $150K+ deals)
per_ae_monthly:
  - avg_stakeholders_per_deal (target by segment)
  - % deals with EB engaged before proposal stage (target: 80%+)
  - % deals lost to "champion left" (target: < 10% — high here = single-thread problem)
```

## Examples

### Example 1: $120K deal stuck in Evaluation — EB silent

**Goal:** EB never met us. Champion responsive but says "EB is busy". Need EB engagement before proposal.

**Steps:**
1. Recipe 5 — gap analysis flags `silent_eb`.
2. Recipe 7 — send champion the intro-request email. Offer 1-pager option as fallback.
3. If champion accepts: prep 1-pager tailored to EB's known priorities (use `account-research-deep` for EB's LinkedIn posts, signals).
4. If silent 5 days: Recipe 8 — escalate to exec-sponsor peer outreach.
5. If still silent 5 more days: this is no longer a real deal; downgrade forecast bucket.

**Result:** Either EB engages within 10 days, or the deal moves out of Commit, freeing AE attention.

### Example 2: $300K enterprise multi-thread audit

**Goal:** Pre-proposal review — confirm we've engaged all critical roles.

**Steps:**
1. Recipe 2 — pull all relevant candidates from Apollo.
2. Recipe 3 — assign roles to each.
3. Recipe 4 — score engagement depth per CRM activity.
4. Recipe 5 — identify gaps (missing role + silent stakeholders).
5. For each gap, recipe 6 picks the tactic; build an outreach plan with deadlines.
6. Render full stakeholder map + plan to Notion; review with manager before proposal.

**Result:** Proposal sent into a fully-engaged buying committee, not a single-thread leap of faith.

## Edge cases / gotchas

- **Champion ≠ EB.** AEs frequently confuse them. Champion advocates internally; EB has budget authority. Same person only in small / flat orgs.
- **Multi-threading is NOT spamming the committee.** Each stakeholder gets relevant content for their role — CFO gets ROI, CISO gets security, EB gets industry context. Wrong content to wrong role = annoying.
- **"My champion will handle the EB"** is the most common single-threading failure. Champions over-promise + under-deliver on internal selling. You need your own EB relationship.
- **Going around the champion** to the EB without champion approval can torch the deal — *always* offer the champion the option to facilitate first.
- **Org chart from Sales Nav can be stale** (LinkedIn lags by 2-12 weeks for new hires + lateral moves). Cross-check with company website + Apollo for recent moves.
- **Procurement / Legal as Blockers** are often added late (Stage 4-5). Engage them in Stage 3 via security-overview share to avoid late-stage drag.
- **Executive-sponsor peer outreach must be coordinated** — your CEO emailing their CEO without telling the AE first looks chaotic and undermines trust with champion.
- **Multi-thread depth needs activity-tracking discipline.** If touches + meetings aren't logged in CRM, engagement-depth scoring is wrong.
- **End-user voice is often skipped** because they don't sign the contract. But their post-purchase satisfaction predicts renewal — engage them even if it doesn't accelerate this deal.
- **Stakeholder map should live in CRM** (custom object: Salesforce Account Team, HubSpot custom object) so reps in adjacent quarters can pick up history. Notion is fine as render, but CRM is the system of record.
- **Counter-thread risk**: if your competitor multi-threads better, they win. Track competitor's stakeholder engagement via discovery questions ("who else on your team has talked to <competitor>?").
- **Don't multi-thread small deals.** For < $25K SMB deals, single-thread is correct — multi-threading just slows things down and annoys the buyer.

## Sources

- Gong multi-threading research: https://www.gong.io/blog/multi-threading/
- Challenger Customer (CEB/Gartner) on buying committees: https://www.challengerinc.com/the-challenger-customer/
- "Single-threaded deals die" — Pavilion: https://www.joinpavilion.com/blog/multi-threading
- LinkedIn Sales Navigator org chart features: https://www.linkedin.com/help/sales-navigator/answer/a541938
- Stakeholder mapping in enterprise B2B: https://www.gong.io/blog/stakeholder-mapping/
- "How to engage a CFO" — Pavilion playbook: https://www.joinpavilion.com/blog/cfo-engagement
- 2026 multi-threading benchmark data: https://www.gong.io/labs/multi-threading-2026/
