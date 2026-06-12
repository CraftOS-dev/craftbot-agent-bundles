<!--
Source: https://www.sec.gov/divisions/corpfin/guidance/regfd-interp.htm
Source: https://www.lw.com/en/insights/regulation-fd-best-practices
Source: https://www.davispolk.com/insights/regulation-fd-current-issues
Source: https://www.cooley.com/news/insights/reg-fd-quiet-period-best-practices
Reference role.md: "Embargoed disclosure playbook"
Round 2 enrichment: NDA template + Reg FD audit register schema + counsel cross-check checklist + DocuSign integration.
-->

# Embargoed financial disclosure protocols

Manages embargoed pre-disclosure of material non-public information under NDA before public release. Counsel-driven; rare. Use cases: M&A counterparty diligence pre-announcement, IPO syndicate pre-launch, occasional pre-earnings preview to a tightly limited counsel-approved group. **Never used to help an analyst beat consensus.** **Defers binding Reg FD interpretation to `legal-counsel`.**

## When to use

- M&A counterparty diligence pre-announcement (under NDA + counsel sign-off).
- IPO syndicate pre-launch (managing underwriters + their selected accounts).
- Testing-the-waters with QIBs under Rule 163B pre-IPO.
- Wall-crossing for confidential financing (debt/equity).
- Rare counsel-approved analyst earnings preview (highly restricted).
- Trigger phrases: "embargoed disclosure", "embargo timing", "NDA + share", "Reg FD audit", "wall cross", "selective disclosure pre-clearance".

NOT for: routine analyst 1:1 (use `equity-analyst-relations-briefings`); 8-K Item 7.01 Reg FD disclosure (use `8k-event-reporting`); quiet-period mgmt (use `quiet-period-mgmt`); IPO Rule 163B testing-the-waters (use `roadshow-ndr-logistics`).

## NEVER permitted

- Selective preview to a favored analyst to help their model.
- Off-the-record number sharing with a top holder.
- Pre-disclosure to journalists for "exclusive" framing of bad news.
- "Soft" pre-tipping under any guise.
- Any selective sharing without NDA + counsel sign-off + Reg FD audit.

## Setup

```bash
# DocuSign for NDA signature (recipient supplies key)
export DOCUSIGN_API_KEY="<from DocuSign Admin>"

# Tools: docx for NDA + embargo memo; notion-mcp for Reg FD audit trail
# Counsel hand-off mandatory; legal-counsel signs every embargo
```

Auth / API key requirements:
- `DOCUSIGN_API_KEY` — DocuSign subscription (recipient supplies; ~$25/user/mo).
- Free fallback: PDF NDA + email + counsel-witnessed signature.
- Counsel is mandatory — never executed without licensed securities counsel sign-off.

Data inputs:
- Trigger event (M&A signing, IPO launch, wall-crossing).
- Counsel-supplied NDA template.
- Recipient list (counsel-approved).
- Specific MNPI to be shared.
- Embargo lift time.
- Wire/EDGAR release plan at embargo lift.

## Use cases + mechanics

### Use case 1: M&A counterparty diligence (pre-signing)

- Counterparty + counsel + advisors signed NDA before any MNPI shared.
- Walled-off team list documented.
- Trading restrictions on signatories (10-day blackout typical).
- Embargo lift = signing announcement (8-K + press release).

### Use case 2: IPO syndicate pre-launch

- Underwriters' research analysts walled-off under firewalls (Rule 137/138/139).
- Underwriters' sales force receives only public S-1 info.
- Pre-launch deal team + selected QIBs under NDA.
- Embargo lift = pricing announcement.

### Use case 3: Wall-crossing for confidential financing

- 5-15 selected institutional investors approached under NDA.
- Wall-cross gives them MNPI; receive their indication of interest.
- "Wall-crossed" investors locked out of trading until deal launches.
- Embargo lift = financing announcement (8-K + press release).
- Tracked in Reg FD audit register with counsel sign-off per investor.

### Use case 4: Rare counsel-approved analyst earnings preview

- Almost never done in modern practice; very high Reg FD risk.
- Even when permitted, narrow factual reaffirmation only; never new MNPI.
- Counsel typically denies.

## Mechanics (general)

1. Identify trigger + counsel sign-off.
2. NDA signed by recipient BEFORE info shared.
3. Embargo timing locked (e.g., "embargo lifts at 4:01 PM ET on [date]").
4. Recipient list documented in `notion-mcp` Reg FD register.
5. Wire release at embargo lift to make info Reg-FD-compliant (simultaneous broad dissemination).
6. Counsel post-embargo review.

## Reg FD audit register schema (notion-mcp)

```
DATE: YYYY-MM-DD
RECIPIENT (org): <name>
RECIPIENT (person): <name + title>
USE CASE: M&A / IPO syndicate / Wall-cross / Other
INFO SHARED: <summary; full memo linked>
NDA SIGNED: <date + DocuSign envelope ID>
EMBARGO LIFT TIME: <ISO timestamp>
COUNSEL APPROVAL: <name + date>
WIRE TIMING: <press release + 8-K planned ISO>
POST-EMBARGO REVIEW: <date + notes>
TRADING RESTRICTIONS: <recipient locked out until [date]>
DEAL ID: <internal tracker if applicable>
```

## Common recipes

### Recipe 1 — Counsel-supplied NDA template
```
[Counsel-supplied template]

THIS NDA is between [Company] and [Recipient]. Recipient acknowledges receipt of
Material Non-Public Information ("MNPI") relating to [topic]. Recipient agrees:

1. To maintain MNPI in strict confidence; restrict access to wall-crossed team;
2. Not to trade in [Company] securities until [embargo lift time];
3. To return or destroy MNPI on request;
4. To indemnify [Company] for any unauthorized disclosure;
5. ... [counsel-supplied additional terms]

Effective: [date]
Term: through [embargo lift + 5 business days]
Recipient signature: ___________________________
[Counsel-supplied additional provisions]
```

### Recipe 2 — DocuSign NDA send
```bash
curl -X POST -H "Authorization: Bearer $DOCUSIGN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "emailSubject": "NDA — [Topic] — Please Sign",
    "documents": [{"documentBase64": "...", "name": "NDA.pdf", "fileExtension": "pdf"}],
    "recipients": {
      "signers": [{
        "email": "recipient@firm.com",
        "name": "Jane Smith",
        "recipientId": "1",
        "routingOrder": "1",
        "tabs": {"signHereTabs": [{...}]}
      }]
    },
    "status": "sent"
  }' \
  "https://api.docusign.com/v2/envelopes"
```

### Recipe 3 — Reg FD audit register entry
```bash
mcp call notion-mcp create_page --database=$REG_FD_DB \
  --properties='{
    "Date": "2026-08-15",
    "Recipient Org": "Beta Capital",
    "Recipient Person": "Jane Smith, PM",
    "Use Case": "Wall-cross",
    "Info Shared": "Q2 2026 financial preview + financing terms",
    "NDA Signed": "2026-08-15 (DocSign env XYZ)",
    "Embargo Lift": "2026-08-22T20:01:00Z",
    "Counsel Approval": "John Doe, 2026-08-14",
    "Wire Timing": "2026-08-22T20:01:00Z",
    "Trading Restriction": "Locked out until 2026-08-23"
  }'
```

### Recipe 4 — Counsel cross-check checklist
```
Pre-embargo checklist (counsel-supervised):
[ ] Materiality determination documented
[ ] NDA executed and stored
[ ] Recipient list approved by counsel
[ ] Embargo lift timing locked + tied to wire release
[ ] Wire vendor briefed on embargo (Business Wire / PR Newswire)
[ ] 8-K Item 7.01 draft prepared for simultaneous filing (if needed)
[ ] Internal trading restriction list updated
[ ] Reg FD audit register entry made BEFORE info shared
```

### Recipe 5 — Embargo memo for recipients
```
SUBJECT: EMBARGOED — [Topic] — Embargo Lifts [Date Time ET]

[Recipient Name],
Per NDA executed [date], the attached MNPI is provided to you in strict
confidence. Embargo lifts at [Date Time ET] when [Company] will issue a press
release and 8-K Item 7.01.

You may not:
- Disclose the contents to anyone outside the wall-crossed team
- Trade in [Company] securities until [embargo lift + 1 business day]
- Discuss with parties not on the attached signed-NDA list

Questions: [Counsel name + email]

[IR or counsel signature]
```

### Recipe 6 — Wire timing coordination (Business Wire)
```bash
# Schedule simultaneous wire release at embargo lift
curl -X POST -H "Authorization: Bearer $BUSINESSWIRE_API_KEY" \
  -d '{
    "title": "[Company] Announces [Topic]",
    "body_html": "...",
    "embargo_until": "2026-08-22T20:01:00Z"
  }' \
  "https://api.businesswire.com/v2/releases"
```

### Recipe 7 — 8-K Item 7.01 simultaneous filing
```python
# Coordinates with 8k-event-reporting skill
# Item 7.01 Reg FD body referencing the embargoed disclosure becoming public
# File at embargo lift = same minute as wire release
```

### Recipe 8 — Post-embargo Reg FD review
```python
# Counsel reviews:
# 1. Did all recipients honor the embargo?
# 2. Any trading by walled-off party during restriction?
# 3. Any leak between embargo + lift?
# 4. Was wire release simultaneous + broad?
# Document findings in audit register
```

### Recipe 9 — Wall-crossing recipient list management
```python
# For confidential financing wall-cross
WALL_CROSS_RULES = {
    "max_recipients": "typically 5-15",
    "selection": "counsel + financial advisor + IR jointly select",
    "criteria": "size of likely participation; trustworthiness; trading discipline",
    "tracking": "Reg FD register + trading restriction notification",
}
```

### Recipe 10 — Leak detection post-embargo
```bash
# Monitor news / Twitter / Reddit for early signal pre-embargo
mcp call mention-mcp search --keyword "$COMPANY $TOPIC" --since "embargo-1d"
# Stock price action analysis pre-embargo
```

## Examples

### Example 1: M&A wall-cross to top holder

**Goal:** Pre-announce M&A signing to top-3 holder for support sign-on.

**Steps:**
1. Counsel + CEO + CFO + financial advisor decide wall-cross is appropriate.
2. Counsel-supplied NDA executed via DocuSign (Recipe 2) — top holder signs.
3. Reg FD register entry made BEFORE info shared (Recipe 3).
4. Embargo memo sent to recipient (Recipe 5).
5. MNPI shared in 60-min meeting (recipient + walled team only).
6. Top holder commits to vote support.
7. Embargo lifts at deal announcement (8-K + wire simultaneously).
8. Counsel post-embargo review (Recipe 8) — no leak; clean.

**Result:** Clean wall-cross; deal announces with anchor shareholder support.

### Example 2: IPO syndicate pre-launch

**Goal:** S-1 effective; 8 underwriters + selected QIBs receive pre-launch financials.

**Steps:**
1. Counsel + underwriters' counsel coordinate.
2. NDAs already in place for managing underwriters.
3. Recipient list (selected QIBs) counsel-approved.
4. NDAs to QIBs (Recipe 2).
5. Pre-launch financial info shared.
6. Trading restrictions enforced via firewalls (Rule 137/138/139).
7. Embargo lift = pricing release.
8. Reg FD register documented.

**Result:** Underwriters' team has full info; QIBs can size orders; clean IPO process.

### Example 3: Confidential debt financing wall-cross

**Goal:** Wall-cross 8 institutional debt investors for confidential refi.

**Steps:**
1. Financial advisor + counsel structure wall-cross.
2. 8 institutional debt investors receive NDA (Recipe 2).
3. Embargo memo (Recipe 5); MNPI shared in process.
4. 7 of 8 confirm participation interest; 1 declines but bound by NDA.
5. Deal launches; embargo lifts; wire + 8-K Item 1.01 (entry into material agreement).
6. Trading restrictions lift T+1.
7. Counsel review (Recipe 8).

**Result:** Refi closes cleanly; market hears as one announcement.

## Edge cases / gotchas

- **Counsel sign-off NEVER skipped.** No embargo without counsel; every step.
- **NDA + Reg FD register BEFORE info shared.** Document chain-of-custody preserved.
- **Recipient trading discipline.** Recipient must commit to no trading until embargo lift + 1 business day; counsel checks.
- **Embargo leak by recipient = securities fraud risk (insider trading).** SEC enforcement.
- **Wire vendor embargo capability.** Business Wire / PR Newswire have embargo features; smaller vendors may not.
- **Cross-channel timing skew.** Wire + 8-K + IR website must be simultaneous within ~minutes; >5 min skew = Reg FD risk.
- **Counsel may deny.** Many proposed embargoes get rejected by counsel as too risky; that's a feature.
- **Multi-recipient confidentiality.** Each recipient signs separate NDA; not group; counsel tracks each.
- **Trading restriction enforcement.** Internal team trading lists must be updated; insider-trading policy applies.
- **Press leak vs investor leak.** Press leaks pre-embargo = monitor with Recipe 10.
- **Underwriter analyst firewall (Rule 137/138/139).** IPO context; managing underwriters' research must be walled off from deal team.
- **Wall-cross overlap with quiet period.** Counsel may require deferral if conflict.
- **Reg FD audit register storage.** Notion is good for ops; some counsel prefer email archive or document mgmt system for legal hold.
- **Embargoed analyst preview = almost never appropriate.** Even when proposed; counsel usually denies.

> Mandatory disclaimer: Embargoed disclosure of material non-public information is governed by Regulation FD, securities anti-fraud rules (10b-5), and tender offer rules where applicable. **Consult licensed securities counsel** for every embargoed disclosure — recipient selection, NDA terms, embargo timing, wire coordination, and post-embargo review. This skill enforces the playbook; counsel approves every step. Selective MNPI disclosure without counsel sign-off + NDA + Reg FD audit trail is a federal securities violation.

## Sources

- SEC Regulation FD Interpretations: https://www.sec.gov/divisions/corpfin/guidance/regfd-interp.htm
- Latham Reg FD Best Practices: https://www.lw.com/en/insights/regulation-fd-best-practices
- Davis Polk Reg FD Current Issues: https://www.davispolk.com/insights/regulation-fd-current-issues
- Cooley Reg FD + Quiet Period: https://www.cooley.com/news/insights/reg-fd-quiet-period-best-practices
- SEC Rule 137/138/139 (IPO analyst firewalls): https://www.sec.gov/rules/final/33-8591.pdf
- SEC Rule 10b-5 (anti-fraud): https://www.law.cornell.edu/cfr/text/17/240.10b-5
- DocuSign API: https://developers.docusign.com/
- See `role.md` -> "Embargoed disclosure playbook"

## Related skills

- `quiet-period-mgmt` — same Reg FD framework; different window.
- `ma-investor-comms` — paired for M&A wall-cross sequence.
- `8k-event-reporting` — Item 7.01 simultaneous filing.
- `roadshow-ndr-logistics` — IPO TTW under Rule 163B is related but distinct.
- `equity-analyst-relations-briefings` — Reg FD context.
