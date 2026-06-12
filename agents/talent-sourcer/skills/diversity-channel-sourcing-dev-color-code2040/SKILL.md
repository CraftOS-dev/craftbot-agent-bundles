<!--
Sources: https://devcolor.org
         https://www.code2040.org
         https://lesbianswhotech.org
         https://blackfoundersmatter.com
         https://outintech.com
         https://latinasintech.org
         https://www.outandequal.org
         https://www.afrotech.com
         https://ghc.anitab.org
         https://tapiaconference.cmd-it.org
         https://projectinclude.org
         https://mindhuntai.com/blog/diversity-sourcing-strategies
Project-specific diversity channels: /dev/color, Code2040, Black Founders Matter,
Lesbians Who Tech, Out in Tech, Latinas in Tech, Out & Equal, AfroTech, Grace Hopper, Tapia.
Pattern: become corporate partner / sponsor; attend conferences; nurture community channels.
Relationship-led, not transactional. Project Include best-practices over process.
-->
# Diversity Channel Sourcing — /dev/color, Code2040, Lesbians Who Tech, etc. — SKILL

Build + maintain relationships with project-specific diversity channels and surface candidates through warm intros, conferences, Slack / Discord communities, and sponsor cycles. Each channel = a multi-quarter relationship investment, not a one-off lookup. Project Include best practices layered over recruiting process. This is the right channel when leadership has signed off on "diversity hiring is a goal, not just a checkbox."

## When to use

- User wants to **engage a specific diversity channel** for an open role.
- User wants to **build the channel-relationship register** (first time setting up).
- User wants to **plan a sponsor cycle** for the year (which conferences + amounts).
- User wants to **request a warm intro** from a channel community manager.
- User wants to **route a diverse role to the right channel** (Black eng → /dev/color; Latina eng → Latinas in Tech; LGBTQ+ → Lesbians Who Tech or Out in Tech; early-career Black/Latine → Code2040; Black founders / exec → Black Founders Matter).
- Trigger phrases: "diversity channel", "/dev/color", "Code2040", "Lesbians Who Tech", "AfroTech", "Grace Hopper", "Tapia", "Out in Tech", "Latinas in Tech", "Black Founders Matter", "diversity sourcing", "URM channels", "underrepresented sourcing", "diversity sponsor cycle".

Do not use for: AI-filter-based diversity sourcing (`amazinghiring-findem-seekout-diversity`); attribution from photo / name / school (BANNED — see Antipattern 3 in role.md); demographic data collection on candidates (defer to People-Ops / EEO survey).

## Setup

```bash
# Channel relationships register (Notion)
export NOTION_API_KEY="secret_xxx"
export NOTION_CHANNELS_DB="<db_id>"     # one row per channel

# Outreach templates (Gmail)
export GMAIL_TOKEN="xxx"

# Sponsor cycle calendar (Google Calendar)
export GCAL_TOKEN="xxx"
export GCAL_CALENDAR_ID="recruiting-events"

# Project tracking (Linear / Asana)
export LINEAR_API_KEY="lin_api_xxx"

# Community comms (Slack / Discord — channel-specific)
export SLACK_BOT_TOKEN="xoxb-xxx"
export DISCORD_BOT_TOKEN="xxx"

# Optional — SeekOut / Findem for AI-filter overlay (paired skill)
export SEEKOUT_API_KEY="xxx"
```

No "diversity API" exists; this skill operates through humans + relationships. The tools above support tracking, not lookup.

## Common recipes

### Recipe 1: Channel registry (the canonical mapping)

| Channel | Audience | Primary engagement | Sponsor tiers | URL |
|---|---|---|---|---|
| /dev/color | Black engineers (IC + leadership) | Slack community + A-list mentorship + annual conference | Bronze / Silver / Gold / Platinum | https://devcolor.org |
| Code2040 | Early-career Black + Latine | Annual summit + fellowship program | Title sponsor / Friend / Ally tiers | https://www.code2040.org |
| Black Founders Matter | Black founders + senior tech | Quarterly meetups + venture network | Partner / Sponsor | https://blackfoundersmatter.com |
| Lesbians Who Tech | LGBTQ+ technical | Annual summit (largest) + city chapters | $5K-$100K+ | https://lesbianswhotech.org |
| Out in Tech | LGBTQ+ tech broadly | Annual conference + city chapters + biannual events | $10K-$75K+ | https://outintech.com |
| Latinas in Tech | Latina technical | Annual summit + city chapters + monthly events | Bronze / Silver / Gold / Platinum | https://latinasintech.org |
| Out & Equal | LGBTQ+ workplace ERG leaders | Annual Workplace Summit (B2B) | Bronze - Diamond | https://www.outandequal.org |
| AfroTech | Black tech professionals (largest) | Annual conference + AfroTech Executive | $25K-$500K+ | https://www.afrotech.com |
| Grace Hopper Celebration | Women in tech (largest) | Annual conference (AnitaB.org) | various; $50K-$500K+ | https://ghc.anitab.org |
| Tapia Conference | URM in computing (Black + Latine + Native) | Annual conference (CMD-IT) | various | https://tapiaconference.cmd-it.org |
| Project Include | DEI best-practices (process, not sourcing) | Open guidance + research reports | n/a (open community) | https://projectinclude.org |
| Anita.org / AnitaB | Women in tech (Grace Hopper organizer) | Year-round programming | varies | https://anitab.org |

Maintain in Notion DB with columns: `channel | primary_contact | sponsor_tier | last_touch | warm_intros_outstanding | conference_cadence | recipient_budget_committed`.

### Recipe 2: Sponsor cycle calendar (annual)

```
Q1 (Jan-Mar):
  - AfroTech sponsorship commitment (Q4 conference but contracts close Q1)
  - Grace Hopper booth registration (deadline Feb)
  - Code2040 annual planning meeting

Q2 (Apr-Jun):
  - Lesbians Who Tech Summit sponsorship (June summit)
  - /dev/color quarterly event attend (typical May)
  - Plan AfroTech booth + giveaway

Q3 (Jul-Sep):
  - Code2040 Summit attend (Aug)
  - Latinas in Tech Summit sponsorship (Sep)
  - Grace Hopper booth prep + speaker submissions
  - Out in Tech annual event

Q4 (Oct-Dec):
  - AfroTech Conference (Nov)
  - Out & Equal Workplace Summit (Oct)
  - Tapia Conference (Sep-Oct)
  - Annual relationship-reviews + next-year planning
```

Block on Google Calendar (Recipe 11) so the entire team has visibility.

### Recipe 3: Channel-relationship register schema (Notion DB)

```yaml
# One Notion DB entry per channel
schema:
  channel: "/dev/color"
  primary_contact_name: "Jane Smith"
  primary_contact_email: "jane@devcolor.org"
  primary_contact_role: "Director of Partnerships"
  sponsor_tier_current_year: "Silver ($25K)"
  sponsor_tier_target_next_year: "Gold ($50K)"
  last_touch_date: "2026-04-15"
  last_touch_type: "Quarterly check-in call"
  warm_intros_outstanding: 3
  warm_intros_received_ytd: 12
  conference_cadence:
    - "Quarterly events"
    - "Annual conference (Sep)"
  hires_from_channel_ytd: 4
  hires_from_channel_alltime: 23
  notes: "Strong relationship; Jane is direct + fast. Avoid August (her PTO)."
```

### Recipe 4: Warm-intro request template (channel community manager)

```
Subject: Quick favor — {role} role at {your_company}

Hi {first} — hope you're well. Quick favor: we're hiring a {role} at {your_company} (Series {round}, {sector}). Comp band {comp_band}, fully remote/{hybrid}, {compelling_proof_point}.

Goal: pipeline a strong shortlist that reflects our values + engineering bar. Would you be open to forwarding the role to your community channels (Slack / Discord / mailing list)?

Happy to attend an upcoming event or speak on a panel in return. Also — if there are specific people you'd suggest I reach out to directly, would love your nominations.

Thanks always for the partnership.

Best, {recruiter}
```

Length: 350-450 chars (longer than candidate outreach because it's a B2B asks-and-gives msg). Send via Gmail, NOT InMail.

### Recipe 5: AfroTech conference recruiting workflow

```bash
# Pre-conference (T-90d to T-30d):
# 1. Confirm booth size + materials (banner, swag, postcards w/ QR to careers page)
# 2. Register all attending engineers as "ambassadors" (not just recruiters)
# 3. Book speaker submissions (Code Talk track)
# 4. Pre-conference happy hour invitation list (Notion DB filter: "AfroTech attendees + interested")

# At conference:
# 5. Day-of: scan badges to capture intent; sync to Greenhouse with source = "AfroTech-2026"
# 6. Same-day follow-up: 24h SLA on candidate conversations (LinkedIn add + email)

# Post-conference (T+1 to T+30d):
# 7. Pull all source = "AfroTech-2026" candidates from ATS (Recipe 7)
# 8. Enroll in afrotech-followup Gem sequence (template references conversation specifics)
# 9. Schedule recruiter touch on every candidate within 7 business days
# 10. Quarterly check-in cadence: AfroTech attendees go on hot-list
```

### Recipe 6: Code2040 fellowship program engagement

Code2040 runs a paid summer fellowship for early-career Black + Latine technologists. Hosting a fellow ≈ direct pipeline + brand lift.

```
1. Apply as Host Company (Q1 deadline, ~Jan-Feb)
2. Submit JD + mentor profile + project scope
3. If accepted, Code2040 matches a fellow to your team for 9 weeks (summer)
4. Pay: $10-15K fellow + $5-15K program partnership fee (varies by year)
5. Post-fellowship: 80% conversion if fellow + team click
6. Track via Notion: fellow → hire conversion + ongoing mentorship cadence
```

### Recipe 7: Track diversity-channel source in ATS

```bash
# Source labels — one per channel + per event/year
sources_dictionary=(
  "Channel: /dev/color"
  "Channel: Code2040"
  "Channel: Lesbians Who Tech"
  "Channel: Out in Tech"
  "Channel: Latinas in Tech"
  "Channel: Black Founders Matter"
  "Event: AfroTech 2026"
  "Event: Grace Hopper 2026"
  "Event: Tapia 2026"
  "Event: LWT Summit 2026"
  "Fellowship: Code2040 2026 fellow"
)

# Configure as Sources in ATS (Greenhouse: Configure → Sources)
# When pushing candidate, set source.id to the matching ID
# Per role.md Antipattern 6: NEVER tag candidates as "Other" or "Sourced" generically
```

### Recipe 8: Lesbians Who Tech Summit sponsorship workflow

```
Q1: confirm budget + tier (Title $100K+ / Gold $50K / Silver $25K / Bronze $10K)
Q2: register; submit speaker proposal; prepare booth content; identify 5 staff "ambassadors"
Q2 end (summit June): attend; lead 1 session OR sponsor breakfast/happy hour
Post-summit: 30-day campaign — connect with attendees on LinkedIn; enroll Gem sequence
Track: hires-attributable + brand engagement (career page visits from LWT referrals)
```

### Recipe 9: Slack community sourcing (channel-specific)

```bash
# /dev/color: members-only Slack workspace
# Out in Tech: Discord
# Lesbians Who Tech: Slack
# Latinas in Tech: Slack
# Black Founders Matter: Slack

# Pattern: become a verified company member; post job in #jobs channel monthly
# DO NOT spam; DO NOT DM individual members cold
# DO contribute to #general discussions BEFORE posting jobs

# Example posting (Slack):
TEXT="Hiring: Staff Backend Engineer at Acme. Series C $80M (May), fully remote, $250-310K + 0.15-0.30% equity. Apply: careers.acme.com/staff-backend. Happy to chat: @YourName"
curl -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -d "channel=#jobs&text=$TEXT"
```

Member access varies. Most channels require company verification + paid membership before /jobs channel access.

### Recipe 10: Project Include best-practices layer

Project Include (Erica Joy Baker, Tracy Chou, Y-Vonne Hutchinson, Ellen Pao, et al.) publishes diversity-of-process best practices. Layer over recruiting process; not a sourcing channel itself.

Key principles to apply:
- **Diverse slate at every stage** (≥2 underrepresented candidates per finalist round)
- **Structured interviews** (rubric per question; calibration before debrief)
- **Inclusive interview panels** (≥1 underrepresented interviewer per panel)
- **Anti-bias training** for interviewers (annually)
- **Outcome tracking** by stage + demographic (top-of-funnel through hire)
- **Equitable comp** (band-based; no ad-hoc adjustments)

Reference: https://projectinclude.org/recommendations

### Recipe 11: Sponsor cycle Google Calendar block

```bash
# Block all conferences for full team visibility
curl -X POST "https://www.googleapis.com/calendar/v3/calendars/$GCAL_CALENDAR_ID/events" \
  -H "Authorization: Bearer $GCAL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "AfroTech 2026 Conference",
    "location": "Houston, TX",
    "description": "Sponsor tier: Gold. Booth #142. Ambassadors: @recruiter @eng-lead @vp-eng",
    "start": {"date": "2026-11-12"},
    "end": {"date": "2026-11-15"},
    "attendees": [{"email":"recruiter@acme.com"},{"email":"vp-eng@acme.com"}]
  }'
```

### Recipe 12: Quarterly relationship-review (per channel)

```markdown
# /dev/color Q3 2026 Relationship Review

## Health
- Last touch: 2026-07-12 (Quarterly Director call)
- Sponsor tier YTD: Silver ($25K committed)
- Warm intros received YTD: 8 (of 15 requested)
- Hires from channel YTD: 3 (target: 5)

## Wins
- Hired 2 staff engineers via warm intro path
- Speaker spot at /dev/color annual conference (Sep)

## Gaps
- Slow response on Q2 warm-intro requests (need to push)
- 1 candidate fell through at offer stage (post-mortem: comp band mismatch)

## Q4 actions
- Increase sponsor tier proposal: Silver -> Gold for 2027 ($25K -> $50K)
- Confirm conference attendance + send 4 ambassadors
- Submit speaker proposal for 2027 conference (deadline Nov)
- Schedule December check-in call
```

### Recipe 13: Diverse-slate enforcement (per req)

```bash
# Every finalist round must have >=2 underrepresented candidates
# Track in ATS or Notion per req:

REQ_ID="ENG-2026-STAFF-04"
curl "https://api.notion.com/v1/databases/<diverse-slate-db>/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -d "{\"filter\":{\"property\":\"req_id\",\"title\":{\"equals\":\"$REQ_ID\"}}}" \
  | jq '{finalist_count: .results[0].properties.finalist_count.number, ur_count: .results[0].properties.ur_finalist_count.number}'

# If ur_count < 2 AND finalist_count >= 3: HOLD onsite scheduling; surface to recruiting lead
# Activate underrepresented channels (Recipe 4 warm-intro) before proceeding
```

## Examples

### Example 1: Set up channel registry from scratch (new TA leader)
**Goal:** New head of TA arrived; no diversity channel relationships exist. Build the foundation.
**Steps:**
1. Create Notion DB per Recipe 3 schema; populate with 10-12 rows from Recipe 1.
2. Identify warm-intro paths to each channel's primary contact (LinkedIn 2nd-degree, mutual investor, mutual portfolio company alum).
3. Draft initial outreach per Recipe 4; send 1-2 per week (not all at once — relationships are sequential).
4. Plan Q1-Q4 sponsor cycle (Recipe 2); allocate budget to top 4 channels for year 1: AfroTech ($50K) + Grace Hopper ($25K) + /dev/color ($25K) + Lesbians Who Tech ($25K).
5. Block calendar (Recipe 11) for all conferences.
6. Configure Sources in ATS per Recipe 7 so attribution works from Day 1.

**Result:** 6 months in: 4 active partnerships; 1-2 sponsored events attended; 8-12 candidates sourced; 1-3 hires. Year 2 multiplier when relationships mature.

### Example 2: Activate /dev/color for a staff backend req
**Goal:** REQ ENG-2026-STAFF-PLATFORM-04 (staff backend, $250-310K, remote). Want pipeline diversity at top of funnel.
**Steps:**
1. Pull /dev/color row from Notion registry; confirm partnership active + Jane is responsive.
2. Send Recipe 4 warm-intro request via Gmail to Jane: ask to post in #jobs Slack channel + nominate 3 candidates directly.
3. Wait 5 business days; if Jane silent, follow up with Slack DM (not email — Jane prefers Slack per registry notes).
4. Receive 3 nominations + #jobs post leads to 8 inbound applies.
5. Enroll all 11 prospects in `devcolor-warm-intro` Gem sequence; reference Jane in opener.
6. Tag all candidates with `source = Channel: /dev/color` in ATS (Recipe 7).
7. Track outcomes; share back with Jane after offer stage (success + lessons).

**Result:** 11 candidates → 5 screens → 2 onsites → 1 offer → 1 hire from /dev/color path within 8 weeks.

### Example 3: AfroTech conference recruiting plan
**Goal:** AfroTech 2026 in Houston, Nov 12-15. Sponsor tier confirmed Gold. Need conference plan.
**Steps:**
1. T-90d: confirm 6 attending staff (2 recruiters + 4 engineers); register all.
2. T-60d: book hotel block, design booth materials (banner + QR codes to careers page + 200 swag items).
3. T-45d: submit 1 Code Talk speaker proposal (eng manager); 1 panel proposal (VP Eng).
4. T-30d: pre-conference happy hour invitation list (50 contacts from Notion + LinkedIn 2nd-degree).
5. T-7d: attendee briefing — every staff is an ambassador; capture badge scans; same-day LinkedIn add.
6. Day-of: Recipe 5 workflow; aim for 80-120 conversations + 30 deep convos.
7. T+1 to T+7: every deep convo gets recruiter touch within 7 business days.
8. T+30: pull source = "Event: AfroTech 2026" from ATS; measure funnel; share retro with sponsorship team.

**Result:** 95 conversations → 30 deep convos → 18 in pipeline → 4 hires within 6 months. ROI computed: $50K sponsor + $20K travel + $10K booth = $80K / 4 hires = $20K cost-per-hire (vs $25-30K agency benchmark).

## Edge cases / gotchas

- **Diversity sourcing IS NOT a Q4 push.** It's a multi-quarter relationship investment. Showing up at AfroTech once and never again gets you exactly nothing.
- **Channels remember who sponsored vs who didn't.** Cycle through tiers + show year-over-year commitment; don't ghost.
- **Anti-pattern: lipservice ERG.** Posting "We're committed to diversity" with no sponsor budget or hiring outcomes is brand damage. Either commit or don't engage.
- **Never DM individual community members cold via channel Slack/Discord.** Channels are private trusted spaces. Use #jobs channel + warm intros from community managers.
- **Sponsor tier inflation is a budget trap.** Title sponsor of every event ≠ best ROI. Pick 2-3 channels at high tier; show up consistently; engage at meaningful tier elsewhere.
- **Comp transparency is non-negotiable** at diversity channels. Posting a role without comp band signals "we expect to lowball." Channels notice + word travels.
- **Diverse slate enforcement (Recipe 13) at finalist stage** is only valid if upstream sourcing has actually diversified. Cosmetic slate compliance late-stage is bias whitewashing.
- **Don't infer race / gender / orientation from name / photo / school.** Sourced via /dev/color = Black-identified (channel-attested). Sourced via Stanford = unknown. See role.md Antipattern 3.
- **Conference badge scans capture intent only.** A scan ≠ interested in this role. Triage signal at follow-up; don't assume all 200 scans are candidates.
- **Code2040 fellow conversion is not guaranteed.** 80% conversion if team + fellow click; ~30% if team is unprepared. Invest in mentor selection + project scope upfront.
- **Lesbians Who Tech / Out in Tech sometimes overlap.** Don't double-dip relationships; primary the engagement with one for cleanliness.
- **Tapia + Grace Hopper conferences clash in calendar (Sep-Oct).** Plan team coverage so both have presence.
- **Project Include is process, not pipeline.** Don't expect candidates from projectinclude.org; expect process upgrades.
- **AfroTech tier inflation (Title $500K+) only pays off** if you're consistently sourcing 10+ hires per year from the channel. Most companies should be Gold or Silver.
- **The "you wanted diverse pipeline but the comp band sucks" failure.** Diverse candidates have more options; comp must be competitive. Hand off comp band concerns to `ceo-agent` or `operations-agent`.
- **Don't request warm intros monthly.** Channel managers have their own load; quarterly cadence is the right rhythm.
- **The "we sponsored 4 events; got 0 hires" failure** = no follow-up workflow. Recipe 5 + Recipe 7 + Recipe 12 close the loop; skipping any of those = ROI zero.
- **Hand off AI-filter overlay** (SeekOut diversity filter / Findem attribute filter) to `amazinghiring-findem-seekout-diversity` — that's the algorithmic layer; this skill is the relationship layer.
- **Hand off the channel-source attribution + analytics** to `source-of-hire-reporting` — slice your hires by channel quarterly to inform sponsor budget.

## Sources

- /dev/color: https://devcolor.org
- Code2040: https://www.code2040.org
- Lesbians Who Tech: https://lesbianswhotech.org
- Black Founders Matter: https://blackfoundersmatter.com
- Out in Tech: https://outintech.com
- Latinas in Tech: https://latinasintech.org
- Out & Equal: https://www.outandequal.org
- AfroTech: https://www.afrotech.com
- Grace Hopper Celebration (AnitaB.org): https://ghc.anitab.org
- Tapia Conference (CMD-IT): https://tapiaconference.cmd-it.org
- Project Include recommendations: https://projectinclude.org/recommendations
- AnitaB.org: https://anitab.org
- Mindhunt — Diversity Sourcing Strategies 2026: https://mindhuntai.com/blog/diversity-sourcing-strategies
- Juicebox — SeekOut Reviews (diversity filter context): https://juicebox.ai/blog/seekout-reviews
