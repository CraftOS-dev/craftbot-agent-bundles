<!--
Sources:
NN/g — Why You Only Need 5 Users — https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/
NN/g — Thinking Aloud — https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/
Lookback API — https://www.lookback.com/docs/api
Otter.ai API — https://help.otter.ai/hc/en-us/articles/360062075953-Otter-API
-->
# Moderated 1:1 Usability — Think-Aloud — SKILL

5 users per round (Nielsen's discount usability rule — surfaces ~85% of issues). Think-aloud protocol — concurrent narration as participants work through tasks. Tools: Lookback (purpose-built for usability) or Zoom + Otter.ai (cheap alt). Transcripts pipe to Dovetail for tag-level synthesis.

## When to use

- Evaluative usability testing on a prototype or live product.
- Iterative test-and-fix cycles (run a round, fix, run again).
- When you need *why* behind a friction point (think-aloud reveals reasoning).
- When stakeholders need to watch sessions live (Lookback's observer mode).

Trigger phrases: "moderated test on this", "think-aloud test", "5 users on the prototype", "schedule a usability round", "Lookback session", "Zoom usability test".

## Setup

```bash
# Lookback (purpose-built moderated usability)
curl -fsSL "https://api.lookback.com/v1/me" \
  -H "Authorization: Bearer $LOOKBACK_API_KEY"

# Otter.ai (transcription)
curl -fsSL "https://otter.ai/api/v1/me" \
  -H "Authorization: Bearer $OTTER_API_KEY"

# Dovetail (synthesis)
curl -fsSL "https://dovetail.com/api/v1/me" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN"
```

Auth:
- `LOOKBACK_API_KEY` — Workspace settings → API. Paid (~$25/researcher/mo + per session).
- `OTTER_API_KEY` — otter.ai → Settings → API. Business tier.
- `DOVETAIL_API_TOKEN` — see `dovetail-research-repository` skill.

Tool choice:
- **Lookback** — purpose-built: screen + face cam + voice + observer chat + auto-upload to Dovetail. Use when budget allows.
- **Zoom + Otter** — cheap alt: $0 (existing Zoom) + Otter Business. Use when budget is tight.

## Common recipes

### Recipe 1: Think-aloud protocol (verbatim — say this)

```markdown
# Pre-session warmup (5 min)
"Thanks for joining. Before we start: this is a study about [product / area].
We're testing the product, not you — there are no wrong answers. If you get
stuck or confused, that's useful data for us, not a failure on your part.

I'm going to ask you to think out loud as you work. Just say whatever comes
to mind — what you're looking at, what you expect, what's confusing. Pretend
I'm not here. The silence is fine; the words are the gold."

# Tasks (5-10 min each)
"OK, the first task: [task in user language — outcome, not feature].
Walk me through how you'd do that."

# Probes (use when participant hesitates)
- "What are you thinking right now?"
- "What did you expect to happen?"
- "Where are you looking?"
- "What would you do next?"

# DON'T (leading)
- ❌ "Did you find that easy?"
- ❌ "Why didn't you click the button?"
- ❌ "Would you use this in real life?"

# Debrief (5-10 min at end)
- "Anything surprised you?"
- "Anything you'd change about how this works?"
- "Anything we should ask the next person?"
- "Anything else you want me to know?"
```

### Recipe 2: Task design

```markdown
# Good task — outcome-framed, real-world
"You're a solo founder and you've just hired your first employee. You want
to give them access to your CRM. Show me how you'd do that."

# Bad task — feature-framed, leading
"Click 'Settings', then 'Team', then 'Invite User'."

# Rules
- Outcome language, not feature language
- Real-world context (give them a backstory)
- One task = one user goal
- 5-10 minutes max per task
- 3-5 tasks per session
```

### Recipe 3: Create a Lookback session

```bash
PROJECT_ID="<lookback-project>"

curl -X POST "https://api.lookback.com/v1/projects/$PROJECT_ID/sessions" \
  -H "Authorization: Bearer $LOOKBACK_API_KEY" \
  -d '{
    "title": "Onboarding flow test — P3",
    "participant_name": "P3",
    "scheduled_at": "2026-06-15T14:00:00Z",
    "duration_minutes": 60,
    "moderator_email": "researcher@yourco.com",
    "recording": {
      "screen": true,
      "face_cam": true,
      "voice": true,
      "system_audio": false
    },
    "observers": ["pm@yourco.com", "designer@yourco.com"]
  }'
```

### Recipe 4: Zoom + Otter pipeline

```bash
# Step 1: schedule Zoom with auto-record + auto-transcript
curl -X POST "https://api.zoom.us/v2/users/me/meetings" \
  -H "Authorization: Bearer $ZOOM_JWT" \
  -d '{
    "topic": "Usability test — P3",
    "type": 2,
    "start_time": "2026-06-15T14:00:00Z",
    "duration": 60,
    "settings": {
      "auto_recording": "cloud",
      "host_video": true,
      "participant_video": true
    }
  }'

# Step 2: after session, Otter webhook fires; pull transcript
curl -fsSL "https://otter.ai/api/v1/transcripts/$TRANSCRIPT_ID" \
  -H "Authorization: Bearer $OTTER_API_KEY" \
  -o "transcript-P3.vtt"

# Step 3: upload to Dovetail
curl -X POST "https://dovetail.com/api/v1/projects/$DOVETAIL_PROJECT/transcripts/upload" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
  -F "file=@transcript-P3.vtt" \
  -F "participant=P3" \
  -F "session_date=2026-06-15"
```

### Recipe 5: Observer notes template (Notion live during session)

```markdown
# Session notes — P3, 2026-06-15

## Pre-session signal
- Role: solo founder, Series A
- Used the product before? No (cold)

## Task 1: Invite new team member
- Time: 4:22 → 8:15 (≈4 min)
- Path: Dashboard → "?" icon → searched "team" → Settings → ...
- Friction: Searched help center first, expected /team in nav. **High friction Q2 (visibility)**.
- Verbatim: "Where's the team page? I keep looking for it." (P3 @ 5:30)
- Completed: yes, with hint at 7:50

## Task 2: ...

## Spontaneous feedback (unprompted)
- "The empty state on Activity Feed is confusing — I don't know what's supposed to be there." (12:14)

## Themes emerging
- Navigation discoverability (settings)
- Empty-state confusion (activity feed)

## Quotes for highlight reel
- "Where's the team page?" — P3 @ 5:30
```

### Recipe 6: Round structure — 5 users + iterate

```python
# Standard iterative round
round_1 = {
    "participants": 5,
    "fix_threshold": "any issue affecting ≥3 of 5",
    "output": "fix list for designers + PM"
}

round_2 = {
    "participants": 5,  # different recruits, same screener
    "test_after": "design + dev fix issues from round 1",
    "compare_to": "round 1 success rates + time-on-task"
}

# Nielsen: 5 users surface ~85% of issues. 5+5 over rounds > 10 in one round.
```

### Recipe 7: Pilot before launch

Always pilot 1 session before recruiting full N=5. Catches:
- Task wording confusion
- Tech setup issues (prototype broken, mic levels)
- Timing miscalculation (sessions running over)

```markdown
# Pilot session brief
- Internal participant OR friendly external
- Run real protocol end-to-end
- Take 15 min after to fix:
  - Task wording
  - Technical issues
  - Probe vocabulary
- Pilot data is *not* in the dataset
```

### Recipe 8: Calculate metrics post-round

```python
def round_metrics(sessions, tasks):
    """sessions: list of {participant, task_id, completed, time_sec, help_count}"""
    by_task = {}
    for t in tasks:
        ts = [s for s in sessions if s["task_id"] == t]
        by_task[t] = {
            "success_rate": sum(s["completed"] for s in ts) / len(ts),
            "median_time": median(s["time_sec"] for s in ts),
            "help_rate":   sum(s["help_count"] > 0 for s in ts) / len(ts),
        }
    return by_task
```

### Recipe 9: Post-session SUS or UMUX-Lite

```markdown
# UMUX-Lite (4 items) — short post-test survey
1. The product's capabilities meet my requirements. (1-7)
2. The product is easy to use. (1-7)
3. [Optional] I would use this product again. (1-7)
4. [Optional] Overall how would you rate ease of use? (1-7)

# UMUX-Lite score → SUS-equivalent: ((Q1-1) + (Q2-1)) × 8.33 + 22.9
# Above 68 = above industry average
```

### Recipe 10: Synthesis handoff to Dovetail

```bash
# After 5 transcripts are uploaded:
# 1. Tag at quote level in Dovetail UI (or auto-tag via Dovetail AI)
# 2. Cluster tags into themes (target ≤7)
# 3. Query themes by tag

curl -fsSL "https://dovetail.com/api/v1/projects/$PROJECT/highlights?tag=nav-discoverability" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
| jq '[.highlights[] | {participant, quote, timestamp}]'

# See dovetail-research-repository skill for full synthesis pipeline
```

## Examples

### Example 1: Test new onboarding — single iteration round
**Goal:** Find friction in the rewritten onboarding flow.

**Steps:**
1. Write 5 outcome-framed tasks (Recipe 2).
2. Recruit 5 via `recruit-user-interviews-respondent-dscout`.
3. Pilot 1 session internally (Recipe 7); fix task wording.
4. Run 5 Lookback sessions (Recipe 3) with observers (PM + designer watching).
5. Take notes per session (Recipe 5).
6. Post-session UMUX-Lite (Recipe 9).
7. Upload transcripts to Dovetail (Recipe 4 step 3).
8. Synthesize themes (Recipe 10).
9. Publish readout via `dovetail-research-repository`.

**Result:** Prioritized friction list with severity + verbatims, ready for fix sprint.

### Example 2: Cheap test — Zoom + Otter for a side project
**Goal:** Validate a flow without paying for Lookback.

**Steps:**
1. Recruit via in-house list or User Interviews.
2. Schedule Zoom with auto-record + auto-transcript (Recipe 4 step 1).
3. Run think-aloud (Recipe 1) with observer in Zoom.
4. Pull Otter transcript (Recipe 4 step 2).
5. Upload to Dovetail (Recipe 4 step 3).

**Result:** Same think-aloud rigor at $0 platform cost.

## Edge cases / gotchas

- **Leading questions.** "Was that easy?" tells the user the answer. Use Recipe 1 probes only.
- **Observer interruption.** Observers asking questions mid-session = contamination. Use Lookback chat OR mute them in Zoom.
- **No pilot.** Skipping pilot = wasted N=1 on task confusion. Always pilot.
- **Tasks as feature instructions.** "Click here" = not a task. Outcome framing per Recipe 2.
- **>5 per round.** Wastes budget per Nielsen. Iterate rounds instead.
- **Combining moderated + unmoderated SUS.** They measure different things; report separately.
- **No incentive logistics.** Tell participants when/how they get paid before session ends.
- **Tech failures.** Prototype loads in private window? Mic permission denied? Pilot catches.
- **Note-taking during moderation.** Moderator typing = participant slowdown. Either silent observer takes notes OR moderator notes only at task end.
- **Participant feels judged.** Reframe in warmup: "we're testing the product, not you" (Recipe 1).
- **Skipping debrief.** Last 5 min is gold — spontaneous insights, suggestions for next session.

## Sources

- [NN/g — Why You Only Need to Test with 5 Users](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/)
- [NN/g — Thinking Aloud: The #1 Usability Tool](https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/)
- [Lookback API](https://www.lookback.com/docs/api)
- [Otter.ai API](https://help.otter.ai/hc/en-us/articles/360062075953-Otter-API)
- [Zoom Meetings API](https://developers.zoom.us/docs/api/meetings/)
- [Dovetail v3 API](https://dovetail.com/help/api)
- [UMUX-Lite — Lewis et al.](https://uxpajournal.org/wp-content/uploads/sites/8/pdf/JUS_Lewis_May2013.pdf)
- [System Usability Scale (SUS)](https://www.usability.gov/how-to-and-tools/methods/system-usability-scale.html)
