# Customer Support Agent — Source Attribution

Section-to-source map for soul.md and role.md. **Not** loaded into context — for human verification.

Authoritative SOTA mapping lives at `reference/SOTA_USE_CASES.md`. URLs in `agent.yaml → sources`.

This agent's v1 build pass derived its SOTA content from direct web research on the 2026 customer-support stack rather than downloaded reference agent files. Round 2 of the methodology can backfill `reference/agents/` with downloads from wshobson/agents, VoltAgent/awesome-claude-code-subagents, msitarzewski/agency-agents.

---

## soul.md → source map

| Section | Source(s) |
|---|---|
| Opening identity + 3 convictions | composition synthesis distilling load-bearing rules from the SOTA platform doctrine: Intercom Fin AI (accuracy-gated auto-reply via Resolution Score), Zendesk Intelligent Triage (categorize as product signal), Kapa.ai (deflection beats response) |
| Purpose | composition from Intercom + Zendesk + Front platform philosophy + bug-normalization industry practice |
| Execution stack | `reference/SOTA_USE_CASES.md` — one bullet per bundled skill pack, named per Round 1 prompt |
| When invoked — Triage mode | Intercom Fin AI Operator workflow + Zendesk Intelligent Triage + Front routing patterns |
| When invoked — Response template mode | platform-native macro APIs + Vale linting conventions |
| When invoked — FAQ + KB mode | Kapa.ai analytics + Notion editorial + Lychee link checking |
| When invoked — Escalation mode | Linear / Jira best-practice escalation patterns + Sentry crash matching |
| When invoked — SLA + on-call mode | Zendesk SLA policies + PagerDuty on-call patterns |
| When invoked — Sentiment + CSAT mode | Loris.ai + Klaus QA + Delighted post-close pattern |
| When invoked — Churn + health mode | Vitally / Catalyst CSP integration patterns |
| When invoked — Incident comms mode | Statuspage.io documented lifecycle |
| When invoked — Community / multilingual mode | Discord / Reddit moderation patterns + DeepL translation flow |
| When invoked — Trust & safety mode | Atomic AI / Perspective API classifier flow |
| Core operating rules | merged from platform doctrine: Intercom (Resolution Score gating = "never bullshit"), Zendesk (tag as product signal), Kapa (deflection beats response), bug-normalization industry rule, post-MPP measurement (clicks > opens), refund-policy compliance |
| Mode-specific decisions | one entry per mode keyed to the matching platform / tool reference |
| Quality gates | platform-native quality gates: Vale lint for voice, structured Linear/Jira payload, Statuspage lifecycle compliance, CSAT auto-routing rules |
| Output format | composition from each platform's canonical formats (Linear issue body, Statuspage update, Delighted survey, etc.) |
| Communication style | distilled from voice doctrine across Loris / Klaus / Intercom support best-practice; AI-slop catch list adapted from `marketing-agent` voltagent-content-quality-editor pattern |
| When to push back | composition synthesis informed by Intercom Resolution Score gating (refuse to fake answer), Stripe refund-policy enforcement, T&S precedence, privacy-as-infrastructure |
| When to defer | composition synthesis with explicit sibling-agent hand-offs (sales-agent, product-manager, technical-writer, marketing-agent, senior-python-engineer) |
| First-conversation routine questions | standard PROACTIVE.md self-init pattern (METHODOLOGY.md decision #3); questions adapted to support workflows (primary platform / ticket volume / engineering destination) |
| Closing rule | distilled summary of the three convictions + sibling-agent hand-off pattern |

---

## role.md → source map

| Section | Source(s) |
|---|---|
| Capability reference → Ticket platforms | direct knowledge of 2026 support-platform landscape (Intercom / Zendesk / Front / Plain / HelpScout / Chatwoot / Crisp / Kustomer / Freshdesk / Pylon / Gladly) |
| Capability reference → Engineering escalation | Linear / Jira / GitHub Issues platform docs |
| Capability reference → Real-time / community channels | Slack / Discord / Microsoft Teams / Reddit / Twitter docs |
| Capability reference → AI doc Q&A | Kapa.ai / Inkeep / Mendable / Markprompt platform docs |
| Capability reference → CSPs | Vitally / Catalyst / ChurnZero / Gainsight / Totango / Custify / Velaris vendor docs |
| Capability reference → Sentiment / QA | Loris.ai / Klaus / MaestroQA / Stylus AI / Perspective API docs |
| Capability reference → Survey | Delighted / Wootric / Survicate / Typeform / Refiner / Hotjar docs |
| Capability reference → Voice | Aircall / Dialpad / Twilio docs |
| Capability reference → Product analytics tied to support | PostHog / Mixpanel / Amplitude / FullStory / LogRocket / Sentry docs |
| Capability reference → Incident comms / status | Statuspage / Better Stack / Instatus / FireHydrant / PagerDuty / Opsgenie docs |
| Capability reference → Refunds / payments | Stripe / Recurly / Chargebee / Paddle docs |
| Capability reference → Reverse-ETL + warehouse | Census / Hightouch / dbt / Metabase / Looker / Hex / Mode docs |
| Triage playbook | composition synthesis from Intercom Fin AI + Zendesk Intelligent Triage docs |
| Routing rule template | composition synthesis informed by Zendesk Triggers + Intercom Conversation Routing patterns |
| Response template playbook + macro voice rules | composition from platform macro APIs (Zendesk / Intercom / Front / HelpScout / Plain) + AI-slop industry catch list |
| FAQ + KB playbook | Kapa.ai analytics + Notion editorial patterns + Lychee linker patterns |
| Escalation playbook + bug normalization template | composition synthesis combining Linear + Jira + Sentry industry-standard structured bug template |
| SLA + on-call playbook | Zendesk SLA Policies + Intercom Conversation SLA + PagerDuty on-call rotation |
| Sentiment + CSAT playbook | Loris.ai + Klaus + Delighted + Survicate platform docs |
| Churn + health scoring playbook + health score formula | Vitally + Catalyst + ChurnZero composite-formula pattern; weights and risk-flag thresholds are industry baseline (recipient should tune) |
| Incident comms playbook + Statuspage lifecycle | Statuspage.io developer docs (incident lifecycle states verbatim) |
| Refund + credit policy | Stripe refund API + industry-standard threshold-gating pattern |
| Multilingual routing playbook | DeepL API + per-language macro library pattern |
| Trust & safety playbook | Atomic AI + Google Perspective API + industry T&S handling pattern |
| Community support playbook | Discord / Reddit / Discourse moderation industry patterns |
| Voice support playbook | Aircall / Dialpad / Twilio transcription patterns |
| AI-slop catch list — support edition | adapted from marketing-agent voltagent-content-quality-editor.md (banned openers + sycophancy + performative empathy + fake-ETA language), narrowed to support-specific phrases |
| Antipattern catalog (fabricated ETA / performative empathy / free-form escalation / premature close / mass-broadcast / internal exposure) | composition synthesis from common support-failure modes documented across Intercom / Zendesk / Front community + industry post-mortems |
| Reporting + dashboard patterns | Census / Hightouch / dbt / Metabase patterns |
| SOTA tool reference | `reference/SOTA_USE_CASES.md` — one H3 per bundled skill pack |
| Updated mappings | translation table: generic category → SOTA replacement |

---

## Notes on "authored from synthesis"

Several sections in this v1 build are composition-synthesis on top of platform documentation rather than verbatim lifts from a reference agent. This is appropriate for v1 — Round 2 can backfill with concrete reference-agent files:

- **Three opening convictions in soul.md** — distillation of platform doctrine: "speed matters but accuracy wins" (Intercom Resolution Score), "tickets are signal not noise" (Zendesk Intelligent Triage), "deflection beats response" (Kapa.ai philosophy).
- **Bug normalization template** — composition synthesis from Linear / Jira / Sentry / industry-standard bug-report templates. Not lifted from a single source; the 11-field structure is canonical.
- **Routing rule template** — composition synthesis informed by Zendesk Triggers + Intercom Conversation Routing.
- **Health score formula** — composite weights (40/20/15/10/10/5) are industry-baseline; recipient should tune to their business model. Documented as a starting point, not as a domain claim.
- **AI-slop catch list — support edition** — adapted from marketing-agent's voltagent-content-quality-editor pattern, narrowed to support-specific phrases ("Sorry to hear that!", "Thank you for your patience!", "I completely understand", "Apologies for the inconvenience!").
- **Antipattern catalog** — composition synthesis from common support-failure modes across Intercom / Zendesk / Front communities. Not lifted from a single source.
- **First-conversation PROACTIVE.md self-init** — standard pattern from METHODOLOGY.md with support-specific routine questions.

No fabricated benchmarks, fake quotes, or fake customer stories. All platform features cited are real and verifiable via the URLs in `agent.yaml → sources`.

---

## How to update this agent

1. **Round 2 backfill (recommended):** download 4-6 reference agents from wshobson/agents (look for `plugins/customer-support/` and `plugins/operations/`), VoltAgent/awesome-claude-code-subagents (categories/09-customer-success), msitarzewski/agency-agents into `reference/agents/`. Diff against composition synthesis; tighten role.md voice where reference language is stronger.
2. **Refresh SOTA tool list:** SOTA changes monthly. Re-fetch each tool's docs URL (in `agent.yaml → sources`); update SOTA_USE_CASES.md confidence ratings if anything shifted.
3. **Refresh CraftBot MCP catalog:** if new MCPs land (e.g., PagerDuty MCP, Statuspage MCP, Kapa MCP), promote them in `agent.yaml` and update role.md SOTA tool reference.
4. **Re-run `build.py`** to regenerate the .craftbot bundle.

---

## SOTA tool sources (June 2026)

These sources back the `role.md → SOTA tool reference (June 2026)` section, the `reference/SOTA_USE_CASES.md` per-use-case mapping, and the 20 bundled skill packs in `skills/` (Round 2 populates SKILL.md contents).

| Tool | Source URL | Used for |
|---|---|---|
| Intercom Fin AI Operator | https://www.intercom.com/help/en/articles/9442290-fin-ai-operator | `skills/intercom-fin-ai-mcp/SKILL.md` — triage + auto-reply + conversation summarization + macros |
| Intercom Conversation Routing | https://www.intercom.com/help/en/articles/9442271-conversation-routing | routing rule patterns |
| Zendesk Intelligent Triage | https://support.zendesk.com/hc/en-us/articles/4408828134298-Intelligent-triage | `skills/zendesk-mcp-ops/SKILL.md` — Zendesk triage + macros |
| Zendesk Macros API | https://developer.zendesk.com/api-reference/ticketing/business-rules/macros/ | macro management |
| Zendesk SLA Policies API | https://support.zendesk.com/hc/en-us/articles/4408839029530 | SLA breach tracking |
| Front API reference | https://dev.frontapp.com/reference | `skills/front-multichannel-inbox/SKILL.md` — Front shared inbox + templates |
| Front Smart Summarize | https://dev.frontapp.com/reference/smart-summarize | conversation summarization for handoff |
| Plain API docs | https://plain.com/docs/api | `skills/plain-modern-tickets/SKILL.md` — Plain GraphQL ticketing |
| HelpScout Mailbox API | https://developer.helpscout.com/mailbox-api/ | `skills/helpscout-mcp/SKILL.md` — HelpScout REST |
| Chatwoot API | https://www.chatwoot.com/developers/api/ | OSS alternative for inbound chatbot |
| Linear API + MCP | https://developers.linear.app/docs | `skills/escalation-linear-jira-engineering/SKILL.md` + `skills/bug-report-normalization-linear/SKILL.md` |
| Atlassian Jira REST API v3 | https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/ | Jira escalation alternative |
| Sentry API | https://docs.sentry.io/api/ | bug normalization crash matching |
| Kapa.ai API | https://docs.kapa.ai/api | `skills/kapa-ai-doc-qa/SKILL.md` + `skills/deflection-metrics-content-gap/SKILL.md` |
| Kapa.ai analytics | https://docs.kapa.ai/analytics | deflection rate + zero-result queries |
| Inkeep docs | https://docs.inkeep.com/ | alt AI doc Q&A |
| Markprompt OSS | https://markprompt.com/docs | free / OSS alt for AI doc Q&A |
| Lychee link checker | https://lychee.cli.rs/ | KB dead-link sweep |
| Notion API | https://developers.notion.com/ | `skills/notion-knowledge-base-management/SKILL.md` — KB editorial SoT |
| Loris.ai | https://loris.ai/ | `skills/sentiment-analysis-cohort-trends/SKILL.md` — per-ticket sentiment |
| Zendesk QA (Klaus) API | https://klausapp.com/api | cohort-level conversation QA |
| Delighted CSAT/CES/NPS API | https://app.delighted.com/docs/api | `skills/csat-ces-nps-instrumentation/SKILL.md` — survey ops |
| Survicate API | https://developers.survicate.com/ | alt survey vendor |
| Wootric / InMoment | https://www.inmoment.com/ | incumbent survey alt |
| Vitally API | https://docs.vitally.io/reference | `skills/churn-prediction-support-signals/SKILL.md` + `skills/customer-health-scoring-vitally-catalyst/SKILL.md` |
| Catalyst (Totango) API | https://help.catalyst.io/ | enterprise CSP alt |
| Totango / Custify / Velaris / ChurnZero / Gainsight | vendor docs | alt CSPs |
| Statuspage developer docs | https://developer.statuspage.io/ | `skills/incident-customer-comms-statuspage/SKILL.md` |
| PagerDuty REST API | https://developer.pagerduty.com/api-reference/ | on-call rotation (no MCP yet — `cli-anything` curl) |
| Opsgenie API | https://docs.opsgenie.com/docs/api-overview | PagerDuty alt |
| Stripe Refunds API | https://stripe.com/docs/api/refunds | refund/credit execution |
| DeepL API | https://www.deepl.com/docs-api | `skills/multilingual-routing` — translation + multilingual support routing |
| Atomic AI | https://atomic.ai/ | `skills/trust-safety-abuse-triage/SKILL.md` — abuse classification |
| Google Perspective API | https://perspectiveapi.com/ | free fallback for basic toxicity scoring |
| PostHog session replay | https://posthog.com/docs/session-replay | self-serve onboarding troubleshooting |
| Aircall developer API | https://developer.aircall.io/api-references/ | `skills/voice-support-aircall-dialpad-twilio/SKILL.md` |
| Dialpad API | https://developers.dialpad.com/ | voice transcription alt |
| Twilio docs | https://www.twilio.com/docs | outbound SMS + voice |
| Productboard API | https://developer.productboard.com/ | feature-request capture |
| Canny / Linear feature-request | https://developers.canny.io/api-reference + Linear MCP | feature-request capture alt |
| Census reverse-ETL | https://docs.getcensus.com/ | warehouse sync from support platforms |
| Hightouch reverse-ETL | https://hightouch.com/docs | Census alt |
| Native CraftBot MCPs (`linear-mcp`, `jira-mcp`, `sentry-mcp`, `slack-mcp`, `discord-mcp`, `discord-mcp-full`, `ms-teams-mcp`, `twilio-mcp`, `stripe-mcp`, `posthog-mcp`, `mixpanel-mcp`, `amplitude-mcp`, `reddit-mcp`, `firecrawl-mcp`, `brightdata-mcp`, `deepl-mcp`, `gmail-mcp`, `notion-mcp`, `postgresql-mcp`) | `agent.yaml` | per-platform escalation, internal comms, refunds, analytics, community, multilingual, KB |

**Total:** 20 bundled skill packs (Round 2 fills SKILL.md) + 20 native MCPs + 7 fallback APIs covering ≥95% of `USE_CASES.md` documented use cases. See `reference/SOTA_USE_CASES.md` for the per-use-case confidence map.
