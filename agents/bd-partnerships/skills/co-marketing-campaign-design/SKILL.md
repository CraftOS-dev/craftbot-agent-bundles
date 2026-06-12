<!--
Source: https://www.crossbeam.com/blog/co-marketing-playbook/ + https://blog.hubspot.com/marketing/co-marketing-guide
Joint co-marketing campaign design + Joint Marketing Agreement (JMA) (June 2026 SOTA).
-->
# Co-Marketing Campaign Design — SKILL

Design and run joint marketing campaigns with partners. Output: shared messaging frame + co-branded asset suite (one-pager, webinar deck, blog series, customer-story video) + distribution split + measurement plan + Joint Marketing Agreement (JMA). Cross-agent hand-off to `marketing-agent` for creative production; this skill owns the BD coordination + governance.

## When to use

- **New partnership goes-live and needs co-marketing kickoff** — within 30 days of agreement signed.
- **Quarterly joint-GTM cycle** — fresh campaign per quarter with strategic partners.
- **Joint customer story production** — co-authored case studies.
- **Event activation** — joint webinar, conference booth, podcast.
- **Co-branded content series** — blog co-author, joint newsletter, joint thought-leadership.
- **Trigger phrases**: "co-marketing campaign", "joint webinar", "co-branded asset", "customer story", "joint blog", "JMA", "co-marketing brief".

Do NOT use this skill for: **internal marketing campaigns** (use `marketing-agent` direct); **MDF processing** (use `mdf-allocation-tracking`); **partner-led webinar logistics** (use `partner-led-webinars-events`); **legal redlines on JMA** (defer to `legal-counsel`).

## Setup

```bash
export MATON_API_KEY="<key>"               # for PandaDoc JMA + HubSpot UTM tracking
# Notion for brief authoring + asset registry
# Cross-agent: marketing-agent (creative production)
# Optional: Buffer / Bitly for UTM management
export BUFFER_API_KEY="<key>"
export BITLY_ACCESS_TOKEN="<token>"
```

## Common recipes

### Recipe 1: Co-marketing brief (canonical template, write to Notion)

```yaml
campaign:
  name: "Brand × Acme — Q3 Co-Marketing"
  partner: "Acme Analytics"
  partner_id: "acme-001"
  start: "2026-07-01"
  end: "2026-09-30"
  objective: "Drive 500 joint leads, 50 SQLs, 10 closed-won in Q3"

  shared_messaging:
    headline: "Two best-in-class tools, one revenue stack"
    sub: "Brand's attribution + Acme's CDP = unified ICP picture and confident pipeline"
    pain_we_solve_together: "Revenue teams using HubSpot + Segment can't tie marketing spend to closed-won; Brand×Acme fixes it in 2 weeks"

  audience:
    primary: "VP Marketing + RevOps at US mid-market SaaS (50-500 employees)"
    secondary: "VP Sales pre-Series-C"
    joint_customer_overlap: 60      # known shared customers from Crossbeam
    addressable_new: 4000

  assets:
    one_pager: "Co-branded 2-page solution brief"
    pitch_deck: "Joint 12-slide deck for AE use"
    customer_story_video: "5-min Loom interview with shared customer"
    blog_series: "3 blog posts, alternating publication on each blog"
    webinar: "45-min joint webinar; Brand hosts, Acme co-presents"
    landing_page: "brand.com/partners/acme + acme.com/partners/brand"
    utm_taxonomy: "utm_campaign=q3-brand-acme; utm_source=brand or acme; utm_medium=blog/email/social/webinar"
    email_template: "Co-signed sequence for shared-customer outbound"

  distribution_split:
    brand_audience: "12K newsletter, 35K LinkedIn followers"
    acme_audience:  "9K newsletter, 28K LinkedIn followers"
    paid_run: "$10K LinkedIn ABM, split 50/50; Acme run on their handle"
    organic_run: "3 LinkedIn posts each, 1 joint Twitter thread, 1 podcast appearance"

  measurement:
    primary_kpi: "Joint pipeline sourced"
    secondary: "Webinar registrations + post-event MQLs + content downloads + blog traffic"
    attribution: "First-touch UTM credits joint campaign; CRM source=Partner+JointCampaign"
    review_cadence: "Weekly stand-up Wednesday; monthly read-out"

  owners:
    brand_owner: "<bd-lead> + <demand-gen-lead>"
    acme_owner:  "<their-bd> + <their-content-lead>"

  risks:
    - "Acme's audience is 30% non-US; need US-only segment for tracking"
    - "JMA not yet signed — block creative until then (see Recipe 9)"

  approvals:
    - "Brand legal-counsel sign off JMA (Recipe 9)"
    - "Both VPs sign off shared messaging"
    - "Customer sign-off for customer-story (Recipe 6)"
```

### Recipe 2: Asset coordination — cross-agent hand-off to marketing-agent

```yaml
# Hand-off contract — what marketing-agent needs from this skill
handoff_to_marketing_agent:
  inputs:
    campaign_brief_url: "notion-page-id://..."
    co_brand_logos:
      - "Brand 256x256 PNG"
      - "Acme 256x256 PNG"
    co_brand_color_palette: "primary #1A2B3C, accent #FF6B35 (Brand); secondary #4A4A4A (Acme)"
    shared_messaging_doc: "notion-page-id://..."
    target_assets: ["one_pager", "pitch_deck", "blog_post_1of3", "social_kit"]
    voice_alignment: "Brand voice → educational + data-driven; Acme voice → conversational + practical"
    delivery_deadline: "2026-07-10"

  outputs_expected_back:
    - "Asset URLs in google-drive-mcp shared folder"
    - "Source files (Figma / Canva)"
    - "Localized variants if applicable"
    - "Sign-off recipient list for both sides"
```

`marketing-agent` owns the actual asset production (`canva-mcp` / `figma-mcp` / `pptx` / `docx`).

### Recipe 3: UTM taxonomy + Bitly links (per-channel attribution)

```bash
# Master campaign UTM
CAMPAIGN="q3-brand-acme"

# Per-channel links
for SOURCE in brand acme; do
  for MEDIUM in email blog social webinar paid; do
    LONG_URL="https://brand.com/joint-offer?utm_campaign=$CAMPAIGN&utm_source=$SOURCE&utm_medium=$MEDIUM&utm_content=joint-q3"
    SHORT=$(curl -X POST "https://api-ssl.bitly.com/v4/shorten" \
      -H "Authorization: Bearer $BITLY_ACCESS_TOKEN" -H "Content-Type: application/json" \
      -d "{\"long_url\":\"$LONG_URL\",\"domain\":\"bit.ly\"}" | jq -r '.link')
    echo "$SOURCE,$MEDIUM,$SHORT,$LONG_URL"
  done
done
```

Store the link table in `google-sheets` shared dashboard; both sides reference same links.

### Recipe 4: Co-branded landing page

```yaml
landing_page:
  url: "https://brand.com/partners/acme"
  sections:
    - hero: "Joint headline + 2 logos + CTA"
    - problem_section: "Pain shared customers feel"
    - solution_section: "How together we solve it"
    - integration_overview: "2-min animated diagram (drawio-mcp source)"
    - customer_proof: "Joint customer logos (5-8) + 1 quote"
    - demo_request_form: "HubSpot embedded form with hidden field campaign=q3-brand-acme"
    - secondary_cta: "Watch the joint webinar replay"

  acme_mirror:
    url: "https://acme.com/partners/brand"
    structure: "Mirror with Acme's voice; same data + assets"
```

Both sides own their own mirror; brand-attributed leads → Brand CRM; acme-attributed → Acme CRM; jointly-attributed → both via webhook.

### Recipe 5: Joint blog series (3 posts, alternating)

```yaml
blog_series:
  - post: "1 of 3: The Revenue Stack Problem"
    publish_on: "brand.com/blog/joint-revenue-stack"
    co_author: "Brand author + Acme guest paragraph"
    cross_link: "Linked from acme.com/blog/about + sidebar"
  - post: "2 of 3: How Joint Customers Win"
    publish_on: "acme.com/blog/joint-customer-wins"
    co_author: "Acme author + Brand quote"
  - post: "3 of 3: Architecture Deep Dive"
    publish_on: "brand.com/blog/joint-architecture"
    co_author: "Brand technical lead + Acme integration engineer"
  cadence: "Weekly, Tuesdays 9am ET"
  syndication: "Both sides amplify on LinkedIn + Twitter + newsletter"
```

### Recipe 6: Customer-story production flow

```yaml
customer_story:
  candidate_account: "Joint customer with 6+ months on both products + measurable outcome"
  candidate_selection:
    sources: ["Crossbeam joint customer list", "CSM nominations"]
    criteria: ["Champion willing to speak", "Quantifiable outcome (revenue or efficiency)", "No competitor mentions"]

  flow:
    step_1_outreach: "BD reaches out via warm intro (CSM); 'we'd love to feature your win'"
    step_2_interview: "30-min recorded call via zoom-mcp; transcript via fathom-api"
    step_3_draft: "We draft 1-pager + 5-min video script"
    step_4_review: "Customer reviews and signs off (legal + marcom on their side)"
    step_5_legal_signoff: "PandaDoc customer story release form (Recipe 7)"
    step_6_publish: "Live on both sites + LinkedIn + newsletter same day"
    step_7_amplify: "Joint paid promotion for 14 days"

  formats:
    - "1-page PDF case study"
    - "5-min video (cut by video-creator cross-agent)"
    - "30-sec social video clip (3 highlight reels)"
    - "Quote block for sales decks"
    - "Win wire for internal channels"
```

### Recipe 7: Customer story release form (via PandaDoc)

```bash
curl -X POST "https://gateway.maton.ai/pandadoc/public/v1/documents" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"Customer Story Release — Acme Corp",
    "template_uuid":"<release-template-id>",
    "recipients":[{"email":"sarah@acmecorp.com","role":"Customer"}],
    "tokens":[
      {"name":"Customer.Name","value":"Acme Corp"},
      {"name":"Vendor.Name","value":"Brand"},
      {"name":"PartnerVendor.Name","value":"Acme Analytics"},
      {"name":"UsageScope","value":"1-page PDF, video (with transcript), social clips, website case study, sales deck quote, press inclusion if asked"},
      {"name":"TerritoryScope","value":"Worldwide"},
      {"name":"TermLength","value":"3 years; auto-renew unless withdrawn 30 days notice"},
      {"name":"WithdrawalRights","value":"Customer may withdraw consent for new uses with 60 days notice; existing materials persist"}
    ]
  }'
```

### Recipe 8: Webinar coordination (cross to partner-led-webinars-events)

For joint webinars, use `partner-led-webinars-events` skill for the operational mechanics. This skill owns the joint-content side: shared agenda, who-pitches-what, post-event lead routing rules.

```yaml
webinar_split:
  registration_routing:
    if registrant_domain == brand_customer: route to acme CRM as new
    if registrant_domain == acme_customer:  route to brand CRM as new
    if registrant_domain == joint_customer: route to both as touched
    if registrant_domain == new:            route to both
  post_event:
    - "Recording shared via google-drive-mcp public link"
    - "Joint thank-you email from both sides"
    - "Survey for follow-up demos (separate by side)"
```

### Recipe 9: Joint Marketing Agreement (JMA)

```bash
curl -X POST "https://gateway.maton.ai/pandadoc/public/v1/documents" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"JMA — Brand × Acme Q3 2026",
    "template_uuid":"<jma-template-id>",
    "recipients":[{"email":"cmo@acme.com","role":"Partner"},{"email":"cmo@brand.com","role":"Vendor"}],
    "tokens":[
      {"name":"CampaignName","value":"Q3 Brand × Acme Joint GTM"},
      {"name":"Term","value":"July 1 - Sep 30, 2026"},
      {"name":"BrandUsageScope","value":"Each party may co-brand assets for the campaign; usage limited to agreed channels (Section 3)"},
      {"name":"BrandUsageRestrictions","value":"No use after Sep 30 without renewal; logos used per brand guidelines (Appendix A); no defacement"},
      {"name":"ContentApprovalProcess","value":"Both CMOs sign off before publication; 5-business-day review window"},
      {"name":"LeadSharingRules","value":"Per Recipe 8 webinar split; per UTM rules; double-opt-in for joint contacts"},
      {"name":"DataTerms","value":"Each party processes own leads under own privacy policy; no PII shared between parties without explicit opt-in"},
      {"name":"CostSharing","value":"Each side covers own labor; shared expenses (e.g., paid promotion $10K) split 50/50"},
      {"name":"TerminationClause","value":"Either party may terminate with 14 days written notice; published assets persist unless materially defective"}
    ]
  }'
```

JMA covers brand usage + content approval + lead sharing + cost split + termination. ALWAYS route through `legal-counsel`.

### Recipe 10: Measurement dashboard (Google Sheets / Notion)

```yaml
dashboard:
  weekly_metrics:
    - "Webinar registrations"
    - "Webinar attendance + replay views"
    - "Blog page views per post (UTM-attributed)"
    - "Landing page conversions"
    - "Joint demo requests"
    - "Joint pipeline created ($)"
    - "Joint closed-won (count + $)"
  attribution:
    primary: "Last-touch UTM (campaign=q3-brand-acme)"
    secondary: "First-touch UTM"
    fallback: "Self-reported lead source"
  dashboards_owners: "BD lead Brand + BD lead Acme co-own"
```

Render via `google-sheets` with formulas; sync weekly via `slack-mcp` digest to both teams.

### Recipe 11: Sign-off workflow

```python
# Pre-publish checklist
checklist = [
    ("JMA signed by both sides", check_pandadoc_status),
    ("Customer release signed (if applicable)", check_pandadoc_status),
    ("Both legal teams reviewed final copy", check_notion_approval),
    ("Both CMOs signed off final asset versions", check_notion_approval),
    ("UTM tracking validated end-to-end", validate_utm),
    ("Landing page A/B test live", check_landing_page),
    ("Email send-list segmented + double-opt-in", check_email_segments),
    ("Webinar Zoom URL + dial-in confirmed", validate_zoom),
]
blocked = [name for name, fn in checklist if not fn()]
if blocked:
    raise RuntimeError(f"Cannot publish — blockers: {blocked}")
```

### Recipe 12: Post-campaign retrospective

```yaml
retro:
  date: "2026-10-15"
  attendees: "Both BD leads + Both demand-gen leads + 1 marketer each side"
  format: "60-min Zoom; pre-read with metrics; 30 min discussion"
  framework: "Start / Stop / Continue"
  outputs:
    - "Metrics summary (final pipeline / closed-won)"
    - "What worked / what didn't"
    - "Q4 next-campaign decision"
    - "Action items in notion-mcp shared workspace"
```

## Examples

### Example 1: Joint webinar campaign (Q3 launch)

**Goal:** First joint webinar with new partner; goal: 250 registrations, 100 attendees, 25 SQLs.

**Steps:**
1. Week 1 — Recipe 1 brief in Notion; both sides sign off.
2. Week 2 — Recipe 9 JMA signed.
3. Week 2-4 — Recipe 2 hand-off to `marketing-agent`; landing page + email seq + social kit built.
4. Week 3-4 — Recipe 3 UTM links generated.
5. Week 5 — Webinar promotion live (each side promotes to own audience).
6. Week 6 — Webinar Day; 320 registered (above goal); 145 attend; 38 SQLs.
7. Week 6-8 — Follow-up flow per Recipe 8.
8. Week 12 — Recipe 12 retro; 8 closed-won attributed.

**Result:** Campaign exceeded SQL goal; pipeline value $640K; ROI 6.4x on $100K invested.

### Example 2: Joint customer story

**Goal:** Feature a flagship joint customer who saved $200K via the integration.

**Steps:**
1. Recipe 6 — Identify candidate via Crossbeam + CSM nomination.
2. Champion interview booked; release form (Recipe 7) routed to customer legal.
3. Interview recorded via `zoom-mcp` + transcript via `fathom-api`.
4. Draft via `docx`; video edit via `video-creator` cross-agent.
5. Customer review; minor edits; sign-off.
6. Joint publish on both blogs + LinkedIn announcement.
7. Promoted via paid LinkedIn ABM 14 days.

**Result:** Customer story drives 12 inbound demos; 4 pipeline; 2 closed in Q4.

### Example 3: Co-branded blog series

**Goal:** 3-post series cementing thought leadership on revenue-stack architecture.

**Steps:**
1. Recipe 5 — Series outline + author assignments + cross-link plan.
2. Both content teams draft in parallel.
3. Each post peer-reviewed by other side before publication.
4. Cadence: Tuesday 9am ET; both sides amplify same day.
5. UTM-tracked traffic flows to landing page (Recipe 4).

**Result:** Series totals 18K page views; 280 demo requests; pipeline of $1.4M after 90 days.

## Edge cases / gotchas

- **JMA before creative.** Publishing co-branded asset without signed JMA opens both sides to brand-usage disputes. JMA first.
- **Brand-guideline mismatches** — partner logo on dark vs light background; minimum margin; co-existing typography. Spell out in JMA Appendix A.
- **Approval fatigue** — too many sign-offs slows campaign. Limit to: each-side legal + each-side CMO. Operators below get review window but not blocking.
- **Audience overlap inflation** — partners over-claim audience size. Validate with public follower counts + open rates.
- **UTM hygiene** — if you don't standardize UTM taxonomy up front, attribution falls apart. Recipe 3 is non-negotiable.
- **Double-opt-in for joint leads** — GDPR + CASL + most US best-practice require explicit consent to share lead between two companies. Build double-opt-in into all forms.
- **Customer release scope is the #1 future-headache** — too narrow ("only this case study") blocks reuse; too broad ("worldwide perpetual unlimited") rarely signed. Default to 3-year multi-format.
- **Customer withdrawal rights** — most customers want a withdrawal clause. Honor it; remove materials from active distribution within 30 days.
- **Cost sharing on paid promotion** can spiral — agree max budget up front; cap variance at 20%.
- **Mid-campaign pivot risk** — one side decides to deprioritize; partner is stuck. Termination clause in JMA covers this.
- **Cross-agent coordination overhead** — this skill defers creative to `marketing-agent`; risk of dropped handoffs. Use Recipe 2 explicit hand-off + Slack channel per campaign.
- **Customer story timing** — most powerful within 90 days of customer's milestone. Past 6 months, energy fades.
- **Lead-routing edge cases** — what if registrant is a joint customer? What if multi-region? Recipe 8 must handle. Test with 10 fake registrants before launch.
- **Time-zone misalignment** for webinars — picking time zone is political. Default: target audience time zone; recording covers the other.
- **Brand voice clash** — Brand is technical-formal; Acme is conversational-casual. Decide whose voice wins per asset; document in brief.
- **Track-record dispute** — both sides may claim same lead. Last-touch UTM is the tiebreaker.
- **Co-branding rules differ by region** — some regions (Japan) very formal about logo lockup; others (US) flexible.
- **Post-campaign asset archive** — keep all assets + JMA + retro in Notion folder forever. New campaigns reference patterns.

## Sources

- Crossbeam co-marketing playbook: https://www.crossbeam.com/blog/co-marketing-playbook/
- HubSpot co-marketing guide: https://blog.hubspot.com/marketing/co-marketing-guide
- Joint Marketing Agreement template (Forrester): https://www.forrester.com/blogs/joint-marketing-agreements/
- Customer story production best practices: https://www.crossbeam.com/blog/co-marketing-customer-stories/
- UTM tracking discipline: https://www.gartner.com/en/marketing/insights/articles/utm-tagging-best-practices
- PandaDoc API for JMA / release forms: https://developers.pandadoc.com/
- Bitly API: https://dev.bitly.com/
- Goldcast / ON24 webinar mechanics: https://www.goldcast.io/blog/co-marketing-webinars
