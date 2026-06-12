<!--
Source: https://www.heyreach.io/ + https://phantombuster.com/ + LinkedIn Sales Navigator
LinkedIn outbound at safe daily volumes (June 2026 SOTA, TOS-aware).
-->
# LinkedIn Sales Navigator Outreach — SKILL

LinkedIn has no public API for connection-sending or DMs. The realistic stack is: **HeyReach** (TOS-respectful, multi-account safe, ~$79/mo), **Phantombuster** (broader scraping + automation, ~$59-149/mo), **TexAu** (cheaper, ~$29-79/mo). All three drive a logged-in LinkedIn session at safe daily limits. Sales Navigator searches give the targeting; the automation tool runs connection + message sequences.

## When to use

- **LinkedIn outbound layer** of a multi-channel sequence (paired with email cadence in `outreach-salesloft-sequences`).
- **Connection-request campaign** to a 100-500 person target list — safe daily volume 15-25 invites per account.
- **Profile-view warmup** before DMing — "let me show up in their notifications first".
- **Sales Nav-list export** for upload to a CRM or enrichment tool.
- **Trigger phrases**: "LinkedIn outreach campaign", "send connection requests to these 50", "warm them up on LinkedIn first", "scrape this Sales Nav list", "LinkedIn sequence to ICP X".

Do NOT use this skill for: **mass cold InMail blasts** (LinkedIn rate-limits + counts InMail credits separately — use sparingly); **competitor employee poaching** (TOS-risky); **personal LinkedIn networking** (use the human UI).

## Setup

```bash
# HeyReach — preferred for safety + multi-account orchestration
export HEYREACH_API_KEY="<key>"
# HeyReach pricing: $79/mo per LinkedIn account (Starter), $999/mo for agency/10-seat

# Phantombuster — broader scraping toolkit
export PHANTOMBUSTER_API_KEY="<key>"
# $59/mo Starter, $149/mo Pro

# TexAu — cheaper alt
export TEXAU_API_KEY="<key>"

# LinkedIn cookie (li_at) — required to drive a session. Pulled from a logged-in browser.
export LI_AT_COOKIE="<cookie-value>"
# Rotate every 30-60 days; LinkedIn invalidates cookies on detection of automation.

# Optional brightdata-mcp for Sales Nav search-result scraping at scale
export BRIGHTDATA_API_KEY="<key>"
```

**Pre-flight requirements:**
- **LinkedIn account** must be a real human-aged account (90+ days old, 100+ connections, with photo + headline). Brand-new "throwaway" accounts get auto-flagged within hours.
- **Sales Navigator subscription** ($99/mo Core, $149/mo Advanced, $169/mo Advanced Plus) — needed for the search filters HeyReach/Phantombuster use.
- **Daily volume limits** (TOS-safe ceilings per account per day):
  - Connection requests: 15-25
  - Messages to 1st-degree connections: 50-100
  - Profile views: 50-100
  - Search results loaded: 100-200
  - InMail (to non-connections): 5-10 (gates on credit balance)

## Common recipes

### Recipe 1: HeyReach — create a LinkedIn sequence campaign

```bash
curl -X POST "https://api.heyreach.io/api/v1/campaign" \
  -H "X-Api-Key: $HEYREACH_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"Q3 — VP Marketing Cold (LinkedIn)",
    "linkedinAccountId":"<your-account-id>",
    "sequence":{
      "steps":[
        {"type":"viewProfile","delayDays":0},
        {"type":"likePost","delayDays":1},
        {"type":"connect","delayDays":2,"message":"Hi {{firstName}} — noticed {{customField1}}. Worth connecting?"},
        {"type":"message","delayDays":3,"text":"{{firstName}}, thanks for the connect — quick question on {{topic}}..."},
        {"type":"message","delayDays":7,"text":"Bumping — any thoughts?"}
      ]
    },
    "dailyLimit":{"invites":20,"messages":40,"views":50}
  }'
```

### Recipe 2: HeyReach — upload leads from a Sales Nav search

```bash
# Step 1: in Sales Nav UI, build the search; copy the URL.
# Step 2: HeyReach imports from URL
curl -X POST "https://api.heyreach.io/api/v1/campaign/<campaign-id>/lead-list" \
  -H "X-Api-Key: $HEYREACH_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "type":"salesNavSearch",
    "salesNavUrl":"https://www.linkedin.com/sales/search/people?keywords=...",
    "maxResults":500
  }'
```

HeyReach pages through the search at safe rates (~100/day per account).

### Recipe 3: Phantombuster — Sales Navigator search export

```bash
# Phantombuster has a "Sales Navigator Search Export" agent
PHANTOM_ID="<agent-id>"
curl -X POST "https://api.phantombuster.com/api/v2/agents/launch" \
  -H "X-Phantombuster-Key-1: $PHANTOMBUSTER_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "id":"'$PHANTOM_ID'",
    "argument":{
      "sessionCookie":"'$LI_AT_COOKIE'",
      "searchUrl":"https://www.linkedin.com/sales/search/people?keywords=VP+Marketing+SaaS",
      "numberOfLines":200,
      "csvName":"q3-vpmkt-export"
    }
  }'
# Returns containerId; poll /agents/fetch-output to get CSV when done (~5-15 min)
```

### Recipe 4: Phantombuster — connection request sender

```bash
PHANTOM_ID="<linkedin-network-booster-agent-id>"
curl -X POST "https://api.phantombuster.com/api/v2/agents/launch" \
  -H "X-Phantombuster-Key-1: $PHANTOMBUSTER_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "id":"'$PHANTOM_ID'",
    "argument":{
      "sessionCookie":"'$LI_AT_COOKIE'",
      "spreadsheetUrl":"https://docs.google.com/spreadsheets/d/<id>/...",
      "message":"Hi #firstName#, noticed #companyName# is hiring SDRs — worth connecting?",
      "numberOfAddsPerLaunch":15,
      "waitDuration":3600
    }
  }'
```

Schedule via Phantombuster's built-in cron at safe hours (8am-5pm local, weekdays).

### Recipe 5: TexAu — cheaper alt (workflow + automation)

```bash
curl -X POST "https://api.texau.com/v1/workflow/run" \
  -H "Authorization: Bearer $TEXAU_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "workflow_id":"<linkedin-connect-workflow>",
    "input":{
      "li_at_cookie":"'$LI_AT_COOKIE'",
      "search_url":"https://www.linkedin.com/sales/search/people?...",
      "max_per_day":20,
      "message_template":"Hi {{first_name}}, ..."
    }
  }'
```

TexAu's workflow builder is more visual; same underlying pattern.

### Recipe 6: Browse + scrape a Sales Nav account list (brightdata-mcp fallback)

```bash
# When HeyReach/Phantombuster API isn't onboarded, brightdata-mcp can render and parse
mcp tool brightdata.scrape_url \
  --url "https://www.linkedin.com/sales/lists/people/<list-id>" \
  --renderJs true \
  --cookies '[{"name":"li_at","value":"'$LI_AT_COOKIE'","domain":".linkedin.com"}]'
```

Returns the rendered DOM; parse with selectors (the DOM changes monthly — keep selectors versioned).

### Recipe 7: 6-step LinkedIn-only sequence

```yaml
# A safer, slower-burn LinkedIn cadence
day_0:
  action: view_profile
  why: "show up in their 'who viewed your profile' notifications"
day_2:
  action: like_recent_post
  why: "low-friction engagement before pitch"
day_4:
  action: connect_request
  message: "Hi {{firstName}}, saw your post on {{recentTopic}} — would love to follow your work."
  why: "no pitch in connect message; acceptance rate doubles"
day_7:  # only if accepted
  action: dm_first
  message: "Thanks for the connect, {{firstName}}. Quick question — how are you handling {{painArea}} at {{companyName}}? Working with a few similar teams on it."
day_10:
  action: dm_followup
  message: "Bumping the thread — happy to share what we're seeing with similar teams. 15 min worth it?"
day_14:
  action: dm_closeout
  message: "Closing the loop — if not the right time, totally understood. Will keep following your work. Open to a chat anytime."
```

### Recipe 8: Hybrid email + LinkedIn cadence (via lemlist or HeyReach)

```yaml
# Run in lemlist (Recipe 7 of outreach-salesloft-sequences) for orchestration
day_0: email_1
day_2: linkedin_view_profile
day_3: linkedin_connect
day_5: email_2 (only if no LinkedIn reply)
day_7: linkedin_dm (only if accepted)
day_10: email_3 (break-up)
```

The cross-channel choreography lifts reply rate ~2-3x vs single-channel.

### Recipe 9: Find a buyer's recent post (personalization hook source)

```bash
# Via playwright-mcp + LinkedIn profile recent activity tab
mcp tool playwright.navigate \
  --url "https://www.linkedin.com/in/<slug>/recent-activity/posts/" \
  --cookies '[{"name":"li_at","value":"'$LI_AT_COOKIE'"}]'
mcp tool playwright.extract_text \
  --selector "div.update-components-text"
```

Pull the first 2-3 posts; pick one to reference in the DM. Hooks tied to *their* content lift reply rate 2-4x.

### Recipe 10: Daily volume monitor + safety dashboard

```python
# Track per-account daily limits via HeyReach stats
import requests, os, datetime
r = requests.get(
    "https://api.heyreach.io/api/v1/linkedin-account/<account-id>/stats",
    headers={"X-Api-Key": os.environ["HEYREACH_API_KEY"]},
    params={"date": datetime.date.today().isoformat()},
).json()

LIMITS = {"invites":25, "messages":100, "views":100}
warnings = []
for k, cap in LIMITS.items():
    used = r.get(f"{k}_today", 0)
    if used > cap * 0.8:
        warnings.append(f"{k}: {used}/{cap} ({int(100*used/cap)}%) — slow down")
    if used > cap:
        warnings.append(f"{k}: EXCEEDED {used}/{cap} — paused for 24h")
print(warnings)
```

Wire to `slack-mcp` for ops alerts.

### Recipe 11: Re-warming a cooled account

```yaml
# If LinkedIn flags an account (warning email, captcha, restricted features):
day_0_to_7: human-only usage (no automation), 0-5 connections, normal engagement
day_8_to_14: restart at 5-10 connections/day with HeyReach
day_15_plus: ramp +2-3 daily, target 15-20/day after 30 days

# If multiple warnings: rotate the LinkedIn account, pause the automation tool's session entirely.
```

## Examples

### Example 1: 200-prospect LinkedIn campaign (HeyReach)

**Goal:** Hit 200 VP Marketing prospects with a 5-step LinkedIn-only sequence over 30 days.

**Steps:**
1. Sales Nav search built in UI; copy URL.
2. Recipe 2 — upload Sales Nav URL to a new HeyReach campaign with daily limit 20 invites.
3. Recipe 1 — define the 5-step sequence (view → like → connect → DM → DM-bump).
4. At 20/day connection requests, 200 takes 10 working days to send. Total elapsed: ~30 days end-to-end.
5. Recipe 10 — daily monitor; pause if Linkedin flags warning.

**Result:** 200 prospects engaged, expected ~40-60 connections accepted (20-30%), ~20-30 DM replies, ~5-10 meetings booked.

### Example 2: Hybrid email + LinkedIn for a 50-account ABM tier

**Goal:** 50 tier-1 accounts × 3 stakeholders each = 150 contacts, hit via email + LinkedIn coordinated.

**Steps:**
1. `account-research-deep` produces brief + 3 stakeholders per account.
2. lemlist hybrid campaign (Recipe 8) loaded with all 150 contacts.
3. lemlist runs day 0 email → day 2 LI view → day 3 LI connect → day 7 LI DM (if accepted) or day 5 email-2 (if not).
4. Replies go to AE inbox; non-replies cycle to break-up email day 10.

**Result:** ~2-3x reply rate vs single-channel; ~15-25 meetings from 150 contacts (10-17% rate, vs 5-8% single-channel).

## Edge cases / gotchas

- **LinkedIn TOS prohibits automation.** All three tools (HeyReach / Phantombuster / TexAu) operate in a gray zone — they drive a human-logged-in session via browser cookie. Safer than running scrapers, but accounts can still be flagged. **Stay under daily limits.**
- **Daily limits are per-account, not per-campaign.** Running two HeyReach campaigns on the same LinkedIn account doubles the volume from LinkedIn's POV; combine totals.
- **Account-bound**: each SDR needs their own LinkedIn + Sales Nav + HeyReach/Phantombuster seat. There's no central "send from team account" mode.
- **Cookie rotation**: `li_at` cookies expire ~30-60 days or sooner on detection. Re-extract from a freshly-logged-in browser. Phantombuster and TexAu both fail silently when the cookie expires.
- **Sales Nav search results paginate at 100/page**; total cap is ~2,500 results visible. For larger TAMs build multiple narrower searches.
- **InMail credits separate**: free InMails to non-connections require credits ($99/mo Sales Nav Core gets 50 credits/mo). Burning credits on cold InMail to wrong-ICP is wasteful; prefer connection-then-DM.
- **Open InMail (free)**: ~5% of LinkedIn users have it enabled; pre-filter your list for "open profile" badge before InMailing — Sales Nav shows this filter.
- **Connection-request message limit**: 300 chars. Long pitches truncate.
- **Acceptance rate without a message** (~30%) often beats *with* a salesy message (~10%). Test no-message vs short-message variants.
- **"Withdraw old pending invites"** monthly — LinkedIn caps total outstanding at ~3,000-5,000 across all accounts. Phantombuster has a "withdraw connection requests" agent for this.
- **Brand-new LinkedIn accounts** get flagged within 24-48h of automation start. Use accounts > 90 days old with > 100 manual connections.
- **Multi-account orchestration** (running 5+ LinkedIn accounts from one team) — HeyReach handles this best with per-account session isolation; Phantombuster requires manual session-per-agent setup.
- **Engagement before pitch** (Recipe 7 day-0 + day-2) lifts connect-acceptance by 2x. Don't skip the warmup.
- **Don't connect-then-pitch in the connect message** — LinkedIn deboost+ flags this pattern. Pitch in DM after acceptance.

## Sources

- HeyReach docs + features: https://www.heyreach.io/
- Phantombuster docs: https://hub.phantombuster.com/docs
- TexAu docs: https://help.texau.com/
- LinkedIn Sales Navigator help: https://www.linkedin.com/help/sales-navigator/
- LinkedIn TOS (automation language): https://www.linkedin.com/legal/user-agreement
- 2026 LinkedIn outbound playbook (HeyReach blog): https://www.heyreach.io/blog/linkedin-outbound-2026
- "Safe daily limits on LinkedIn" — Phantombuster: https://phantombuster.com/blog/safe-linkedin-limits
