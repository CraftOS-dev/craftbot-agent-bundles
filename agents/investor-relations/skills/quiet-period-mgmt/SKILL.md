<!--
Source: https://www.sec.gov/divisions/corpfin/guidance/regfd-interp.htm
Source: https://www.niri.org/standards-of-practice
Source: https://www.cooley.com/news/insights/reg-fd-quiet-period-best-practices
Source: https://www.lw.com/en/insights/regulation-fd-best-practices
Source: https://www.davispolk.com/insights/regulation-fd-current-issues
Reference role.md: "Quiet period playbook" + "Reg FD decision tree"
Round 2 enrichment: auto-reply template + Reg FD audit register schema + calendar block-out + manual-override sign-off.
-->

# Quiet period management (~2-week pre-earnings lockout)

Manages the ~2-week quiet-period lockout for public companies pre-earnings (typically last 2 weeks of quarter through earnings call). Calendar lockout enforced; outbound auto-reply on IR inbox; analyst 1:1s + conference appearances + guidance refinement all DECLINED. Reg FD interpretation is counsel-driven; this skill enforces the playbook. **Defers binding Reg FD interpretation to `legal-counsel` + `compliance-agent`.**

## When to use

- Entering quiet period (T-~14 days from earnings call).
- Handling inbound investor / analyst requests during quiet period.
- Manual override requests (rare; require board + exec + counsel sign-off).
- IPO quiet period management (40-day pre-IPO post-S-1 effective).
- Trigger phrases: "quiet period", "Reg FD quiet period", "lockout", "block-out calendar", "quiet period auto-reply".

NOT for: ongoing Reg FD interpretation (use `embargoed-disclosure-protocols` or counsel direct); guidance setting (use `guidance-setting`); earnings prep (use `earnings-call-script-qa`).

## Setup

```bash
# Tools (all CraftBot defaults):
# - gmail-mcp + outlook-mcp for auto-reply
# - google-calendar-mcp for block-out
# - notion-mcp for Reg FD audit register
# - slack-mcp for IR + exec internal coordination

# Counsel hand-off:
# - legal-counsel (binding interpretation)
# - compliance-agent (framework + monitoring)
```

Auth / API key requirements:
- `gmail-mcp` / `outlook-mcp` OAuth (free).
- `notion-mcp` (free / personal; team $10/user/mo).
- No paid platform required; this is process-driven.

Data inputs:
- Earnings call date (drives quiet-period boundary).
- IR contact list (CEO/CFO/IR/comms).
- Inbound investor + analyst request log (for review).
- Counsel-supplied auto-reply boilerplate.
- Prior quiet period Reg FD register (for pattern consistency).

## Quiet period definition

- **Conventional:** ~2 weeks before quarter-end through earnings call release.
- **Reg FD technically:** Selective disclosure of MNPI prohibited at ALL times; quiet period is institutional self-imposed.
- **IPO quiet period (separate):** From S-1 filing through ~40 days post-effective for non-WKSIs.
- **WKSIs (Well-Known Seasoned Issuers):** Greater latitude under Rule 168/169 but still adhere.

## Reg FD decision tree (during quiet period)

```
Inbound request received -> Categorize:

1. Public-info-only request (10-K linkout, prior call transcript)?
   YES -> Reply with link; no MNPI risk; document in register

2. Specific Q from analyst about current quarter?
   YES -> AUTO-DECLINE: "We're in our quiet period until [date]"
        + counsel cc; log in register

3. Repeat 1:1 standing meeting in quiet period window?
   YES -> RESCHEDULE to post-earnings; no exception

4. Conference appearance pre-arranged before quiet period started?
   - If can be moved: MOVE
   - If can't: CANCEL or send IR rep with prepared remarks only
   - Counsel sign-off

5. Press inquiry (non-investor)?
   YES -> Standard PR comms; defer financial questions to "wait for earnings"

6. Material news event during quiet period?
   YES -> 8-K Item 7.01 Reg FD disclosure; escalate to counsel + CEO/CFO

7. Bank corporate-access desk requesting NDR slot?
   YES -> DECLINE for during-window; offer post-call slot

8. Existing 1:1 commitment with top-3 holder/PM?
   - Counsel can authorize narrow exception: "Will discuss only published info"
   - Reg FD audit + counsel sign-off required
   - DEFAULT: reschedule
```

## Outbound auto-reply template (counsel-supplied)

```
Subject: Re: [Original Subject] — Quiet Period Notice

Thank you for your message. {Company} is currently in its scheduled quiet
period in advance of our [Q-N FY] earnings release on [Date]. During this
period, we are not commenting on operational or financial performance.

Our most recent disclosures are available at ir.company.com.

We look forward to engaging with you following our earnings release.
The webcast of our earnings call will be live at ir.company.com/events/
[Date] at [Time] ET.

For inquiries that cannot wait, please contact:
- Media: media@company.com
- General: ir@company.com (response will follow earnings)

Best,
Investor Relations Team
{Company}
```

## Reg FD audit register schema (notion-mcp)

```
DATE: YYYY-MM-DD
INBOUND FROM: <Name + Firm>
REQUEST TYPE: 1:1 / Email Q / Conference / Press / Inadvertent
TOPIC: Strategy / Financials / Guidance / Operational
HANDLING: Auto-reply / Reschedule / Cancel / Narrow Exception (counsel approved)
COUNSEL CC: yes/no + name
DOCUMENTED: timestamp of audit-trail entry
NOTES: any context
```

Counsel reviews register monthly for pattern issues + Reg FD compliance.

## Common recipes

### Recipe 1 — Enable Gmail auto-reply
```bash
mcp call gmail-mcp set_vacation_responder \
  --enabled true \
  --start "2026-07-14T00:00:00Z" \
  --end "2026-07-30T22:00:00Z" \
  --subject "Quiet Period — Will Respond Post-Earnings" \
  --body "$(cat quiet_period_auto_reply.txt)"
```

### Recipe 2 — Enable Outlook auto-reply
```bash
mcp call outlook-mcp set_out_of_office \
  --enabled true \
  --start "2026-07-14T00:00:00Z" \
  --end "2026-07-30T22:00:00Z" \
  --internal_message "$(cat quiet_period_internal.txt)" \
  --external_message "$(cat quiet_period_external.txt)"
```

### Recipe 3 — Calendar block-out
```bash
mcp call google-calendar-mcp create_event \
  --calendar "ir-team@company.com" \
  --summary "QUIET PERIOD — NO ANALYST 1:1s NO GUIDANCE NO CONFERENCES" \
  --start "2026-07-14T00:00:00Z" \
  --end "2026-07-30T22:00:00Z" \
  --visibility "private" \
  --description "No new investor or analyst commitments. Reg FD lockout."
```

### Recipe 4 — Reg FD register entry (notion-mcp)
```bash
mcp call notion-mcp create_page --database=$REG_FD_DB \
  --properties='{
    "Date": "2026-07-20",
    "Inbound From": "Jane Smith (Acme Capital)",
    "Request Type": "1:1",
    "Topic": "Q2 segment trends",
    "Handling": "Reschedule to Aug 5 (post-earnings)",
    "Counsel CC": "yes - John Doe",
    "Documented": "2026-07-20T10:30:00Z",
    "Notes": "Standing quarterly 1:1; routine reschedule"
  }'
```

### Recipe 5 — Slack alert to internal team
```bash
mcp call slack-mcp post_message \
  --channel "#ir-team-private" \
  --text ":lock: QUIET PERIOD ACTIVE: Jul 14 - Jul 30. No analyst 1:1s. No guidance refinement. Inbounds -> auto-reply + Reg FD register. Escalations -> #ir-counsel."
```

### Recipe 6 — Narrow-exception sign-off workflow
```python
# Rare; counsel-supervised; documented heavily
def narrow_exception(inbound_request):
    return {
        "requestor": "...",
        "scope": "discuss only published filings + prior call commentary",
        "counsel_approval": "John Doe, [date]",
        "ceo_or_cfo_approval": "Jane CEO, [date]",
        "reg_fd_documentation": "register entry + meeting notes saved",
        "post_meeting_summary": "filed within 24h",
    }
```

### Recipe 7 — IPO quiet period (40-day post-effective)
```python
# Different rules; counsel-supervised
IPO_QUIET_PERIOD = {
    "duration": "40 days from S-1 effective date for non-WKSIs",
    "permitted": "factual business communications; ordinary-course; pre-existing disclosures",
    "prohibited": "promotional materials; forward-looking statements outside S-1; analyst calls",
    "rule": "Rule 168 + Rule 169 safe harbors",
}
```

### Recipe 8 — Materials-on-IR-website refresh (during quiet)
```python
# Only static published content + prior calls + investor day replay
# NO new commentary during quiet; even an FAQ update is risky if material
```

### Recipe 9 — Pre-quiet-period notification (T-3)
```bash
# Notify all standing analyst contacts T-3 of quiet period start
mcp call gmail-mcp send_email \
  --to "$(cat analyst_list.txt | paste -sd, -)" \
  --subject "Quiet Period Notice — ACME" \
  --body "We enter our quiet period [date]; earnings call [date]. Replies post-call."
```

### Recipe 10 — Post-quiet-period unlock notification
```bash
# T+1 after earnings: unlock + send "now open" notice
mcp call gmail-mcp send_email \
  --to "$(cat analyst_list.txt | paste -sd, -)" \
  --subject "Available for 1:1s — ACME Q2 Update" \
  --body "Quiet period ended. Available for 1:1s. Schedule via [link]."
```

### Recipe 11 — Material event during quiet period (escalation)
```python
# If material event happens during quiet:
# 1. Counsel + CEO + CFO + Board chair (within 1 hour)
# 2. Materiality determination (counsel)
# 3. If material -> 8-K Item 7.01 + press release simultaneously
# 4. If not material -> document in Reg FD register; no public action
# Coordinates with `8k-event-reporting`
```

### Recipe 12 — Post-period Reg FD register review
```bash
# Counsel reviews register at end of each quiet period
# Pattern check: any reply that may have been MNPI-adjacent?
# Document review in audit trail; flag for next-cycle adjustment
```

## Examples

### Example 1: Q2 2026 quiet period (steady-state)

**Goal:** Q2 close July 28; earnings Jul 30; quiet period Jul 14 - Jul 30.

**Steps:**
1. T-3 (Jul 11): pre-quiet-period notice to analyst list (Recipe 9).
2. T-0 (Jul 14, 12:01 AM): enable auto-replies (Recipes 1 + 2); block calendar (Recipe 3); Slack alert (Recipe 5).
3. Jul 14-30: handle inbounds per decision tree; log each in register (Recipe 4).
4. ~25 inbounds during window; all routed cleanly; 3 narrow exceptions counsel-approved (Recipe 6).
5. T+0 (Jul 30 4:01 PM ET): earnings release; quiet period ends at release.
6. T+1: unlock notification (Recipe 10); resume 1:1 scheduling.
7. T+10: counsel reviews register (Recipe 12); zero compliance flags.

**Result:** Clean Reg FD compliance; analyst goodwill preserved; auto-reply rate >95%.

### Example 2: Material event during quiet period

**Goal:** Major customer contract loss announced by customer on Jul 22 (mid-quiet-period).

**Steps:**
1. Hour 0: IR sees news; immediately escalates (Recipe 11).
2. Hour 1: counsel + CEO + CFO + board chair convened.
3. Hour 3: counsel materiality determination — MATERIAL.
4. Hour 6: 8-K Item 7.01 drafted + counsel-reviewed.
5. Hour 8: press release drafted (`quarterly-earnings-press-release` skill scope).
6. Hour 12: wire goes; 8-K files; brief CFO statement on IR site.
7. Hour 24: analyst calls flood; counsel-approved talking points only.
8. Quiet period RESUMES post-disclosure for Q2 earnings call Jul 30.

**Result:** Reg FD-compliant material disclosure; quiet period maintained for full earnings.

### Example 3: Pre-IPO quiet period

**Goal:** S-1 effective Sept 1; 40-day quiet period through Oct 11.

**Steps:**
1. Counsel briefs IR + exec team on Rule 168/169 safe harbors.
2. Pre-S-1 "ordinary course" comms permitted (factual; no promotional).
3. Auto-reply for non-permitted inquiries (Recipe 2; IPO variant).
4. Calendar block-out (Recipe 3).
5. Counsel reviews ALL public utterances pre-clearance.
6. Reg FD register kept by counsel.

**Result:** No gun-jumping violations; S-1 process clean.

## Edge cases / gotchas

- **"Quiet period" is institutional not statutory.** Reg FD applies always; the institutional 2-week window is custom; counsel can shorten/extend.
- **Standing 1:1 reschedule signaling.** If you cancel an analyst meeting standing 4 quarters, signals strain; manage expectations.
- **Conference appearance pre-commitment.** Honor or pre-announce withdrawal; binary signal otherwise.
- **Inadvertent disclosure during quiet period.** Reg FD requires "promptly" remedy (24h conventional 8-K Item 7.01).
- **Senior exec at industry conference.** CEO/CFO speaking engagement = high MNPI risk during quiet period; cancel or pre-clear remarks.
- **Internal-employee accidental leak.** Confidentiality training matters; one slip = Reg FD risk.
- **Bank corp-access desk pressure.** Banks push hardest in quiet period (their clients hungriest); blanket decline.
- **Counsel-supplied template freshness.** Counsel may update auto-reply boilerplate annually; refresh.
- **Multi-jurisdiction lockout (EU MAR).** EU listed = also EU MAR closed period; more restrictive; coordinate with EU counsel.
- **Pre-existing PR commitments.** Trade press interviews etc.; defer financial Qs only.
- **Investor inquiries to CFO directly.** Sometimes investors email CFO bypassing IR; auto-reply hits CFO inbox too.
- **Sales channel disclosure to customers.** Sales updates that touch financial trends = MNPI risk; coach sales team.
- **Quiet-period social media.** CEO/CFO Twitter/LinkedIn — silence or counsel-approved only.

> Mandatory disclaimer: Quiet period management implements counsel's interpretation of Regulation FD. Interpretation of Reg FD safe harbors, materiality determinations, narrow exceptions, and material-event disclosure obligations during quiet period are counsel decisions. **Consult licensed securities counsel** for binding Reg FD interpretation, any narrow exception authorization, any material event response during quiet, and any inadvertent-disclosure remedy.

## Sources

- SEC Regulation FD Interpretations: https://www.sec.gov/divisions/corpfin/guidance/regfd-interp.htm
- NIRI Standards of Practice: https://www.niri.org/standards-of-practice
- Cooley Reg FD + Quiet Period: https://www.cooley.com/news/insights/reg-fd-quiet-period-best-practices
- Latham Reg FD Best Practices: https://www.lw.com/en/insights/regulation-fd-best-practices
- Davis Polk Reg FD Current Issues: https://www.davispolk.com/insights/regulation-fd-current-issues
- SEC Rule 168 + 169 (IPO Quiet Period): https://www.sec.gov/rules/final/33-8591.pdf
- EU Market Abuse Regulation (MAR): https://www.esma.europa.eu/policy-activities/market-abuse/market-abuse-mar
- See `role.md` -> "Quiet period playbook" + "Reg FD decision tree"

## Related skills

- `embargoed-disclosure-protocols` — closely related Reg FD framework.
- `equity-analyst-relations-briefings` — analyst 1:1s suspended during this.
- `8k-event-reporting` — Item 7.01 for material-event disclosure during quiet.
- `earnings-call-script-qa` — prep activity during quiet period.
- `roadshow-ndr-logistics` — NDR meetings suspended during this.
