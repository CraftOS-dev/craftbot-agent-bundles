<!--
Source: https://www.rocketmoney.com/ + https://www.lunchmoney.app/ + https://actualbudget.com/
-->
# Subscription Tracker + Cancellation — SKILL

Detect recurring charges + duplicates + low-usage subscriptions; recommend keep/cancel/negotiate/downgrade; draft cancellation outreach. Rocket Money auto-detects + handles cancellation negotiation; Bobby is manual; agent path uses `actual-budget-mcp` / `ynab-mcp` / `lunchmoney-mcp` for txn analysis + `gmail-mcp` for outreach.

## When to use this skill

- **"Audit my subscriptions"** — quarterly review.
- **"What am I paying for?"** — surface state.
- **"Cancel Netflix" (and others)** — draft outreach.
- **"Detect duplicate streaming"** — dedup recommendation.
- **Annual budget review** — Q1 / pre-tax-season.

**Do NOT use this skill when:**
- General personal finance / budget — handled by `actual-budget-mcp` / `ynab-mcp` directly.
- Business / corp-card subscriptions — see `expense-tracking-expensify-ramp-brex`.
- Family-shared subscription disputes — out of scope; handle in family meeting.

## Setup

### Personal-finance MCPs (in agent.yaml)

- `actual-budget-mcp` — open-source budgeting; txn analysis
- `ynab-mcp` — You Need A Budget
- `lunchmoney-mcp` — modern personal finance
- `gmail-mcp` — outreach drafting
- `notion-mcp` — subscription DB
- `stripe-mcp` — personal Stripe data if applicable

### Optional: Rocket Money

Rocket Money is the consumer SOTA (auto-detect + cancellation negotiation). Limited public API. Agent recommends user install + manages workflow from Notion DB instead.

```bash
# Web: https://www.rocketmoney.com/
# iOS / Android apps for live detection
```

### Notion Subscription DB schema

```
| Field | Type | Notes |
|---|---|---|
| Vendor | Title | Name |
| Service category | Select | Streaming / Cloud / SaaS / Gym / News / Productivity / Insurance / Other |
| Monthly amount | Number | $ |
| Annual amount | Formula | Monthly × 12 |
| Cadence | Select | Monthly / Annual / Lifetime |
| Renewal date | Date | Next charge |
| Last used | Date | Manual update |
| Status | Select | Active / Negotiating / Cancelling / Cancelled |
| Cancel link | URL | Direct cancel form |
| Account email | Email | For outreach |
| Notes | Text | Retention-offer history |
| Decision | Select | Keep / Cancel / Negotiate / Downgrade |
| Annual savings if cut | Formula | Annual × (Decision == Cancel) |
```

## Common recipes

### Recipe 1: Pull last 12 months of txns

```bash
mcp tool actual-budget.list_transactions \
  --account-id "<>" \
  --start "2025-06-01" \
  --end "2026-06-01" \
  > txns.json
```

Or via YNAB / Lunch Money:

```bash
mcp tool lunchmoney.list_transactions \
  --start-date "2025-06-01" \
  --end-date "2026-06-01"
```

### Recipe 2: Detect recurring subscriptions (Python)

```python
import json, collections, datetime
txns = json.load(open("txns.json"))

# Group by vendor name (loose normalization)
by_vendor = collections.defaultdict(list)
for t in txns:
    name = normalize(t['merchant'])  # strip suffixes, lowercase
    by_vendor[name].append(t)

# Detect subscriptions: vendor with ≥3 charges, similar amount, regular cadence
subscriptions = []
for vendor, ts in by_vendor.items():
    if len(ts) < 3: continue
    amounts = [t['amount'] for t in ts]
    if max(amounts) - min(amounts) > 1.0: continue  # too variable
    sorted_ts = sorted(ts, key=lambda t: t['date'])
    gaps = [(sorted_ts[i+1]['date'] - sorted_ts[i]['date']).days for i in range(len(sorted_ts)-1)]
    avg_gap = sum(gaps) / len(gaps)
    if 25 <= avg_gap <= 35:
        cadence = 'monthly'
    elif 360 <= avg_gap <= 370:
        cadence = 'annual'
    else:
        continue
    subscriptions.append({
        "vendor": vendor,
        "amount": ts[-1]['amount'],
        "cadence": cadence,
        "first_seen": sorted_ts[0]['date'],
        "last_seen": sorted_ts[-1]['date'],
        "occurrences": len(ts),
    })

print(f"{len(subscriptions)} subscriptions detected")
```

### Recipe 3: Detect duplicates / overlapping categories

```python
CATEGORIES = {
    'streaming': ['netflix','hulu','disney+','hbo','peacock','paramount+','apple tv+'],
    'cloud': ['dropbox','google one','icloud','onedrive'],
    'notes': ['notion','obsidian','evernote','craft','apple notes'],
    'music': ['spotify','apple music','tidal','youtube music'],
}

for cat, vendors in CATEGORIES.items():
    matches = [s for s in subscriptions if any(v in s['vendor'].lower() for v in vendors)]
    if len(matches) > 1:
        print(f"DUPLICATE in {cat}: {[m['vendor'] for m in matches]}")
        print(f"  Total monthly: ${sum(m['amount'] for m in matches if m['cadence']=='monthly'):.2f}")
```

### Recipe 4: Push to Notion subscription DB

```bash
for s in $subscriptions:
    curl -X POST https://api.notion.com/v1/pages \
      -H "Authorization: Bearer $NOTION_TOKEN" \
      -H "Notion-Version: 2022-06-28" \
      -d '{
        "parent":{"database_id":"<sub-db-id>"},
        "properties":{
          "Vendor":{"title":[{"text":{"content":"'"$s.vendor"'"}}]},
          "Monthly amount":{"number":'"$s.amount"'},
          "Cadence":{"select":{"name":"'"$s.cadence"'"}},
          "Renewal date":{"date":{"start":"'"$next_renewal"'"}}
        }
      }'
```

### Recipe 5: Recommend decision per subscription

```python
for s in subscriptions:
    last_used = look_up(s['vendor'])
    days_unused = (today - last_used).days

    if days_unused > 90:
        decision = "Cancel"
    elif s in duplicates:
        decision = "Cancel (duplicate)"
    elif s['cadence'] == 'monthly' and s['amount'] > 15:
        decision = "Negotiate"
    elif s['amount'] > 50 and 'P1' not in priority:
        decision = "Downgrade"
    else:
        decision = "Keep"
    s['decision'] = decision
```

### Recipe 6: Draft cancellation email

```bash
mcp tool gmail.draft \
  --to "support@vendor.com" \
  --subject "Cancellation request — Account [email]" \
  --body "Hi,

I'd like to cancel my subscription to [Service].

Account email: <user-email>
Customer ID (if known): <id>

Please confirm:
1. Cancellation effective date
2. Final charge amount (if any)
3. Whether any cancellation fee applies

I'd appreciate confirmation in writing.

Thanks,
[Name]"
```

### Recipe 7: Retention-offer counter

If vendor responds with retention offer, draft counter:

```markdown
Hi,

Thanks for the offer. I'd consider staying if:
- $X/month (current is $Y)
- OR downgrading to [tier] at $Z/month

If neither works, please proceed with cancellation.

Thanks,
[Name]
```

### Recipe 8: Direct-cancel URL lookup

Some vendors have direct-cancel URLs (per JustDeleteMe / DoYou Cancel):

```python
DIRECT_CANCEL = {
    'netflix': 'https://www.netflix.com/CancelPlan',
    'spotify': 'https://www.spotify.com/account/subscription/',
    'youtube premium': 'https://www.youtube.com/paid_memberships',
    'dropbox': 'https://www.dropbox.com/account/billing',
    'apple icloud': 'https://www.icloud.com/settings/',
    'amazon prime': 'https://www.amazon.com/mc/prime/cancel',
}

for s in cancel_targets:
    url = DIRECT_CANCEL.get(s['vendor'].lower())
    if url: print(f"Cancel {s['vendor']} directly: {url}")
    else: # Recipe 6 outreach
        pass
```

### Recipe 9: Track cancellation outcome

```bash
# Update Notion entry post-cancel
curl -X PATCH https://api.notion.com/v1/pages/<page-id> \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -d '{
    "properties":{
      "Status":{"select":{"name":"Cancelled"}},
      "Notes":{"rich_text":[{"text":{"content":"Cancelled 2026-06-10; confirmation #ABC123"}}]}
    }
  }'
```

### Recipe 10: Annual savings summary

```python
total_cancelled = sum(s['annual'] for s in subscriptions if s['decision']=='Cancel')
total_negotiated = sum((s['annual_pre'] - s['annual_post']) for s in subscriptions if s['decision']=='Negotiate' and s.get('annual_post'))
print(f"Cancelled: ${total_cancelled}/yr")
print(f"Negotiated savings: ${total_negotiated}/yr")
print(f"Total saved: ${total_cancelled + total_negotiated}/yr")
```

### Recipe 11: Quarterly review reminder

```bash
mcp tool google-calendar.create_event \
  --summary "Subscription Audit Q3" \
  --start "2026-09-01" \
  --end "2026-09-01" \
  --all-day true \
  --recurrence "RRULE:FREQ=YEARLY;BYMONTH=1,4,7,10;BYMONTHDAY=1"
```

## Examples

### Example 1: New user audit

**Goal:** User wants to know what they're paying for + what to cut.

**Steps:**
1. Recipe 1: pull 12 months from Actual Budget.
2. Recipe 2: detect 18 subscriptions.
3. Recipe 3: identify 3 duplicates (Netflix + Hulu + Disney+; Dropbox + Google One; Notion + Obsidian).
4. Recipe 4: surface for last-used input.
5. Recipe 6: agent recommends:
   - Cancel Hulu ($14.99/mo unused 4 months)
   - Cancel Google One ($1.99/mo redundant)
   - Negotiate Comcast ($75 → $55 offered, push to $50)
   - Downgrade Spotify family ($16) → individual ($10)
6. Recipe 8 / 7: surface direct-cancel + draft outreach.
7. Recipe 5: log to Notion.
8. Recipe 11: schedule quarterly.

**Result:** $324/yr savings identified.

### Example 2: Single cancellation

**Goal:** User says "cancel my New York Times."

**Steps:**
1. Recipe 8: direct-cancel URL https://help.nytimes.com/cancel.
2. Recipe 6: draft outreach as fallback.
3. Recipe 9: update Notion post-confirm.

**Result:** Cancelled with confirmation tracked.

### Example 3: Annual review with negotiation

**Goal:** Annual review; want to renegotiate phone + internet.

**Steps:**
1. Pull current rate from Actual Budget.
2. Research competitor offers.
3. Recipe 7: draft retention-offer counter.
4. Submit to vendor.
5. Track outcome.

**Result:** Phone $80 → $60; internet $75 → $55 = $480/yr saved.

## Edge cases / gotchas

- **Vendor name normalization**: "NETFLIX.COM" vs "Netflix Inc." Same vendor. Need fuzzy match.
- **Variable amount subscriptions**: AWS / GCP vary monthly — don't auto-flag as subscription.
- **Annual-pay vs monthly**: Annual subscriptions look like 1 charge/year — easy to miss in monthly scan. Recipe 2 catches with 360-370 day gap.
- **Family-shared**: Spotify Family, Netflix multi-screen, iCloud Family. Don't cancel if family using it.
- **Bundled subscriptions**: Disney+ + Hulu + ESPN+ bundle. Treat as one. Surface to user.
- **Trial periods auto-rolling**: Detect 30-day-free → first paid charge pattern.
- **Negotiation timing**: Negotiate before renewal, not after charge. Set Recipe 11 reminder before renewal date.
- **Retention-offer false ceiling**: First offer is rarely final. Push back politely once.
- **Cancellation requires phone call** (Comcast, gym memberships): Surface phone number + script.
- **Dark-pattern cancellation flows**: Some vendors hide cancel button. Use JustDeleteMe (https://justdeleteme.xyz/) as reference.
- **Gift subscriptions**: Sometimes shows on card. Don't auto-cancel — verify with giftor.
- **Tax-deductible subscriptions**: Adobe / GitHub / etc. may be Schedule C. Tag separately.
- **Rocket Money / Bobby limitations**: Auto-cancel has 30-50% success rate; Bobby Pro $0.99/mo iOS-only for quick view, not analysis. Hard-to-cancel needs manual outreach + escalation.
- **YNAB vs Actual vs Lunch Money**: All work for Recipe 1. YNAB has zero-based budgeting; Actual is OSS; Lunch Money is most modern UI.

## Sources

- [Rocket Money](https://www.rocketmoney.com/)
- [Bobby (iOS)](https://apps.apple.com/app/bobby-budget-subscriptions/id1080524953)
- [Lunch Money](https://www.lunchmoney.app/)
- [YNAB](https://www.ynab.com/)
- [Actual Budget](https://actualbudget.com/)
- [JustDeleteMe](https://justdeleteme.xyz/)
- [Trim / Hiatus (negotiation)](https://www.hiatusapp.com/)
