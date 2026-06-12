<!--
Source: https://developer.aircall.io/api-references/ + Dialpad + Twilio
Aircall AI Assist (transcription endpoint): https://support.aircall.io/en-gb/articles/17784000797853
-->
# Voice Support — Aircall / Dialpad / Twilio — SKILL

Phone-call transcription → ticket creation → sentiment + summary → post-call recap email. Three options: Aircall (CRM-first), Dialpad (AI-first, transcription included), Twilio Programmable Voice + Whisper (self-hosted). Plus a post-call email recap pattern.

## When to use

- **Recipient handles phone support** — even rare voice calls benefit from ticketification.
- **Voice channel routing** — calls become Zendesk/Intercom tickets with channel=voice.
- **Sentiment + summary on phone tickets** — same pipeline as text tickets.
- **Post-call recap** — customer gets email with summary + next steps.
- **Outbound voice/SMS escalation** — Twilio for high-touch comms.

Trigger phrases: "phone ticket", "call transcription", "voice support", "Aircall call", "Dialpad transcript", "Twilio voice".

## Setup

```bash
# Aircall (AI Assist add-on required for transcription endpoint)
curl -sS "https://api.aircall.io/v1/calls" \
  -u "$AIRCALL_API_ID:$AIRCALL_API_TOKEN" | jq .

# Dialpad
curl -sS "https://dialpad.com/api/v2/calls" \
  -H "Authorization: Bearer $DIALPAD_TOKEN" | jq .

# Twilio
curl -sS "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Calls.json" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" | jq .
```

Auth + env:
- `AIRCALL_API_ID` + `AIRCALL_API_TOKEN` — at `Dashboard > Integrations & API > Create API Key`. Basic auth (`api_id:api_token`).
- `DIALPAD_TOKEN` — at `Settings > Authentication > Generate token`. AI features included on all Dialpad plans.
- `TWILIO_ACCOUNT_SID` + `TWILIO_AUTH_TOKEN` — at console.twilio.com.
- Aircall AI Assist add-on **required** for transcription endpoint (paid extra on top of standard plan).

Workspace prerequisites:
- Phone numbers configured.
- Webhook endpoints to receive `call.ended` events.
- ESP channel type `voice` configured in Zendesk / Intercom.

## Common recipes

### Recipe 1: Aircall — list recent calls

```bash
curl -sS "https://api.aircall.io/v1/calls?per_page=50&direction=inbound&status=done" \
  -u "$AIRCALL_API_ID:$AIRCALL_API_TOKEN" | jq '.calls[] | {id, started_at, duration, raw_digits, recording, transcription_id: .ai_assist_data.transcription_id}'
```

`.ai_assist_data.transcription_id` exists only with AI Assist add-on.

### Recipe 2: Aircall — fetch transcription (AI Assist required)

```bash
curl -sS "https://api.aircall.io/v1/calls/$CALL_ID/transcription" \
  -u "$AIRCALL_API_ID:$AIRCALL_API_TOKEN" | jq '{
    language,
    duration_seconds,
    speakers: .participants,
    segments: [.transcription.segments[] | {start, end, speaker, text}]
  }'
```

Returns time-segmented transcript with speaker diarization.

### Recipe 3: Aircall — real-time transcription (during call)

```bash
curl -sS "https://api.aircall.io/v1/calls/$CALL_ID/realtime_transcription" \
  -u "$AIRCALL_API_ID:$AIRCALL_API_TOKEN" | jq .
```

Use for live-coaching workflows. Available with AI Assist Pro tier.

### Recipe 4: Dialpad — fetch call recording + transcript

```bash
# Get call metadata
curl -sS "https://dialpad.com/api/v2/calls/$CALL_ID" \
  -H "Authorization: Bearer $DIALPAD_TOKEN" | jq '{id, direction, duration, started_at, recording_url, transcript_url}'

# Fetch transcript (Dialpad returns it as a structured doc)
curl -sS "$TRANSCRIPT_URL" \
  -H "Authorization: Bearer $DIALPAD_TOKEN" | jq '.'
```

Dialpad transcription / AI summary included in all plans (2026 pricing).

### Recipe 5: Dialpad — call summary

```bash
curl -sS "https://dialpad.com/api/v2/calls/$CALL_ID/summary" \
  -H "Authorization: Bearer $DIALPAD_TOKEN" | jq '{
    purpose: .summary.purpose,
    outcome: .summary.outcome,
    action_items: .summary.action_items,
    sentiment: .summary.sentiment
  }'
```

Dialpad auto-generates structured summary.

### Recipe 6: Twilio — transcribe via webhook

```bash
# Twilio call setup with transcription callback
curl -sS -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Calls.json" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
  -d "To=+15551234567" \
  -d "From=+15559876543" \
  -d "Url=https://yourapp.example.com/twiml/inbound" \
  -d "Record=true" \
  -d "RecordingStatusCallback=https://yourapp.example.com/webhooks/twilio/recording" \
  -d "Transcribe=true" \
  -d "TranscribeCallback=https://yourapp.example.com/webhooks/twilio/transcript"
```

Twilio's built-in transcription is basic; for higher accuracy, pipe recording to Whisper API (Recipe 11).

### Recipe 7: Push transcription as Intercom conversation

```bash
TRANSCRIPT=$(jq -r '.segments[] | "\(.speaker): \(.text)"' < transcript.json)
CALLER_EMAIL=$(jq -r '.caller_email' < call.json)
CALL_DURATION=$(jq -r '.duration_seconds' < call.json)

curl -sS -X POST "https://api.intercom.io/conversations" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" -H "Intercom-Version: 2.13" \
  -H "Content-Type: application/json" \
  -d "{
    \"from\":{\"type\":\"user\",\"email\":\"$CALLER_EMAIL\"},
    \"body\":\"<h3>Call from $CALLER_EMAIL (${CALL_DURATION}s)</h3><pre>$TRANSCRIPT</pre><p>Audio: <a href=\\\"$RECORDING_URL\\\">recording</a></p>\",
    \"custom_attributes\":{\"channel\":\"voice\",\"call_id\":\"$CALL_ID\"}
  }"
```

Sets `channel=voice` so reporting can segment by channel.

### Recipe 8: Push transcription as Zendesk ticket

```bash
curl -sS -X POST "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  -d "{
    \"ticket\":{
      \"subject\":\"Call from $CALLER ($CALL_DURATION sec)\",
      \"requester\":{\"name\":\"$CALLER_NAME\",\"email\":\"$CALLER_EMAIL\"},
      \"comment\":{
        \"body\":\"## Call transcript\\n\\n$TRANSCRIPT\\n\\n## Recording\\n$RECORDING_URL\",
        \"html_body\":\"...\",
        \"uploads\":[]
      },
      \"via\":{\"channel\":\"voice\"},
      \"tags\":[\"channel-voice\",\"auto-created\"]
    }
  }"
```

### Recipe 9: Score sentiment on transcript

Use the `sentiment-analysis-cohort-trends` skill. Transcripts work as well as text for Loris / Klaus / Claude scoring.

```bash
TRANSCRIPT_TEXT=$(jq -r '[.segments[].text] | join(" ")' < transcript.json)

curl -sS https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d "{\"model\":\"claude-sonnet-4-5-20250929\",\"max_tokens\":256,\"messages\":[{
    \"role\":\"user\",\"content\":\"Score 0-100. STRICT JSON: {\\\"score\\\":int, \\\"emotion\\\":string}. Transcript:\\n$TRANSCRIPT_TEXT\"
  }]}" | jq -r '.content[0].text' | jq .
```

### Recipe 10: Post-call recap email

```bash
SUMMARY=$(generate_summary "$TRANSCRIPT_TEXT")  # Claude or Dialpad summary
NEXT_STEPS=$(extract_action_items "$TRANSCRIPT_TEXT")

mcp tool gmail.send \
  --to "$CALLER_EMAIL" \
  --subject "Recap of our call today" \
  --body "$(cat <<EOF
Hi $CALLER_FIRST_NAME,

Thanks for the call. Quick recap:

**What we discussed:**
$SUMMARY

**Next steps:**
$NEXT_STEPS

**Ticket reference:** $TICKET_URL

Let me know if I missed anything.

— $AGENT_NAME
EOF
)"
```

### Recipe 11: Self-hosted Whisper (Twilio recording → transcript)

```bash
# When Twilio recording completes
RECORDING_URL="https://api.twilio.com/.../recording.wav"

# Download
curl -sS "$RECORDING_URL" -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" -o recording.wav

# Transcribe via OpenAI Whisper API
curl -sS -X POST "https://api.openai.com/v1/audio/transcriptions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@recording.wav" \
  -F model="whisper-1" \
  -F response_format="verbose_json" \
  -F language="en" | jq '{text, segments}'

# OR self-host with whisper.cpp
uvx --from openai-whisper whisper recording.wav --model small --output_format json
```

Whisper is highly accurate for English; for non-English, test against Dialpad/Aircall's native.

### Recipe 12: Outbound SMS escalation via Twilio

```bash
# When a critical-tier ticket has no response in 30min, SMS the on-call
curl -sS -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN" \
  -d "To=+15551234567" \
  -d "From=$TWILIO_FROM" \
  -d "Body=URGENT: Enterprise ticket INT-12345 unresponded for 30min. https://app.intercom.com/..."
```

Use sparingly — SMS pages should be rare and meaningful.

## Examples

### Example 1: Aircall inbound call → full pipeline

**Goal:** Customer calls; transcript becomes Intercom ticket within 5min of call end.

**Steps:**
1. Aircall webhook `call.ended` fires.
2. Wait 60s for transcription processing.
3. Recipe 2 — fetch transcription.
4. Recipe 7 — push as Intercom conversation.
5. Recipe 9 — score sentiment; tag conversation.
6. Recipe 10 — send recap email to customer.
7. If sentiment < 30: route to CSM via `multichannel-routing-rules` skill.

**Result:** Phone call becomes searchable, taggable, surveyable ticket.

### Example 2: Twilio + Whisper self-hosted

**Goal:** Avoid paying for Aircall AI Assist or Dialpad AI plans.

**Steps:**
1. Twilio call recording completes; webhook to your endpoint.
2. Recipe 11 — download + Whisper transcription.
3. Recipe 7 / 8 — push as ticket.
4. Recipe 9 — sentiment via Claude.
5. Recipe 10 — recap email.

**Result:** End-to-end voice → ticket workflow with $0 in vendor AI fees (Whisper API costs ~$0.006/min).

## Edge cases / gotchas

- **Aircall AI Assist is paid** — without it, you only get audio recordings, no transcription via API. The base Aircall plan doesn't include `transcription` endpoint.
- **Aircall vs Dialpad pricing** — Aircall: cheaper base but AI is extra. Dialpad: more expensive base, AI included. For high-volume voice, Dialpad cost-effective.
- **Transcription latency** — Aircall: 30-120s post-call. Dialpad: real-time available. Whisper: minutes (depends on length).
- **Speaker diarization quality** — Aircall / Dialpad good; Whisper requires post-processing with `pyannote.audio` for diarization.
- **Language detection** — Aircall supports 24 languages, AI Assist Pro plan. Dialpad similar. Whisper supports 90+; auto-detect available.
- **Audio file retention** — Aircall: 30d default. Dialpad: longer. Twilio: configurable. Download promptly if you need permanent storage.
- **Privacy / consent** — recording requires consent in many jurisdictions (US two-party states, EU GDPR). Use Aircall / Dialpad's built-in beep + consent intro.
- **Recap email subject is sensitive** — "Recap of our call" sounds like sales spam; tweak subject for inbound support context.
- **Caller email lookup** — phone-only callers won't have email; create as "anonymous" requester or prompt during call.
- **Twilio call routing TwiML** — programmable voice requires writing TwiML XML responses; non-trivial. Consider Twilio Flex / Aircall / Dialpad for managed.
- **Recording file format** — Aircall returns MP3, Dialpad WAV, Twilio WAV. Normalize for downstream processing.
- **Cost of Whisper API** — $0.006/min adds up; for 10k calls/mo × 10min = $600/mo. Self-hosting whisper.cpp on a small GPU instance is cheaper.

## Sources

- [Aircall API references](https://developer.aircall.io/api-references/)
- [Aircall — export call transcriptions via API](https://support.aircall.io/en-gb/articles/17784000797853)
- [Aircall AI Assist transcription](https://support.aircall.io/hc/en-gb/articles/10375545740701-How-to-use-Call-Transcription)
- [Dialpad API docs](https://developers.dialpad.com/)
- [Twilio Programmable Voice docs](https://www.twilio.com/docs/voice)
- [OpenAI Whisper API](https://platform.openai.com/docs/guides/speech-to-text)
- [Aircall vs Dialpad 2026 (Nextiva)](https://www.nextiva.com/blog/aircall-vs-dialpad.html)
