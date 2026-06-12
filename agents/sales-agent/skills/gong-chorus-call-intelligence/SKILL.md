<!--
Source: https://app.gong.io/settings/api/documentation + https://help.fathom.video/en/articles/8430832-fathom-api
Call intelligence (Gong / Chorus / Fathom / Fireflies / tl;dv) — June 2026 SOTA.
-->
# Gong + Chorus + Fathom + Fireflies + tl;dv Call Intelligence — SKILL

Pull call transcripts + analytics for coaching, MEDDIC field-fill, objection mining, and deal-coaching signals. Gong is the enterprise standard ($1.6k+/seat/yr). Chorus is similar (Zoom-acquired, no public API — workaround via email export). Fathom + Fireflies + tl;dv are first-class API notetakers, much cheaper, used as Gong-lite or in addition to it.

## When to use

- **Post-call analysis**: pull transcript + extract talk-listen ratio, monologue length, objection mentions, sentiment shift, next-steps.
- **MEDDIC field-fill**: scan transcript for the buyer's stated metrics, EB title, decision criteria, pain quotes; auto-populate CRM fields.
- **Objection mining**: search across recent calls for "concerns", "worried", "competitor", "price"; group by frequency for battlecard updates.
- **Coaching extraction**: AE talk-listen ratio; question count; long-monologue flags.
- **Trigger phrases**: "summarize the call with X", "what did they push back on", "extract action items from yesterday's demo", "AE coaching report for this week", "find all calls where competitor Y came up".

Do NOT use this skill for: **transcribing a call you didn't already record** (Gong/Chorus/Fathom must be the joining notetaker — outside scope); **live coaching during a call** (real-time prompts belong to Gong Assist / Fathom Live — UI features, not API); **non-sales meetings** (use general meeting MCPs).

## Setup

```bash
# Managed OAuth via Maton for the four with first-class APIs
export MATON_API_KEY="<maton-key>"

# Direct fallbacks
export GONG_ACCESS_KEY="<gong-key>"        # Settings → Company → API; Enterprise+ only
export GONG_ACCESS_KEY_SECRET="<secret>"   # paired with access key for Basic Auth
export FATHOM_API_KEY="<key>"              # Settings → Integrations → API
export FIREFLIES_API_KEY="<key>"           # User Settings → Developer Settings → API
export TLDV_API_KEY="<key>"                # Workspace Settings → API (Business plan+)
# Chorus has no public API — use email-export workaround (see Recipe 9)
```

Pricing reference:
- **Gong**: ~$1,600-2,000/seat/year, enterprise-only sales motion; API included on Pro+.
- **Chorus**: Zoom-bundled or Chorus standalone ~$1,200/seat/yr; no public API.
- **Fathom**: free (unlimited recording!) + $19/seat/mo for Premium (CRM sync), $32 Team Edition (admin).
- **Fireflies**: $0 free (limited), $18/seat/mo Pro, $29 Business.
- **tl;dv**: free + $20/seat/mo Pro, $39 Business (CRM + API).

## Common recipes

### Recipe 1: Gong — list calls in a date range

```bash
curl -X POST "https://gateway.maton.ai/gong/v2/calls/extensive" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filter":{
      "fromDateTime":"2026-06-01T00:00:00Z",
      "toDateTime":"2026-06-09T23:59:59Z",
      "primaryUserIds":["<ae-user-id>"]
    },
    "contentSelector":{"context":"Extended","contextTiming":["Now"],"exposedFields":{"parties":true,"content":{"trackers":true,"topics":true,"pointsOfInterest":true},"interaction":{"speakers":true,"questions":true}}}
  }'
```

Returns calls with `id`, `parties`, `topics`, `trackers` (Gong's mention-of-keyword tracker fires for "competitor", "pricing", "objection" etc).

### Recipe 2: Gong — pull a transcript

```bash
curl -X POST "https://gateway.maton.ai/gong/v2/calls/transcript" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filter":{"callIds":["<call-id>"]}
  }' | jq '.callTranscripts[0].transcript[] | {speakerId, sentences: [.sentences[].text]}'
```

Returns sentence-level transcript with `start`, `end`, `speakerId`. Pair with `/calls/users/extensive` to map `speakerId` to person names.

### Recipe 3: Gong — talk-listen ratio + question count for an AE

```bash
# Get call stats for one rep over a week
curl -X POST "https://gateway.maton.ai/gong/v2/calls/extensive" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "filter":{"fromDateTime":"2026-06-01T00:00:00Z","toDateTime":"2026-06-07T23:59:59Z","primaryUserIds":["<ae-id>"]},
    "contentSelector":{"context":"Extended","exposedFields":{"interaction":{"speakers":true,"questions":true}}}
  }' | jq '[.calls[] | {
    callId: .metaData.id,
    talkRatio: (.interaction.speakers[] | select(.id == "<ae-id>") | .talkTime),
    questions: (.interaction.questions | length)
  }]'
```

Coaching benchmarks: AE talk-time 40-50% on discovery, 35-45% on demo; > 60% = AE is monologuing; < 30% = AE is being interrogated. Question count > 8 on discovery; < 5 = under-discovered.

### Recipe 4: Gong — tracker search (find all calls where "competitor X" came up)

```bash
# Trackers are configured in Gong UI; here we filter by tracker name
curl -X POST "https://gateway.maton.ai/gong/v2/calls/extensive" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "filter":{"fromDateTime":"2026-04-01T00:00:00Z","toDateTime":"2026-06-09T23:59:59Z"},
    "contentSelector":{"exposedFields":{"content":{"trackers":true}}}
  }' | jq '.calls[] | select(.content.trackers[]?.name | test("CompetitorX"))'
```

### Recipe 5: Fathom — list recent meetings

```bash
curl -X GET "https://api.fathom.video/external/v1/meetings?from=2026-06-01&to=2026-06-09" \
  -H "X-Api-Key: $FATHOM_API_KEY"
```

Returns meetings with `id`, `summary`, `action_items[]`, `share_url`. Fathom auto-extracts action items via LLM — usually better than Gong's structured fields for small teams.

### Recipe 6: Fathom — pull transcript for one meeting

```bash
curl -X GET "https://api.fathom.video/external/v1/meetings/<meeting-id>/transcript" \
  -H "X-Api-Key: $FATHOM_API_KEY"
```

Returns the transcript as time-stamped segments with speaker labels.

### Recipe 7: Fireflies — GraphQL query for meeting transcript

```bash
curl -X POST "https://api.fireflies.ai/graphql" \
  -H "Authorization: Bearer $FIREFLIES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query":"query Transcript($id: String!) { transcript(id: $id) { id title sentences { text speaker_name start_time } summary { keywords action_items } } }",
    "variables":{"id":"<transcript-id>"}
  }'
```

Fireflies offers AI-generated `summary.action_items` and `summary.keywords` out of the box.

### Recipe 8: tl;dv — get meeting + AI report

```bash
curl -X GET "https://gateway.maton.ai/tldv/v1/meetings/<meeting-id>" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

Returns `transcript_url`, `ai_notes`, `highlights[]`. tl;dv's `ai_notes` is structured (decisions, action items, questions) and works well as a MEDDIC-fill input.

### Recipe 9: Chorus workaround — email export parse

```bash
# In Chorus UI: configure "send transcript to email" per call.
# Forward those emails to a parsed mailbox; extract body via gmail-mcp.
# Example: pull all Chorus emails this week, dump transcripts to disk.

# Via gmail-mcp
# search: from:noreply@chorus.ai subject:"Call recap"
# for each: read body, save to /tmp/chorus-<callId>.txt
```

This is the only path until Chorus exposes a public API; Zoom acquired Chorus in 2021 and the API has been promised but not shipped as of June 2026.

### Recipe 10: Extract MEDDIC fields from a transcript (LLM-driven)

```python
# Run after Recipe 2 / 6 / 7 — feed transcript to a model to extract MEDDIC
import anthropic, json, os
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

transcript = open("/tmp/call-123-transcript.txt").read()

prompt = f"""From the sales call transcript below, extract MEDDIC fields. Return strict JSON with keys:
- metrics: the business outcome the buyer named (verbatim if possible)
- economic_buyer: name + title of the person with budget authority, or null
- decision_criteria: the criteria the buyer said they'd evaluate on
- decision_process: the buyer's stated steps from now to signed contract
- identify_pain: the specific pain the buyer articulated (verbatim quote preferred)
- champion: name of the person actively advocating, or null
For each field add a quality score 0-3 (0=empty, 1=hypothesis, 2=stated by buyer, 3=stated+documented evidence).

Transcript:
{transcript}
"""

resp = client.messages.create(model="claude-sonnet-4-5", max_tokens=1500, messages=[{"role":"user","content":prompt}])
meddic = json.loads(resp.content[0].text)
print(meddic)
```

Then write back to CRM via `hubspot-sales-mcp` recipe 2.

### Recipe 11: Objection mining across calls (last 30 days)

```python
# Pull all calls in last 30 days, search for objection patterns, group by frequency
import requests, os, re
from collections import Counter

resp = requests.post(
    "https://gateway.maton.ai/gong/v2/calls/extensive",
    headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"},
    json={"filter":{"fromDateTime":"2026-05-09T00:00:00Z","toDateTime":"2026-06-09T23:59:59Z"}}
).json()

OBJECTION_PATTERNS = {
    "price": r"\b(too expensive|pricing|budget|cost|too high)\b",
    "competitor": r"\b(we use [A-Z]|we have|already with|happy with)\b",
    "timing": r"\b(not now|not the right time|next quarter|later)\b",
    "feature_gap": r"\b(missing|doesn't have|need.*to|can it)\b",
    "internal_buy_in": r"\b(get approval|need to talk|run it by)\b",
}

counts = Counter()
for call in resp.get("calls", []):
    transcript = requests.post(
        "https://gateway.maton.ai/gong/v2/calls/transcript",
        headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"},
        json={"filter":{"callIds":[call["metaData"]["id"]]}}
    ).json()
    text = " ".join([s["text"] for t in transcript.get("callTranscripts", []) for sent in t.get("transcript", []) for s in sent.get("sentences", [])])
    for label, pat in OBJECTION_PATTERNS.items():
        if re.search(pat, text, re.I):
            counts[label] += 1

print(counts.most_common())
```

Output drives battlecard updates (`sales-enablement-battlecards-roi-calculators`).

## Examples

### Example 1: AE weekly coaching report

**Goal:** Every Monday, generate a coaching summary per AE: talk-listen ratio, monologue count, question count, top-3 objections from the week.

**Steps:**
1. Recipe 1 — list last week's calls per AE.
2. Recipe 3 — extract talk-listen + question count per call.
3. Recipe 11 — pull top objections heard.
4. Aggregate to a Notion page per AE with diff vs prior week. Slack DM the AE with one coaching ask.

**Result:** Manager has 5-min coaching ammunition for each AE every Monday.

### Example 2: Auto-fill MEDDIC after each discovery call

**Goal:** Within 1 hour of a discovery call ending, populate MEDDIC fields on the related deal.

**Steps:**
1. Gong webhook fires on call-complete → posts to your handler.
2. Recipe 2 — pull transcript.
3. Recipe 10 — LLM extracts MEDDIC fields.
4. `hubspot-sales-mcp` recipe 2 — PATCH deal with extracted fields.
5. If any field is 0/1 quality, create a HubSpot task: "Re-engage to validate <field>".

**Result:** Zero manual MEDDIC entry; gaps surfaced same-day.

## Edge cases / gotchas

- **Gong API requires Pro+ tier**. Starter tier is UI-only. Confirm with customer's Gong CSM before assuming API access.
- **Gong Basic Auth uses `<access_key>:<secret>` base64-encoded** when going direct (not via gateway). Forgetting the secret = 401.
- **Gong's `extensive` endpoint is paginated** — when filtering by date, you'll get a `cursor` field; loop until no cursor.
- **Talk-time ratio counts silence as zero** — a 30-min call with 5-min silence + 12 AE / 13 buyer is 41% AE, not 48%. Don't conflate "time spoken" with "share of voice".
- **Fathom's free tier records unlimited meetings** but the API is gated on Premium ($19/seat/mo). Check the user's plan before assuming `/external/v1/` access.
- **Fireflies GraphQL has aggressive rate limits** (300 req/hour on free, 600 on Pro). Cache transcript pulls.
- **tl;dv's webhook payload omits the transcript** — you get a meeting ID and must call `/meetings/<id>` to fetch.
- **Chorus has no API**. Anyone telling you otherwise is selling a scraper. Use the email-export workaround (Recipe 9) or migrate to Gong/Fathom.
- **Speaker-attribution can be wrong** when 2+ buyers are on a call (especially Zoom virtual backgrounds). Always verify by checking `speakerId` vs participant list before quoting in CRM.
- **Sensitive content**: transcripts may include PII / customer confidential data. Strip / redact before sending to external LLMs; prefer on-platform models (Gong Assist) for sensitive industries.
- **Latency on transcript availability**: Gong ~5-15 min post-call; Fathom ~3-5 min; Fireflies ~5-10 min; tl;dv ~5 min. Don't pull immediately on call-end webhook — schedule a 10-min delay.
- **Long calls (90+ min) chunked LLM extraction**: feeding a 90-min transcript (~25k tokens) into a small context window will lose info. Chunk to 5-min segments, extract per-chunk, merge MEDDIC fields with last-wins or quality-wins logic.

## Sources

- Gong API docs: https://app.gong.io/settings/api/documentation
- Gong calls/transcript reference: https://us-12345.api.gong.io/v2/calls/transcript (live; example schema)
- Fathom API: https://help.fathom.video/en/articles/8430832-fathom-api
- Fireflies API docs: https://docs.fireflies.ai/
- tl;dv API: https://docs.tldv.io/
- 2026 call intelligence comparison (Gong vs Fathom vs Fireflies vs tl;dv): https://www.gong.io/blog/best-ai-meeting-assistant/
- MEDDIC fill from call transcript pattern: https://www.gong.io/blog/meddic-from-call-data/
