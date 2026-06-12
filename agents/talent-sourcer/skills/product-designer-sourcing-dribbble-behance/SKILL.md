<!--
Sources: https://www.twine.net/blog/best-dribbble-alternatives-to-hire-top-designers/
         https://amazinghiring.com/blog/searching-for-designers-on-dribbble-and-behance
         https://www.behance.net/dev
Behance — long-form case studies; UX/UI seniority signal.
Dribbble — shots / brand / motion; for-hire filter.
Both paywall sourcing in 2026; native search limited.
Alternatives: Twine, Toptal Design.
-->
# Product Designer Sourcing — Dribbble + Behance — SKILL

Source product designers via Behance (long-form case studies — UX/UI seniority signal), Dribbble (shots, brand, motion + for-hire filter), and Twine / Toptal Design as alternatives. Both Behance + Dribbble increasingly paywall sourcing in 2026. Cross-reference each find with LinkedIn for current employer + Apollo for email enrichment.

## When to use

- User wants to **source senior / staff / principal product designers**.
- User wants to **find for-hire designers** (Dribbble "for hire" + Behance "Hire Me" filter).
- User wants to **validate design portfolio** before outreach (long-form case study vs surface shots).
- User asks for "design system experts", "B2B SaaS designers", "brand designers", "motion / graphic designers".
- Trigger phrases: "designer sourcing", "Behance search", "Dribbble find", "product designer hire", "Hire Me filter", "design portfolio review".

Do not use for: graphic / illustration / motion-only sourcing (refer to Dribbble + Twine specifically); engineering / sales / exec sourcing (other skills); contracted design via Toptal Design (`contractor-sourcing-toptal-turing-pesto`).

## Setup

```bash
# Behance — Adobe-owned. API requires app approval (free but takes 5-10 business days).
# https://www.behance.net/dev
export BEHANCE_CLIENT_ID="xxx"

# Dribbble — Jobs API paid; profile API limited.
# https://developer.dribbble.com/v2/
export DRIBBBLE_ACCESS_TOKEN="xxx"

# Twine — alternative; no public API; firecrawl scrape.
# https://www.twine.net/

# Toptal Design — email intake only; no API.

# LinkedIn Sales Nav + Apollo for email enrichment.
export APOLLO_API_KEY="xxx"
```

## Common recipes

### Recipe 1: Behance — "Available for Hire" filter

```bash
# All Behance users marked available for hire
curl "https://api.behance.net/v2/users?available_for_hire=1&country=US&client_id=$BEHANCE_CLIENT_ID"

# Response: array of users with display name, profile_url, fields (design specialty), location
```

The `available_for_hire` flag is candidate-set — strongest intent signal.

### Recipe 2: Behance — project search (long-form portfolio)

```bash
# Search projects by tag + field
curl "https://api.behance.net/v2/projects?q=design+system&field=UX&time=year&sort=appreciations&client_id=$BEHANCE_CLIENT_ID"

# Per project, pull owner profile
curl "https://api.behance.net/v2/projects/{project_id}?client_id=$BEHANCE_CLIENT_ID"
# Response includes owner_id → pull /users/{owner_id}
```

Behance projects are long-form (10-30 slide case studies with wireframes + iteration + rationale). Strong signal of UX/UI process maturity.

### Recipe 3: Behance — user profile + project list

```bash
USER_ID=12345
curl "https://api.behance.net/v2/users/$USER_ID?client_id=$BEHANCE_CLIENT_ID"

# Project list — what kind of work do they actually do?
curl "https://api.behance.net/v2/users/$USER_ID/projects?client_id=$BEHANCE_CLIENT_ID&per_page=20"
```

### Recipe 4: Dribbble — for-hire designer search

```bash
# Dribbble has a "for hire" filter on shots page (UI: dribbble.com/designers?hireable=true)
# Programmatic via API:
curl "https://api.dribbble.com/v2/jobs/applicants?available_for_hire=true" \
  -H "Authorization: Bearer $DRIBBBLE_ACCESS_TOKEN"
```

Dribbble shots are small-format snapshots. Best for visual / brand / motion designers. Less signal of UX process maturity than Behance.

### Recipe 5: Dribbble — user profile + shots

```bash
USER_ID=12345
curl "https://api.dribbble.com/v2/users/$USER_ID" \
  -H "Authorization: Bearer $DRIBBBLE_ACCESS_TOKEN"

# Shots
curl "https://api.dribbble.com/v2/users/$USER_ID/shots" \
  -H "Authorization: Bearer $DRIBBBLE_ACCESS_TOKEN"
```

### Recipe 6: Cross-reference Behance/Dribbble → LinkedIn

```python
# Behance / Dribbble profile → LinkedIn lookup
designer = {
    "name": "Jane Designer",
    "location": "Berlin",
    "behance_url": "https://behance.net/janedesigner",
    "current_company_self_reported": "Acme Co"
}

# Search LinkedIn Sales Nav by name + location
linkedin_match = linkedin_sales_nav.search(
    fullname=designer["name"],
    location=designer["location"]
)

# Verify cross-platform identity (Recipe 10 in technical-sourcing-developer-focused.md)
confidence = verify_identity(behance=designer, linkedin=linkedin_match)

if confidence >= 70:
    designer["linkedin_url"] = linkedin_match["url"]
    designer["current_company_verified"] = linkedin_match["company"]
```

### Recipe 7: Apollo email enrichment

```bash
curl -X POST "https://api.apollo.io/v1/people/match" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -d '{
    "first_name": "Jane",
    "last_name": "Designer",
    "domain": "acme.com",
    "linkedin_url": "https://linkedin.com/in/janedesigner"
  }'

# Returns: email (verified band), current_company, title, phone
```

### Recipe 8: Designer ICP cluster (3-tier)

| Tier | Where to source | Portfolio signal | Reply rate baseline |
|------|-----------------|------------------|---------------------|
| Staff / Principal Product Designer | Behance (B2B SaaS case studies) | Design system docs + research artifacts + measurable impact | 12-18% |
| Senior Product Designer | Behance (mid) + Dribbble (mid) + LinkedIn | Multi-screen flows + a/b testing + design ops references | 10-15% |
| Mid Product Designer / Visual Designer | Dribbble + LinkedIn + Twine | Polished shots + brand work + landing pages | 15-22% |
| Designer + Engineer hybrid | GitHub (design-system repos) + Storybook contributor lists | Code commits to design system | 8-12% (niche) |

### Recipe 9: 3-touch designer sequence (portfolio-anchored)

| # | Day | Channel | Format | Goal |
|---|-----|---------|--------|------|
| 1 | 0 | LinkedIn InMail / Behance message | <400 char, reference specific Behance/Dribbble project | Show you actually saw their work |
| 2 | 5 | Email | Attach JD + 1-page brief of design challenges (concrete) | Designer attraction |
| 3 | 14 | LinkedIn message | "If now isn't right, what would make a future role compelling for you?" | Open feedback lane |

See `passive-candidate-outreach-campaigns` Recipe 5 for full template.

### Recipe 10: Cold InMail template — Behance case study reference

```
Subject: Your {company} design system

Hi {first} — your {project_name} case study is impressive (esp the {specific_artifact} doc). We're scaling a similar system at {your_co} (Series B B2B SaaS, 50k users) and looking for a staff PD to lead it. Worth 20 min? Best, {recruiter}
```

Char count: 280. Reference a specific case-study artifact ("the design tokens audit", "the research-to-shipping timeline"). Generic "your design work" reads as fake.

### Recipe 11: Twine — fallback marketplace

```bash
# Twine — no public API; firecrawl scrape with caution
firecrawl.scrape("https://www.twine.net/find-work?role=product-designer&location=us", {
  "extract": {"schema": {"name": "string", "rate": "string", "skills": "array", "twine_url": "string"}}
})
```

Twine is designer + freelancer marketplace. Lower seniority floor than Toptal Design but faster turn for project work.

### Recipe 12: Toptal Design — email intake (no API)

```
Email: hire@toptal.com
Subject: Design hire — Staff Product Designer, B2B SaaS, US

Hi Toptal — we're looking for a Staff Product Designer for a Series B B2B SaaS co (Acme, NYC + remote OK). Scope: lead design system + 2 IC reports. Comp band $180-220K + equity. JD attached.

Looking to interview 5-8 candidates within 2 weeks. Best,
{recruiter}
```

Toptal returns 5-8 vetted candidates within 5-10 business days at $100-200/hr equivalent comp band.

### Recipe 13: Portfolio quality screening (the 5-minute filter)

For each sourced designer, screen portfolio in 5 minutes:

| Screen pass | Pass criteria | Skip if |
|------------|---------------|---------|
| **Process maturity** | Case study shows: problem → research → iteration → ship → measure | Only final-screen pretty pictures |
| **Variety + depth** | 3-5 projects spanning B2B + B2C OR depth in 1 area | Single 1-screen mockup repeated |
| **Recent activity** | Latest project within 18 months | Last project >3 years ago = career gap |
| **Specific impact** | "Reduced onboarding drop-off 30%" / "Lifted conversion 12%" | All-vibes-no-numbers |
| **Design system signal** (for staff IC roles) | Tokens, doc, components, contribution model | Only screens, no system |

5-min screen filters 60-70% of Behance/Dribbble noise before outreach.

## Examples

### Example 1: Source 25 staff product designers for B2B SaaS
**Goal:** Staff PDs with design-system depth, US-based or remote-US.
**Steps:**
1. Behance: `available_for_hire=1, country=US, field=UX` (Recipe 1).
2. Per profile, pull project list (Recipe 3); 5-min portfolio screen (Recipe 13).
3. Cross-reference LinkedIn (Recipe 6) for current employer + tenure.
4. Apollo enrich for email (Recipe 7).
5. Score per `passive-candidate-outreach-campaigns` segmentation matrix.
6. Outreach via Recipe 10 (Behance-case-study-referenced InMail).

**Result:** 25 portfolio-validated staff PDs with verified contact; reply rate 12-18%.

### Example 2: Find a brand designer fast via Dribbble
**Goal:** Brand designer for a 4-week rebrand sprint.
**Steps:**
1. Dribbble for-hire search (Recipe 4); filter by skills=[branding, logo, identity].
2. Per shot list (Recipe 5), portfolio review.
3. Twine fallback if Dribbble pool insufficient (Recipe 11).
4. Toptal Design if needing vetted top-3% (Recipe 12).
5. Send Recipe 10 variant — reference specific shot.

**Result:** 5-10 brand designers identified within 2 days; project starts within week.

### Example 3: Validate "senior PD" LinkedIn claim via Behance portfolio
**Goal:** Candidate's LinkedIn says senior PD at FAANG; validate via Behance case studies.
**Steps:**
1. Lookup Behance via display name + location (Recipe 3).
2. Pull project list; 5-min portfolio screen (Recipe 13).
3. Score: process maturity (yes/no), recent activity (yes/no), specific impact (yes/no), design system signal (yes/no).
4. 4/4 = validated senior; 2-3/4 = mid-level; <2 = mis-leveled.

**Result:** Reduces level-mismatch in hiring; senior-IC roles need full case study process; mid-level can stretch.

## Edge cases / gotchas

- **Behance API requires app approval (5-10 business days).** Plan in advance; alternative is firecrawl scrape (ToS-aligned at low volume).
- **Dribbble Jobs API is paid + low quota.** Free tier covers minimal. Most teams use Dribbble for browsing + LinkedIn for sourcing.
- **Many top designers DON'T have public Behance / Dribbble.** They keep work confidential (employer-owned) or have personal site only. Absence of public portfolio ≠ no skill. Cross-reference LinkedIn + personal site (linktr.ee, read.cv).
- **read.cv** is the new designer-portfolio platform (since 2022); rapidly growing 2024-2026. Worth adding to source mix.
- **Generic "I love your design" InMail tanks reply rate to 2-3%.** ALWAYS reference a specific project, artifact, or design decision (Recipe 10).
- **Behance + Dribbble PMs are typically B2C / brand / agency.** B2B SaaS PDs are increasingly on LinkedIn + read.cv, not Behance. Calibrate per role-shape.
- **Portfolio noise floor is high.** 60-70% of for-hire Behance/Dribbble profiles are graphic designers, illustrators, students, or non-PMs. 5-min screen (Recipe 13) is non-negotiable.
- **Dribbble has a strong "shots culture" that rewards polish over process.** Senior PDs with great shipping records often have weak Dribbble accounts. Don't penalize for low Dribbble signal in senior IC.
- **Toptal Design is comp band $100-200/hr (equivalent $200-400K FTE for full-time engagement).** Confirm with Toptal before intake.
- **For "design system" roles specifically**, GitHub (Storybook, Tailwind, MUI contributor lists) is sometimes better signal than Behance — design system work tends to be code-adjacent.
- **AmazingHiring overlays Dribbble + Behance + LinkedIn + personal site** for designers — paid seat alternative if you're sourcing 50+ designers/quarter.
- **Behance pulls Adobe Creative Cloud activity** — many UX designers use Figma, not Adobe stack. Their Behance may be sparse despite strong skill. Cross-validate via Figma Community profiles.
- **Figma Community profiles** — new sourcing surface in 2025-2026; high-signal for design-tooling-savvy designers (https://www.figma.com/community/profile/{handle}).
- **Hand off outreach prose** to `cold-inmail-warm-intro` for high-priority finds.
- **Hand off to `contractor-sourcing-toptal-turing-pesto`** for contract / fractional design.
- **Defer to `passive-candidate-outreach-campaigns`** for multi-touch sequence.

## Sources

- Twine — Best Dribbble Alternatives 2026: https://www.twine.net/blog/best-dribbble-alternatives-to-hire-top-designers/
- AmazingHiring — Search for Designers on Dribbble + Behance: https://amazinghiring.com/blog/searching-for-designers-on-dribbble-and-behance
- Behance API: https://www.behance.net/dev
- Dribbble API: https://developer.dribbble.com/v2/
- Toptal Design: https://www.toptal.com/designers
- Twine: https://www.twine.net/
- read.cv (new portfolio platform): https://read.cv/
- Figma Community: https://www.figma.com/community
