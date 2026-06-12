<!--
Sources:
ResearchOps Community — https://researchops.community
Kate Towsey — Research That Scales — https://www.amazon.com/Research-That-Scales-Operations-Function/dp/1959029037
User Interviews — Research Ops Guide — https://www.userinterviews.com/blog/what-is-research-operations
-->
# ResearchOps — Panel + Budget + Tool Stack — SKILL

Kate Towsey "Research That Scales" + ResearchOps Community playbook. Own the participant pool (consented panel + privacy + incentives), tool stack (Dovetail + Maze + UI + Lookback), and repository taxonomy. Budget per quarter; SLA per request; intake form for ad-hoc.

## When to use

- Setting up a ResearchOps function from scratch.
- Designing the participant panel + recruitment infrastructure.
- Quarterly budget planning + tool stack review.
- Building intake form + SLA + escalation paths.
- Compliance review (GDPR / CCPA / PCI).

Trigger phrases: "set up ResearchOps", "panel management", "research budget", "intake form", "Kate Towsey", "tool stack matrix".

## Setup

```bash
# Notion for wiki + intake form + tool stack
curl -fsSL "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28"

# User Interviews / Respondent / dscout panel admin endpoints
# See recruit-user-interviews-respondent-dscout skill

# Spreadsheet for budget tracking (or finance system via cli-anything)
```

## Common recipes

### Recipe 1: The 4 ResearchOps pillars (Towsey)

```markdown
# 4 pillars

## 1. Participants
- Owned panel of consented users
- Privacy + GDPR compliance
- Incentive workflow (auto-pay)
- Anti-fatigue rules (max N studies per quarter per participant)

## 2. Process
- Intake form (templated request)
- Triage SLA
- Stages: Plan → Recruit → Run → Synthesize → Publish

## 3. Tools
- Repository: Dovetail / Notably / Marvin
- Recruit: User Interviews / Respondent / dscout / Prolific
- Test: Maze / UserTesting / Lyssna / Lookback
- IA: Optimal Workshop / UXtweak
- Synthesis: Dovetail + Hugging Face (clustering)

## 4. Knowledge
- Research repository (atomic UX research model)
- Persona library
- Journey maps
- Insights linked to PRDs + Linear
```

### Recipe 2: Build intake form (Notion)

```markdown
# Research Intake Form

## Requester
- Name + role + team
- Date

## The decision
- What decision will this research inform?
- Who owns the decision?
- When does the decision need to be made?

## Research questions
- What are you trying to learn? (≤5 questions)

## Sample
- Who? (segment + behavior)
- How many?
- Existing customers or external?

## Timeline
- When do you need the readout?

## Pre-existing context
- What research already exists on this topic?
- Why isn't existing research enough?

## Budget
- Confirmed budget for incentives + tools

## Outputs
- Notion readout + Dovetail insights + Linear handoff?
```

### Recipe 3: Triage SLA

```markdown
# Triage SLA (researcher response time)

| Request type | Triage SLA | Lead time |
|---|---|---|
| Strategic study (multi-week) | 2 business days | 4-8 weeks |
| Tactical study (1-2 weeks) | 1 business day | 2-3 weeks |
| Ad-hoc consult (Office hours) | Same week | 1 day |
| Insight library query | Same day | 30 min |
| Recruit-only support | 2 business days | 1-2 weeks |
| Accessibility study | 2 business days | 4 weeks |

## Triage outputs
- Accept / pair / reject (with reason)
- Estimated effort + timeline
- Assigned researcher
- Decision-owner sign-off scheduled
```

### Recipe 4: Build the owned panel

```python
# Panel CRM in Notion or HubSpot
panel_schema = {
    "participant_id": "string",
    "consent_date": "date",
    "consent_version": "string",  # for re-consent on change
    "segment": "select",  # founder, PM, designer, etc.
    "demographics": "select",
    "company_stage": "select",
    "tool_usage": "multi_select",
    "last_studied_date": "date",
    "studies_count_this_quarter": "number",
    "studies_total": "number",
    "honorarium_total": "number",
    "satisfaction_avg": "number",  # post-session rating
    "right_to_withdraw": "boolean",
    "do_not_recruit_until": "date",
    "tags": "multi_select"
}

# Anti-fatigue rules
def can_recruit(participant):
    return (
        participant["studies_count_this_quarter"] < 2
        and (today() - participant["last_studied_date"]).days > 60
        and participant["do_not_recruit_until"] < today()
    )
```

### Recipe 5: Incentive workflow

```markdown
# Incentive workflow

## Standard rates (2026)
- Consumer 30-min: $50
- Consumer 60-min: $100
- B2B mid 60-min: $150
- B2B senior 60-min: $200-400
- B2B C-suite 60-min: $400-1000
- Accessibility study: above-standard +25%
- Diary study (14-day): $500-1000

## Payment cadence
- Pay within 48h of session
- Auto-trigger via Tremendous / Bonusly / Amazon GC API
- Track in spreadsheet + finance log

## Anti-shame
- "Sorry for the wait" → loses panel trust
- Late payment = future no-show + reputation hit
```

### Recipe 6: Tool stack matrix

```markdown
# Tool stack — by category

## Repository
- **Primary:** Dovetail ($199/mo+)
- **Alt:** Notably (free), Marvin (AI-first)
- **Notes:** Repository is the spine; never compromise here

## Recruit
- **B2C/B2B fast:** User Interviews
- **B2B specialist:** Respondent
- **Mobile / diary:** dscout
- **Academic / survey:** Prolific
- **Accessibility:** Fable
- **In-product intercept:** Ethnio

## Test
- **Moderated:** Lookback (or Zoom + Otter)
- **Unmoderated:** Maze (Figma) / UserTesting (enterprise) / Lyssna (design)
- **IA:** Optimal Workshop (Treejack + OptimalSort + Chalkmark)
- **Surveys:** Sprig (event-trigger) / Survicate (multi-channel) / Typeform (long-form)

## Analytics + replay
- **Replay:** FullStory / LogRocket / Hotjar / Clarity (free)
- **Behavioral:** PostHog / Mixpanel / Amplitude

## Synthesis
- **Tag + cluster:** Dovetail
- **Embedding cluster (high vol):** Hugging Face

## Total tool spend (typical)
- Small team (1 researcher): $400-800/mo
- Mid team (3 researchers): $1500-3000/mo
- Enterprise: $5000+/mo
```

### Recipe 7: Quarterly budget template

```markdown
# Quarterly research budget

## Tool spend (subscription)
- Dovetail: $199 × 3 = $597
- User Interviews: $300 × 3 = $900
- Maze: $99 × 3 = $297
- Lookback: $100 × 3 = $300
- Optimal Workshop: $166 × 3 = $498
- Otter: $20 × 3 = $60
- **Subtotal:** $2652

## Incentives (per study × studies/quarter)
- 4 moderated rounds × 5 × $100 = $2000
- 2 unmoderated rounds × 30 × $20 = $1200
- 1 diary study × 12 × $500 = $6000
- 2 NPS analyses (no recruit) = $0
- **Subtotal:** $9200

## Panel platform fees (per recruit)
- User Interviews recruit fee × 25 = $625
- Respondent recruit fee × 8 × $50 = $400
- **Subtotal:** $1025

## Contractor / agency
- Accessibility specialist day rate × 2 days = $3000

## Total quarterly: $15,877
```

### Recipe 8: Compliance + privacy checklist

```markdown
# Per-study compliance checklist

## Before recruit
- [ ] Consent language matches latest version
- [ ] Recording consent explicit
- [ ] Data retention period stated
- [ ] Right to withdraw clause
- [ ] GDPR / CCPA / PIPEDA considerations per region

## During study
- [ ] Recording stored in compliant location (Dovetail SOC 2)
- [ ] PII minimized in transcripts
- [ ] No sensitive data screen capture without explicit consent

## After study
- [ ] Honorarium paid within 48h
- [ ] Data retained per policy; auto-delete scheduled
- [ ] Participant withdrawal request → full erasure flow
- [ ] No DM to participants outside platform without consent

## Annual
- [ ] Re-consent panel members on policy changes
- [ ] Audit tool vendor SOC 2 / ISO 27001 status
- [ ] DPA (Data Processing Agreement) on file with each vendor
```

### Recipe 9: Repository governance

```markdown
# Repository governance

## Tag taxonomy
- Owned by ResearchOps lead
- Quarterly review + cleanup
- Tag additions require approval (prevent sprawl)

## Insight library curation
- Researcher publishes; ResearchOps lead reviews
- "Featured insights" rotated quarterly (highlights for org)
- Stale insights marked deprecated annually

## Persona governance
- Researcher authors; ResearchOps lead reviews
- Quarterly refresh check
- Retirement when segment changes or unstudied >18 months

## Documentation
- Public to org (Notion read access)
- Tool credentials in 1Password / Vault
- Vendor contracts + SLAs documented
```

### Recipe 10: Office hours + Slack ops

```markdown
# Day-to-day ops

## Office hours (see research-democratization-training)
- Weekly 60-min block
- 4 × 15-min slots
- Calendly signup

## Slack channels
- #user-research (broadcasts + insights)
- #user-research-help (PM/designer questions)
- #research-ops (internal)
- #panel-recruit (recruit comms)

## Cadence
- Daily: monitor Slack help channel
- Weekly: office hours + insight broadcast
- Monthly: research showcase lunch-and-learn
- Quarterly: budget review + tool stack review + repository governance
```

## Examples

### Example 1: Stand up ResearchOps function
**Goal:** Build ResearchOps from scratch for a Series B team.

**Steps:**
1. Document 4 pillars (Recipe 1).
2. Build intake form (Recipe 2).
3. Define SLA (Recipe 3).
4. Set up owned panel (Recipe 4).
5. Incentive workflow (Recipe 5).
6. Tool stack + budget (Recipes 6-7).
7. Compliance checklist (Recipe 8).
8. Repository governance (Recipe 9).
9. Office hours + Slack (Recipe 10).

**Result:** Researcher-able org with consistent quality + governance.

### Example 2: Quarterly review + tool stack rationalization
**Goal:** Reduce tool spend while maintaining quality.

**Steps:**
1. Audit current spend (Recipe 7).
2. Tool consolidation candidates (e.g., Lyssna for IA + 5-sec; drop Optimal Workshop).
3. Cost-benefit per tool.
4. Negotiate annual contracts with usage commitment.

**Result:** Sustainable tool stack with clearer ROI.

## Edge cases / gotchas

- **Panel without consent management.** GDPR violation; risk legal exposure.
- **Honorarium late.** Panel trust evaporates; future no-shows rise.
- **No intake form.** Ad-hoc requests overload researchers.
- **No SLA.** Stakeholders expect instant; reality bites.
- **Anti-fatigue ignored.** Same panel members in every study = professional respondent risk.
- **Repository as junkdrawer.** Without governance, becomes unsearchable in 6 months.
- **Vendor sprawl.** 12 tools = no one knows the stack. Consolidate to 6-8.
- **Compliance retrofit.** Build privacy in from day 1; retrofitting is painful + risky.
- **No backup researcher.** Single-point-of-failure on team.
- **Forgetting accessibility tooling.** axe-core / Fable budget often skipped first; mandatory.
- **No KPI on ResearchOps function.** Track: studies completed, time-to-recruit, repository searches, PRD citations, NPS of researcher service.
- **Quarterly review skipped.** Tools accumulate; budget grows.

## Sources

- [ResearchOps Community](https://researchops.community)
- [Kate Towsey — Research That Scales](https://www.amazon.com/Research-That-Scales-Operations-Function/dp/1959029037)
- [User Interviews — Research Ops Guide](https://www.userinterviews.com/blog/what-is-research-operations)
- [NN/g — ResearchOps](https://www.nngroup.com/articles/research-ops/)
- [Dovetail — Tag taxonomies](https://dovetail.com/blog/tag-taxonomy)
- [Tremendous API (incentives)](https://docs.tremendous.com)
- [GDPR overview](https://gdpr-info.eu/)
