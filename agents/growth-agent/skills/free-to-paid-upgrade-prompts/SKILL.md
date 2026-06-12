<!--
Source: Pocus PQL guide + Stackmatix PLG funnel + Customer.io/Intercom event-trigger patterns
-->
# Free-to-Paid Upgrade Prompts SKILL

> PQL-triggered upgrade prompts at moments of value realization (usage limits, premium-feature interest, team-size growth), plus trial-end conversion flows. The most leveraged paid conversion lever in PLG.

## When to use

Trigger phrases:
- "Increase free-to-paid conversion"
- "Upgrade prompt design"
- "Trial-end conversion flow"
- "When should we show the upgrade modal?"
- "Trigger upgrade at usage limit"

Pair: `pql-product-qualified-leads-framework` (scoring upstream), `in-app-messaging-intercom-drift-pendo` (delivery), `behavioral-cohort-design` (audience), `price-experimentation-van-westendorp-conjoint` (price point).

## Setup

```bash
export POSTHOG_PERSONAL_API_KEY="phx_..."
export INTERCOM_TOKEN="dG9rOi..."
export CUSTOMERIO_API_KEY="cio_..."
export GROWTHBOOK_API_KEY="gb_..."
```

Required events:
- `Limit Approached` (with `usage_pct`, `limit_type`)
- `Premium Feature Attempted` (`feature_name`)
- `Team Member Invited` (PQL signal)
- `Subscription Started` (conversion outcome)

## PQL trigger taxonomy (when to show)

| Trigger | When to fire | Why effective | Conversion uplift typical |
|---|---|---|---|
| **Usage limit 80%+** | User approaching free cap | Value-realization apex | 5-15% trial-to-paid |
| **Premium feature attempted** | User clicks paywalled feature | Intent signal | 8-20% |
| **Team-size 3+** | Multi-user activity | Buyer ≠ user; champion identified | 10-25% (enterprise tier) |
| **Project / artifact threshold** | Magic-number-N hit | Habit formed | 5-12% |
| **Trial day 7 / day 12 / day 14** | Time-based pre-end | Urgency | 15-30% trial-end conv |
| **Frequency 7+ days/30** | Habit formed | Sticky user | 6-15% |
| **Integration connected** | Multi-tool commitment | High switching cost | 12-25% |

## Common recipes

### Recipe 1: PostHog cohort — "Approaching limit"

```sql
-- Define cohort
SELECT person_id
FROM events
WHERE event = 'Limit Approached'
  AND properties.usage_pct >= 80
  AND timestamp >= now() - INTERVAL 7 DAY
  AND person_id NOT IN (
    SELECT distinct_id FROM events
    WHERE event = 'Subscription Started'
  )
```

Persist to PostHog cohort + sync to Intercom / Customer.io via Hightouch (`reverse-etl-hightouch-census-growth`).

### Recipe 2: Intercom — show in-app upgrade modal

```bash
# Create message campaign triggered on tag
curl -X POST "https://api.intercom.io/messages" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -d '{
    "message_type": "inapp",
    "subject": "Ready to go unlimited?",
    "body": "<p>You hit 87% of your free workspace cap.</p><p>Pro gives you unlimited + advanced features. $39/mo.</p>",
    "template": "plain",
    "from": {"type": "admin", "id": "12345"},
    "to": {"type": "user", "user_id": "USER_ID"},
    "buttons": [
      {"text": "Upgrade to Pro", "url": "/pricing?utm_source=limit_approached"},
      {"text": "See plans", "url": "/pricing"}
    ]
  }'
```

### Recipe 3: Customer.io — event-triggered campaign

```bash
curl -X POST "https://api.customer.io/v1/campaigns" \
  -H "Authorization: Bearer $CUSTOMERIO_API_KEY" \
  -d '{
    "name": "Upgrade prompt - approaching limit",
    "trigger": {
      "type": "event",
      "event_name": "Limit Approached",
      "conditions": [{"property": "usage_pct", "operator": "gte", "value": 80}]
    },
    "actions": [
      {
        "type": "email",
        "delay_minutes": 0,
        "template": "tpl_upgrade_at_limit",
        "subject": "Your workspace is filling up"
      },
      {
        "type": "in_app",
        "delay_minutes": 1440,
        "template": "tpl_upgrade_modal"
      }
    ],
    "exit_criteria": ["Subscription Started", "Day 14"]
  }'
```

### Recipe 4: Trial-end conversion sequence (canonical 5-touch)

```text
Day -7 (mid-trial)      → Email: "Here's what you've achieved in 7 days"
                         (educational — shows value)

Day -3                  → Email + in-app modal: "Trial ends in 3 days"
                         (urgency starts)

Day 0 (trial end)       → Email: "Your trial ends today"
                         + in-app block to premium feature
                         (last-call)

Day +1                  → Email: "We lost you — here's 20% off"
                         (last-chance discount; some teams skip)

Day +7                  → Email: "Come back? Here's what's new"
                         (re-entry; merges with win-back)
```

### Recipe 5: A/B test trigger timing (when to fire)

```javascript
await growthbook.create_experiment({
  name: "upgrade-trigger-timing",
  hypothesis: "Showing upgrade modal at 70% usage converts higher than 90%",
  variants: [
    { name: "control_90pct", weight: 0.34 },
    { name: "treatment_80pct", weight: 0.33 },
    { name: "treatment_70pct", weight: 0.33 }
  ],
  primary_metric: "upgrade_conversion_rate",
  secondary_metrics: ["modal_dismissal_rate", "support_tickets_about_pricing"],
  guardrails: ["churn_rate_within_30d"],
  sample_size: 3000
});
```

### Recipe 6: Pricing copy A/B (anchor + value)

```text
Variant A (anchor):  "Upgrade to Pro for unlimited workspaces — $39/mo"
Variant B (value):   "Save 3 hours/week with Pro — $39/mo"
Variant C (compare): "Pro ($39/mo) vs Free: 3x faster, unlimited"
Variant D (loss aversion): "Don't lose your work — Pro keeps everything saved forever"
```

Loss-aversion typically wins for at-risk users; value typically wins for engaged.

### Recipe 7: Trial-end discount: when and how much

```text
Discount logic:
- New trials: no discount; 14-day trial standard
- Trial-end day 0-1: 10-20% off first 3 mo (common)
- Trial-end day 7+: discount fading; consider win-back at 30d
- Never repeat-discount same user (trains discount-only behavior)

Caution: heavy discounting trains the audience.
  Use only as last-ditch; track repeat-discount rate.
```

### Recipe 8: Behavioral progressive disclosure (best for PLG)

```text
Idea: don't show pricing until value is realized.

State machine:
  1. Free user, < 3 sessions:  no upgrade UI shown
  2. Free user, 3-10 sessions:  soft hint banner "Try Pro free for 7 days"
  3. Free user, hits limit:    inline modal with upgrade CTA
  4. Free user, hits premium feature attempt: paywall modal
  5. Free user, 30+ sessions:  email with case study + upgrade CTA
```

Configurable in Intercom via tags + Series.

### Recipe 9: Track upgrade attribution

```sql
SELECT
  properties.upgrade_source,  -- 'limit_approached' / 'feature_paywall' / 'pricing_page_direct'
  count() AS conversions,
  avg(properties.subscription_value) AS avg_arpu
FROM events
WHERE event = 'Subscription Started'
  AND timestamp >= now() - INTERVAL 30 DAY
GROUP BY properties.upgrade_source
ORDER BY conversions DESC
```

Top source = the trigger to amplify. Often: limit-approached + feature-paywall combined > all marketing-attributed conversions.

### Recipe 10: Frequency cap (avoid prompt fatigue)

```python
# Max 1 in-app upgrade modal per 7 days
# Max 1 upgrade email per 5 days
# Track dismissal: 3+ dismissals → cool-down for 14 days

def can_show_upgrade(user):
    if user.upgrade_dismissals_30d >= 3:
        return False
    if user.last_upgrade_prompt_at and (now() - user.last_upgrade_prompt_at).days < 7:
        return False
    return True
```

### Recipe 11: Friction-reduction — single-click upgrade

```text
1. Pre-auth payment via card-on-file from trial
2. One-click upgrade button in modal
3. Plan auto-selected based on usage profile
4. Confirmation: "You've upgraded! Pro features unlocked."

Result: 2-3x conversion vs "Click → checkout flow → form → confirm".
```

## Examples

### Example 1: B2B SaaS, trial-to-paid 8% (low)

Diagnose: 60% of trials never see pricing page; 70% don't get a single in-app prompt.

Plan:
1. Add usage-limit trigger (Recipe 1): cohort, sync to Intercom (Recipe 2).
2. Trial-end sequence (Recipe 4) via Customer.io.
3. Single-click upgrade button (Recipe 11).
4. A/B test discount value (no discount vs 15% off Recipe 7).

Expected: trial-to-paid 8% → 16-22% over 60 days.

### Example 2: Freemium app, upgrade rate 1.2%

Diagnose: limit set too high; users don't hit it for 60+ days; lose interest.

Plan:
1. Lower free limit (5 → 3 projects) for new signups (grandfather existing).
2. Earlier triggering at 70% usage instead of 90% (Recipe 5).
3. Progressive disclosure (Recipe 8).

Expected: upgrade rate 1.2% → 3-5%.

### Example 3: Multi-seat B2B

Trigger: 3+ team members active in 7 days.

Modal: "Your team is growing. Upgrade to Team plan ($79/mo) for shared workspaces + admin controls."

Bypass champion-as-buyer: alert account admin via email + in-app for buying decision.

Expected: team-upgrade rate of 8-15% among multi-seat orgs.

## Edge cases / gotchas

- **Trigger too early = churn before conversion** — showing upgrade modal day 1 trains "this is salesy". Earliest reasonable: post-activation event.
- **Trigger too late = forgot the user** — if user hits limit and you wait 7 days, they've started using a competitor.
- **Modal fatigue** — show too often → dismiss-rate climbs; eventual ad-blocker blocks. Frequency cap (Recipe 10).
- **Confusion about cause of conversion** — upgrade-source attribution must be exact; users hit pricing page from many entry points.
- **Discount cannibalization** — if you offer 20% off at trial-end, repeat trialers expect it. Limit per-user.
- **Charging the wrong person** — modal shown to user without buyer permission → friction. Bypass: alert account admin separately.
- **Trial-restart abuse** — block re-trial via email/IP/device fingerprint after one trial.
- **Pricing copy in modal ≠ pricing page** — if discount in modal differs from public pricing, users feel deceived; consistency matters.
- **Modal that blocks workflow** — never block users from work. Modals dismissable, never gated entirely. Soft paywalls only.
- **GDPR — usage-based triggers** — track-and-target requires consent; verify before deploying.
- **Mobile UX** — full-screen modals on small phones feel intrusive. Use bottom-sheet pattern.

## Sources

- Pocus — Definitive PQL guide: https://www.pocus.com/blog/the-definitive-pql-guide-part-1
- Stackmatix PLG funnel metrics: https://www.stackmatix.com/blog/plg-funnel-metrics
- Customer.io campaigns: https://customer.io/docs/journeys/campaigns/
- Intercom Series: https://www.intercom.com/help/en/articles/4001923-create-a-series
- Lenny's PLG Handbook (free-to-paid): https://plghandbook.com/
- Andrew Chen — PLG upgrade prompts: https://andrewchen.com/
- GrowthBook MCP (A/B): https://blog.growthbook.io/introducing-the-first-mcp-server-for-experimentation-and-feature-management/
