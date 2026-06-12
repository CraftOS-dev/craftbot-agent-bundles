<!--
Sources:
dscout API + diary study template — https://dscout.com/api
NN/g — Diary Studies — https://www.nngroup.com/articles/diary-studies/
Indeemo (alt) — https://www.indeemo.com
-->
# Diary Studies — dscout 7-30 Day — SKILL

Longitudinal, in-context mobile-first diary studies via dscout Missions. 8-15 participants × 7-30 days with text + photo + video + screen recording prompts. Surfaces habits, mood, contextual usage, and pattern-over-time that moderated sessions can't see. Indeemo is the mobile + web alt.

## When to use

- Understanding how product fits into daily life over time.
- Habit formation / behavior change studies.
- Pre/post change studies (before X vs after X).
- Surfacing edge cases that come up rarely in any one session.
- Building empathy through participant-generated artifacts.

Trigger phrases: "diary study", "14-day study on X", "longitudinal research", "in-context behavior", "dscout mission", "Indeemo".

## Setup

```bash
# dscout
curl -fsSL "https://dscout.com/api/v1/me" \
  -H "Authorization: Bearer $DSCOUT_API_KEY"

# Indeemo (alt)
curl -fsSL "https://api.indeemo.com/v1/me" \
  -H "Authorization: Bearer $INDEEMO_API_KEY"
```

Auth + cost:
- `DSCOUT_API_KEY` — Mission dashboard → Settings. Paid per-participant (~$300-1000 / 7-30 day mission).
- `INDEEMO_API_KEY` — Indeemo subscription (~$1500/mo platform fee + per-participant).

## Common recipes

### Recipe 1: Mission structure (Day 0 → Day N)

```markdown
# Diary Study Plan: [Study Name]

**Duration:** 14 days · **Participants:** 12 · **Honorarium:** $500/participant

## Day 0 — Onboarding mission
- "Welcome — show us your current setup. Take a video walkthrough of how you use [tool / activity] today."
- "What problems are you trying to solve right now?"
- Confirms phone calibration + consent

## Day 1-N — Daily prompts (mix types)

### Daily prompts (recurring)
- Behavioral: "What did you do today with [topic]? Tap photo / video."
- Reflective: "How did you feel about [domain] today? 1-7 scale + 1-sentence why."
- Artifactual: "Show us the [artifact] you used today."

### Variable prompts (selectively triggered)
- "Did you encounter [specific event] today? Yes/no + brief description."
- "Show us a moment that surprised you."

## Day N/2 — Mid-study check-in (15-min video call)
- Clarify confusing entries
- Re-energize participant
- Surface emerging themes
- Identify drop-out risk

## Day N — Final reflection
- "Looking back, what changed over these [N] days?"
- "What's the one thing you wish [tool] did that it doesn't?"
- "If we made [hypothetical change], how would your day be different?"
- SUS / UMUX-Lite if evaluative
```

### Recipe 2: Create dscout mission

```bash
curl -X POST "https://dscout.com/api/v1/missions" \
  -H "Authorization: Bearer $DSCOUT_API_KEY" \
  -d '{
    "title": "Founder daily inbox check — 14 days",
    "duration_days": 14,
    "target_count": 12,
    "honorarium_cents": 50000,
    "criteria": {
      "role": ["founder", "ceo"],
      "company_stage": ["seed", "series_a"],
      "device": "ios_or_android_with_camera"
    },
    "prompts": [
      {"day": 0, "type": "onboarding", "title": "Show us your inbox", "body": "Take a 60-sec video walking through how you check email this morning."},
      {"day": 1, "frequency": "daily", "type": "behavioral", "title": "Today inbox check", "body": "How many emails today? Show one that mattered."},
      {"day": 1, "frequency": "daily", "type": "reflective", "title": "How did inbox feel today?", "body": "1-7 scale + 1-sentence why."},
      {"day": 7, "type": "check_in", "title": "Mid-study reflection", "body": "What pattern have you noticed?"},
      {"day": 14, "type": "reflection", "title": "Final wrap", "body": "What changed over 2 weeks?"}
    ],
    "consent": {"recording": true, "data_retention_days": 365}
  }'
```

### Recipe 3: Daily monitoring routine

```python
# Morning + evening check
def daily_diary_check(mission_id, api_token):
    import requests
    r = requests.get(
        f"https://dscout.com/api/v1/missions/{mission_id}/participants",
        headers={"Authorization": f"Bearer {api_token}"}
    )
    participants = r.json()["participants"]
    flagged = []
    for p in participants:
        # No entry today?
        if p["last_entry_date"] < today():
            flagged.append({"id": p["id"], "issue": "no_entry_today", "action": "nudge"})
        # Drop-off risk (no entry for 2+ days)
        if p["consecutive_missed_days"] >= 2:
            flagged.append({"id": p["id"], "issue": "drop_off_risk", "action": "personal_message_or_remove"})
    return flagged
```

### Recipe 4: Nudge non-responders

```bash
# Polite, no-shame nudge after 24h skip
curl -X POST "https://dscout.com/api/v1/participants/$PARTICIPANT_ID/messages" \
  -H "Authorization: Bearer $DSCOUT_API_KEY" \
  -d '{
    "body": "Hi! Just a friendly check-in — we missed your entry today. No worries if life got busy. If you have 2 mins now, today is still open. If not, no problem; tomorrow is fine. — [Researcher]"
  }'
```

### Recipe 5: Remove disengaged participants

```python
# Day 3 cutoff: remove participants who haven't engaged
def remove_disengaged(mission_id, participants):
    """
    Cut at day 3 if:
    - 0 entries
    - No response to onboarding mission
    """
    to_remove = [p for p in participants
                 if p["onboarding_complete"] is False
                 or p["entries_count"] == 0]
    for p in to_remove:
        # Replace with backup recruit
        ...
    return len(to_remove)

# Better to remove + replace than to dilute data
```

### Recipe 6: Pull entries for synthesis

```bash
curl -fsSL "https://dscout.com/api/v1/missions/$MISSION_ID/entries" \
  -H "Authorization: Bearer $DSCOUT_API_KEY" \
| jq '[.entries[] | {
    participant_id,
    day,
    prompt_id,
    type,
    text,
    media_urls,
    timestamp
  }]'
```

### Recipe 7: Longitudinal synthesis pattern

```python
# Pattern-over-time analysis
def longitudinal_themes(entries):
    """
    Group by:
    1. Theme (cross-cutting)
    2. Per-participant over time (within-subject)
    3. Per-day across participants (between-subject by day)
    """
    by_theme = defaultdict(list)
    by_pid_day = defaultdict(list)
    by_day = defaultdict(list)

    for e in entries:
        for tag in e.get("tags", []):
            by_theme[tag].append(e)
        by_pid_day[(e["participant_id"], e["day"])].append(e)
        by_day[e["day"]].append(e)

    # Surface:
    # - themes that intensify over time
    # - themes that decay (novelty effect)
    # - per-participant shifts
    return {"by_theme": by_theme, "by_pid_day": by_pid_day, "by_day": by_day}
```

### Recipe 8: Upload to Dovetail for tagging

```bash
# Dovetail with day tag + participant tag
while read -r ENTRY; do
  P_ID=$(echo "$ENTRY" | jq -r '.participant_id')
  DAY=$(echo "$ENTRY" | jq -r '.day')
  BODY=$(echo "$ENTRY" | jq -r '.text')

  curl -X POST "https://dovetail.com/api/v1/projects/$DOVETAIL_PROJECT/notes" \
    -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
    -d "{
      \"title\": \"$P_ID day $DAY\",
      \"body\": \"$BODY\",
      \"tags\": [\"day-$DAY\", \"$P_ID\"]
    }"
done < <(curl -fsSL "https://dscout.com/api/v1/missions/$MISSION_ID/entries" \
         -H "Authorization: Bearer $DSCOUT_API_KEY" | jq -c '.entries[]')
```

### Recipe 9: Mid-study check-in script

```markdown
# Mid-study 15-min call (Day 7 of 14)

## Goals
1. Clarify confusing entries
2. Re-energize the participant
3. Surface emerging themes
4. Identify drop-out risk

## Script
- "Thanks for participating so far — really appreciate the entries."
- "I noticed [specific entry from their feed] — can you tell me more about that?"
- "Anything you've noticed about your own [behavior] since starting?"
- "Any prompts that feel weird or off?"
- "How's the experience overall? Anything we should change for week 2?"
- Confirm Day 14 reflection scheduled
```

### Recipe 10: Final report template

```markdown
# Diary Study Report: [Name]

**Date:** [YYYY-MM-DD] · **N=[12] × [14 days]** · **Total entries:** [~250]
**Researcher:** [Name] · **dscout mission:** [link]

## TL;DR
- [Top 1-2 themes + how they evolved over time]
- [Recommendation in 1 sentence]

## Method
- 14-day dscout mission with daily prompts + check-in + reflection
- 12 participants, $500 honorarium
- Synthesis: Dovetail with day-tag + theme tag

## Themes (5-7)

### Theme 1: [Name] — Pattern over time
- **Day 1-3:** [pattern]
- **Day 7-10:** [shift]
- **Day 14:** [end state]
- **Verbatims:**
  > "Day 2: [quote]" — P3
  > "Day 9: [quote]" — P3
  > (same participant evolution shown)

### Theme 2: ...

## Cross-theme observations
- Habit formation arc: [pattern]
- Novelty decay: [where engagement drops]
- Surprise findings: [emergent patterns]

## Recommendations
1. [Action + rationale + owner]
2. ...

## Appendix
- dscout mission: [link]
- Dovetail synthesis: [link]
- Day-by-day participant grids: [linked]
```

## Examples

### Example 1: 14-day diary study on inbox habits
**Goal:** Surface real-world email check behavior that interviews can't show.

**Steps:**
1. Plan mission (Recipe 1) with mix of behavioral + reflective + artifactual prompts.
2. Create dscout mission (Recipe 2).
3. Daily monitoring (Recipe 3); nudge non-responders (Recipe 4); remove disengaged (Recipe 5).
4. Day 7 mid-study calls (Recipe 9).
5. Pull entries (Recipe 6) + upload to Dovetail (Recipe 8).
6. Longitudinal synthesis (Recipe 7).
7. Final report (Recipe 10).

**Result:** Pattern-over-time evidence: how inbox stress evolves from Monday morning to Friday evening, week 1 vs week 2.

### Example 2: Lightweight diary with Typeform (no dscout budget)
**Goal:** Approximate a diary study without paying dscout.

**Steps:**
1. Build daily Typeform with simple prompts.
2. Email participants the link daily via Gmail cron.
3. Pull responses to Airtable / CSV.
4. Synthesize in Dovetail or Notion.

**Result:** Lower-friction, lower-fidelity, but workable.

## Edge cases / gotchas

- **Day-3 disengagement.** Catch early; replace fast.
- **Over-prompting fatigue.** >3 prompts/day = drop-off. Aim 1-2/day + occasional variable.
- **Vague prompts.** "How was your day?" = no data. Behavioral + specific.
- **Forgetting mid-study touch.** Day 7 call dramatically increases day 8-14 engagement.
- **Honorarium delays.** Pay within 48h of mission complete; participants in panel community talk.
- **Time-zone-blind prompting.** Push notifications at 3am local = drop-off.
- **No consent for video.** Re-confirm at signup; some participants opt for text-only.
- **Mixing study types.** Diary = generative + behavioral. Don't drop in usability tasks mid-mission.
- **Single-day reflection only.** Longitudinal value is the curve. Always include daily prompts.
- **Day-N reflection rushed.** Plan ≥15-min reflection at end; otherwise insights lost.
- **Sample <8.** Below 8, longitudinal patterns unstable.
- **Indeemo vs dscout.** Indeemo for web + mobile mix; dscout for pure mobile.

## Sources

- [dscout API](https://dscout.com/api)
- [dscout diary study template](https://dscout.com/people-nerds/diary-study-template)
- [NN/g — Diary Studies: Understanding Long-Term User Behavior](https://www.nngroup.com/articles/diary-studies/)
- [Indeemo](https://www.indeemo.com)
- [Dovetail v3 API](https://dovetail.com/help/api)
- [Typeform Create API](https://www.typeform.com/developers/create)
