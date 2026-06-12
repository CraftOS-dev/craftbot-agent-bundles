<!--
Sources:
Dovetail v3 API — https://dovetail.com/help/api
Daniel Pidcock — Atomic UX Research — https://www.atomicresearch.co
Dovetail — atomic research blog — https://dovetail.com/blog/atomic-research
Notably (alt) — https://notably.ai
Marvin (alt) — https://heymarvin.com
-->
# Dovetail Research Repository — SKILL

Dovetail v3 as the canonical research repository. Atomic UX research model (Pidcock): Experiments → Facts → Insights → Conclusions. Tag taxonomy with naming convention. Persona-link every quote. Stakeholders self-serve from the repo. Notably (free) and Marvin (AI-first) are alts.

## When to use

- Setting up or maintaining a research repository.
- Synthesizing 5-25 transcripts after a research round.
- Building / maintaining canonical tag taxonomy.
- Publishing insights that stakeholders self-serve.
- Migrating from ad-hoc Notion docs to a real research repo.

Trigger phrases: "synthesize these transcripts", "set up Dovetail", "research repository", "atomic UX", "tag taxonomy", "insight library", "self-serve research".

## Setup

```bash
# Dovetail
curl -fsSL "https://dovetail.com/api/v1/me" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN"

# Notably (free alt)
curl -fsSL "https://api.notably.ai/v1/me" \
  -H "Authorization: Bearer $NOTABLY_API_TOKEN"

# Marvin (AI-first alt)
curl -fsSL "https://api.heymarvin.com/v1/me" \
  -H "Authorization: Bearer $MARVIN_API_TOKEN"
```

Auth + cost:
- `DOVETAIL_API_TOKEN` — Settings → API. Paid ~$199/mo+.
- `NOTABLY_API_TOKEN` — free tier available.
- `MARVIN_API_TOKEN` — paid; AI auto-tagging stronger.

## Common recipes

### Recipe 1: Atomic UX research model (Pidcock)

```markdown
# Atomic UX research layers

| Layer | What | Example |
|---|---|---|
| **Experiments** | The studies — interviews, usability tests, tree tests | "Q3 founder JTBD — 12 interviews" |
| **Facts** | Raw observations — quotes tagged at highlight level | "I miss replies daily." — P7 @ 12:30 |
| **Insights** | Synthesized themes from facts | "Inbox-overload pain mentioned in 9 of 12 founder interviews" |
| **Conclusions** | Recommendations from insights | "Scope notifications surface; measure reply-time before/after" |

# In Dovetail:
- Experiment = Project
- Facts = Highlights (quote-level)
- Insights = Insight cards
- Conclusions = linked from Insight to Linear / Notion
```

### Recipe 2: Tag taxonomy structure

```markdown
# Tag taxonomy — naming convention

## Hierarchical pattern: <type>/<topic>/<specific>

## Theme tags (top-level — the patterns)
- theme/inbox-overload
- theme/setup-friction
- theme/value-discovery

## Sub-theme tags (specifics inside a theme)
- theme/inbox-overload/missed-reply
- theme/inbox-overload/false-priority

## Persona tags
- persona/solo-founder
- persona/team-lead
- persona/enterprise-buyer

## Stage tags (when in journey)
- stage/discovery
- stage/onboarding
- stage/activation
- stage/retention
- stage/expansion

## Affect tags (emotional valence)
- affect/pain
- affect/delight
- affect/confusion
- affect/relief

## Method tags (where it came from)
- method/jtbd-interview
- method/usability
- method/diary
- method/nps-comment
- method/support-ticket
```

### Recipe 3: Create a Dovetail project

```bash
PROJECT_ID=$(curl -fsSL -X POST "https://dovetail.com/api/v1/projects" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Inbox-overload generative — Q3 2026",
    "template": "interview_study",
    "tags": ["method/jtbd-interview", "stage/discovery"]
  }' | jq -r '.data.id')

echo "$PROJECT_ID"
```

### Recipe 4: Upload transcript

```bash
# Upload audio/video file (Dovetail auto-transcribes via Whisper)
curl -X POST "https://dovetail.com/api/v1/projects/$PROJECT_ID/transcripts/upload" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
  -F "file=@interview-P3.mp4" \
  -F "participant_name=P3" \
  -F "session_date=2026-06-15"

# Or upload existing transcript (VTT / SRT / text)
curl -X POST "https://dovetail.com/api/v1/projects/$PROJECT_ID/notes" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
  -F "file=@transcript-P3.vtt" \
  -F "participant_name=P3"
```

### Recipe 5: Auto-tag via Dovetail AI

```bash
# Dovetail Magic (AI tagging) — accepts existing taxonomy
curl -X POST "https://dovetail.com/api/v1/projects/$PROJECT_ID/auto_tag" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
  -d '{
    "tags": [
      "theme/inbox-overload",
      "theme/setup-friction",
      "affect/pain",
      "affect/delight"
    ],
    "scope": "all_transcripts"
  }'

# Human-review the AI tags — accept / reject / refine
```

### Recipe 6: Query highlights by tag

```bash
# All quotes for "inbox-overload" theme
curl -fsSL "https://dovetail.com/api/v1/projects/$PROJECT_ID/highlights?tag=theme/inbox-overload" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
| jq '{
    count: (.highlights | length),
    unique_participants: (.highlights | map(.participant_id) | unique | length),
    top_quotes: [.highlights[:5] | .[] | {
      participant: .participant_id,
      quote: .text,
      timestamp,
      url: .dovetail_url
    }]
  }'
```

### Recipe 7: Create canonical Insight card

```bash
# Insight = the synthesized theme (Atomic Layer 3)
curl -X POST "https://dovetail.com/api/v1/projects/$PROJECT_ID/insights" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
  -d '{
    "title": "Inbox-overload pain dominates morning workflow for solo founders",
    "summary": "9 of 12 founders cited inbox overload as primary morning friction. Pattern: open Slack → check Gmail → switch to paper notebook for to-dos.",
    "evidence_highlight_ids": ["hl_123", "hl_456", "hl_789", "hl_abc"],
    "recommendation": "Scope a unified notifications surface that reduces inbox-overload by surfacing priority emails alongside Slack DMs.",
    "owner": "researcher@yourco.com",
    "linked_linear_issue": "https://linear.app/yourco/issue/PROD-1234"
  }'
```

### Recipe 8: Synthesis procedure (paste-ready)

```markdown
# Synthesis procedure (per research round)

## 1. Source the transcripts (within 24h of last session)
- Upload all transcripts to Dovetail (Recipe 4)
- Tag each with `persona/`, `method/`, `stage/`

## 2. First-pass tag (1-2 days)
- Read each transcript fully
- Tag quotes at highlight level
- Use existing taxonomy where possible; create new tags sparingly
- Dovetail AI suggests; you clean up

## 3. Cluster tags into themes (half day)
- Group similar tags
- Rename to behavior-led labels (not jargon)
- Cap at ≤7 themes per study

## 4. Pull verbatims per theme (1 hour)
- 2-3 quotes per theme
- Include source: P-ID + timestamp + Dovetail URL
- Confirm cross-participant (not single-voice)

## 5. Count theme occurrences (1 hour)
- "9 of 12 founders mentioned" — actual count from tag query
- Multi-mention per participant = still 1 (don't double-count)

## 6. Name the recommendation per theme (1 hour)
- More research / scope / measure / deprioritize
- Per-theme owner + ETA

## 7. Publish Insight + Readout (1 day)
- Dovetail insight card per theme (Recipe 7)
- Notion readout linking back to insights
```

### Recipe 9: Repository "front page" — Notion narrative

```markdown
# Research Repository — Front Page (Notion)

## How to use this repo

### Find an answer
- Search by tag: [Dovetail saved searches link]
- Browse by persona: [persona pages]
- Browse by stage: [journey-stage pages]

### Cite in your PRD
- Every insight has a stable Dovetail URL
- Quote + link in PRD evidence section
- See `customer-journey-service-blueprint` for journey artifacts

## Personas
[Link to each persona doc]

## Journey maps
[Link to each journey map]

## Active studies
[Live table from Notion DB — projects in flight]

## Recent insights (last 30 days)
[Live table from Dovetail API → Notion]

## Tag taxonomy
[Living reference — Recipe 2]

## Office hours
[Schedule — researcher available for PM consults]
```

### Recipe 10: Notably / Marvin fallback

```bash
# Notably (free) — same atomic model
curl -X POST "https://api.notably.ai/v1/projects" \
  -H "Authorization: Bearer $NOTABLY_API_TOKEN" \
  -d '{"name": "Inbox JTBD Q3"}'

# Marvin (AI-first) — auto-extract themes
curl -X POST "https://api.heymarvin.com/v1/sessions" \
  -H "Authorization: Bearer $MARVIN_API_TOKEN" \
  -F "file=@interview-P3.mp4" \
  -F "auto_tag=true"

# Notably for budget-constrained orgs; Marvin for AI-first speed
```

## Examples

### Example 1: Set up the repository from scratch
**Goal:** Migrate from scattered Notion docs to a real research repo.

**Steps:**
1. Set up Dovetail workspace (manual).
2. Build tag taxonomy (Recipe 2) — document in Notion.
3. Build "front page" (Recipe 9).
4. Backfill 3 prior studies into Dovetail with consistent tagging.
5. Train team via `research-democratization-training`.
6. Set up Linear ↔ Insight linking (Recipe 7).

**Result:** Stakeholders self-serve via Dovetail; PMs cite insights in PRDs.

### Example 2: Synthesize 12 JTBD interviews
**Goal:** Generate canonical insights for the JTBD study.

**Steps:**
1. Upload all transcripts (Recipe 4).
2. Auto-tag via Dovetail AI (Recipe 5); human-review.
3. Synthesize per procedure (Recipe 8).
4. Create Insight cards per theme (Recipe 7).
5. Publish Notion readout linking to insights.
6. PM picks up insights in PRD via `linear-mcp` link.

**Result:** Canonical, self-serve evidence for stakeholders.

## Edge cases / gotchas

- **Tag taxonomy chaos.** >50 tags = noise; collapse + rename quarterly.
- **AI auto-tag without review.** Magic isn't magic; always human-confirm.
- **Single-participant theme.** Need ≥3 of N participants per insight.
- **Insight without recommendation.** "Users struggle with X" without action = useless.
- **No source links.** Insight without traceable quote → opinion in 3 months.
- **Mixing methods in same insight.** Insight from interviews + survey = note that explicitly.
- **Repository as graveyard.** Without front page + active maintenance, stakeholders ignore.
- **PII in transcripts.** Sanitize or use Dovetail's PII redaction.
- **GDPR right-to-erasure.** Build process: participant ID → all highlights + transcripts deleted.
- **Stale insights.** Mark insights with "Last validated" date; refresh ≥annually.
- **Repository tool migration cost.** Notably / Marvin migration is non-trivial; sample test before committing.
- **Stakeholder training matters.** Self-serve requires team knows how to search.

## Sources

- [Dovetail v3 API](https://dovetail.com/help/api)
- [Daniel Pidcock — Atomic UX Research](https://www.atomicresearch.co)
- [Dovetail — Atomic Research blog](https://dovetail.com/blog/atomic-research)
- [Notably (free alt)](https://notably.ai)
- [Marvin (AI-first alt)](https://heymarvin.com)
- [ResearchOps Community — Repository guides](https://researchops.community)
- [Kate Towsey — Research That Scales](https://www.amazon.com/Research-That-Scales-Operations-Function/dp/1959029037)
