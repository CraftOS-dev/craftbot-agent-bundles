<!--
Source: https://developers.salesloft.com/api.html + https://developers.outreach.io/api/ + https://app.gong.io/settings/api/documentation
Salesloft + Outreach + Gong admin (June 2026 SOTA).
-->
# Salesloft + Outreach + Gong — Admin Ops — SKILL

Admin-mode operations across sales-engagement + conversation intelligence. Salesloft cadence governance + user provisioning; Outreach sequence governance + prospect import; Gong scorecard creation + smart tracker setup + user provisioning. Each has a REST admin API surface — calls are governance, not seller-facing.

## When to use

- **Provision a new rep** — create Salesloft + Outreach + Gong users in one shot.
- **Cadence / sequence governance** — list, audit, archive duplicates or stale templates.
- **Cadence template publish** — push a new approved template org-wide.
- **Gong scorecard create / update** — add a new call review rubric.
- **Gong smart trackers** — add a keyword to detect for objections, competitors.
- **Deactivate rep on offboarding** — pull licenses across all three tools.
- **Trigger phrases**: "create Salesloft user", "push a new cadence", "Gong scorecard", "smart tracker", "offboard rep tech stack", "cadence audit".

Do NOT use this skill for: **AE-facing outreach copy** (use `outreach-salesloft-sequences` in parent sales-agent); **call analysis** (use `gong-chorus-call-intelligence` in parent); **enrichment** (use `data-enrichment-zoominfo-apollo-clay`); **lead routing** (use `lead-routing-leandata-chili-piper`).

## Setup

```bash
# Salesloft — Personal API token (Settings → Your Account → API Token)
export SALESLOFT_TOKEN="<token>"

# Outreach — OAuth client_credentials (Org Admin → Integrations → API)
export OUTREACH_CLIENT_ID="<id>"
export OUTREACH_CLIENT_SECRET="<secret>"
# Then fetch access token (Recipe 1)
export OUTREACH_TOKEN="<bearer>"

# Gong — App-only access (Settings → API → Generate)
export GONG_ACCESS_KEY="<key>"
export GONG_SECRET="<secret>"
# Gong uses Basic auth: base64(access_key:secret)
export GONG_BASIC=$(printf "$GONG_ACCESS_KEY:$GONG_SECRET" | base64)

# Or all via api-gateway proxy
export MATON_API_KEY="<key>"
```

Required:
- Admin role on all 3 platforms
- Salesloft: Team/Enterprise plan for admin API
- Outreach: API requires Professional+ tier
- Gong: API requires Premium tier; rate-limited 3 calls/sec

## Common recipes

### Recipe 1: Outreach OAuth token refresh

```bash
# Client credentials flow — server-to-server
curl -X POST "https://api.outreach.io/oauth/token" \
  -d "grant_type=client_credentials" \
  -d "client_id=$OUTREACH_CLIENT_ID" \
  -d "client_secret=$OUTREACH_CLIENT_SECRET" \
  -d "scope=accounts.all sequences.all users.all prospects.all"
# Returns access_token (lasts ~2 hours)
```

### Recipe 2: Create Salesloft user

```bash
curl -X POST "https://api.salesloft.com/v2/users" \
  -H "Authorization: Bearer $SALESLOFT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newrep@co.com",
    "first_name": "Alice",
    "last_name": "Rep",
    "team_id": 4567,
    "role_id": 12,
    "active": true
  }'
```

### Recipe 3: Create Outreach user

```bash
curl -X POST "https://api.outreach.io/api/v2/users" \
  -H "Authorization: Bearer $OUTREACH_TOKEN" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{
    "data": {
      "type": "user",
      "attributes": {
        "email": "newrep@co.com",
        "firstName": "Alice",
        "lastName": "Rep",
        "locked": false,
        "userType": "Standard"
      }
    }
  }'
```

### Recipe 4: Create Gong user

```bash
curl -X POST "https://api.gong.io/v2/users" \
  -H "Authorization: Basic $GONG_BASIC" \
  -H "Content-Type: application/json" \
  -d '{
    "users": [{
      "emailAddress": "newrep@co.com",
      "firstName": "Alice",
      "lastName": "Rep",
      "title": "Account Executive",
      "managerId": "5012345"
    }]
  }'
```

### Recipe 5: List Salesloft cadences (audit)

```bash
curl "https://api.salesloft.com/v2/cadences?per_page=100&include_paging_counts=true" \
  -H "Authorization: Bearer $SALESLOFT_TOKEN" \
  | jq '.data[] | {id, name, current_state, shared, total_actions, created_at, updated_at}'
```

### Recipe 6: Archive duplicate / stale cadences

```python
import requests, os
from datetime import datetime, timedelta

token = os.environ["SALESLOFT_TOKEN"]
hdr = {"Authorization": f"Bearer {token}"}
page = 1
stale = []
while True:
    r = requests.get(f"https://api.salesloft.com/v2/cadences",
                     headers=hdr, params={"page": page, "per_page": 100}).json()
    for c in r.get("data", []):
        updated = datetime.fromisoformat(c["updated_at"].replace("Z","+00:00"))
        if updated < datetime.now(updated.tzinfo) - timedelta(days=180):
            stale.append(c)
    if not r.get("metadata", {}).get("paging", {}).get("next_page"):
        break
    page += 1

# Archive (Salesloft cadences are archived via PATCH current_state = archived)
for c in stale:
    requests.patch(f"https://api.salesloft.com/v2/cadences/{c['id']}",
                   headers=hdr, json={"current_state": "archived"})
    print(f"Archived: {c['name']}")
```

### Recipe 7: Publish Outreach sequence as team template

```bash
curl -X POST "https://api.outreach.io/api/v2/sequences" \
  -H "Authorization: Bearer $OUTREACH_TOKEN" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{
    "data": {
      "type": "sequence",
      "attributes": {
        "name": "Enterprise Outbound — 14 day",
        "enabled": true,
        "shareType": "shared",
        "sequenceType": "interval",
        "tags": ["enterprise", "outbound", "2026Q3"]
      }
    }
  }'
```

### Recipe 8: Create Gong call scorecard

```bash
curl -X POST "https://api.gong.io/v2/calls/scorecards" \
  -H "Authorization: Basic $GONG_BASIC" \
  -H "Content-Type: application/json" \
  -d '{
    "scorecard": {
      "name": "Discovery Call — MEDDIC v2",
      "questions": [
        {"questionText": "Did the rep identify the Economic Buyer?", "scoreType": "BINARY"},
        {"questionText": "Were Metrics quantified (deal value, ROI)?", "scoreType": "BINARY"},
        {"questionText": "Was Champion explicitly named and confirmed?", "scoreType": "BINARY"},
        {"questionText": "Was a next step set with date?", "scoreType": "BINARY"},
        {"questionText": "Overall: ready to advance to demo?", "scoreType": "FIVE_POINT"}
      ]
    }
  }'
```

### Recipe 9: Add Gong smart tracker (keyword detection)

```bash
curl -X POST "https://api.gong.io/v2/settings/trackers" \
  -H "Authorization: Basic $GONG_BASIC" \
  -H "Content-Type: application/json" \
  -d '{
    "trackers": [{
      "name": "Competitor: AcmeRival",
      "keywords": ["AcmeRival", "Acme Rival", "Acme rival platform"],
      "category": "COMPETITOR"
    }, {
      "name": "Objection: Price",
      "keywords": ["too expensive", "out of budget", "cant afford", "cheaper alternative"],
      "category": "OBJECTION"
    }]
  }'
```

### Recipe 10: Cross-tool offboarding (deactivate rep)

```python
# Single shot: deactivate across all three platforms
import requests, os

rep_email = "leaver@co.com"

# 1. Salesloft — find user, set active=false
sl_token = os.environ["SALESLOFT_TOKEN"]
u = requests.get(f"https://api.salesloft.com/v2/users",
                 headers={"Authorization": f"Bearer {sl_token}"},
                 params={"email": rep_email}).json()["data"][0]
requests.patch(f"https://api.salesloft.com/v2/users/{u['id']}",
               headers={"Authorization": f"Bearer {sl_token}"},
               json={"active": False})

# 2. Outreach — lock user
or_token = os.environ["OUTREACH_TOKEN"]
u = requests.get("https://api.outreach.io/api/v2/users",
                 headers={"Authorization": f"Bearer {or_token}"},
                 params={"filter[email]": rep_email}).json()["data"][0]
requests.patch(f"https://api.outreach.io/api/v2/users/{u['id']}",
               headers={"Authorization": f"Bearer {or_token}",
                        "Content-Type": "application/vnd.api+json"},
               json={"data": {"type": "user", "id": u["id"],
                              "attributes": {"locked": True}}})

# 3. Gong — deactivate
gong_basic = os.environ["GONG_BASIC"]
requests.put("https://api.gong.io/v2/users/extensive",
             headers={"Authorization": f"Basic {gong_basic}"},
             json={"filter": {"emailAddresses": [rep_email]},
                   "update": {"active": False}})

print(f"Deactivated {rep_email} across Salesloft + Outreach + Gong")
```

### Recipe 11: Gong call extraction (for stalled-deal Slack alerts)

```bash
# Get recent calls for an opportunity owner
curl -X POST "https://api.gong.io/v2/calls/extensive" \
  -H "Authorization: Basic $GONG_BASIC" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "fromDateTime": "2026-06-01T00:00:00Z",
      "toDateTime": "2026-06-11T23:59:59Z",
      "primaryUserIds": ["5012345"]
    },
    "contentSelector": {
      "exposedFields": {
        "content": {"trackers": true, "topics": true},
        "interaction": {"speakers": true, "sentiment": true}
      }
    }
  }'
```

### Recipe 12: Salesloft cadence step audit

```python
# Find cadences with > 10 steps (too long, low completion)
import requests, os

token = os.environ["SALESLOFT_TOKEN"]
hdr = {"Authorization": f"Bearer {token}"}

cadences = requests.get("https://api.salesloft.com/v2/cadences?per_page=100",
                        headers=hdr).json()["data"]
for c in cadences:
    if c["total_actions"] > 10:
        print(f"BLOAT: {c['name']} — {c['total_actions']} actions")
```

## Examples

### Example 1: New AE onboarding (provision across stack)

**Goal:** Day 1 — new AE has Salesloft + Outreach + Gong accounts active.

**Steps:**
1. Pull AE info (email, name, manager, team) from HR system or notion onboarding doc.
2. Run Recipe 2 (Salesloft) + Recipe 3 (Outreach) + Recipe 4 (Gong) in parallel.
3. Add to default shared cadences (Salesloft `cadence_memberships` POST).
4. Subscribe to Gong call review for their pod manager (Gong `POST /v2/calls/subscribers`).
5. Slack confirmation to #sales-ops + manager.

**Result:** AE has working access on day 1; no day-3 ticket queue.

### Example 2: Quarterly cadence audit + cleanup

**Goal:** Cull stale + duplicate cadences; reduce SDR confusion.

**Steps:**
1. Recipe 5 — pull all cadences with metadata.
2. Recipe 6 — flag those not updated in 180+ days as stale.
3. Manual review with sales-enablement: which named cadences are still official?
4. Archive stale + duplicates via Recipe 6.
5. Recipe 12 — flag cadences with > 10 steps for redesign.

**Result:** Cadence inventory cut 40-60%; SDR onboarding doc is sane.

### Example 3: Competitor smart-tracker rollout

**Goal:** A new competitor "BetaCo" emerges; track mention rate across all calls.

**Steps:**
1. Recipe 9 — add smart tracker with keyword variants ("BetaCo", "Beta Co", "Beta platform").
2. Wait 1 week to accumulate data.
3. Pull tracker hits via Recipe 11 with `trackers: true` in contentSelector.
4. Report to product marketing: top 10 calls where BetaCo was discussed.
5. Use rate of mention to seed `win-loss-reporting-at-scale` competitor analysis.

**Result:** Early-warning system for competitor entrants; battlecard requests prioritized.

## Edge cases / gotchas

- **Salesloft API token is user-scoped, not org-scoped** — token tied to admin user; rotates if admin leaves. Use a service account.
- **Outreach OAuth refresh token expires** — client_credentials flow is the right pattern; refresh is automatic.
- **Gong API rate limit is harsh** — 3 calls/sec, 10K calls/day. Batch endpoints exist (`/v2/calls/extensive`); use them.
- **Gong API uses Basic auth, not Bearer** — base64(key:secret), not OAuth.
- **Outreach JSON:API spec** — strict; Content-Type `application/vnd.api+json`, every entity wrapped in `{"data": {...}}`. Easy 400 errors.
- **Cadence `current_state` values**: `draft`, `active`, `archived`. Not `enabled` / `disabled`.
- **Outreach sequence templates vs sequences** — templates are reusable; sequences are instances. Don't conflate.
- **Gong scorecards must be assigned to call types** — creating doesn't auto-apply; configure via `POST /v2/calls/scorecards/{id}/assignments`.
- **User deactivation isn't deletion** — preserves data. Don't `DELETE` users; `PATCH active=false`.
- **Salesloft cadence_memberships unique constraint** — adding same user twice = 422 error. Idempotent: check first.
- **Gong trackers can be too broad** — "price" matches "your pricing is reasonable" → false positive. Phrase whole queries.
- **API key rotation** — Salesloft tokens persist until revoked; rotate quarterly. Document in notion runbook.
- **Outreach `userType` values**: `Standard`, `Admin`, `SalesLeader`. Wrong value = silent permission gap.
- **Cross-tool sync lag** — Salesloft → Salesforce sync is 5-min batched. Don't expect immediate state.
- **Gong includes both Zoom + Meet + Teams** — but recording-coverage gaps if Zoom integration is broken. Quarterly Recording-Coverage audit.

## Sources

- [Salesloft API docs](https://developers.salesloft.com/api.html)
- [Salesloft Cadences API](https://developers.salesloft.com/api.html#tag/Cadences)
- [Outreach API docs (JSON:API)](https://developers.outreach.io/api/)
- [Outreach Sequences API](https://developers.outreach.io/api/reference/tag/Sequence)
- [Gong API docs](https://app.gong.io/settings/api/documentation)
- [Gong Calls API + Trackers](https://help.gong.io/article/uw3rq02kk6-public-api)
- [Outreach OAuth client-credentials](https://developers.outreach.io/api/authentication/)
- [Salesloft rate limits](https://developers.salesloft.com/docs/rate-limits)
