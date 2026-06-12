---
name: document-analytics-time-to-sign
description: Track document funnel analytics — sent → opened → viewed → signed — via native dashboards (PandaDoc, Proposify, Qwilr, DocuSign Insights), DocuSign Connect webhooks → PostHog / Mixpanel / Amplitude, custom dashboards. Track view-time per section, drop-off, time-to-sign, conversion rate. Use when the user says "time to sign", "drop-off", "completion rate", "proposal analytics", "DocuSign Insights", "PandaDoc analytics", "PostHog / Mixpanel / Amplitude integration".
---

# Document analytics — Time-to-sign / view / drop-off / conversion

This skill ships the metrics + observability layer on doc + e-sign flows. Use native dashboards for quick wins; pipe webhook events to product-analytics for deep funnels.

## When to use

User says:

- "How long does it take buyers to sign?"
- "Where do they drop off in the proposal?"
- "DocuSign analytics / Connect webhook"
- "PandaDoc / Proposify / Qwilr analytics"
- "PostHog / Mixpanel / Amplitude for documents"
- "Funnel: sent → opened → signed"
- "Section-by-section view-time"
- "Why are deals stuck at proposal stage?"

Companion skills:
- `proposal-automation-pandadoc-proposify-qwilr` — source of view events.
- `e-signature-docusign-adobe-sign-pandadoc` — source of sign events.
- `document-workflow-routing-approval` — internal approval funnel.
- `audit-trail-e-sign-versioning` — event-stream archival.

## Setup

```bash
# DocuSign Connect (webhook config in DocuSign Admin UI)
# https://developers.docusign.com/platform/webhooks/connect/

# PandaDoc webhooks (Settings → Webhooks)
# https://developers.pandadoc.com/reference/webhooks

# Proposify webhooks (Account → Integrations)
# Qwilr webhooks (Settings → Integrations)

# Product-analytics MCPs (all available)
# posthog-mcp, mixpanel-mcp, amplitude-mcp

# Standalone SDKs
pip install posthog mixpanel-python amplitude-analytics

# Custom dashboard
pip install dash plotly streamlit pandas
# or BI tools: Looker / Metabase / Cube
```

## Common recipes

### Recipe 1: Standard event taxonomy

```python
EVENTS = {
    "doc_created":      "Doc generated in PandaDoc / DocuSign / etc.",
    "doc_sent":         "Sent to recipient",
    "doc_first_opened": "Recipient first opened",
    "doc_section_viewed": "Recipient viewed section (per-section heatmap)",
    "doc_section_time": "Section view duration",
    "doc_commented":    "Recipient added comment",
    "doc_question":     "Recipient asked clarifying question",
    "doc_signed":       "Signature event",
    "doc_completed":    "All signers done",
    "doc_declined":     "Recipient declined",
    "doc_expired":      "TTL passed without action",
}
PROPERTIES = ["envelope_id","doc_id","template_id","template_version",
              "deal_id","deal_value","counterparty","party_role","sender_email","recipient_email",
              "time_to_first_open_s","time_to_sign_s","sections_viewed_count","sections_total"]
```

Standardize across PandaDoc / DocuSign / Proposify to enable cross-platform funnel.

### Recipe 2: DocuSign Connect — webhook config

In DocuSign Admin → Connect → Add Configuration:
- URL: `https://your-app/webhooks/docusign`
- Format: JSON
- Events: Sent / Delivered / Completed / Declined / Voided
- HMAC signing: ON; copy the key into env `DOCUSIGN_CONNECT_KEY`

```python
# Receiver
@app.post("/webhooks/docusign")
async def docusign_connect(req: Request):
    body = await req.body()
    # Verify signature
    sig = req.headers.get("X-DocuSign-Signature-1")
    if not verify_hmac(body, sig, os.environ["DOCUSIGN_CONNECT_KEY"]):
        return Response(status_code=401)
    payload = await req.json()
    env_data = payload["data"]
    event_name = {
        "envelope-sent":"doc_sent",
        "envelope-delivered":"doc_first_opened",   # DocuSign "delivered" = recipient opened
        "envelope-completed":"doc_completed",
        "envelope-declined":"doc_declined",
        "envelope-voided":"doc_expired"
    }.get(payload["event"])
    if event_name:
        track(event_name, {
            "envelope_id": env_data["envelopeId"],
            "recipient_email": env_data["recipients"][0]["email"],
            "timestamp": env_data["statusChangedDateTime"],
        })
    return {"ok": True}
```

### Recipe 3: PandaDoc — webhook config

```bash
curl -X POST https://api.pandadoc.com/public/v1/webhooks \
  -H "Authorization: API-Key $PANDADOC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "PostHog Funnel",
    "url": "https://your-app/webhooks/pandadoc",
    "shared_key": "shared_secret",
    "events": [
      "document_state_changed",
      "document_updated",
      "recipient_completed"
    ]
  }'
```

Verify `X-Pandadoc-Signature` HMAC on inbound.

### Recipe 4: PostHog — capture event

```python
from posthog import Posthog
posthog = Posthog(project_api_key=POSTHOG_KEY, host="https://us.i.posthog.com")
posthog.capture(
    distinct_id=recipient_email,
    event="doc_first_opened",
    properties={
        "envelope_id": "env_abc123",
        "deal_value": 240000,
        "template_id": "msa-v3.1",
        "party_role": "customer",
    },
    timestamp=event_ts
)
```

### Recipe 5: Mixpanel — capture event

```python
from mixpanel import Mixpanel
mp = Mixpanel(MIXPANEL_TOKEN)
mp.track(
    distinct_id=recipient_email,
    event_name="doc_signed",
    properties={
        "$insert_id": f"sign-{envelope_id}",   # idempotent
        "envelope_id": envelope_id,
        "time_to_sign_hours": elapsed_h,
    }
)
```

### Recipe 6: Amplitude — capture event

```python
from amplitude import Amplitude, BaseEvent
amp = Amplitude(AMPLITUDE_API_KEY)
amp.track(BaseEvent(
    event_type="doc_signed",
    user_id=recipient_email,
    event_properties={"envelope_id": envelope_id, "deal_value": 240000},
    time=int(event_ts * 1000)
))
```

### Recipe 7: Compute time-to-sign

```python
import pandas as pd
events = pd.read_csv("doc_events.csv")    # via Recipe 4-6 ingestion → BI
pivot = events.pivot_table(
    index="envelope_id",
    columns="event",
    values="timestamp",
    aggfunc="min"
)
pivot["time_to_first_open_h"] = (pivot["doc_first_opened"] - pivot["doc_sent"]).dt.total_seconds() / 3600
pivot["time_to_sign_h"] = (pivot["doc_signed"] - pivot["doc_sent"]).dt.total_seconds() / 3600
print(pivot[["time_to_first_open_h","time_to_sign_h"]].describe())
```

### Recipe 8: Funnel chart — sent → opened → signed

```python
import plotly.graph_objects as go
sent = len(events[events.event=="doc_sent"])
opened = len(events[events.event=="doc_first_opened"])
signed = len(events[events.event=="doc_signed"])
fig = go.Figure(go.Funnel(
    y=["Sent","Opened","Signed"],
    x=[sent, opened, signed],
    textinfo="value+percent initial"
))
fig.write_html("funnel.html")
```

### Recipe 9: Per-section view-time heatmap (PandaDoc)

```python
# PandaDoc webhook includes recipient activity with per-section time
@app.post("/webhooks/pandadoc")
async def pandadoc_webhook(req: Request):
    body = await req.json()
    if body["event"] == "recipient_completed":
        # Pull doc analytics from PandaDoc API
        analytics = requests.get(
            f"https://api.pandadoc.com/public/v1/documents/{body['data']['id']}/details",
            headers={"Authorization": f"API-Key {PANDADOC_KEY}"}
        ).json()
        # Section timings (if your template uses named sections)
        for section in analytics.get("sections", []):
            posthog.capture(
                distinct_id=body["data"]["recipient_email"],
                event="doc_section_time",
                properties={
                    "section_name": section["name"],
                    "time_spent_s": section["time_spent"],
                    "envelope_id": body["data"]["id"]
                }
            )
```

### Recipe 10: Drop-off detection

```python
# Drop-off = opened but not signed within X hours
import pandas as pd
threshold_h = 72
opened_only = pivot[(pivot["doc_first_opened"].notna()) & (pivot["doc_signed"].isna())]
opened_only["hours_since_open"] = (pd.Timestamp.utcnow() - opened_only["doc_first_opened"]).dt.total_seconds() / 3600
dropoffs = opened_only[opened_only["hours_since_open"] > threshold_h]
print(f"Drop-offs: {len(dropoffs)}")
# Auto-nudge via Slack
for env_id in dropoffs.index:
    slack_post(f"📉 Drop-off alert: {env_id} stuck >72h after open. Suggest follow-up.")
```

### Recipe 11: A/B test template versions

```python
# Random assign template at send time
import random
template_uuid = random.choice(["tmpl_v3.1_concise", "tmpl_v3.1_detailed"])
pdoc = create_pandadoc(template_uuid=template_uuid, ...)
posthog.capture(
    distinct_id=recipient_email,
    event="doc_template_assigned",
    properties={"envelope_id": env_id, "template_variant": template_uuid}
)
# Compare signed % per variant in PostHog funnel
```

### Recipe 12: Cohort metrics — by deal size

```python
events["deal_bucket"] = pd.cut(events.deal_value, bins=[0, 25000, 100000, 500000, float("inf")],
                                labels=["<25K","25-100K","100-500K","500K+"])
cohort = events.groupby(["deal_bucket","event"]).size().unstack(fill_value=0)
cohort["close_rate"] = cohort.get("doc_signed", 0) / cohort.get("doc_sent", 1)
print(cohort[["doc_sent","doc_signed","close_rate"]])
```

### Recipe 13: Streamlit dashboard skeleton

```python
import streamlit as st, pandas as pd
events = pd.read_parquet("events.parquet")
st.title("Document Analytics")
col1, col2, col3 = st.columns(3)
col1.metric("Sent (30d)", len(events[events.event=="doc_sent"]))
col2.metric("Signed (30d)", len(events[events.event=="doc_signed"]))
col3.metric("Median time-to-sign (h)", events.median_tts_h.median())
st.subheader("Funnel")
st.plotly_chart(make_funnel_chart(events))
st.subheader("Drop-offs (open > 72h, no sign)")
st.dataframe(get_dropoffs(events))
```

## Examples

### Example 1: AE dashboard — time-to-sign per rep

**Goal:** Show each AE their median time-to-sign + drop-off rate.
**Steps:**
1. Recipe 2-6 — pipe events to PostHog with `sender_email` property.
2. Recipe 7 — compute TTS per AE.
3. Recipe 12 — cohort by AE.
4. Recipe 13 — Streamlit dash.

**Result:** Reps see their own funnel; sales leader sees team's.

### Example 2: Auto-nudge stalled deals

**Goal:** Reduce drop-offs by auto-nudging buyers stuck >48h after open.
**Steps:**
1. Recipe 10 — drop-off detection cron.
2. `slack-mcp` alerts AE.
3. AE one-click sends nudge via PandaDoc resend.

**Result:** Close-rate uplift via faster nudges.

### Example 3: A/B test "concise" vs "detailed" proposal

**Goal:** Find which template wins.
**Steps:**
1. Recipe 11 — random template at send.
2. Recipe 8 — funnel per variant.
3. After 50 sends per arm, report.

**Result:** Data-driven template iteration.

## Edge cases / gotchas

- **DocuSign "Delivered" ≠ "Opened".** Delivered = recipient received envelope; opened = recipient viewed. Some Connect configs conflate.
- **Recipient masquerade.** If sender opens for the recipient (e.g., legal team reviewing), it counts as opened — false positive. Tag internal IPs.
- **Multi-signer envelopes.** "Signed" = which signer? Track per-signer; aggregate to envelope completion.
- **Time-zone drift.** All timestamps to UTC. Convert at display time only.
- **PostHog batching.** Default batches up to 100; high-volume needs async client.
- **Mixpanel `$insert_id`.** Use to dedupe re-delivered webhooks.
- **Sample bias.** A/B should be random; not selected by template defaults.
- **GDPR + analytics.** Recipient email is PII; hash before sending to product-analytics if not consented.
- **DocuSign Insights tier.** Native dashboards require Premier / Enterprise tier.
- **PandaDoc Analytics access.** Available on Essentials+; deep heatmaps on Business+.
- **Webhook delivery delay.** DocuSign Connect can lag 1-10 min; don't expect real-time.
- **Webhook idempotency.** Retries on 5xx; key by (envelope_id, event, timestamp).
- **Section names must match template.** If template renames a section between versions, analytics history breaks.
- **Cohort cardinality.** Buckets like "deal_value" should be discrete; raw values explode dashboards.
- **Funnel definitions.** PostHog / Mixpanel / Amplitude each define funnels slightly differently — confirm UTC + order.
- **Survival analysis.** Time-to-sign is right-censored; consider survival (Kaplan-Meier) for accurate medians when some never sign.

## Sources

- [DocuSign Connect docs](https://developers.docusign.com/platform/webhooks/connect/) — webhook config.
- [DocuSign Insights](https://www.docusign.com/products/insight) — native analytics product.
- [PandaDoc Webhooks](https://developers.pandadoc.com/reference/webhooks) — events + payload.
- [PandaDoc Analytics](https://support.pandadoc.com/hc/en-us/articles/360011434073-Document-tracking-and-analytics) — native dashboards.
- [Proposify Webhooks](https://support.proposify.com/en/articles/4533537-webhooks) — events.
- [Qwilr Analytics](https://qwilr.com/features/analytics/) — native dashboards.
- [PostHog Python SDK](https://posthog.com/docs/libraries/python) — capture API.
- [Mixpanel Python](https://developer.mixpanel.com/docs/python) — capture API.
- [Amplitude Python SDK](https://www.docs.developers.amplitude.com/data/sdks/python/) — track API.
- [Streamlit](https://docs.streamlit.io/) — dashboard framework.
- [Plotly funnel charts](https://plotly.com/python/funnel-charts/) — funnel viz.
- Sister skills: `proposal-automation-pandadoc-proposify-qwilr`, `e-signature-docusign-adobe-sign-pandadoc`, `document-workflow-routing-approval`, `audit-trail-e-sign-versioning`.
