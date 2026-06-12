<!--
Source: https://www.userevidence.com/
SlapFive: https://www.slapfive.com/
Influitive: https://influitive.com/
ReferenceEdge / Point of Reference: https://www.point-of-reference.com/
role.md customer reference + analyst-relations playbooks: internal
-->
# Customer Reference Program for PR — UserEvidence + SlapFive + Influitive — SKILL

Customer reference program purpose-built for PR: Notion reference DB + UserEvidence (survey-based proof points, AI-attested) + SlapFive (customer marketing platform, story library) + Influitive (advocate community + reference orchestration). Tag-match references to journalist beats + analyst inquiries + sales pursuits. Permission-tier discipline: named / industry / anonymous / no-quote.

## When to use this skill

- **Match journalist beat to a reference** — reporter pitch asks for a "fintech CFO using AI" → query Notion DB for tagged customers.
- **Build a Magic Quadrant / Wave reference list** — analyst requires 5-15 customer interviews; pull pre-cleared references.
- **Customer case study production** — interview transcript → one-page case study draft via Claude → permission-cleared.
- **Awards application customer proof** — Inc 5000 / Fast Co MIC / G2 awards often require customer testimonials.
- **Press release customer quote** — embargo'd launches with named customer attribution.
- **Co-authored thought leadership** — exec + customer joint LinkedIn newsletter or Substack post.
- **Survey-based proof points** — UserEvidence-style attested data ("87% of customers report X improvement, AI-verified").

**Do NOT use this skill when:**
- The ask is sales-only reference (no media/analyst) — defer to `sales-agent` / sales ops.
- The ask is internal customer success — defer to `customer-success-agent`.
- The customer hasn't signed a reference agreement — STOP, get permission FIRST.

## Setup

### UserEvidence

```bash
# https://www.userevidence.com — survey-based AI-attested customer proof points
# Pricing: plans typically $20K-$60K/yr
export USEREVIDENCE_API_KEY="<key>"
export USEREVIDENCE_API_BASE="https://api.userevidence.com/v1"
export USEREVIDENCE_ORG_ID="<id>"
```

UserEvidence runs survey campaigns to customer base → AI-verifies + extracts attested proof points + auto-generates content tiles, social cards, sales slides. Solves "where's the data" gap during PR/sales asset creation.

### SlapFive

```bash
# https://www.slapfive.com — customer marketing platform
# Pricing: ~$30K-$80K/yr
export SLAPFIVE_API_KEY="<key>"
export SLAPFIVE_API_BASE="https://api.slapfive.com/v2"
```

SlapFive = customer story library + advocate management. Strong on collecting + curating story content + matching stories to use cases.

### Influitive

```bash
# https://influitive.com — advocate community + reference orchestration
# Pricing: ~$30K-$100K/yr
export INFLUITIVE_API_KEY="<key>"
export INFLUITIVE_API_BASE="https://api.influitive.com/v1"
```

Influitive = gamified advocate community (challenges, points, rewards) + reference request orchestration. Best for orgs with 50+ active advocates.

### ReferenceEdge / Point of Reference (Salesforce-native alternates)

If org is Salesforce-heavy: ReferenceEdge / Point of Reference embed reference DB directly in SFDC + AE workflow.

### Notion customer reference DB schema

Per reference:
- `customer_id` (text)
- `company_name` (text)
- `vertical` (multi-select: SaaS, fintech, healthcare, retail, education, gov, etc.)
- `company_size` (select: SMB, mid-market, enterprise)
- `region` (multi-select: US, EU, UK, APAC, LatAm)
- `use_case_tags` (multi-select)
- `executive_contact` (text — name + title + email + phone)
- `comms_buyer` (text — internal champion who approved reference)
- `permission_level` (select: named_logo+quote, named_logo_only, industry_only, anonymous, no_press)
- `permission_signed_date` (date)
- `permission_expires_date` (date)
- `outcomes_quantified` (rich text — e.g., "47% reduction in time-to-close")
- `outcomes_qualitative` (rich text)
- `prior_press_history` (multi-text — previous coverage / quotes)
- `prior_analyst_briefings` (multi-text — Gartner/Forrester/IDC dates)
- `last_used_for_reference_date` (date)
- `usage_cooldown_until` (date — auto-set 30-90 day cooldown post-use)
- `case_study_url` (URL)
- `userevidence_attestation_id` (text)
- `slapfive_story_id` (text)
- `influitive_advocate_id` (text)
- `journalists_introduced_to` (multi-text — log of warm intros)
- `analyst_interviews_completed` (multi-text — log)

## Common recipes

### Recipe 1: Match journalist beat to reference

```bash
# Journalist beat: "fintech, AI/ML, mid-market CFO"
# Pull matching customers

journalist_beats='fintech,AI/ML'
journalist_persona='CFO'
journalist_company_size='mid-market'

matches=$(notion-mcp query --db customer_references \
  --filter "
    vertical IN ($journalist_beats) AND
    company_size = '$journalist_company_size' AND
    permission_level IN ('named_logo+quote','named_logo_only') AND
    (last_used_for_reference_date IS NULL OR usage_cooldown_until < TODAY())
  " \
  --sort "outcomes_quantified DESC")

echo "$matches" | jq '.[] | {
  company_name, executive_contact, outcomes_quantified, 
  permission_level, prior_press_history
}'
```

### Recipe 2: Cleared-customer warm intro draft

```python
# Don't send journalist directly to customer; pitch to internal champion first

match = notion_mcp.query_one(filter=...)

intro_draft = claude.generate(prompt=f"""
Warm-intro draft to internal champion {match['comms_buyer']} re: {match['company_name']} 
serving as media reference for {journalist['outlet']}.

Reporter background: {journalist['name']}, {journalist['title']}, {journalist['outlet']}.
Recent articles: {journalist['recent_articles']}.

Story angle: {story_angle}.

Champion's history with us: {match['prior_press_history']}.
Permission level: {match['permission_level']}.

Draft email under 200 words. Acknowledge the cooldown / their time.
Frame as opportunity, not ask. Specify exactly what's needed
(15-min call OR written quote OR named in release).
""")

# Send to internal champion FIRST; once approved, then to customer exec
gmail_mcp.send(
    to=match['comms_buyer'],
    subject=f"Quick: {match['company_name']} as media reference for {journalist['outlet']}?",
    body=intro_draft,
)
```

### Recipe 3: Permission tier discipline

```yaml
permission_levels:
  named_logo+quote:
    - logo in press release / on website / in social
    - attributed quote in press release with name + title
    - 1:1 interview with reporter on-record
    - ok for analyst report references
    - awards application proof
    
  named_logo_only:
    - logo in press release / on website / customer carousel
    - NO attributed quote without separate per-instance permission
    - ok in aggregated case study landing page
    
  industry_only:
    - "a Fortune 500 financial services company..."
    - no company name disclosed
    - aggregated proof points only
    
  anonymous:
    - "one of our enterprise customers..."
    - no identifying details
    - usage for stats only (no narrative)
    
  no_press:
    - sales-internal reference only
    - do NOT cite to press / analyst / public materials
```

Enforce in tooling: querying by permission_level filters out reference categories that don't match the use case.

### Recipe 4: UserEvidence survey campaign for proof points

```bash
# Launch survey to verify quantified outcomes for a use case
curl -X POST "$USEREVIDENCE_API_BASE/campaigns" \
  -H "Authorization: Bearer $USEREVIDENCE_API_KEY" \
  -d '{
    "name": "Q3 2026 ROI Survey: Customer Acquisition Cost",
    "audience": "customers_using_feature_x_for_6mo_plus",
    "questions": [
      {
        "type": "metric",
        "prompt": "By what percentage did your CAC change after adopting Acme?",
        "validate": "ai_attestation"
      },
      {
        "type": "open_quote",
        "prompt": "Describe the impact in 1-2 sentences. Quote may be used in marketing.",
        "permission_required": "named_quote"
      }
    ],
    "incentive": "$50 amazon gc per response",
    "target_responses": 50
  }'

# UserEvidence auto-generates attested content tiles
# Each tile = AI-verified proof point with customer name + attribution
# Pull into PR release / sales deck / awards submission

curl "$USEREVIDENCE_API_BASE/campaigns/$CAMPAIGN_ID/attestations" \
  -H "Authorization: Bearer $USEREVIDENCE_API_KEY" \
| jq '.attestations[] | {
    customer_name, metric, value, quote, attestation_url,
    permission_for_pr: .permissions.pr_use_approved
  }'
```

UserEvidence's value: AI-attested means the proof point has a verifiable provenance chain → defensible in legal / regulatory contexts where "X% improvement" claims need backing.

### Recipe 5: SlapFive story library curation

```bash
# Pull all stories tagged for current PR campaign
curl "$SLAPFIVE_API_BASE/stories?\
tags=ai,enterprise,roi&\
status=approved&\
permission=public" \
  -H "X-API-Key: $SLAPFIVE_API_KEY" \
| jq '.stories[] | {
    customer_name, headline, body, vertical, use_case_tags,
    media_assets: .assets[].url,
    permission_level
  }'

# Filter to high-fit stories for upcoming launch
# Hand off to press release / blog / sales deck per channel
```

### Recipe 6: Influitive advocate community + reference request

```bash
# Influitive advocates have opted in to be available for references
# Create challenge to find advocates interested in this specific journalist

curl -X POST "$INFLUITIVE_API_BASE/targets" \
  -H "X-API-Key: $INFLUITIVE_API_KEY" \
  -d '{
    "title": "15-min interview with TechCrunch on AI adoption",
    "description": "Reporter writing about mid-market CFOs adopting AI. Looking for 3 customers willing to share 15 min on-record. Logo + name + title attribution.",
    "filters": {
      "vertical": "fintech",
      "title_contains": "CFO",
      "company_size": "mid-market"
    },
    "incentive_points": 500,
    "deadline_days": 5
  }'

# Advocates self-select; reduces friction vs cold-pull from DB
# Best when org has 100+ active Influitive advocates
```

### Recipe 7: Customer interview → case study draft

```python
# Customer agrees to 30-min interview
# Record via zoom-mcp; pull transcript via youtube-mcp-transcript or zoom transcript

transcript = zoom_mcp.get_meeting_transcript(meeting_id)

case_study = claude.generate(prompt=f"""
Generate a one-page case study from this customer interview transcript.

Structure:
- Customer: name, vertical, size
- Challenge: 80 words
- Solution: 80 words  
- Results: 3 quantified outcomes (use customer's words from transcript)
- Quote: pull 1 strong quote from transcript verbatim (do NOT paraphrase quotes)

Permission level: {permission_level}.
If named_logo_only: redact name from quotes but keep company name in heading.
If industry_only: replace company name with "a Fortune 500 financial services company".

Transcript: {transcript}
""")

# Output to docx for customer approval
docx_skill.render(template="case_study.docx", content=case_study, output="draft.docx")

# Send to customer champion for approval BEFORE any external use
gmail_mcp.send(
    to=customer_champion_email,
    subject=f"Draft case study for your review — {company_name}",
    body="Per our conversation. Please review and flag anything to change.",
    attachments=["draft.docx"]
)
```

### Recipe 8: Analyst reference orchestration (Magic Quadrant / Wave)

```python
# Gartner / Forrester typically require 5-15 customer interviews per vendor
# Pre-clear references; brief them on analyst's question framework

mq_requirements = {
    "analyst_firm": "Gartner",
    "report_name": "MQ for AI Sales Platforms",
    "lead_analyst": "Jane Smith",
    "interview_count_required": 12,
    "vertical_mix": ["SaaS", "fintech", "healthcare", "retail"],
    "geo_mix": ["US", "EU", "APAC"],
    "company_size_mix": ["mid-market", "enterprise"],
    "interview_window": "2026-07-15 to 2026-08-15"
}

# Query Notion for matching references
candidates = notion_mcp.query(
    filter="""
    permission_level IN ('named_logo+quote','named_logo_only') AND
    vertical IN ({mq_requirements['vertical_mix']}) AND
    region IN ({mq_requirements['geo_mix']}) AND
    company_size IN ({mq_requirements['company_size_mix']}) AND
    (last_used_for_reference_date IS NULL OR usage_cooldown_until < TODAY())
    """
)

# Brief each candidate on Gartner's typical questions BEFORE interview
for customer in candidates[:15]:
    brief = claude.generate(prompt=f"""
    Brief {customer['executive_contact']} on Gartner MQ customer reference interview.
    
    What to expect:
    - 30-45 min call with {mq_requirements['lead_analyst']}
    - Open-ended product use questions (not script)
    - Honesty matters more than positivity
    - May ask about competitors evaluated
    - May ask about gaps / criticisms
    - Will be cited (anonymously by default) in MQ scorecard
    
    Our product capabilities the analyst will probe:
    {product_capability_summary}
    
    Don't coach toward specific answers. Encourage candid feedback.
    """)
    
    gmail_mcp.send(to=customer['executive_contact'], body=brief, ...)
    notion_mcp.update(customer['customer_id'], analyst_interviews_completed=[{
        "firm": "Gartner",
        "report": mq_requirements['report_name'],
        "scheduled_date": interview_date,
        "status": "briefed"
    }])
```

### Recipe 9: Cooldown enforcement

```python
# Don't burn out customer goodwill by over-asking
# Auto-set cooldown post-use: 30 days for quick quote, 60 days for interview, 90 days for analyst

def use_reference(customer_id, use_type):
    cooldown_days = {
        "quote_in_release": 30,
        "press_interview": 60,
        "analyst_interview": 90,
        "case_study_video": 120,
    }[use_type]
    
    notion_mcp.update(
        customer_id,
        last_used_for_reference_date=TODAY(),
        usage_cooldown_until=TODAY() + timedelta(days=cooldown_days),
    )

# Query that respects cooldown
available = notion_mcp.query(
    filter="""
    permission_level NOT 'no_press' AND
    (last_used_for_reference_date IS NULL OR usage_cooldown_until < TODAY())
    """
)
```

### Recipe 10: Awards customer testimonial pull

```bash
# Inc 5000 / Fast Co MIC / G2 awards often request customer testimonials
# Pull approved testimonials from UserEvidence / SlapFive / Notion

testimonials=$(notion-mcp query --db customer_references \
  --filter "
    permission_level = 'named_logo+quote' AND
    outcomes_quantified IS NOT NULL
  " \
  --limit 10)

# Format for award submission
echo "$testimonials" | jq -r '.[] | 
  "**\(.company_name)** (\(.vertical), \(.company_size))\n" +
  "\"\(.outcomes_qualitative)\"\n" +
  "— \(.executive_contact)\n\n" +
  "Quantified: \(.outcomes_quantified)\n"
'
```

## Examples — full customer reference program

```yaml
day_1_setup:
  - notion customer_references DB initialized
  - userevidence account; first survey targeting 6mo+ customers
  - slapfive (if budget) for story library
  - influitive (if budget + 100+ advocates) for community
  - sales ops + cs sync on initial 20-30 references seeded into DB
  - permission agreement templates (logo+quote, logo_only, industry_only, anonymous) created in vault

ongoing_cadence:
  weekly:
    - new customers achieving milestone outcomes → invite to reference program (gmail-mcp + perm signing flow)
    - userevidence pulse survey to active customers
    - dedupe + tag-cleanup in notion DB
  
  monthly:
    - new case study production (1-2/month)
    - story library refresh in slapfive
    - cooldown expiry review (notify champions of customers becoming available again)
    - influitive challenges for upcoming PR/analyst needs
  
  quarterly:
    - permission re-confirmation for customers approaching 1yr+ in DB
    - DB audit: tag drift, stale outcomes, exec departures
    - reference utilization report: which customers used N times, who's overused, who's underutilized

journalist_pitch_workflow:
  - pr lead pitches story
  - matching customers queried from notion DB (recipe 1)
  - cold-pull blocked if cooldown active or permission missing
  - warm intro via internal champion (recipe 2)
  - customer agrees → schedule via google-calendar-mcp
  - log to notion: journalists_introduced_to + new cooldown set
  - post-interview: thank-you note + send the published article when live

analyst_workflow:
  - mq/wave submission requires 5-15 references
  - query notion for vertical/geo/size mix (recipe 8)
  - brief each customer on analyst's typical questions
  - schedule interviews via google-calendar-mcp
  - track completion in notion analyst_interviews_completed
  - post-publication: share results back with customer references
```

## Edge cases

### Permission expiry
Customer signs reference permission for 1-year window; track expiry in `permission_expires_date`. Auto-flag at 60 days before expiry for renewal outreach. Using expired permission = legal + relationship risk.

### Exec departure
Customer champion leaves → reference permission may be void. Quarterly DB audit: check via LinkedIn or Common Room signals if exec has changed companies. If yes: re-request permission from successor or downgrade to industry_only.

### Cooldown violations damage relationships
Asking a customer for 4th media reference in 90 days burns the relationship. Enforce cooldown via tooling, not just policy. PR lead override should require explicit re-permission confirmation from the customer.

### UserEvidence AI attestation vs SOC 2
UserEvidence attestations include audit-defensible provenance chain. This matters for B2B SaaS regulated-industry buyers (financial services, healthcare) who require defensible data. "Claimed 47% improvement" without attestation = legal risk in some categories.

### SlapFive vs UserEvidence overlap
SlapFive = story library curator. UserEvidence = survey-based proof-point factory. Use both:
- SlapFive for narrative case studies + media assets
- UserEvidence for quantified attested proof points

Some orgs run only one. UserEvidence is better for proof points; SlapFive is better for stories.

### Influitive advocate fatigue
Gamified advocate communities work for ~12-18 months before participation drops. Refresh challenges + rewards + content regularly. Influitive ROI depends on 100+ active advocates; smaller orgs see diminishing returns.

### Anonymous references for analyst MQ
Gartner / Forrester typically anonymize customer references in published reports — but vendor briefer knows which customer said what. Customer can be "named" to analyst even when permission_level is `industry_only`. Permission only governs PUBLIC use.

### Competitor analyst references
A customer using both you + competitor might serve as reference for both. This is FINE — analysts probe for honest evaluations. Don't pressure customer to position one way; analyst spots it immediately.

### Customer asks for review of quote BEFORE press release publishes
Always honor. Standard practice: customer signs off on attributed quote within 48-72hrs of release. Failure to confirm = remove or paraphrase quote. Never assume "implicit approval."

### Net Promoter Score (NPS) doesn't qualify someone as reference
High-NPS customer ≠ willing reference. Confirm:
1. Permission to use as reference (signed agreement)
2. Comfort with PR (some prefer sales-only)
3. Specific use case alignment (NPS measures sentiment, not relevance)

### Tag taxonomy drift
Over 12-24 months, DB tags drift (5 variants of "fintech": "fintech", "Fintech", "FinTech", "financial services", "finance"). Quarterly cleanup. Define canonical tag taxonomy. Use Notion select fields (not free-text) to enforce.

### Hand-off to crisis comms
Customer reference may need RAPID retraction during crisis (e.g., customer ends contract publicly). Configure alert: if customer name appears in negative news → pause all PR uses of that reference + escalate to PR lead. Hand off pattern with `crisis-comms-24-48-72-hour-playbook`.

### Hand-off to analyst-relations
Magic Quadrant / Wave reference orchestration overlaps with `analyst-relations-gartner-forrester-idc`. Reference program owns the customer DB + permission tier; analyst skill owns the briefing + survey + interview orchestration.

### Hand-off to thought leadership
Customer co-authored content (LinkedIn newsletter, Substack post) requires reference DB entry + permission_level confirmation. Hand off draft to `executive-thought-leadership-linkedin-substack` once customer approves participation.

### Hand-off to press release skill
Quote in press release uses references that confirm `permission_level = named_logo+quote`. Hand off to `press-release-writing-distribution` with quote text + customer info; that skill handles the embargo + 48hr customer sign-off requirement.

### International references + GDPR
EU customer reference data subject to GDPR. Permission_agreement must include explicit consent for cross-border data use if reference will be cited globally. Stricter than US. Defer to legal for EU/UK reference templates.

### CRM sync (Salesforce / HubSpot)
Sales already has reference logs in SFDC / HubSpot for sales-internal use. Sync to Notion via `cli-anything` curl on schedule. Avoid duplicate sources of truth — PR DB = subset of sales DB filtered for media/analyst permission.

## Sources

- **UserEvidence (survey-based AI-attested proof points)**: https://www.userevidence.com/
- **UserEvidence platform overview**: https://www.userevidence.com/platform
- **SlapFive (customer marketing platform)**: https://www.slapfive.com/
- **SlapFive product**: https://www.slapfive.com/product
- **Influitive (advocate community)**: https://influitive.com/
- **Influitive API**: https://influitive.docs.apiary.io/
- **Point of Reference (SFDC-native)**: https://www.point-of-reference.com/
- **Gartner MQ customer reference methodology**: https://www.gartner.com/en/research/methodologies/magic-quadrants-research
- **G2 customer reference best practices**: https://learn.g2.com/customer-references
- **role.md customer reference + analyst-relations playbooks**: internal `agent_bundle/agents/pr-comms/role.md`
