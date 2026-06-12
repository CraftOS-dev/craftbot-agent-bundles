<!--
Source: https://perspectiveapi.com/ + https://atomic.ai/ + Google Perspective API
-->
# Trust & Safety Abuse Triage — SKILL

Classify support messages for abuse / fraud / T&C violations / spam. Confidence-gated auto-escalation. Customer-facing replies stay gentle (no commitments); internal evidence chain carries full classification result. Primary: Atomic AI (paid); free fallback: Google Perspective API.

## When to use

- **New conversation** with abusive language, threats, harassment.
- **Suspected fraud** — chargeback bait, fake refund requests, identity theft attempts.
- **T&C violations** — using the product to do prohibited things.
- **Spam detection** — automated / repetitive low-quality content.
- **Account-level action** — suspension / banning decisions for paying customers.

Trigger phrases: "is this abuse", "fraud triage", "T&C violation", "spam classifier", "ban this user".

## Setup

```bash
# Atomic AI (paid — contact sales)
curl -sS "https://api.atomic.ai/v1/classify" \
  -H "Authorization: Bearer $ATOMIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text":"sample"}'

# Google Perspective API (free, 1 QPS)
# Request quota at: https://developers.perspectiveapi.com/s/docs-get-started
curl -sS "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=$PERSPECTIVE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"comment":{"text":"sample"},"requestedAttributes":{"TOXICITY":{}}}'
```

Auth + env:
- `ATOMIC_API_KEY` — Atomic AI account, paid.
- `PERSPECTIVE_API_KEY` — Google Cloud API key. Free tier: 1 QPS, request bump for higher.
- `ANTHROPIC_API_KEY` — for Claude-based fallback / nuance pass.

Workspace prerequisites:
- T&S queue / team in Zendesk / Intercom / Front.
- Evidence-chain Notion DB or warehouse table.
- Suspension / ban runbook in Notion.

## Common recipes

### Recipe 1: Classify via Atomic AI

```bash
curl -sS -X POST "https://api.atomic.ai/v1/classify" \
  -H "Authorization: Bearer $ATOMIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"$MESSAGE_TEXT\",\"categories\":[\"abuse\",\"fraud\",\"tc_violation\",\"spam\",\"identity_theft\"]}" \
  | jq '.results'
```

Returns confidence scores per category. Threshold per `role.md`: ≥0.8 → auto-route, 0.5-0.8 → human review queue, <0.5 → standard triage.

### Recipe 2: Classify via Google Perspective (free fallback)

```bash
curl -sS "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=$PERSPECTIVE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"comment\":{\"text\":\"$MESSAGE_TEXT\"},
    \"requestedAttributes\":{
      \"TOXICITY\":{},
      \"SEVERE_TOXICITY\":{},
      \"IDENTITY_ATTACK\":{},
      \"INSULT\":{},
      \"PROFANITY\":{},
      \"THREAT\":{}
    },
    \"languages\":[\"en\"]
  }" | jq '.attributeScores | with_entries(.value = .value.summaryScore.value)'
```

Returns 0-1 score per attribute. Free for non-commercial; commercial needs `GOOGLE_CLOUD_PROJECT`.

### Recipe 3: Claude nuance pass (for ambiguous cases)

```bash
PROMPT="Classify this support message for trust-and-safety concerns. Be conservative — false positives hurt customer trust. Output STRICT JSON:
{
  \"category\": \"abuse|fraud|tc_violation|spam|none\",
  \"confidence\": 0-1,
  \"reason\": \"brief reason\",
  \"recommended_action\": \"auto_route|human_review|standard_triage\"
}

Message:
$MESSAGE_TEXT"

curl -sS https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d "{\"model\":\"claude-sonnet-4-5-20250929\",\"max_tokens\":256,\"messages\":[{\"role\":\"user\",\"content\":\"$PROMPT\"}]}" \
  | jq -r '.content[0].text' | jq .
```

Use after Atomic / Perspective for cases where confidence is 0.5-0.8; Claude is good at nuance / context.

### Recipe 4: Auto-route to T&S queue (Zendesk)

```bash
curl -sS -X PUT "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets/$TICKET_ID.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  -d '{
    "ticket":{
      "group_id":'$TS_GROUP_ID',
      "priority":"normal",
      "tags":["ts-flagged","ts-category-'$CATEGORY'","triage-done"],
      "comment":{
        "body":"T&S auto-flag: category='$CATEGORY', confidence='$CONF'. Source: atomic-ai. See internal note for full classification.",
        "public":false
      }
    }
  }'
```

`public:false` keeps the classification internal-only.

### Recipe 5: Customer-facing reply (gentle decline)

Per `role.md`: don't accuse, no commitments, no internal info.

```bash
REPLY="Hi,

I've reviewed your message and unfortunately we won't be able to help with this request. If you have a different issue you'd like support on, please feel free to reach out.

— Support team"

# Send via platform
```

Variations by category:
- `abuse`: "We're unable to continue this conversation. Future messages on this topic won't receive a response."
- `fraud`: "Your account has been flagged for review. You'll hear from our team within 5 business days."
- `tc_violation`: "This use case isn't supported by our Terms of Service. We're not able to assist."
- `spam`: (silent — don't reply)

### Recipe 6: Log evidence chain

```bash
curl -sS -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "parent":{"database_id":"'$TS_EVIDENCE_DB_ID'"},
    "properties":{
      "Title":{"title":[{"text":{"content":"[ts-flag] ticket-12345 — abuse 0.92"}}]},
      "Ticket":{"url":"https://app.intercom.com/.../12345"},
      "Category":{"select":{"name":"abuse"}},
      "Confidence":{"number":0.92},
      "Classifier":{"select":{"name":"atomic_ai"}},
      "Date":{"date":{"start":"2026-06-09"}},
      "Action Taken":{"select":{"name":"routed_to_ts_queue"}}
    },
    "children":[
      {"object":"block","type":"heading_2","heading_2":{"rich_text":[{"text":{"content":"Classification result"}}]}},
      {"object":"block","type":"code","code":{"rich_text":[{"text":{"content":"{...full atomic ai JSON...}"}}],"language":"json"}},
      {"object":"block","type":"heading_2","heading_2":{"rich_text":[{"text":{"content":"Source message"}}]}},
      {"object":"block","type":"quote","quote":{"rich_text":[{"text":{"content":"<paste source message>"}}]}}
    ]
  }'
```

Evidence chain preserves classifier output, source text, action taken — discoverable for appeals / legal.

### Recipe 7: Cross-platform repeat-offender detection

```sql
-- Has this customer been flagged before?
SELECT
  email,
  COUNT(*) AS flags_total,
  COUNT(*) FILTER (WHERE date >= NOW() - INTERVAL '30 days') AS flags_30d,
  ARRAY_AGG(DISTINCT category) AS categories,
  MAX(date) AS last_flag
FROM ts.evidence
WHERE email = 'user@example.com'
GROUP BY email;
```

`flags_30d >= 3` = repeat offender; escalate to suspension review.

### Recipe 8: Suspension workflow

```bash
# Mark account suspended in your auth system (e.g., Stytch)
curl -sS -X PUT "https://api.stytch.com/v1/users/$USER_ID" \
  -u "$STYTCH_PROJECT_ID:$STYTCH_SECRET" \
  -d '{"trusted_metadata":{"status":"suspended","reason":"ts_abuse","by":"agent","date":"2026-06-09"}}'

# Document in Notion
mcp tool notion.create_page \
  --parent_database_id $SUSPENSIONS_DB_ID \
  --properties '{"User":"user@example.com","Reason":"abuse repeat","Approver":"$ADMIN_NAME","Date":"2026-06-09","Review Date":"2026-07-09"}'
```

Suspensions: time-bounded (30d); require human review before permanent ban.

### Recipe 9: Ban workflow (paying customer)

```bash
# 1. Run Recipe 7 to confirm repeat-offender pattern
# 2. Open a Notion review page
mcp tool notion.create_page \
  --parent_database_id $BANS_DB_ID \
  --properties '{
    "User":"user@example.com",
    "Category":"abuse",
    "Evidence Pages":"<comma-separated notion page IDs>",
    "MRR":"$200",
    "Tenure (mo)":"18",
    "Refund Owed":"$135 (pro-rata)",
    "Status":"Pending Lead Approval"
  }'

# 3. Slack lead for approval
mcp tool slack.chat_postMessage --channel '#ts-bans' \
  --text "Ban approval needed: user@example.com (abuse, 5 flags, MRR $200). Notion: <url>."

# 4. After approval — execute ban + pro-rata refund (next recipe)
```

Paying-customer bans need explicit approval + refund per policy.

### Recipe 10: Pro-rata refund execution

```bash
DAYS_REMAINING=$((($(date -u -d "$NEXT_BILL_DATE" +%s) - $(date -u +%s)) / 86400))
DAYS_IN_PERIOD=30
REFUND_AMOUNT_CENTS=$(( $LAST_CHARGE_CENTS * $DAYS_REMAINING / $DAYS_IN_PERIOD ))

# stripe-mcp
mcp tool stripe.refund_create \
  --charge_id "ch_xxx" \
  --amount $REFUND_AMOUNT_CENTS \
  --reason "ban_pro_rata"

# Log to warehouse
psql -c "INSERT INTO support.refunds (customer_id, amount_cents, reason, executed_at) VALUES ('$USER_ID', $REFUND_AMOUNT_CENTS, 'ban_pro_rata', NOW())"
```

### Recipe 11: Webhook auto-flagging on incoming message

```python
# On conversation.message.created webhook:
def handle(payload):
    text = payload['message']['body']
    if len(text) > 50000:  # too long to classify
        return _route_human_review(payload, reason='too_long')

    scores = atomic_classify(text)  # Recipe 1
    if not scores:
        scores = perspective_classify(text)  # Recipe 2 fallback

    max_cat = max(scores, key=scores.get)
    conf = scores[max_cat]

    if conf >= 0.8:
        _auto_route_ts(payload, max_cat, conf)
        _log_evidence(payload, max_cat, conf)
    elif conf >= 0.5:
        # Claude nuance pass (Recipe 3)
        claude_result = claude_classify(text)
        if claude_result['confidence'] >= 0.8:
            _auto_route_ts(payload, claude_result['category'], claude_result['confidence'])
        else:
            _route_human_review(payload, reason='ambiguous')
    # else: standard triage continues
```

### Recipe 12: Quarterly false-positive audit

```sql
-- Were ts-flagged tickets actually problematic, or did we over-flag?
SELECT
  category,
  COUNT(*) AS flagged,
  SUM(CASE WHEN final_action = 'no_action' THEN 1 ELSE 0 END) AS fp,
  ROUND(100.0 * SUM(CASE WHEN final_action = 'no_action' THEN 1 ELSE 0 END) / COUNT(*), 1) AS fp_pct
FROM ts.evidence
WHERE date >= NOW() - INTERVAL '90 days'
GROUP BY 1 ORDER BY fp_pct DESC;
```

`fp_pct > 20%` for any category = classifier is over-firing; tune thresholds.

## Examples

### Example 1: Abusive language → auto-route

**Goal:** Customer DMs profanity-laden message. Triage cleanly.

**Steps:**
1. Recipe 1 (Atomic) — TOXICITY=0.94, IDENTITY_ATTACK=0.71.
2. Confidence ≥ 0.8 → auto-route to T&S queue (Recipe 4).
3. Customer-facing reply: gentle decline (Recipe 5, abuse variant).
4. Evidence chain logged in Notion (Recipe 6).
5. Recipe 7 — check repeat-offender; this is their 1st flag, no further action.

**Result:** Conversation stops; classifier output preserved; customer can appeal.

### Example 2: Fraud pattern → suspension

**Goal:** Customer requests refund citing nonexistent product issues; 3rd flag in 30d.

**Steps:**
1. Recipe 1 — FRAUD=0.62.
2. Recipe 3 (Claude nuance) — confirms `fraud` 0.82.
3. Recipe 4 — route to T&S queue.
4. Recipe 7 — repeat offender (3 flags).
5. Recipe 8 — suspend account (30d).
6. Customer-facing reply: fraud variant (Recipe 5).
7. Recipe 6 — evidence chain.
8. Stripe refund: NOT auto-issued (suspect fraud).
9. Notion suspension page for human follow-up.

**Result:** Account suspended; full evidence preserved; manual review scheduled.

## Edge cases / gotchas

- **Avoid auto-bans** — bans for paying customers need explicit lead + legal approval. Automate flagging, not punishment.
- **Multilingual** — Perspective supports limited non-English; Atomic supports more. For DeepL-translated text, classify the original AND the translation (catches edge cases).
- **Context matters** — "You're killing me" in a venting customer ≠ a threat. Use Claude nuance (Recipe 3) for ambiguous classifications.
- **Free Perspective tier = 1 QPS** — bulk classification needs paid quota. Bursty workloads need batching.
- **Atomic API SLA** — ~99% uptime; have Perspective as automatic fallback (Recipe 11).
- **Legal preservation** — once flagged, retain the source message + classification 90d minimum for appeal cycle. Don't auto-delete tickets.
- **Bias in classifiers** — toxicity classifiers historically over-flag AAVE, profanity in venting contexts, mental-health language. Quarterly FP audit (Recipe 12).
- **GDPR right to erasure** — if user invokes erasure, ts-evidence becomes a retention question. Consult legal.
- **Don't expose category to customer** — saying "we flagged you for fraud" gives attackers feedback to refine. Use the generic decline templates.
- **Cross-platform user identity** — same user across Discord / Slack / email may be 3 separate ts-flag chains. Maintain a manual mapping for known repeat-offenders.
- **Spam reply pattern** — for confirmed spam, *silently delete* rather than reply; spammers feed off engagement.
- **Don't classify minors** — products with under-18 user bases need stricter handling; consult legal counsel.

## Sources

- [Google Perspective API docs](https://perspectiveapi.com/)
- [Perspective getting started](https://developers.perspectiveapi.com/s/docs-get-started)
- [Atomic AI (paid, contact-sales)](https://atomic.ai/)
- [Anthropic Claude for nuanced classification](https://docs.anthropic.com/en/docs/about-claude/use-cases/classification)
- [Stytch user suspension docs](https://stytch.com/docs/api/update-user)
- [Trust & safety triage playbook (role.md)](../../role.md)
