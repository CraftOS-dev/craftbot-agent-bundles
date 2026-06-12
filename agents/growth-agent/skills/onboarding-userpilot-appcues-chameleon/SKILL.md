<!--
Source: Userpilot blog Appcues alternatives + Chameleon comparison + Pendo 2025 in-app guidance ranking
-->
# Onboarding Platform Choice + Checklist Spec SKILL

> Decision matrix for Userpilot / Appcues / Pendo / Chameleon / Whatfix; checklist+progress design spec; API recipes for each platform via cli-anything curl (no native MCPs as of June 2026).

## When to use

Trigger phrases:
- "Build onboarding flow"
- "Which onboarding tool should we use?"
- "Add a product tour"
- "Onboarding checklist design"
- "Replace our [Appcues / Pendo / Chameleon]"

Pair: `activation-funnel-aha-moment` (defines the target event), `time-to-value-ttv-optimization` (the success metric), `in-app-messaging-intercom-drift-pendo` (post-onboarding messaging).

## Setup

```bash
# No native MCPs — REST APIs via cli-anything
export USERPILOT_API_KEY="up_..."
export APPCUES_TOKEN="apc_..."
export PENDO_INTEGRATION_KEY="pdo_..."
export CHAMELEON_API_KEY="chmln_..."
export WHATFIX_API_KEY="wfx_..."
```

Required client-side: SDK install per platform (recipient owns).

## Platform decision matrix (June 2026)

| Tool | Web | Mobile | Analytics depth | Pricing (annual) | Best when |
|---|---|---|---|---|---|
| **Pendo** | ✓ | ✓ (iOS, Android, RN, Flutter SDKs) | Best-in-class (full product analytics + replay) | $15K-140K | You want unified analytics+guidance+replay; mid-large org |
| **Userpilot** | ✓ | ✓ (iOS, Android, RN, Flutter) | Funnels + cohorts built-in | $249/mo+ ($3K-30K/yr) | Mid-market mid-budget; want product analytics included |
| **Appcues** | ✓ | ✓ (iOS, Android — native mobile flows) | Basic — pair with Amplitude/Mixpanel | $299/mo+ ($3.6K-50K/yr) | Mobile-native focus; iOS+Android-first |
| **Chameleon** | ✓ | ✗ web-only | External (Amplitude / Mixpanel / Segment) | Custom ($10K+) | Pixel-perfect CSS web; dev/design-friendly |
| **Whatfix** | ✓ | ✓ | Enterprise DAP analytics | Enterprise ($30K+) | Internal apps; enterprise change-management |
| **Userflow** | ✓ | ✗ | Basic | $200/mo+ | Dev-friendly setup; React-component-style flows |
| **Stonly** | ✓ | ✓ | Decision-tree guides | $99/mo+ | Self-serve knowledge base + guides |

Mobile note: Appcues + Pendo are the only "native mobile-first" choices. Web-only orgs can ignore mobile column.

## Selection logic (3-question decision)

```text
Q1: Web only, web + mobile, or mobile-first?
   web-only        → Chameleon / Userflow / Userpilot / Pendo Web
   web + mobile    → Pendo / Userpilot / Appcues
   mobile-first   → Appcues (best mobile UX) / Pendo

Q2: Want product analytics included or pair with PostHog/Amp/Mixpanel?
   included        → Pendo (best) / Userpilot (mid)
   pair w/ external → Chameleon / Userflow / Appcues

Q3: Budget tier?
   < $5K/yr       → Userflow / Stonly / Userpilot Starter
   $5-25K/yr      → Userpilot / Appcues
   $25K+          → Pendo / Whatfix
```

## Onboarding checklist spec (the deliverable)

Every platform supports checklist + progress widget. Below is the canonical spec.

```yaml
checklist:
  name: "Get to first value in 5 steps"
  target_audience: "Newly signed-up users (Day 0-7)"
  target_metric: "Activation event (e.g., First Document Shared)"
  position: "Bottom-right floating widget (web) / Home tab (mobile)"
  visibility: "Until completed OR dismissed 3 times"
  steps:
    - id: "verify_email"
      title: "Verify your email"
      cta: "Resend verification"
      completion_event: "Email Verified"
      estimated_time_seconds: 60
      hint: "Check spam if you don't see it within 2 min."
    - id: "complete_profile"
      title: "Add your name and role"
      cta: "Open settings"
      completion_event: "Profile Updated"
      estimated_time_seconds: 90
    - id: "create_workspace"
      title: "Create your first workspace"
      cta: "Create workspace"
      completion_event: "Workspace Created"
      estimated_time_seconds: 120
      hint: "Use a template to start fast."
    - id: "invite_teammate"
      title: "Invite a teammate (optional but recommended)"
      cta: "Send invite"
      completion_event: "Invite Sent"
      estimated_time_seconds: 30
      optional: true
    - id: "first_value_action"
      title: "Share your first document"
      cta: "Share now"
      completion_event: "Document Shared"
      estimated_time_seconds: 60
      celebration: "You're activated! Confetti."
  
  metrics_to_track:
    - per_step_completion_rate
    - dropoff_step (which step has highest abandonment)
    - time_to_full_completion (p25, p50, p75)
    - activation_lift (treatment vs no-checklist control)
```

## Common recipes

### Recipe 1: Userpilot — create checklist via API

```bash
curl -X POST "https://api.userpilot.io/v1/checklists" \
  -H "Authorization: Bearer $USERPILOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Get to first value",
    "audience": {"segment_id": "newly_signed_up"},
    "tasks": [
      {"label": "Verify email", "completion_event": "email_verified"},
      {"label": "Create workspace", "completion_event": "workspace_created"},
      {"label": "Share first document", "completion_event": "document_shared"}
    ],
    "visibility": "until_completed",
    "position": "bottom_right"
  }'
```

### Recipe 2: Appcues — create flow

```bash
curl -X POST "https://api.appcues.com/v2/accounts/$APPCUES_ACCOUNT_ID/flows" \
  -H "Authorization: Bearer $APPCUES_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Onboarding tour",
    "steps": [
      {"type": "tooltip", "target": "#dashboard-nav",
       "title": "Your home base", "content": "All your projects live here."},
      {"type": "modal", "title": "Create your first project",
       "cta": {"text": "Create project", "action": "navigate", "url": "/new"}}
    ],
    "trigger": {"type": "first_login"}
  }'
```

### Recipe 3: Pendo — create guide

```bash
curl -X POST "https://app.pendo.io/api/v1/guide" \
  -H "x-pendo-integration-key: $PENDO_INTEGRATION_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Onboarding tour",
    "audience": {"id": "newly_signed_up_segment"},
    "steps": [
      {"location": "selector:#main-nav",
       "content": "<h2>Welcome</h2><p>Start with the dashboard.</p>"}
    ],
    "isPublished": true
  }'
```

### Recipe 4: Chameleon — create tour

```bash
curl -X POST "https://api.chameleon.io/v1/tours" \
  -H "X-Account-Token: $CHAMELEON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "First-time tour",
    "trigger": "after_signup",
    "steps": [
      {"selector": "#sidebar", "text": "Sidebar overview", "position": "right"}
    ]
  }'
```

### Recipe 5: Branched onboarding (multi-persona)

When users self-identify role in signup ("designer / engineer / PM"), branch:

```text
if role == 'designer':    show tour focused on design library
if role == 'engineer':    show API quickstart
if role == 'pm':          show roadmap template
```

In Userpilot: create role-specific segments + role-specific checklists. In Pendo: use page rules + segments.

### Recipe 6: Compute checklist effectiveness (PostHog)

```sql
SELECT
  variant,
  count() AS users,
  countIf(activated) * 100.0 / count() AS activation_rate_pct,
  avg(ttv_min) AS avg_ttv_min
FROM cohort_with_checklist_treatment
GROUP BY variant
```

Treatment lift = treatment_activation - control_activation. MDE typically 3-5pp for checklist tests.

### Recipe 7: Self-host alternative (zero vendor cost)

For PLG teams who want zero vendor cost, build in-house with feature flags:
```javascript
// Pseudocode using GrowthBook + own UI
const onboardingState = useUser().onboarding;
if (!onboardingState.email_verified) showStep('verify');
else if (!onboardingState.workspace_created) showStep('workspace');
// ...
```

Pros: no vendor, no $$. Cons: engineering cost, no analytics built-in.

### Recipe 8: Identify checklist abandonment step (key insight)

```sql
WITH steps AS (
  SELECT 'verify' AS step UNION ALL SELECT 'workspace' UNION ALL SELECT 'invite' UNION ALL SELECT 'share'
)
SELECT
  s.step,
  countDistinctIf(person_id, started) AS started,
  countDistinctIf(person_id, completed) AS completed,
  completed * 100.0 / started AS step_completion_pct
FROM steps s
JOIN cohort_with_step_progress c ON 1=1
GROUP BY s.step
ORDER BY step_completion_pct ASC
```

Lowest step_completion_pct = the friction point. Redesign that step.

## Examples

### Example 1: Web-only B2B SaaS, $8K/yr budget

Decision: Userpilot (mid-market + budget fit, included analytics).

Deliverable: 5-step checklist (above spec), branched by ICP segment (marketing / sales / ops roles).

Success metric: activation_rate from 28% → 45% in Q3.

### Example 2: Mobile-first consumer app

Decision: Appcues (native iOS/Android flows).

Deliverable: 3-step tap-through tour on Day 0; 5-message in-app message series Day 1-7.

Success metric: D7 retention from 22% → 30%.

### Example 3: Enterprise internal tool

Decision: Whatfix (enterprise DAP for internal apps).

Deliverable: contextual help overlays + decision-tree guides.

Success metric: support tickets -40% in 90 days.

## Edge cases / gotchas

- **Onboarding overload kills activation** — long tours with 8+ steps train users to dismiss. Stick to ≤ 5 steps; allow skip.
- **CTA-clicked ≠ completed** — track downstream completion event, not just CTA click. Users click "Create workspace" but bail before saving.
- **Mobile flow chrome differs by OS** — Appcues / Pendo SDKs cover iOS + Android; test on both. Native modal patterns differ.
- **Dismissal once vs dismissed-3-times** — config matters; one-dismiss kills repeat-engagement; persistent widget annoys.
- **A/B test bias from selection** — newly-signed-up cohort may differ across treatment vs control if randomization happens post-signup. Randomize at user creation.
- **Vendor lock-in via tour content** — moving from Userpilot to Appcues = rewrite all tours. Keep YAML spec source-of-truth.
- **Cost escalates with MAU** — pricing tiers usually based on MAU. Pendo at 100K MAU can hit $80K+/yr.
- **Analytics duplication** — Pendo + PostHog = two product-analytics sources; reconcile or choose one as source of truth.
- **Mobile SDK update cycle** — Apple/Google app store updates require SDK refreshes; budget for it.
- **GDPR cookie consent** — onboarding tools store identifier cookies; check consent banner integration.

## Sources

- Userpilot — Appcues alternatives 2025: https://userpilot.com/blog/appcues-alternatives/
- Chameleon — Userpilot alternatives: https://www.chameleon.io/alternative/userpilot-alternatives
- Pendo — Top 8 in-app guidance tools 2025: https://www.pendo.io/pendo-blog/the-top-8-in-app-guidance-tools-in-2025/
- Appcues — PLG metrics: https://www.appcues.com/blog/product-led-growth-metrics
- Whatfix — DAP enterprise: https://whatfix.com/
- Userflow — React-component style: https://userflow.com/
- Stackmatix PLG onboarding: https://www.stackmatix.com/blog/plg-onboarding-activation
