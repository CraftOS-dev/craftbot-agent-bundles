<!--
Source: https://developers.outreach.io/api/ + https://developers.salesloft.com/api.html
Outreach + Salesloft + lemlist + Instantly — multi-channel sequence orchestration (June 2026 SOTA).
-->
# Outreach + Salesloft + lemlist + Instantly — Sequences SKILL

Four sequence engines, picked by use case: **Outreach** + **Salesloft** for enterprise SDR teams with deep CRM integration and managers reviewing call/email mix; **lemlist** for personalized hybrid email+LinkedIn at SMB scale; **Instantly** for high-volume cold email with built-in warmup. All four covered via the Maton `api-gateway` managed-OAuth proxy.

## When to use

- **Design a multi-channel cadence** (email + LinkedIn + phone) — Outreach / Salesloft are the standard; lemlist if email+LinkedIn natively orchestrated.
- **Launch a cold email campaign** with throttled sends, A/B subjects, warmup — Instantly is the volume play; lemlist for personalization-first.
- **Enroll a batch of contacts** in an existing sequence after enrichment / handoff.
- **Pause / resume / move** contacts between sequences when stage or signal changes.
- **Trigger phrases**: "build a 7-touch sequence", "enroll these 30 contacts in cadence Y", "set up an outbound campaign for ICP X", "pause everyone whose deal closed", "A/B test these subjects".

Do NOT use this skill for: **single one-off emails** (just send via `gmail` / `outlook`); **transactional sends** (use Resend / Postmark via `api-gateway`); **email warmup** (use the dedicated `cold-email-deliverability-warmup` skill).

## Setup

```bash
# Managed OAuth via Maton
export MATON_API_KEY="<maton-key>"

# Direct fallbacks (only if gateway unavailable):
export OUTREACH_ACCESS_TOKEN="<oauth-token>"            # Outreach.io OAuth 2.0, refresh every 7200s
export SALESLOFT_API_KEY="<api-key>"                    # Salesloft personal access token
export LEMLIST_API_KEY="<api-key>"                      # lemlist team settings
export INSTANTLY_API_KEY="<api-key>"                    # Instantly v2 key
```

Auth notes:
- **Outreach**: full OAuth 2.0; user-scoped; refresh token required. Free trial available; paid starts at $100/seat/mo.
- **Salesloft**: legacy API keys still supported; OAuth recommended for new apps. Pricing on request, ~$100-160/seat/mo.
- **lemlist**: team-level API key; pricing $59-99/seat/mo.
- **Instantly**: workspace API key; $37-97/mo per workspace flat (unlimited mailboxes), separate plan for warmup ($30/mo per workspace).

## Common recipes

### Recipe 1: Outreach — create a sequence (manual mailbox steps)

```bash
curl -X POST "https://gateway.maton.ai/outreach/api/v2/sequences" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{
    "data":{
      "type":"sequence",
      "attributes":{
        "name":"Q3 — ICP VPMarketing Cold",
        "shareType":"shared",
        "sequenceType":"interval",
        "scheduleIntervalType":"calendar",
        "primaryReplyAction":"finish",
        "primaryReplyPauseType":"primary"
      }
    }
  }'
```

Returns the sequence `id`. Then add steps via `/api/v2/sequenceSteps` (1 call per step, ordering by `order`).

### Recipe 2: Outreach — add an email step + template

```bash
# Step 1: create the step
curl -X POST "https://gateway.maton.ai/outreach/api/v2/sequenceSteps" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{
    "data":{
      "type":"sequenceStep",
      "attributes":{"order":1,"stepType":"auto_email","interval":0},
      "relationships":{"sequence":{"data":{"type":"sequence","id":"<seq-id>"}}}
    }
  }'

# Step 2: create the template
curl -X POST "https://gateway.maton.ai/outreach/api/v2/sequenceTemplates" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/vnd.api+json" \
  -d '{
    "data":{
      "type":"sequenceTemplate",
      "attributes":{"isReply":false},
      "relationships":{
        "sequenceStep":{"data":{"type":"sequenceStep","id":"<step-id>"}},
        "template":{"data":{"type":"template","id":"<template-id>"}}
      }
    }
  }'
```

`interval` is in *days* from prior step. For Day 0, set `interval: 0`.

### Recipe 3: Outreach — enroll a prospect

```bash
curl -X POST "https://gateway.maton.ai/outreach/api/v2/sequenceStates" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/vnd.api+json" \
  -d '{
    "data":{
      "type":"sequenceState",
      "relationships":{
        "prospect":{"data":{"type":"prospect","id":"<prospect-id>"}},
        "sequence":{"data":{"type":"sequence","id":"<seq-id>"}},
        "mailbox":{"data":{"type":"mailbox","id":"<mailbox-id>"}}
      }
    }
  }'
```

`mailbox` must be the user's connected inbox; one prospect can be in only one sequence at a time per mailbox.

### Recipe 4: Salesloft — create a cadence

```bash
curl -X POST "https://gateway.maton.ai/salesloft/v2/cadences" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"Q3 — ICP CTO Cold",
    "team_cadence":true,
    "shared":true,
    "remove_bounces_enabled":true,
    "remove_replies_enabled":true,
    "external_identifier":"q3-icp-cto-cold"
  }'
```

### Recipe 5: Salesloft — add steps with day intervals

```bash
curl -X POST "https://gateway.maton.ai/salesloft/v2/steps" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "cadence_id":<cadence-id>,
    "type":"Email",
    "day":1,
    "name":"Day 1 — opener",
    "details":{"email_template_id":<template-id>,"step_type":"Email"}
  }'
```

Step types: `Email`, `Phone`, `Other` (custom — LinkedIn, in-mail, gift). `day` is calendar day index from enrollment.

### Recipe 6: Salesloft — bulk enroll people

```bash
curl -X POST "https://gateway.maton.ai/salesloft/v2/cadence_memberships" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "person_id":<person-id>,
    "cadence_id":<cadence-id>,
    "user_id":<sdr-user-id>,
    "currently_on_cadence":false
  }'
```

Loop 100x for 100 prospects; respect 600 req/min rate limit.

### Recipe 7: lemlist — create a personalized hybrid campaign

```bash
curl -X POST "https://gateway.maton.ai/lemlist/api/campaigns" \
  -u ":$LEMLIST_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"Q3 ICP Hybrid",
    "campaignSchedule":{"timezone":"UTC","startHour":"09:00","endHour":"17:00","weekDays":["Mon","Tue","Wed","Thu"]},
    "steps":[
      {"type":"email","delay":0,"subject":"{{firstName}}, quick thought on {{companyName}}","body":"Hi {{firstName}},\n\nNoticed {{customVar1}}..."},
      {"type":"linkedinVisit","delay":1},
      {"type":"linkedinInvite","delay":2,"message":"Hi {{firstName}} — followed up via email last week."},
      {"type":"email","delay":4,"subject":"re:","body":"Bumping the thread."},
      {"type":"linkedinMessage","delay":6,"message":"Worth a quick chat?"}
    ]
  }'
```

Note: `linkedinInvite` + `linkedinMessage` require lemlist's LinkedIn integration ($59 add-on or Pro plan); without it, those steps silently skip.

### Recipe 8: lemlist — add leads to a campaign

```bash
curl -X POST "https://gateway.maton.ai/lemlist/api/campaigns/<campaign-id>/leads" \
  -u ":$LEMLIST_API_KEY" -H "Content-Type: application/json" \
  -d '[
    {"email":"sam@acme.com","firstName":"Sam","companyName":"Acme","customVar1":"your Series B last month"},
    {"email":"pat@globex.io","firstName":"Pat","companyName":"Globex","customVar1":"your CTO joined from Stripe"}
  ]'
```

### Recipe 9: Instantly — create + launch a cold campaign (v2 API)

```bash
curl -X POST "https://gateway.maton.ai/instantly/api/v2/campaigns" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"Q3 Cold — VP Marketing",
    "campaign_schedule":{
      "schedules":[{"name":"Default","timing":{"from":"09:00","to":"17:00"},"days":{"1":true,"2":true,"3":true,"4":true,"5":false,"6":false,"0":false},"timezone":"America/New_York"}]
    },
    "sequences":[{
      "steps":[
        {"type":"email","delay":0,"variants":[{"subject":"{{firstName}}, quick question","body":"Hi {{firstName}}, ..."}]},
        {"type":"email","delay":3,"variants":[{"subject":"re:","body":"Bumping..."}]},
        {"type":"email","delay":7,"variants":[{"subject":"closing the loop","body":"Last note..."}]}
      ]
    }],
    "email_list":["sender1@brand-cold.com","sender2@brand-cold.com"],
    "daily_limit":50,
    "stop_on_reply":true,
    "stop_on_auto_reply":true
  }'
```

### Recipe 10: Instantly — add leads via v2

```bash
curl -X POST "https://gateway.maton.ai/instantly/api/v2/leads/list" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "campaign":"<campaign-id>",
    "skip_if_in_workspace":true,
    "skip_if_in_campaign":true,
    "leads":[
      {"email":"sam@acme.com","first_name":"Sam","last_name":"Lee","company_name":"Acme","custom_variables":{"hook":"Series B last month"}},
      {"email":"pat@globex.io","first_name":"Pat","last_name":"Cruz","company_name":"Globex","custom_variables":{"hook":"CTO ex-Stripe"}}
    ]
  }'
```

### Recipe 11: Pause / finish sequence (all four platforms)

```bash
# Outreach
curl -X PATCH "https://gateway.maton.ai/outreach/api/v2/sequenceStates/<state-id>" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/vnd.api+json" \
  -d '{"data":{"type":"sequenceState","id":"<state-id>","attributes":{"state":"paused"}}}'

# Salesloft
curl -X DELETE "https://gateway.maton.ai/salesloft/v2/cadence_memberships/<membership-id>" \
  -H "Authorization: Bearer $MATON_API_KEY"

# lemlist
curl -X POST "https://gateway.maton.ai/lemlist/api/campaigns/<campaign-id>/leads/<lead-email>/unsubscribe" \
  -u ":$LEMLIST_API_KEY"

# Instantly
curl -X POST "https://gateway.maton.ai/instantly/api/v2/leads/list/<lead-id>" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{"status":"paused"}'
```

### Recipe 12: A/B subject variants (Instantly + Outreach)

```bash
# Instantly: variants array in step (Recipe 9 already shows). Engine auto-balances.
# Outreach: create two sequenceTemplates on same step, set isReply on neither — Outreach rotates 50/50.
```

## Examples

### Example 1: Build + launch a 7-touch SDR cadence in Outreach

**Goal:** Ship a Day-0 / Day-2 LI / Day-4 email / Day-7 call / Day-10 break-up cadence and enroll 200 prospects.

**Steps:**
1. Recipe 1: create sequence "Q3 ICP VPMktg".
2. Recipe 2 x5 with email/call/LinkedIn step types; intervals 0, 2, 2, 3, 3 days.
3. Pre-create templates in Outreach UI (or via `/api/v2/templates`), record IDs.
4. Use `apollo-clay-lead-enrichment` recipe 1 to source the 200 prospects; upsert to Outreach as `prospects` via `/api/v2/prospects`.
5. Recipe 3 in a loop (or `bulkEnroll` endpoint) to enroll all 200 with the SDR's mailbox.
6. After 14 days: pull `/api/v2/mailings?filter[sequenceState]=<id>` for reply/open/bounce stats; if reply-rate < 2%, iterate copy.

**Result:** Live cadence with 200 enrolled, dashboard reportable in Outreach UI + via API.

### Example 2: High-volume Instantly cold campaign with warmup

**Goal:** 5,000 sends/week across 10 mailboxes on a cold-outbound domain, with warmup running in parallel.

**Steps:**
1. Pre-flight: run `cold-email-deliverability-warmup` skill recipes to verify SPF/DKIM/DMARC + 4-week warmup complete.
2. Recipe 9: create campaign with `daily_limit: 50` per mailbox (10 mailboxes x 50 = 500/day, 5x weekdays = 2,500/week — adjust to 100/mailbox after 2 weeks healthy).
3. Recipe 10: bulk-upload 5,000 enriched leads (use `apollo-clay-lead-enrichment` first to verify deliverability).
4. Monitor `GET /api/v2/campaigns/<id>/analytics` daily — alert if bounce > 2%, reply-rate < 2%, or complaint > 0.1%.
5. After week 2, raise `daily_limit` to 100 if healthy.

**Result:** ~2,500-5,000 sends/week with deliverability monitored, leads flowing into CRM via Instantly's HubSpot/Salesforce integration.

## Edge cases / gotchas

- **Outreach requires JSON-API content type** (`application/vnd.api+json`) and the `data.type` envelope; plain JSON gets 400. Easy to miss when copy-pasting from other API examples.
- **Outreach mailbox connection** is per-user — you can create a sequence centrally but enrollment must specify a mailbox the *enrolling* user owns. Sharing mailboxes across SDRs is not supported.
- **Salesloft cadence `day` is calendar days from enrollment**, not days-between. Day 0 is sent immediately; Day 1 is next business day at the cadence's send window. Skipped weekend days are configurable per workspace.
- **lemlist LinkedIn steps require Pro plan** ($99/seat); without it, LinkedIn steps silently skip and the cadence shortens — quietly.
- **lemlist API auth is HTTP Basic with empty user + API-key as password** (`-u ":KEY"`). Bearer auth gives 401.
- **Instantly v2 deprecated several v1 endpoints in Q4 2025**; if you see `/api/v1/...` in examples online, prefer v2 paths. v1 still works but is read-only for new accounts.
- **Instantly's "Stop on auto-reply"** is conservative — it pauses if any auto-reply phrase matches, including OOO. Set `stop_on_auto_reply: false` if you want OOOs to *not* pause (and handle OOO separately).
- **Rate limits**: Outreach 10k req/hr per app; Salesloft 600 req/min per token; lemlist 60 req/min; Instantly 60 req/min (higher on enterprise).
- **Inbox rotation is mandatory** at >100/day per mailbox. Burning a single inbox is the #1 cause of cold-domain blacklisting. Instantly auto-rotates; Outreach/Salesloft require manual round-robin (set `mailbox` per enrollment).
- **Reply detection is heuristic** — all four platforms occasionally miss replies in long threads or replies-from-shared-inbox. Pair with a CRM-side check (`hubspot-sales-mcp` recipe 8) for stale-thread detection.
- **CAN-SPAM / GDPR**: every send must include sender postal address + unsubscribe link. All four platforms inject this on shared templates but custom templates need explicit footers.

## Sources

- Outreach.io API: https://developers.outreach.io/api/
- Salesloft API: https://developers.salesloft.com/api.html
- lemlist API: https://developer.lemlist.com/
- Instantly API v2: https://help.instantly.ai/en/articles/8500911-instantly-api-v2
- Outreach.io vs Salesloft 2026 review: https://blog.gong.io/outreach-vs-salesloft/
- Instantly vs lemlist for cold outbound 2026: https://www.smartlead.ai/blog/instantly-vs-lemlist
