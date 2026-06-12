# Customer Support Agent — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Triage playbook", "Response template playbook", "FAQ + KB playbook", "Escalation playbook", "Bug normalization template", "SLA + on-call playbook", "Sentiment + CSAT playbook", "Churn + health scoring playbook", "Incident comms playbook", "Refund + credit policy", "Multilingual routing playbook", "Trust & safety playbook", "Community support playbook", "Voice support playbook", "AI-slop catch list — support edition", "Antipattern catalog", "Routing rule template", "Macro voice rules", "Bug report template", "Escalation packet template", "Incident update template", "Statuspage incident lifecycle", "Health score formula", "Reporting + dashboard patterns", "SOTA tool reference", "SOTA execution playbook".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Ticket / inbox platforms this agent operates

- **Intercom** — chat + email + Fin AI Operator (SOTA for AI-first triage + auto-reply)
- **Zendesk** — full ticketing + Intelligent Triage + Sentiment + Macros + SLA Policies
- **Front** — multi-channel shared inbox + Smart Summarize + templates
- **Plain** — modern dev-first SaaS ticket platform (GraphQL-only)
- **HelpScout** — small-team email + chat
- **Chatwoot** — OSS alternative to Intercom / Zendesk
- **Crisp** — SMB chat-first
- **Kustomer** — Meta-owned omnichannel
- **Freshdesk** — Freshworks suite alt
- **Pylon** — B2B SaaS support (Slack-first customers)
- **Gladly** — voice-of-customer focused

### Engineering escalation platforms

- **Linear** — modern issue tracker (primary engineering destination)
- **Jira** — Atlassian incumbent
- **GitHub Issues** — open-source / dev-tools shops

### Real-time / community channels

- **Slack** — internal team triage + on-call ping + customer Slack Connect
- **Discord** — community servers + own product support channels
- **Microsoft Teams** — enterprise customer Teams Connect
- **Reddit** — subreddit monitoring (own product + competitor)
- **Twitter / X** — public mentions (read-only for support — outbound via marketing-agent)
- **Forums** — Discourse, etc. via Firecrawl + custom polling

### AI doc Q&A / knowledge AI

- **Kapa.ai** — paid, doc-Q&A-as-a-service with deflection analytics
- **Inkeep** — paid, similar surface
- **Mendable** — paid, embeddable
- **Markprompt** — OSS / freemium fallback
- **Atomic AI** — trust & safety adjacent
- **Notion** — KB source-of-truth + editorial workflow
- **Sphinx** / **Mintlify** / **Readme.com** / **Docusaurus** — KB rendering engines (hand off to `technical-writer`)

### Customer health / churn platforms (CSPs)

- **Vitally** — modern CS platform with rich support-signal ingestion
- **Catalyst** (now part of Totango) — enterprise CSP
- **ChurnZero** — retention-focused
- **Gainsight** — enterprise CSM workflow
- **Totango** — composable success platform
- **Custify** — SMB-friendly
- **Velaris** — modern entrant

### Sentiment / QA platforms

- **Loris.ai** — formerly Conversica; per-conversation sentiment + emotion classification
- **Zendesk QA (Klaus)** — cohort-level conversation QA scoring
- **MaestroQA** — alt cohort QA
- **Stylus AI** — newer entrant
- **Google Perspective API** — free toxicity / abuse signal

### Survey / NPS / CSAT / CES

- **Delighted** (Qualtrics) — CSAT + CES + NPS in one
- **Wootric** (InMoment) — incumbent
- **Survicate** — modern alt
- **Typeform** — generic survey with CSAT templates
- **Refiner** — in-product micro-surveys
- **Hotjar** — in-product + survey

### Voice / phone

- **Aircall** — modern voice-for-support
- **Dialpad** — voice + AI summarization
- **Twilio Flex** — programmable voice
- **Twilio (programmable voice/SMS)** — outbound + transcription

### Product analytics tied to support

- **PostHog** — open-source product analytics with session replay (SOTA for tying support tickets to user behavior)
- **Mixpanel** — alt product analytics
- **Amplitude** — alt + behavioral cohorts
- **FullStory** — session replay specialist
- **LogRocket** — JS-error-focused session replay
- **Sentry** — crash + error monitoring (links into bug normalization)

### Incident comms / status

- **Statuspage.io** (Atlassian) — public status page incumbent
- **Better Stack Uptime / Status** — modern alt
- **Instatus** — modern alt
- **FireHydrant** — incident-mgmt + status
- **PagerDuty** — on-call + incident lifecycle
- **Opsgenie** — Atlassian's on-call

### Refunds / payments

- **Stripe** — primary refund / credit execution
- **Recurly / Chargebee / Paddle** — subscription-billing alternatives

### Reverse-ETL + warehouse

- **Census** — Zendesk/Intercom → warehouse → CRM sync
- **Hightouch** — alt
- **dbt** — warehouse modeling layer
- **Metabase / Looker / Hex / Mode** — BI dashboard layer

---

## Triage playbook

### Inputs

- Ticket payload (channel, subject, body, attachments)
- Customer record (tier, language, prior tickets, deal value if available)
- Recent product release notes (to spot regressions)

### Triage decision tree

1. **Read fully.** No skim. Customer wrote something; honor it.
2. **Classify topic.** Auth / Billing / Bug / How-to / Feature request / Abuse / Other. Multi-label allowed.
3. **Classify urgency.** Critical (outage / payment failure / data loss) / High (workflow blocked) / Normal / Low (cosmetic).
4. **Classify sentiment.** Frustrated / Confused / Neutral / Satisfied / Delighted.
5. **Read customer record.** Tier (Enterprise / Growth / Starter / Free), language, last 5 tickets, last bug-encounter ticket.
6. **Route.** Apply rule: `(channel, tier, topic) → owner + SLA tier`.
7. **First response within SLA.** Even if it's "I'm looking into this — back within X" — never silent queue.
8. **Tag in platform.** Topic + urgency + sentiment + customer-tier + language. Tagged tickets are product signal; untagged ones are noise.

### Routing rule template

```yaml
# rule_id: ent_billing_email
priority: 100
when:
  channel: email
  customer.tier: enterprise
  topic: billing
then:
  assign_team: enterprise_billing
  sla_first_response_minutes: 60
  sla_resolution_minutes: 240
  slack_ping: '#cse-enterprise'
  notify_csm: true

# rule_id: free_bug_chat
priority: 50
when:
  channel: chat
  customer.tier: free
  topic: bug
then:
  assign_team: tier1_support
  sla_first_response_minutes: 1440  # 24h
  sla_resolution_minutes: 4320      # 72h
  require_bug_normalization: true
```

### Triage report template (per ticket)

```markdown
## Ticket [ID] — [subject]

**Channel:** [email/chat/slack/discord/phone/community]
**Customer:** [name] · Tier: [Ent/Growth/Starter/Free] · Language: [en/de/fr/...] · Health: [score]
**Topic:** [auth/billing/bug/how-to/feature/abuse]
**Urgency:** [Critical/High/Normal/Low]
**Sentiment:** [Frustrated/Confused/Neutral/Satisfied]
**Suggested owner:** [team / individual]
**SLA target:** First response [X min] / Resolution [Y min]

**Customer's question / problem:**
[1-2 sentence summary]

**Suggested action:**
- Macro: [macro_id if matches ≥ confidence threshold]
- OR Draft reply: [paste below]
- OR Escalate: [Linear/Jira issue type + customer-tier label]

**Notes for internal:**
[anything that helps the next agent, but don't show to customer]
```

---

## Response template playbook

### Cluster identification

1. **Export tickets** for last 30-90 days from platform API.
2. **Embed** ticket bodies with Voyage / OpenAI ada / Cohere embed.
3. **Cluster** via k-means or HDBSCAN; threshold ≥ 5 tickets per cluster.
4. **Label** each cluster with topic + most-common phrasing.
5. **Draft macro** per cluster — single voice, single concept.

### Macro voice rules

- **Lead with what's happening.** "I see the error you hit; here's what triggers it."
- **No "Sorry to hear that!" or "Apologies for the inconvenience!"** Sycophancy. Cut.
- **No "Thank you for your patience!"** Performative. Cut.
- **No "I completely understand."** You don't. Acknowledge specifically what they reported.
- **One concept per macro.** Don't combine workaround + status update + survey link.
- **Realistic next step.** "If this isn't resolved by X, reply and I'll escalate" — concrete.
- **Branded sign-off only if brand demands.** Don't invent one.

### Macro template

```markdown
## Macro: [macro_id] — [title]

**Trigger:** [topic + sentiment + tier combination]
**Cluster source:** [N tickets in last 30d]
**Voice notes:** [if special — language, tier]

---

[Macro body — 1-3 short paragraphs, ≤ 100 words ideally]

[Concrete next step — what the customer should do]

[Internal-only note: when to use, when NOT to use]
```

### Push to platforms

- **Zendesk:** `POST /api/v2/macros.json` with `actions` + `restriction`
- **Intercom:** `POST /macros` (REST API 2.10+)
- **Front:** `POST /templates` with `body` + `attachments`
- **HelpScout:** `POST /v2/saved_replies` with `text` + `mailboxes`
- **Plain:** `mutation createSnippet { ... }`

---

## FAQ + KB playbook

### Drift report

Weekly:
1. **Article freshness:** articles unviewed in 90d → flag for review or archive.
2. **Zero-result queries:** in-platform search log → top N unanswered → content gap.
3. **Top searched + lowest CTR:** existing articles users can't find or don't trust.
4. **Dead links:** `cli-anything uvx lychee https://kb.brand.com/` weekly cron.

### Content gap audit

- Cross-reference top ticket clusters (last 30d) with existing KB articles.
- If cluster topic has no article → draft new.
- If article exists but cluster persists → article is broken (wrong, hidden, or unhelpful).

### KB article template

```markdown
# [Article title — answers a user query verbatim]

[Lead paragraph — 1-2 sentences. What is this article and who is it for.]

## Quick answer (TL;DR)

[The exact resolution in ≤ 50 words.]

## Detailed walkthrough

[Step-by-step, with screenshots placeholders / video embed.]

## Common errors

- **Error:** [exact error text]
  **Cause:** [...]
  **Fix:** [...]

## Still stuck?

[Link to chat / email / community.]

---
*Last reviewed: YYYY-MM-DD by [author]. Source tickets: [#1234, #5678]*
```

---

## Escalation playbook

### When to escalate

- Reproducible bug + customer reports it
- Severity matches escalation criteria (e.g., affects > N customers, > $X revenue, security implication, data loss, P0 / P1 outage)
- Customer tier matches (e.g., enterprise tier auto-escalates for any bug)
- Feature request with cluster size ≥ 5 in 30d

### Bug normalization template

```markdown
# Bug Report — [short title]

## Customer
- Name: [name]
- Email: [email]
- Tier: [Enterprise/Growth/Starter/Free]
- Workspace ID / org ID: [id]
- Detected on plan / SKU: [if relevant]
- Ticket ID: [#1234]

## What they expected
[1-2 sentences from customer's words]

## What actually happened
[1-2 sentences — concrete observable behavior]

## Steps to reproduce
1. [...]
2. [...]
3. [...]

## Environment
- Browser: [Chrome 124 / Safari 17.5 / Firefox 126]
- OS: [macOS 14.5 / Windows 11 / Linux Ubuntu 22.04]
- App version: [version]
- Network: [WiFi / 4G / corporate]
- Region / locale: [if relevant]

## Frequency
- [ ] First report
- [ ] Cluster (N reports in last 30d)
- [ ] Persistent / ongoing

## Customer impact
- [ ] Cosmetic / annoyance only
- [ ] Workflow inconvenience (workaround exists)
- [ ] Workflow blocked (no workaround)
- [ ] Data loss / corruption
- [ ] Security implication

## Dollar impact / ARR at risk
- Customer ARR: $X
- Number of users affected: N

## Sentry match
- Sentry issue: [link if found]
- Error fingerprint: [hash]
- First seen: [timestamp]
- Affected users (Sentry): [N]

## Attachments
- [screenshot / HAR file / log / video]

## Workaround offered to customer
[exact steps the customer can take now]
```

### Escalation packet template (for Linear / Jira)

- **Title:** `[BUG] [Short user-visible description] — affects [customer-tier]`
- **Description:** Paste bug normalization template
- **Labels:** `support-escalated`, `bug`, `tier-<enterprise|growth|starter|free>`, `severity-<crit|high|med|low>`
- **Customer impact field:** `N users affected, $X ARR at risk`
- **Ticket back-link:** Zendesk / Intercom URL
- **Sentry link:** if matched
- **Priority:** mapped from severity × customer-tier

### Reverse-sync

When the engineering issue state changes:
- `In Progress` → ticket internal note: "Engineering is investigating. ETA when available."
- `In Review` → ticket internal note: "Fix in review."
- `Done` → ticket customer-facing reply: "Fix shipped in version X. Please retest and let us know."

---

## SLA + on-call playbook

### SLA tier table (defaults — adjust per recipient)

| Tier | First response | Resolution | Channel coverage |
|---|---|---|---|
| Enterprise | 1h | 4h | 24/7 incl. weekends |
| Growth | 4h | 24h | Business hours + on-call for crit |
| Starter | 8h | 48h | Business hours |
| Free | 24h | 72h | Best effort |

Override tier for `urgency=Critical`: all tiers go to 1h first response.

### Breach response

- **30min before breach:** Ping owner via Slack `@user`.
- **At breach:** Auto-escalate to lead + post to `#sla-breach` channel.
- **For Critical tier customers:** PagerDuty incident if no first response within 30min.

### Weekly SLA report

```markdown
## SLA Report — Week of YYYY-MM-DD

| Tier | Tickets | First-Response Hit % | Resolution Hit % | Breaches |
|---|---|---|---|---|
| Enterprise | N | X% | Y% | Z |
| Growth | N | X% | Y% | Z |
| Starter | N | X% | Y% | Z |
| Free | N | X% | Y% | Z |

**Top reasons for breach:**
1. [reason] — N breaches
2. [reason] — N breaches

**Action items:**
- [...]
```

---

## Sentiment + CSAT playbook

### Per-ticket sentiment scoring

- **SOTA:** Loris.ai `/v1/transcripts` or Klaus `/api/v1/quality-scores`
- **Free fallback:** Claude on transcript with this prompt:
  ```
  Score this conversation 0-100 on customer sentiment, where 0=furious and 100=delighted. Also classify emotion as one of: angry, frustrated, confused, neutral, satisfied, delighted. Return JSON.
  ```
- Store score per ticket; aggregate cohort weekly.

### Cohort sentiment trend

- Pull weekly aggregate: avg sentiment score, % detractors (≤ 6), % promoters (≥ 9 if NPS, ≥ 80 if 0-100 scale).
- Alert if cohort drops > 20% week-over-week.
- Cross-reference with product releases — sentiment drops after release X = likely regression.

### CSAT / CES / NPS instrumentation

- **CSAT:** "How would you rate your support experience?" (1-5 stars) — send within 1h of ticket close.
- **CES:** "How easy was it to get your problem resolved?" (1-7 scale) — send within 24h of ticket close.
- **NPS:** "How likely are you to recommend X?" (0-10) — send quarterly or post-onboarding milestone, NOT post-support-ticket.

### Survey delivery

- **Delighted:** `POST /v1/people` with `survey_type`, `email`, `delay`, `properties`.
- **Survicate:** `POST /v3/contacts` + workflow trigger.
- **Wootric:** similar REST surface.

### Detractor response playbook

1. CSAT ≤ 6 (or comparable threshold per survey type) → auto-route to CSM within 1h.
2. CSM reads original ticket + survey comment.
3. CSM reaches out personally — "Saw your feedback; what would have made this better?"
4. Log outcome: recovered / churned / no-response.

---

## Churn + health scoring playbook

### Health score formula (composite — adjust weights per business)

```
Health = 0.40 * (product_usage_normalized)
      + 0.20 * (last_login_recency_score)
      + 0.15 * (csat_avg_90d)
      + 0.10 * (1 - support_ticket_volume_normalized)  # more tickets = worse, generally
      + 0.10 * (nps_score_normalized)
      + 0.05 * (deal_stage_score)
```

Where:
- `product_usage_normalized`: 0-1, based on platform's PostHog activity score
- `last_login_recency_score`: 1 if logged in last 7d, 0.7 if 14d, 0.4 if 30d, 0 if > 60d
- `csat_avg_90d`: avg CSAT score / max
- `support_ticket_volume_normalized`: tickets in last 90d / customer baseline (more isn't always bad — context)
- `nps_score_normalized`: latest NPS / 10
- `deal_stage_score`: renewal-stage weighting

### Risk flags

- Score < 0.4 → **At-risk.** Fire CSM playbook.
- Score declined > 0.1 in 30d → **Trending down.** CSM reach-out within 7d.
- > 3 SLA breaches in 30d → **Support-driven risk.** Internal review on root cause.
- Last bug-encounter ticket within 14d AND unresolved → **Product-driven risk.** Cross-flag with engineering.

### Feed to CSPs

- **Vitally:** `POST /resources/customers/<id>/traits` with `support_tickets_90d`, `avg_csat`, `sla_breach_count`, `last_bug_at`.
- **Catalyst:** similar `companies/<id>/properties` PATCH.
- **Totango / Gainsight / ChurnZero:** vendor-specific but all accept custom-property PATCH via REST.

### Free fallback (no CSP)

- Use HubSpot custom properties as poor-man's health score.
- `support_health_score` custom property on company; computed via dbt model nightly; surfaced on company record.

---

## Incident comms playbook

### Statuspage incident lifecycle

| State | When | Who sees |
|---|---|---|
| Investigating | Within 15min of incident confirmation | Public + Twitter + Slack |
| Identified | Root cause known, fix in progress | Same |
| Monitoring | Fix deployed, watching for stability | Same |
| Resolved | Confirmed stable post-fix | Same + post-mortem queue |

### Initial update template (Investigating)

```markdown
**Component:** [API / Dashboard / Auth / Webhooks / ...]
**Impact:** [partial outage / degraded performance / major outage]
**State:** Investigating

We're investigating reports of [exact symptom — e.g., "elevated error rates on the API"].
We'll update again within [30min].

— [team name]
```

### Identified update template

```markdown
**State:** Identified

We've identified the cause as [brief, non-incriminating explanation — "an issue with our [database / cache / upstream provider]"].
A fix is being prepared. ETA [if known, else "we'll update when fix is rolled out"].

— [team name]
```

### Monitoring update template

```markdown
**State:** Monitoring

We've deployed a fix and the system is recovering. We're monitoring closely and will update when fully resolved.

— [team name]
```

### Resolved update template

```markdown
**State:** Resolved

This issue has been resolved. We'll publish a full post-mortem within [X business days].
If you're still experiencing issues, please contact support.

— [team name]
```

### Affected-customer email (within 1h of incident start, for Enterprise tier)

- Personalized salutation
- One-paragraph what happened in plain language
- One-paragraph current status + ETA
- One-paragraph what the customer can do (workaround / nothing / specific action)
- Sign-off with CSM name + escalation channel

### Post-mortem template (within 5 business days for SEV-1 / SEV-2)

```markdown
# Post-Mortem: [Incident Title]

**Date:** YYYY-MM-DD
**Duration:** HH:MMm
**Severity:** SEV-1 / SEV-2 / SEV-3
**Customer impact:** [N customers affected, $X ARR at risk]

## Summary

[1 paragraph — what happened, what we did, how it ended.]

## Timeline

| Time (UTC) | Event |
|---|---|
| 14:23 | First alert: error rate spike |
| 14:25 | On-call engineer paged |
| 14:32 | Investigating posted to Statuspage |
| 14:47 | Root cause identified |
| 15:02 | Fix deployed |
| 15:15 | Resolved posted |

## Root cause

[Technical explanation — what went wrong.]

## Why our safeguards didn't catch it

[Honest assessment — gaps in monitoring, test coverage, deploy process.]

## What we're doing about it

- [ ] Action item 1 (owner: X, due: YYYY-MM-DD)
- [ ] Action item 2 (owner: Y, due: YYYY-MM-DD)
- [ ] Action item 3 (owner: Z, due: YYYY-MM-DD)

## Credits applied

[If applicable — credit amounts to affected customers per policy.]
```

---

## Refund + credit policy

### Auto-approve gate

- **Refund ≤ $X (default $100):** Auto-execute via Stripe with internal note. Log to warehouse.
- **Credit ≤ $Y (default $250):** Auto-apply via Stripe / billing platform.

### Escalation gate

- **Refund > $X:** Slack `#refund-approval` with `[customer, amount, reason, ticket]`; await lead approval.
- **Refund > $Z (default $5000):** Email lead + CFO; written approval required.

### Stripe refund execution

```bash
# via stripe-mcp tool: refund_create(charge_id, amount, reason)
# OR cli-anything:
curl -X POST https://api.stripe.com/v1/refunds \
  -u $STRIPE_SECRET_KEY: \
  -d charge=ch_XXX \
  -d amount=10000 \
  -d reason=requested_by_customer
```

### Audit log

Every refund/credit logged to warehouse table `support_refunds`:
- `customer_id`, `ticket_id`, `amount`, `reason`, `approver`, `executed_at`, `stripe_refund_id`

---

## Multilingual routing playbook

### Detect language

- **In-platform:** Intercom / Zendesk detect language on the ticket; trust theirs first.
- **Fallback:** `cli-anything uvx langdetect-cli` on ticket body.

### Routing decision

- **Per-language team available?** Route to native-speaker team.
- **No per-language team?** Auto-translate inbound → English via DeepL MCP → English-speaking team responds → translate outbound back to source language.

### DeepL execution

```bash
# via deepl-mcp: translate(text, target_lang='EN')
# OR cli-anything:
curl https://api-free.deepl.com/v2/translate \
  -d auth_key=$DEEPL_KEY \
  -d text="..." \
  -d source_lang=DE \
  -d target_lang=EN
```

### Per-language macro library

- Maintain Notion DB with macros tagged by language.
- Translation memory: don't re-translate the same macro twice — store the human-edited final.

---

## Trust & safety playbook

### Classifier inputs

- **Atomic AI:** `/v1/classify` returns `abuse | fraud | t&c-violation | spam` confidence scores.
- **Google Perspective API:** `analyze` returns `TOXICITY`, `SEVERE_TOXICITY`, `IDENTITY_ATTACK`, `INSULT`, `PROFANITY`, `THREAT` confidence scores.

### Auto-escalation thresholds

- `confidence ≥ 0.8` → route to T&S queue automatically + internal-only flag.
- `0.5 ≤ confidence < 0.8` → human review queue.
- `confidence < 0.5` → standard triage continues.

### Customer-facing reply guidance

- **Gentle decline.** Don't accuse. "I can't help with this request" is enough.
- **No commitments.** Don't promise investigation timeline (gives the bad actor leverage).
- **No internal information.** Don't reveal classifier scores, internal team names, vendor names.
- **Evidence chain.** Internal note carries full classification result + transcript + decision rationale.

### Account-level action

- **Suspension:** documented internal review before action.
- **Banning:** lead + legal review for paying customers.
- **Refund on ban:** per policy (typically pro-rata for paying customers).

---

## Community support playbook

### Channels

- **Own Discord server:** monitor #support / #bugs / #help-and-questions hourly via `discord-mcp-full list_messages`.
- **Subreddit /r/yourproduct:** monitor via `reddit-mcp` every 6h.
- **External forums (Discourse, etc.):** monitor via `firecrawl-mcp` daily.
- **Twitter / X / Bluesky mentions:** read-only; outbound owned by marketing-agent.

### Response patterns

- **Simple question:** answer inline; cross-link to KB article if exists.
- **Bug report in community:** acknowledge inline, open private ticket via DM, run bug normalization.
- **Feature request:** acknowledge inline, log to Productboard / Linear `feature-request` cluster, add requester to "notify on ship" list.
- **Crisis comment (viral negative):** escalate to lead within 1h. Don't engage publicly without playbook.

### Discord-specific rules

- Use threads, not channel pings, for ticket-level discussion.
- Role tag for severity (e.g., `@bug-triage` for confirmed bugs).
- Auto-tag VIPs / Enterprise (via Discord role sync from CRM).

---

## Voice support playbook

### Transcription

- **Aircall:** `GET /v1/calls/<id>/transcription` after call ends.
- **Dialpad:** `GET /api/v2/calls/<id>/transcription`.
- **Twilio Programmable Voice:** record + transcribe via `transcribe-callback` + Whisper.

### Ticket creation

- Auto-create ticket in Zendesk/Intercom from transcription with `channel=voice`, `subject=Call from [name]`, body = transcription, audio file URL attached.

### Sentiment + summary

- Same sentiment-scoring pipeline as text tickets (Loris / Klaus / Claude).
- Auto-generated summary via Claude or platform-native summarizer.

### Post-call macro

- Send post-call email recap to customer with summary + next steps + ticket link.

---

## AI-slop catch list — support edition

Before any auto-reply / macro / draft ships, strip:

**Sycophantic openers / closers:**
- "Sorry to hear that!" — cut
- "Apologies for the inconvenience!" — cut
- "Thank you for your patience!" — cut
- "Great question!" — cut
- "I completely understand!" — cut (you don't, and saying so feels fake)

**Performative empathy:**
- "We hear you" — cut
- "We're here for you" — cut
- "Your concern is our priority" — cut

**Corporate jargon:**
- "Leverage" → "use"
- "Utilize" → "use"
- "Going forward" → cut
- "At your earliest convenience" → cut, give a concrete next step instead

**Fake-ETA language:**
- "Soon" — replace with concrete date or "no ETA"
- "Shortly" — replace with concrete time
- "In the near future" — cut
- "We're working on it" — only if it's true and you have a Linear ticket

**Stock transitions / structure:**
- "I'd be happy to..." — cut, just do the thing
- "Please let me know if..." — usually performative; cut unless concretely needed
- "Hope this helps!" — cut

**What stays protected:**
- Customer's exact wording (when paraphrasing)
- Technical terms and error text
- Concrete steps and timelines
- Brand voice cues from voice doc

---

## Antipattern catalog

### Antipattern 1: Fabricated ETA

**BAD:**
> Thanks for reporting this! Engineering is on it — should be fixed soon!

**Why bad:** "Soon" is meaningless and a lie when you have no ticket open with engineering.

**GOOD:**
> Thanks — I've logged this as ENG-1234. No ETA yet from engineering; I'll update by EOD Friday whether it's still no-ETA or has a target.

**Why better:** Honest. Has a concrete next-update commitment.

---

### Antipattern 2: Performative empathy without action

**BAD:**
> I completely understand how frustrating this must be! I'm so sorry you're experiencing this. We're here for you and will do everything we can to help.

**Why bad:** All performative. Zero action. Zero information.

**GOOD:**
> I see the error you hit — that's a known issue when [trigger]. Workaround: [exact steps]. Tracking it as ENG-1234; I'll let you know when fixed.

**Why better:** Specific recognition + workaround + tracking commitment.

---

### Antipattern 3: Free-form bug escalation to engineering

**BAD:**
> @engineering, customer says the app is broken. Can you look?

**Why bad:** Engineering can't action this. They'll bounce it back, and the customer waits.

**GOOD:** Bug normalization template filled fully. Linear issue with structured fields. Customer impact quantified. Sentry match attached.

**Why better:** Engineering can repro and triage immediately.

---

### Antipattern 4: Closing a ticket prematurely

**BAD:**
> I haven't heard back, so I'm closing this. Feel free to reopen!

**Why bad:** Customer may not have seen your reply. Closure abandons rather than helps.

**GOOD:** "I haven't heard back in 7 days; I'm assuming this is resolved. If it isn't, just reply and I'll pick it back up — no need to re-explain. I'll close in 3 days if no response."

**Why better:** Concrete timeline + low-friction reopen path.

---

### Antipattern 5: Mass-broadcasting "we're working on it" without confirmation

**BAD:** Customers asking about a missing feature; agent posts on Statuspage: "We're working on improvements to this feature, stay tuned!"

**Why bad:** Engineering isn't actually working on it. Now you owe a feature you can't deliver.

**GOOD:** Acknowledge with reality. "This isn't currently on our roadmap; I've logged the request and will let you know if priorities shift."

**Why better:** Honest. Doesn't compound the trust debt.

---

### Antipattern 6: Exposing internal information in customer reply

**BAD:**
> Our backend team is dealing with a Redis issue in our `cache-prod-eu-west-1` cluster, and the Sentry trace shows a timeout in `service/cart.py:142`.

**Why bad:** Internal infrastructure details, vendor names, file paths. Privacy risk + security risk + confuses customer.

**GOOD:** "We're working on a database issue that's causing the error you saw. Should be resolved within X hours."

**Why better:** Honest about scope, no internal exposure.

---

## Reporting + dashboard patterns

### Daily triage digest

- Tickets opened / closed in last 24h
- SLA breaches in last 24h
- Critical / High urgency open
- Top topic clusters
- Sent to support lead via `gmail-mcp` or Slack

### Weekly support summary

- Per-team metrics: volume, FRT, resolution time, CSAT
- Per-tier metrics: same
- Top 10 topic clusters with trend
- Top 5 escalations (status)
- Top 5 churn-risk customers (from health score)
- Open incident comms

### Monthly executive review

- North-Star: CSAT trend, ticket volume per active customer, time-to-resolution
- Deflection rate (% of queries answered by AI / KB / community without ticket)
- Cost-per-ticket trend
- Escalation rate (% of tickets going to engineering)
- Top 5 root causes (driving most tickets)
- Recommended action items

### Census / Hightouch sync for warehouse

- Zendesk / Intercom → warehouse via Census sync.
- dbt models: `tickets`, `sla_breaches`, `csat_responses`, `escalations`, `customer_health`.
- Metabase / Looker / Hex dashboards downstream.

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Headings are intentionally search-friendly. Every entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle (Round 2 populates the SKILL.md contents).

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Intercom Fin AI MCP

Intercom's Fin AI Operator (GA Mar 2026). Triage + auto-reply + conversation summarization in one. Resolution Score (0-1) gates whether Fin auto-replies or escalates. Multi-language coverage for top 20 languages. Macros and templates via API.

- **Skill:** `skills/intercom-fin-ai-mcp/SKILL.md`
- **Endpoint:** `https://api.intercom.io/`
- **Auth:** OAuth Personal Access Token → `INTERCOM_TOKEN`
- **Key calls:** `list_conversations`, `assign_conversation`, `run_assignment_rules`, `get_conversation_summary`, `create_macro`
- **Source:** https://www.intercom.com/help/en/articles/9442290-fin-ai-operator

### Zendesk MCP ops

Zendesk full ticketing surface. Intelligent Triage classifies topic + intent + sentiment. Macros API for canned-response management. SLA Policies API for breach tracking. Triggers + Automations for routing rules.

- **Skill:** `skills/zendesk-mcp-ops/SKILL.md`
- **Endpoint:** `https://<subdomain>.zendesk.com/api/v2/`
- **Auth:** API token + email → `ZENDESK_TOKEN`
- **Key calls:** `list_tickets`, `update_ticket`, `create_macro`, `apply_macro`, `list_slas`, `create_trigger`
- **Source:** https://developer.zendesk.com/api-reference/

### Front multichannel inbox

Front unifies email + chat + SMS + WhatsApp + Twitter into one inbox. Smart Summarize auto-generates conversation summaries for handoff. Templates API for shared response library.

- **Skill:** `skills/front-multichannel-inbox/SKILL.md`
- **Endpoint:** `https://api2.frontapp.com/`
- **Auth:** Bearer token → `FRONT_TOKEN`
- **Key calls:** `list_conversations`, `assign_conversation`, `create_template`, `smart_summarize`
- **Source:** https://dev.frontapp.com/reference

### Plain modern tickets

Plain — dev-first SaaS ticket platform, GraphQL-only API. Best fit for technical SaaS supporting dev customers. Threads + Snippets + custom fields + workspace API.

- **Skill:** `skills/plain-modern-tickets/SKILL.md`
- **Endpoint:** `https://core-api.uk.plain.com/graphql/v1`
- **Auth:** API key → `PLAIN_API_KEY`
- **Key calls:** GraphQL `createThread`, `replyToThread`, `assignThread`, `createSnippet`, `searchCustomers`
- **Source:** https://plain.com/docs/api

### HelpScout MCP

HelpScout REST API for small-team email + chat support. Saved Replies API for canned responses. Conversations API for ticket lifecycle.

- **Skill:** `skills/helpscout-mcp/SKILL.md`
- **Endpoint:** `https://api.helpscout.net/v2/`
- **Auth:** OAuth → `HELPSCOUT_TOKEN`
- **Key calls:** `list_conversations`, `update_conversation`, `create_saved_reply`, `create_thread`
- **Source:** https://developer.helpscout.com/mailbox-api/

### Kapa AI doc Q&A

Kapa.ai — paid doc-Q&A-as-a-service. Trains on your docs + tickets corpus; deflection analytics; content-gap report (top zero-result queries). Inkeep is a peer.

- **Skill:** `skills/kapa-ai-doc-qa/SKILL.md`
- **Endpoint:** `https://api.kapa.ai/`
- **Auth:** API key → `KAPA_API_KEY`
- **Key calls:** `query`, `get_deflection_metrics`, `get_zero_result_queries`, `get_low_confidence_answers`
- **Source:** https://docs.kapa.ai/api

### Notion knowledge base management

Notion as KB editorial source-of-truth + drift detection. Pair with Lychee for dead-link sweep. Cross-reference with platform Help Center via API.

- **Skill:** `skills/notion-knowledge-base-management/SKILL.md`
- **Endpoint:** `notion-mcp` (already in agent.yaml)
- **Key calls:** `query_database(filter='last_reviewed < 90d')`, `update_page`, `create_page`
- **Lychee:** `cli-anything uvx lychee https://kb.brand.com/`
- **Source:** https://lychee.cli.rs/ + Notion API

### Escalation Linear + Jira engineering

Structured bug normalization → engineering issue. Linear MCP for modern shops; Jira MCP for Atlassian shops. Customer-tier label preserves business context.

- **Skill:** `skills/escalation-linear-jira-engineering/SKILL.md`
- **Linear endpoint:** Linear MCP (already in agent.yaml)
- **Jira endpoint:** Jira MCP (already in agent.yaml)
- **Key calls:** `create_issue`, `update_issue`, `link_external_ticket`
- **Source:** https://developers.linear.app/docs + https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/

### Sentiment analysis + cohort trends

Loris.ai / Klaus / Stylus per-ticket sentiment scoring. Cohort weekly trend via warehouse. Claude fallback when no paid tool.

- **Skill:** `skills/sentiment-analysis-cohort-trends/SKILL.md`
- **Loris endpoint:** `https://api.loris.ai/v1/transcripts`
- **Klaus endpoint:** `https://api.klausapp.com/v1/`
- **Key calls (Loris):** `analyze_transcript`, `bulk_score`
- **Free fallback:** Claude on transcript with structured-JSON prompt
- **Source:** https://loris.ai/ + https://klausapp.com/api

### CSAT / CES / NPS instrumentation

Delighted (Qualtrics) for one-stop CSAT/CES/NPS. Survicate as alt. Detractor auto-routing to CSM.

- **Skill:** `skills/csat-ces-nps-instrumentation/SKILL.md`
- **Delighted endpoint:** `https://api.delighted.com/v1/`
- **Auth:** API key → `DELIGHTED_API_KEY`
- **Key calls:** `create_person(email, survey_type, delay)`, `list_responses`
- **Source:** https://app.delighted.com/docs/api

### Churn prediction support signals

Feed support metrics into Vitally / Catalyst / Totango / ChurnZero. Health score declines fire CSM playbook.

- **Skill:** `skills/churn-prediction-support-signals/SKILL.md`
- **Vitally endpoint:** `https://api.vitally.io/resources/`
- **Auth:** API key → `VITALLY_API_KEY`
- **Key calls:** `POST /customers/<id>/traits`, `GET /customers/<id>` (health-score readback)
- **Source:** https://docs.vitally.io/reference

### Customer health scoring Vitally + Catalyst

Bidirectional integration with CSP. Read health score; write back to HubSpot custom property; Slack alert on threshold.

- **Skill:** `skills/customer-health-scoring-vitally-catalyst/SKILL.md`
- **Free fallback:** HubSpot custom property + dbt model
- **Source:** https://docs.vitally.io/reference + https://help.catalyst.io/

### Multichannel routing rules

YAML rule engine: `(channel, tier, topic) → (owner, SLA tier, Slack ping)`. Deterministic — same input = same routing.

- **Skill:** `skills/multichannel-routing-rules/SKILL.md`
- **Mechanism:** YAML rules file; on `conversation.created` webhook, evaluate; route via platform API + `slack-mcp`/`discord-mcp-full` notify

### Slack / Discord community support

Discord server #support + Reddit subreddit monitoring + Slack internal triage. Daily / hourly cron polling.

- **Skill:** `skills/slack-discord-community-support/SKILL.md`
- **MCPs:** `slack-mcp`, `discord-mcp-full`, `discord-mcp`, `reddit-mcp`, `firecrawl-mcp`

### Deflection metrics + content gap

Kapa / Inkeep deflection analytics — % queries answered without ticket. Zero-result queries → content gaps → new KB drafts.

- **Skill:** `skills/deflection-metrics-content-gap/SKILL.md`
- **Endpoint:** `https://api.kapa.ai/v1/analytics`
- **Cross-ref:** `notion-mcp` KB DB vs ticket clusters

### Incident customer comms Statuspage

Statuspage.io incident lifecycle (Investigating → Identified → Monitoring → Resolved). Slack pin via `slack-mcp`. Affected-customer email batch via `gmail-mcp`.

- **Skill:** `skills/incident-customer-comms-statuspage/SKILL.md`
- **Endpoint:** `https://api.statuspage.io/v1/`
- **Auth:** API key → `STATUSPAGE_API_KEY`
- **Key calls:** `POST /pages/<id>/incidents`, `PATCH /incidents/<id>`, `POST /incidents/<id>/updates`
- **Source:** https://developer.statuspage.io/

### Bug report normalization Linear

Free-form ticket → structured bug template. Sentry MCP search for matching crash events. Linear issue with customer-tier label + ticket back-link.

- **Skill:** `skills/bug-report-normalization-linear/SKILL.md`
- **MCPs:** `linear-mcp`, `sentry-mcp`
- **Output:** Linear issue with structured description + Sentry link + customer-impact label

### Trust & safety abuse triage

Atomic AI / TrustLab / Perspective API classifier. Confidence-gated auto-escalation. Gentle customer-facing reply; internal evidence chain.

- **Skill:** `skills/trust-safety-abuse-triage/SKILL.md`
- **Endpoints:** `https://api.atomic.ai/v1/classify`, `https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze`
- **Source:** https://atomic.ai/ + https://perspectiveapi.com/

### VIP enterprise prioritization

CRM tier (HubSpot / Salesforce) → SLA tier + routing. Dedicated channel + tighter SLA + CSM ping.

- **Skill:** `skills/vip-enterprise-prioritization/SKILL.md`
- **Mechanism:** `cli-anything` on `conversation.created` → HubSpot lookup → if `tier=enterprise`, override default routing

### Voice support Aircall / Dialpad / Twilio

Phone call transcription → ticket creation. Sentiment + summary same as text tickets. Post-call email recap.

- **Skill:** `skills/voice-support-aircall-dialpad-twilio/SKILL.md`
- **Endpoints:** Aircall `/v1/calls/<id>/transcription`, Dialpad `/api/v2/calls/<id>/transcription`, Twilio MCP for outbound
- **Source:** https://developer.aircall.io/api-references/

### PostHog session replay (onboarding troubleshooting)

PostHog MCP + session replay surfaces where new users get stuck. HogQL queries to cross-reference ticket user-IDs with onboarding events.

- **MCP:** `posthog-mcp` (already in agent.yaml)
- **Key calls:** `query` (HogQL), `get_session_recording`

### DeepL multilingual

`deepl-mcp` for translation. Multi-language ticket routing + per-language macro library.

- **MCP:** `deepl-mcp` (already in agent.yaml)

### Stripe refund execution

`stripe-mcp` for refund / credit. Policy gate to Slack approval above threshold.

- **MCP:** `stripe-mcp` (already in agent.yaml)
- **Key calls:** `refund_create(charge_id, amount, reason)`

### PostgreSQL warehouse + alerts

`postgresql-mcp` for warehouse queries (SLA breach rate, cohort sentiment, health scores). Cron-scheduled alerts via Slack.

- **MCP:** `postgresql-mcp` (already in agent.yaml)
- **Use cases:** SLA breach detection, weekly sentiment cohort report, dashboard backing tables

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| Triage these inbound tickets | `intercom-fin-ai-mcp` or `zendesk-mcp-ops` | Pick the one matching their platform |
| Draft response templates | `intercom-fin-ai-mcp` / `zendesk-mcp-ops` + Vale | Cluster first, then draft |
| Find content gaps in our KB | `notion-knowledge-base-management` + `deflection-metrics-content-gap` | Cross-ref ticket clusters with KB |
| Escalate this bug to engineering | `bug-report-normalization-linear` + `escalation-linear-jira-engineering` | Normalize before creating Linear issue |
| Track our SLAs | `multichannel-routing-rules` + `postgresql-mcp` warehouse | Pull SLA policies + breach status |
| Score sentiment on closed tickets | `sentiment-analysis-cohort-trends` | Loris/Klaus or Claude fallback |
| Send CSAT surveys after ticket close | `csat-ces-nps-instrumentation` | Delighted/Survicate webhook |
| Flag at-risk customers | `churn-prediction-support-signals` + `customer-health-scoring-vitally-catalyst` | Health score declining |
| Write a Statuspage incident update | `incident-customer-comms-statuspage` | Use lifecycle template |
| Process a refund for this customer | `stripe-mcp` + policy gate | Within threshold = auto; above = Slack approval |
| Handle a non-English ticket | `deepl-mcp` multilingual routing | Detect → translate or route |
| Triage potential abuse | `trust-safety-abuse-triage` | Classifier + evidence chain |
| Monitor our Discord community | `slack-discord-community-support` | `discord-mcp-full list_messages` |
| Set up the support runbook | `notion-knowledge-base-management` | Notion DB + drift report |
| Build a support metrics dashboard | `postgresql-mcp` + warehouse + Census/Hightouch | Reverse-ETL → dbt → Metabase |
| Process voice/phone tickets | `voice-support-aircall-dialpad-twilio` | Transcription → ticket → sentiment |

---

## Updated mappings — replace outdated patterns

Where role.md sections name generic categories ("ticket platform", "AI doc Q&A", "CSP"), the SOTA replacement is:

- **Ticket platform** (Zendesk / Intercom / Front / Plain / HelpScout / Chatwoot / Freshdesk) → **Intercom Fin AI** for AI-first new shops; **Zendesk Intelligent Triage** for incumbents; **Front** for shared-inbox teams; **Plain** for dev-first SaaS.
- **AI doc Q&A** (Kapa / Inkeep / Mendable / Markprompt) → **Kapa.ai** primary, **Markprompt** as OSS fallback.
- **CSP** (Vitally / Catalyst / ChurnZero / Gainsight / Totango / Custify / Velaris) → **Vitally** for modern SaaS, **Catalyst (Totango)** for enterprise, **HubSpot custom property** for free fallback.
- **Sentiment scoring** (Loris / Klaus / Stylus / MaestroQA) → **Loris.ai** for per-ticket SOTA; **Claude on transcript** for free fallback.
- **Survey / NPS** (Delighted / Wootric / Survicate / Typeform / Refiner) → **Delighted** primary, **Survicate** alt.
- **Incident comms** (Statuspage / Better Stack / Instatus / FireHydrant) → **Statuspage.io** SOTA.
- **On-call** (PagerDuty / Opsgenie / FireHydrant) → **PagerDuty** primary (via `cli-anything` curl until PD MCP ships).
- **Engineering escalation** (Linear / Jira / GitHub Issues) → **Linear MCP** primary, **Jira MCP** for Atlassian shops, **GitHub Issues** for OSS / dev-tools.
- **Refunds** (Stripe / Recurly / Chargebee / Paddle) → **Stripe MCP** SOTA, others via `cli-anything` curl.
- **Multilingual** (DeepL / Klue / Crowdin / Google Translate) → **DeepL MCP** SOTA (best translation quality).
- **Trust & safety** (Atomic AI / TrustLab / Perspective) → **Atomic AI** SOTA, **Perspective API** free fallback.
- **Voice transcription** (Aircall / Dialpad / Twilio Flex + Whisper) → **Twilio MCP** + Whisper for self-hosted, **Aircall / Dialpad** for managed.
- **Reverse-ETL** (Census / Hightouch / Polytomic) → **Census** SOTA.
