---
name: ga4-doc-analytics
description: Programmatic GA4 doc analytics with the Google Analytics Data API — `pip install google-analytics-data`. High-exit pages, scroll depth, engaged time, content-grouping reports. Use when the user has GA4 on their docs site and wants Claude to query it directly.
---

# GA4 Data API — Doc Analytics

GA4 is on most docs sites by default. The Data API (`google-analytics-data` Python SDK) lets the agent query traffic, exit rates, engaged sessions, and content-grouping reports directly without screen-scraping the UI.

## When to use this skill

- Audit existing docs traffic and find content gaps.
- Identify high-exit pages.
- Measure docs-led signup conversion.
- Cross-reference content engagement (scroll depth, engaged sessions) with high-traffic pages.

## Setup

### Prerequisites

- GA4 property already running on the docs site.
- A Google Cloud project with the **Google Analytics Data API** enabled.
- A service account with the `Analytics Viewer` role added to the GA4 property.

### Install

```bash
uv add google-analytics-data
# or
pip install google-analytics-data
```

### Auth — service account JSON

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json
export GA4_PROPERTY_ID=123456789      # from GA4 Admin → Property Settings
```

Per `cli-anything` invocation, the agent loads both env vars before running the script.

## Common recipes

### Recipe 1: Top 20 docs pages by sessions (last 30 days)

```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest, OrderBy
import os

client = BetaAnalyticsDataClient()
req = RunReportRequest(
    property=f"properties/{os.environ['GA4_PROPERTY_ID']}",
    date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
    dimensions=[Dimension(name="pagePath")],
    metrics=[Metric(name="sessions"), Metric(name="engagedSessions"),
             Metric(name="averageSessionDuration"), Metric(name="bounceRate")],
    order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
    limit=20,
)
res = client.run_report(req)
for row in res.rows:
    print(row.dimension_values[0].value, [m.value for m in row.metric_values])
```

Run with `cli-anything`:

```bash
uv run --with google-analytics-data python ga4_top_pages.py
```

### Recipe 2: High-exit pages

GA4 doesn't expose an "exit rate" dimension directly; compute as `1 - (engagedSessions / sessions)`:

```python
metrics=[Metric(name="sessions"), Metric(name="engagedSessions"), Metric(name="exits")]
# in the result row: exit_rate = exits / sessions
```

Filter to docs pages only:

```python
from google.analytics.data_v1beta.types import FilterExpression, Filter
req = RunReportRequest(
    ...,
    dimension_filter=FilterExpression(filter=Filter(
        field_name="pagePath",
        string_filter=Filter.StringFilter(
            match_type=Filter.StringFilter.MatchType.BEGINS_WITH,
            value="/docs/")),
    ),
)
```

### Recipe 3: Engaged sessions by page

```python
metrics=[Metric(name="engagedSessions"),
         Metric(name="userEngagementDuration"),
         Metric(name="scrolledUsers")]
```

`scrolledUsers` = number of users who scrolled past 90% (GA4 default `scroll` event threshold).

### Recipe 4: Content groupings

Tag each docs page with a `content_group` in GA4 (e.g., `tutorial`, `reference`, `how-to`, `explanation`):

```html
<script>
  gtag('event', 'page_view', { content_group: 'reference' });
</script>
```

Then group reports by `contentGroup` dimension to compare Diátaxis quadrants.

### Recipe 5: Search-then-exit ("found nothing")

Search-from-docs is captured by `view_search_results`. To find queries that didn't lead anywhere:

```python
dimensions=[Dimension(name="searchTerm")]
metrics=[Metric(name="searchResultsViews"), Metric(name="searchExits")]
```

A query with `searchExits / searchResultsViews > 0.6` means readers searched, didn't find an answer, left.

### Recipe 6: Real-time API (last 30 minutes)

```python
from google.analytics.data_v1beta.types import RunRealtimeReportRequest

req = RunRealtimeReportRequest(
    property=f"properties/{os.environ['GA4_PROPERTY_ID']}",
    dimensions=[Dimension(name="unifiedScreenName")],
    metrics=[Metric(name="activeUsers")],
)
res = client.run_realtime_report(req)
```

Useful for verifying that an analytics integration just deployed is firing events.

### Recipe 7: Cohort retention (docs onboarding flow)

```python
from google.analytics.data_v1beta.types import (
    Cohort, CohortSpec, CohortsRange, RunReportRequest)

req = RunReportRequest(
    ...,
    cohort_spec=CohortSpec(
        cohorts=[Cohort(
            name="june-tutorial-readers",
            dimension="firstSessionDate",
            date_range=DateRange(start_date="2026-06-01", end_date="2026-06-07"))],
        cohorts_range=CohortsRange(
            granularity=CohortsRange.Granularity.DAILY, end_offset=14),
    ),
    dimensions=[Dimension(name="cohort"), Dimension(name="cohortNthDay")],
    metrics=[Metric(name="cohortActiveUsers")],
)
```

Tracks how many tutorial-quickstart readers come back over 14 days.

## Common dimensions and metrics for docs

| Dimension | Use |
|---|---|
| `pagePath`, `pageTitle` | per-URL reports |
| `landingPagePlusQueryString` | entry-point analysis |
| `sessionSource` / `sessionMedium` | acquisition |
| `country`, `language` | i18n decisions |
| `deviceCategory` | mobile vs desktop docs UX |
| `contentGroup` | Diátaxis-quadrant rollups |
| `searchTerm` | docs-internal search analytics |

| Metric | Meaning |
|---|---|
| `sessions` | total visits |
| `engagedSessions` | sessions > 10s OR with 2+ pageviews OR with conversion event |
| `userEngagementDuration` | total engaged time (seconds) |
| `averageSessionDuration` | session length |
| `bounceRate` | `1 - (engagedSessions / sessions)` |
| `screenPageViews` | pageviews |
| `scrolledUsers` | users who scrolled past 90% |
| `exits` | sessions that ended on a page |

## Edge cases

- **Sampling:** GA4 sampling kicks in for very large date ranges; reduce range or use BigQuery export.
- **Custom events:** if the user has custom events (`feedback_yes`, `feedback_no`, `copy_code`), surface them via `eventCount` + `eventName` dimension.
- **API quota:** 25,000 tokens/day per property by default; cache results aggressively.
- **OAuth vs service account:** service account is the right path for agent use; OAuth requires interactive consent.
- **Cookie banner reject rate:** if users reject analytics cookies, traffic numbers undercount. Cross-reference with server-side logs.

## Pairs well with

- `microsoft-clarity-doc-analytics` — Clarity for behavior, GA4 for traffic / acquisition.
- `algolia-doc-search` — GA4 internal search, Algolia DocSearch Insights for the embedded search bar.

## Sources

- google-analytics-data: https://pypi.org/project/google-analytics-data/
- GA4 Data API docs: https://developers.google.com/analytics/devguides/reporting/data/v1
- GA4 Data API reference: https://developers.google.com/analytics/devguides/reporting/data/v1/rest
