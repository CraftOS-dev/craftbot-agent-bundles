<!--
Source: Segment Tracking Plan docs + RudderStack OSS docs + genesys CDP alternatives + mParticle mobile-first
-->
# CDP Setup — Segment / RudderStack / mParticle SKILL

> Choose CDP, design event taxonomy (Object-Action past-tense), write tracking plan in Notion. Foundation for every downstream tool (analytics, lifecycle, attribution, reverse-ETL).

## When to use

Trigger phrases:
- "Set up our CDP"
- "Segment vs RudderStack"
- "Event taxonomy / tracking plan"
- "Naming convention for events"
- "Standardize our data layer"
- "Mobile + web unified tracking"

Pair: `reverse-etl-hightouch-census-growth` (downstream activation), `behavioral-cohort-design` (cohorts on top of events), `cli-anything` (CDP API for instrumentation).

## Setup

```bash
export SEGMENT_WRITE_KEY="<key>"
export RUDDERSTACK_WRITE_KEY="<key>"
export RUDDERSTACK_DATA_PLANE_URL="https://..."
export MPARTICLE_API_KEY="<key>"
export MPARTICLE_API_SECRET="<secret>"
export HIGHTOUCH_CDP_TOKEN="<token>"
export TEALIUM_TOKEN="<token>"
export NOTION_TOKEN="ntn_..."   # tracking plan host
```

## Platform decision matrix

| CDP | Cost (2026) | Best when | Integrations | Warehouse-native |
|---|---|---|---|---|
| **Segment** | $0-50K/yr (tiered) | Default, broad needs | 350+ | Via Reverse-ETL add-on |
| **RudderStack** | OSS free / $0-9K cloud | Cost-sensitive; warehouse-first | 200+ | Yes, native |
| **mParticle** | Custom enterprise | Mobile-first orgs | 350+ | Add-on |
| **Hightouch CDP** | Custom | Composable; warehouse-as-CDP | 150+ destinations | Yes, native |
| **Tealium** | Enterprise | 1,300+ integrations | 1,300+ | Yes |
| **Snowplow** (OSS) | OSS free / $0-20K | Custom schema; warehouse-first | Custom | Yes, native |

## Selection logic

```text
Q1: Already in warehouse-native modern stack?
   yes → RudderStack OSS / Hightouch CDP / Snowplow
   no  → Segment / mParticle / Tealium

Q2: Mobile-first?
   yes → mParticle (best mobile SDKs) / Segment
   no  → all viable

Q3: Cost sensitivity?
   bootstrapped → RudderStack OSS / Snowplow OSS
   mid           → Segment Team / Hightouch CDP
   enterprise   → Tealium / mParticle

Q4: Integration depth?
   broad → Tealium (1,300+) / Segment (350+)
   moderate → RudderStack / Hightouch
```

## Event taxonomy — the canonical rules

```text
1. Object-Action format (past-tense): "Subscription Started"
   - NOT: "subscribe" or "subscription" or "createSubscription"
2. Title-Case
3. No abbreviations
4. Same event name across platforms (web, iOS, Android, server)
5. Properties = noun:value pairs ("plan_tier": "Pro")
6. Standard properties on every event:
   - timestamp (auto)
   - user_id / anonymous_id (auto via Identify)
   - context (page URL, referrer, UTM, device)
   - revenue, currency (if commerce)
```

### Examples

```text
GOOD:
  "Account Created"       (props: signup_source, plan_tier)
  "Document Shared"       (props: document_id, share_method, recipient_count)
  "Subscription Started"  (props: plan, price, currency, billing_cycle)
  "Payment Failed"        (props: error_code, attempted_amount)

BAD:
  "page_view"             (snake_case + ambiguous)
  "user_signup"           (snake_case)
  "subscribed"            (no object)
  "Subscription"          (no action)
  "click_button"          (too generic; what button?)
```

## Common recipes

### Recipe 1: Segment Identify + Track (web JS)

```javascript
// Identify
analytics.identify("user_abc123", {
  email: "user@acme.com",
  first_name: "Jane",
  company: "Acme Corp",
  plan_tier: "Pro",
  created_at: "2026-01-15T10:00:00Z"
});

// Track
analytics.track("Document Shared", {
  document_id: "doc_456",
  share_method: "email",
  recipient_count: 3,
  workspace_id: "ws_789"
});

// Group (B2B)
analytics.group("acme_co_id", {
  name: "Acme Corp",
  industry: "SaaS",
  employees: 200,
  plan_tier: "Pro"
});
```

### Recipe 2: Segment server-side via curl

```bash
curl -X POST "https://api.segment.io/v1/track" \
  -u "$SEGMENT_WRITE_KEY:" \
  -d '{
    "userId": "user_abc123",
    "event": "Subscription Started",
    "properties": {
      "plan": "Pro",
      "price": 49,
      "currency": "USD",
      "billing_cycle": "monthly"
    },
    "context": {"ip": "1.2.3.4"}
  }'
```

### Recipe 3: RudderStack (drop-in Segment replacement)

```javascript
// Same JS API as Segment
rudderanalytics.identify("user_abc123", {email: "user@acme.com"});
rudderanalytics.track("Document Shared", {...});
```

```bash
curl -X POST "${RUDDERSTACK_DATA_PLANE_URL}/v1/track" \
  -u "$RUDDERSTACK_WRITE_KEY:" \
  -d '{"userId": "user_abc123", "event": "Subscription Started", "properties": {...}}'
```

### Recipe 4: mParticle mobile (iOS Swift)

```swift
import mParticle_Apple_SDK

// Init
MParticle.sharedInstance().start(withOptions: MParticleOptions(key: API_KEY, secret: API_SECRET))

// Identify
let request = MParticleUser.identifyRequest()
request.email = "user@acme.com"
MParticle.sharedInstance().identity.identify(request, completion: nil)

// Track
let event = MPEvent(name: "Document Shared", type: .other)
event.customAttributes = ["document_id": "doc_456", "share_method": "email"]
MParticle.sharedInstance().logEvent(event)
```

### Recipe 5: Tracking plan in Notion (the deliverable)

```markdown
# Event Tracking Plan — Acme Corp

| Event | Triggered When | Required Properties | Source(s) | Status | Owner |
|---|---|---|---|---|---|
| Account Created | After email verification | email, plan_tier, signup_source | web, mobile | Live | Eng + PM |
| Subscription Started | Stripe webhook on success | plan, price, currency, billing_cycle | server | Live | Eng |
| Document Created | On first save | document_id, type, workspace_id | web, mobile | Live | PM |
| Document Shared | On share button click | document_id, share_method, recipient_count | web | Live | PM |
| Limit Approached | Hourly cron check | limit_type, usage_pct | server | Beta | Eng |
| Activation Event Hit | When 3 docs created | n_docs | server | Live | PM |
```

### Recipe 6: Validation — Avo / Iteratively style

```python
# Add a schema-validator before sending to CDP
EVENT_SCHEMA = {
    "Document Shared": {
        "required": ["document_id", "share_method", "recipient_count"],
        "types": {
            "document_id": str,
            "share_method": str,
            "recipient_count": int
        }
    }
}

def track(event_name, props):
    schema = EVENT_SCHEMA.get(event_name)
    if not schema:
        raise ValueError(f"Unknown event: {event_name}")
    for req in schema["required"]:
        if req not in props:
            raise ValueError(f"Missing required prop: {req}")
        if not isinstance(props[req], schema["types"][req]):
            raise TypeError(f"Wrong type for {req}")
    # ... fire to CDP
```

### Recipe 7: Identity stitching (anonymous → identified)

```javascript
// Pre-signup (anonymous)
analytics.track("Pricing Page Viewed");  // tied to anonymous_id

// On signup
analytics.identify("user_abc123", {email});
// Segment automatically merges anonymous_id → user_id history

// Verify in PostHog / Amplitude: prior anon events now attributed to user_abc123
```

### Recipe 8: Destination routing

```text
Segment (or RudderStack) destination configuration:

Event "Subscription Started" → routes to:
  - PostHog (analytics)
  - Amplitude (analytics)
  - Stripe (already there)
  - Customer.io (lifecycle)
  - HubSpot (CRM)
  - Slack (#sales channel)

Event "Document Shared" → routes to:
  - PostHog
  - Mixpanel
  - Heap

Configure routing rules per event in Segment / RudderStack UI.
```

### Recipe 9: Audit + dedupe events

```sql
-- In warehouse, find dup events
SELECT
  event_name,
  user_id,
  timestamp,
  COUNT(*) AS occurrences
FROM cdp_events
WHERE created_at >= now() - INTERVAL 30 DAY
GROUP BY event_name, user_id, timestamp
HAVING COUNT(*) > 1
LIMIT 100
```

Common causes: client + server double-firing, retry on 5xx, browser back-button.

Fix: idempotency keys.

### Recipe 10: PII handling

```text
DO send to CDP:
  email (hashed for some destinations)
  user_id (internal)
  company name
  behavioral events
  device context

DON'T send to CDP:
  Full credit card number (PCI)
  SSN, government IDs
  Health info (HIPAA)
  Free-text comments (may contain PII)

Use Segment Privacy Controls or RudderStack PII transforms to redact in transit.
```

### Recipe 11: Mobile-app event timing

```text
Events fire even when offline → SDK buffers and sends on next online.

Order-of-arrival NOT guaranteed; events have client_timestamp + server_timestamp.

For activation/retention analysis, use client_timestamp (true event time).
For real-time triggers, use server_timestamp.
```

## Examples

### Example 1: B2B SaaS, no CDP yet, mid-budget

Decision: Segment Team tier ($0-50K/yr). Standard tooling, broad integrations, fastest setup.

Deliverables (Recipe 5):
- 30-event tracking plan in Notion
- Naming convention doc
- Validation schemas (Recipe 6)
- Destination map (Recipe 8): PostHog, Customer.io, HubSpot, Slack, warehouse

Timeline: 4-6 weeks engineering work.

### Example 2: Bootstrapped, warehouse-first, $0 budget

Decision: RudderStack OSS self-hosted + Postgres warehouse + PostHog.

Same tracking plan; runs on existing infra. No marginal CDP cost.

### Example 3: Mobile-first social app

Decision: mParticle (best mobile SDKs).

Plus: iOS + Android tracking plan, server-side fallback for ad-blocked events.

## Edge cases / gotchas

- **Renaming events post-launch is catastrophic** — every downstream tool (analytics, lifecycle, attribution) breaks. Plan naming carefully; rarely change.
- **Snake_case vs Title Case inconsistency** — mixing destroys analytics. Enforce via schema validator.
- **Property explosion** — adding new properties per event is fine, but watch for unbounded cardinality (e.g., URL as property).
- **PII in property values** — accidentally including email in `error_message`. Sanitize before send.
- **Anonymous → identified merge failure** — if user_id assigned late, prior anon events orphaned. Identify ASAP.
- **Server-side vs client-side duplicate firing** — purchase event from web client + Stripe webhook → 2x revenue. Use server-side as source of truth.
- **GDPR consent + tracking plan** — consent state must gate CDP firing in EU.
- **Mobile event order-of-arrival** — events arrive out of order; use client_timestamp for time-based analysis.
- **CDP outage = data loss** — buffer client-side, retry; server-side queue with persistent storage.
- **Versioning** — schema migrations breaks consumers; version events via property `_v: 2`.
- **Cost escalation** — CDPs charge by MTU (monthly tracked users). 1M MTU on Segment ~$50K+/yr; on RudderStack OSS = $0.
- **Reverse-ETL replaces some CDP destinations** — for warehouse-native, RudderStack + Hightouch may be simpler than full Segment.

## Sources

- Segment Tracking Plan docs: https://segment.com/docs/connections/spec/tracking-plan/
- Segment Spec — Identify/Track/Group: https://segment.com/docs/connections/spec/
- RudderStack docs (OSS): https://www.rudderstack.com/docs/
- mParticle docs: https://docs.mparticle.com/
- Hightouch CDP: https://hightouch.com/platform/customer-data-platform
- Tealium iQ: https://www.tealium.com/products/iq-tag-management/
- Snowplow (OSS): https://snowplow.io/
- Avo (tracking plan governance): https://avo.app/
- Iteratively (Amplitude-bought, similar role): https://amplitude.com/data
- Genesys — CDP alternatives 2026: https://genesysgrowth.com/blog/best-alternatives-for-twilio-segment
