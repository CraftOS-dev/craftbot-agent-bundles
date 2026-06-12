<!--
Source: https://www.eclincher.com/articles/autonomous-crisis-detection-for-brands-how-ai-monitors-reputation-risk-in-real-time-2026-guide
Emplifi real-time crisis: https://emplifi.io/resources/blog/real-time-crisis-management/
Crisis playbook: role.md "Crisis comms playbook"
Brand24 webhook integration
-->
# Social Crisis Communications — SKILL

Brand24 webhook on threshold breach → Slack alert → auto-pull mention cluster → draft 3 statement variants (apology / clarification / holding) → legal review hook → deploy via Buffer cascade across owned channels. Early detection reduces reputational damage 40%. SLA: acknowledge < 60 min / position statement < 4 hrs / detailed response < 24 hrs.

## When to use this skill

- **Brand24 webhook fires** on threshold breach (volume / sentiment / reach).
- **Negative-mention velocity > 100/hr or 2x baseline**.
- **Single mention reach > 1M with negative sentiment**.
- **Hashtag formation against brand** (>1k uses in 24h on new tag).
- **Named-person (executive / spokesperson) mention** in negative context.
- **Customer-harm mention surfaces** (any volume, escalate immediately).

**Do NOT use this skill when:**
- A single negative comment (no velocity) — `social-customer-service-handoff`.
- Routine negative sentiment in baseline — `sentiment-mention-triage`.
- Pre-emptive PR campaign (proactive) — `marketing-agent`'s PR flow.

## Setup

### Brand24 webhook → Slack

```bash
mcp tool brand24.subscribe_webhook \
  --project_id "$BRAND24_PROJECT_ID" \
  --event "threshold_breach" \
  --url "https://hooks.slack.com/services/<...>/crisis-watch" \
  --conditions '{
    "negative_volume_24h": ">2x_baseline",
    "single_mention_reach": ">1000000",
    "negative_sentiment_pct": ">50",
    "new_hashtag_volume": ">1000_in_24h"
  }'
```

### Buffer cascade pre-config

```bash
# Pre-define crisis-cascade channel list
export CRISIS_CHANNELS='["linkedin_company","twitter","instagram","tiktok","threads","bluesky","facebook"]'
```

### Legal-review hook (Notion + Slack)

```yaml
crisis_legal_review_db:
  columns: [Crisis ID, Created at, Draft variant A (apology), Variant B (clarification), Variant C (holding), Recommended variant, Legal status (pending/approved/rejected/needs-edit), Legal notes, Approved at, Deployed at]
```

### Notion Crisis Log DB

Columns: `Crisis ID / Detected at / Trigger (webhook condition) / Mention cluster URLs / Reach / Sentiment / Variant chosen / Statement URL / Cascade channels / Acknowledge time / Statement time / Detailed response time / Resolution time / Lessons learned`.

## Common recipes

### Recipe 1: Webhook handler

```python
@webhook_handler('/crisis-watch')
def on_threshold_breach(payload):
    crisis = notion.create(crisis_db, {
        'Crisis ID': f"CRISIS-{int(time.time())}",
        'Detected at': now(),
        'Trigger': payload['condition'],
        'Mention cluster URLs': payload['top_mentions_urls'],
        'Reach': payload['cluster_reach'],
        'Sentiment': payload['sentiment_breakdown']
    })
    # 1. Slack alert with ALL HANDS
    slack.post('#crisis-watch', f"""🚨 CRISIS DETECTED
Crisis ID: {crisis['Crisis ID']}
Trigger: {payload['condition']}
Reach: {payload['cluster_reach']:,}
Top mentions: {payload['top_mentions_urls'][:5]}

3-variant draft incoming. Acknowledge SLA: 60 min from {now()}.
""")
    # 2. Auto-pull cluster + classify
    cluster = mcp.brand24.get_mentions(project_id=BRAND24_PROJECT_ID,
                                        cluster_id=payload['cluster_id'])
    fact_pattern = analyze_fact_pattern(cluster)
    # 3. Draft 3 variants
    drafts = draft_three_variants(fact_pattern, crisis['Crisis ID'])
    notion.update(crisis['id'], drafts)
    # 4. Pin in Slack
    slack.post('#crisis-watch', format_drafts(drafts))
```

### Recipe 2: Three-variant draft engine (per role.md)

```python
def draft_three_variants(fact_pattern, crisis_id):
    return {
        'Variant A (apology)': APOLOGY_TEMPLATE.format(
            issue=fact_pattern['issue_summary'],
            apology_target=fact_pattern['affected_audience'],
            concrete_action=fact_pattern['proposed_remediation'],
            timeline=fact_pattern['remediation_timeline']
        ),
        'Variant B (clarification)': CLARIFICATION_TEMPLATE.format(
            accurate_facts=fact_pattern['verified_facts'],
            misrepresentation=fact_pattern['misrepresented_claims'],
            verifiable_detail=fact_pattern['verifiable_evidence']
        ),
        'Variant C (holding)': HOLDING_TEMPLATE.format(
            issue_summary=fact_pattern['issue_summary'],
            investigation_status='under investigation',
            timeline_commitment=fact_pattern['expected_clarity_eta']
        ),
        'Recommended variant': recommend_variant(fact_pattern)
    }

APOLOGY_TEMPLATE = """We are aware of {issue} affecting {apology_target}.

We're sorry. This is not the standard we hold ourselves to.

Concrete action: {concrete_action}.

Timeline: {timeline}.

We'll provide an update within 24 hrs. For affected customers: <support_link>."""

CLARIFICATION_TEMPLATE = """We've seen reports about {issue_summary}. To clarify the facts:

{accurate_facts}

Some reports have inaccurately stated {misrepresentation}. The verifiable detail: {verifiable_detail}.

We're committed to transparency. Questions: <press_link>."""

HOLDING_TEMPLATE = """We're aware of {issue_summary} and are investigating.

We're committed to sharing details when confirmed — expected within {timeline_commitment}.

Affected customers can reach support at <support_link>.

We'll update here as we learn more."""
```

### Recipe 3: Fact-pattern analyzer

```python
def analyze_fact_pattern(cluster):
    # Cluster mentions by claim / theme
    claims = cluster_claims_via_llm(cluster)  # via Claude / OpenAI
    return {
        'issue_summary': claims['top_claim'],
        'affected_audience': claims['who_is_affected'],
        'severity': claims['severity_score'],
        'verified_facts': internal_lookup_for_facts(claims['claim_list']),
        'misrepresented_claims': identify_misrepresentations(claims['claim_list']),
        'verifiable_evidence': pull_evidence_from_internal_systems(claims),
        'proposed_remediation': remediation_template(claims),
        'remediation_timeline': estimate_timeline(claims),
        'expected_clarity_eta': '4 hrs',  # default holding-statement timeline
    }
```

### Recipe 4: Variant recommendation logic

```python
def recommend_variant(fp):
    # Per role.md crisis playbook
    if fp['severity'] in ('customer_harm', 'data_breach', 'fatal_product_defect'):
        return 'A (apology)'  # accountability first
    if fp['misrepresented_claims'] and fp['verifiable_evidence']:
        return 'B (clarification)'  # facts are clear, narrative is not
    return 'C (holding)'  # default when facts still unclear
```

### Recipe 5: Legal review hook

```python
# After drafts ready, post in Slack with approve / edit buttons
@slack_command('/crisis-approve')
def approve(crisis_id, variant_key, approver_email):
    crisis = notion.get(crisis_db, crisis_id)
    if crisis['Legal status'] != 'pending':
        return slack.respond("Legal must review before approval")
    notion.update(crisis_id, {
        'Legal status': 'approved',
        'Variant chosen': variant_key,
        'Approved at': now(),
        'Legal approver': approver_email
    })
    deploy_cascade(crisis_id)
```

### Recipe 6: Cascade deployment via Buffer

```python
def deploy_cascade(crisis_id):
    crisis = notion.get(crisis_db, crisis_id)
    statement = crisis[crisis['Variant chosen']]
    
    # Cascade across all owned channels
    update = mcp.buffer.create_update(
        channelIds=json.loads(os.environ['CRISIS_CHANNELS']),
        text=statement,
        channelData=per_channel_variants(statement),
        scheduledAt=now() + timedelta(minutes=2)  # 2-min buffer for last-min review
    )
    notion.update(crisis_id, {
        'Statement URL': update['id'],
        'Cascade channels': os.environ['CRISIS_CHANNELS'],
        'Statement time': now() + timedelta(minutes=2)
    })
    # Pin on website + email opt-in alert
    update_website_banner(text=statement[:200])
    trigger_customer_email_alert(crisis_id)
```

### Recipe 7: SLA watchdog (60-min acknowledge / 4-hr position / 24-hr detail)

```python
@scheduled('*/5 * * * *')  # every 5 min
def sla_watchdog():
    open_crises = notion.query(crisis_db, filter={'Resolution time': None})
    for c in open_crises:
        detected = c['Detected at']
        elapsed_min = (now() - detected).total_seconds() / 60
        
        if not c['Acknowledge time'] and elapsed_min > 60:
            slack.post('#crisis-watch', f"⚠ {c['Crisis ID']} — ACK SLA BREACH at {int(elapsed_min)} min")
        elif not c['Statement time'] and elapsed_min > 240:
            slack.post('#crisis-watch', f"⚠ {c['Crisis ID']} — STATEMENT SLA BREACH at {int(elapsed_min/60)} hrs")
        elif not c['Detailed response time'] and elapsed_min > 24*60:
            slack.post('#crisis-watch', f"⚠ {c['Crisis ID']} — DETAILED RESPONSE SLA BREACH at {int(elapsed_min/60)} hrs")
```

### Recipe 8: Earned-media outreach

```python
# After statement deployed, push to journalists
PR_LIST = [
    'reporter1@techoutlet.com',
    'reporter2@business.com',
    # ... pre-curated journalist list (inherited from marketing-agent PR work)
]
for email in PR_LIST:
    mcp.gmail.send(to=email,
                   subject=f"Statement from <brand>: {fact_pattern['issue_summary']}",
                   body=PR_OUTREACH_TEMPLATE.format(statement=statement, contact='press@brand.com'))
```

### Recipe 9: Internal staff communication

```python
# Slack #all-hands
slack.post('#all-hands', f"""Team — we're managing a public incident.

Crisis ID: {crisis_id}
What happened: {fact_pattern['issue_summary']}
Public statement: <link>
Customer-impact: {fact_pattern['affected_audience']}

If asked: refer to the public statement. Do NOT speculate publicly.
Internal contact: @comms-lead

Updates will be posted here every 4 hrs until resolved.""")

# CEO Loom video for staff (if material)
if fact_pattern['severity'] in ('high', 'critical'):
    # Trigger CEO video flow
    pass
```

### Recipe 10: Post-crisis retro (within 7 days of resolution)

```python
def post_crisis_retro(crisis_id):
    c = notion.get(crisis_db, crisis_id)
    retro = {
        'Crisis ID': crisis_id,
        'Total duration_hrs': (c['Resolution time'] - c['Detected at']).total_seconds() / 3600,
        'Ack within SLA': (c['Acknowledge time'] - c['Detected at']).total_seconds() / 60 < 60,
        'Statement within SLA': (c['Statement time'] - c['Detected at']).total_seconds() / 60 < 240,
        'Detailed within SLA': (c['Detailed response time'] - c['Detected at']).total_seconds() / 60 < 24*60,
        'Sentiment recovery_hrs': time_to_baseline_sentiment(c),
        'Reach negative cluster': c['Reach'],
        'Lessons learned': '<populate manually>'
    }
    notion.create(crisis_retro_db, retro)
    slack.post('#leadership', format_retro(retro))
```

## Examples

### Example A: Data-breach crisis flow

```yaml
t+0min: Brand24 webhook fires — '50k users tweet "brand x data leaked"' cluster
t+2min: Slack #crisis-watch alert; drafts auto-generated
t+10min: legal + comms team join Slack thread
t+30min: variant A (apology) approved
t+35min: cascade deploys (LinkedIn, X, IG, FB, Threads, Bluesky)
t+45min: website banner up; email alert sent
t+60min: ACK SLA met
t+4hr: detailed statement + remediation page live
t+24hr: status update + free credit monitoring offer
t+72hr: full retrospective; security audit announcement
t+7day: post-crisis retro logged; lessons added to playbook
```

### Example B: Single-source false claim (clarification path)

```yaml
trigger: viral X thread "brand X uses slave labor" by influencer with 2M followers
fact_pattern: claim is false; brand has third-party audit reports
variant_chosen: B (clarification) with audit evidence link
deployment: X reply to original thread + cross-post to LinkedIn/IG/Threads
follow_up: invite influencer to fact-check call
result: original thread deleted at t+24hr; sentiment recovery in 48hr
```

### Example C: Holding statement scenario

```yaml
trigger: viral video "brand X product injured my kid"
fact_pattern: facts unclear; investigating
variant_chosen: C (holding) — "We're investigating; affected customer support active"
follow_up_timeline:
  t+4hr: holding statement update
  t+8hr: facts emerge — product was counterfeit, not ours
  t+12hr: variant B (clarification) deployed with proof
  t+24hr: full statement + counterfeit-warning + customer-protection
```

## Edge cases

### False-positive webhook
Brand24 threshold may fire on a news story unrelated to brand. Manually validate before public response. 2-min Slack thread review before deploy.

### Multiple-crisis overlap
If two crises hit same week, each gets own crisis ID + variant track. Don't merge messaging — confuses public.

### Legal-team unavailable (after hours)
Pre-approve "holding statement" template language. Variant C can ship without case-by-case legal review when severity ≤ medium.

### Voice drift in apology
Apology in corporate-speak feels insincere. Use brand-voice doc + human language. Variant A template lets brand voice through.

### Multi-language statement
Brand operating in multi-market — statement variants per language. Use `deepl-mcp` for first-pass translation; human review.

### Spokesperson named
When CEO / exec is named, they (not generic brand voice) must speak. Coordinate via direct-comms channel; brand cascade waits.

### Counter-attack risk
Don't punch back at accusers in statement — even if wrong. Show evidence; let public adjudicate.

### Statement-too-late penalty
60-min ack SLA is non-negotiable. Beyond 60 min, public assumes brand is in damage-control or hiding.

### Statement-too-early risk
Pushing detailed response before facts clear → reversing later = double crisis. Holding statement at minimum to claim acknowledgment.

### Cascade-channel inconsistency
Different statement on different platform = additional crisis ("brand told X one thing on Twitter, another on LinkedIn"). Cascade identical core statement.

### Customer DMs flood
Crisis incoming DMs may 10x normal. Pre-prepare auto-response template; route to dedicated crisis-support queue.

### Internal-leak risk
Staff sees crisis details first — internal Slack leaks fuel external speculation. Don't share specifics until public statement deployed.

### Retraction handling
If facts change post-statement, formal correction post. Don't silently delete. Maintain transparency.

### Reach-decay watch
Initial cluster may rapidly amplify or die. Monitor via Brand24 — if dying, lighter response; if amplifying, full cascade.

### Astroturf detection
Coordinated inauthentic posting may simulate crisis. Cross-check accounts: new accounts, similar timestamps, shared content. Brand24 + manual check.

### Recovery monitoring
Post-statement, sentiment may take 24-72 hrs to recover. Track baseline; alert if NOT recovering.

## Sources

- **Eclincher — autonomous crisis detection 2026**: https://www.eclincher.com/articles/autonomous-crisis-detection-for-brands-how-ai-monitors-reputation-risk-in-real-time-2026-guide
- **Emplifi — real-time crisis management**: https://emplifi.io/resources/blog/real-time-crisis-management/
- **Brand24 webhook integration**: https://brand24.com/integrations/webhook/
- **Buffer cascade deploy**: https://buffer.com/developers/api
- **Role.md "Crisis comms playbook"**: SLA matrix + 3-variant draft engine
- **PR Council — crisis communications guide 2026**: https://prcouncil.net/
- **Bernstein Crisis Management**: https://bernsteincrisismanagement.com/
