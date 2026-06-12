<!--
Source: https://hypeauditor.com/
AQS score model: https://hypeauditor.com/blog/hypeauditor-fake-followers-detection/
ContentGrip — 81% of marketers encountered fraud last 12 months: https://www.contentgrip.com/influencer-marketing-fraud-detection/
-->
# Influencer Fraud Detection — HypeAuditor AQS — SKILL

Every creator outreach passes HypeAuditor AQS (Audience Quality Score) 1-100 gate before brief send. Reject AQS < 70. HypeAuditor uses 53+ behavioral patterns trained on 1B+ Instagram / TikTok / YouTube profiles. 95%+ fraud detection rate. 81% of marketers encountered influencer fraud in last 12 months (ContentGrip 2026). Reject anything below threshold no matter the follower count.

## When to use this skill

- **Every influencer match** from `influencer-outreach-modash-aspire-grin`.
- **Quarterly audit** of contracted creators in current programs.
- **Post-publish audit** of campaign performance — fraud-aware ROAS calculation.
- **Pre-acquisition due diligence** on creator agency / influencer roster.

**Do NOT use this skill when:**
- Discovery itself — that's Modash + audience filtering. Fraud check comes AFTER discovery.
- Vetting brand accounts (not influencers) — use `social-listening-brandwatch-mention-talkwalker` for sentiment + reach.

## Setup

### HypeAuditor API

```bash
export HYPEAUDITOR_KEY="<key>"
# Endpoint: https://api.hypeauditor.com/v1/
# Pricing: Pay-per-report or subscription tier
# Single report: $7 / Bulk pack: $5/report at 100+ / Pro plan: unlimited $399+/mo
```

### Modash Fallback (lighter fraud screen)

```bash
# Already configured in influencer-outreach-modash-aspire-grin
# Modash returns: real_followers_pct, mass_followers_pct, suspicious_pct
```

### Notion Vetting Log

Columns: `Handle / Platform / AQS / Audience-authenticity% / Real-followers% / Mass-follower% / Suspicious% / Avg-likes-authentic% / Engagement-rate-authentic / Brand-safety / Decision (approve/reject/borderline) / Decision date / Override reason`.

## Common recipes

### Recipe 1: AQS check single handle

```bash
curl -G https://api.hypeauditor.com/v1/instagram/account \
  -H "Authorization: Bearer $HYPEAUDITOR_KEY" \
  --data-urlencode "username=creator_handle"
```

Returns:
```json
{
  "data": {
    "username": "creator_handle",
    "aqs": 78,
    "audience_quality": {
      "real_followers_pct": 72,
      "mass_followers_pct": 14,
      "suspicious_pct": 10,
      "influencers_pct": 4
    },
    "engagement_rate_total": 3.4,
    "engagement_rate_authentic": 2.8,
    "audience_breakdown": {
      "country": {"US":0.62,"UK":0.12,"CA":0.07},
      "age": {"18-24":0.35,"25-34":0.42,"35-44":0.15},
      "gender": {"female":0.61,"male":0.38}
    },
    "brand_safety": {"score":85, "flags":[]}
  }
}
```

### Recipe 2: Apply AQS gate (per role.md threshold)

```python
def aqs_decision(aqs_data):
    aqs = aqs_data['aqs']
    if aqs >= 80: return ('approve', 'strong default-include')
    if aqs >= 70: return ('approve', 'viable, monitor authenticity')
    return ('reject', f'AQS {aqs} below 70 threshold — bot/mass-follower/growth-trick farm risk')

# Per role.md:
# AQS 90+ : premium
# AQS 80-89: strong
# AQS 70-79: viable
# AQS <70 : REJECT
```

### Recipe 3: Bulk vetting

```python
candidates = notion.query(crm_db, filter={'Status':'sourced','AQS': None})
for c in candidates:
    if c['Followers'] > 100_000_000:
        continue  # mega-celeb, separate manual review
    try:
        aqs_data = hypeauditor.check(handle=c['Handle'], platform=c['Platform'].lower())
        decision, reason = aqs_decision(aqs_data['data'])
        
        notion.update(c['id'], {
            'AQS': aqs_data['data']['aqs'],
            'Real-followers%': aqs_data['data']['audience_quality']['real_followers_pct'],
            'Mass-follower%': aqs_data['data']['audience_quality']['mass_followers_pct'],
            'Suspicious%': aqs_data['data']['audience_quality']['suspicious_pct'],
            'Engagement-rate-authentic': aqs_data['data']['engagement_rate_authentic'],
            'Brand-safety': aqs_data['data']['brand_safety']['score'],
            'Decision': decision,
            'Decision date': today(),
            'Status': 'vetted' if decision == 'approve' else 'rejected'
        })
    except HypeAuditorAPIError as e:
        notion.update(c['id'], {'Decision':'borderline', 'Override reason':f"API error: {e}"})
```

### Recipe 4: Secondary signals (anti-fraud)

Even with AQS ≥ 70, manually flag:

```python
def secondary_flags(aqs_data):
    flags = []
    er_authentic = aqs_data['engagement_rate_authentic']
    er_total = aqs_data['engagement_rate_total']
    if (er_authentic / er_total) < 0.6:
        flags.append('engagement-rate gap — likely engagement pod or comment bots')
    if aqs_data['audience_quality']['mass_followers_pct'] > 25:
        flags.append('mass-followers > 25% — quality dilution')
    
    if 'audience_country' in aqs_data:
        max_country = max(aqs_data['audience_country'].values())
        if max_country < 0.20:
            flags.append('audience too dispersed — no geographic lock')
    
    if aqs_data['brand_safety']['score'] < 70:
        flags.append(f"brand-safety flags: {aqs_data['brand_safety']['flags']}")
    
    return flags
```

### Recipe 5: Audience-match audit (campaign-specific)

```python
def audience_match(aqs_data, target):
    breakdown = aqs_data['audience_breakdown']
    country_match = breakdown['country'].get(target['country'], 0)
    age_match = sum(breakdown['age'].get(a, 0) for a in target['age_buckets'])
    gender_match = breakdown['gender'].get(target['gender'], 0) if target['gender'] != 'all' else 1
    
    score = (country_match + age_match + gender_match) / 3
    return {
        'score': score,
        'country_match': country_match,
        'age_match': age_match,
        'gender_match': gender_match,
        'qualified': country_match > 0.6 and age_match > 0.5 and gender_match > 0.5
    }
```

### Recipe 6: Growth-trick farm detection

Sudden follower jumps + low engagement = bought followers.

```python
# HypeAuditor's growth history endpoint
curl -G https://api.hypeauditor.com/v1/instagram/account/growth \
  -H "Authorization: Bearer $HYPEAUDITOR_KEY" \
  -d "username=creator" \
  -d "period=12months"

# Look for spikes >10% in single month without corresponding engagement spike
def growth_trick_detection(growth_history):
    flags = []
    for i in range(1, len(growth_history)):
        prev = growth_history[i-1]
        curr = growth_history[i]
        follower_growth = (curr['followers'] - prev['followers']) / max(prev['followers'], 1)
        eng_growth = (curr['avg_engagement'] - prev['avg_engagement']) / max(prev['avg_engagement'], 1)
        if follower_growth > 0.10 and eng_growth < 0.02:
            flags.append(f"{curr['month']}: followers +{follower_growth*100:.0f}%, engagement only +{eng_growth*100:.0f}%")
    return flags
```

### Recipe 7: TikTok-specific (different patterns than IG)

```bash
curl -G https://api.hypeauditor.com/v1/tiktok/account \
  -H "Authorization: Bearer $HYPEAUDITOR_KEY" \
  -d "username=tt_handle"
```

TikTok ER baseline is higher (5-9% per role.md). Fraud check tunes:
- AQS ≥ 70 still applies
- Engagement rate < 2% on > 100k followers = suspicious (lower than TikTok baseline)
- Comment authenticity > 60% required (TikTok comment-bot epidemic)

### Recipe 8: YouTube creator vetting

```bash
curl -G https://api.hypeauditor.com/v1/youtube/account \
  -H "Authorization: Bearer $HYPEAUDITOR_KEY" \
  -d "username=yt_handle"
```

YouTube fraud signals different — view-count inflation, sub-bot, click-farms:
- AQS ≥ 70
- View-to-subscriber ratio sanity-check (10-30% normal range)
- Watch time + avg view duration via YouTube API cross-check

### Recipe 9: Quarterly contracted-creator audit

```python
# Re-check every contracted creator quarterly
for c in notion.query(crm_db, filter={'Status': 'shipping'}):
    new_aqs = hypeauditor.check(handle=c['Handle'])['data']
    if new_aqs['aqs'] < 70:
        slack.post('#influencer-program',
            f"⚠ AQS drop: @{c['Handle']} was {c['AQS']}, now {new_aqs['aqs']}. Review contract.")
        notion.update(c['id'], {'AQS': new_aqs['aqs'], 'Status': 'borderline-review'})
```

### Recipe 10: Override workflow

For mid-tier creators where AQS sits at 65-69, manual override allowed with documented reason:

```python
def override(handle, current_aqs, reason, approver_email):
    notion.update_page(handle_to_notion_id(handle), {
        'AQS': current_aqs,
        'Decision': 'approve',
        'Override reason': f"{reason} | approved by {approver_email} on {today()}"
    })
    audit_log.append(handle=handle, decision='override_approve',
                     aqs=current_aqs, reason=reason, approver=approver_email)
```

## Examples

### Example A: 50-creator shortlist vetting

```yaml
input: 50 candidates from Modash search
pipeline:
  step_1: HypeAuditor AQS pull (50 reports = $250 at $5/each Pro)
  step_2: Apply gate (>=70 = approve, <70 = reject)
  step_3: Secondary flags review (recipe 4)
  step_4: Audience-match score (recipe 5)
output:
  - 32 approved (AQS >=70 + audience-match >0.6)
  - 11 borderline (AQS 65-69 — manual override consideration)
  - 7 rejected (AQS <65 OR brand-safety <70)
```

### Example B: Suspicious creator deep-dive

```yaml
handle: '@suspicious_creator'
aqs: 58
findings:
  - real_followers: 45%, mass_followers: 38%, suspicious: 12% (3% influencer)
  - engagement_rate_total: 4.2% but engagement_rate_authentic: 1.1%
  - growth_history: +18k followers in March 2026, engagement flat → buy-burst suspected
  - audience_country: 22% Bangladesh, 18% Indonesia, 12% Brazil — incoherent geo for US-targeted brand
decision: reject (no override approved)
```

### Example C: Quarterly contracted-creator drift

```yaml
program: spring_2026
quarterly_check:
  - 12 creators initially approved AQS 78-92
  - Q2 re-check: 1 dropped to 64 (over-monetized, audience disengaged)
  - action: pause @creator-X, exit contract at end of current cycle
```

## Edge cases

### HypeAuditor cost at scale
500 reports/mo = $2500-$3500. For >100 reports/mo, Pro plan ($399+/mo, unlimited) breaks even.

### Cross-platform same creator
Same handle on IG + TikTok + YouTube needs 3 separate reports. Use platform with highest budget allocation as gate.

### False-positive on rapid organic growth
Genuine viral creator may have +30%/month spikes. Cross-check viral post URLs from growth window — if viral content is verifiable, override allowed.

### New creator (< 10k followers)
HypeAuditor may have limited history. AQS may be conservative-low. For nano tier (<10k), allow Modash-only check + smaller test budget.

### Mid-tier follower count + low ER
A 200k account with 0.5% ER may be legit B2B niche where engagement is naturally low. Industry-context override: B2B SaaS, finance, healthcare often have lower-than-baseline ER.

### Mega-celebrity (>10M followers)
AQS at >10M tier averages 50-70 (real audience has high mass-follower count by nature). Lower threshold OK (e.g., AQS ≥ 60) but require manual brand-safety check + tier-specific contract terms.

### Brand-safety flag types
- "controversial topic" — flags posts referencing protest, religion, politics
- "explicit language" — > 5% posts contain profanity
- "endorsement gaps" — past undisclosed sponsored content (FTC risk)
- "competitor mention" — recent competitor promotion

Per category, decide tolerance.

### Time-series fraud (engagement pod cycles)
Some creators cycle in/out of engagement pods. ER may swing month-to-month. Take 6-month rolling average; don't gate on single month.

### Geographic discount
Markets with high bot prevalence (e.g., some Southeast Asia markets) — AQS thresholds 10pts lower (60 vs 70) per role.md override allowance, with explicit annotation.

### Vetting cost vs creator value
A $200 micro-creator vetting cost $5 = 2.5%. A $50k macro vet at $5 = 0.01%. Always vet macro+ tier; nano tier optional batch-vet at lower threshold (AQS ≥ 65).

### Modash audience-quality cross-check
Modash returns lower-confidence fraud-screen signals. Use Modash to filter before paying for HypeAuditor on bulk shortlist. After Modash filter, only top 30% should hit HypeAuditor.

### Audience inflation post-contract
Some creators buy followers AFTER signing. Quarterly re-check (Recipe 9) catches; contract should reserve right to terminate on AQS drop > 15pts.

### Disclosure compliance audit
Check past 90 days posts for missing #ad / #sponsored tags. HypeAuditor flags brand-mention posts; manually verify disclosure. Penalty: pull from program.

## Sources

- **HypeAuditor**: https://hypeauditor.com/
- **HypeAuditor fake-follower detection blog**: https://hypeauditor.com/blog/hypeauditor-fake-followers-detection/
- **HypeAuditor AQS methodology**: https://hypeauditor.com/about/methodology/
- **ContentGrip — 81% influencer fraud rate 2026**: https://www.contentgrip.com/influencer-marketing-fraud-detection/
- **Modash fraud screen (Discovery API)**: https://www.modash.io/influencer-marketing-api/discovery
- **FTC disclosure rules**: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- **Role.md "Influencer outreach playbook" — AQS gate threshold**
