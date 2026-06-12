# Customer Support Agent — Use Cases

**Tier:** **general** · **Category:** support
**Core job:** End-to-end customer support for teams managing real ticket volume — triage, response templates, FAQ, escalation, SLA, CSAT, sentiment, churn signals, incident comms, multi-channel.

> Ships with the SOTA support stack (Intercom Fin AI / Zendesk Triage / Front / Plain, Kapa AI doc Q&A, Linear / Jira / Sentry escalation, Vitally / Catalyst health scoring, Delighted CSAT, Statuspage incident comms, Stripe refunds, DeepL multilingual) — executes end-to-end, not just direct. This file is bundled but **not** loaded into the agent's context.

---

## What this agent is supposed to do

### Ticket triage
- Auto-categorize by topic (auth / billing / bug / how-to / feature / abuse / other)
- Auto-classify urgency (critical / high / normal / low) and sentiment (frustrated → delighted)
- Auto-route by `(channel, customer-tier, topic)` rule engine
- First-response within SLA per tier
- Tag every ticket with topic + urgency + sentiment + tier + language (product signal)

### Response template generation
- Cluster tickets by embedding (≥ 5 tickets per cluster threshold)
- Draft canonical macros per cluster
- Vale brand-voice lint pass before publish
- Push to Zendesk Macros / Intercom Macros / Front Templates / HelpScout Saved Replies / Plain Snippets
- Notion source-of-truth for cross-platform consistency

### FAQ generation + KB management
- Drift detection (articles unviewed in 90d, dead links via Lychee)
- Zero-result query analysis → content gaps
- Cross-reference top ticket clusters with existing KB
- Auto-draft new FAQ entries with ticket-ID citations
- Push approved drafts to Help Center via platform API

### Engineering escalation
- Bug normalization template (repro, expected, actual, env, customer impact, $ARR at risk)
- Sentry MCP crash matching
- Linear / Jira issue creation with customer-tier label and ticket back-link
- Reverse-sync from engineering status → ticket internal notes
- Productboard / Canny / Linear feature-request capture with cluster sizing

### SLA tracking + breach alerts
- Tiered SLA: Enterprise 1h / 4h, Growth 4h / 24h, Starter 8h / 48h, Free 24h / 72h
- 30-min-before-breach Slack ping to owner
- At-breach lead escalation + PagerDuty for critical tier
- Weekly SLA breach report by team / tier / channel

### Sentiment analysis
- Per-ticket scoring via Loris.ai / Klaus / Claude fallback
- Cohort weekly trend (alert on > 20% WoW decline)
- Cross-reference with product releases (post-release regression detection)
- Emotion classification (angry / frustrated / confused / neutral / satisfied / delighted)

### CSAT / CES / NPS measurement
- Post-ticket-close CSAT (1-5 stars) within 1h
- Post-resolution CES (1-7 scale) within 24h
- Quarterly NPS independent of support events
- Detractor auto-route to CSM
- Delighted / Survicate / Wootric platform integration

### Churn prediction from support signals
- Feed support metrics (ticket volume 90d, avg CSAT, SLA breach count, last-bug-encounter) to Vitally / Catalyst / Totango / ChurnZero / Gainsight
- Read-back health score; CSM playbook fires on decline
- HubSpot custom-property writeback for CRM visibility

### Customer health scoring
- Composite formula: usage + recency + CSAT + ticket-volume + NPS + deal-stage
- Risk flags (score < 0.4, 30d decline > 0.1, > 3 SLA breaches, last bug unresolved)
- Bidirectional CSP integration

### Multi-channel routing
- Email + chat (Intercom / Zendesk / Front / Plain / HelpScout)
- Slack Connect for B2B customer Slack channels
- Discord server #support / #bugs / #help-and-questions
- Microsoft Teams for enterprise customers
- Reddit subreddit + Twitter mentions monitoring
- Phone via Aircall / Dialpad / Twilio Flex transcription
- Unified inbox routing rules

### Conversation summarization for handoffs
- Intercom Fin AI / Front Smart Summarize / Zendesk Agent Copilot
- Claude fallback with structured template (problem / attempts / current state / next step / mood)

### Deflection metrics + content optimization
- Kapa / Inkeep deflection rate (% queries answered without ticket)
- Zero-result query → content gap audit
- Low-confidence answer → content quality audit

### Bug report normalization → Linear/Jira
- Structured template extraction from free-form ticket
- Sentry crash matching
- Customer-tier label + dollar-impact quantification
- Reverse-sync engineering status → ticket comments

### Feature request capture + product backlog
- Embedding-cluster feature requests over 30 days
- Productboard / Linear `feature-request` label with cluster size
- Notify-on-ship list per requester

### Auto-reply for common questions
- Intercom Fin AI Operator with Resolution Score gating
- Zendesk Answer Bot for legacy installs
- Kapa-trained model via webhook on conversation.created
- Escalate-to-human handoff on confidence < threshold

### Macro / canned response management
- Cross-platform macro library via Notion source-of-truth
- Vale brand-voice lint enforcement
- API push to all support platforms in sync

### VIP / enterprise prioritization
- CRM tier (HubSpot / Salesforce) read on conversation.created
- Override default routing for enterprise tier
- Dedicated Slack channel + CSM ping + tighter SLA

### On-call rotation for engineering escalation
- PagerDuty / Opsgenie incident creation
- Auto-route by topic = bug + urgency = critical
- Slack #on-call channel pin

### Post-incident customer communications
- Statuspage incident lifecycle (Investigating → Identified → Monitoring → Resolved)
- Affected-customer email within 1h for Enterprise tier
- Post-mortem within 5 business days for SEV-1 / SEV-2
- Slack #status-updates auto-pin

### Refund / credit policy execution
- Stripe MCP refund_create within threshold = auto
- Above threshold = Slack approval gate
- Audit log to warehouse table

### Multilingual support routing
- Language detect (in-platform or langdetect-cli fallback)
- Route to per-language team if available
- DeepL MCP auto-translate if not (bidirectional)
- Per-language macro library

### Trust & safety triage
- Atomic AI / Perspective API classifier
- Confidence-gated auto-escalation (≥ 0.8 → T&S queue)
- Customer-facing gentle decline; internal evidence chain
- Account-level action review

### Self-serve onboarding troubleshooting
- PostHog session replay for stuck-users
- HogQL cross-reference ticket-user-IDs with onboarding events
- Pattern recognition → product team handoff

### Community support
- Discord server hourly monitoring
- Reddit subreddit 6-hourly polling
- Forum (Discourse) daily via Firecrawl
- Crisis comment escalation < 1h

### Voice support
- Aircall / Dialpad / Twilio call transcription
- Auto-create ticket from transcription
- Same sentiment-scoring pipeline as text
- Post-call email recap with summary + next steps + ticket link

### Ticket reporting + executive dashboards
- Census / Hightouch sync → warehouse → dbt models
- Metabase / Looker / Hex dashboards
- Daily triage digest, weekly summary, monthly executive review
- North-Star: CSAT trend, deflection rate, escalation rate, time-to-resolution

---

## Execution status (SOTA — June 2026)

Every documented use case has a concrete SOTA execution mechanism. The "draft only, can't act" gaps are closed via shipped MCPs (Intercom / Zendesk / Linear / Sentry / Stripe / Slack / Discord / PostHog / DeepL / Twilio) and well-documented APIs (Kapa / Vitally / Delighted / Statuspage / PagerDuty / Aircall / Atomic AI) reachable through `cli-anything` curl.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Ticket triage (topic / urgency / sentiment) | Intercom Fin AI / Zendesk Intelligent Triage | `intercom-fin-ai-mcp` skill / `zendesk-mcp-ops` skill |
| Response template generation | Cluster + Vale + platform macro API | `cli-anything` + Vale lint + platform curl |
| FAQ generation from recurring tickets | Kapa.ai / Inkeep / Markprompt | `cli-anything` + Kapa API |
| KB management + drift detection | Notion + Lychee + Kapa | `notion-mcp` + `cli-anything uvx lychee` |
| Escalation rules + engineering handoff | Linear MCP / Jira MCP | `linear-mcp` / `jira-mcp` |
| SLA tracking + breach alerts | Platform SLA webhooks + Slack | `cli-anything` + `slack-mcp` |
| Sentiment analysis (per-ticket + cohort) | Loris / Klaus + warehouse / Claude fallback | `cli-anything` + `postgresql-mcp` |
| CSAT / CES / NPS measurement | Delighted / Survicate / Wootric | `cli-anything` curl |
| Churn prediction from support signals | Vitally / Catalyst / ChurnZero | `cli-anything` + Vitally API |
| Customer health scoring | Vitally / Catalyst / Totango / HubSpot fallback | `cli-anything` + writeback |
| Multi-channel routing | Front / Intercom / Zendesk + Slack + Discord + Teams | platform MCPs + `slack-mcp` + `discord-mcp-full` + `ms-teams-mcp` |
| Conversation summarization | Fin / Smart Summarize / Claude template | platform MCPs + LLM |
| Deflection metrics + content gap | Kapa / Inkeep analytics | `cli-anything` + Kapa API |
| Bug report normalization → Linear | Linear MCP + Sentry MCP + structured template | `linear-mcp` + `sentry-mcp` |
| Feature request capture + backlog | Productboard / Linear cluster | `cli-anything` + `linear-mcp` |
| Auto-reply (common questions) | Intercom Fin AI Resolution Score gating | `intercom-fin-ai-mcp` config |
| Macro / canned response mgmt | Platform macro APIs + Vale + Notion SoT | `cli-anything` + Vale + `notion-mcp` |
| VIP / enterprise prioritization | HubSpot tier read + platform routing override | `cli-anything` rule engine |
| On-call rotation | PagerDuty REST + Slack | `cli-anything` curl + `slack-mcp` |
| Post-incident comms (Statuspage) | Statuspage.io lifecycle API | `cli-anything` curl + `slack-mcp` |
| Refund / credit policy | Stripe MCP + Slack approval gate | `stripe-mcp` + `slack-mcp` |
| Multilingual support routing | DeepL MCP + langdetect + ESP routing | `deepl-mcp` + `cli-anything` |
| Trust & safety triage | Atomic AI / Perspective API | `cli-anything` curl |
| Self-serve onboarding troubleshooting | PostHog session replay + HogQL | `posthog-mcp` |
| Community support (Discord / Reddit / forums) | Discord MCP + Reddit MCP + Firecrawl | `discord-mcp-full` + `reddit-mcp` + `firecrawl-mcp` |
| Voice support (phone tickets) | Aircall / Dialpad / Twilio transcription | `cli-anything` + `twilio-mcp` |
| Ticket reporting + dashboards | Census/Hightouch → warehouse → BI | `postgresql-mcp` + `cli-anything` |
| Inbound chatbot (Plain / Chatwoot) | Plain GraphQL / Chatwoot REST | `cli-anything` curl |

---

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Kapa.ai / Inkeep AI doc Q&A | ⚠ | Paid API key required; Markprompt OSS fallback works immediately |
| Loris.ai / Klaus sentiment scoring | ⚠ | Paid API key required; Claude on transcript is the free fallback |
| Vitally / Catalyst / ChurnZero CSP | ⚠ | Paid SaaS; HubSpot custom property + dbt model is the free fallback |
| Atomic AI / TrustLab classifier | ⚠ | Paid SaaS; Google Perspective API is free (1 QPS) |
| PagerDuty on-call MCP | ⚠ | No PagerDuty MCP in catalog yet — `cli-anything` curl against PD REST works fully |
| Aircall / Dialpad voice transcription | ⚠ | Vendor-specific keys required; Twilio MCP + Whisper is self-hosted alt |
| Statuspage paid tier | ⚠ | Free tier limited; Better Stack Uptime is alt |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete execution path. The 5% residual is paid SaaS APIs the recipient owns (Kapa, Loris, Vitally, Atomic AI, Statuspage paid features, Aircall/Dialpad voice) — each has a documented free or open-source fallback. The previous "agent can categorize but not act" / "agent can suggest but not escalate" / "agent can read but not refund" gaps are all closed via shipped MCPs and `cli-anything` curl.

---

## When to use this agent

- "Triage today's open tickets and tag them"
- "Generate response templates for our top 20 ticket clusters"
- "Audit our KB for drift and content gaps"
- "Escalate this bug to engineering with a structured payload"
- "Set up SLA tracking with breach alerts to Slack"
- "Score sentiment on last week's closed tickets and show me the cohort trend"
- "Send CSAT surveys after every ticket close and route detractors to CSMs"
- "Feed support metrics to Vitally so health scores stay current"
- "Write a Statuspage incident update for the auth outage we just had"
- "Process this $150 refund per policy"
- "Route this German ticket to either the DE team or auto-translate"
- "Set up Discord community-channel monitoring with daily digest"

## When NOT to use this agent

- Expansion / upsell motion from happy support customers — hand off to `sales-agent`
- Deep feature-request prioritization (roadmap-grade RICE/MoSCoW) — hand off to `product-manager`
- Doc rewrites at scale (not just gap-fill) — hand off to `technical-writer`
- Testimonials, case studies, marketing from happy customers — hand off to `marketing-agent`
- In-product onboarding redesign — hand off to `product-manager` + `marketing-agent`
- Engineering work for the support tooling stack itself — hand off to `senior-python-engineer`
- Brand voice strategy at the agency-engagement level — `marketing-agent` starts; brand strategist specialist (v1) for full depth
- Legal disputes / chargebacks beyond standard refund policy — flag for legal sign-off
