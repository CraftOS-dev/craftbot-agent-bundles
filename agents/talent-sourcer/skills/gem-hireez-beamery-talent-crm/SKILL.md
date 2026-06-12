<!--
Sources: https://www.selectsoftwarereviews.com/reviews/gem
         https://www.gem.com/blog/candidate-sourcing-software
         https://explore.hireez.com/blog/how-to-source-candidates-on-github/
         https://beamery.com/platform/talent-acquisition/talent-crm/
         https://www.metaview.ai/resources/blog/sourcing-tools-for-recruiters
Gem — 800M+ DB + sequence + Chrome ext; best for high-growth in-house outbound.
hireEZ — AI Boolean Builder + 45+ source agg + sequencer; mid-market budget.
Beamery — enterprise CRM (CHRO grade) + deep ATS/HRIS integrations.
-->
# Gem / hireEZ / Beamery — Talent CRM — SKILL

Run the talent-CRM layer: candidate database, sequence enrollment, ATS push, analytics. Gem for high-growth in-house teams (800M+ DB + Chrome extension). hireEZ for mid-market (AI Boolean + 45+ sources). Beamery for enterprise (CHRO grade + global TA). All three expose REST APIs for sequence + prospect + ATS push.

## When to use

- User wants to **enroll candidates in a multi-touch sequence** (3-5 step).
- User wants to **manage hot-list / talent community** at scale (>100 prospects).
- User wants to **push sourced candidates to ATS** on Applied stage with source attribution.
- User wants **per-sequence analytics** (reply rate, open rate, sequence completion).
- Trigger phrases: "enroll in sequence", "talent CRM", "Gem sequence", "hireEZ outreach", "Beamery enroll", "push to Greenhouse", "sequence analytics".

Do not use for: authoring the InMail prose (`cold-inmail-warm-intro` + `passive-candidate-outreach-campaigns`); LinkedIn Boolean string itself (`linkedin-recruiter-boolean-search-strings`); ATS interview-pipeline workflows — those defer to parent `operations-agent`'s `hiring-pipeline-greenhouse-ashby-lever` skill.

## Setup

```bash
# Gem — paid seat ~$200-400/user/mo; high-volume tiers higher.
# https://app.gem.com/settings/api
export GEM_API_KEY="xxx"

# hireEZ — paid seat ~$250-450/user/mo.
# https://app.hireez.com/settings/api
export HIREEZ_API_KEY="xxx"

# Beamery — enterprise contract; pricing via sales.
# https://app.beamery.com/settings/api
export BEAMERY_API_KEY="xxx"

# ATS keys for push-to-ATS recipes.
export GREENHOUSE_API_KEY="harvest_xxx"
export ASHBY_API_KEY="xxx"
export LEVER_API_KEY="xxx"
```

## Common recipes

### Recipe 1: Gem — create a sequence (3-step outreach)

```bash
curl -X POST "https://api.gem.com/v1/sequences" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Staff Backend - 2026Q3",
    "owner_email": "recruiter@yourco.com",
    "steps": [
      {
        "day": 0,
        "channel": "linkedin_inmail",
        "subject": "Your {oss_project} work",
        "body": "Hi {first} — saw your recent commits to {oss_project}; the {specific_pr_or_feature} change was clever. We are hiring a staff platform eng to lead our {your_domain} infra. Worth 20 min to compare notes? Best, {recruiter}"
      },
      {
        "day": 4,
        "channel": "email",
        "subject": "Re: {previous_subject}",
        "body": "Following up — adding our engineering blog: {blog_url}. Specifically the post on {specific_topic} maps directly to the role. Worth a quick chat? Best, {recruiter}"
      },
      {
        "day": 11,
        "channel": "linkedin_message",
        "subject": "{first} — one last thought",
        "body": "Soft-breakup time. If now isn'\''t right, want me to circle back in 6 mo when {your_co} ships {upcoming_milestone}? Best, {recruiter}"
      }
    ]
  }'
```

### Recipe 2: Gem — enroll a prospect in a sequence

```bash
# Single prospect
curl -X POST "https://api.gem.com/v1/sequences/{sequence_id}/enroll" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  -d '{
    "prospect_id": "{id}",
    "start_step": 1,
    "tokens": {
      "oss_project": "ray",
      "specific_pr_or_feature": "scheduler eviction patch",
      "your_domain": "ML platform",
      "your_co": "Acme",
      "recruiter": "Sarah Chen"
    }
  }'

# Bulk enroll (up to 50 per call)
curl -X POST "https://api.gem.com/v1/sequences/{sequence_id}/enroll_batch" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  -d '{
    "prospects": [
      {"prospect_id": "p1", "tokens": {...}},
      {"prospect_id": "p2", "tokens": {...}}
    ]
  }'
```

### Recipe 3: Gem — pause sequence on reply

Gem auto-pauses sequences when a prospect replies (any channel). Verify via:

```bash
curl "https://api.gem.com/v1/prospects/{prospect_id}/sequences" \
  -H "Authorization: Bearer $GEM_API_KEY"

# Response: status == "paused_replied" when reply detected
```

If the API hasn't caught the reply (rare, ~2-5% miss rate), force pause:

```bash
curl -X POST "https://api.gem.com/v1/sequences/{sequence_id}/pause" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  -d '{"prospect_id": "{id}", "reason": "manual_reply_received"}'
```

### Recipe 4: Gem — tag for hot-list segmentation

```bash
curl -X POST "https://api.gem.com/v1/prospects/{prospect_id}/tags" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  -d '{"tags": ["hot-list-eng-staff-3mo", "diversity-channel-devcolor", "target-account-stripe"]}'

# Query hot-list when a req opens
curl "https://api.gem.com/v1/prospects?tags=hot-list-eng-staff-3mo,hot-list-eng-staff-6mo&last_touch_gt=30days&limit=200" \
  -H "Authorization: Bearer $GEM_API_KEY"
```

### Recipe 5: Gem — sequence analytics + A/B comparison

```bash
# Per-step analytics
curl "https://api.gem.com/v1/sequences/{sequence_id}/analytics" \
  -H "Authorization: Bearer $GEM_API_KEY"

# Response:
# {
#   "step_1": {"sent": 200, "opened": 110, "replied": 28, "open_rate": 0.55, "reply_rate": 0.14},
#   "step_2": {"sent": 172, "opened": 95, "replied": 12, ...},
#   ...
# }

# A/B test — two sequences with different subject lines
curl -X POST "https://api.gem.com/v1/sequences/ab_test" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  -d '{
    "sequence_a_id": "{id1}",
    "sequence_b_id": "{id2}",
    "split": 0.5,
    "duration_days": 14
  }'
```

### Recipe 6: Gem — push prospect to ATS on Applied

```bash
# Greenhouse — Gem has native integration; configure once, auto-push on stage change.
# Manual push:
curl -X POST "https://api.gem.com/v1/prospects/{prospect_id}/push_to_ats" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  -d '{
    "ats": "greenhouse",
    "job_id": "{greenhouse_job_id}",
    "source_id": "{greenhouse_source_id}",
    "stage": "Application Review"
  }'

# Direct Greenhouse fallback (when Gem integration not configured)
curl -X POST "https://harvest.greenhouse.io/v1/candidates" \
  -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: {user_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "{first}",
    "last_name": "{last}",
    "email_addresses": [{"value": "{email}", "type": "personal"}],
    "social_media_addresses": [{"value": "{linkedin_url}"}],
    "applications": [{"job_id": {job_id}, "source_id": {source_id}}]
  }'
```

### Recipe 7: hireEZ — AI Boolean Builder + sequencer

```bash
# Generate Boolean from JD (covered in linkedin-recruiter-boolean-search-strings, Recipe 12)
curl -X POST "https://api.hireez.com/v1/boolean/generate" \
  -H "Authorization: Bearer $HIREEZ_API_KEY" \
  -d '{"job_description": "<full JD>", "platform": "linkedin"}'

# Enroll prospects in a hireEZ sequence
curl -X POST "https://api.hireez.com/v1/sequences/{seq_id}/enroll" \
  -H "Authorization: Bearer $HIREEZ_API_KEY" \
  -d '{
    "prospect_ids": ["p1", "p2"],
    "tokens": {"first": "Jane", "role": "Staff Backend"}
  }'

# hireEZ supports 12-channel outreach (email, LinkedIn, SMS, etc.)
curl "https://api.hireez.com/v1/sequences/{seq_id}/analytics" \
  -H "Authorization: Bearer $HIREEZ_API_KEY"
```

### Recipe 8: Beamery — enterprise CRM workflow

```bash
# Create a Beamery campaign (Beamery's term for sequence)
curl -X POST "https://api.beamery.com/v1/campaigns" \
  -H "Authorization: Bearer $BEAMERY_API_KEY" \
  -d '{
    "name": "Staff Backend Pipeline Q3",
    "owner": "recruiter@yourco.com",
    "messages": [
      {"day": 0, "channel": "email", "template_id": "{template_id_1}"},
      {"day": 5, "channel": "linkedin", "template_id": "{template_id_2}"}
    ]
  }'

# Enroll talent pool
curl -X POST "https://api.beamery.com/v1/campaigns/{id}/enroll" \
  -H "Authorization: Bearer $BEAMERY_API_KEY" \
  -d '{"talent_pool_id": "{pool_id}"}'

# Pull CRM-wide analytics (Beamery's strength vs Gem)
curl "https://api.beamery.com/v1/analytics/funnel?period=30d&segment_by=source" \
  -H "Authorization: Bearer $BEAMERY_API_KEY"
```

### Recipe 9: Gmail-only fallback when no CRM seat

When recipient has no Gem / hireEZ / Beamery, fall back to `gmail-mcp` low-scale sequencing:

```python
# Pseudo — agent-side via gmail-mcp + notion-mcp candidate DB
prospects = notion.query("Hot list", filter={"tag": "eng-staff"})

for p in prospects[:50]:  # cap at 50/day to avoid spam flags
    # Step 1 — email today
    gmail.send(to=p["email"], subject=f"Your {p['oss_project']} work",
               body=template_step1.format(**p))
    notion.update(p["id"], {"last_touch": today(), "sequence_step": 1, "next_touch_due": today() + 4})

# Cron next day — find prospects whose next_touch_due == today, send step 2
due = notion.query("Hot list", filter={"next_touch_due": today(), "sequence_step": {"<": 5}})
for p in due:
    gmail.send(to=p["email"], subject=f"Re: {p['oss_project']}",
               body=templates[p["sequence_step"] + 1].format(**p))
    notion.update(p["id"], {"sequence_step": p["sequence_step"] + 1,
                            "next_touch_due": today() + intervals[p["sequence_step"]]})
```

Cap at 50 emails/day per sender → 250-300/week. Beyond that you need a CRM seat for sender-reputation management.

### Recipe 10: Per-source attribution at ATS push

When pushing to ATS, ALWAYS set the source field:

```bash
# Greenhouse — source_id maps to Configure → Sources
# Common values: 1=LinkedIn, 2=Referral, 3=Gem, 4=hireEZ, 5=Boomerang, 6=Diversity Channel
# Pull source list once and cache:
curl "https://harvest.greenhouse.io/v1/sources" -u "$GREENHOUSE_API_KEY:"

# Ashby — sourceId set via candidate.create body
# Pull source list:
curl -X POST "https://api.ashbyhq.com/source.list" -u "$ASHBY_API_KEY:"

# Lever — sources is an array on candidate
# Pull tags + sources:
curl "https://api.lever.co/v1/sources" -u "$LEVER_API_KEY:"
```

Source attribution at push = source-of-hire reporting works. Skipped = `source-of-hire-reporting` skill can't function (Antipattern 6 in role.md).

## Examples

### Example 1: Build + enroll a 5-step Gem sequence for 100 staff backend prospects
**Goal:** Source 100 staff backend engineers → enroll all in a 5-step sequence with A/B subject test.
**Steps:**
1. `linkedin-recruiter-boolean-search-strings` → 100 candidates in CSV.
2. Upload CSV to Gem → bulk-add as prospects with `source = "LinkedIn Recruiter"`.
3. Create Sequence A (subject: "Your {oss_project} work") + Sequence B (subject: "{first}, quick thought") (Recipe 1).
4. A/B split enrollment 50/50 (Recipe 5).
5. Tag all with `hot-list-eng-staff-3mo`, `target-account-{company}` (Recipe 4).
6. Monitor analytics for 14 days; pick winner; re-enroll the 50 in losing arm.

**Result:** A/B winner identified within 14 days; reply-rate lift typically +30-50% for winning subject; rest of pipeline funneled through winning template.

### Example 2: Push 30 prospects to Greenhouse with source attribution
**Goal:** Move 30 Gem prospects who replied "interested" into Greenhouse Applied stage.
**Steps:**
1. Query Gem for prospects: `status=replied_positive, sequence_id={id}`.
2. For each: pull profile + email + LinkedIn.
3. Greenhouse `POST /v1/candidates` (Recipe 6) with `source_id` = Gem source ID.
4. Tag in Gem: `pushed_to_ats=true, ats_id={greenhouse_id}`.
5. Hand off to `operations-agent` for interview scheduling.

**Result:** 30 prospects in Greenhouse with proper source attribution; sourcer drops out of pipeline; recruiter coord owns from here.

### Example 3: Hot-list query when new req opens
**Goal:** Don't cold-source; query hot-list first (Antipattern 4 in role.md).
**Steps:**
1. New req opens: Staff Backend, 3-month start.
2. Query Gem (Recipe 4): `tags=hot-list-eng-staff-3mo OR hot-list-eng-staff-6mo, last_touch_gt=30days`.
3. Pull 40 matches → personalize hook with new-req context.
4. Enroll in priority sequence (shorter, more direct: 3-step vs 5).
5. THEN start cold sourcing for the gap (per `source-diversification-3-sources-per-role`).

**Result:** 8-12 hot-list candidates engaged within day 1; 3-5× faster than cold-only sourcing; nurture investment pays off.

## Edge cases / gotchas

- **Gem auto-pauses on reply but reply-detection has ~2-5% miss rate.** Always verify before next send if prospect has interacted on a different channel. Force-pause manually if needed (Recipe 3).
- **hireEZ AI Boolean Builder output is LinkedIn-flavored** — paste-ready into Recruiter; needs reformatting for Sales Nav (different operator syntax) or SeekOut.
- **Beamery enterprise contract typically requires SSO + DPA + 50+ seat commit.** Not viable for startups; switch to Gem.
- **Sequence subject + body tokens unset = literal `{token}` in send.** Pre-validate all token map keys present per prospect; reject enrollment if any required token missing.
- **Gmail-fallback sender reputation tanks at >100 cold emails/day from one address.** Cap at 50; rotate across 2-3 sender addresses if higher volume needed.
- **Source attribution at ATS push is the most-skipped step.** Auto-fail without it (`source-of-hire-reporting` can't function). Hard-block ATS push if `source_id` not set.
- **Gem + hireEZ + Beamery all auto-dedupe by email.** Adding same email twice updates existing prospect; doesn't create dupe. Safe to re-upload CSV.
- **LinkedIn InMail sent via Gem still consumes your Recruiter InMail quota.** 150/mo (Recruiter Corporate). Plan against.
- **Sequence pauses on reply BUT replies on a different channel may not pause** (e.g., InMail reply pauses LinkedIn step but not email steps in some legacy Gem configs). Verify via test enrollment.
- **A/B testing requires sample size ≥30 per arm for statistical signal.** Don't conclude winner with N=10 per arm; reply-rate noise dominates.
- **hireEZ's 12-channel outreach includes SMS** — only legal where candidate consented (TCPA / CAN-SPAM). Default to LinkedIn + email; enable SMS only with explicit opt-in.
- **Beamery's CRM-wide analytics aggregate across all campaigns** — useful for org-level reporting but slow to load (10-30s queries). Cache results for daily dashboard.
- **Defer ATS workflow** (interview scheduling, scorecards, offers) to parent `operations-agent`'s `hiring-pipeline-greenhouse-ashby-lever` skill — this skill stops at Applied push.
- **Cap monthly outreach per sequence at 2,000.** Beyond that, sender domain reputation degrades + LinkedIn account-flag risk rises sharply.

## Sources

- SelectSoftware Reviews — Gem Expert Review 2026: https://www.selectsoftwarereviews.com/reviews/gem
- Gem — Best Candidate Sourcing Software 2026: https://www.gem.com/blog/candidate-sourcing-software
- hireEZ — Complete Guide to Source Candidates on GitHub (AI Boolean Builder): https://explore.hireez.com/blog/how-to-source-candidates-on-github/
- Beamery — Talent CRM Platform 2026: https://beamery.com/platform/talent-acquisition/talent-crm/
- Metaview — Top 10 Sourcing Tools for Recruiters 2026: https://www.metaview.ai/resources/blog/sourcing-tools-for-recruiters
- Greenhouse Harvest API: https://developers.greenhouse.io/harvest.html
- Ashby API: https://developers.ashbyhq.com/
- Lever API: https://hire.lever.co/developer/documentation
