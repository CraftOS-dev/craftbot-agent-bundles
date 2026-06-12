<!--
Source: https://app.delighted.com/docs/api + https://docs.sprig.com/ + https://developers.notion.com/ + https://developers.linear.app/
-->
# Voice of Customer Reporting — SKILL

Synthesize multi-source customer signals (interviews + NPS + CSAT/CES + ticket-cluster themes + churn-reason tags + Sprig micro-surveys) into themed VOC report. Cluster via embeddings; tag themes product/support/sales/marketing; route product-tagged to Linear with `voice-of-customer` label; render quarterly docx. Quote verbatim; weight by customer count x revenue impact.

## When to use

- **Quarterly VOC synthesis** — quarterly report for product manager + leadership.
- **Pre-roadmap planning** — feed top themes into product manager prioritization.
- **Ad-hoc theme deep-dive** — "What are customers saying about feature X?"
- **Churn-reason rollup** — monthly churn reasons synthesized for board.
- **Pre-CAB meeting prep** — what themes to present?
- **Customer interview synthesis** — after 5+ interviews, cluster into themes.

This skill **reads from** `nps-csat-ces-tracking` (survey comments), `customer-advisory-board-cab` (CAB meeting feedback), customer-support-agent's ticket warehouse (cluster themes), and `churn-save-motion-intervention` (outcome notes). It **feeds** product-manager (Linear roadmap input), sales-agent (battlecards), marketing-agent (content), customer-support-agent (docs gap).

Trigger phrases: "voice of customer", "VOC report", "customer themes", "synthesize feedback", "roadmap input", "churn reasons".

## Setup

```bash
# Signal sources
export DELIGHTED_API_KEY="<key>"
export SPRIG_API_KEY="<key>"

# Embedding for clustering (Claude generates, embeddings via Cohere/Voyage/OpenAI)
export COHERE_API_KEY="<key>"
export OPENAI_API_KEY="<key>"
export VOYAGE_API_KEY="<key>"

# linear-mcp + notion-mcp + postgresql-mcp already wired
```

Workspace prerequisites:
- Postgres tables: `delighted_responses`, `support_tickets`, `interview_notes`, `churn_reasons`, `cab_feedback`.
- Notion "VOC Insights" DB with: Theme, Quarter, Customer Count, ARR Impact, Source Mix, Tag (product/support/sales/marketing), Verbatim Quotes (rich text), Linear Issue (relation), Status.
- Linear `voice-of-customer` label + workflow.

## Synthesis sources (6 channels)

| # | Source | Pull mechanism |
|---|---|---|
| 1 | Customer interviews | Fathom transcripts -> Notion interview DB |
| 2 | NPS comments | Delighted API |
| 3 | CSAT / CES comments | Delighted API |
| 4 | Ticket-cluster themes | Postgres (from customer-support-agent warehouse) |
| 5 | Churn-reason tags | CSP / save plan outcomes |
| 6 | Sprig in-product survey results | Sprig API |

## Common recipes

### Recipe 1: Pull NPS comments from Delighted (90d)

```bash
curl -sS "https://api.delighted.com/v1/responses?since=$(date -u -d '90 days ago' +%s)&expand=person" \
  -u "$DELIGHTED_API_KEY:" \
  | jq '.[] | select(.comment != null and (.comment | length) > 20) | {
      comment, score, email: .person.email, created_at
    }' > nps_comments.jsonl
```

### Recipe 2: Pull CSAT / CES comments

```bash
curl -sS "https://api.delighted.com/v1/responses?survey_type=csat&since=$(date -u -d '90 days ago' +%s)" \
  -u "$DELIGHTED_API_KEY:" > csat_responses.jsonl

curl -sS "https://api.delighted.com/v1/responses?survey_type=ces&since=$(date -u -d '90 days ago' +%s)" \
  -u "$DELIGHTED_API_KEY:" > ces_responses.jsonl
```

### Recipe 3: Pull Sprig responses

```bash
curl -sS "https://api.sprig.com/v1/responses?survey_id=$SURVEY_ID&since=$(date -u -d '90 days ago' +%s)" \
  -H "Authorization: Bearer $SPRIG_API_KEY" > sprig_responses.jsonl
```

Doc: https://docs.sprig.com/

### Recipe 4: Pull ticket-cluster themes from Postgres

```sql
SELECT
  cluster_label,
  count(DISTINCT customer_id) AS customer_count,
  count(*) AS ticket_count,
  array_agg(DISTINCT customer_id) AS customers,
  sum(arr) AS total_arr,
  array_agg(snippet) FILTER (WHERE snippet IS NOT NULL) AS verbatim_snippets
FROM support_ticket_clusters
WHERE created_at >= now() - INTERVAL '90 days'
GROUP BY cluster_label
HAVING count(DISTINCT customer_id) >= 3
ORDER BY count(DISTINCT customer_id) DESC;
```

### Recipe 5: Pull churn reasons

```sql
SELECT
  reason_code,
  count(*) AS churn_count,
  sum(arr) AS arr_lost,
  array_agg(verbatim_notes) FILTER (WHERE verbatim_notes IS NOT NULL) AS quotes
FROM churn_log
WHERE churned_at >= now() - INTERVAL '90 days'
GROUP BY reason_code
ORDER BY arr_lost DESC;
```

### Recipe 6: Pull interview transcripts from Notion

Via `notion-mcp database_query` on "Customer Interviews" DB; pull last 90d; extract `transcript_text` property.

### Recipe 7: Combine sources + embed

```python
all_comments = []
all_comments.extend(load_jsonl("nps_comments.jsonl"))
all_comments.extend(load_jsonl("csat_responses.jsonl"))
all_comments.extend(load_jsonl("ces_responses.jsonl"))
all_comments.extend(load_jsonl("sprig_responses.jsonl"))
all_comments.extend(ticket_themes_from_recipe_4)
all_comments.extend(interview_chunks_from_recipe_6)

# Embed via Voyage (or Cohere / OpenAI)
import voyageai
client = voyageai.Client(api_key=os.environ["VOYAGE_API_KEY"])
embeddings = client.embed(
    [c["comment"] for c in all_comments],
    model="voyage-3",
).embeddings
```

### Recipe 8: HDBSCAN clustering

```python
import hdbscan
clusterer = hdbscan.HDBSCAN(min_cluster_size=3, metric='cosine')
labels = clusterer.fit_predict(embeddings)

# Group comments by cluster
from collections import defaultdict
clusters = defaultdict(list)
for comment, label in zip(all_comments, labels):
    if label != -1:  # -1 is noise
        clusters[label].append(comment)
```

Minimum 3 customers per cluster (signal threshold).

### Recipe 9: Theme labeling + tagging

```python
for cluster_id, comments in clusters.items():
    sample_quotes = [c["comment"] for c in comments[:5]]

    prompt = f"""
Given these customer comments from the same theme cluster:
{sample_quotes}

1. Suggest a short theme label (5-10 words).
2. Tag the theme: product / support / sales / marketing.
3. Suggest a 1-sentence summary.
4. Pick the 2-3 most powerful verbatim quotes.
"""
    labeled = claude.generate(prompt)

    # Compute customer count and ARR impact
    unique_customers = set(c.get("customer_id") for c in comments if c.get("customer_id"))
    arr_impact = postgres.query(f"SELECT sum(arr) FROM customers WHERE customer_id = ANY('{list(unique_customers)}')")

    # Write to Notion VOC Insights
    notion.create_page(
        parent={"database_id": VOC_INSIGHTS_DB_ID},
        properties={
            "Theme": {"title": [{"text": {"content": labeled.theme_label}}]},
            "Quarter": {"select": {"name": current_quarter}},
            "Customer Count": {"number": len(unique_customers)},
            "ARR Impact": {"number": arr_impact},
            "Tag": {"select": {"name": labeled.tag}},
            "Source Mix": {"multi_select": [{"name": s} for s in source_mix]},
            "Verbatim Quotes": {"rich_text": [{"text": {"content": "\\n\\n".join(labeled.quotes)}}]},
            "Status": {"status": {"name": "Synthesized"}},
        },
    )
```

### Recipe 10: Route product-tagged themes to Linear

```python
for theme in voc_themes_this_quarter:
    if theme.tag == "product":
        linear.create_issue(
            title=f"[VOC] {theme.label}",
            description=f"""
Customer count: {theme.customer_count}
ARR impact: ${theme.arr_impact:,.0f}
Quarter: {theme.quarter}

Verbatim quotes:
{theme.quotes}

Source mix: {theme.source_mix}

Routed from VOC Insights: {theme.notion_url}
""",
            team_id=PRODUCT_TEAM_ID,
            labels=["voice-of-customer"],
            priority=2 if theme.arr_impact > 100000 else 3,
        )
```

### Recipe 11: Cross-feed to other agents

```python
# Support-tagged -> customer-support-agent (docs gap signal)
for theme in support_tagged:
    notion.create_page(parent={"database_id": SUPPORT_DOCS_GAPS_DB_ID}, ...)

# Sales-tagged -> sales-agent (battlecard input)
for theme in sales_tagged:
    notion.create_page(parent={"database_id": SALES_BATTLECARDS_DB_ID}, ...)

# Marketing-tagged -> marketing-agent (content strategy)
for theme in marketing_tagged:
    notion.create_page(parent={"database_id": MARKETING_VOC_INPUT_DB_ID}, ...)
```

### Recipe 12: Generate quarterly VOC docx report

```python
docx.create(
    output="voc-2026-q2.docx",
    content=f"""
# Voice of Customer Report - {quarter}

Period: {start_date} to {end_date}
Customers represented: {customer_count_total}
Themes identified: {theme_count}

## Top themes (ranked by customer count x revenue impact)

{render_themes_section()}

## Trends quarter-over-quarter

{render_trends_section()}

## Recommended product roadmap input (top 3)

{render_product_recommendations()}

## Recommended support / docs input

{render_support_recommendations()}

## Recommended sales battlecards

{render_sales_recommendations()}
"""
)
```

### Recipe 13: Trend QoQ comparison

```sql
SELECT
  theme_label,
  count(*) FILTER (WHERE quarter = 'Q1 2026') AS q1_mentions,
  count(*) FILTER (WHERE quarter = 'Q2 2026') AS q2_mentions,
  (count(*) FILTER (WHERE quarter = 'Q2 2026') - count(*) FILTER (WHERE quarter = 'Q1 2026'))
  * 1.0 / nullif(count(*) FILTER (WHERE quarter = 'Q1 2026'), 0) AS qoq_change
FROM voc_themes
GROUP BY theme_label
ORDER BY qoq_change DESC;
```

Themes spiking up = urgent attention; themes dropping = likely shipped or pivoted away.

## Examples

### Example 1: Quarterly VOC report (zero-touch synthesis)

**Goal:** End of Q2; product manager has VOC report by July 5.

**Steps:**
1. June 28: Recipes 1-6 pull all sources for Q2.
2. June 29: Recipe 7 embeds; Recipe 8 clusters.
3. June 30: Recipe 9 labels themes; writes to Notion VOC Insights.
4. July 1: Recipe 10 + 11 routes to Linear + cross-feeds.
5. July 2: Recipe 12 docx; email to product-manager + leadership.
6. July 5: PM uses report for Q3 planning.

**Result:** Data-driven Q3 roadmap input.

### Example 2: "What are customers saying about SSO?" deep-dive

**Goal:** PM asks ad-hoc: themes around SSO?

**Steps:**
1. Recipe 1-6 with text filter: WHERE comment ILIKE '%SSO%' OR %single sign-on% OR %SAML%
2. Recipe 7 embed those comments only.
3. Recipe 8 cluster: 4 sub-clusters (Okta-integration friction, AzureAD complexity, OAuth confusion, SCIM provisioning gaps).
4. Recipe 9 labels each.
5. Write up + Slack to PM with verbatims.

**Result:** PM gets specific, actionable customer voice in <2h.

## Edge cases / gotchas

- **Cluster cardinality** — too many clusters (> 25) = noise; too few (< 5) = themes too broad. Tune `min_cluster_size` quarterly.
- **PII in comments** — customer emails/names in NPS comments. Strip before embedding/clustering; redact in final report.
- **Embedding cost at scale** — 100k comments at Voyage = ~$100. Use cohort sampling for large volumes.
- **Single-customer themes** — one loud customer dominates a cluster. Min 3 customers per cluster filter (HDBSCAN setting).
- **Source weighting bias** — NPS comments are 2x as frequent as interviews; theme volume reflects source mix, not customer reality. Weight by source.
- **Linear issue duplication** — same theme repeats across quarters; check if Linear issue exists before creating new one.
- **Theme misattribution** — "Support is slow" tagged as support, but root cause is product confusion -> mistag as product. Manual review of top 3 themes.
- **Verbatim quotes attribution** — always cite customer + tier (anonymized if NDA). Never paste without source.
- **Churn-reason taxonomy drift** — CSMs use different codes. Standardize: Product, Pricing, Onboarding, Service, External. Document; train.
- **Embeddings model swap** — switching Voyage -> Cohere shifts cluster results; re-cluster historical before comparing QoQ.
- **Survey-only synthesis misses tickets** — best signal comes from cross-source. Don't run synthesis with NPS-only.
- **Don't let synthesized themes feel "AI-generated"** — preserve customer's own language; theme labels = 5-10 words, not corporate jargon.

## Sources

- [Delighted Responses API](https://app.delighted.com/docs/api)
- [Sprig API responses](https://docs.sprig.com/)
- [Notion database query](https://developers.notion.com/reference/post-database-query)
- [Voyage AI embeddings](https://docs.voyageai.com/docs/embeddings)
- [Cohere embeddings](https://docs.cohere.com/reference/embed)
- [OpenAI text-embedding-3-large](https://platform.openai.com/docs/guides/embeddings)
- [HDBSCAN clustering](https://hdbscan.readthedocs.io/en/latest/)
- [Linear API create issue](https://developers.linear.app/docs/graphql/working-with-the-graphql-api)
- [Fathom transcripts API](https://help.fathom.video/en/articles/8430832-fathom-api)
- [Voice of Customer best practices (Qualtrics)](https://www.qualtrics.com/experience-management/customer/voice-of-customer/)
