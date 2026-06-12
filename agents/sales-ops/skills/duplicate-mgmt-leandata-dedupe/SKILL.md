<!--
Source: https://docs.leandata.com/dedup + https://cloudingo.com/ + https://www.validity.com/products/dupeblocker/
Duplicate management — LeanData Dedup + Cloudingo + DupeBlocker (June 2026 SOTA).
-->
# Duplicate Management — LeanData Dedup + Cloudingo + DupeBlocker — SKILL

Daily dedup scans with fuzzy matching (email + phone + domain + normalized name). LeanData Dedup (Salesforce-native), Cloudingo (Salesforce-native, mature), DupeBlocker (Validity), HubSpot built-in deduper. Match score thresholds → auto-merge above threshold, human-review queue 75-90%, suppress < 75%. Custom Python fallback via rapidfuzz when no paid tool.

## When to use

- **Daily dedup scan** — sweep new leads/contacts for duplicates.
- **Auto-merge high-confidence matches** — same email or email+phone.
- **Human-review queue** — fuzzy name + domain matches in 75-90% range.
- **Manual fuzzy match batch** — backlog cleanup via Python.
- **Tune thresholds** — too many false positives? Too many misses?
- **Trigger phrases**: "dedupe leads", "duplicate scan", "merge duplicates", "fuzzy match", "Cloudingo", "LeanData Dedup", "dupe queue".

Do NOT use this skill for: **lead routing** (use `lead-routing-leandata-chili-piper`); **enrichment** (use `data-enrichment-zoominfo-apollo-clay`); **account hierarchy** (use `contact-account-hierarchy-maintenance`).

## Setup

```bash
# Salesforce — standard auth
sf org login web --alias prod

# Cloudingo — API key (Settings → Cloudingo API)
export CLOUDINGO_API_KEY="<key>"
export CLOUDINGO_BASE="https://api.cloudingo.com/v3"

# LeanData Dedup — Salesforce-native; no separate API
# DupeBlocker (Validity) — admin via Salesforce UI

# HubSpot built-in dedup — Operations Hub
export HUBSPOT_PRIVATE_APP_TOKEN="<token>"

# Python deps for custom fuzzy
pip install pandas rapidfuzz phonenumbers
```

Required:
- Cloudingo: paid (~$500-3000/mo by volume)
- LeanData Dedup: bundled with LeanData routing
- DupeBlocker: paid by Validity (~$1K-5K/yr)
- HubSpot Operations Hub Pro for built-in dedup tools

## Common recipes

### Recipe 1: Fuzzy match threshold matrix (canonical)

```
Email exact match              → 100% confidence → auto-merge
Email + phone exact match      → 100%            → auto-merge
Normalized name (Levenshtein < 2) + domain exact → 95% → auto-merge
Normalized name + phone exact (no email)         → 90% → auto-merge
Normalized name (Levenshtein < 3) + same city + same employer → 75% → human-review
Normalized name only           → < 50%           → suppress (likely twin / common name)
```

Apply via Cloudingo Rules, LeanData Dedup Match Nodes, or custom Python (Recipe 5).

### Recipe 2: Salesforce native Duplicate Rule (no paid tool)

```xml
<!-- force-app/main/default/duplicateRules/Lead.Duplicate_Email.duplicateRule-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<DuplicateRule xmlns="http://soap.sforce.com/2006/04/metadata">
    <actionOnInsert>Block</actionOnInsert>
    <actionOnUpdate>Block</actionOnUpdate>
    <isActive>true</isActive>
    <masterLabel>Block Duplicate Email Leads</masterLabel>
    <operationsOnInsert>
        <allowSave>false</allowSave>
        <alertText>A Lead with this email already exists.</alertText>
        <reportDuplicates>true</reportDuplicates>
    </operationsOnInsert>
    <matchingRules>
        <matchingRule>Email_Match_Rule</matchingRule>
    </matchingRules>
</DuplicateRule>
```

Deploy via SFDX:
```bash
sf project deploy start --target-org prod \
  --source-dir force-app/main/default/duplicateRules/
```

### Recipe 3: Cloudingo dedup job trigger

```bash
# List existing dedup jobs
curl "$CLOUDINGO_BASE/jobs" -H "Authorization: Bearer $CLOUDINGO_API_KEY"

# Trigger a job (configured in Cloudingo UI: filter + match rules + action)
curl -X POST "$CLOUDINGO_BASE/jobs/<job_id>/run" \
  -H "Authorization: Bearer $CLOUDINGO_API_KEY"

# Check results
curl "$CLOUDINGO_BASE/jobs/<job_id>/results?limit=100" \
  -H "Authorization: Bearer $CLOUDINGO_API_KEY"
```

### Recipe 4: HubSpot deduper API

```bash
# HubSpot's built-in dedup recommendations
curl "https://api.hubapi.com/crm/v3/objects/contacts/duplicates/preview" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN" \
  | jq '.results[] | {primary_id, duplicate_id, match_score, matched_fields}'

# Auto-merge above threshold
curl -X POST "https://api.hubapi.com/crm/v3/objects/contacts/merge" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"primaryObjectId": "12345", "objectIdToMerge": "12346"}'
```

### Recipe 5: Custom Python fuzzy dedup (no paid tool)

```python
import pandas as pd
from rapidfuzz import fuzz, process
import phonenumbers

leads = pd.read_csv('salesforce_leads.csv')

# Normalize
def normalize_email(e): return (e or "").lower().strip()
def normalize_name(f, l): return f"{(f or '').lower().strip()} {(l or '').lower().strip()}".strip()
def normalize_phone(p, region='US'):
    try:
        n = phonenumbers.parse(p, region)
        return phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164)
    except: return None
def domain_of(e): return (e or "").split("@")[-1].lower() if "@" in (e or "") else ""

leads['email_norm']  = leads['email'].apply(normalize_email)
leads['name_norm']   = leads.apply(lambda r: normalize_name(r['first_name'], r['last_name']), axis=1)
leads['phone_norm']  = leads['phone'].apply(normalize_phone)
leads['email_domain']= leads['email_norm'].apply(domain_of)

# 1) Email exact match → 100% auto-merge candidates
dupes_email = leads[leads.duplicated('email_norm', keep=False) & leads['email_norm'].astype(bool)]
print(f"Email-exact dupes: {dupes_email.shape[0]}")

# 2) Phone exact match (when email missing)
no_email = leads[~leads['email_norm'].astype(bool)]
dupes_phone = no_email[no_email.duplicated('phone_norm', keep=False) & no_email['phone_norm'].astype(bool)]

# 3) Fuzzy name + domain (95% threshold)
candidates = []
for i, row in leads.iterrows():
    if not row['name_norm']: continue
    domain_peers = leads[(leads['email_domain'] == row['email_domain']) & (leads.index != i)]
    for j, peer in domain_peers.iterrows():
        score = fuzz.token_sort_ratio(row['name_norm'], peer['name_norm'])
        if score >= 95:
            candidates.append({
                'a': row['id'], 'b': peer['id'],
                'a_name': row['name_norm'], 'b_name': peer['name_norm'],
                'score': score, 'domain': row['email_domain'],
                'action': 'auto_merge'
            })
        elif 75 <= score < 95 and row['city'] == peer['city']:
            candidates.append({
                'a': row['id'], 'b': peer['id'],
                'a_name': row['name_norm'], 'b_name': peer['name_norm'],
                'score': score, 'domain': row['email_domain'],
                'action': 'human_review'
            })

pd.DataFrame(candidates).drop_duplicates(['a','b']).to_csv('dedup_candidates.csv', index=False)
```

### Recipe 6: Salesforce merge API (after dedup decision)

```bash
# Merge 2 Lead records (master + duplicate)
curl -X POST "https://gateway.maton.ai/salesforce/services/data/v60.0/composite/sobjects/Lead/merge" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "masterRecordId": "00QXX0000123ABC",
    "duplicateRecordIds": ["00QXX0000456DEF"]
  }'

# Merge Contact records (similar pattern)
# Up to 2 duplicates can merge into master in one call
```

### Recipe 7: Human-review queue in Notion

```python
# Render 75-90% confidence matches to Notion for SalesOps reviewer
import requests, os, pandas as pd

candidates = pd.read_csv('dedup_candidates.csv')
review_queue = candidates[candidates['action'] == 'human_review']

notion = requests.Session()
notion.headers.update({"Authorization": f"Bearer {os.environ['NOTION_TOKEN']}",
                       "Notion-Version": "2022-06-28"})

for _, c in review_queue.iterrows():
    notion.post("https://api.notion.com/v1/pages", json={
        "parent": {"database_id": os.environ['DEDUP_DB_ID']},
        "properties": {
            "Match A": {"title": [{"text": {"content": c['a_name']}}]},
            "Match B": {"rich_text": [{"text": {"content": c['b_name']}}]},
            "Score": {"number": int(c['score'])},
            "Domain": {"rich_text": [{"text": {"content": c['domain']}}]},
            "Status": {"select": {"name": "Pending Review"}},
            "Salesforce A": {"url": f"https://salesforce.com/{c['a']}"},
            "Salesforce B": {"url": f"https://salesforce.com/{c['b']}"}
        }
    })
```

### Recipe 8: LeanData Dedup config (no-code)

LeanData Dedup is configured in the LeanData app UI — no API. Pattern:

```
Match Logic:
  - Email Match (exact)               → 100% confidence → Auto-Merge
  - Phone Match (E.164)               → 95% → Auto-Merge
  - Fuzzy Name + Domain               → 85% → Human Review
  - Fuzzy Name + Title + Account      → 75% → Human Review

Merge Master Selection:
  - Prefer record with: more recent activity, more populated fields, owner != null

Excluded Records:
  - Records owned by 'Marketing Automation' (HubSpot/Marketo import)
  - Records in stage 'Closed - Disqualified'
```

Audit via Salesforce reports on the LeanData audit objects.

### Recipe 9: DupeBlocker rule (Salesforce-native)

DupeBlocker config in Salesforce UI under "DupeBlocker Console":

```
Scenario: Block duplicate Account creation
Conditions:
  - Account.Name matches existing (fuzzy 90%)
  - AND Account.BillingCity matches
Action: Block + show alert to user
Allow override: Yes (admin role)
```

### Recipe 10: Weekly dedup accuracy review

```python
# Compare: human reviewer decisions vs automated thresholds
import pandas as pd

audit = pd.read_csv('dedup_audit_last_week.csv')
# columns: candidate_id, auto_action, human_decision, score, match_type

# False positives — auto-merged but human says "different person"
fp = audit[(audit['auto_action']=='auto_merge') & (audit['human_decision']=='unmerge')]
print(f"False positives this week: {len(fp)} / {len(audit[audit['auto_action']=='auto_merge'])}")

# Missed duplicates — suppressed (< 75%) but human found in manual review
fn = audit[(audit['auto_action']=='suppress') & (audit['human_decision']=='merge')]
print(f"Missed dupes: {len(fn)}")

# Tune: if FP > 1% → raise auto-merge threshold to 97%
# Tune: if FN > 5/week in similar pattern → add a new match rule
```

### Recipe 11: Email domain whitelist for high-volume re-orgs

```yaml
# For companies with high turnover (consulting firms, agencies):
# email match alone isn't enough — same email aliased to different humans
domain_whitelist_email_only:
  - none  # default: email match always wins

# For these domains, require email + phone or email + name match:
domain_require_secondary_match:
  - bigconsulting.com  # consultancy with shared client emails
  - agency-bg.com
  - bigtech.com  # shared bots / re-issued addresses

# Apply via Cloudingo conditional rule or Python branching
```

### Recipe 12: Backlog cleanup (one-time fuzzy match all Leads)

```python
# Annual cleanup: scan ALL leads, not just new
import pandas as pd, requests, os
from rapidfuzz import fuzz

# Pull all leads via Salesforce Bulk API
# ...
leads = pd.read_csv('all_leads_export.csv')

# Run Recipe 5 logic over full set
# Render results: auto_merge candidates, human_review queue, suppressed
# Stagger merges: 100/day to avoid Salesforce mass-DML governor limits

merge_queue = leads[...]  # auto_merge results from Recipe 5
for batch in [merge_queue[i:i+100] for i in range(0, len(merge_queue), 100)]:
    for _, pair in batch.iterrows():
        # Recipe 6 merge call
        requests.post(...)
    # Wait 1 day before next batch
```

## Examples

### Example 1: Daily dedup (Cloudingo)

**Goal:** Every day at 6am, scan + auto-merge high-confidence dupes; queue medium for review.

**Steps:**
1. Configure Cloudingo job (UI): filter = "Lead.CreatedDate > LAST_DAY", match rules per Recipe 1.
2. Schedule job daily 6am.
3. Recipe 3 — programmatically check results: count merged + count queued.
4. If queued > 50: Slack alert to SalesOps to clear queue same day.
5. Recipe 10 — weekly review of false-positive rate; tune thresholds quarterly.

**Result:** Lead duplication < 1% steady-state; AEs trust contact records.

### Example 2: Backlog cleanup (no paid tool)

**Goal:** Pre-rollout cleanup before deploying LeanData routing. ~50K leads, unknown dupe rate.

**Steps:**
1. Recipe 12 — bulk-export all leads.
2. Recipe 5 — run Python fuzzy match over full set.
3. Stage in 3 buckets: auto-merge (95%+), human-review (75-94%), suppress (< 75%).
4. Recipe 7 — render review queue to notion; assign reviewer.
5. Approve merges in batches of 100/day via Recipe 6.
6. After 2 weeks: 8% dedup rate, clean dataset ready for LeanData routing.

**Result:** Dedup rate from 8% to < 1%; reps stop seeing duplicate accounts.

### Example 3: Threshold tuning after false-positive complaints

**Goal:** Auto-merge wrongly merged two reps named "Mike Chen" at the same company.

**Steps:**
1. Investigate: both records had same name + same domain → 95% auto-merge.
2. Look at context: different phones, different titles, different start dates.
3. Update Recipe 1 rule: name + domain alone = human-review (not auto-merge); require name + domain + (phone OR title-match) for auto.
4. Recipe 10 — re-run over last 30 days; flag any other suspect auto-merges.
5. Unmerge if necessary (Salesforce: not always possible — record creation order matters).
6. Document threshold rationale in notion.

**Result:** Twin-as-one false positives drop to near zero; trust in dedup restored.

## Edge cases / gotchas

- **Email aliasing** — `name+spam@gmail.com`, `name@firstcorp.com` vs `name@parentcorp.com` post-merger. Normalize cautiously.
- **Salesforce Lead-to-Contact conversion creates apparent dupes** — same person exists as Lead + Contact. Convert Lead first, then dedup Contacts.
- **Multi-byte name issues** — Asian names ("李 明" vs "Li Ming") — Levenshtein on ASCII misses. Use Unicode-aware fuzzy.
- **High turnover companies** (consultancies, agencies) — same email aliased to different people. Require secondary signal.
- **Father-son or twin names** — same name + same company + different person. Suppress < 50% threshold catches some; not all.
- **DupeBlocker / Cloudingo / LeanData write to same audit object?** No — each writes to its own. Audit consolidation needed for full picture.
- **Master record selection** — wrong master (e.g., older but more complete) loses recent data. Define master-selection logic explicitly.
- **Merge is destructive** — Salesforce merge deletes the duplicate; no undo. Be cautious with auto-merge.
- **Lookup field handling on merge** — child records (activities, opportunities) reparent to master. Verify in sandbox.
- **Cloudingo rate limits** — Salesforce Bulk API quotas apply. Large merges chunk to 200 records/call.
- **HubSpot Auto-Merge is one-way** — keeps the older record; can't choose master.
- **GDPR + dedupe** — right-to-be-forgotten requests must hard-delete; merge isn't enough.
- **Cross-object dedup** — same person as Lead + Contact + multiple Contacts under different Accounts. Conversion + cross-object scan needed.
- **Phone normalization country codes** — `+15551234567` vs `(555) 123-4567` is same E.164. `+44...` is UK. Phonenumbers library handles.
- **Cloudingo allows "soft merge"** — both records survive, marked related. Useful for reversible dedup.
- **LinkedIn URL matching** — strong signal but format varies (`linkedin.com/in/name`, `linkedin.com/in/name-123`). Normalize.

## Sources

- [LeanData Dedup documentation](https://docs.leandata.com/dedup)
- [Cloudingo documentation](https://cloudingo.com/help-center/)
- [DupeBlocker (Validity)](https://www.validity.com/products/dupeblocker/)
- [Salesforce Duplicate Rules](https://help.salesforce.com/s/articleView?id=sf.duplicate_rules_map_of_reference.htm)
- [Salesforce Merge API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_composite_sobject_tree.htm)
- [HubSpot Dedup Tools](https://knowledge.hubspot.com/contacts/merge-duplicate-contacts)
- [RapidFuzz Python library](https://maxbachmann.github.io/RapidFuzz/)
- [Phonenumbers library](https://github.com/daviddrysdale/python-phonenumbers)
