<!--
Sources: SCIP Ethical Intelligence https://www.scip.org/page/Ethical-Intelligence
         SCIP Code of Ethics implementation https://www.scip.org/page/Implementing-Competitive-Intelligence-Ethics-Policy
         Aqute — sticking to SCIP code https://www.aqute.com/blog/is-it-impossible-to-stick-to-scips-code-of-ethics
Companion playbook: role.md → "Ethical CI playbook (SCIP code)" + "Antipattern 5 — Pretexting"
-->

# Ethical public-source-only methodology (SCIP code enforcement)

SCIP Code of Ethics enforced on every move. **Hard nos:** pretexting, identity misrepresentation, login-walled scraping the agent doesn't have legitimate access to, social engineering, paying for insider info, recording without consent. **Soft cautions** (flag, don't auto-decline — defer to user): accidentally-public docs, Glassdoor scrape, aggressive trial-account use, gated community infiltration. Every CI deliverable carries a one-line provenance footer naming the source category + ethics class.

## When to use

- "Is this method SCIP-compliant?"
- Pre-deliverable provenance footer check
- Source addition / new method approval
- Gut-check on a borderline tactic
- Onboarding a new CI team member
- Post-incident review (a sales rep took an unethical shortcut)
- Building the per-source ToS-class register

## When NOT to use

- Pure authoring help → other authoring skills are SCIP-aware already
- Legal-binding compliance review → escalate to legal/GC
- Customer-facing privacy / GDPR → privacy-by-design + DPO consult

## Setup

```bash
# No paid tooling needed. Self-contained.
# Optionally: register of approved sources
mkdir -p data/ethics
# data/ethics/source-register.yaml
```

MCPs in `agent.yaml`: `firecrawl-mcp` (read robots.txt + ToS), `slack-mcp` (flag review queue), `linear-mcp` (review tickets).

## Common recipes

### Recipe 1: Source-register YAML

```yaml
# data/ethics/source-register.yaml
sources:
  - name: G2 reviews
    url_pattern: https://www.g2.com/products/*/reviews
    class: public
    method: scrape via Apify
    tos_review: 2026-05-01
    notes: Public reviews; respect robots.txt; commercial use OK per ToS section 4.

  - name: Glassdoor reviews
    url_pattern: https://www.glassdoor.com/Reviews/*
    class: ToS-grey-flagged
    method: scrape via firecrawl
    tos_review: 2026-05-01
    notes: ToS prohibits unauthorized scraping; soft-caution.
            Flag in every deliverable. Recipient approval required.

  - name: Competitor pricing page
    url_pattern: https://*/pricing
    class: public
    method: Visualping / firecrawl
    tos_review: rolling
    notes: Public-facing; element-level monitor permitted.

  - name: SEC EDGAR
    url_pattern: https://www.sec.gov/edgar/*
    class: public
    method: sec-edgar-mcp
    tos_review: 2026-01-01
    notes: Government public domain; rate-limit-respecting only.

  - name: LinkedIn public profile
    url_pattern: https://www.linkedin.com/in/*
    class: public-view-only
    method: linkedin skill (OAuth)
    notes: Public view OK; do NOT scrape pages outside OAuth-permitted endpoints;
           NEVER send unsolicited connection requests for CI purposes.

  - name: Sales Navigator saved-search export
    url_pattern: linkedin sales nav
    class: paid-licensed
    method: linkedin skill (OAuth)
    notes: Recipient must have valid seat; outputs are recipient's licensed data.

  - name: Reddit search
    url_pattern: https://reddit.com/*
    class: public
    method: reddit-mcp / PRAW
    notes: Public posts; respect anonymity — do NOT deanonymize.

  - name: Patent filings
    url_pattern: https://patents.uspto.gov/*
    class: public
    method: uspto-mcp
    notes: Government public domain.
```

### Recipe 2: Hard-no checklist (refuse + flag)

```python
HARD_NOS = [
    "pretexting",                       # impersonate a prospect/journalist/analyst
    "identity_misrepresentation",        # fake name / company / role
    "login_walled_scraping",             # scrape behind auth we don't have
    "recording_without_consent",         # call/meeting recording
    "insider_info",                       # pay employees, accept leaks
    "social_engineering",                 # manipulate to extract data
    "competitor_employee_pretexting",     # fake recruiter / fake buyer
    "fake_review_posting",                # write fake reviews
    "log_dump_extraction",                # stolen logs / data
    "unauthorized_api_use",               # use unauth credentials
]

def check_request(request_description):
    for n in HARD_NOS:
        if hard_no_pattern_match(n, request_description):
            return {"action": "REFUSE", "reason": f"SCIP hard no: {n}"}
    return {"action": "OK"}
```

### Recipe 3: Soft-caution flagger

```python
SOFT_CAUTIONS = {
    "accidentally_public_docs": "Public-by-mistake docs are technically public, ethically grey.",
    "glassdoor_scrape":          "Glassdoor ToS prohibits scraping; flag in provenance footer.",
    "aggressive_trial_signup":   "Multiple trial signups under fake identities = pretexting.",
    "gated_community":            "Joining a private Slack/Discord for CI may violate ToS.",
    "screenshot_paywalled":       "Paywalled content shared on Twitter = public, but flag.",
    "ex_employee_outreach":       "OK if they reach out organically; do NOT solicit confidential info.",
}

def check_soft(method):
    if method in SOFT_CAUTIONS:
        return {"action":"FLAG", "warning":SOFT_CAUTIONS[method], "recipient_approval":True}
    return {"action":"OK"}
```

### Recipe 4: Per-deliverable provenance footer (auto-generated)

```python
def provenance_footer(sources, ethics_class="public-source-only"):
    lines = [
        "─" * 60,
        f"SOURCES (retrieval timestamps + ethics class)",
        "─" * 60,
    ]
    for s in sources:
        lines.append(f"• {s['url']} ({s['category']}, {s['retrieved_at']}, {s['ethics_class']})")
    lines += [
        "─" * 60,
        f"ETHICS CLASS: {ethics_class} · SCIP-compliant",
        f"PMM APPROVED: {pmm_signoff_str()}",
        "─" * 60,
    ]
    return "\n".join(lines)
```

### Recipe 5: ToS-class pass via LLM

```python
import anthropic
client = anthropic.Anthropic()

def check_tos_class(source_url):
    # Pull robots.txt + visible ToS link
    robots = firecrawl_scrape(f"{root(source_url)}/robots.txt")
    tos    = firecrawl_scrape(find_tos_link(source_url))
    msg = client.messages.create(
        model="claude-opus-4-7-1m",
        max_tokens=2000,
        messages=[{"role":"user","content":f"""Classify the ToS class of scraping the URL below for competitive intelligence purposes.
Return JSON: {{class: public|ToS-grey|ToS-prohibited, evidence: quote_from_tos, recommend: proceed|flag|refuse}}

URL: {source_url}
robots.txt: {robots[:2000]}
ToS excerpt: {tos[:5000]}
"""}],
    )
    return json.loads(msg.content[0].text)
```

### Recipe 6: Two-source triangulation (kill-sheet pattern)

```python
def triangulate(claim, sources_found):
    return {
        "claim": claim,
        "n_sources": len(sources_found),
        "passes": len(sources_found) >= 2,
        "sources": sources_found,
        "if_one_source": "Flag claim, hold from kill-sheet" if len(sources_found) == 1 else None,
    }
```

Per role.md "Two-source triangulation" pattern.

### Recipe 7: SCIP ethical-CI decision tree

```
1. Is the data publicly accessible without login? → YES → proceed.
2. Does access require auth?
   2a. Auth I/recipient legitimately has? → YES → proceed.
   2b. Auth I/recipient does NOT have? → NO. Refuse.
3. Does method require impersonation?
   3a. YES → Refuse (hard no).
4. Does method record audio/video without explicit consent?
   4a. YES → Refuse (hard no).
5. Does method require payment to an insider?
   5a. YES → Refuse (hard no).
6. Is the source on the soft-caution list (Glassdoor / gated community / trial-spam)?
   6a. YES → Flag in deliverable; defer to recipient.
7. Otherwise → Proceed; document in provenance footer.
```

### Recipe 8: Trial-signup ethics-check

```python
def check_trial_signup(rep_real_id, recipient_purpose):
    return {
        "ok_if": [
            "Rep uses their real name + company",
            "Trial-signup ToS permits the use case",
            "Recipient is genuinely evaluating purchase fit OR doing approved CI",
        ],
        "not_ok_if": [
            "Fake name / fake company / fake role",
            "ToS prohibits CI use (some explicitly do)",
            "Multiple signups under different aliases (pretexting)",
        ],
        "must_document_in_deliverable": True,
    }
```

### Recipe 9: Buyer-interview vendor approval pattern

```yaml
# Klue Win/Loss, ClozeLoop, Primary Intelligence — all SCIP-compliant
# Self-run win/loss interviews also OK if:
#  - Buyer consented to interview
#  - Recording-with-consent only
#  - No insider-info coercion
```

### Recipe 10: Ex-employee outreach guardrail

```yaml
# If a former competitor employee reaches out organically:
allowed:
  - Listen to what they volunteer in public conversation.
  - Discuss public competitor information (positioning, pricing).

NOT allowed:
  - Ask for confidential roadmap details.
  - Ask for customer lists or pricing terms.
  - Ask for unreleased product specs.
  - Pay them for info.
  - Sign them under NDA to share confidential info.
```

### Recipe 11: Deliverable pre-publish ethics-check

```python
def ethics_check_deliverable(deliverable):
    issues = []
    for claim in deliverable["claims"]:
        if not claim.get("source_url"):
            issues.append(f"No source for: {claim['text'][:50]}")
        if claim.get("ethics_class") in ("ToS-grey-flagged","ToS-prohibited"):
            issues.append(f"Flag in footer: {claim['source_url']}")
    if not deliverable.get("provenance_footer"):
        issues.append("Missing provenance footer")
    return issues
```

### Recipe 12: Slack incident-flag

```python
def flag_ethics_incident(actor, action, source, severity="medium"):
    requests.post(SLACK_WEBHOOK_URL, json={
        "channel":"#ci-ethics-review",
        "text":f":warning: Ethics flag: {actor} attempted *{action}* on {source}. Severity: {severity}.",
    })
```

### Recipe 13: Quarterly source-register audit

```python
def audit_source_register():
    for s in source_register:
        if s["tos_review_age_months"] > 6:
            print(f"REVIEW: {s['name']} — ToS-class last verified {s['tos_review']}")
        if s.get("blocked") and not s.get("removed"):
            print(f"REMOVE: {s['name']} — blocked but still in register")
```

## Examples

### Example 1: New source request — should we use this?

**Request:** "Can I scrape competitor's customer-list from their case-study LP?"

**Steps:**
1. Recipe 5 → check ToS-class via LLM.
2. ToS allows case-study content viewing; commercial use grey if extracted to internal DB.
3. Recipe 7 → decision tree → no auth required → soft-caution flag.
4. Recipe 4 → add to provenance footer with `class: public, method: firecrawl, scope: customer-logos-on-public-case-studies`.

**Verdict:** Proceed; flag in footer; cite case-study URL per logo.

### Example 2: Rep asks "can I create a fake LinkedIn account to scope their sales team?"

**Steps:**
1. Recipe 2 → matches `identity_misrepresentation`. Hard no.
2. Recipe 12 → flag the request to #ci-ethics-review.
3. Offer SCIP-compliant alternative: Sales Nav saved search (`competitor-hiring-intel-linkedin-sales-nav` Recipe 1) under rep's real identity.

**Verdict:** Refuse; alternative provided.

### Example 3: Provenance footer on kill sheet

**Goal:** Render compliant footer.

**Steps:**
1. Pull all sources used in the kill sheet.
2. Recipe 4 → render footer.
3. Recipe 11 → ethics-check before publish.

**Output:**

```
─────────────────────────────────────────
SOURCES (retrieval timestamps + ethics class)
─────────────────────────────────────────
• https://www.g2.com/products/acme/reviews/45678 (G2 review, 2026-06-10, public)
• https://www.g2.com/products/acme/reviews/45712 (G2 review, 2026-06-10, public)
• https://www.trustradius.com/products/acme/reviews?#rev_88991 (TR review, 2026-06-09, public)
• https://acme.example.com/pricing (pricing page, 2026-06-11, public)
─────────────────────────────────────────
ETHICS CLASS: public-source-only · SCIP-compliant
PMM APPROVED: yes (signoff: 2026-06-09, @pmm-lead)
─────────────────────────────────────────
```

### Example 4: Glassdoor inclusion request

**Request:** PMM wants Glassdoor sentiment in next battlecard.

**Steps:**
1. Recipe 3 → SOFT_CAUTIONS flags `glassdoor_scrape`.
2. Recipient approval requested (e.g., legal / VP-PMM signoff).
3. If approved → Recipe 4 footer marks `glassdoor — ToS-grey-flagged`.
4. If denied → drop Glassdoor; substitute G2/TR sentiment + public press.

## Edge cases / gotchas

- **"Everyone does it"** — pretexting via fake-prospect demo is widespread in the field. Still a SCIP hard no; CraftBot refuses regardless of industry norm.
- **ToS-grey ≠ refused** — Glassdoor is grey, not refused; defer to recipient. Don't auto-block.
- **Accidentally-public docs** — Google Drive links shared publicly are technically public; ethically grey. Flag.
- **Ex-employee organic reach-out** — listening is OK; soliciting confidential is not. Recipe 10.
- **Buyer-interview vendors are SCIP-clean** — Klue Win/Loss, ClozeLoop, Primary Intelligence. Use them, not pretexting.
- **Robots.txt** — respect; treat `Disallow:` as soft signal even if not legally binding.
- **Rate-limit-respecting** — SEC EDGAR 10rps; respect. Bombardment = abuse.
- **Per-source ToS drift** — ToS change every few months; re-verify quarterly (Recipe 13).
- **Subpoena / litigation** — if recipient is in litigation with competitor, route through legal.
- **Recording calls for "training"** — explicit consent required; "this call is recorded for quality" common notice satisfies single-party consent in most US states, but EU + 2-party-consent states need both-party consent. Check jurisdiction.
- **Don't conflate ethics with legal** — SCIP is industry ethics code; some unethical acts are still legal, and vice versa. Both matter.
- **Anchor in role.md** — role.md "Ethical CI playbook (SCIP code)" is the canonical text; this skill operationalizes it.
- **PROACTIVE.md** — source-register review quarterly (Recipe 13).
- **Provenance footer is mandatory** — every deliverable carries it; Recipe 4 auto-generates.

## Sources

- SCIP Ethical Intelligence — https://www.scip.org/page/Ethical-Intelligence
- SCIP Code of Ethics implementation — https://www.scip.org/page/Implementing-Competitive-Intelligence-Ethics-Policy
- Aqute — Is it impossible to stick to SCIP's code? — https://www.aqute.com/blog/is-it-impossible-to-stick-to-scips-code-of-ethics
- role.md → "Ethical CI playbook (SCIP code)" + "Antipattern 5 — Pretexting" + "Provenance footer template"

## Related skills

- All other skills depend on this for ToS-class flagging
- `competitor-review-g2-trustradius-capterra` — Glassdoor flagging
- `competitor-hiring-intel-linkedin-sales-nav` — SCIP guardrails on outreach
- `competitor-product-teardown-depth` — trial-signup ethics-check
- `ci-delivery-slack-crm-klue-insider` — provenance footer in every digest item
