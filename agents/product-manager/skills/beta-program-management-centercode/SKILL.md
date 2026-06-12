<!--
Sources:
Centercode — https://www.centercode.com/api
PostHog feature flags — https://posthog.com/docs/feature-flags
-->
# Beta Program Management (Centercode + PostHog) — SKILL

Centercode is the enterprise-grade beta program platform (recruitment, NDA, structured feedback, bug tracking). For lightweight betas, PostHog feature flags + targeted segment + Slack feedback channel cover 80% of the need at $0. This pack picks between them and operates the program.

## When to use

- Running a managed beta program with NDA, tester onboarding, and structured feedback.
- Lightweight feature-flag betas with a targeted user segment.
- Pre-GA validation of a feature with 20-200 beta users.
- Closed-beta NDA programs for enterprise features.
- Gathering structured feedback (surveys, bug reports, usage telemetry).

Trigger phrases: "set up a beta", "beta program for feature X", "invite testers", "feature flag rollout", "limited release", "closed beta".

## Setup

### Lightweight default — PostHog feature flags

```bash
# PostHog MCP — covers feature flags + cohort targeting + analytics
mcp tool posthog.viewer
```

Auth:
- `POSTHOG_API_KEY` — see `amplitude-mixpanel-posthog-product-analytics` skill.

### Centercode (enterprise tier, paid)

```bash
curl -fsSL "https://api.centercode.com/v1/projects" \
  -H "Authorization: Bearer $CENTERCODE_API_KEY"
```

Auth:
- `CENTERCODE_API_KEY` — from Centercode account settings. Pricing: contact sales (enterprise contract).

## Common recipes

### Recipe 1: PostHog feature flag for a beta cohort

```bash
# 1. Create the flag
mcp tool posthog.create_feature_flag \
  --key "onboarding-revamp-beta" \
  --name "Onboarding Revamp — Beta" \
  --filters '{
    "groups":[
      {
        "properties":[
          {"key":"email","value":["beta1@x.com","beta2@x.com","beta3@x.com"],"operator":"exact"}
        ],
        "rollout_percentage":100
      },
      {
        "properties":[{"key":"plan","value":"pro","operator":"exact"}],
        "rollout_percentage":10
      }
    ]
  }'
```

### Recipe 2: PostHog graduated rollout

```bash
# Start at 10% → 25% → 50% → 100% over 4 weeks
for PCT in 10 25 50 100; do
  echo "Setting onboarding-revamp-beta to $PCT% — confirm? [y/N]"
  read CONFIRM
  if [ "$CONFIRM" = "y" ]; then
    mcp tool posthog.update_feature_flag \
      --key "onboarding-revamp-beta" \
      --filters "{\"groups\":[{\"rollout_percentage\":$PCT}]}"
    echo "Now at $PCT%; monitoring for 1 week."
    # Wait 7 days, check metrics, then bump
  fi
done
```

### Recipe 3: Beta cohort recruitment via email

```bash
# 1. Define the recruitment criteria
mcp tool posthog.query --query "
  SELECT email, distinct_id
  FROM persons
  WHERE properties.plan IN ('pro','enterprise')
    AND properties.activation_completed = true
    AND properties.opted_in_beta = true
  LIMIT 50
" > beta-candidates.json

# 2. Email invite
jq -r '.results[].email' beta-candidates.json | while read EMAIL; do
  mcp tool gmail.send --to "$EMAIL" \
    --subject "Invite: Early access to onboarding revamp" \
    --body "$(cat invite-template.md)"
  sleep 5
done

# 3. Add accepted testers to the feature flag (Recipe 1)
```

### Recipe 4: Slack feedback channel setup

```bash
# Create a private channel for beta testers + internal team
mcp tool slack.create_channel \
  --name "beta-onboarding-revamp" \
  --private true \
  --topic "Beta feedback for onboarding revamp. Post bugs/screenshots/ideas. PM owner: @you"

# Invite testers (after they accept beta)
mcp tool slack.invite_users \
  --channel "beta-onboarding-revamp" \
  --user_ids '["U123","U456","U789"]'
```

### Recipe 5: Centercode — create a beta project

```bash
curl -X POST "https://api.centercode.com/v1/projects" \
  -H "Authorization: Bearer $CENTERCODE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Onboarding Revamp Beta — Q3 2026",
    "description":"Closed beta for the 3-step guided onboarding",
    "nda_required":true,
    "tester_target":100,
    "duration_days":30
  }'
```

### Recipe 6: Centercode — invite testers from a recruitment campaign

```bash
curl -X POST "https://api.centercode.com/v1/projects/$PROJECT_ID/testers" \
  -H "Authorization: Bearer $CENTERCODE_API_KEY" \
  -d '{
    "invitations":[
      {"email":"beta1@x.com","first_name":"Sara","segment":"solo-founder"},
      {"email":"beta2@x.com","first_name":"James","segment":"team"}
    ]
  }'
```

### Recipe 7: Pull beta feedback (Centercode)

```bash
curl -fsSL "https://api.centercode.com/v1/projects/$PROJECT_ID/feedback" \
  -H "Authorization: Bearer $CENTERCODE_API_KEY" \
| jq '.feedback[] | {tester: .tester.email, category, severity, title, description}'
```

### Recipe 8: Lightweight feedback survey (Maze)

For PostHog-flagged betas, use Maze for structured surveys:

```bash
# Trigger a Maze survey to beta testers after 7 days of use
curl -X POST "https://api.maze.co/v1/surveys" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
  -d '{
    "name":"Onboarding Revamp Beta — 7-day check-in",
    "blocks":[
      {"type":"nps","question":"How likely are you to recommend the new onboarding to a peer?"},
      {"type":"open_text","question":"What works well?"},
      {"type":"open_text","question":"What is frustrating?"},
      {"type":"likert","question":"How easy was it to get to first value?","scale":7}
    ]
  }'
```

### Recipe 9: Beta exit criteria checklist

```markdown
# Beta Exit Criteria — Onboarding Revamp

Beta moves to GA when:

- [ ] ≥50 testers have completed the full flow
- [ ] D7 retention for beta cohort ≥ control + 3pp
- [ ] No P0 bugs open (Severity = Critical)
- [ ] ≤3 P1 bugs open (Severity = High)
- [ ] NPS from beta cohort ≥ 30
- [ ] Beta survey response rate ≥ 40%
- [ ] Eng sign-off on monitoring + kill-switch
- [ ] Support team trained on common edge cases
- [ ] Help docs published
- [ ] Marketing brief drafted (defer to marketing-agent)
```

### Recipe 10: Auto kill-switch on guardrail breach

```bash
# Cron daily: check beta cohort error rate; if >5x baseline, kill the flag
BASELINE=$(mcp tool posthog.query --query "SELECT avg(error_rate) FROM events WHERE timestamp >= now() - INTERVAL 14 DAY")
BETA=$(mcp tool posthog.query --query "
  SELECT avg(error_rate) FROM events
  WHERE timestamp >= now() - INTERVAL 1 DAY
    AND person.properties.\$feature/onboarding-revamp-beta = true
")

if [ $(echo "$BETA > $BASELINE * 5" | bc) = "1" ]; then
  mcp tool posthog.update_feature_flag --key "onboarding-revamp-beta" --filters '{"groups":[{"rollout_percentage":0}]}'
  mcp tool slack.post --channel "#product-leads" --text "🚨 Auto-killed beta — error rate $BETA vs baseline $BASELINE"
fi
```

## Examples

### Example 1: Lightweight closed beta (PostHog default)
**Goal:** Recruit 30 beta testers, ship safely to GA in 4 weeks.

**Steps:**
1. Create feature flag (Recipe 1) — start with explicit emails only.
2. Recruit via Recipe 3 (email invite to PostHog cohort).
3. Set up Slack feedback channel (Recipe 4).
4. After 1 week: send Maze survey (Recipe 8).
5. Run graduated rollout (Recipe 2): week 2 = 25%, week 3 = 50%, week 4 = 100%.
6. Verify exit criteria (Recipe 9) before final 100%.
7. Kill-switch (Recipe 10) running daily.

**Result:** 30-tester beta with safety nets and a path to GA.

### Example 2: Enterprise NDA beta (Centercode)
**Goal:** 100-tester managed beta with NDA, structured feedback.

**Steps:**
1. Create Centercode project (Recipe 5) — NDA required.
2. Recruit + invite (Recipe 6).
3. Centercode handles NDA signing, onboarding, tester portal.
4. Weekly: pull feedback (Recipe 7); triage in Linear with `beta-feedback` label.
5. Bi-weekly tester webinar (PMs can be hands-on at this tier).
6. Exit criteria (Recipe 9) + sign-off.

**Result:** Enterprise-grade managed beta with audit trail.

## Edge cases / gotchas

- **NDA enforcement** is Centercode's killer feature; PostHog can't gate access by NDA. If NDA matters → Centercode.
- **Tester selection bias.** Self-selected beta testers skew engaged; their metrics overstate GA outcomes. Adjust expectations.
- **Feature flag cleanup.** Old flags pile up; clean once a beta graduates (PostHog can flag stale ones).
- **Sample size for stats.** 30 testers is fine for qualitative; for statistically significant lift, need 1000+ (see `statsig-growthbook-experiments`).
- **Beta cohort identification.** PostHog injects `$feature/<flag-key>` as a person property — use it to segment in analytics.
- **Email deliverability.** Beta invite emails should come from a trusted domain; bulk Gmail risks spam folder. Limit to 100/day per sender.
- **Tester churn.** 30-40% of opted-in testers go silent; recruit 1.5x your target.
- **Compensation.** Beta testers expect SOMETHING — early access, swag, a credit, or a public thank-you. Plan it.
- **Communication cadence.** Beta needs a weekly check-in cadence; without it, feedback dries up by week 2.
- **GA cutoff.** Don't drag betas past 6 weeks; tester engagement decays. Either ship or pull.

## Sources

- [Centercode API docs](https://www.centercode.com/api)
- [Centercode beta best practices](https://www.centercode.com/blog)
- [PostHog feature flags](https://posthog.com/docs/feature-flags)
- [PostHog gradual rollout](https://posthog.com/docs/feature-flags/rollout-strategies)
- [Reforge — Beta program checklist](https://www.reforge.com/blog/closed-beta)
- [Statsig — Feature flag best practices](https://statsig.com/blog/feature-flag-best-practices)
- [Maze for beta surveys](https://maze.co)
