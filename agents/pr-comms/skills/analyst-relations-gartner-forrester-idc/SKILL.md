<!--
Source: https://spotlightar.com/blog/gartner-magic-quadrant-steps/
Gartner methodology: https://www.gartner.com/en/research/magic-quadrant
Forrester Wave: https://go.forrester.com/research/wave-methodology/
IDC MarketScape: https://www.idc.com/research/services/marketscape
-->
# Analyst Relations — Gartner / Forrester / IDC — SKILL

Vendor-initiated briefings are FREE (per Gartner methodology). Pair with `pptx` skill for briefing deck. Track Magic Quadrant / Wave / MarketScape inclusion criteria in `notion-mcp`. Customer reference orchestration via `customer-reference-program-pr`. Quarterly briefing cadence + annual MQ/Wave submission cycle.

## When to use this skill

- **Quarterly analyst briefing program** — 4-8 analyst firms × 4 briefings/year per firm.
- **Magic Quadrant / Wave / MarketScape submission** — annual category report participation.
- **Analyst Peer Insights / vendor profile management** — Gartner Peer Insights + Forrester customer reference programs.
- **Pre-launch analyst pre-brief** — exclusive heads-up to lead analysts before public launch.
- **Strategic analyst coverage** — boutique firms (Constellation, GigaOm, 451 Research, ABI) where Gartner inclusion may be out of reach.

**Do NOT use this skill when:**
- The "analyst" is a financial analyst covering public stocks — defer to `investor-relations`.
- The opportunity is a press interview, not analyst briefing — use `journalist-outreach-cold-warm-embargoed`.
- The customer reference is for press placement, not analyst — use `customer-reference-program-pr` directly.

## Setup

### Analyst firm vendor portals

```yaml
gartner:
  portal: https://www.gartner.com/en/vendors
  briefing_request: https://www.gartner.com/en/vendors/briefings
  cost: free briefings; paid for Strategic Consulting
  scopes:
    - Magic Quadrant
    - Hype Cycle
    - Critical Capabilities
    - Peer Insights vendor profile

forrester:
  portal: https://go.forrester.com/research/become-a-forrester-vendor/
  briefing_request: https://www.forrester.com/contact/
  cost: free briefings; paid for analyst access subscriptions
  scopes:
    - Forrester Wave
    - Total Economic Impact (TEI) studies
    - New Wave (emerging categories)

idc:
  portal: https://www.idc.com/about/vendor
  cost: free briefings
  scopes:
    - MarketScape
    - MaturityScape
    - FutureScape

boutique:
  - Constellation Research (https://www.constellationr.com/)
  - GigaOm (https://gigaom.com/)
  - 451 Research / S&P Global (https://www.451research.com/)
  - ABI Research (https://www.abiresearch.com/)
  - Omdia (https://omdia.tech.informa.com/)
```

### Notion analyst DB schema

Per analyst:
- `firm` (select: Gartner, Forrester, IDC, Constellation, GigaOm, etc.)
- `analyst_name` (text)
- `analyst_title` (text)
- `coverage_area` (multi-select)
- `recent_research` (multi-text — links to last 5 reports)
- `briefing_history` (multi-text — past briefings with us)
- `last_briefing_date` (date)
- `next_briefing_planned` (date)
- `customer_refs_provided` (multi-text — references we've shared)
- `analyst_sentiment` (select: positive, neutral, mixed, negative)
- `outreach_status` (select: not-engaged, briefed, recurring, paying-client)
- `vendor_portal_id` (text)

### MQ / Wave / MarketScape tracking DB

Per report we're tracking:
- `firm` (select)
- `report_name` (text)
- `category` (text)
- `lead_analyst` (text)
- `co_authors` (multi-text)
- `last_published` (date)
- `next_expected` (date)
- `inclusion_criteria` (rich text)
- `application_deadline` (date)
- `customer_refs_required_count` (number)
- `customer_refs_provided` (multi-text)
- `briefing_completed` (checkbox)
- `survey_submitted` (checkbox)
- `interview_completed` (checkbox)
- `published` (checkbox)
- `our_placement` (text — e.g., Leader, Challenger, Visionary, Niche)

### pptx skill

For briefing decks (8-slide standard structure).

## Common recipes

### Recipe 1: Analyst landscape mapping (per category)

```bash
# Identify analysts covering your category
# 1. Gartner Peer Insights search
firecrawl scrape --url "https://www.gartner.com/reviews/market/<your-category>" \
| jq -r '.analyst_attribution[]'

# 2. Forrester category page
firecrawl scrape --url "https://go.forrester.com/research/categories/<your-cat>" \
| jq -r '.analysts[]'

# 3. IDC analyst directory
firecrawl scrape --url "https://www.idc.com/research/services?cat=<your-cat>"

# 4. LinkedIn search for "Gartner analyst <category>"
# 5. Recent research releases — pull author + topic

# Sync to Notion analyst DB
for a in $analysts; do
  notion-mcp upsert_page --db analysts --properties "$a"
done
```

### Recipe 2: Request vendor briefing (Gartner)

```bash
# Gartner: submit via vendor portal (no API)
mcp tool playwright-mcp.browser_navigate --url "https://www.gartner.com/en/vendors/briefings"

# Fill request form
# - Company: Acme Corp
# - Product: AI Infrastructure
# - Target analyst: [name]
# - Briefing topic: [proposed talking points]
# - Suggested dates: 3-4 options 4-8 weeks out
# - Duration: 30 min
# - Format: video conference

# Forrester
# Email arelations@forrester.com with same details

# IDC
# Submit via https://www.idc.com/about/contact (briefing form)

# Boutique firms: email directly to analyst
```

### Recipe 3: Briefing deck via pptx skill (8-slide standard)

```python
deck_content = {
    'slide_1': {
        'title': f'Acme Corp Briefing for {analyst["firm"]} ({analyst["name"]})',
        'date': briefing_datetime,
        'subtitle': 'AI Infrastructure Category Update'
    },
    'slide_2': {  # Company snapshot
        'founding': '2018, San Francisco',
        'employees': 240,
        'customers': 200,
        'funding': '$50M Series B (Sequoia, Jun 2026)',
        'revenue_range': '$10M-$25M ARR'
    },
    'slide_3': {  # Market position
        'we_play_in': 'AI infrastructure for enterprise',
        'we_compete_with': 'Vertex AI, SageMaker, niche AI platforms',
        'our_wedge': '10x faster fine-tuning + transparent token economics'
    },
    'slide_4': {  # Product overview
        'differentiators': [
            '1. Inference latency < 50ms at scale',
            '2. Transparent token-level cost attribution',
            '3. Per-customer fine-tuning at $/M tokens, not infra rental'
        ],
        'screenshots': [...]
    },
    'slide_5': {  # Customer proof
        'customers': [
            {'name': 'Acme Customer 1', 'use_case': '...', 'outcome': '60% cost reduction'},
            {'name': 'Acme Customer 2', 'use_case': '...', 'outcome': '3x dev velocity'},
            {'name': 'Acme Customer 3', 'use_case': '...', 'outcome': '99.9% uptime'},
        ]
    },
    'slide_6': {  # Roadmap (next 12 months at high level)
        'q3_2026': 'Multi-region failover GA',
        'q4_2026': 'Enterprise SSO + audit log',
        'q1_2027': 'Hybrid cloud / on-prem option (high-level only)',
        'q2_2027': 'Compliance certifications (FedRAMP, etc.)'
    },
    'slide_7': {  # Recent milestones
        'series_b': '$50M Sequoia-led, June 2026',
        'customer_wins': '+45 in Q2',
        'press': 'TechCrunch, The Information, Bloomberg coverage in Q2',
        'awards': 'Inc 5000 #847; Fast Co MIC AI category finalist'
    },
    'slide_8': {  # Q&A backup
        'common_questions': [
            'Pricing model details',
            'Customer geographic split',
            'Partnership strategy',
            'Hiring trajectory'
        ]
    }
}

pptx_mcp.render(template='analyst_briefing.pptx', content=deck_content, output=f'briefings/{analyst["firm"]}_{briefing_datetime}.pptx')
```

### Recipe 4: Briefing execution (30 min standard)

```yaml
30_min_briefing_agenda:
  0_5_min: introductions + agenda confirm
  5_10_min: company snapshot + market position (slides 2-3)
  10_20_min: product overview + customer proof (slides 4-5)
  20_25_min: roadmap + recent milestones (slides 6-7)
  25_30_min: Q&A (analyst-led)

15_min_followup_qa:
  - additional specifics analyst requests
  - customer reference offers
  - product demo (if analyst requests)
```

Record briefing via `zoom-mcp` (with analyst permission). Transcript for follow-up doc generation.

### Recipe 5: Follow-up within 24 hours

```bash
# Thank-you email + briefing summary + customer reference list
gmail-mcp send \
  --to "$analyst_email" \
  --subject "Acme briefing follow-up: $briefing_date" \
  --body "Hi $analyst_name,

Thanks for the 30 minutes today. Per your questions:

1. Customer references — I'll have these intros coordinated within 5 business days:
   - [Customer A — fintech vertical]
   - [Customer B — healthtech vertical]
   - [Customer C — retail vertical]

2. Product docs you requested:
   - [Attached: technical_overview.pdf]
   - [Attached: pricing_model.pdf]
   - [Attached: security_overview.pdf]

3. Topics for next briefing (suggested for Q4):
   - [Topic 1]
   - [Topic 2]

Happy to schedule the next briefing 12-16 weeks out.

— Maria
press-ar@acme.com"

# Log to Notion
notion-mcp update_row --filter "analyst=$analyst_name" \
  --last_briefing_date "$(date -I)" \
  --next_briefing_planned "$(date -d '+12 weeks' -I)" \
  --briefing_summary "..."
```

### Recipe 6: Magic Quadrant / Wave submission (annual cycle)

```bash
# When Gartner announces new MQ in your category:

# Step 1: Track inclusion criteria
firecrawl scrape --url "$mq_announcement_url" \
> mq_criteria.md

# Step 2: Check if we meet inclusion bar
prompt="Check Acme's eligibility for this MQ.

INCLUSION CRITERIA: $(cat mq_criteria.md)
ACME FACTS:
- ARR: $20M
- Customers: 200
- Regions: US + EU
- Years in market: 8

For each criterion, output ELIGIBLE / NOT ELIGIBLE / MARGINAL with reasoning."
eligibility=$(claude --prompt "$prompt")

# Step 3: If eligible, register intent via Gartner vendor portal
# Step 4: Complete vendor survey (often 100+ questions)
# Step 5: Provide 5-15 customer references for analyst interviews
# Step 6: Schedule analyst interview (1-2 hours, deep dive)
# Step 7: Submit by deadline
```

### Recipe 7: Customer reference orchestration (for MQ submission)

```python
# 5-15 customer references required for typical MQ submission
required_refs = 10
mq_criteria_for_refs = ['multi-region', 'production_scale', '12mo+_tenure', 'diverse_use_cases']

# Pull eligible refs from customer reference DB
candidates = notion.query(
    database='customer_references',
    filter={
        'press_permission': True,
        'analyst_briefing_willing': True,
        'tenure_months_gte': 12,
    }
)

# Diversify across criteria
selected = select_diverse(candidates, criteria=mq_criteria_for_refs, count=required_refs)

# Pre-brief each reference
for ref in selected:
    # Schedule briefing call
    google-calendar-mcp create_event \
        --title f"MQ ref prep: {ref['contact_name']} for Gartner interview" \
        --duration_min 45

    # Send prep doc
    gmail-mcp send \
        --to ref['contact_email'] \
        --subject "Gartner Magic Quadrant interview prep" \
        --body f"""
Hi {ref['contact_name']},

Gartner is interviewing customers for the {mq_name} report. We'd love to have you participate.

Time: 45 min, scheduled at your convenience
Format: Phone or Zoom with analyst
What they'll ask:
- Your use case + business outcome
- Decision criteria when you chose Acme
- Your experience with onboarding, support, product capability
- Comparison to alternatives you evaluated
- Areas of strength + areas for improvement

Pre-call prep doc: [attached, 1-pager]

Confirm time + I'll coordinate with the analyst's team.

Thanks for being part of this!
— Maria
"""
```

### Recipe 8: Post-publication amplification

```bash
# When MQ / Wave / MarketScape publishes
if [ "$our_placement" = "Leader" ] || [ "$our_placement" = "Strong Performer" ]; then
  # Press release (via press-release-writing-distribution)
  # CEO LinkedIn post
  # Twitter announcement
  # Update website analyst page
  # Sales enablement updated material
  # Customer reference outreach: "you helped get us here"

  press-release-skill draft --topic "$mq_name placement" --tier "T1"
  linkedin create_post --org $ORG_URN --text "..."
fi

# If lost / not included, learn:
# - Why? (gap in criteria? not enough customer refs?)
# - Iterate for next cycle
# - Consider boutique firm placement (GigaOm Radar, Constellation ShortList)
```

## Examples — annual analyst relations program

```yaml
quarterly_cadence:
  - 6-8 analyst briefings per quarter (across Gartner, Forrester, IDC, boutique)
  - each briefing: 4-6 weeks prep + 30-min briefing + 24-hr followup + customer refs as requested

annual_mq_wave_cycle:
  q1:
    - identify announced MQs / Waves in our category
    - check inclusion eligibility
    - submit briefing requests for lead analyst
    
  q2:
    - briefings completed
    - vendor survey drafted (often 100+ questions)
    - customer reference pre-brief begun
    
  q3:
    - vendor survey submitted by deadline
    - customer reference interviews scheduled with analyst
    - lead analyst follow-up calls
    
  q4:
    - MQ / Wave publication
    - amplification + sales enablement

quarterly_review:
  - per-analyst sentiment shift (positive / neutral / negative)
  - customer reference utilization rate
  - briefing-to-MQ-inclusion conversion
```

## Edge cases

### Briefings are FREE (per Gartner methodology)
Don't pay for briefings. Gartner sales reps may pitch "Strategic Consulting" — separate paid product. Vendor briefings themselves are free. Same Forrester, IDC.

### Below MQ inclusion bar?
Typical inclusion bar:
- Gartner MQ: $20M+ ARR, 100+ customers, 2+ regions
- Forrester Wave: $10M+ revenue, 50+ customers
- IDC MarketScape: varies

Below bar? Target:
- Hype Cycle mention (lower bar)
- Vendor Profile (mention without ranking)
- Boutique firm (Constellation ShortList, GigaOm Radar — lower bar, growing influence)

### Customer reference quality > quantity
5 strong references > 15 weak ones. Strong = multi-year tenure + production scale + multi-stakeholder usage + willing to speak candidly. Pre-brief each rigorously.

### Don't over-prep references
References that sound rehearsed are flagged. Brief on:
- What Gartner asks
- Time commitment
- Your role
DON'T scripted answers. Authentic perspective wins.

### Analyst sentiment shift detection
Quarterly: review what each analyst has published in your category. Sentiment shift = signal. If analyst's recent research starts citing your competitor more, time for a briefing.

### Don't argue with analysts
If MQ result is unfavorable, don't argue. Ask for written feedback ("can you share the specific gaps you observed?"). Use feedback to iterate. Public disputes over MQ placement damage relationship.

### Lead-analyst vs co-author dynamics
Lead analyst has 70% of the influence. Co-authors review + sign off. Focus briefing energy on lead. Co-author courtesy briefings (15-min) at follow-up.

### Boutique firm strategic value
Constellation, GigaOm, 451, ABI publish faster + with lower bar. Use:
- Year 1: boutique firm placement (Constellation ShortList, GigaOm Radar)
- Year 2-3: build to Gartner Cool Vendor or Hype Cycle
- Year 4+: MQ / Wave inclusion if scale supports

### Hand-off to investor-relations
If analyst coverage interacts with public-equity story (post-IPO), coordinate with `investor-relations` agent. Analyst report can move stock; SEC disclosure may apply.

### Recording briefings (with permission)
Always ask permission to record. Some firms decline. If allowed, `zoom-mcp` records + transcribes → feeds into briefing notes + sales enablement.

### Pre-announce product roadmap
Briefings allow more roadmap detail than press would. Standard:
- 0-6 months: public roadmap items only
- 6-12 months: high-level themes, no specific dates
- 12+ months: directional only

Brief NDA in place with analyst firms for sensitive material.

### Inquiry calls (paid)
Beyond free briefings, "inquiry calls" with Gartner clients allow vendor to be on the receiving end of customer questions. Paid service. Sales value: when a Gartner client researches your category, you can be the vendor they call.

### Customer reference burnout
Same customers shouldn't be tapped repeatedly. Rotate. Build a deep bench (30-50 willing customers) via `customer-reference-program-pr` skill.

### MQ position language discipline
Don't claim "Gartner Leader" in marketing unless your placement is in the Leaders quadrant. Gartner enforces aggressively. Use exact language they publish.

### Post-publication republishing rights
Analyst firm reports are copyrighted. Vendors can:
- Quote excerpts with attribution
- Link to firm's report URL
- License the full report (separate paid agreement)

Don't reproduce report verbatim.

## Sources

- **Spotlight AR Gartner MQ steps**: https://spotlightar.com/blog/gartner-magic-quadrant-steps/
- **Gartner Magic Quadrant methodology**: https://www.gartner.com/en/research/magic-quadrant
- **Gartner vendor briefings**: https://www.gartner.com/en/vendors/briefings
- **Forrester Wave methodology**: https://go.forrester.com/research/wave-methodology/
- **Forrester vendor program**: https://go.forrester.com/research/become-a-forrester-vendor/
- **IDC MarketScape**: https://www.idc.com/research/services/marketscape
- **Constellation Research**: https://www.constellationr.com/
- **GigaOm Radar**: https://gigaom.com/
- **role.md analyst relations playbook**: internal
