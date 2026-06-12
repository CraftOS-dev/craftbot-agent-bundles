<!--
Sources:
Intercom API — https://developers.intercom.com/intercom-api-reference
Zendesk API — https://developer.zendesk.com/api-reference/
Dovetail v3 API — https://dovetail.com/help/api
Hugging Face — text clustering — https://huggingface.co/blog/text-clustering
-->
# Support Ticket Thematic Analysis — SKILL

Pull support tickets from Intercom / Zendesk / Front / HelpScout. Cluster by tag + body via Dovetail OR embedding-based clustering for high volume. Identify product-friction themes (vs one-off issues) by count + frequency. Tie themes to research findings for triangulation. Output: VoC report + PM handoff.

## When to use

- Quarterly VoC report.
- Triangulating user research findings with support patterns.
- Identifying top product friction from real-world usage.
- Feature gap analysis (what users repeatedly ask for).
- Pre-PRD discovery (what's blocking users today).

Trigger phrases: "analyze support tickets", "what are users complaining about", "ticket themes", "Intercom thematic", "Zendesk patterns", "VoC report".

## Setup

```bash
# Intercom
curl -fsSL "https://api.intercom.io/me" \
  -H "Authorization: Bearer $INTERCOM_API_TOKEN" \
  -H "Intercom-Version: 2.11"

# Zendesk
curl -fsSL "https://yourcompany.zendesk.com/api/v2/users/me.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN"

# Front
curl -fsSL "https://api2.frontapp.com/me" \
  -H "Authorization: Bearer $FRONT_API_TOKEN"

# HelpScout
curl -fsSL "https://api.helpscout.net/v2/users/me" \
  -H "Authorization: Bearer $HELPSCOUT_API_TOKEN"

# Dovetail
curl -fsSL "https://dovetail.com/api/v1/me" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN"
```

## Common recipes

### Recipe 1: Pull tickets from Intercom (last 90 days)

```bash
SINCE_TS=$(date -d '90 days ago' +%s)

curl -fsSL "https://api.intercom.io/conversations/search" \
  -H "Authorization: Bearer $INTERCOM_API_TOKEN" \
  -H "Intercom-Version: 2.11" \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": {
      \"operator\": \"AND\",
      \"value\": [
        {\"field\": \"created_at\", \"operator\": \">\", \"value\": $SINCE_TS},
        {\"field\": \"state\", \"operator\": \"=\", \"value\": \"closed\"}
      ]
    },
    \"pagination\": {\"per_page\": 150}
  }" \
| jq '[.conversations[] | {
    id, created_at, state, tags: [.tags.tags[].name],
    body: .source.body, customer_id: .user.user_id
  }]' > intercom-tickets.json
```

### Recipe 2: Pull tickets from Zendesk

```bash
curl -fsSL "https://yourcompany.zendesk.com/api/v2/search.json?query=type:ticket+created>90days+status:solved" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
| jq '[.results[] | {
    id, created_at, subject, description, tags,
    priority, satisfaction_rating: .satisfaction_rating.score,
    requester_id
  }]' > zendesk-tickets.json
```

### Recipe 3: Pull tickets from Front

```bash
curl -fsSL "https://api2.frontapp.com/conversations?q[statuses][]=archived&q[created_after]=$SINCE_TS&limit=100" \
  -H "Authorization: Bearer $FRONT_API_TOKEN" \
| jq '[.["_results"][] | {id, subject, tags: .tags[].name, status, created_at}]'
```

### Recipe 4: Tag taxonomy for product tickets

```markdown
# Suggested tag taxonomy

## Issue category (top-level)
- issue/bug
- issue/feature-request
- issue/how-to
- issue/billing
- issue/account
- issue/integration

## Sub-category
- issue/bug/data-loss
- issue/bug/sync-error
- issue/feature-request/missing-export
- issue/integration/slack-broken

## Product area
- area/dashboard
- area/inbox
- area/settings
- area/integrations
- area/billing

## Severity
- severity/critical
- severity/major
- severity/minor
- severity/cosmetic
```

### Recipe 5: Upload to Dovetail for tagging

```bash
while read -r TICKET; do
  ID=$(echo "$TICKET" | jq -r '.id')
  BODY=$(echo "$TICKET" | jq -r '.body // .description')
  EXISTING_TAGS=$(echo "$TICKET" | jq -r '.tags | join(",")')

  curl -X POST "https://dovetail.com/api/v1/projects/$DOVETAIL_PROJECT/notes" \
    -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
    -d "{
      \"title\": \"Ticket $ID\",
      \"body\": \"$BODY\",
      \"tags\": [\"source/intercom\", \"$EXISTING_TAGS\"]
    }"
done < <(jq -c '.[]' intercom-tickets.json)
```

### Recipe 6: Embedding-based clustering for 1000+ tickets

```python
# Same pattern as nps-verbatim-thematic-coding Recipe 6
import requests
import numpy as np
from sklearn.cluster import HDBSCAN
import umap

def cluster_tickets(tickets, hf_token):
    texts = [t["body"] or t["description"] for t in tickets]
    embeddings = np.array(requests.post(
        "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2",
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": texts}
    ).json())

    reduced = umap.UMAP(n_components=10, metric="cosine").fit_transform(embeddings)
    labels = HDBSCAN(min_cluster_size=15).fit_predict(reduced)

    clusters = {}
    for i, label in enumerate(labels):
        if label == -1: continue
        clusters.setdefault(label, []).append(tickets[i])
    return clusters
```

### Recipe 7: Frequency × severity prioritization

```python
def prioritize_themes(clusters):
    """
    Score = ticket count × avg severity × avg negative-sentiment
    """
    prioritized = []
    for cluster_id, tickets in clusters.items():
        count = len(tickets)
        avg_severity = mean(t.get("severity_score", 2) for t in tickets)
        avg_sat = mean(t.get("satisfaction_rating", 3) for t in tickets if t.get("satisfaction_rating"))
        score = count * avg_severity * (5 - avg_sat)
        prioritized.append({
            "cluster_id": cluster_id,
            "count": count,
            "score": score,
            "sample_titles": [t["subject"] for t in tickets[:3]]
        })
    return sorted(prioritized, key=lambda x: x["score"], reverse=True)
```

### Recipe 8: VoC report template

```markdown
# Voice of Customer: Q3 2026 Support Patterns

**N=1247 closed tickets · Period:** Q3 2026
**Sources:** Intercom (B2C), Zendesk (B2B)
**Researcher:** [Name]

## TL;DR
- Top 3 themes by frequency × severity:
  1. CSV import failures (98 tickets, severity 3.2 avg)
  2. Slack sync delay (76 tickets, severity 2.8 avg)
  3. Pricing confusion at upgrade (54 tickets, severity 2.4 avg)
- Estimated user impact: ~12% of MAU
- Top action: ship CSV import fix in next sprint

## Method
- Pull 90 days of closed tickets via Intercom + Zendesk APIs
- Embedding-based clustering (Hugging Face sentence-transformers)
- Per-cluster manual review + label
- Cross-reference with research findings from JTBD interviews

## Themes

### Theme 1: CSV import failures (98 tickets)
- **Pattern:** Users uploading >5MB CSV files see silent failure
- **Sample tickets:** [ticket IDs]
- **Sample verbatims:**
  > "Tried to import 8000 leads — nothing happened, no error." — Intercom #4823
  > "CSV uploader times out, then I lose my work." — Zendesk #9012
- **Severity:** 3.2 avg (Major)
- **Cross-reference:** Mentioned in 4 of 12 JTBD interviews as "deal-breaker for migration"
- **Recommendation:** Eng priority — chunk upload for >5MB; surface error state
- **Owner:** Eng / PM
- **ETA:** Sprint 14

### Theme 2: ...

## Cross-source comparison
- Intercom (consumer): top theme = pricing confusion (low ARPU → price-sensitive)
- Zendesk (enterprise): top theme = SSO integration gaps (enterprise IT requirements)

## Triangulation with research
- Theme 1 (CSV) confirmed by JTBD interviews + diary study
- Theme 2 (Slack sync) NEW signal — recommend follow-up moderated test
- Theme 3 (pricing) confirmed by NPS detractor cluster

## Recommendations
1. [Priority 1 with owner + ETA]
2. ...

## Sources
- Intercom tickets: [link]
- Zendesk tickets: [link]
- Dovetail synthesis: [link]
```

### Recipe 9: Linear handoff per theme

```bash
# File theme as Linear issue for PM triage
curl -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_TOKEN" \
  -d '{
    "query": "mutation { issueCreate(input: {title: \"CSV import failure pattern (98 support tickets, severity 3.2)\", description: \"Pulled from Q3 VoC analysis. See [Dovetail link]. Recommend ship CSV import fix in next sprint.\", teamId: \"<team-id>\", labelIds: [\"<voc-label>\", \"<research-label>\"]}) { success issue { id title url } } }"
  }'
```

### Recipe 10: Continuous VoC dashboard

```markdown
# Continuous VoC cadence

## Daily
- Auto-pull new tickets from Intercom + Zendesk
- Auto-tag via embedding model (review weekly)
- Surface emerging themes (sudden spike in any cluster)

## Weekly
- Review auto-tags; clean up taxonomy
- Flag spikes (>20% week-over-week)
- Slack notification to PM channel

## Monthly
- Run full clustering refresh
- Update VoC dashboard
- Cross-reference with active research

## Quarterly
- VoC report
- Action plan with owners
- Retrospective on prior quarter actions
```

## Examples

### Example 1: Quarterly VoC for executive readout
**Goal:** Surface top product friction from 1247 tickets.

**Steps:**
1. Pull Intercom + Zendesk (Recipes 1-2).
2. Embedding cluster (Recipe 6).
3. Prioritize (Recipe 7).
4. Cross-reference with research (Recipe 8 triangulation).
5. Report (Recipe 8).
6. Linear handoff (Recipe 9).

**Result:** Defensible PM backlog with ticket counts as evidence.

### Example 2: Single-theme deep dive
**Goal:** Understand CSV import pattern beyond ticket count.

**Steps:**
1. Filter tickets by tag (Recipe 5 query Dovetail).
2. Read top 20 tickets in full.
3. Identify pattern (file size, error type, user segment).
4. Recommend specific fix (chunked upload + clear error).

**Result:** Actionable bug pattern instead of abstract category.

## Edge cases / gotchas

- **One-off issues miscoded as theme.** Cluster threshold ≥15 tickets to count as theme.
- **Bug reports vs feature requests.** Separate buckets; different actions.
- **Survivor bias.** Only tickets — happy users don't ticket. Pair with NPS / interviews.
- **Severity inferred from priority field.** Not always accurate; sample-check.
- **Tag taxonomy explosion.** >20 tags = noise. Cluster + collapse quarterly.
- **Embedding model latency / cost.** For 10k+ tickets, batch + cache.
- **Tickets reflecting support process issues.** "Long wait time" = support staffing, not product. Filter.
- **Sentiment as proxy.** CSAT score useful but not all platforms have it.
- **Stale tickets in cluster.** Filter by 90-180 day window; older = less actionable.
- **PII in ticket bodies.** Sanitize before uploading to Dovetail / HF.
- **GDPR right-to-erasure.** User-deletion request → remove from analysis dataset.
- **Multi-language tickets.** Translate first or use multilingual embedding model.

## Sources

- [Intercom API Reference](https://developers.intercom.com/intercom-api-reference)
- [Zendesk API Reference](https://developer.zendesk.com/api-reference/)
- [Front API](https://dev.frontapp.com)
- [HelpScout API](https://developer.helpscout.com/mailbox-api/)
- [Dovetail v3 API](https://dovetail.com/help/api)
- [Hugging Face — text clustering](https://huggingface.co/blog/text-clustering)
- [Linear API](https://developers.linear.app)
- [NN/g — Voice of Customer](https://www.nngroup.com/articles/voice-of-customer/)
