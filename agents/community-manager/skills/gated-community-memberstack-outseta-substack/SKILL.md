<!--
Sources: https://www.memberstack.com/ + https://www.outseta.com/ + https://substack.com/ + https://whop.com/ + https://www.skool.com/ + https://www.circle.so/pricing + https://stripe.com/docs
-->
# Gated Community (Memberstack / Outseta / Substack / Whop / Skool) — SKILL

Stack options for gated paid community: Memberstack (Webflow-friendly), Outseta (all-in-one CRM + paywall + native community), Substack Paid (newsletter + chat), Whop (creator-economy gated Discord), Skool (course + community bundle), Circle Paid Memberships (native Circle). Stripe-driven membership tier sync to Discord/Slack roles via webhook. Tiered access with auto-role promotion + downgrade on payment failure.

## When to use

- Choosing a gated community stack — first time monetization.
- Existing free community moving to paid tier (e.g., Circle → Circle Paid, Discord → Whop).
- Creator-economy gating (Discord behind Patreon-equivalent).
- Course + community bundle (Skool / Mighty).
- Newsletter-as-community paid tier (Substack Chat).
- Setting up automatic role-sync on payment events (subscribed → role X; canceled → role removed).
- Migrating from one paywall to another (e.g., Memberstack → Outseta).
- Compliance / tax handling for international paying members.

Trigger phrases: "paid community", "gated community", "paywall", "Memberstack", "Outseta", "Substack paid", "Whop", "Skool", "Circle paid", "creator monetization", "Discord paywall", "role sync", "Patreon Discord".

## Setup

```bash
# Memberstack
export MEMBERSTACK_SECRET=$(op item get memberstack --fields secret_key)
curl -H "X-API-KEY: $MEMBERSTACK_SECRET" \
  https://admin.memberstack.com/members

# Outseta
export OUTSETA_KEY=$(op item get outseta --fields api_key)
export OUTSETA_SECRET=$(op item get outseta --fields api_secret)
curl -H "Authorization: Outseta $OUTSETA_KEY:$OUTSETA_SECRET" \
  "https://brand.outseta.com/api/v1/crm/people"

# Substack — no public API for paid subscribers (as of 2026)
# Use Stripe direct queries + Substack admin export for sync

# Whop
curl -H "Authorization: Bearer $WHOP_API_KEY" \
  https://api.whop.com/api/v2/memberships

# Skool — no full API (closed); use webhook + Zapier alt

# Circle paid memberships
curl -H "Authorization: Bearer $CIRCLE_API_TOKEN" \
  "https://api.circle.so/v1/paid_memberships"

# Stripe (for cross-platform sync source-of-truth)
mcp tool stripe.subscriptions_list --status active --limit 100
```

Auth + env:
- `MEMBERSTACK_SECRET` — Memberstack → Dev tools → API keys.
- `OUTSETA_KEY` + `OUTSETA_SECRET` — Outseta → Admin → Settings → API.
- `WHOP_API_KEY` — Whop → Settings → API → Generate.
- `CIRCLE_API_TOKEN` — Circle → Settings → API access.
- `STRIPE_SECRET_KEY` — Stripe Dashboard → Developers → API keys.
- `DISCORD_BOT_TOKEN` — for role sync.
- Webhook secrets per platform for signature verification.

Workspace prerequisites:
- Stripe account configured with tier products: `free`, `member ($9/mo)`, `vip ($29/mo)`, `vip-annual ($299/yr)`.
- Discord/Slack/Circle roles created per tier.
- Webhook endpoint (Vercel/Cloudflare/AWS Lambda) with signature verification.
- Failed-payment recovery flow (Stripe Smart Retries enabled).

## Common recipes

### Recipe 1: Stack selection matrix

| Profile | Stack | Why |
|---|---|---|
| Webflow site + paid community | Memberstack + Circle/Discord | Best Webflow integration |
| All-in-one CRM + paywall + community | Outseta | One vendor; built-in community native |
| Newsletter primary | Substack Paid + Chat | Newsletter audience inherits community |
| Creator gated Discord | Whop | Best Discord-native creator workflow |
| Course + community bundle | Skool or Mighty | Bundled learning + community |
| Already on Circle, want paid | Circle Paid Memberships | Native zero-integration |
| Custom stack, full control | Stripe + custom backend + Discord role bot | Most flexible, most engineering |

### Recipe 2: Memberstack → Discord role sync

```python
# Webhook from Memberstack on subscription event
@app.post("/webhook/memberstack")
def memberstack_hook(payload, signature):
    if not verify_memberstack_signature(payload, signature, MEMBERSTACK_WEBHOOK_SECRET):
        return 401

    member = payload["data"]
    discord_id = member["customFields"].get("discord_id")
    if not discord_id:
        return 200  # no discord linked

    event = payload["event"]
    tier = member["planConnections"][0]["plan"]["name"] if member["planConnections"] else None

    if event == "member.plan.subscribed":
        role_id = ROLE_MAP[tier]  # e.g., {"vip": "123", "member": "456"}
        discord_full.add_member_role(
            guild_id=GUILD, user_id=discord_id, role_id=role_id
        )
    elif event in ("member.plan.canceled", "member.plan.payment_failed"):
        # Remove all paid roles
        for r in PAID_ROLES:
            discord_full.remove_member_role(
                guild_id=GUILD, user_id=discord_id, role_id=r
            )
        if event == "member.plan.payment_failed":
            # Grace period: 7 days
            schedule_grace_removal(discord_id, days=7)
```

### Recipe 3: Outseta CRM + paywall + community config

```bash
# Create plan
curl -X POST https://brand.outseta.com/api/v1/billing/plans \
  -H "Authorization: Outseta $OUTSETA_KEY:$OUTSETA_SECRET" \
  -d '{
    "Name": "VIP Annual",
    "Description": "VIP all-access annual",
    "Amount": 299,
    "BillingTerm": 365,
    "TrialPeriodDays": 7
  }'

# Sign up flow embed code (drop into Webflow / static site)
# <div data-o-link="auth?registrationPlanUid=PLAN_UID"></div>

# Webhook for subscription events
# POST /webhook/outseta:
# - subscription.created → add discord role
# - subscription.canceled → schedule role removal
# - subscription.payment_failed → grace period
```

Outseta's "Community" feature is bundled native; for Discord/Slack also bind:

```python
@app.post("/webhook/outseta")
def outseta_hook(payload):
    if payload["EventName"] == "Subscription.Created":
        person = payload["Entity"]["Person"]
        discord_id = person["CustomProperties"].get("DiscordId")
        plan_uid = payload["Entity"]["Plan"]["Uid"]
        role_id = ROLE_MAP[plan_uid]
        discord_full.add_member_role(GUILD, discord_id, role_id)
```

### Recipe 4: Substack Paid + Chat setup

```bash
# Substack has no public API for paid subscribers
# Workflow:
# 1. Configure paid tiers in Substack admin → Paid posts → Settings
# 2. Enable Chat → restrict to paid subscribers
# 3. Set up Stripe webhook directly (Substack uses Stripe under the hood):
#    Stripe Dashboard → Webhooks → Add endpoint
#    Events: customer.subscription.created, customer.subscription.deleted

# Discord sync via Stripe webhook (Recipe 7)
```

Substack Chat: paid-tier-restricted access in the publication. Notes (public) feed = top-of-funnel.

### Recipe 5: Whop gated Discord

```bash
# Create product in Whop
curl -X POST https://api.whop.com/api/v2/products \
  -H "Authorization: Bearer $WHOP_API_KEY" \
  -d '{
    "name": "VIP Community Access",
    "price": 29,
    "interval": "monthly",
    "discord_integration": {
      "guild_id": "'$GUILD'",
      "role_ids": ["'$VIP_ROLE_ID'"]
    }
  }'

# Whop auto-syncs Discord roles on purchase + cancel; no custom webhook needed
# Verify roles via dashboard at app.whop.com/dashboard
```

Whop is Discord-native; choose this if Discord-gating is the entire product.

### Recipe 6: Circle Paid Memberships

```bash
# Create paid plan in Circle
curl -X POST https://api.circle.so/v1/paid_membership_plans \
  -H "Authorization: Token $CIRCLE_API_TOKEN" \
  -d '{
    "name": "VIP",
    "amount_cents": 2900,
    "billing_interval": "monthly",
    "trial_days": 7,
    "access_groups": ["VIP Spaces"]
  }'

# Get current paying members
curl -H "Authorization: Token $CIRCLE_API_TOKEN" \
  "https://api.circle.so/v1/paid_memberships?status=active" \
  | jq '.paid_memberships[]'
```

Circle Paid handles tax / payment / dunning automatically. Zero custom backend.

### Recipe 7: Stripe-as-source-of-truth cross-sync

When using Stripe directly with no SaaS paywall:

```python
# Stripe webhook → multi-platform sync
import stripe
stripe.api_key = STRIPE_SECRET_KEY

@app.post("/webhook/stripe")
def stripe_hook(payload, signature):
    event = stripe.Webhook.construct_event(
        payload, signature, STRIPE_WEBHOOK_SECRET
    )

    if event["type"] == "customer.subscription.created":
        sub = event["data"]["object"]
        customer = stripe.Customer.retrieve(sub["customer"])
        discord_id = customer["metadata"].get("discord_id")
        plan = sub["items"]["data"][0]["price"]["nickname"]
        if discord_id:
            discord_full.add_member_role(GUILD, discord_id, ROLE_MAP[plan])

    elif event["type"] == "customer.subscription.deleted":
        sub = event["data"]["object"]
        customer = stripe.Customer.retrieve(sub["customer"])
        discord_id = customer["metadata"].get("discord_id")
        if discord_id:
            for r in PAID_ROLES:
                discord_full.remove_member_role(GUILD, discord_id, r)

    elif event["type"] == "invoice.payment_failed":
        # Grace period — Stripe Smart Retries handles next 7 days
        sub = stripe.Subscription.retrieve(event["data"]["object"]["subscription"])
        customer = stripe.Customer.retrieve(sub["customer"])
        discord_id = customer["metadata"].get("discord_id")
        slack_mcp.chat_postMessage(
            channel="#community-billing-alerts",
            text=f"Payment failed for <@{customer['email']}> ({discord_id}). "
                 f"Stripe Smart Retries will attempt next 7d."
        )
```

### Recipe 8: Tier table for member-facing pricing page

```markdown
| Tier | Price | Discord access | Live AMAs | Office hours | Course access | Swag |
|---|---|---|---|---|---|---|
| **Free** | $0 | #general only | Public AMAs | — | — | — |
| **Member** | $9/mo | All channels | Member AMAs | Group office hours | 50% off | Quarterly |
| **VIP** | $29/mo | All + #vip + DM ambassadors | Private VIP AMAs | 1:1 office hours | Free | Monthly |
| **VIP Annual** | $299/yr | All + lifetime alumni role | Anniversary VIP event | 1:1 office hours | Free | Welcome kit + monthly |
```

Pin this in `#about` / community landing page.

### Recipe 9: Payment-failure grace flow

```python
# 7-day grace period before role removal on payment_failed
import time
def schedule_grace_removal(discord_id, days=7):
    scheduler.add_job(
        remove_paid_roles,
        trigger="date",
        run_date=datetime.now() + timedelta(days=days),
        args=[discord_id],
        id=f"grace-{discord_id}",
        replace_existing=True,
    )

# On successful retry, cancel grace job
@app.post("/webhook/stripe-success")
def cancel_grace(payload):
    if event["type"] == "invoice.payment_succeeded":
        scheduler.remove_job(f"grace-{discord_id}")
```

Notify member during grace via Discord DM:
```
Hey! Your payment didn't go through. We've kept your VIP access for 7 days
while Stripe retries. Update card: {stripe_portal_url}
```

### Recipe 10: Migration playbook (Memberstack → Outseta)

```python
# 1. Export Memberstack members + tiers
import requests
ms_members = requests.get(
    "https://admin.memberstack.com/members",
    headers={"X-API-KEY": MEMBERSTACK_SECRET},
).json()

# 2. Import to Outseta
for m in ms_members:
    requests.post(
        "https://brand.outseta.com/api/v1/crm/people",
        headers={"Authorization": f"Outseta {OUTSETA_KEY}:{OUTSETA_SECRET}"},
        json={
            "Email": m["email"],
            "FirstName": m["firstName"],
            "LastName": m["lastName"],
            "CustomProperties": {
                "DiscordId": m["customFields"].get("discord_id"),
                "MigratedFrom": "Memberstack",
                "MigratedOn": str(datetime.now()),
            },
        },
    )

# 3. Recreate Stripe subscriptions on Outseta plan ids
# (Outseta will issue new Stripe subscriptions; cancel old Memberstack ones)

# 4. Update Webflow embed code: data-o-link → memberstack:* → outseta:*

# 5. Sunset Memberstack webhook; enable Outseta webhook
```

## Examples

### Example 1: Creator launching $9/mo Discord (Whop)

**Goal:** Solo creator, 12k Discord free members, wants paid VIP tier.

**Steps:**
1. Whop product setup (Recipe 5) → auto Discord integration.
2. Create `VIP` Discord role; restrict #vip-channels to that role.
3. Pin pricing page in `#about` (Recipe 8).
4. Launch announcement post → DM to engaged free members.
5. Whop handles billing, role sync, refunds. Creator-side: just monitor.

**Result:** 380 paid in month 1 ($3,420 MRR). Zero engineering hours.

### Example 2: B2B SaaS community with tiered access (Outseta)

**Goal:** B2B SaaS with $9/mo Member + $29/mo VIP + free public Discord.

**Steps:**
1. Outseta plans created (Recipe 3).
2. Outseta embed code on Webflow site checkout.
3. Discord roles + #vip channels created.
4. Outseta webhook → Discord role sync.
5. Outseta's native community used for member-only doc + announcements; Discord for chat.
6. Stripe Smart Retries enabled for dunning (Recipe 9).
7. Monthly: pull `paid_memberships?status=active` → reconcile against Discord role membership.

**Result:** 270 Members + 45 VIPs. Outseta consolidates CRM (revenue team uses it) + paywall + native community.

### Example 3: Webflow-first SaaS (Memberstack + Discord)

**Goal:** Webflow-built marketing site; want paid Discord access.

**Steps:**
1. Memberstack plans on Webflow pricing page.
2. Stripe under the hood (Memberstack manages).
3. Webhook (Recipe 2) → Discord role sync.
4. Memberstack `discord_id` custom field captured on signup (after OAuth dance).
5. Grace period flow (Recipe 9) on payment failures.

**Result:** Memberstack handles auth + billing; Discord becomes the gated community. ~$15/mo Memberstack cost.

### Example 4: Newsletter-first paid community (Substack)

**Goal:** Newsletter has 50k free / 3k paid subscribers. Wants community for paid only.

**Steps:**
1. Enable Substack Chat → restrict to paid (Recipe 4).
2. Substack Notes for public top-of-funnel.
3. No Discord; chat lives in Substack.
4. Stripe webhook (Recipe 7) → if discord_id custom_field exists, dual-sync to Discord VIP role.
5. Monthly community digest goes out via Substack post (paid-only).

**Result:** Zero external community tool. ~$0 incremental cost. Tradeoff: Substack Chat UI is lightweight vs Discord.

## Edge cases / gotchas

- **Webhook signature verification** — Memberstack HMAC-SHA256, Outseta bearer, Stripe HMAC. Verify or risk fake events.
- **Race conditions on role sync** — payment created + canceled in same minute. Use idempotency keys + state machine.
- **Discord ID linking** — OAuth flow needed: Memberstack/Outseta → Discord OAuth → store discord_id. Without this, no sync possible.
- **Substack no API** — does not expose paid subscriber list publicly. Use Stripe directly + CSV exports for reconciliation.
- **Whop locked to Discord** — Discord-first; for Slack/Circle use Outseta/Memberstack.
- **Tax compliance** — VAT/GST/sales tax. Stripe Tax helps. Substack / Whop / Outseta auto-handle. Memberstack does not.
- **Grandfather pricing** — lock by plan_id; new tiers go to new pricing.
- **Refund vs payment-failed** — immediate role removal for refunds; grace period for payment-failed.
- **Multiple subscriptions per member** — VIP + VIP-Annual upgrade = 2 active. Pick max-tier.
- **Cancel-but-keep-access-until-period-end** — Stripe default. Don't remove role until period end.
- **Role hierarchy** — bot must have role higher than tier roles. Common cause of "bot fails to assign role".
- **Skool / Mighty closed ecosystems** — no public API. Webhooks only; no programmatic member CRUD.
- **Substack Chat moderation** — limited; cannot replicate Discord automod.
- **Circle Paid + Memberstack double-paywall** — if both active, double charging. Pick one source-of-truth.

## Sources

- [Memberstack docs](https://docs.memberstack.com/)
- [Outseta API](https://developers.outseta.com/)
- [Substack help — Paid](https://support.substack.com/hc/en-us/articles/360037486012)
- [Substack Chat](https://substack.com/note)
- [Whop API docs](https://docs.whop.com/)
- [Skool community help](https://www.skool.com/help)
- [Circle API reference](https://api.circle.so/)
- [Stripe webhook signing](https://stripe.com/docs/webhooks/signatures)
- [Stripe Smart Retries](https://stripe.com/docs/billing/revenue-recovery/smart-retries)
- [Stripe Tax](https://stripe.com/docs/tax)
- [Discord Add Guild Member Role](https://discord.com/developers/docs/resources/guild#add-guild-member-role)
