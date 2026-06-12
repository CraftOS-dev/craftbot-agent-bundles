<!--
Source: https://developers.friendbuy.com/ + https://developer.referralcandy.com/ + https://docs.influitive.com/ + https://docs.growsurf.com/ + https://help.tremendous.com/ + https://stripe.com/docs/api/customer_balance_transactions + https://app.delighted.com/docs/api
-->
# Referral Programs — Friendbuy / ReferralCandy / GrowSurf / Influitive / Tremendous — SKILL

Orchestrate customer referral programs end-to-end: identify eligible referrers (NPS >= 8 + active >= 6mo), generate personal referral links, track referred signups, reward referrer + referee on qualified events, and report on program ROI. Primary stacks: Friendbuy / ReferralCandy / GrowSurf / Mention Me / Referral Rock for the referral platform; Tremendous / Stripe credits / service credits for payouts. Free fallback: Notion tracker + Stripe credit issuance.

## When to use

- **Stand up a new referral program** — pick platform (Friendbuy SaaS-native; GrowSurf modern; ReferralCandy ecom-native; Influitive advocacy-led), define reward tiers, launch.
- **Invite existing promoters to refer** — NPS 9-10 + tenure 6mo+ -> referral invite email + personal link.
- **Issue referral reward** — referred signup converts to paid; auto-issue $X credit to referrer + $Y discount to referee.
- **Quarterly referral reminder** — nudge inactive referrers who haven't shared in 90d.
- **Audit program ROI** — referrals invited / shared / converted / ARR contributed / CAC payback.
- **Reward fulfillment alternate path** — referrer wants Tremendous gift card not service credit; switch payout.

This skill **reads from** `nps-csat-ces-tracking` (promoter list source) and `customer-milestone-anniversary` (1yr+ tenure check). It **feeds** `customer-advocacy-case-study-reference` (high-converting referrers are advocacy candidates) and finance reporting (referral CAC).

Trigger phrases: "referral program", "Friendbuy", "ReferralCandy", "GrowSurf", "Mention Me", "Influitive referral", "referral link", "refer a friend", "Tremendous payout", "referral reward".

## Setup

```bash
# Friendbuy (SaaS-native referral platform)
export FRIENDBUY_API_KEY="<key>"
export FRIENDBUY_MERCHANT_ID="<merchant-id>"

# ReferralCandy (ecom-style + SaaS)
export REFERRALCANDY_ACCESS_ID="<access-id>"
export REFERRALCANDY_SECRET_KEY="<secret>"

# GrowSurf (modern SaaS referral)
export GROWSURF_API_KEY="<key>"
export GROWSURF_CAMPAIGN_ID="<campaign-id>"

# Mention Me (enterprise referral)
export MENTIONME_API_KEY="<key>"

# Referral Rock (SMB referral)
export REFERRALROCK_API_KEY="<key>"

# Influitive (advocacy-led referrals)
export INFLUITIVE_API_TOKEN="<token>"
export INFLUITIVE_SUBDOMAIN="acme"

# Tremendous (reward fulfillment - gift cards / Visa cards)
export TREMENDOUS_API_KEY="<key>"
export TREMENDOUS_FUNDING_SOURCE_ID="<id>"
export TREMENDOUS_CAMPAIGN_ID="<id>"

# Stripe (service credit fallback) - via stripe-mcp
# Delighted (eligible promoter list) - via cli-anything curl
```

Workspace prerequisites:
- Eligibility rule: NPS >= 8 AND tenure >= 180 days AND health_score >= 0.6.
- Reward tier defined and approved by finance + legal (tax disclosures, ToS).
- Notion "Referrals" DB with: Referrer, Referrer Email, Platform Link, Referee, Referee Email, Status (Invited / Shared / Signed Up / Converted / Rewarded), Reward Type, Reward Amount, Created, Converted At, ARR Contributed.
- Cron job: nightly Delighted promoter pull + 90-day inactive referrer reminder.

## Reward tier reference

| Event | Referrer reward | Referee reward |
|---|---|---|
| Qualified signup (trial start) | $25 service credit | 10% off first 3 months |
| Converted to paid | $200 service credit OR $200 Tremendous | 10% off first 3 months |
| Annual plan converted | $500 OR $500 Tremendous | 1 free month |
| Enterprise referral (closed-won, > $50k ARR) | $1000 Tremendous + thank-you call | Negotiated |

Always disclose in T&Cs: max payout per referrer per year, tax form thresholds (US: $600/yr triggers 1099), and platform-specific reward expiry.

## Common recipes

### Recipe 1: Pull eligible referrers (Delighted promoter + tenure filter)

```bash
curl -sS "https://api.delighted.com/v1/responses?score=8..10&since=$(date -u -d '30 days ago' +%s)&expand=person" \
  -u "$DELIGHTED_API_KEY:" | jq '.[] | {
    email: .person.email,
    name: .person.name,
    score
  }'
```

Then filter via Postgres for tenure + health:

```sql
SELECT p.email, p.name, p.score, c.signup_date, c.health_score
FROM delighted_promoters p
JOIN customers c ON c.email = p.email
LEFT JOIN referrers r ON r.email = p.email
WHERE p.score >= 8
  AND c.signup_date <= now() - INTERVAL '180 days'
  AND c.health_score >= 0.6
  AND (r.last_invited IS NULL OR r.last_invited < now() - INTERVAL '90 days');
```

Doc: https://app.delighted.com/docs/api

### Recipe 2: Create / fetch Friendbuy personal referral link

```bash
curl -sS -X POST "https://api.friendbuy.com/v1/advocates" \
  -H "Authorization: Bearer $FRIENDBUY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "merchantId": "'$FRIENDBUY_MERCHANT_ID'",
    "email": "'$REFERRER_EMAIL'",
    "name": "'$REFERRER_NAME'",
    "customerId": "'$STRIPE_CUSTOMER_ID'"
  }' | jq -r '.shareLink'
```

Doc: https://developers.friendbuy.com/

### Recipe 3: GrowSurf participant + share link

```bash
curl -sS -X POST "https://api.growsurf.com/v2/campaign/$GROWSURF_CAMPAIGN_ID/participant" \
  -H "Authorization: Bearer $GROWSURF_API_KEY" \
  -d '{
    "email": "'$REFERRER_EMAIL'",
    "firstName": "'$REFERRER_FIRST_NAME'",
    "metadata": {"tier": "growth", "csm": "'$CSM_NAME'"}
  }' | jq -r '.shareUrl'
```

Doc: https://docs.growsurf.com/

### Recipe 4: ReferralCandy customer enrollment

```bash
curl -sS -X POST "https://my.referralcandy.com/api/v1/customers" \
  -u "$REFERRALCANDY_ACCESS_ID:$REFERRALCANDY_SECRET_KEY" \
  -d "email=$REFERRER_EMAIL" \
  -d "first_name=$REFERRER_FIRST_NAME" \
  -d "purchase_amount=0" \
  -d "purchase_timestamp=$(date +%s)"
```

Doc: https://developer.referralcandy.com/

### Recipe 5: Influitive challenge for referral submission

```bash
curl -sS -X POST "https://$INFLUITIVE_SUBDOMAIN.influitive.com/api/v1/members/$MEMBER_ID/challenges/$REFERRAL_CHALLENGE_ID/activities" \
  -H "Authorization: Token token=$INFLUITIVE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "completed": false,
    "metadata": {
      "referee_email": "'$REFEREE_EMAIL'",
      "referee_company": "'$REFEREE_COMPANY'"
    }
  }'
```

Doc: https://docs.influitive.com/

### Recipe 6: Draft personalized referral invite

```python
prompt = f"""
Draft a 4-5 sentence referral invite email.

Referrer: {referrer.name}
Tenure: {tenure_months} months
NPS: {referrer.nps_score}/10
Specific outcome they hit: {referrer.success_milestone}

Asks:
1. Refer one peer who'd benefit; they get 10% off; you get $200 credit when they convert.
2. Personal share link: {share_link}

Rules:
- Lead with the specific outcome they achieved.
- Don't say "Hope you're doing well" or "Just touching base."
- No emoji. No "thrilled".
- Sign from {csm.name}.
"""
body = claude.generate(prompt)
gmail.send_email(to=[referrer.email], subject=f"{referrer.name} - quick favor", body=body)
```

### Recipe 7: Webhook handler — referral converted -> issue reward

```python
# Webhook payload from Friendbuy / GrowSurf when a referee converts
event = json.loads(request.body)

if event["type"] == "referral.converted":
    referrer_email = event["data"]["advocate_email"]
    referee_email = event["data"]["referee_email"]
    arr = event["data"]["plan_arr"]

    # Issue referrer reward (Tremendous $200)
    issue_tremendous_reward(referrer_email, 200, campaign=TREMENDOUS_CAMPAIGN_ID)

    # OR issue Stripe service credit
    # issue_stripe_credit(referrer_stripe_id, 20000)  # cents

    # Notion log
    notion.update_page(referral_page_id, {"Status": "Rewarded", "Reward Amount": 200, "ARR Contributed": arr})
```

### Recipe 8: Issue Tremendous payout

```bash
curl -sS -X POST "https://www.tremendous.com/api/v2/orders" \
  -H "Authorization: Bearer $TREMENDOUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "ref-'$REFERRAL_ID'",
    "payment": {"funding_source_id": "'$TREMENDOUS_FUNDING_SOURCE_ID'"},
    "rewards": [{
      "value": {"denomination": 200, "currency_code": "USD"},
      "campaign_id": "'$TREMENDOUS_CAMPAIGN_ID'",
      "recipient": {"email": "'$REFERRER_EMAIL'", "name": "'$REFERRER_NAME'"}
    }]
  }'
```

Doc: https://help.tremendous.com/hc/en-us/categories/360002107552-API

### Recipe 9: Issue Stripe service credit (free reward path)

```bash
# $200 service credit to referrer's Stripe customer balance
curl -sS -X POST "https://api.stripe.com/v1/customers/$STRIPE_CUSTOMER_ID/balance_transactions" \
  -u "$STRIPE_SECRET_KEY:" \
  -d "amount=-20000" \
  -d "currency=usd" \
  -d "description=Referral reward: $REFEREE_NAME signed up"
```

Doc: https://stripe.com/docs/api/customer_balance_transactions

### Recipe 10: Apply referee discount on signup (Stripe coupon)

```bash
# Apply 10% off coupon to referee's subscription
curl -sS -X POST "https://api.stripe.com/v1/subscriptions/$REFEREE_SUBSCRIPTION_ID" \
  -u "$STRIPE_SECRET_KEY:" \
  -d "coupon=referral_10pct_3mo"
```

The coupon `referral_10pct_3mo` should be pre-created with `percent_off=10` + `duration=repeating` + `duration_in_months=3`.

### Recipe 11: Get referral program analytics (Friendbuy)

```bash
curl -sS "https://api.friendbuy.com/v1/reports/campaign-performance?merchantId=$FRIENDBUY_MERCHANT_ID&from=2026-04-01&to=2026-06-30" \
  -H "Authorization: Bearer $FRIENDBUY_API_KEY" | jq '.'
```

Returns referrers, shares, signups, conversions, payout total.

### Recipe 12: Quarterly inactive-referrer reminder

```sql
-- Referrers who got a link but haven't shared in 90+ days
SELECT r.email, r.name, r.platform_link, r.last_invited
FROM referrers r
LEFT JOIN referral_events e ON e.referrer_email = r.email AND e.event_type = 'share' AND e.timestamp >= now() - INTERVAL '90 days'
WHERE r.last_invited >= now() - INTERVAL '180 days'
  AND e.id IS NULL;
```

Send a single nudge via Gmail; no further follow-up.

### Recipe 13: Notion referral tracker upsert

```python
notion.create_page(
    parent={"database_id": REFERRALS_DB_ID},
    properties={
        "Referrer": {"title": [{"text": {"content": referrer.name}}]},
        "Referrer Email": {"email": referrer.email},
        "Platform Link": {"url": share_link},
        "Status": {"status": {"name": "Invited"}},
        "Reward Type": {"select": {"name": "Tremendous $200"}},
        "Created": {"date": {"start": today_iso}},
        "Source": {"select": {"name": "Delighted NPS 10"}},
    },
)
```

### Recipe 14: Program ROI report (xlsx)

```sql
SELECT
  date_trunc('month', converted_at) AS month,
  count(*) AS converted_referrals,
  sum(arr_contributed) AS arr_contributed,
  sum(reward_amount) AS total_rewards_paid,
  sum(arr_contributed) / NULLIF(sum(reward_amount), 0)::numeric AS roi_ratio,
  sum(reward_amount) / NULLIF(count(*), 0)::numeric AS cost_per_acquisition
FROM referrals
WHERE converted_at IS NOT NULL
  AND converted_at >= now() - INTERVAL '12 months'
GROUP BY 1
ORDER BY 1;
```

Output to `xlsx` skill -> finance + CS leadership share.

## Examples

### Example 1: NPS 10 promoter -> referral invite -> converted in 30 days

**Goal:** Acme.Jane scored 10 on NPS; convert her into an active referrer.

**Steps:**
1. Tue 23:00 UTC: Recipe 1 finds Jane (NPS 10, 14mo tenure, health 0.82).
2. Wed 06:00 UTC: Recipe 2 generates Friendbuy share link for Jane.
3. Wed 09:00 UTC: Recipe 6 drafts personalized invite ("Saw your NPS - 60% reduction in onboarding time stood out. Your peer at Globex would love that story; here's a link..."); Recipe 13 logs.
4. Wed 14:00 UTC: Jane shares with 2 contacts.
5. Wed + 21 days: Globex.Sara signs up via link; Recipe 10 applies 10% coupon.
6. Wed + 35 days: Sara converts to paid annual ($12k ARR); Recipe 7 fires.
7. Recipe 8 issues $200 Tremendous to Jane; Notion status -> Rewarded.

**Result:** $200 reward; $12k ARR; 60x ROI on this referral.

### Example 2: Quarterly inactive-referrer sweep

**Goal:** 47 referrers got links in Q1; only 12 shared. Nudge the rest.

**Steps:**
1. Recipe 12 returns 35 inactive referrers.
2. Recipe 6 drafts a soft nudge ("Quick note - your link is still active; any chance you have a peer who'd benefit?").
3. Gmail send (rate-limited 50/hr, send via Mixmax or `gmail-mcp` directly).
4. 14-day measurement: 5 shared post-nudge; 2 converted.
5. Document the conversion lift in CS playbook.

**Result:** Reactivated dormant referrers; 5% net lift on the cohort.

### Example 3: Switch from Stripe credit to Tremendous payout

**Goal:** Referrer requested gift card not service credit.

**Steps:**
1. Verify referrer eligibility + reward amount.
2. Reverse pending Stripe credit if applicable: `POST /customer_balance_transactions` with positive amount.
3. Recipe 8 issues Tremendous payout.
4. Recipe 13 updates Notion: Reward Type = Tremendous $200; Reward Status = Sent.
5. Email referrer: "Sent the $200 gift card via Tremendous; arrives in ~24h. Thanks again."

**Result:** Referrer satisfied; reward fulfilled; bookkeeping clean.

## Edge cases / gotchas

- **Self-referral fraud** — referrer creates a fake email and "refers themselves." Block via duplicate-phone, duplicate-IP, duplicate-payment-method checks. Friendbuy + ReferralCandy do this; if rolling your own, add at Stripe layer.
- **Referee uses VPN / different account** — same physical user signs up under different email to get the discount. Hard to fully block; spot-check large rewards before paying out.
- **Reward tax thresholds** — US: payouts > $600/yr per recipient = 1099 filing required. Tremendous tracks; service credits don't trigger 1099 but consult finance.
- **Coupon stacking** — referee already had a separate promo code; layering 10% off referral on top can exceed margin caps. Stripe coupon `applies_to` + `restrictions` should enforce.
- **Referee bounces after 14d** — auto-issued $200 referrer reward + churning referee = negative ROI. Wait 30d or until 2nd month payment confirmed before paying out (`converted_at >= now() - INTERVAL '30 days'`).
- **Platform vendor lock-in** — Friendbuy stores shareLink state; switching to GrowSurf later requires re-onboarding all referrers. Mirror shareLink state in Notion or Postgres as SOT.
- **GDPR + referee consent** — referee in EU needs to consent to data sharing before being marketed to. Check that the platform handles this (Friendbuy / Mention Me do; some don't).
- **Reward expiry** — Tremendous gift cards expire after Y days if unclaimed; Stripe credit doesn't expire but stale credits skew NRR math. Document the expiry policy.
- **Currency mismatches** — EU referrer earns $200 in USD; converting to EUR via Tremendous adds 2-3% fee. Issue local currency where supported.
- **Influitive cost** — Influitive is a points-game advocacy platform (~$30k/yr). For pure referral, Friendbuy / GrowSurf are cheaper.
- **Customer NDA constraints** — some customers' contracts forbid public referral participation. Check Notion customer-NDA flag before inviting.
- **Reward fatigue** — same referrer gets 4 rewards in a month and stops sharing. Soft cap at 3 paid rewards / quarter; CSM-Lead approval for above.
- **Anonymous referrals** — referrer wants payout but referee doesn't want vendor knowing the connection. Honor; pay referrer; don't reveal referee identity in case study or marketing.
- **Cross-system referrer ID collision** — Friendbuy advocate ID != Stripe customer ID != Notion page ID. Maintain a canonical Postgres `referrers` table with all platform IDs joined.

## Sources

- [Friendbuy Developer Docs](https://developers.friendbuy.com/)
- [Friendbuy Advocate API reference](https://developers.friendbuy.com/api/advocates)
- [ReferralCandy API](https://developer.referralcandy.com/)
- [GrowSurf REST API](https://docs.growsurf.com/integrations/rest-api)
- [Mention Me API](https://mentionme.com/developer/)
- [Referral Rock API](https://docs.referralrock.com/)
- [Influitive Advocate API](https://docs.influitive.com/)
- [Tremendous Orders API](https://help.tremendous.com/hc/en-us/categories/360002107552-API)
- [Stripe customer balance transactions](https://stripe.com/docs/api/customer_balance_transactions)
- [Stripe coupons API](https://stripe.com/docs/api/coupons)
- [Delighted Responses API](https://app.delighted.com/docs/api)
- [IRS 1099-MISC threshold guidance](https://www.irs.gov/forms-pubs/about-form-1099-misc)
