<!--
Source: https://www.madgicx.com/blog/facebook-ad-fatigue
Source: https://revealbot.com/blog/facebook-dayparting
Ad fatigue detection + rotation via thresholds and automation rules.
-->
# Ad Fatigue Rotation Strategy — SKILL

Creative fatigue silently burns 20-40% of spend at scale. This skill encodes the thresholds (frequency, CPM rise, CTR decline, hook retention) + the auto-rotation rules (Madgicx / Revealbot / custom Python on `postgresql-mcp` warehouse) + the Slack alert wiring to keep the matrix fresh.

## When to use this skill

- **Always-on monitoring** — daily / hourly check on active campaigns.
- **Scale event** — fatigue compounds faster at higher spend.
- **Long-running creative** — >2 weeks live with no refresh.
- **Audience exhaustion** — small audience pool burns frequency fast.
- **Frequency / CPM rise alert** triggered.

**Do NOT use this skill when:**
- New campaign (<7d) — too noisy for fatigue read.
- Brand awareness with high frequency goal (frequency is the point, not a problem).

## Setup

### Fatigue thresholds (2026 SOTA)

| Signal | Threshold | Action |
|---|---|---|
| Frequency (7d window, prospecting) | > 2.5 | Rotate within 48h |
| Frequency (7d, retargeting) | > 4.0 | Rotate / pause + warm-cycle |
| CPM week-over-week | +30% | Investigate; rotate if creative-attributed |
| CTR week-over-week | -25% | Rotate within 48h |
| Hook retention 3s (video) | -20% from launch | New hook variant |
| CPA week-over-week | +20% | Combined diagnosis (creative / audience / offer) |
| Reach decay (DAU served) | -40% week-over-week | Audience exhausted; expand or rotate |

### Tools

- **Madgicx** — Meta-specialized, fatigue detector built in; $99-499/mo
- **Revealbot** — cross-platform (Meta + Google + TikTok); $99+/mo; native rule engine
- **Custom Python on `postgresql-mcp`** — free, max control, requires warehouse + cron
- **Meta's own "Ads Performance" tab** — surfaces high-frequency ads; manual

### Slack alert config

```bash
export SLACK_WEBHOOK_URL="<webhook-from-#ads-alerts>"
```

## Common recipes

### Recipe 1: SQL on postgresql-mcp — fatigue detection daily

```sql
WITH today AS (
  SELECT ad_id, ad_name, frequency, ctr, cpm
  FROM ads_warehouse.daily_ad_metrics
  WHERE date = CURRENT_DATE - 1
),
week_ago AS (
  SELECT ad_id, AVG(ctr) AS ctr_avg, AVG(cpm) AS cpm_avg, AVG(frequency) AS freq_avg
  FROM ads_warehouse.daily_ad_metrics
  WHERE date BETWEEN CURRENT_DATE - 8 AND CURRENT_DATE - 2
  GROUP BY ad_id
)
SELECT
  t.ad_id, t.ad_name, t.frequency,
  ROUND(t.ctr * 100, 2) AS ctr_pct,
  ROUND(t.cpm, 2) AS cpm,
  ROUND((t.cpm / w.cpm_avg - 1) * 100, 1) AS cpm_delta_pct,
  ROUND((t.ctr / w.ctr_avg - 1) * 100, 1) AS ctr_delta_pct,
  CASE
    WHEN t.frequency > 2.5 THEN 'FATIGUE-HIGH-FREQ'
    WHEN (t.ctr / w.ctr_avg - 1) < -0.25 THEN 'FATIGUE-CTR-DROP'
    WHEN (t.cpm / w.cpm_avg - 1) > 0.30 THEN 'FATIGUE-CPM-RISE'
    ELSE 'OK'
  END AS fatigue_flag
FROM today t
JOIN week_ago w ON t.ad_id = w.ad_id
WHERE 
  t.frequency > 2.5
  OR (t.ctr / w.ctr_avg - 1) < -0.25
  OR (t.cpm / w.cpm_avg - 1) > 0.30
ORDER BY t.frequency DESC;
```

### Recipe 2: Python script — auto-pause + Slack alert

```python
import os, requests, json
from sqlalchemy import create_engine

engine = create_engine(os.environ["DATABASE_URL"])
with engine.connect() as c:
    rows = c.execute("""... query above ...""").fetchall()

for r in rows:
    # Pause via Meta MCP
    requests.post(
      "https://graph.facebook.com/v19.0/" + r.ad_id,
      data={"status": "PAUSED", "access_token": os.environ["META_ACCESS_TOKEN"]})

    # Slack alert
    requests.post(os.environ["SLACK_WEBHOOK_URL"], json={
      "text": f":fire: Ad fatigue paused: {r.ad_name} | Freq={r.frequency:.2f} | CTR Δ={r.ctr_delta_pct}% | CPM Δ={r.cpm_delta_pct}% | Flag: {r.fatigue_flag}",
      "blocks": [
        {"type":"section","text":{"type":"mrkdwn",
          "text": f"*Ad paused due to fatigue*\n• Name: `{r.ad_name}`\n• ID: `{r.ad_id}`\n• Frequency (7d): {r.frequency:.2f}\n• CTR Δ vs 7d avg: {r.ctr_delta_pct}%\n• CPM Δ: {r.cpm_delta_pct}%\n• Flag: {r.fatigue_flag}"}},
        {"type":"actions","elements":[
          {"type":"button","text":{"type":"plain_text","text":"Queue creative refresh"},
           "url": f"https://linear.app/team/new?title=Refresh+{r.ad_name}"}]}
      ]})
```

### Recipe 3: Revealbot rule — auto-pause on fatigue

```yaml
# Configured in Revealbot UI; saving spec for reproducibility
rule:
  name: "Meta — auto-pause high-frequency ads"
  applies_to: all_active_ads_in_prospecting_campaigns
  conditions:
    - metric: frequency
      time_window: last_7_days
      operator: ">"
      value: 2.5
  action: pause
  notification: slack:#ads-alerts

rule_refresh_alert:
  name: "Meta — alert when CTR drops"
  conditions:
    - metric: ctr_change
      compare: previous_7d
      operator: "<"
      value: -25
  action: notify  # no auto-pause; require human review
  notification: slack:#ads-alerts
```

### Recipe 4: Madgicx integration

```
# Madgicx UI setup (no API; document config):
# 1. Connect Meta ad account
# 2. Enable "Ad Fatigue Detector"
# 3. Set thresholds in Madgicx Settings → Automation Rules → Fatigue
#    - Frequency > 2.5: pause
#    - CPC rise > 50%: pause
#    - CTR drop > 30%: pause
# 4. Enable "Auto-Rotation" to swap to fresh creative from staged library
```

### Recipe 5: Manual weekly fatigue audit

```bash
# Pull adset-level frequency + CPM + CTR
mcp tool meta-ads.get_campaign_insights \
  --campaign_id "ALL" \
  --level "ad" \
  --metrics '["frequency","cpm","ctr","ctr_unique"]' \
  --date_preset "last_7d" \
  --breakdowns '[]' > weekly-fatigue.json

jq '.data[] | select(.frequency > 2.5 or .ctr < 0.005) | {ad_id, ad_name, freq: .frequency, ctr: .ctr}' weekly-fatigue.json
```

### Recipe 6: Creative refresh queue — Linear / Asana

```python
# When fatigue alert fires, auto-create refresh task in Linear
import requests
def queue_refresh(ad_name, ad_id, fatigue_flag):
    requests.post(
      "https://api.linear.app/graphql",
      headers={"Authorization": os.environ["LINEAR_API_KEY"]},
      json={"query": """
        mutation { issueCreate(input: {
          teamId: "<team-id>",
          title: "Creative refresh: %s",
          description: "Ad ID: %s\\nFatigue type: %s\\nQueued by ads-specialist agent.",
          labelIds: ["refresh","fatigue"]
        }) { success issue { id identifier } } }
      """ % (ad_name, ad_id, fatigue_flag)})
```

### Recipe 7: Hook retention curve from Meta breakdown

```bash
# Meta video view breakdown — 3s vs 25% vs 50% vs 75% vs 100%
mcp tool meta-ads.get_ad_insights \
  --ad_id "$AD_ID" \
  --metrics '["impressions","video_p25_watched_actions","video_p50_watched_actions",
              "video_p75_watched_actions","video_p100_watched_actions","video_play_actions",
              "video_3s_views"]' \
  --date_preset "last_14d"

# Compute 3s view rate = video_3s_views / impressions
# Compare to launch-week baseline. Drop > 20% = hook fatigue.
```

### Recipe 8: Refresh cadence rule per account

```yaml
spend_tier_rules:
  small_account:
    monthly_spend: "<$10K"
    refresh_cadence: monthly (whole library)
  medium:
    monthly_spend: "$10K-50K"
    refresh_cadence: 20% of creative every 2 weeks
  large:
    monthly_spend: ">$50K"
    refresh_cadence: 30% of creative weekly
    auto_rotation: enabled (Madgicx / Revealbot)
```

## Examples — fatigue rotation playbook

```yaml
weekly_routine:
  monday_morning:
    - run: fatigue SQL on postgresql-mcp
    - flag: ads exceeding any threshold
    - slack: post summary to #ads-alerts
  
  monday_action:
    - review flagged ads with team
    - decide: rotate / pause / extend
    - queue refresh tasks in Linear
  
  wednesday_check:
    - re-run SQL; verify pauses took effect
    - confirm Madgicx/Revealbot rules firing
  
  friday_creative_planning:
    - new briefs authored for next week's refresh
    - hand off to designers / video team

monthly_routine:
  audit:
    - full account fatigue scan
    - check refresh cadence vs spend tier rule
    - update Madgicx thresholds if account scaled
```

## Edge cases

### Frequency at adset vs ad level
Meta reports frequency at adset level by default. Drill to ad level via `breakdowns=["ad_id"]` to find which ad in adset is burning.

### Frequency for retargeting is acceptable
Retargeting (hot) frequency can sit at 5-8 without performance harm — the audience opts in to repeat exposure. Apply the prospecting threshold (2.5) only to cold campaigns.

### CPM rise not always fatigue
CPM can rise due to: seasonal auction competition (Black Friday), audience expansion to costlier placements, bid strategy change. Cross-check with reach delta.

### CTR drop not always fatigue
Drop may indicate audience shift (broadened) or platform change. Cross-check with frequency + reach.

### Hook retention vs full-view
A great hook + bad mid-roll = high 3s view rate but low 25%+ view rate. Diagnose where the drop happens; rotate accordingly.

### Auto-pause vs alert-only
Auto-pause for clear thresholds (freq > 3.5, CTR drop > 35%). Alert-only for marginal cases — humans decide.

### Refresh starvation
If you pause faster than designers ship, account empties. Maintain "creative library" in staged state — 30-60 days of inventory.

### Frequency capping inside Meta
Set `frequency_cap` on adset: `{"event":"IMPRESSIONS","interval_days":7,"max_frequency":2}`. Prevents fatigue from occurring but limits reach.

### TikTok fatigue is faster
TikTok burns creative ~2x faster than Meta. Lower threshold (CTR drop > 20%, refresh weekly).

### Google PMax fatigue
PMax mixes assets — no clean per-asset fatigue read. Refresh asset group as whole monthly; rotate Asset Strength = "Excellent" to "Good" via swapping.

### LinkedIn fatigue
LinkedIn ads sustain longer (B2B, narrower audience). Frequency threshold can run 5-7 / 30d before fatigue shows.

## Sources

- Madgicx ad-fatigue guide: https://www.madgicx.com/blog/facebook-ad-fatigue
- Revealbot rules + dayparting: https://revealbot.com/blog/facebook-dayparting
- Meta frequency capping: https://www.facebook.com/business/help/870462676388943
- Meta video metrics: https://www.facebook.com/business/help/229540808697088
- Google PMax Asset Strength: https://support.google.com/google-ads/answer/12230255
- TikTok creative refresh cadence: https://ads.tiktok.com/help/article/creative-best-practices
- Slack incoming-webhook docs: https://api.slack.com/messaging/webhooks
- Linear GraphQL API: https://developers.linear.app/docs/graphql/working-with-the-graphql-api
