<!--
Source: https://openfeature.dev/ · https://docs.launchdarkly.com/ · https://docs.statsig.com/ · https://docs.getunleash.io/
Authored: June 2026 for the devops-engineer agent bundle.
-->

# Feature Flags (OpenFeature + LaunchDarkly / Statsig / Unleash / Flagsmith)

Decouple deploy from release. **OpenFeature** (CNCF, vendor-neutral SDK) as
the application layer + backend of choice: **LaunchDarkly** (enterprise),
**Statsig** (modern, generous free tier), **Unleash** (OSS, self-host),
**Flagsmith** (OSS), **GrowthBook** (OSS + paid). Ship dark, enable by
cohort, monitor SLI, expand. Tie flag changes to incident.io for auto-rollback.

## When to use

- "We want to ship this without enabling it for everyone."
- A/B test or experimentation framework.
- Kill switches for risky code paths.
- Trunk-based development — ship to main constantly, gate via flags.
- Operational toggles ("turn off the slow feature during incident").

Skip when: configuration that almost never changes (use ConfigMap);
secrets (use Vault); team is 1-2 people on a side project.

## Setup

```bash
# OpenFeature SDKs
uv add openfeature-sdk                          # Python
npm install @openfeature/server-sdk             # Node
go get github.com/open-feature/go-sdk           # Go

# Provider SDKs (pick one)
uv add openfeature-launchdarkly-provider
uv add openfeature-statsig-provider
uv add openfeature-unleash-provider

# Backend CLIs
brew install launchdarkly/tap/ldcli              # LaunchDarkly
npm install -g statsig-cli                       # Statsig
brew install unleash/unleash/unleash-cli         # Unleash
```

API keys:
- LaunchDarkly: SDK key per env (server-side) + REST API key for ops.
- Statsig: Server secret key + Console API key.
- Unleash (self-hosted): generate API token in admin UI.
- Flagsmith: Environment key.

## Common recipes

### Recipe 1 — OpenFeature Python with LaunchDarkly

```python
from openfeature import api
from openfeature.contrib.provider.launchdarkly import LaunchDarklyProvider
import launchdarkly_server_sdk as ld

ld_client = ld.LDClient(config=ld.Config(sdk_key=os.environ["LD_SDK_KEY"]))
api.set_provider(LaunchDarklyProvider(ld_client))

client = api.get_client()

# Evaluate
show_new_checkout = client.get_boolean_value(
    flag_key="new-checkout-flow",
    default_value=False,
    evaluation_context={
        "targetingKey": user_id,
        "plan": user.plan,
        "country": user.country,
    },
)
```

The flag evaluation context drives the targeting rules in the backend UI.

### Recipe 2 — OpenFeature TypeScript with Statsig

```typescript
import { OpenFeature } from "@openfeature/server-sdk";
import { StatsigProvider } from "@openfeature/statsig-provider";

OpenFeature.setProvider(new StatsigProvider({
  sdkKey: process.env.STATSIG_SECRET!,
  options: { environment: { tier: process.env.NODE_ENV } },
}));

const client = OpenFeature.getClient();

const showNewCheckout = await client.getBooleanValue(
  "new-checkout-flow",
  false,
  { targetingKey: userId, plan: user.plan, country: user.country }
);
```

### Recipe 3 — LaunchDarkly REST API (declarative flag changes)

```bash
# Toggle a flag via API
curl -X PATCH "https://app.launchdarkly.com/api/v2/flags/my-project/new-checkout-flow" \
  -H "Authorization: $LD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '[{ "op": "replace", "path": "/environments/production/on", "value": true }]'

# Bulk export
ldcli flags list --project my-project --output json > flags.json
ldcli flags import --project my-project --file flags-updated.json
```

### Recipe 4 — Statsig CLI ops

```bash
statsig-cli gates list --env prod
statsig-cli gates create --name new_checkout --description "..."
statsig-cli gates update --name new_checkout --target-app "ios,web" --pass-percentage 10
statsig-cli experiments create --name checkout_layout_test --variants "A,B"
```

### Recipe 5 — Unleash self-hosted (OSS)

```bash
# Deploy to K8s
helm repo add unleash https://docs.getunleash.io/helm-charts
helm upgrade --install unleash unleash/unleash -n unleash --create-namespace

# Use
curl -X POST http://unleash.myorg.com/api/admin/projects/default/features \
  -H "Authorization: $UNLEASH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "new-checkout-flow", "type": "release", "description": "..."}'
```

```python
from openfeature.contrib.provider.unleash import UnleashProvider
import UnleashClient

unleash = UnleashClient(
    url="http://unleash.myorg.com/api/",
    app_name="my-app",
    custom_headers={"Authorization": os.environ["UNLEASH_TOKEN"]},
)
unleash.initialize_client()
api.set_provider(UnleashProvider(unleash))
```

### Recipe 6 — Progressive rollout (5 → 25 → 50 → 100%)

```bash
# LaunchDarkly via API
for pct in 5 25 50 75 100; do
  curl -X PATCH ".../flags/new-checkout-flow" -H "Authorization: $LD_API_KEY" \
    -d "[{\"op\":\"replace\",\"path\":\"/environments/production/rules/0/clauses/0/values\",\"value\":[\"${pct}%\"]}]"
  sleep 1800           # 30 min between stages
  # In real practice: query SLI, abort on regression
done
```

In LD UI, this is Targeting → Add Rule → Percentage rollout.

### Recipe 7 — Auto-rollback on SLO breach

```yaml
# alertmanager → webhook → flag-killswitch Lambda
- alert: NewCheckoutErrorRateHigh
  expr: rate(http_errors_total{flag="new-checkout-flow",exposed="true"}[5m]) > 0.05
  for: 2m
  labels: { severity: critical }
  annotations:
    summary: "Auto-disabling new-checkout-flow"
    webhook_url: "https://lambda.aws.com/disable-flag?name=new-checkout-flow"
```

Lambda calls LaunchDarkly REST to set flag off + posts to Slack.

### Recipe 8 — Flag-as-code (Terraform LaunchDarkly provider)

```hcl
resource "launchdarkly_feature_flag" "new_checkout" {
  project_key = "myorg"
  key         = "new-checkout-flow"
  name        = "New checkout flow"
  description = "Enables the 2026 checkout redesign"
  variation_type = "boolean"
  variations {
    value = "true"
    name  = "Enabled"
  }
  variations {
    value = "false"
    name  = "Disabled"
  }
  defaults {
    on_variation  = 0
    off_variation = 1
  }
  tags = ["growth", "checkout"]
}

resource "launchdarkly_feature_flag_environment" "new_checkout_prod" {
  flag_id        = launchdarkly_feature_flag.new_checkout.id
  env_key        = "production"
  on             = true
  fallthrough { rollout_weights = [25000, 75000] }   # 25% enabled
  off_variation = 1
}
```

```bash
tofu plan && tofu apply
```

### Recipe 9 — Local dev fallback

```python
# Defaults work offline / on misconfigured providers
client = api.get_client()
value = client.get_boolean_value("flag", default_value=False, ...)
# If provider is down, returns default_value (False). Always set a safe default.
```

### Recipe 10 — Experimentation (Statsig)

```typescript
const experiment = await client.getObjectValue(
  "checkout_layout_test",
  { layout: "control" },
  { targetingKey: userId }
);
// Statsig exposes: experiment.layout = "A" | "B" | "control"

// Log conversion event for stat sig analysis
statsig.logEvent({ user, eventName: "purchase", value: cart.total });
```

Statsig auto-computes p-values + lift; LaunchDarkly Experimentation +
GrowthBook similar.

### Recipe 11 — Choose backend

| Tool | Best for | Pricing | OSS? |
|---|---|---|---|
| LaunchDarkly | Enterprise; rich targeting; experimentation | $$$$ paid | Closed |
| Statsig | Mid-size; great free tier; experimentation-first | Generous free + paid | Closed (SDKs open) |
| Unleash | Self-hosted; OSS-first | OSS free + paid managed | Apache 2.0 |
| Flagsmith | Self-hosted OSS alt | OSS free + paid | BSD-3 |
| GrowthBook | OSS A/B testing + flags | OSS free + paid | MIT |
| OpenFeature | SDK only; pair with a backend | Free | Apache 2.0 |

### Recipe 12 — Flag debt cleanup

Flag debt = flags that are 100% on or 100% off and forgotten. Tools:

```bash
# LaunchDarkly Code References finds usages in repos
ldcli code-refs --project myorg --repo-name myorg/api --branch main
# Reports flags with no code refs → safe to delete

# Manual review query
ldcli flags list --output json | \
  jq '.items[] | select(.environments.production.on == false and .environments.production.fallthrough.variation == 1) | .key'
```

Quarterly flag review: delete dead flags; convert "permanent" toggles to
config.

## Examples

### Example 1 — Ship checkout rewrite behind a flag

**Goal:** New checkout flow live but disabled; ramp over a week.

1. Create flag `new-checkout-flow` in LaunchDarkly (Recipe 3 or UI).
2. Code path:

   ```python
   if client.get_boolean_value("new-checkout-flow", False, eval_ctx):
       return new_checkout(...)
   return old_checkout(...)
   ```

3. Deploy with flag at 0% — code is shipped but inert.
4. Day 1: 1% rollout, watch SLI for 4h.
5. Day 2: 5%. Day 3: 25%. Day 5: 50%. Day 7: 100%.
6. After 1 week stable at 100%, delete the old code path + remove flag.

**Result:** Deploy without rollout coupling; any regression aborts via flag flip.

### Example 2 — Vendor migration: LaunchDarkly → Statsig

**Goal:** Cut LaunchDarkly cost; migrate to Statsig free tier.

1. Add OpenFeature abstraction (Recipe 1).
2. Replace provider import: `LaunchDarklyProvider` → `StatsigProvider`.
3. Export flag config from LD (Recipe 3); import to Statsig.
4. Dual-write phase: keep both providers; OpenFeature's MultiProvider votes
   on values, logs disagreements.
5. After 2 weeks parity: remove LD provider, cancel LD plan.

**Result:** Same code, different backend, lower cost.

## Edge cases / gotchas

- **Flag evaluation is HOT path.** Provider SDKs cache locally; <1ms typical.
  Don't fetch from network on every request.
- **Default values are safety nets.** If the provider is down, the SDK
  returns the default. Always default to the SAFE behavior (typically
  `False` for new feature flags, `True` for kill switches).
- **Context cardinality**: targeting on email/user ID balloons evaluation
  cost. Use group/cohort attrs where possible.
- **Flag lifecycle**: temporary flags die. Permanent flags = config. Tag
  flags accordingly; auto-cleanup tools flag dead ones.
- **Targeting rules are evaluated server-side** in some providers (LaunchDarkly
  streams rules to SDK and evaluates locally); ensure SDK has the latest.
- **Webhook latency**: kill-switch via webhook is async; expect 5-30 sec
  before the kill propagates to all SDKs. For instant kill, route via
  service mesh.
- **Statsig environments**: configure `tier` in evaluation context; Statsig
  doesn't separate envs by API key like LD does.
- **Unleash open-source vs Enterprise**: features like SSO, audit logs are
  Enterprise-only. Plan for that if compliance matters.
- **Flag exposure logging** drives experimentation analytics; without it,
  flag groups can't be A/B-tested.
- **Avoid nested flags**: `if flag_a and flag_b` creates 4 combinations.
  Test the matrix or simplify.
- **OpenFeature spec changes**: SDK versions before v1.0 had API drift.
  Pin to `>= 1.0` and migrate on majors.

## Sources

- https://openfeature.dev/ — OpenFeature
- https://openfeature.dev/specification/ — OpenFeature spec
- https://docs.launchdarkly.com/ — LaunchDarkly docs
- https://docs.statsig.com/ — Statsig docs
- https://docs.getunleash.io/ — Unleash docs
- https://docs.flagsmith.com/ — Flagsmith docs
- https://docs.growthbook.io/ — GrowthBook docs
- https://launchdarkly.com/blog/the-flag-debt-problem/ — flag debt patterns
- https://martinfowler.com/articles/feature-toggles.html — Pete Hodgson feature toggles
- https://www.split.io/blog/feature-flags/ — Split's flag taxonomy
