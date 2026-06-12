<!--
Source: https://github.com/wshobson/agents/blob/main/plugins/business-analytics/skills/kpi-dashboard-design/SKILL.md
Repo: wshobson/agents

NOTE: WebFetch returned a SUMMARY; substance preserved below.
See source URL for full content.
-->

# KPI Dashboard Design

Comprehensive patterns for building effective Key Performance Indicator dashboards across organizational levels.

## KPI Tier Framework

| Tier | Audience | Update Frequency |
|---|---|---|
| **Strategic** | Executives | Monthly/Quarterly |
| **Tactical** | Managers | Weekly/Monthly |
| **Operational** | Teams | Real-time/Daily |

## SMART KPI Framework

- **Specific** — clear definition
- **Measurable** — quantifiable
- **Achievable** — realistic targets
- **Relevant** — aligned to goals
- **Time-bound** — defined period

## Dashboard Hierarchy

- **Executive summaries** — 4-6 headline metrics
- **Department-specific views** — focused subset per function
- **Detailed drilldowns** — enable root cause analysis

## Critical Best Practices

- **Limit to 5-7 KPIs.** Focus on what matters.
- **Show context** through comparisons and trends — not bare numbers.
- **Avoid vanity metrics** that don't drive decisions.
- **Don't overcrowd** the dashboard.
- **Don't obscure** the calculation methodology — show how each metric is computed.

## Practical Troubleshooting

- **Metric contradictions** — align formulas explicitly (e.g., how annual plans normalize to monthly revenue)
- **False positives** — supplement infrastructure metrics with customer-perceived quality indicators
- **Database strain** — pre-aggregate metrics to summary tables rather than querying live production data
- **Alert fatigue** — use dynamic thresholds based on rolling averages instead of static cutoffs

## Related skills

Cross-references `data-storytelling` for translating dashboard insights into narratives.
