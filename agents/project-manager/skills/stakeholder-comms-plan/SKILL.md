<!--
Source: https://www.pmi.org/learning/library/stakeholder-management-engagement-influence-10072
Source: https://www.atlassian.com/work-management/project-management/raci-chart
-->
# Stakeholder Comms Plan (Power-Interest + RACI) — SKILL

Mendelow Power-Interest grid + per-stakeholder comms plan + RACI matrix per major deliverable. Stops the two most common PM failures: surprised sponsors and "nobody told me."

## When to use

- Identifying + classifying stakeholders at kickoff (Mendelow 2×2).
- Documenting per-stakeholder info needs, channel, frequency, owner.
- Building a RACI matrix for major deliverables (or DACI for decisions, DRI for ownership).
- Auditing the comms plan when a stakeholder says "I didn't know" — gap analysis.

Trigger phrases: "stakeholder map", "Power-Interest", "Mendelow grid", "RACI", "DACI", "comms plan", "who needs what", "stakeholder cadence", "communication matrix".

## Setup

```bash
# Notion DB (primary storage)
mcp tool notion.search_pages --query "Stakeholder"

# Excalidraw for Power-Interest 2×2 grid
mcp tool excalidraw.generate_diagram --type "quadrant" --help
```

Auth: same as Notion + Excalidraw default tools. No paid tooling required.

## Common recipes

### Recipe 1: Mendelow Power-Interest grid (ASCII)
```
                  HIGH INTEREST
                       │
       KEEP INFORMED   │   MANAGE CLOSELY
       (low P/hi I)    │   (hi P/hi I)
                       │
─── LOW POWER ─────────┼──────── HIGH POWER ───
                       │
       MONITOR         │   KEEP SATISFIED
       (low P/lo I)    │   (hi P/lo I)
                       │
                  LOW INTEREST

Quadrant behaviors:
  MANAGE CLOSELY  | full updates, sponsor brief, 1:1 cadence, in decisions
  KEEP SATISFIED  | exec-summary monthly, escalations only, in decisions affecting them
  KEEP INFORMED   | standup access, weekly status, channel access, in design reviews
  MONITOR         | channel access only, no required syncs
```

### Recipe 2: Stakeholder DB schema (Notion)
```yaml
Database: "Stakeholders — [Project]"
Properties:
  Name:                  title
  Role:                  rich_text
  Org:                   select        # internal / customer / vendor / partner
  Power:                 select        # High / Medium / Low
  Interest:              select        # High / Medium / Low
  Quadrant:              formula       # derived from P+I
  Info_needs:            multi_select  # Outcomes / Risks / Decisions / Budget / Schedule / Tech / Compliance
  Primary_channel:       select        # Email / Slack / Teams / 1:1 / Stand-up / Status report
  Frequency:             select        # Daily / Weekly / Biweekly / Monthly / On-event
  Cadence_notes:         rich_text
  Owner_for_comm:        person        # who from team owns this relationship
  Escalation_path:       rich_text
  Last_contact:          date
  Engagement_level:      select        # Champion / Supporter / Neutral / Skeptic / Blocker
```

### Recipe 3: Quadrant formula in Notion
```javascript
// Formula property — Quadrant
if(and(prop("Power") == "High", prop("Interest") == "High"), "MANAGE CLOSELY",
if(and(prop("Power") == "High", prop("Interest") == "Low"),  "KEEP SATISFIED",
if(and(prop("Power") == "Low",  prop("Interest") == "High"), "KEEP INFORMED",
"MONITOR")))
```

### Recipe 4: Comms plan template (markdown)
```markdown
# [Project] — Stakeholder Comms Plan

## Stakeholder matrix
| Stakeholder | Role | Power | Interest | Quadrant | Info needs | Channel | Frequency | Owner |
|---|---|---|---|---|---|---|---|---|
| Alice | VP Product (Sponsor) | High | High | Manage closely | Outcomes, decisions, RAG | 1-pg brief + 30-min 1:1 | Weekly Wed | PM |
| Bob | VP Eng | High | Med | Keep satisfied | Cross-team risks, hire asks | Email summary | Biweekly | PM |
| Carol | QA Lead | Med | High | Keep informed | Sprint progress, defect trend | Standup + Slack | Daily | PM |
| Dan | CFO | High | Low | Keep satisfied | Budget vs actual, contingency draws | Email + monthly steering | Monthly | PM |
| Eve | Design Lead | Med | High | Keep informed | Design reviews, blockers | Slack + design review | Weekly Tue | Design Lead |
| Frank | Customer Success Lead | Low | High | Keep informed | Launch comms, training | Slack channel + bi-weekly | Biweekly | PM |
| Grace | Legal | High | Low | Keep satisfied | Compliance, terms changes | Email, on-event | On-event | Legal Counsel |
| Hank | Sales Lead | Low | Med | Monitor | Launch date, talk-track | Channel only | On-event | Marketing |

## Cadence calendar
- **Monday standup** — team — 15min sync
- **Tuesday design review** — Eve + Design team + PM — 30min
- **Wednesday sponsor 1:1** — Alice + PM — 30min
- **Friday weekly status email** — all stakeholders — async
- **Monthly steering** — Alice + Bob + Dan + PM — 60min
- **On-event ad-hoc** — Grace, Hank, Frank per cadence

## Engagement strategy
- **Champions:** Alice, Eve — leverage for stage-gate sponsorship
- **Supporters:** Bob, Carol, Frank — keep informed; ask for cross-team unblock when needed
- **Neutrals:** Dan, Hank — provide just-enough; surface only on-need
- **Skeptics / Blockers:** [none currently] — flag immediately if any emerge
```

### Recipe 5: RACI matrix template
```markdown
# [Project] — RACI

Legend: R = Responsible (does the work) · A = Accountable (single throat) · C = Consulted (input) · I = Informed (kept aware)

| Activity / Deliverable | Sponsor | PM | Eng Lead | Design Lead | QA Lead | Legal |
|---|---|---|---|---|---|---|
| Charter sign-off | A | R | C | C | I | C |
| Sprint planning | I | A | R | C | C | — |
| Critical-bug triage | I | C | A | I | R | — |
| Design review sign-off | I | I | C | A | C | — |
| Budget contingency draw (≤$10k) | A | R | I | I | I | — |
| Budget contingency draw (>$10k) | A | R | C | C | C | C |
| Vendor SOW sign | A | C | I | I | I | R |
| UAT pass / fail | I | A | C | C | R | I |
| Launch go/no-go | A | R | C | C | C | C |
| Retro participation | I | A | R | R | R | — |
| Stakeholder status report | I | A,R | I | I | I | I |

Rule: every row has EXACTLY ONE A. Multiple R/C OK. Multiple A's = nobody accountable.
```

### Recipe 6: DACI variant for decision rights
```markdown
# Decision: <decision name>

Legend: D = Driver (owns getting decision made) · A = Approver (yes/no) · C = Contributors (input) · I = Informed

| Decision | Driver | Approver | Contributors | Informed |
|---|---|---|---|---|
| Methodology selection (waterfall/agile/hybrid) | PM | Sponsor | Eng Lead, Design Lead | Steering committee |
| Vendor selection | PM | Sponsor + Procurement | Eng Lead, Finance | Team |
| Scope-cut decisions | PM | Sponsor | Eng Lead, Design Lead, CSM | Team |
| Release-blocker triage | Eng Lead | PM | QA Lead, Design Lead | Sponsor |
```

### Recipe 7: Sponsor brief template (1-page weekly)
```markdown
# [Project] — Sponsor Brief — Week of [YYYY-MM-DD]

**TL;DR:** [1 sentence: status + 1 ask]

## RAG
🟢 Scope · 🟠 Schedule · 🟢 Budget · 🟢 Quality · 🟠 Risk

## Top-3 risks
1. R-007 — SSO cert renewal — Eng Lead — mitigation in flight
2. R-002 — Design capacity — PM — contractor PO pending sponsor sign
3. R-001 — Cross-team dep on auth — Eng Lead — buffer 2d

## Decisions needed THIS WEEK
- [ ] Approve $7k crash (3.1.3 + 2.2.2) for 5d schedule recovery — by Fri
- [ ] Sign contractor SOW for Design (Recipe 4 R-002) — by Wed

## What changed since last week
- Beta to 5 design partners shipped Tue (milestone hit)
- 2 risks moved to RED zone — both mitigation owners assigned

## Next week
- Beta feedback synthesis Wed
- Stage-gate G3 review Fri
```

### Recipe 8: Power-Interest visualization (Excalidraw 2×2)
```bash
mcp tool excalidraw.generate_diagram \
  --type "quadrant" \
  --xlabel "Power" --ylabel "Interest" \
  --cells '[
    {"x":"high","y":"high","label":"Alice (Sponsor)","color":"red"},
    {"x":"high","y":"med", "label":"Bob (VP Eng)","color":"amber"},
    {"x":"med", "y":"high","label":"Carol (QA Lead), Eve (Design)","color":"amber"},
    {"x":"high","y":"low", "label":"Dan (CFO), Grace (Legal)","color":"amber"},
    {"x":"low", "y":"high","label":"Frank (CSM)","color":"green"},
    {"x":"low", "y":"med", "label":"Hank (Sales)","color":"green"}
  ]'
```

### Recipe 9: Comms gap audit
```python
# audit.py — check every Power-High stakeholder has a comms entry
import json, sys

stakeholders = json.load(open("stakeholders.json"))
gaps = []
for s in stakeholders:
    if s["Power"] == "High":
        if not s.get("Frequency") or s["Frequency"] == "Monitor":
            gaps.append(f"{s['Name']} ({s['Role']}): High Power but Frequency={s.get('Frequency','MISSING')}")
        if not s.get("Owner_for_comm"):
            gaps.append(f"{s['Name']}: High Power but no Owner_for_comm")
        if not s.get("Last_contact"):
            gaps.append(f"{s['Name']}: High Power but never contacted")

if gaps:
    print("COMMS GAPS — fix before status meeting:")
    for g in gaps: print(f"  - {g}")
    sys.exit(1)
print("Comms plan complete — no Power-High gaps")
```

### Recipe 10: Engagement-level shift detection
```sql
-- Pseudo-SQL on the Stakeholder DB
-- Flag any stakeholder whose Engagement_level dropped from Champion/Supporter to Neutral/Skeptic/Blocker
SELECT name, prev_engagement, current_engagement, last_contact
FROM stakeholders
WHERE prev_engagement IN ('Champion','Supporter')
  AND current_engagement IN ('Neutral','Skeptic','Blocker')
ORDER BY current_engagement DESC;
```

### Recipe 11: Multi-channel comms plan (channel × stakeholder)
```csv
channel,stakeholder,frequency,owner,info_pushed
email,Alice,Weekly Fri,PM,Sponsor brief (1-page)
1:1_video,Alice,Weekly Wed,PM,Decisions + risks discussion
slack_channel,team,Daily,PM,Standup + ad-hoc
email,Dan,Monthly first-Mon,PM,Budget vs actual + EVM snapshot
status_archive_notion,all,Weekly,PM,Full status report
sponsor_brief,Alice,Weekly,PM,1-page TL;DR
steering_review,Alice+Bob+Dan,Monthly third-Wed,PM,RAG + decisions + portfolio
launch_comms,Frank+Hank,On-event,Marketing,Talk-track + dates
on-event_legal,Grace,On-event,Legal,Compliance changes
```

## Examples

### Example 1: Identify stakeholders at kickoff
**Goal:** 30 days to launch; haven't formally mapped stakeholders.

**Steps:**
1. Brainstorm full stakeholder list (PM solo, 15 min) — 14 names.
2. PM + Sponsor together: classify each on Power + Interest (Recipe 1).
3. Drop into Notion DB (Recipe 2) with Quadrant formula (Recipe 3).
4. Per quadrant, define info needs + channel + frequency (Recipe 4).
5. Run Recipe 9 audit → 2 High-Power gaps identified.
6. Sponsor 1:1 to close gaps; brief team.

**Result:** Live comms plan with 14 stakeholders mapped, weekly cadence on calendar.

### Example 2: Audit when stakeholder is surprised
**Goal:** CFO complained "I had no idea budget was tracking 8% over." Audit.

**Steps:**
1. Pull Stakeholders DB row for CFO → Frequency=Monthly, Channel=email.
2. Check Last_contact → 35 days (1 week stale).
3. Check sent emails for budget content → 2 in last 60d but no variance call-out.
4. Root cause: comms plan said "budget" but template didn't include EVM until W4.
5. Fix: add EVM snapshot to monthly CFO email (Recipe 11 update); send immediate catch-up brief.

**Result:** Gap closed; comms plan updated; antipattern noted in lessons-learned.

## Edge cases / gotchas

- **Power ≠ seniority.** A junior employee with veto power on something (e.g., compliance lead) has High Power on that decision. Score per project.
- **Interest changes over time.** Stakeholders inflate Interest near launch + decline post-launch. Re-score at each stage-gate.
- **Champions can become skeptics.** Track Engagement_level deltas; intervene early (Recipe 10).
- **"Inform everyone" = inform nobody.** Mass-CC kills signal. Tailor info to needs per quadrant.
- **Sponsor in two quadrants?** No — sponsor is always Manage Closely. If not, recharter.
- **Stakeholders external to org.** Vendors, partners, customers, regulators count. Don't omit.
- **One A per RACI row.** Two A's = nobody accountable. Three I's per row is fine, but every row needs an A.
- **RACI vs DACI vs DRI.** RACI for ongoing activities; DACI for one-shot decisions; DRI for ownership in async organizations. Pick one frame per project.
- **Cadence drift.** "Weekly" becomes "when I get to it." Schedule recurring + automate.
- **Time-zone hygiene.** Multi-region projects: schedule 1:1s in stakeholder's TZ; send async status pre-EOD-stakeholder-Friday.
- **Sponsor brief != full status.** 1-pager (Recipe 7) for sponsor; full report for archive. Don't reverse.
- **Legal/compliance stakeholders.** Often Low Interest but veto power = High Power. Easy to under-engage; over-correct by including on-event.
- **Engagement_level scoring is judgment.** Calibrate quarterly. Skeptic ≠ bad; skeptics surface risks. Blocker = action needed.
- **Comms plan is a living doc.** Re-review at every stage-gate + after any sponsor / steering change.

## Sources

- [PMI stakeholder management engagement](https://www.pmi.org/learning/library/stakeholder-management-engagement-influence-10072)
- [Atlassian RACI chart guide](https://www.atlassian.com/work-management/project-management/raci-chart)
- [Atlassian DACI framework](https://www.atlassian.com/team-playbook/plays/daci)
- [Mendelow Power-Interest grid (original)](https://www.bookmanagement.com/stakeholder-mapping/)
- [PMBOK 7th Edition: Stakeholder performance domain](https://www.pmi.org/standards/pmbok)
- [Smartsheet stakeholder analysis](https://www.smartsheet.com/free-stakeholder-analysis-templates-excel)
- [DRI convention (Apple)](https://www.atlassian.com/blog/teamwork/directly-responsible-individuals)
