# Talent Sourcer — Role Content (appended to AGENT.md)

This content is appended to the recipient's `AGENT.md` after import. It is **not** in the agent's default turn-by-turn context — the agent reads `soul.md` every turn and **greps** `AGENT.md` for deep references when stuck.

Use **searchable H2/H3 headings** the agent will literally grep for: "LinkedIn Recruiter Boolean library", "GitHub search operator reference", "Cold InMail template library", "Sequence pattern by role", "Diversity channel relationship playbook", "Source-of-hire dashboard schema", "ATS handoff API recipes", "Contractor marketplace routing matrix", "SOTA tool reference (June 2026)".

---

## Header note

This file appends to `AGENT.md` and is **not** loaded into the agent's default context. Grep when stuck. Searchable headings include: "LinkedIn Recruiter Boolean library", "GitHub search operator reference", "Stack Exchange API recipes", "Cold InMail template library", "Sequence pattern by role", "Hot-list segmentation patterns", "Target-company mapping playbook", "Exec sourcing playbook", "Diversity channel relationship playbook", "Boomerang re-engagement playbook", "Source-of-hire dashboard schema", "ATS handoff API recipes", "Contractor marketplace routing matrix", "JD optimization checklist", "Antipattern catalog", "SOTA tool reference (June 2026)".

---

## Capability reference

> Factual lists banished from soul.md. Tagged with subsection headings the agent will grep for.

### Sourcing channels (multi-tier)

- **Primary (always check):** LinkedIn Recruiter / Sales Nav, internal ATS (alumni, past applicants, hot-list), employee referrals.
- **Channel-specific by role family:**
  - Engineering / Data / ML: GitHub, Stack Overflow, Kaggle, DEV.to, HackerRank, LeetCode, conference speaker lists (PyCon, ICML, KubeCon, AI Engineer Summit).
  - Design: Behance, Dribbble, Awwwards, Twine, Toptal Design.
  - Sales: RepVue, Bravado, LinkedIn Sales Nav, Pavilion (RevOps community).
  - Customer Success: Gain Grow Retain, CS in Focus, LinkedIn.
  - Marketing: Demand Curve, Reforge, Superpath (content marketing), LinkedIn.
  - Ops / G&A: LinkedIn, Indeed, niche associations (CFO Leadership Council, etc.).
- **Aggregators:** SeekOut, Findem, AmazingHiring, hireEZ, Loxo, Leonar, Juicebox.
- **Niche boards:** Wellfound (startups), Hired (curated matching), Built In (US tech metros), Otta (curated), Y Combinator Work at a Startup (YC-only), Dice (US tech generalist), We Work Remotely (remote).
- **Diversity channels:** /dev/color, Code2040, Black Founders Matter, Lesbians Who Tech, Out in Tech, Latinas in Tech, Out & Equal, AfroTech, Grace Hopper Celebration, Tapia Conference, Project Include (process), Anita.org / AnitaB.
- **Vetted contractor marketplaces:** Toptal (top 3%), Turing (24h match), Andela (Africa-focused), Arc.dev (1% accept), Lemon.io (startup-focused), Pesto (Indian senior eng), Distributed.
- **Exec-only:** Lusha (verified executive phones), RocketReach (700M+ contacts), ContactOut (alt email + cell).
- **Boomerang / alumni:** Internal Notion DB + Enterprise Alumni + PeoplePath + LinkedIn change tracking.

### Sourcing aggregator capabilities

- **SeekOut.** 800M+ profile DB; 330M underrepresented profiles; explicit diversity filters; SeekOut Assist (April 2026) auto-generates Boolean from JD; technical-skill filters + GitHub activity scoring; clearance filter for cleared roles.
- **Findem.** Attribute-based filters (surfaces qualified candidates that title-based search misses); people-as-data graph; AI matching; CHRO/HRBP-friendly UI.
- **AmazingHiring.** 50+ developer networks (GitHub, Stack Overflow, Kaggle, Bitbucket, DEV.to, HackerRank, LeetCode); optional Diversity filter on request; developer-specific scoring.
- **hireEZ.** 45+ platform aggregation; AI Boolean builder (auto-generates from JD); 12-channel outreach sequencing; mid-market pricing.
- **Gem.** 800M+ profile DB; AI-first; multi-stage email sequencing; Chrome extension for inline sourcing; analytics; full-funnel.
- **Beamery.** Enterprise talent CRM; CHRO + TA leader-grade; deep ATS/HRIS integrations; global TA strategy focus.
- **Phenom.** Talent Experience Platform; career site + chatbot + CMS + CRM + AI scheduling + video assessments; full lifecycle.
- **Eightfold AI.** Talent intelligence; silver-medalist + alumni re-engagement; deep-learning skill matching; workforce intelligence.
- **Loxo.** 800M+ profile DB; sourcing + ATS + CRM all-in-one; basic plan free.
- **Leonar.** Mid-market; strong sourcing at moderate price; natural-language search (late 2025).
- **Juicebox.** Natural-language search pioneer; pasted JD → candidate list.

### Contact finder API matrix

- **Apollo** — 275M+ contacts, 65+ filter criteria; strongest free tier for full platform eval.
- **RocketReach** — 700M+ professionals; high-accuracy individual lookup with confidence scoring; alt path on missing LinkedIn.
- **Lusha** — verified business emails + direct phones; best for executive search + phone outreach.
- **Hunter.io** — real free tier, safe brand, honest verification; founder/solo SDR favorite.
- **Findymail** — <5% bounce rate via proprietary verification; Chrome extension auto-exports Sales Nav.
- **Snov.io** — public API; email verification; multi-touch outreach in one tool.
- **AnyMail Finder** — public API; bulk lookup; per-credit pricing.
- **ContactOut** — alt email + cell; strong on personal email when business email unknown.
- **FullEnrich** — most pragmatic for stitching into data pipelines (Snowflake, dbt).
- **Derrick** — newer; high-accuracy LinkedIn-tied lookup.
- **Wiza** — Sales Nav export + verified email; mid-market.

### Cold InMail benchmarks (2026)

- **Reply rate baselines:** average 10-25%; well-structured 35-50%; elite 30-40%.
- **By function:** HR/TA 12.08%, PM 10.24%, Operations 10.02%, Engineering 7-9%, Sales 8-11%, Marketing 9-12%.
- **Levers:** under 400 chars (22% lift), 16-27 char subject (30.5% lift), view profile first (78% acceptance lift).
- **LinkedIn Recruiter AI assist:** 69% reply-rate lift since April 2026.
- **Subject lines that work:** "Quick question, {first}", "{Company} hiring", "Saw your {talk/post/repo}", "{Mutual connection} suggested".
- **Subject lines that don't:** "Job opportunity", "Hi {first} — exciting role!", "Are you open to new roles?".

### ATS handoff matrix

| ATS | Candidate-create endpoint | Source field | Bulk import | Webhook on Applied |
|---|---|---|---|---|
| Greenhouse | `POST /v1/candidates` | `source_id` in body | yes (`/candidates` batch) | yes (`candidate_stage_change`) |
| Ashby | `POST /candidate.create` | `sourceId` param | yes (`/candidate.createBatch`) | yes (Ashby webhooks) |
| Lever | `POST /v1/candidates` | `sources` array | yes (CSV import) | yes (Lever Hooks) |
| Workable | `POST /spi/v3/candidates` | `domain` field | yes | yes |
| Zoho Recruit | `POST /api/v2/Candidates` | `Source` field | yes | yes (Zoho workflows) |
| SmartRecruiters | `POST /v201704/postings/{id}/candidates` | `source.sourceType` | yes | yes |

### LinkedIn 40-filter reference (Recruiter + Sales Nav)

Geography, current company, past company, current title, past title, school, years of experience, years at current company, function, industry, seniority, profile language, group membership, skills, certifications, languages, willing to relocate, recent activity, employer signals (recent layoffs / new funding), TeamLink (mutual connections), Open Candidates flag, Project / Folder, Saved Search membership, InMail status (opened / not yet contacted / replied), interest signals (Open to Work, Career Interests), Spotlights (Open to Work, Liking job posts, Following company), profile completeness, photo presence, recent job change (predicts tenure), company size, company growth rate, headquarter geography, Premium subscriber, profile views in last 90d, sentiment signals (recent talks / publications), school graduation year, military experience.

---

## LinkedIn Recruiter Boolean library

> Battle-tested Boolean string patterns by role family. Adapt; don't copy blindly.

### Senior Backend Engineer (Python / Go) — startup ICP

```
(("staff" OR "principal" OR "senior" OR "lead") AND ("software engineer" OR "backend engineer" OR "platform engineer"))
AND (Python OR Golang OR Go OR Rust)
AND ("distributed systems" OR Kubernetes OR microservices OR "API design")
AND NOT (recruiter OR consultant OR "hiring manager" OR student OR intern)
```
Filter layer: geography (target metros), current company size (50-1000), seniority (Senior IC / Manager+), years experience 5+.

### Staff Frontend Engineer (React / TypeScript) — growth-stage

```
(("staff" OR "principal" OR "senior staff") AND ("frontend engineer" OR "web engineer" OR "UI engineer"))
AND (React AND (TypeScript OR Typescript))
AND ("design system" OR Storybook OR accessibility OR "web performance")
AND NOT (recruiter OR consultant OR student OR intern)
```
Filter layer: seniority Senior IC, years experience 7+, current company stage Series A-D.

### Engineering Manager (50-150 person team)

```
(("engineering manager" OR "director of engineering" OR "VP engineering") AND NOT (CTO OR "CTO/VP"))
AND ("team of" OR "leading" OR "managing")
AND ("hired" OR "scaled" OR "grew the team")
AND NOT (recruiter OR consultant)
```
Filter layer: function Engineering, seniority Director / VP, current company headcount 100-500.

### Product Designer (B2B SaaS)

```
(("senior product designer" OR "staff product designer" OR "lead designer" OR "principal designer") AND ("B2B" OR "SaaS" OR "enterprise"))
AND (Figma AND ("design system" OR "design ops"))
AND (research OR "user research" OR "user testing")
AND NOT (graphic OR brand OR illustration OR motion OR student)
```
Filter layer: function Design, current company industry SaaS/B2B, geography target metros.

### Account Executive (SaaS $50-150K ACV)

```
(("account executive" OR "senior AE" OR "enterprise AE") AND ("SaaS" OR "B2B"))
AND ("quota" OR "ARR" OR "ACV" OR "closed won")
AND ("100%" OR "110%" OR "120%" OR "President's Club" OR "President Club")
AND NOT (BDR OR SDR OR "sales development" OR student)
```
Filter layer: function Sales, seniority Senior IC, years experience 3-7, current company SaaS.

### CTO / VP Engineering (Series B-D startups)

```
((CTO OR "chief technology officer" OR "VP of engineering" OR "head of engineering") AND ("series B" OR "series C" OR "series D" OR "growth stage"))
AND ("scaled" OR "hired" OR "built the team" OR "founding")
AND NOT (recruiter OR consultant OR student OR "in transition")
```
Filter layer: function Engineering, seniority CXO/VP, current/past company Series B-D, tenure 3-5 years at current role.

---

## GitHub search operator reference

> Hard-won syntax. Test on github.com/search before hitting the API.

### User search operators

```
location:"San Francisco" language:python followers:>50 repos:>10
location:Berlin OR location:Munich language:Go
language:Rust sort:followers-desc
fullname:"John Doe" location:NYC
```

### Repo search operators

```
language:TypeScript stars:>500 forks:>50 pushed:>2025-06-01
"distributed systems" in:name,description language:Go stars:>100
topic:machine-learning language:Python stars:50..500 forks:5..50
org:openai language:Python
```

### Commit search operators

```
author:torvalds path:kernel/sched
committer-date:>2026-01-01 language:rust
hash:a1b2c3d4
```

### REST API pattern

```bash
# User search
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/users?q=language:python+location:berlin+followers:>50&sort=followers&per_page=100"

# Repo contributors
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100"

# User repos (validate depth in language)
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/users/{login}/repos?type=owner&sort=updated&per_page=100"
```

### GraphQL pattern (preferred for contributor extraction)

```graphql
query ContributorScoring($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    collaborators(first: 100, affiliation: ALL) {
      edges {
        node {
          login
          email
          location
          contributionsCollection(from: "2025-06-01T00:00:00Z") {
            totalCommitContributions
            totalRepositoryContributions
          }
        }
      }
    }
  }
}
```

---

## Stack Exchange API recipes

```bash
# Top-reputation users by tag
curl "https://api.stackexchange.com/2.3/users?order=desc&sort=reputation&site=stackoverflow&tagged=python&pagesize=100"

# User top tags (validate domain depth)
curl "https://api.stackexchange.com/2.3/users/{id}/top-tags?site=stackoverflow"

# User top answers (signal of teaching ability)
curl "https://api.stackexchange.com/2.3/users/{id}/answers?order=desc&sort=votes&site=stackoverflow"
```

Score formula: `score = log(reputation) × (top_tag_match ? 1.5 : 1) × (recent_activity_within_30d ? 1.3 : 0.7)`. Filter at reputation > 5000 for senior; > 20000 for staff+.

---

## Cold InMail template library

### Engineering (passive — recent OSS commit signal)

```
Subject: Your {oss_project} work
Hi {first} — saw your recent commits to {oss_project}; the {specific_pr_or_feature} change was clever. We're hiring a staff platform eng to lead our {your_domain} infra (similar problem space). Worth 20 min to compare notes? Best, {recruiter}
```
Char count: 312. View profile first.

### Engineering (active — recent job change signal)

```
Subject: Quick thought, {first}
Saw you just joined {current_company} 3 mo back — congrats. Not pulling you out, but wanted to put us on your radar for 12-18 mo from now. We're a {stage} {sector} co building {what_problem}. Worth a coffee whenever? Best, {recruiter}
```
Char count: 287.

### Product designer (B2B SaaS, design-system depth)

```
Subject: Your {company} design system
Hi {first} — your work on the {company} design system is impressive (esp the {specific_component} doc). We're scaling a similar system at {your_co} and looking for a staff PD to lead it. Worth a 20 min chat? Best, {recruiter}
```
Char count: 292.

### CTO / VP Eng (recent funding event signal)

```
Subject: After the {company} round
{first} — congrats on the {company} {round} round. As you scale through this next chapter, we're hiring a VP Eng for a {sector} co at the {stage} level. Different scope but similar challenges (1-on-1 with {mutual_connection} if useful). Worth 30 min? Best, {recruiter}
```
Char count: 358. Warm-intro path identified before sending.

### Sales (RepVue rep, top quota signal)

```
Subject: Your {company} numbers
Hi {first} — RepVue surfaced you as a top-quota AE at {company}. Our $120K ACV B2B SaaS co is hiring; OTE band $230-260K. Worth 20 min for a comp + scope comparison? Best, {recruiter}
```
Char count: 245. RepVue comp transparency upfront.

### Warm intro request (via mutual connection)

```
Subject: Quick favor — {first_target}
Hi {first_mutual} — saw you're connected with {first_target} at {company_target}. We're looking to chat with them about a {role} role at our {stage} {sector} co; would you be open to a quick warm intro? Happy to share the pitch first. Best, {recruiter}
```

### Engineering re-engagement (boomerang / alumni)

```
Subject: Miss you, {first}
{first} — it's been {N} months since you left {company}. The team's grown since then; we just shipped {recent_milestone}. If your current role isn't quite right, we'd love to chat about {role_we_have} — different scope from when you were here. Coffee? Best, {recruiter}
```
Char count: 348. For alumni 12-18 months post-departure.

---

## Sequence pattern by role

### Engineering (passive, 5-touch sequence)

| # | Day | Channel | Format | Goal |
|---|---|---|---|---|
| 1 | 0 | LinkedIn InMail | <400 char, profile-view-first | First-touch context + role fit signal |
| 2 | 4 | Gmail | Reply to thread; add 1 specific point + value (link to engineering blog) | Reinforce + reduce ambiguity |
| 3 | 9 | LinkedIn message (different angle) | Open-source / tech-stack-specific question | Different hook angle |
| 4 | 16 | Gmail | Soft break-up: "if not now, OK to circle back in 6 mo?" | Open future door |
| 5 | 30 | LinkedIn message | Final touch: link to recent product launch + open invite | Last opportunity |

Pause sequence on any reply. Re-enroll after 90 days for "not now" responses.

### Sales (passive, 4-touch sequence, faster cadence)

| # | Day | Channel | Format | Goal |
|---|---|---|---|---|
| 1 | 0 | LinkedIn InMail | <400 char, comp transparency, RepVue benchmark cite | First-touch with $$ data |
| 2 | 3 | Gmail | Reply with 1-pager on deal sizes / quota / OTE | Concrete proof |
| 3 | 7 | LinkedIn message | "If timing's off, OK to refer me to a peer who'd be a fit?" | Open referral lane |
| 4 | 14 | Gmail | Break-up: "leaving this open" | Polite close |

### Executive (CTO / VP Eng, 3-touch sequence)

| # | Day | Channel | Format | Goal |
|---|---|---|---|---|
| 1 | 0 | Warm intro via mutual board member / investor (preferred) | High-context email | Trust transfer + brief |
| 2 | 7 | Direct cold InMail OR follow-up to warm path | <400 char, role + comp range | Direct ask |
| 3 | 21 | Calendar link / "any 30 min in next 2 weeks?" | Frictionless next step | Book |

---

## Hot-list segmentation patterns

### Standard tags

- `hot-list-eng-staff-3mo` (engineering, staff level, ready in 3 months)
- `hot-list-eng-staff-12mo` (staff IC, future)
- `hot-list-eng-manager-6mo` (manager, mid-window)
- `hot-list-design-pd-12mo` (product designer, future)
- `hot-list-ae-enterprise-3mo` (sales, enterprise AE, near-term)
- `hot-list-exec-cto` (executive, ongoing)
- `boomerang-eng` (alumni — engineering)
- `boomerang-12mo` (alumni at the 12-month post-departure window)
- `target-account-{company-slug}` (account-based sourcing tag)
- `diversity-channel-devcolor`, `diversity-channel-code2040`, etc.
- `referral-source-{employee-slug}` (referral attribution)

### Query patterns

```bash
# Hot-list query when a req opens
curl "https://api.gem.com/v1/prospects?tag=hot-list-eng-staff-3mo&tag=hot-list-eng-staff-6mo&last_touch_gt=30days"

# Boomerang fast-track when alumni applies (Greenhouse)
curl -X PATCH "https://harvest.greenhouse.io/v1/applications/{id}/tags" \
  -d '{"tags":["BOOMERANG", "fast-track"]}'
```

### Nurture cadence

- Monthly newsletter via Mailchimp: 1 product win + 1 culture story + 1 open role (light touch — not a pitch).
- Quarterly virtual event: AMA with engineering / design / sales leader; auto-invite to active hot-list segments.
- Ad-hoc: when a req opens, query hot-list FIRST; enroll matches in priority sequence with personalized hook.

---

## Target-company mapping playbook

1. **Crunchbase signal pull** — filter by funding stage (`series_a` / `series_b` / `series_c` / `series_d`), recent round (last 90 days), headcount band, industry.
2. **Layoff signal layer** — cross-reference Layoffs.fyi + WARN database; companies with recent layoffs in adjacent functions = high-intent passive pool.
3. **Per company: LinkedIn Sales Nav search** — `current company:{company} AND title:{target_role} AND tenure>1yr`.
4. **Contact enrichment** — pipe each candidate through Apollo `/v1/mixed_people/search` for email + phone + tenure validation.
5. **Bulk enroll** — load into Gem / hireEZ / Beamery with `target_account = {company_slug}` tag for tracking.
6. **Outreach personalization** — reference recent company news in InMail token (`{employer_proof_point} = {recent funding | recent product launch | layoff signal}`).

---

## Exec sourcing playbook (CTO / VP-Eng)

1. **Build target list (3 layers):**
   - Layer 1: direct competitors (same sector, similar stage)
   - Layer 2: acquired startups (2-3 years post-acquisition = key talent looking again)
   - Layer 3: late-stage / megacap engineering orgs (Google L7+, Meta E7+, Stripe / Snowflake / Databricks senior — open to startup at right comp)
2. **Score candidates:** tenure 3-5 years at level (open to move); recent funding event at current employer (predicts dissatisfaction or windfall — both create movement); domain depth match.
3. **Verify contact (2-source confirmation):**
   - Lusha for verified executive direct phones
   - RocketReach for personal email
   - ContactOut for alt-email + cell
   - Reject candidates without 2-source confirmation; sender reputation > volume.
4. **Identify warm-intro path per candidate:** mutual board member / investor / shared past-employer alum / shared school cohort. Warm intros for execs are non-negotiable.
5. **Brief packet for `ceo-agent` handoff:**
   - Target list with verified contacts + warm-intro path
   - Per candidate: 1-paragraph profile + signal-of-fit
   - Comp band reference (Pave / Carta Total Comp / Levels.fyi for benchmark)
   - Defer compensation philosophy + offer structure to `ceo-agent`.

---

## Diversity channel relationship playbook

### Channel relationships register (Notion DB)

| Channel | Primary contact | Sponsor tier | Last touch | Warm-intro requests outstanding | Conference cadence |
|---|---|---|---|---|---|
| /dev/color | {name + email} | {tier} | {date} | {N} | annual conference + quarterly events |
| Code2040 | {name + email} | {tier} | {date} | {N} | annual summit |
| Black Founders Matter | {name + email} | {tier} | {date} | {N} | quarterly meetup |
| Lesbians Who Tech | {name + email} | {tier} | {date} | {N} | annual summit (Lesbians Who Tech Summit) |
| Out in Tech | {name + email} | {tier} | {date} | {N} | annual conference + biannual events |
| Latinas in Tech | {name + email} | {tier} | {date} | {N} | annual summit |
| Out & Equal | {name + email} | {tier} | {date} | {N} | annual workplace summit |
| AfroTech | {name + email} | {tier} | {date} | {N} | annual conference |
| Grace Hopper Celebration | {name + email} | {tier} | {date} | {N} | annual (largest women-in-tech) |
| Tapia Conference | {name + email} | {tier} | {date} | {N} | annual (Latine + Black + other URM) |

### Sponsor cycle calendar (quarterly)

- Q1: AfroTech sponsorship commitment + Grace Hopper booth registration
- Q2: Lesbians Who Tech Summit sponsorship + /dev/color quarterly event attend
- Q3: Code2040 summit + Latinas in Tech sponsorship
- Q4: Out & Equal workplace summit + Tapia Conference + annual relationship-reviews

### Warm-intro request template (channel community manager)

```
Hi {first} — hope you're well. We're hiring a {role} at {company} (Series {round}, {sector}). Goal: pipeline a strong shortlist that reflects our values + engineering bar. Would you be open to forwarding the role to your community channels (Slack / Discord / mailing list)? Happy to attend an upcoming event or speak on a panel in return. Best, {recruiter}
```

---

## Boomerang re-engagement playbook

### Alumni DB schema (Notion)

- `name`, `linkedin_url`, `last_role`, `manager`, `team`
- `departure_date`, `departure_reason`, `sentiment_at_exit` (positive / neutral / negative)
- `current_company`, `current_role`, `tenure_at_current`
- `last_touch_date`, `touch_history`
- `linkedin_change_alert_subscribed` (boolean)
- `eligibility_flag` (some companies block re-hire post-termination — flag legal review)

### Quarterly re-engagement cadence

1. Week 1 of Q: Pull alumni DB; segment by `departure_date_gt_12mo` and `sentiment_at_exit != negative`.
2. Week 2: Author quarterly newsletter via Mailchimp — 1 product win + 1 culture update + open roles + alumni spotlight.
3. Week 3: LinkedIn alumni group post (if company has alumni group).
4. Week 4: 1:1 "we miss you" outreach to 5-10 highest-priority alumni (tenured + positive-sentiment + role-match).

### LinkedIn change tracking

- Subscribe via SeekOut alerts: `tag=alumni-yourco AND linkedin_role_changed=true`
- OR Gem alerts: `prospect.tag = alumni AND job_change_within_30d`
- Trigger re-engagement when alum changes role; window of 30-90 days post-change is peak.

### ATS auto-flag on return

```bash
# Greenhouse — auto-tag returning alumni
curl -X POST "https://harvest.greenhouse.io/v1/applications/{id}/tags" \
  -H "Authorization: Basic {token}" \
  -d '{"tags": ["BOOMERANG", "fast-track", "previous-tenure-{N}-yrs"]}'

# Ashby — auto-set candidate tag
curl -X POST "https://api.ashbyhq.com/candidate.addTag" \
  -d '{"candidateId":"{id}","tagId":"boomerang"}'
```

---

## Source-of-hire dashboard schema

### Per-source weekly metrics (Google Sheet schema)

| Column | Type | Description |
|---|---|---|
| `week_of` | date | Week start |
| `source` | enum | LinkedIn / GitHub / referrals / Wellfound / Gem / Boomerang / employee-referral / diversity-channel / other |
| `req_id` | string | Requisition ID |
| `sourced` | int | Candidates contacted from this source |
| `contacted` | int | Outreach sent |
| `replied` | int | Replied with interest |
| `screened` | int | Passed recruiter screen |
| `offered` | int | Offer extended |
| `hired` | int | Offer accepted + start date confirmed |
| `source_to_contact_pct` | derived | contacted / sourced |
| `contact_to_reply_pct` | derived | replied / contacted |
| `reply_to_screen_pct` | derived | screened / replied |
| `screen_to_offer_pct` | derived | offered / screened |
| `offer_acceptance_pct` | derived | hired / offered |

### Per-req monthly diversification check

| Check | Pass criteria | Action if fail |
|---|---|---|
| ≥3 active sources | True | Add 4th source + Boolean string |
| No single source >60% of pipeline | True | Rebalance: pause dominant; activate underused |
| Source-to-contact >25% | True | Refine targeting (filter precision) |
| Contact-to-reply >5% (eng) / >8% (sales) | True | A/B subject + intro; re-segment |
| Diversity channels active | ≥3 channels engaged | Activate sponsor / event / warm intro |

---

## ATS handoff API recipes

### Greenhouse (Harvest API)

```bash
# Create candidate from sourced prospect (on Applied stage)
curl -X POST "https://harvest.greenhouse.io/v1/candidates" \
  -H "Authorization: Basic $(echo -n $GH_TOKEN: | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "email_addresses": [{"value":"jane@example.com","type":"personal"}],
    "phone_numbers": [{"value":"+1234567890","type":"mobile"}],
    "social_media_addresses": [{"value":"https://linkedin.com/in/janedoe"}],
    "applications": [{"job_id": 12345, "source_id": 67890}]
  }'
```

### Ashby

```bash
curl -X POST "https://api.ashbyhq.com/candidate.create" \
  -H "Authorization: Basic $(echo -n $ASHBY_KEY: | base64)" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "linkedInUrl": "https://linkedin.com/in/janedoe",
    "sourceId": "{source-id}",
    "applicationFormDefinitionId": "{form-id}",
    "jobId": "{job-id}"
  }'
```

### Lever

```bash
curl -X POST "https://api.lever.co/v1/candidates" \
  -H "Authorization: Basic $(echo -n $LEVER_KEY: | base64)" \
  -d '{
    "name": "Jane Doe",
    "emails": ["jane@example.com"],
    "links": ["https://linkedin.com/in/janedoe"],
    "sources": ["LinkedIn Recruiter"],
    "stage": "applicant-new",
    "origin": "sourced"
  }'
```

### Zoho Recruit

```bash
curl -X POST "https://recruit.zoho.com/recruit/v2/Candidates" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_TOKEN" \
  -d '{"data":[{"First_Name":"Jane","Last_Name":"Doe","Email":"jane@example.com","Source":"LinkedIn"}]}'
```

---

## Contractor marketplace routing matrix

| Marketplace | Speed | Cost band | Sweet spot | API access | Notes |
|---|---|---|---|---|---|
| Toptal | 5-10 days | $100-200/hr | Premium, top 3%; finance + dev + design + PM | Email intake | Slow but highest filter |
| Turing | 24h | $40-80/hr (40-60% below Toptal) | Mid-senior dev; global | Yes (Turing API) | Fastest at scale |
| Andela | 1-2 weeks | $40-80/hr mid-level | Africa-based dev teams (full teams better than solo) | Email intake | Full-team strength |
| Arc.dev | 72h | $50-90/hr | 1% accept; AI-matched dev | Yes (Arc Employer API) | AI matching depth |
| Lemon.io | 24-48h | $55-95/hr | Startup-focused EU/LatAm dev; no subscription | Yes (intake form API) | Most Toptal-equivalent at lower price |
| Pesto | 3-7 days | $30-60/hr | Indian senior eng | Email intake | Senior India focus |
| Distributed | 1-2 weeks | varies | Full distributed teams | Email intake | Team build, not solo |
| Twine | varies | $30-150/hr | Designer marketplace | Yes | Design-specific alt to Toptal Design |

### Decision tree

- Premium budget + slow OK → **Toptal**
- Mid-budget + 24h SLA → **Turing** (global) or **Lemon.io** (startup-EU/LatAm)
- Full team / Africa nearshore → **Andela**
- AI-matched best-fit → **Arc.dev**
- India senior eng → **Pesto**
- Design-only → **Twine** or Toptal Design
- Distributed team-build → **Distributed**

---

## JD optimization checklist

> When Textio / Datapeople not in budget. Run JD through this manual pass before posting.

1. **Gendered language removal.** Scrub: "ninja", "rockstar", "guru", "manpower", "chairman", "salesman", "warrior", "dominant", "aggressive". Replace with role-neutral verbs ("lead", "operate", "build").
2. **Age-coded language removal.** Scrub: "digital native", "energetic", "young team", "recent grad mindset". Replace with skill-tied phrasing.
3. **Must-have count.** Cap at 6-8 must-haves. >8 must-haves drops female applicant rate ~30-40%.
4. **Comp transparency.** Include comp band where legal (CA / CO / NY / WA require it; voluntary elsewhere boosts apply rate).
5. **Concrete impact framing.** Use "day-1 ramp" + "30/60/90 plan" + measurable outcomes. Replace "fast-paced startup" with "we ship 2x/week and read code reviews on weekends sometimes".
6. **Skills > years.** Replace "10+ years experience" with "you've done X, Y, Z". Years filters out non-traditional paths.
7. **Inclusive culture statement.** Brief, specific. "We hire from across backgrounds; here's our diversity commitment + measured progress." Not corporate boilerplate.
8. **No "rockstar"-level salary expectations.** If you want senior IC, offer senior IC comp. Underpriced JDs filter out the candidates you want.

---

## Antipattern catalog

### Antipattern 1: 1,000-char Boolean keyword that returns 0 results

**BAD:**
```
("senior software engineer" OR "staff software engineer" OR "principal software engineer" OR "lead software engineer" OR "founding engineer") AND (Python OR Go OR Golang OR Rust OR TypeScript OR Java) AND (Kubernetes OR Docker OR microservices OR "service mesh" OR Istio OR Envoy OR gRPC OR Kafka) AND ("AWS" OR "GCP" OR "Azure") AND (PostgreSQL OR MySQL OR DynamoDB OR Redis) AND NOT (recruiter OR consultant OR contractor OR student OR intern OR coach OR career)
```
**Why it's bad:** Too many AND clauses kill the result set; LinkedIn requires ALL clauses match. 0 results because no one has every term in their profile.

**GOOD:**
```
("staff" OR "principal" OR "senior") AND ("software engineer" OR "platform engineer")
AND (Python OR Go OR Golang)
AND (Kubernetes OR microservices)
AND NOT (recruiter OR consultant)
```
**Why it's better:** Each AND should be a distinct must-have. Use LinkedIn's 40 filters (geography, current company, etc.) for the rest, not the keyword string. Returns 80-200 candidates — the sweet spot.

### Antipattern 2: Blast outreach (same template, 500 candidates)

**BAD:** Send "Hi {first}, exciting role at our company, are you interested?" to 500 candidates same template, same subject line.

**Why it's bad:** Reply rate <2%; sender reputation tanks; LinkedIn rate-limits InMail; gmail flags as spam. Wastes credits.

**GOOD:** Segment 500 candidates by (role + level + stage of current company); 3 templates per segment; A/B test subject + opening; pause-on-reply; refine per week.

**Why it's better:** Per-segment templates reply at 8-15%; segmented A/B identifies the +30% lift variant within 2 weeks; sender reputation preserved.

### Antipattern 3: Inferring diversity from photo / name / school

**BAD:** Reviewer marks Indian-sounding name → infers South Asian → counts toward "API diversity goal".

**Why it's bad:** Inaccurate (names != ethnicity); risks EEO violations; reproduces bias.

**GOOD:** Diversity attribution from explicit opt-in (candidate self-IDs in screener), channel-source (sourced via Code2040 = Black/Latine pipeline), or SeekOut/Findem probabilistic signal (with confidence band; never treated as ground truth).

**Why it's better:** Legally defensible; ethically grounded; measurable at top-of-funnel without invading privacy.

### Antipattern 4: Skipping hot-list when a req opens

**BAD:** Req opens → recruiter immediately drafts new Boolean → cold sources 200 fresh candidates.

**Why it's bad:** Ignores 30-100 warmer hot-list candidates who already know the company; 3-5x slower funnel; wastes existing nurture investment.

**GOOD:** Req opens → query hot-list (`tag=hot-list-{role}-{stage}`) → enroll matches in priority sequence with personalized hook → THEN cold sourcing for the remainder.

**Why it's better:** Hot-list candidates convert 3-5x faster; nurture investment pays off; faster time-to-fill.

### Antipattern 5: Single-source >60% of pipeline

**BAD:** 80% of hires from LinkedIn Recruiter. Other channels barely touched.

**Why it's bad:** LinkedIn pricing change / seat loss / policy change destroys 80% of pipeline overnight. No backup channel.

**GOOD:** ≥3 sources; no source >60%; weekly diversification review; rebalance when one source dominates.

**Why it's better:** Pipeline resilient to single-channel disruption; surfaces candidates LinkedIn won't.

### Antipattern 6: Outreach without source-attribution

**BAD:** All candidates show "source = sourced" in ATS; no per-channel attribution.

**Why it's bad:** Source-of-hire reporting impossible; channel investment is guesswork; cost-per-hire untrackable per source.

**GOOD:** Every candidate carries `source = {LinkedIn | GitHub | Wellfound | Gem-sequence | Boomerang | Code2040 | etc.}` tag at moment of contact. ATS source field populated on every push.

**Why it's better:** Real source-of-hire data; informed channel investment; per-source funnel optimization.

---

## SOTA tool reference (June 2026)

> Generated from `reference/SOTA_USE_CASES.md`. One H3 per tool — grep-friendly. Each subsection 10-30 lines pointing to its bundled skill pack + brief usage note.

### LinkedIn Recruiter + Sales Navigator

**Use for:** Primary sourcing surface for all roles. Boolean string authoring + 40-filter layering + InMail outreach + Sales Nav for warm-intro routing.
**Skill pack:** [`linkedin-recruiter-boolean-search-strings`](skills/linkedin-recruiter-boolean-search-strings/SKILL.md) + [`cold-inmail-warm-intro`](skills/cold-inmail-warm-intro/SKILL.md)
**Install:** LinkedIn Recruiter seat required (Lite / Pro / Corporate tiers); Talent Solutions API for partner-approved integration only.
**Quick recipe:**
```
# Boolean for staff backend eng (under 1000 chars)
("staff" OR "principal" OR "senior") AND ("software engineer" OR "backend engineer")
AND (Python OR Golang) AND ("distributed systems" OR Kubernetes)
AND NOT (recruiter OR student)
```
**Source:** https://www.talentprise.com/linkedin-boolean-search-guide/

### GitHub (REST + GraphQL APIs)

**Use for:** Developer sourcing by language + stars + commits + contribution graphs. 180M+ active developers.
**Skill pack:** [`github-talent-mining-language-stars-commits`](skills/github-talent-mining-language-stars-commits/SKILL.md) + [`technical-sourcing-developer-focused`](skills/technical-sourcing-developer-focused/SKILL.md)
**Install:** `github` MCP + GitHub personal access token (recipient).
**Quick recipe:**
```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/users?q=language:python+location:berlin+followers:>50&sort=followers&per_page=100"
```
**Source:** https://docs.github.com/en/rest/search/search

### Stack Overflow (Stack Exchange API)

**Use for:** Developer sourcing by reputation + top-tag activity. Jobs discontinued 2022 but profile search remains.
**Skill pack:** [`stack-overflow-talent-reputation-tag`](skills/stack-overflow-talent-reputation-tag/SKILL.md)
**Install:** No auth required for public Stack Exchange API (rate-limited).
**Quick recipe:**
```bash
curl "https://api.stackexchange.com/2.3/users?order=desc&sort=reputation&site=stackoverflow&tagged=python&pagesize=100"
```
**Source:** https://api.stackexchange.com/docs

### SeekOut

**Use for:** 800M+ profile DB, 330M underrepresented profiles, explicit diversity filters, technical-skill + GitHub activity scoring, SeekOut Assist Boolean from JD.
**Skill pack:** [`amazinghiring-findem-seekout-diversity`](skills/amazinghiring-findem-seekout-diversity/SKILL.md) + [`technical-sourcing-developer-focused`](skills/technical-sourcing-developer-focused/SKILL.md)
**Install:** SeekOut paid seat ($500+/user/mo typical).
**Quick recipe:** Use SeekOut Assist UI → paste JD → review auto-generated Boolean + diversity filter overlay → run search.
**Source:** https://juicebox.ai/blog/seekout-reviews

### Findem

**Use for:** Attribute-based candidate filters (surfaces qualified candidates missed by title-based search), people-as-data graph.
**Skill pack:** [`amazinghiring-findem-seekout-diversity`](skills/amazinghiring-findem-seekout-diversity/SKILL.md)
**Install:** Findem paid seat.
**Source:** https://www.findem.ai/

### AmazingHiring

**Use for:** 50+ developer network aggregation (GitHub, Stack Overflow, Kaggle, etc.); optional Diversity filter on request.
**Skill pack:** [`amazinghiring-findem-seekout-diversity`](skills/amazinghiring-findem-seekout-diversity/SKILL.md) + [`technical-sourcing-developer-focused`](skills/technical-sourcing-developer-focused/SKILL.md)
**Install:** AmazingHiring paid seat.
**Source:** https://amazinghiring.com

### hireEZ

**Use for:** 45+ platform aggregation + AI Boolean builder + 12-channel outreach sequencing; mid-market pricing.
**Skill pack:** [`gem-hireez-beamery-talent-crm`](skills/gem-hireez-beamery-talent-crm/SKILL.md) + [`linkedin-recruiter-boolean-search-strings`](skills/linkedin-recruiter-boolean-search-strings/SKILL.md)
**Install:** hireEZ paid seat.
**Source:** https://explore.hireez.com/

### Gem

**Use for:** Talent CRM with 800M+ profile DB + AI-first sourcing + multi-stage email sequencing + Chrome extension + analytics.
**Skill pack:** [`gem-hireez-beamery-talent-crm`](skills/gem-hireez-beamery-talent-crm/SKILL.md) + [`passive-candidate-outreach-campaigns`](skills/passive-candidate-outreach-campaigns/SKILL.md) + [`hot-list-talent-community-mgmt`](skills/hot-list-talent-community-mgmt/SKILL.md)
**Install:** Gem paid seat.
**Quick recipe:**
```bash
# Enroll prospect in sequence
curl -X POST "https://api.gem.com/v1/sequences/{id}/enroll" \
  -H "Authorization: Bearer $GEM_KEY" \
  -d '{"prospect_id":"{id}","start_step":1}'
```
**Source:** https://www.selectsoftwarereviews.com/reviews/gem

### Beamery

**Use for:** Enterprise talent CRM (CHRO + global TA leader-grade); deep ATS/HRIS integrations.
**Skill pack:** [`gem-hireez-beamery-talent-crm`](skills/gem-hireez-beamery-talent-crm/SKILL.md)
**Install:** Beamery enterprise contract.
**Source:** https://beamery.com/platform/talent-acquisition/talent-crm/

### Phenom / Eightfold AI / Symphony Talent (SmashFly)

**Use for:** Enterprise talent experience platforms (career site + chatbot + CRM + CMS + AI scheduling + talent marketplace + alumni re-engagement).
**Skill pack:** Pattern-mapped via `gem-hireez-beamery-talent-crm` skill + parent agent (operations-agent) for ATS integration.
**Install:** Enterprise contract.
**Source:** https://www.phenom.com/ + https://www.goperfect.com/blog/10-best-eightfold-ai-alternatives-for-talent-intelligence-in-2026

### Apollo.io

**Use for:** 275M+ contact DB + Crunchbase-like company graph; B2B prospecting API for contact enrichment.
**Skill pack:** [`target-company-mapping-crunchbase-linkedin`](skills/target-company-mapping-crunchbase-linkedin/SKILL.md) + [`cto-vp-eng-exec-sourcing`](skills/cto-vp-eng-exec-sourcing/SKILL.md)
**Install:** Apollo API key (free tier covers MVP).
**Quick recipe:**
```bash
curl -X POST "https://api.apollo.io/v1/mixed_people/search" \
  -H "X-Api-Key: $APOLLO_KEY" \
  -d '{"person_titles":["Staff Engineer"],"organization_locations":["Berlin"]}'
```
**Source:** https://www.apollo.io/product/api

### Crunchbase Enterprise

**Use for:** 4M+ private company graph + predictive funding / acquisition / IPO signals. Target-account mapping.
**Skill pack:** [`target-company-mapping-crunchbase-linkedin`](skills/target-company-mapping-crunchbase-linkedin/SKILL.md)
**Install:** Crunchbase Enterprise API key.
**Source:** https://www.crunchbase.com/api

### Lusha / RocketReach / ContactOut / Findymail / Hunter / Snov / AnyMail Finder

**Use for:** Contact enrichment (email + phone + alt-email). 2-source verification before outreach.
**Skill pack:** [`cto-vp-eng-exec-sourcing`](skills/cto-vp-eng-exec-sourcing/SKILL.md) + [`target-company-mapping-crunchbase-linkedin`](skills/target-company-mapping-crunchbase-linkedin/SKILL.md)
**Install:** Per-vendor paid seat (Hunter free tier covers low scale).
**Quick recipe:**
```bash
# RocketReach
curl "https://api.rocketreach.co/v2/api/lookupProfile?api_key=$RR_KEY&linkedin_url={url}"

# Lusha (exec phone)
curl "https://api.lusha.com/v2/person?email={email}" -H "api_key: $LUSHA_KEY"

# Findymail
curl -X POST "https://app.findymail.com/api/search" \
  -H "Authorization: Bearer $FM_KEY" \
  -d '{"linkedin_url":"{url}"}'
```
**Source:** https://www.findymail.com/blog/best-email-finder-tools/

### Wellfound + Built In + Hired + Otta

**Use for:** Niche job boards for startup + tech metros + curated audiences. Posting + candidate sourcing.
**Skill pack:** [`hired-wellfound-built-in-otta-niche-boards`](skills/hired-wellfound-built-in-otta-niche-boards/SKILL.md)
**Install:** Wellfound Recruit Pro ($499/mo); Built In paid metro plan; Otta employer dashboard; Hired curated tier.
**Source:** https://wellfound.com/recruit/pricing + https://www.glozo.com/blog/niche-it-job-boards-recruiters-2025

### RepVue

**Use for:** Sales talent sourcing by quota attainment + employer rating; 2026 comp benchmarks (SDR $60K/$85K OTE).
**Skill pack:** [`sales-talent-sourcing-repvue`](skills/sales-talent-sourcing-repvue/SKILL.md)
**Install:** RepVue employer plan.
**Source:** https://www.repvue.com/employers

### Behance + Dribbble

**Use for:** Product designer sourcing. Behance for long-form case studies; Dribbble for shots / brand / motion.
**Skill pack:** [`product-designer-sourcing-dribbble-behance`](skills/product-designer-sourcing-dribbble-behance/SKILL.md)
**Install:** Behance API app approval + Dribbble jobs API (paid).
**Quick recipe:**
```bash
curl "https://api.behance.net/v2/users?available_for_hire=1&country={c}&client_id=$BEHANCE_KEY"
```
**Source:** https://www.behance.net/dev

### Toptal / Turing / Andela / Arc.dev / Lemon.io / Pesto

**Use for:** Vetted contractor marketplaces. Routing by urgency + budget + geography.
**Skill pack:** [`contractor-sourcing-toptal-turing-pesto`](skills/contractor-sourcing-toptal-turing-pesto/SKILL.md)
**Install:** Per-vendor enrollment (Toptal/Andela email intake; Turing/Arc.dev/Lemon.io API).
**Source:** https://lemon.io/blog/toptal-alternatives/

### Textio + Datapeople

**Use for:** JD optimization. Textio for outcome-based language guidance; Datapeople for readability + template enforcement.
**Skill pack:** Embedded in [`employer-brand-in-outreach`](skills/employer-brand-in-outreach/SKILL.md)
**Install:** Textio / Datapeople paid seat.
**Source:** https://www.index.dev/blog/textio-review

### Greenhouse / Ashby / Lever / Zoho Recruit (ATS handoff)

**Use for:** Push sourced candidates on Applied stage; source-attribution field; source-of-hire reporting.
**Skill pack:** Hand off to parent `operations-agent`'s `hiring-pipeline-greenhouse-ashby-lever` skill; per-API recipes in this role.md.
**Install:** Per-ATS API key (recipient).
**Source:** https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable

### Diversity channels (community-led)

**Use for:** /dev/color, Code2040, Black Founders Matter, Lesbians Who Tech, Out in Tech, Latinas in Tech, Out & Equal, AfroTech, Grace Hopper Celebration, Tapia Conference.
**Skill pack:** [`diversity-channel-sourcing-dev-color-code2040`](skills/diversity-channel-sourcing-dev-color-code2040/SKILL.md)
**Install:** Channel-specific membership + sponsor cycle commitment.
**Source:** https://devcolor.org + https://www.code2040.org + https://lesbianswhotech.org + https://projectinclude.org

### Boomerang / alumni tools

**Use for:** Alumni database + LinkedIn change tracking + quarterly newsletter + ATS auto-flag on return.
**Skill pack:** [`boomerang-alumni-re-engagement`](skills/boomerang-alumni-re-engagement/SKILL.md)
**Install:** Notion DB + Mailchimp + SeekOut/Gem alerts + ATS API.
**Source:** https://ks-agents.com/blog/boomerang-employees-alumni-network-strategy/

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Source X engineers" | `linkedin-recruiter-boolean-search-strings` + `github-talent-mining-language-stars-commits` + `gem-hireez-beamery-talent-crm` | Layer ≥3 channels; check hot-list first |
| "Author a Boolean for {role}" | `linkedin-recruiter-boolean-search-strings` | Then SeekOut/hireEZ AI Boolean if available |
| "Write an InMail to {candidate}" | `cold-inmail-warm-intro` | <400 chars; view profile first; warm intro fallback |
| "Set up an outreach sequence" | `passive-candidate-outreach-campaigns` + `gem-hireez-beamery-talent-crm` | Segment first; A/B from step 1 |
| "Find a CTO / VP Eng candidate" | `cto-vp-eng-exec-sourcing` + `target-company-mapping-crunchbase-linkedin` | Warm intro non-negotiable; brief to ceo-agent |
| "Build a target-company list" | `target-company-mapping-crunchbase-linkedin` | Crunchbase signal + Layoffs.fyi layer |
| "Source from {GitHub / Stack Overflow}" | `github-talent-mining-language-stars-commits` + `stack-overflow-talent-reputation-tag` | Cross-reference both for confidence |
| "Help with diversity sourcing" | `diversity-channel-sourcing-dev-color-code2040` + `amazinghiring-findem-seekout-diversity` | Project channels + AI filter overlay |
| "Re-engage alumni" | `boomerang-alumni-re-engagement` | Quarterly cadence + LinkedIn change alerts |
| "Find a contractor for {scope}" | `contractor-sourcing-toptal-turing-pesto` | Match by urgency + budget + geo |
| "Source a product designer" | `product-designer-sourcing-dribbble-behance` | Behance Hire Me + Twine fallback |
| "Find sales talent" | `sales-talent-sourcing-repvue` + `linkedin-recruiter-boolean-search-strings` | RepVue quota filter + Sales Nav |
| "Audit our source-of-hire" | `source-of-hire-reporting` + `source-to-contact-metrics` | 12-month per-source breakdown; flag single-source >60% |
| "Manage talent community" | `hot-list-talent-community-mgmt` | Tag by readiness; quarterly newsletter |
| "Post to niche board" | `hired-wellfound-built-in-otta-niche-boards` | Wellfound free for startups |
| "Optimize this JD" | `employer-brand-in-outreach` (JD sub-skill) | Textio/Datapeople or manual checklist |
| "Verify candidate experience SLA" | `candidate-experience-hygiene-response-time` | 24h reply / 7d stage |
| "Push candidate to ATS" | `gem-hireez-beamery-talent-crm` push-to-ATS sub-recipe + parent operations-agent's ATS skill | Hand off completes scope |

---

## Brief / Output templates

### Sourcing strategy brief (per req)

```markdown
# {Role} Sourcing Strategy — {Date}

## ICP
- Must-have: {3-6 must-haves}
- Nice-to-have: {3-5 nice-to-haves}
- Disqualifiers: {2-3 disqualifiers}
- Comp band: {range}
- Geo: {locations}
- Diversity goals: {channel-active + ≥3 channels engaged}

## Channels (≥3)
1. **LinkedIn Recruiter**: Boolean = `…` ; target candidate count = {N}
2. **{Channel 2}**: Boolean / filter = `…` ; target = {N}
3. **{Channel 3}**: Boolean / filter = `…` ; target = {N}

## Funnel projection
- Sourced: {N1}
- Contacted: {N1 × source-to-contact %}
- Replied: {N2 × contact-to-reply %}
- Screened: {N3 × reply-to-screen %}
- Hired: {N4 × screen-to-offer × offer-acceptance %}

## Hot-list pull (before cold sourcing)
- Existing hot-list match: {N} candidates
- Boomerang match: {N}
- Referral seed: {N}

## Hand-off
- ATS push on Applied: {Greenhouse | Ashby | Lever | Zoho}
- Recruiter coordinator owns interview pipeline
```

### Candidate brief (per exec / specialist handoff)

```markdown
# {Candidate Name} — {Role Brief} — {Date}

## Profile snapshot
- Current: {role} at {company} ({tenure})
- Past: {1-2 highlights}
- Domain depth: {1-2 sentences}
- LinkedIn: {url} | GitHub: {url} | Personal: {url}

## Contact (2-source verified)
- Email: {primary} (source 1: {source}, source 2: {source})
- Phone: {primary} (source 1: {source}, source 2: {source})

## Signal of fit (3 bullets)
- {bullet 1}
- {bullet 2}
- {bullet 3}

## Warm-intro path
- Mutual: {name} ({connection type})
- Intro request status: {drafted / sent / replied / closed}

## Outreach status
- Last touch: {date} via {channel}
- Reply status: {none | replied positive | replied not now | declined}
- Next action: {action + date}

## Comp context
- Pave / Carta / Levels.fyi band: {range}
- Defer offer strategy to: ceo-agent (exec) or operations-agent (IC/manager)
```

### Source-of-hire monthly dashboard (xlsx / google-sheet template)

| Source | Hires (m1) | Hires (m2) | Hires (m3) | % of total | Avg time-to-hire | Avg cost-per-hire | Quality score (3-mo) |
|---|---|---|---|---|---|---|---|
| LinkedIn Recruiter | {N} | {N} | {N} | {%} | {days} | {$} | {1-5} |
| GitHub mining | {N} | {N} | {N} | {%} | {days} | {$} | {1-5} |
| Employee referral | {N} | {N} | {N} | {%} | {days} | {$} | {1-5} |
| Wellfound | {N} | {N} | {N} | {%} | {days} | {$} | {1-5} |
| Gem outbound | {N} | {N} | {N} | {%} | {days} | {$} | {1-5} |
| Boomerang | {N} | {N} | {N} | {%} | {days} | {$} | {1-5} |
| Diversity channel | {N} | {N} | {N} | {%} | {days} | {$} | {1-5} |
| Other | {N} | {N} | {N} | {%} | {days} | {$} | {1-5} |

**Flags:**
- [ ] Any single source >60% — REBALANCE
- [ ] Source-to-contact <25% — refine ICP / Boolean
- [ ] Top-of-funnel diversity <stated goal — activate underused channels

---

## Closing rules

Boolean before browse. Passive over active. ≥3 sources per req. Diversity is intentional. Hot-list first when a req opens. Warm intro beats cold. Verify contact via 2 sources. 24h reply SLA. Hand off on Applied. Always disclose for binding employment-law decisions. Boolean search beats LinkedIn search filters by 10×; passive candidates are the talent; diversity sourcing requires intentional channels.
