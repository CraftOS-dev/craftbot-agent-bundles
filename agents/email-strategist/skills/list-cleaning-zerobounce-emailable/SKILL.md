<!--
Source: ZeroBounce, Emailable, NeverBounce, BriteVerify, Kickbox, DeBounce
Pre-send batch validation + inline signup validation.
-->
# List Cleaning + Verification (ZeroBounce / Emailable / Kickbox) — SKILL

Pre-send list validation removes invalids, catch-alls, spam traps, and role addresses. Inline validation at signup prevents 90% of bounces. Use ZeroBounce / Emailable / NeverBounce / BriteVerify / Kickbox / DeBounce.

## When to use

- "Clean our list before next campaign"
- "Inline validate email at signup form"
- "Our bounce rate is 4% — what to do"
- "Detect spam traps in our list"
- "Validate a 500K-row import before pushing to Klaviyo"

## Setup

```bash
# Pick one (or two for cross-validation on critical lists)
# ZeroBounce  — $0.0065/email at volume, best catch-all + trap detection
# Emailable   — $0.005/email, fast batch
# NeverBounce — $0.008/email, real-time API
# BriteVerify (Validity) — $0.01/email, enterprise FBL data
# Kickbox     — $0.008/email, good API + free 100/day
# DeBounce    — $0.004/email, cheapest
```

Auth:

```bash
export ZEROBOUNCE_API_KEY="<key>"      # https://www.zerobounce.net/members/apikey/
export EMAILABLE_API_KEY="<key>"        # https://app.emailable.com/keys
export NEVERBOUNCE_API_KEY="<key>"      # https://app.neverbounce.com/account/api
export KICKBOX_API_KEY="<key>"
```

## Common recipes

### Recipe 1: ZeroBounce — single-record real-time validation (signup form)

```bash
curl -s "https://api.zerobounce.net/v2/validate?api_key=$ZEROBOUNCE_API_KEY&email=user@example.com&ip_address=" | jq
```

Returns:
```json
{
  "address": "user@example.com",
  "status": "valid",
  "sub_status": "",
  "free_email": false,
  "did_you_mean": null,
  "account": "user",
  "domain": "example.com",
  "domain_age_days": "9210",
  "smtp_provider": "google",
  "mx_record": "aspmx.l.google.com",
  "mx_found": "true",
  "firstname": null,
  "lastname": null
}
```

Status taxonomy:
- `valid` — accept
- `invalid` — reject (does not exist)
- `catch-all` — accept with caution (cannot verify; some domains accept all)
- `spamtrap` — reject + log (known trap)
- `abuse` — reject (known complainer)
- `do_not_mail` — reject (role address, complainer, blacklist)
- `unknown` — temporarily failed verification; recheck later

### Recipe 2: ZeroBounce — batch (sendfile API)

```bash
# Submit a CSV with email column
curl -X POST "https://bulkapi.zerobounce.net/v2/sendfile" \
  -F "api_key=$ZEROBOUNCE_API_KEY" \
  -F "file=@subscribers.csv" \
  -F "email_address_column=1" \
  -F "return_url=https://brand.com/webhooks/zerobounce"

# Returns file_id; poll status
curl "https://bulkapi.zerobounce.net/v2/filestatus?api_key=$ZEROBOUNCE_API_KEY&file_id=<file-id>" | jq

# Download results when complete
curl "https://bulkapi.zerobounce.net/v2/getfile?api_key=$ZEROBOUNCE_API_KEY&file_id=<file-id>" \
  -o results.csv
```

### Recipe 3: Emailable — batch

```bash
# Submit
BATCH_ID=$(curl -X POST "https://api.emailable.com/v1/batch" \
  -H "Authorization: Bearer $EMAILABLE_API_KEY" \
  -d '{"emails":["a@example.com","b@example.com",...]}' | jq -r '.id')

# Poll
curl "https://api.emailable.com/v1/batch/$BATCH_ID" \
  -H "Authorization: Bearer $EMAILABLE_API_KEY" | jq

# Results when complete
curl "https://api.emailable.com/v1/batch/$BATCH_ID/results" \
  -H "Authorization: Bearer $EMAILABLE_API_KEY" | jq '.emails[] | {email, state, reason}'
```

### Recipe 4: NeverBounce — real-time single

```bash
curl -X POST "https://api.neverbounce.com/v4/single/check" \
  -d "key=$NEVERBOUNCE_API_KEY&email=user@example.com&address_info=1&credits_info=1"
```

### Recipe 5: Inline validation at signup

JS snippet for forms (rejects typos + invalid addresses at form-submit):

```html
<form id="signup" onsubmit="return validateAndSubmit(event)">
  <input type="email" id="email" required />
  <button type="submit">Sign up</button>
</form>

<script>
async function validateAndSubmit(e) {
  e.preventDefault();
  const email = document.getElementById('email').value;

  // Pre-validate via your backend (proxies ZeroBounce — never expose key client-side)
  const r = await fetch('/api/validate-email', {
    method: 'POST',
    body: JSON.stringify({email}),
    headers: {'Content-Type':'application/json'}
  });
  const result = await r.json();

  if (result.status === 'invalid' || result.status === 'spamtrap' || result.status === 'do_not_mail') {
    alert('Please enter a valid email address.');
    return false;
  }
  if (result.did_you_mean) {
    if (!confirm(`Did you mean ${result.did_you_mean}?`)) return false;
  }

  // Proceed with signup
  document.getElementById('signup').submit();
}
</script>
```

Backend proxy:

```python
from flask import request, jsonify
import requests, os

@app.post('/api/validate-email')
def validate():
    email = request.json['email']
    r = requests.get(
        'https://api.zerobounce.net/v2/validate',
        params={'api_key': os.environ['ZEROBOUNCE_API_KEY'], 'email': email}
    )
    return jsonify(r.json())
```

### Recipe 6: Cross-validation for high-stakes lists

For high-volume imports (>100K from new source), validate via TWO services + suppress anything either flags:

```python
import requests

def validate_dual(email):
    zb = requests.get('https://api.zerobounce.net/v2/validate', params={'api_key': ZB_KEY, 'email': email}).json()
    em = requests.post('https://api.emailable.com/v1/verify', headers={'Authorization': f'Bearer {EM_KEY}'}, json={'email': email}).json()
    safe = (zb.get('status') == 'valid') and (em.get('state') == 'deliverable')
    return safe, {'zerobounce': zb.get('status'), 'emailable': em.get('state')}
```

### Recipe 7: Push validated list to Klaviyo

```python
import requests, csv, os

KLAVIYO_KEY = os.environ['KLAVIYO_API_KEY']

with open('zerobounce_results.csv') as f:
    rows = csv.DictReader(f)
    valid_emails = [r['email'] for r in rows if r['status'] == 'valid']

# Bulk import as subscribed profiles
chunks = [valid_emails[i:i+100] for i in range(0, len(valid_emails), 100)]
for chunk in chunks:
    requests.post(
        'https://a.klaviyo.com/api/profile-subscription-bulk-create-jobs',
        headers={'Authorization': f'Klaviyo-API-Key {KLAVIYO_KEY}', 'revision': '2024-10-15', 'Content-Type': 'application/json'},
        json={
            'data': {
                'type': 'profile-subscription-bulk-create-job',
                'attributes': {
                    'profiles': {'data': [{'type':'profile','attributes':{'email':e,'subscriptions':{'email':{'marketing':{'consent':'SUBSCRIBED'}}}}} for e in chunk]},
                    'custom_source': 'zerobounce-validated-import'
                }
            }
        }
    )
```

### Recipe 8: Per-validation cost calculator

```python
def cost(list_size, service='zerobounce'):
    rates = {'zerobounce': 0.0065, 'emailable': 0.005, 'neverbounce': 0.008,
             'briteverify': 0.01, 'kickbox': 0.008, 'debounce': 0.004}
    return list_size * rates[service]

# 500K list cleanup
print(f"ZeroBounce: ${cost(500_000, 'zerobounce'):,.0f}")  # $3,250
print(f"Emailable: ${cost(500_000, 'emailable'):,.0f}")    # $2,500
print(f"DeBounce: ${cost(500_000, 'debounce'):,.0f}")      # $2,000
```

### Recipe 9: ZeroBounce AI score (newer feature)

```bash
curl "https://api.zerobounce.net/v2/scoring?api_key=$ZEROBOUNCE_API_KEY&email=user@example.com"
```

Returns 0-10 score (10 = highly deliverable, 0 = highly risky). Useful for catch-all addresses that can't be conclusively validated.

### Recipe 10: Suppress at ESP

```python
# Push invalid + spamtrap + do_not_mail to Klaviyo suppression
import requests

for email, status in invalid_rows:
    requests.post(
        'https://a.klaviyo.com/api/profile-suppression-bulk-create-jobs',
        headers={'Authorization': f'Klaviyo-API-Key {KLAVIYO_KEY}', 'revision':'2024-10-15'},
        json={'data':{'type':'profile-suppression-bulk-create-job','attributes':{
            'profiles':{'data':[{'type':'profile','attributes':{'email':email}}]},
            'reason':f'List-validation: {status}'
        }}}
    )
```

## Examples

### Example 1: Pre-launch full-list clean for 500K subscribers

**Goal:** before next major campaign, clean list to reduce bounce + complaint risk.

**Steps:**

1. Export list from Klaviyo: `list_profiles` with engagement metadata.
2. Filter to validate-worthy:
   - All addresses (including engaged) — sanity
   - OR engaged-only (cost saving) — but spam traps hide there too
3. Submit batch to ZeroBounce (Recipe 2).
4. Wait ~30 min for 500K results.
5. Categorize:
   - `valid` (~85% expected) → keep
   - `invalid` (~5%) → suppress
   - `catch-all` (~5%) → optionally keep with caution flag
   - `spamtrap` (~0.1%) → suppress immediately + investigate source
   - `do_not_mail` (~5%) → suppress
6. Push suppression list to Klaviyo (Recipe 10).
7. Send next campaign with improved bounce rate (target <2%).

### Example 2: Inline validation at signup

**Goal:** prevent invalid signups from entering list.

**Steps:**

1. Backend proxy validate endpoint (Recipe 5).
2. Frontend hook on form submit — validate before POST to your signup endpoint.
3. Handle typo suggestions: ZeroBounce returns `did_you_mean` for common typos (gmial.com → gmail.com).
4. Reject `invalid` / `spamtrap` / `do_not_mail` outright.
5. Log catch-all + unknown — flag profile but accept; suppress later if bounces.
6. Reduce bounce rate from 4% to <0.5% within 30 days.

## Edge cases

- **Catch-all domains** (often corporate) accept all incoming mail without signaling validity. Cannot be conclusively validated. Send anyway and watch for bounces, OR exclude from imports if list quality matters more than reach.
- **Disposable email domains** (mailinator, guerrillamail, 10minutemail) — ZeroBounce flags via `free_email: true + smtp_provider: <known-disposable>`. Block these at signup.
- **Spam traps** are seeded addresses by ISPs (Spamhaus, etc.) — hitting one triggers a reputation hit. Validators catch known traps but not all. Cross-validate for high-risk lists.
- **Role addresses** (info@, admin@, support@) — almost always lead to complaints when sent marketing. Suppress entirely.
- **Cost** — $0.005-$0.01 per record at scale ($2,500-$5,000 for 500K). Negotiate at >1M volume.
- **Privacy** — sending emails to a third party validator is processing PII; ensure DPA / GDPR coverage. ZeroBounce / Emailable / NeverBounce are SOC2 + GDPR compliant.
- **Re-validation cadence** — validate full list quarterly; validate inactive subset semi-annually. Don't validate "engaged 30d" — they're already validated by real engagement.
- **Hard-bounce after validation** is uncommon but happens — addresses can go invalid between validation and send. Always re-suppress on bounce regardless of validation.
- **Rate limits** — most validators allow 10-50 req/s on real-time API. For higher, use batch.
- **Free tiers** — Kickbox 100/day, NeverBounce 1000 lifetime, Emailable 250 free. Test before committing.

## Sources

- [ZeroBounce API](https://www.zerobounce.net/v2/documentation/)
- [Emailable API](https://emailable.com/docs/api/)
- [NeverBounce API](https://developers.neverbounce.com/)
- [BriteVerify API](https://docs.briteverify.com/)
- [Kickbox API](https://docs.kickbox.com/)
- [DeBounce API](https://docs.debounce.io/)
- [Klaviyo bulk subscription job](https://developers.klaviyo.com/en/reference/bulk_subscribe_profiles)
- [Klaviyo suppression](https://developers.klaviyo.com/en/reference/suppress_profiles)
