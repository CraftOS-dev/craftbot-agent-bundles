<!--
Sources: https://www.gem.com/blog/candidate-sourcing-software
         https://connectsafely.ai/articles/linkedin-inmail-templates-response-rates-2026
         https://salesflow.io/blog/linkedin-inmail-best-practices-improve-response-rates
         https://careery.pro/blog/recruiter-outreach-templates
         https://expandi.io/blog/linkedin-recruiter-message-templates/
3-5 step multi-touch sequences boost reply 3-5× vs single touches.
Segment by role + level + stage of current company.
A/B from step 1; pause on reply; re-enroll after 90 days for "not now".
-->
# Passive Candidate Outreach Campaigns — SKILL

Design + run 3-5 step multi-touch sequences for passive candidates. Segment first; A/B test from step 1; pause on reply; re-enroll after 90 days for "not now" responses. Multi-stage sequences boost reply rate 3-5× over single touches. Segmentation lifts another 2-3×.

## When to use

- User wants to **design an outreach sequence** for a new req or persona.
- User wants to **refine an underperforming sequence** (low reply rate, high drop-off mid-sequence).
- User wants to **segment a candidate list** before enrolling (don't blast same template to 500).
- User asks "what should my touches look like?" or "how many emails should I send?".
- Trigger phrases: "outreach sequence", "campaign design", "multi-touch", "segment candidates", "A/B test outreach", "low reply rate", "sequence didn't work".

Do not use for: authoring single InMail prose (`cold-inmail-warm-intro`); enrolling/managing in Gem/hireEZ/Beamery (`gem-hireez-beamery-talent-crm`); LinkedIn Boolean (`linkedin-recruiter-boolean-search-strings`).

## Setup

```bash
# This skill is template + design — operates via gem-hireez-beamery-talent-crm or gmail fallback.
# Required: at least one CRM key or gmail-mcp.
export GEM_API_KEY="xxx"            # primary
# OR
export HIREEZ_API_KEY="xxx"          # fallback
# OR
# gmail-mcp only — for <50 prospects/week
```

## Common recipes

### Recipe 1: Segmentation matrix (ALWAYS do this first)

Segment 500-candidate list along 3 axes before authoring sequences:

| Axis 1: Role family | Axis 2: Seniority | Axis 3: Current company stage |
|---------------------|-------------------|-------------------------------|
| Backend Eng | IC | Pre-seed / Seed |
| Frontend Eng | Senior IC | Series A-B |
| ML Eng | Staff / Principal | Series C-D |
| Eng Manager | Manager | Late / IPO'd |
| Product Designer | Director / VP | Megacap (Google / Meta / etc.) |

3 × 4 × 5 = 60 cells. Realistically, 5-8 cells contain >20 candidates. Author 1 sequence template per cell with role-cell-specific hook.

### Recipe 2: 5-touch engineering sequence (passive, default)

| # | Day | Channel | Format | Goal | Char limit |
|---|-----|---------|--------|------|------------|
| 1 | 0 | LinkedIn InMail | <400 char, profile-view-first | First-touch context + role fit signal | 350 |
| 2 | 4 | Gmail | Reply to thread; add 1 specific point + value (link to eng blog) | Reinforce + reduce ambiguity | 200 |
| 3 | 9 | LinkedIn message (different angle) | Open-source / tech-stack-specific question | Different hook angle | 280 |
| 4 | 16 | Gmail | Soft break-up: "if not now, OK to circle back in 6 mo?" | Open future door | 220 |
| 5 | 30 | LinkedIn message | Final touch: link to recent product launch + open invite | Last opportunity | 180 |

Pause sequence on any reply. Re-enroll after 90 days for "not now" responses.

### Recipe 3: 4-touch sales sequence (faster cadence, comp upfront)

| # | Day | Channel | Format | Goal |
|---|-----|---------|--------|------|
| 1 | 0 | LinkedIn InMail | <400 char, comp transparency, RepVue benchmark cite | First-touch with $$ data |
| 2 | 3 | Gmail | Reply with 1-pager on deal sizes / quota / OTE | Concrete proof |
| 3 | 7 | LinkedIn message | "If timing's off, OK to refer me to a peer who'd be a fit?" | Open referral lane |
| 4 | 14 | Gmail | Break-up: "leaving this open" | Polite close |

Sales candidates value speed + transparency. 14-day window vs eng's 30-day.

### Recipe 4: 3-touch executive sequence (warm intro non-negotiable)

| # | Day | Channel | Format | Goal |
|---|-----|---------|--------|------|
| 1 | 0 | Warm intro via mutual board member / investor (preferred) | High-context email | Trust transfer + brief |
| 2 | 7 | Direct cold InMail OR follow-up to warm path | <400 char, role + comp range | Direct ask |
| 3 | 21 | Calendar link / "any 30 min in next 2 weeks?" | Frictionless next step | Book |

Execs ignore cold sequences. Warm intro at step 1 is non-negotiable. See `cto-vp-eng-exec-sourcing` for full playbook.

### Recipe 5: 3-touch design sequence (portfolio-anchored)

| # | Day | Channel | Format | Goal |
|---|-----|---------|--------|------|
| 1 | 0 | LinkedIn InMail | <400 char, reference specific Behance/Dribbble project | Show you actually saw their work |
| 2 | 5 | Email | Attach JD + a 1-page brief of design challenges (concrete) | Designer attraction |
| 3 | 14 | LinkedIn message | "If now isn't right, what would make a future role compelling for you?" | Open feedback lane |

### Recipe 6: A/B test design (step-1 subject + opener)

```python
# Pseudo — split 200 prospects into 2 groups of 100; track reply rate per group
import random

prospects = load_csv("staff_backend_q3.csv")
random.shuffle(prospects)

template_a = {
    "subject": "Your {oss_project} work",
    "opener": "Hi {first} — saw your recent commits to {oss_project}; the {specific_pr} change was clever."
}
template_b = {
    "subject": "{first}, quick thought",
    "opener": "Hi {first} — your work on {company_recent_project} was sharp."
}

for i, p in enumerate(prospects):
    arm = "A" if i % 2 == 0 else "B"
    template = template_a if arm == "A" else template_b
    gem.enroll(p, sequence=f"staff-backend-{arm}", tokens={**p, **template})
    notion.tag(p["id"], f"ab-arm-{arm}")

# After 14 days: query Gem analytics per arm; pick winner if delta > 30%; re-enroll losers in winner template
```

Minimum sample size per arm: 30. Below that, noise dominates and "winner" is statistical artifact.

### Recipe 7: Token map per segment (the actual personalization lever)

For each segment, define the token map BEFORE drafting templates:

```yaml
segment: "staff-backend-series-bc"
tokens:
  first: "{candidate.first_name}"
  oss_project: "{candidate.top_starred_repo}"        # from GitHub mining
  specific_pr: "{candidate.most_recent_merged_pr}"   # from GitHub commit history
  recent_funding: "{candidate.current_company.last_round}"  # from Crunchbase
  domain: "infrastructure"
  your_co: "Acme"
  recruiter: "Sarah Chen"
```

If any required token is unset for a prospect → kick to manual outreach pile. Don't send templates with `{oss_project}` literally in the body.

### Recipe 8: Reply triage taxonomy (what to do with each response)

| Reply type | Action | Tag | Re-enroll? |
|------------|--------|-----|-----------|
| "Yes, interested" | Calendar link within 2h | `replied_interested` | n/a |
| "Maybe / tell me more" | Reply with 1-pager + scheduling | `replied_maybe` | n/a |
| "Not now / not interested" | Polite thanks; tag for 90-day re-enroll | `replied_not_now` | yes, +90d |
| "Already in process at competitor" | Tag; pause for 6 mo; circle back | `replied_in_process` | yes, +180d |
| "Take me off list" | Honor immediately; ADD to suppression list | `replied_unsub` | NEVER |
| Auto-reply (out-of-office) | Pause sequence; resume after return date | `auto_reply_ooo` | resume |
| No reply after step 5 | Tag for re-enroll in 6 mo with new angle | `no_reply` | yes, +180d |

### Recipe 9: 90-day re-enrollment workflow

```bash
# Weekly cron: find prospects tagged "replied_not_now" or "no_reply" where last_touch > 90d
curl "https://api.gem.com/v1/prospects?tags=replied_not_now,no_reply&last_touch_lt=$(date -d '90 days ago' +%Y-%m-%d)" \
  -H "Authorization: Bearer $GEM_API_KEY"

# For each match: enroll in a FRESH sequence (different angle — new role, new funding event, new product launch)
# Never re-enroll in the same template — the cold-opener becomes warm-opener variant
```

### Recipe 10: Sequence performance benchmarks (when to investigate)

| Metric | Healthy | Investigate at |
|--------|---------|----------------|
| Step 1 open rate | 50-70% | <40% → subject line problem |
| Step 1 reply rate | 8-15% (eng), 10-15% (sales), 12-18% (HR/PM) | <5% → segmentation / template fit |
| Step 2-3 reply lift | +30-50% cumulative | <20% lift → step 2 not adding value |
| Step 4-5 reply lift | +10-20% cumulative | <5% lift → fatigue; cut to 3-step |
| Cumulative sequence reply rate | 25-40% | <15% → wholesale redesign |
| Reply-to-screen pass rate | 50-70% | <30% → mis-segmenting (wrong-fit replies) |

## Examples

### Example 1: Refine a 4% reply rate sequence
**Goal:** User's step-1 InMail at 4% reply (benchmark: 8-15%). Diagnose and fix.
**Steps:**
1. Pull sample of 20 sent step-1 InMails.
2. Check subject line: is it 16-27 chars? Is it specific (mentions candidate's work)?
3. Check char count: <400? Profile-view-first executed?
4. Check segmentation: are all 20 the same role family / seniority / company stage? If not, sequence is too generic.
5. Hypothesis: subject is generic ("Job opportunity"). Rewrite to "{first}, your {oss_project} work" + re-enroll.
6. A/B test for 14 days.

**Result:** Subject lift typically +40-80% on personalized vs generic. Reply rate should rise to 8-12%.

### Example 2: Design a sequence for a new niche role (GPU kernel engineer)
**Goal:** New req — GPU kernel engineer (CUDA + Triton). No existing template.
**Steps:**
1. Define segments: (a) FAANG GPU kernel ICs (10-15 candidates), (b) Top-rep SO `cuda` taggers (20 candidates), (c) PyTorch/Triton contributors (30 candidates). 3 segments.
2. Per segment, author 1 step-1 InMail referencing source-specific signal:
   - Segment A: "Saw your {patent_filed} work on the H100 schedulers" (uses Findem `patents_filed` filter).
   - Segment B: "Your StackOverflow CUDA answers on warp-divergence" (Stack Overflow attribute).
   - Segment C: "Your recent commits to PyTorch eager-mode" (GitHub commit signal).
3. 5-touch eng sequence (Recipe 2) per segment.
4. Token map per segment (Recipe 7).
5. Enroll all 3 segments simultaneously; track per-segment reply rate.

**Result:** Per-segment reply rate variance reveals which channel is strongest for niche role; double-down on winner.

### Example 3: Auto-pause sequence when candidate accepts at competitor
**Goal:** Candidate enrolled in sequence; LinkedIn job-change alert fires showing they joined Stripe.
**Steps:**
1. SeekOut / Gem LinkedIn change alert triggers (recipient subscribed).
2. Auto-pause sequence; tag `joined_competitor_{date}`.
3. Schedule 12-month re-engage (alumni-style — different sequence template; "wanted to congrats on Stripe; if scope wasn't right, here's what we're working on" style).
4. Add to `boomerang-alumni-re-engagement` hot-list with `external-alumni-{company}` tag.

**Result:** No wasted sends; future re-engage at peak signal (12-18 months in).

## Edge cases / gotchas

- **Single-template-blast at 500 candidates = <2% reply rate.** Segment first. Always. (Antipattern 2 in role.md.)
- **A/B winner declared at N<30 per arm is noise, not signal.** Wait for sample size.
- **Step-1 subject line ALWAYS drives the open-rate funnel.** Optimize subject FIRST; everything else is downstream.
- **Reply-to-screen pass rate <30% means wrong-fit replies** — sequence too broad; tighten segment criteria.
- **Long sequences (6+ touches) annoy.** Stop at 5. Reply lift past step 5 is <5%.
- **Don't send all touches on LinkedIn.** Mix in email — different channels avoid same-feed fatigue. Gem/hireEZ both support this.
- **Pause sequence on auto-reply (out-of-office).** Resume after return date OR after 14 days. Continuing through OOO wastes touches.
- **Unsubscribe requests must be honored within 10 business days (CAN-SPAM).** Add to suppression list at the platform level (Gem/hireEZ/Beamery all support).
- **GDPR / EU candidates require explicit lawful-basis** for outreach. Cold outreach OK for legitimate-interest under recital 47; reply-with-unsub flow required. Defer compliance review to `operations-agent`.
- **Cap touches per LinkedIn account at 30 InMails/week.** Beyond that, LinkedIn flags. Distribute across multiple recruiter seats if higher volume needed.
- **Token map gaps must hard-fail enrollment.** Sending `Hi {first}, saw your work on {oss_project}` literally is catastrophic for sender reputation + brand.
- **90-day re-enrollment requires a FRESH angle.** Re-enrolling in the same template = annoyance. New role, new event, new framing.
- **Sequence analytics need 14-21 days to settle.** Reply distribution is long-tailed; calling winner at day 7 typically misreads.
- **For "we don't have CRM seat":** Gmail-fallback (Recipe 9 in `gem-hireez-beamery-talent-crm`) caps at 50/day; if higher needed, invest in Gem $200-400/mo.
- **Hand off to `gem-hireez-beamery-talent-crm`** for actual platform enrollment. This skill designs sequences; that skill ships them.
- **Hand off to `cold-inmail-warm-intro`** for individual InMail prose authoring on the highest-priority candidates (where templates fall short).

## Sources

- Gem — Best Candidate Sourcing Software 2026: https://www.gem.com/blog/candidate-sourcing-software
- ConnectSafely — LinkedIn InMail Templates Response Rates 2026: https://connectsafely.ai/articles/linkedin-inmail-templates-response-rates-2026
- Salesflow — LinkedIn InMail Best Practices 2026: https://salesflow.io/blog/linkedin-inmail-best-practices-improve-response-rates
- Careery — Recruiter Outreach Templates 2026: https://careery.pro/blog/recruiter-outreach-templates
- Expandi — Best LinkedIn Recruiter Message Templates 2026: https://expandi.io/blog/linkedin-recruiter-message-templates/
- Metaview — Sourcing Tools 2026 (multi-stage benchmarks): https://www.metaview.ai/resources/blog/sourcing-tools-for-recruiters
