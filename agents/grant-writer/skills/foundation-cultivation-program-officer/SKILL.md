---
name: foundation-cultivation-program-officer
description: Build multi-touch cultivation cadences with foundations — research priorities, request PO call before LOI, track all touches in Bloomerang/DonorPerfect/Salesforce CRM + Notion relationship notes. Use when the user says "cultivate <foundation>" / "build a PO relationship" / "before we send the LOI".
---

# Foundation cultivation + program officer relationship building

Foundations don't fund based on one proposal — they fund based on a cultivated relationship. The 12-month cadence: discover → research → warm intro → PO call → LOI → full proposal → decision → stewardship → renewal. PO call before LOI confirms fit and saves wasted submissions.

## When to use

- New foundation prospect added to pipeline
- Org is over-reliant on cold submissions and decline rate is too high
- Annual cultivation planning for top 10 foundation relationships
- After site visit / convening / event where new PO was met
- Restarting cultivation with a lapsed funder (didn't fund last cycle but worth re-engaging)

Do NOT use this skill for:
- LOI / proposal drafting itself (→ `loi-letter-of-inquiry-drafting`, `full-grant-proposal-narrative-methods-evaluation`)
- Multi-grant pipeline analytics (→ `multi-grant-pipeline-mgmt`)
- Declined-grant feedback request (→ `declined-grant-iteration`)

## Setup

```bash
# Tools
# - gmail-mcp or outlook-mcp (cultivation emails)
# - google-calendar-mcp (PO touchpoint reminders)
# - notion-mcp (foundation profile cards + relationship notes)
# - CRM via cli-anything (Bloomerang, DonorPerfect, Salesforce Nonprofit Cloud)

# CRM selection by org size
# <$1M revenue: Bloomerang + Notion (no native grants in Bloomerang; pair)
# $1-10M: DonorPerfect (light grant tracking) or Bloomerang Standard
# >$10M: Salesforce Nonprofit Cloud (NPSP/EDA) — full grant compliance
```

Auth / API key requirements:
- Bloomerang — API key
- DonorPerfect — API key
- Salesforce — OAuth + connected app

## Common recipes

### Recipe 1: 12-month cultivation cadence

```markdown
| Month | Touch | Tool | Goal |
|---|---|---|---|
| 1 | Research PO + funder priorities | firecrawl-mcp + ProPublica + Candid | Build profile card |
| 1 | LinkedIn / warm-intro request | gmail-mcp | Request intro via mutual connection |
| 2 | PO call request (15 min) | gmail-mcp + google-calendar-mcp | Confirm fit before LOI |
| 3 | LOI sent (if invited) | docx + gmail-mcp / portal | Earn full proposal invite |
| 4-5 | Full proposal | proposal mode | Win the grant |
| 6 | Decision + thank-you + site visit offer | gmail-mcp | Build relationship regardless |
| 7-9 | Quarterly impact update / annual report | docx | Stewardship |
| 10-11 | Invitation to event / convening | gmail-mcp + google-calendar-mcp | Build personal relationship |
| 12 | Renewal LOI / next-cycle outreach | LOI mode | Sustain pipeline |
```

### Recipe 2: Foundation profile card in Notion

```markdown
# <Foundation Name>
- **Tax ID / EIN:** XX-XXXXXXX
- **Subsection:** 501(c)(3) private foundation (subsection 04)
- **Annual giving:** $<amount> (from latest 990 PF)
- **Geographic focus:** <areas>
- **Program areas:** <areas>
- **Avg grant size:** $<amount> (from last 10 grants)
- **Range:** $<min> - $<max>
- **Cycle:** LOI <month>, Full proposal <month>, Decision <month>

## Program officer
- **Name:** <Name>
- **Title:** <Program Officer, Program X>
- **Background:** <years at foundation; prior role>
- **LinkedIn:** <link>
- **Publications / talks:** <if any>

## Recent grantees (signal)
- <Peer org>: $<amount> (FY <year>) — <project>
- <Peer org>: $<amount> (FY <year>) — <project>
- <Peer org>: $<amount> (FY <year>) — <project>

## Our touches log
| Date | Touch type | Owner | Notes | Next action |
|---|---|---|---|---|
| 2026-03-15 | Email intro via Sarah Chen | SC | PO replied positive; suggested call | Schedule call |
| 2026-04-02 | PO call (Zoom 15min) | SC + ED | Discussed alignment; PO suggested specific framing | Send LOI Q3 |
| 2026-06-01 | LOI sent | SC | Acknowledged; decision Aug | Wait |
```

### Recipe 3: Warm intro request

```markdown
Subject: Quick favor — <Foundation> intro

<Mutual connection first name>,

Hope you're well. I'm working on a project at <Org> on <topic>, and I noticed
<Foundation> recently funded <peer org> for similar work. I'd love to learn more
about how their priorities align with ours.

Would you be open to a quick email intro to <PO name>? Happy to draft something
you can forward, or just a sentence from you would mean a lot.

Thanks for considering,
<Name>
```

### Recipe 4: PO call request

```markdown
Subject: <Org name> — fit with <Foundation>'s <priority> priority?

Dear <PO First Name>,

[Hook: "Sarah Chen at <peer org> suggested I reach out" OR "I read your <article/post> on <topic>."]

<Org> works on <topic> in <geo>. We're planning <project>, and I believe it
fits <Foundation>'s <priority> priority. Before submitting an LOI, I'd love
to confirm fit and learn what would strengthen our submission.

Would a brief 15-minute call be useful? I'm flexible Tuesday-Thursday next week.

Best,
<Name>
<Title>, <Org>
<Phone> | <Email>
```

### Recipe 5: PO call prep

```markdown
## Pre-call (1 hour prep)
- Re-read foundation strategy + 3 recent grants in same priority
- Bring 3 specific questions: (1) fit confirmation, (2) framing advice, (3) timing
- Prepare 60-second org pitch + 30-second project pitch

## During call (15 min)
- Min 0-2: introductions + thanks
- Min 2-5: org + project overview (don't pitch; share)
- Min 5-12: questions + listening
- Min 12-15: next steps + thanks

## Post-call (within 24 hours)
- Thank-you email reiterating key points discussed
- Update Notion profile card touches log
- Update calendar with LOI submission date if confirmed
```

### Recipe 6: Quarterly impact update (stewardship)

```markdown
Subject: <Org> Q1 impact update for <Foundation>

Dear <PO First Name>,

Thank you again for <Foundation>'s investment in <project>. Quick update this quarter:

- **Progress:** <2-3 specific accomplishments with metrics>
- **What we learned:** <1 specific insight>
- **Where we're going next quarter:** <1-2 specific milestones>

Happy to set up a site visit if useful. We'd be honored to host you.

Thanks,
<Name>
```

Sent quarterly during the grant period — not just at formal report time.

### Recipe 7: Site visit invitation

```markdown
Subject: Site visit invitation — <project> in action

Dear <PO First Name>,

We'd love to host you to see <project> in action. <Brief description: 1-2 sentences>.

Suggested visit:
- Date options: <3 weekdays>
- Duration: 90 minutes (program tour + Q&A with staff + ED meeting)
- Location: <address + parking notes>

Please let us know what works.

Thanks,
<Name>
```

Site visits are the single highest-leverage cultivation activity. Push for at least 1 per top-10 funder per year.

### Recipe 8: CRM logging — Salesforce Nonprofit Cloud example

```bash
# Via cli-anything → Salesforce SOQL or NPSP
sfdx force:data:soql:query -q "SELECT Id, Name, npe01__SystemAccountProcessor__r.Name FROM Account WHERE Type = 'Foundation'"

# Log a touch in NPSP
sfdx force:data:record:create -s Task -v "Subject='PO call' WhoId='<contact_id>' WhatId='<account_id>' Description='...'"
```

CRM stores: contact records, accounts, opportunities (proposals), activities (touches), reports.

### Recipe 9: Bloomerang sync (smaller orgs)

```bash
# Bloomerang API for constituent + interaction tracking
curl -H "X-API-KEY: $BLOOMERANG_KEY" \
  "https://api.bloomerang.co/v2/constituent?id=<funder_constituent_id>"

# Log interaction
curl -H "X-API-KEY: $BLOOMERANG_KEY" \
  -X POST "https://api.bloomerang.co/v2/interaction" \
  -d '{"constituentId": 12345, "channel": "phone", "subject": "PO call", "notes":"..."}'
```

Bloomerang has no native grants module. Pair with Notion pipeline.

### Recipe 10: Annual top-10 cultivation review

```markdown
## Q4 cultivation review (annual)
For each of top 10 funder relationships:
- Touches this year (count + type)
- PO call done?
- Site visit done?
- Quarterly updates sent?
- Renewal LOI submitted / planned?

If any top-10 funder has <4 touches this year, the relationship is at risk.
```

### Recipe 11: Decline → re-cultivate

```markdown
## After a decline, cultivation continues
- Send thank-you within 1 week (even though declined)
- Request feedback within 30 days (skill: declined-grant-iteration)
- Continue quarterly updates
- Invite to event / convening (positions you as a sector resource)
- Re-submit next cycle with adjusted ask + stronger evidence
```

### Recipe 12: Multi-year funder relationship plan

```markdown
## Year 1: New relationship
- LOI → Proposal → Decision
- Foundation evaluates fit and execution

## Year 2: First renewal cycle
- Demonstrate Year 1 outcomes
- Build PO personal relationship via site visit
- Apply for renewal grant

## Year 3-5: Trusted partner
- Foundation may multi-year you
- Earlier inclusion in their strategy thinking
- Reference grantee for their other due diligence
```

## Examples

### Example 1: New cultivation for Hewlett Foundation

**Goal:** Build relationship with Hewlett before submitting LOI in Q4.

**Steps:**
1. Build profile card in Notion (Recipe 2) — pull 990, recent grants, PO name.
2. Identify mutual connection on LinkedIn; request warm intro (Recipe 3).
3. Email PO requesting 15-min call (Recipe 4).
4. Prep call (Recipe 5); reconfirm fit + framing.
5. Send thank-you within 24 hours; update Notion.
6. Schedule LOI submission per PO's guidance.
7. Send quarterly updates for the rest of the year (Recipe 6).
8. Invite PO to fall convening.

**Result:** Warm relationship with Hewlett PO; LOI submitted with fit confirmed; visible touches log in Notion.

### Example 2: Stewarding a current funder for renewal

**Goal:** Cultivate Robert Wood Johnson Foundation PO during Year 1 of grant for renewal in Year 2.

**Steps:**
1. Send Q1 impact update email (Recipe 6).
2. Invite PO for site visit Q2 (Recipe 7).
3. Site visit: host PO, demonstrate program, introduce key staff + beneficiary (consent).
4. Q3 impact update.
5. Submit interim report on time + 2 weeks early.
6. Q4: invite to convening + start renewal conversation.
7. Year 2 LOI / proposal with strong outcomes evidence.

**Result:** PO knows project deeply; renewal more likely with documented Year 1 success.

## Edge cases / gotchas

- **Unsolicited funders.** Many large foundations (Gates, Ford, MacArthur) explicitly do not accept unsolicited LOIs. Cultivation alternatives: be invited via existing grantees, attend their convenings, publish work in spaces they read.
- **Don't ask for the next grant in stewardship emails.** Stewardship is about updates + relationship; sales feels gross. Save the ask for renewal LOI.
- **PO turnover.** POs move every 2-4 years on average. New PO = rebuild relationship. Watch foundation staff pages + LinkedIn.
- **Email cadence:** quarterly is right. Monthly = annoying. Annual = forgotten. Quarterly = thoughtful.
- **Personal vs org relationship.** Personal relationship lives with the staff member who built it. Document in CRM so it survives staff transitions.
- **Site visits require staffing.** ED + Program Lead + key staff. Don't show up understaffed.
- **Don't oversell on PO call.** Listen more than you talk. PO offers fit feedback; agree where fit is real; defer where it isn't.
- **Foundation event ROI.** Most foundation events (galas, convenings, briefings) are net positive cultivation. Send senior staff.
- **CRM hygiene.** Touch log must be updated within 24 hours. A CRM with 6-month-old data is worse than no CRM.
- **Don't bcc funders on group emails.** Personalized communication only.

## Sources

- Inside Philanthropy — LOI Explainer: https://www.insidephilanthropy.com/explainers/what-is-a-letter-of-inquiry-loi
- Nonprofit Point — Best CRM for Nonprofits: https://nonprofitpoint.com/best-crm-for-nonprofits/
- Bloomerang Nonprofit CRM: https://bloomerang.com/blog/nonprofit-crm/
- Bloomerang: https://bloomerang.com/
- DonorPerfect: https://www.donorperfect.com/
- Salesforce Nonprofit Cloud: https://www.salesforce.org/products/nonprofit-cloud/
- Cube84 — Bloomerang vs Salesforce NPSP: https://cube84.com/blog/bloomerang-vs-salesforce-nonprofit-cloud-vs-npsp-which-crm-is-best-for-your-nonprofit
- Council on Foundations — Cultivation best practices: https://www.cof.org/
