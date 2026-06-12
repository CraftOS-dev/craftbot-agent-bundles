<!--
Sources:
FullStory — https://developer.fullstory.com/server/v1
LogRocket — https://docs.logrocket.com/reference
Microsoft Clarity (free) — https://learn.microsoft.com/en-us/clarity/setup-and-installation
-->
# FullStory / LogRocket / Clarity Session Replay — SKILL

Session replay is the qualitative side of product analytics: watch what users actually do, where they rage-click, dead-click, hit errors, and abandon. This pack covers FullStory, LogRocket, and Microsoft Clarity (free fallback) for querying friction-filtered sessions.

## When to use

- Diagnosing why a funnel step is leaking ("users land on step 2 and bounce — why?").
- Investigating a bug report ("user says the save button is broken").
- Validating a new release ("any rage clicks on the new onboarding?").
- Extracting verbatim UX issues for the PRD problem section.
- Quarterly "top friction signals" review for the design team.

Trigger phrases: "session replay", "watch user sessions", "find rage clicks", "diagnose this bug", "what are users doing on page X", "UX friction".

## Setup

### FullStory (paid, enterprise default)

```bash
curl -fsSL "https://api.fullstory.com/v2/users/_self" \
  -H "Authorization: Basic $FULLSTORY_API_KEY"
```

Auth:
- `FULLSTORY_API_KEY` — Server API key from FullStory → Settings → Integrations → API Keys.

### LogRocket (paid, dev-focused)

```bash
curl -fsSL "https://api.logrocket.com/v1/orgs/$ORG_ID/projects" \
  -H "Authorization: Token $LOGROCKET_API_KEY"
```

Auth:
- `LOGROCKET_API_KEY` — generated in LogRocket → Project Settings → API Tokens.

### Microsoft Clarity (FREE — default fallback)

```bash
# Clarity has limited REST API; mostly dashboard + data export.
# Project insights via Data Export API:
curl -fsSL "https://www.clarity.ms/export-data/api/v1/project-live-insights?numOfDays=7" \
  -H "Authorization: Bearer $CLARITY_API_TOKEN"
```

Auth:
- `CLARITY_API_TOKEN` — Project → Settings → Data Export. Free unlimited.

## Common recipes

### Recipe 1: FullStory — find sessions with rage clicks

```bash
# Last 7 days, sessions containing rage-click events
curl -fsSL "https://api.fullstory.com/sessions/v1/search" \
  -H "Authorization: Basic $FULLSTORY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "since":"2026-06-02T00:00:00Z",
    "until":"2026-06-09T00:00:00Z",
    "events":[{"name":"rage_click"}],
    "limit":50
  }' \
| jq '.sessions[] | {url: .replayUrl, user: .user.uid, rageClicks: .eventCount}'
```

### Recipe 2: FullStory — sessions that errored on a specific page

```bash
curl -fsSL "https://api.fullstory.com/sessions/v1/search" \
  -H "Authorization: Basic $FULLSTORY_API_KEY" \
  -d '{
    "since":"2026-06-02T00:00:00Z",
    "url_contains":"/onboarding/step-2",
    "events":[{"name":"error"}],
    "limit":25
  }' \
| jq '.sessions[] | {url: .replayUrl, errors: .events[] | select(.name=="error") | .message}'
```

### Recipe 3: LogRocket — sessions by user identifier

```bash
# Find a specific user's last 5 sessions
curl -fsSL "https://api.logrocket.com/v1/orgs/$ORG_ID/sessions" \
  -H "Authorization: Token $LOGROCKET_API_KEY" \
  -d "filter[user_id]=$USER_ID&sort=-created_at&limit=5" \
| jq '.data[] | {url: .replay_url, started: .started_at, duration: .duration_seconds}'
```

### Recipe 4: LogRocket — sessions with frontend errors

```bash
curl -fsSL "https://api.logrocket.com/v1/orgs/$ORG_ID/sessions" \
  -H "Authorization: Token $LOGROCKET_API_KEY" \
  -d 'filter[has_errors]=true&filter[created_at_gte]=2026-06-02' \
| jq '.data[] | {url: .replay_url, errorCount: .error_count, firstError: .first_error.message}'
```

### Recipe 5: Clarity — heatmap + click insights (free)

```bash
# Project-level live insights (top-clicked elements + dead clicks)
curl -fsSL "https://www.clarity.ms/export-data/api/v1/project-live-insights?numOfDays=7" \
  -H "Authorization: Bearer $CLARITY_API_TOKEN" \
| jq '.metrics[] | select(.metricName | IN("Dead clicks","Rage clicks","Quick backs"))'
```

### Recipe 6: Triage top-friction sessions for the design review

```python
# Pull rage-click sessions, rank by event count, output a markdown brief
import requests
import os

API = "https://api.fullstory.com/sessions/v1/search"
H = {"Authorization": f"Basic {os.environ['FULLSTORY_API_KEY']}", "Content-Type":"application/json"}
body = {
    "since":"2026-06-02T00:00:00Z",
    "events":[{"name":"rage_click"}],
    "limit":100
}
sessions = requests.post(API, headers=H, json=body).json()["sessions"]

# Group by URL pattern; top-5 most-rage-clicked pages
from collections import Counter
pages = Counter()
for s in sessions:
    pages[s.get("pageUrl","unknown")] += s.get("eventCount", 1)

print("# Top friction pages — last 7 days\n")
for url, count in pages.most_common(5):
    print(f"- **{url}** — {count} rage clicks")
    # Pull 2 sample replay URLs for each
    samples = [s["replayUrl"] for s in sessions if s.get("pageUrl") == url][:2]
    for sample in samples:
        print(f"  - Replay: {sample}")
```

### Recipe 7: Watch funnel exits (sessions that abandoned the activation flow)

```bash
curl -fsSL "https://api.fullstory.com/sessions/v1/search" \
  -H "Authorization: Basic $FULLSTORY_API_KEY" \
  -d '{
    "since":"2026-06-02T00:00:00Z",
    "url_contains":"/onboarding",
    "events_not":[{"name":"first_value_event"}],
    "limit":20
  }' \
| jq '.sessions[] | {url: .replayUrl, lastPage: .pages[-1].url, duration: .durationSeconds}'
```

### Recipe 8: Bug investigation from a support ticket

```python
# Customer email -> their last session
import requests
EMAIL = "user@example.com"

# FullStory user lookup
H = {"Authorization": f"Basic {os.environ['FULLSTORY_API_KEY']}"}
user = requests.get(
    f"https://api.fullstory.com/users/v1?email={EMAIL}",
    headers=H
).json()["users"][0]

# Sessions for that user
sessions = requests.get(
    f"https://api.fullstory.com/users/v1/individual/{user['id']}/sessions",
    headers=H
).json()["sessions"]

print(f"Latest 3 sessions for {EMAIL}:")
for s in sessions[:3]:
    print(f"  - {s['replayUrl']} ({s['startTime']}, {s['duration']}s)")
```

### Recipe 9: Tag a session for follow-up

```bash
# FullStory custom event — annotate a watched session
curl -X POST "https://api.fullstory.com/sessions/v1/$SESSION_ID/events" \
  -H "Authorization: Basic $FULLSTORY_API_KEY" \
  -d '{
    "name":"pm_review",
    "properties":{
      "reviewer":"<pm>",
      "verdict":"bug",
      "linear_issue":"https://linear.app/team/issue/PROD-1234"
    }
  }'
```

### Recipe 10: Weekly friction digest

```bash
# Combined: list top-5 rage-click pages + top-3 error pages last week.
# Output goes into the weekly stakeholder update under "Lowlights" or "UX watch."
{
  echo "## UX friction — week of $(date +%Y-%m-%d)"
  echo
  echo "### Top rage-click pages"
  # (Recipe 6 output)
  echo
  echo "### Top error pages"
  curl -fsSL "https://api.fullstory.com/sessions/v1/search" \
    -H "Authorization: Basic $FULLSTORY_API_KEY" \
    -d "{\"since\":\"$(date -d '7 days ago' +%Y-%m-%dT00:00:00Z)\",\"events\":[{\"name\":\"error\"}],\"limit\":200}" \
  | jq -r '[.sessions[]] | group_by(.pageUrl) | map({url:.[0].pageUrl, errors: length}) | sort_by(-.errors) | .[0:3] | .[] | "- \(.url): \(.errors)"'
} > friction-digest.md
```

## Examples

### Example 1: PRD problem section sourced from session replay
**Goal:** Anchor the PRD problem in actual user behavior.

**Steps:**
1. Pull rage-click sessions for the affected page (Recipe 1).
2. Watch the top 5-10 (Recipe 6 ranks them).
3. Take notes on the specific friction (verbatim, e.g., "user clicks the disabled Save button 8 times").
4. Cite 2-3 replay URLs in the PRD problem section (with consent caveat).
5. Cross-reference with `dovetail-research-synthesis` themes — does the replay corroborate the interview signal?

**Result:** PRD problem is doubly cited: replay + interview.

### Example 2: Post-release UX validation
**Goal:** Confirm the onboarding revamp doesn't introduce new rage clicks.

**Steps:**
1. Day 1 post-release: query rage-clicks on `/onboarding` (Recipe 1, scoped to since launch).
2. Compare volume to the pre-release baseline (`since` set to a prior week).
3. If volume increased → flag a P0 bug; iterate before continuing rollout.
4. Document in the experiment readout (`statsig-growthbook-experiments`).

**Result:** No silent UX regressions ship.

## Edge cases / gotchas

- **Paid plans.** FullStory ~$199/mo+; LogRocket ~$99/mo+. Clarity is free.
- **Consent + privacy.** GDPR/CCPA require consent before recording; many session-replay tools redact form fields by default — confirm config.
- **PII masking.** Confirm names/emails/passwords aren't captured. FullStory + LogRocket + Clarity all support field-level masking; verify before sharing replay URLs.
- **Replay storage.** Sessions expire (FullStory: 30-90 days by plan; LogRocket: 30 days). Save important replays to S3 / local within retention window.
- **Sampling.** FullStory samples sessions at higher tier; LogRocket records 100% by default. Mixing the two in analysis biases counts.
- **Mobile vs web.** FullStory and LogRocket both support web + mobile but the event schema differs. Don't merge counts across platforms without normalizing.
- **Clarity is read-only.** No way to programmatically retrieve full session videos via API; you get aggregate metrics. For session URLs you must use the dashboard.
- **Rate limits.** FullStory: 60 req/min on the v1 search. LogRocket: 100 req/min. Plan for paginated pulls.
- **Replay URLs require login.** Shared replay URLs prompt for login by default; use shareable links (FullStory) or `share=true` mode (LogRocket) — but those expose PII unless properly masked.
- **Don't replace analytics with replay.** Replay = qualitative why; Amplitude/Mixpanel/PostHog = quantitative how-many. Use together.

## Sources

- [FullStory Server API](https://developer.fullstory.com/server/v1)
- [LogRocket REST API reference](https://docs.logrocket.com/reference)
- [Microsoft Clarity setup](https://learn.microsoft.com/en-us/clarity/setup-and-installation)
- [Clarity Data Export API](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api)
- [FullStory Frustration Signals](https://help.fullstory.com/hc/en-us/articles/360020623834-Frustration-Signals)
- [LogRocket session search docs](https://docs.logrocket.com/docs/searching-sessions)
- [Nielsen Norman — Why use session replay](https://www.nngroup.com/articles/session-replay)
