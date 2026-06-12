<!--
Source: https://nvca.org/wp-content/uploads/2019/06/NVCA-Model-Term-Sheet-1.doc
Source: https://www.foley.com/insights/publications/2025/10/breaking-down-the-nvca-what-founders-and-vcs-need-to-know/
Source: https://www.pillarlegalpc.com/series-a-term-sheet-liquidation-preference/
Reference role.md: "Term sheet review playbook"
-->

# Term sheet review — NVCA-grade (Oct 2025 model)

Clause-by-clause review of a priced-round term sheet against NVCA Model Documents (Oct 2025 update — U.S. industry benchmark). Standard 2026 economics: 1x non-participating preferred (98% of Q2 2025 U.S. rounds per Pillar Legal), broad-based weighted-average anti-dilution, single-trigger acceleration on involuntary termination + change-of-control. Control: 5-7 person board, standard protective provisions limited to enumerated list. New in Oct 2025: tranched financings formally addressed in SPA Annex.

## When to use

- Term sheet received from VC; founder needs market-vs-deviation analysis.
- Pre-negotiation prep — which clauses to push back on, which to accept.
- Counter-term-sheet drafting against incoming offer.
- Multi-offer comparison (term sheet A vs B vs C).
- Trigger phrases: "term sheet", "review terms", "liquidation preference", "anti-dilution", "protective provisions", "drag-along", "NVCA", "preferred terms".

NOT for: drafting binding docs (defer to `legal-counsel`); cap-table modeling (use `fundraising-strategy-priced-safe-venture-debt-rbf`).

## Setup

```bash
# NVCA Model Term Sheet (Oct 2025) — free
curl -O https://nvca.org/wp-content/uploads/2019/06/NVCA-Model-Term-Sheet-1.doc

# Cooley GO template library (free)
# https://www.cooleygo.com/documents/

# Carta Term Sheet Diff (paid; recipient may have)
```

## The NVCA model structure

```
1. Investment terms        — Round size, price per share, pre-money, post-money
2. Capitalization          — Pre + post cap table, including option pool top-up
3. Closing                 — Single close vs tranched (NEW Oct 2025: tranched in SPA Annex)
4. Dividends               — Cumulative vs non-cumulative; default non-cumulative
5. Liquidation Preference  — 1x non-participating (market) vs 1x participating (founder-unfriendly)
6. Conversion              — Automatic on IPO; optional otherwise
7. Anti-dilution           — Broad-based weighted-average (market) vs full-ratchet (founder-unfriendly)
8. Pay-to-Play             — Optional; pro-rata participation enforcement
9. Redemption              — Standard NVCA excludes; some funds push (resist)
10. Voting                 — Preferred votes as-converted to common
11. Protective provisions  — Enumerated list of preferred consent rights
12. Board                  — Composition (investor / founder / independent split)
13. Information rights     — Annual audit, quarterly + monthly mgmt accts, budget
14. Registration rights    — Demand, S-3, piggyback (post-IPO)
15. Right of First Refusal — On common transfers; founder common only
16. Right of Co-Sale       — Preferred ride along on common sales
17. Drag-Along             — Majority preferred + majority common forces sale
18. Pre-emptive rights     — Pro-rata in future rounds
19. Vesting                — 4yr w/ 1yr cliff (founder); acceleration on involuntary + CoC
20. Founder Activities     — Non-compete, non-solicit
21. No-shop                — 30-45 day exclusive negotiation period
22. Confidentiality        — Term sheet confidential
```

## Clause-by-clause: market vs deviation

### Liquidation Preference

```
MARKET 2026 (Pillar Legal Q2 2025):
  - 1x non-participating preferred (98% of US rounds)
  - Multiple liquidation tranches in seniority (Series B > Series A > Seed)

DEVIATIONS:
  - 1x participating  → double-dip; founder unfavorable; rare in healthy markets
  - 2x non-participating → unusual; signals concern about exit
  - Full participating → very founder-unfavorable; pushback hard
```

### Anti-dilution

```
MARKET 2026:
  - Broad-based weighted-average (BB-WA)

DEVIATIONS:
  - Narrow-based weighted-average → modestly worse for founders
  - Full ratchet → very founder-unfavorable; rare; signal of investor concern
  - No anti-dilution → very founder-favorable; rare in priced rounds
```

### Board composition

```
MARKET 2026 (typical Series A):
  - 5 seats: 2 founder + 2 investor + 1 mutual independent
  - Series B grows to 7: 2 founder + 3 investor + 2 independent

DEVIATIONS:
  - Investor-majority at Series A → founder-unfavorable; pushback
  - Independent picked solely by investor → pushback; should be mutual
```

### Protective provisions

```
NVCA standard list (preferred consent required):
  - Amend charter / bylaws
  - Issue stock senior or pari passu to existing preferred
  - Increase / decrease authorized stock
  - Liquidation / dissolution / change of control
  - Pay dividends to common
  - Repurchase stock (other than at-cost from terminated employees)
  - Sell assets > X% of company
  - Incur debt > $X
  - Change board size
  - Change # of preferred director seats
  - Engage in certain transactions with affiliates

DEVIATIONS:
  - Adding "hire/fire CEO" → founder-unfavorable
  - Adding "annual budget approval" → board work, not preferred consent
  - Removing standard items → founder-favorable
```

### Vesting + acceleration

```
MARKET 2026:
  - Founders: 4yr vesting, 1yr cliff (standard NVCA)
  - Double-trigger acceleration on Change of Control + Involuntary Termination
  - Single-trigger only on Death/Disability

DEVIATIONS:
  - Single-trigger CoC only → founder-favorable; common at Seed
  - No acceleration → very investor-favorable; pushback
  - "Cause" definition broad → investor-favorable; tighten language
```

## Common recipes

### Recipe 1 — Liquidation preference waterfall

```python
def lp_waterfall(exit_value, preferred_stack, common_shares, total_preferred_shares):
    """preferred_stack: list of dicts sorted by seniority desc.
    Each: {label, raise, lp_mult, participating, conv_shares}"""
    remaining = exit_value
    payouts = []
    for tranche in preferred_stack:
        lp = tranche["raise"] * tranche["lp_mult"]
        if remaining > 0:
            paid = min(lp, remaining)
            payouts.append({"label": tranche["label"], "type": "LP", "amount": paid})
            remaining -= paid
    # Common + preferred-as-converted split residual
    if remaining > 0:
        # For non-participating, each preferred class compares LP vs as-converted; takes max
        total_shares_for_residual = common_shares + sum(t["conv_shares"] for t in preferred_stack if not t["participating"])
        per_share = remaining / total_shares_for_residual if total_shares_for_residual > 0 else 0
        payouts.append({"label": "common + preferred-as-converted", "type": "residual", "amount": remaining, "per_share": per_share})
    return payouts

stack = [
    {"label": "Series B", "raise": 25_000_000, "lp_mult": 1.0, "participating": False, "conv_shares": 2_500_000},
    {"label": "Series A", "raise": 10_000_000, "lp_mult": 1.0, "participating": False, "conv_shares": 2_000_000},
    {"label": "Seed",     "raise": 3_000_000,  "lp_mult": 1.0, "participating": False, "conv_shares": 1_000_000},
]
print(lp_waterfall(80_000_000, stack, common_shares=6_500_000, total_preferred_shares=5_500_000))
```

### Recipe 2 — Anti-dilution price adjustment (BB-WA)

```python
def broad_based_wa_adjustment(prior_price, prior_shares_outstanding, prior_options_pool,
                                new_price, new_shares_issued):
    """BB-WA: NewCP = OldCP × (A + B) / (A + C)
    A = shares + options outstanding before new issuance
    B = new_issued_shares × new_price / prior_price (notional 'as-if-at-prior-price')
    C = new_issued_shares (actual)
    """
    A = prior_shares_outstanding + prior_options_pool
    B = (new_shares_issued * new_price) / prior_price
    C = new_shares_issued
    new_cp = prior_price * (A + B) / (A + C)
    return new_cp

# Down round: prior preferred at $5; raising new at $3.50; 2M new shares
print(broad_based_wa_adjustment(5.00, 8_000_000, 1_200_000, 3.50, 2_000_000))
```

### Recipe 3 — Pre + post cap-table impact (option pool top-up)

```python
def cap_table_post_round(pre_cap, raise_amount, pre_money_val, target_pool_post):
    pre_money_per_share = pre_money_val / pre_cap["total_shares"]
    new_shares = raise_amount / pre_money_per_share
    # Pool top-up paid by pre-money holders
    shares_pre_pool_adj = pre_cap["total_shares"] + new_shares
    target_pool_shares = shares_pre_pool_adj * target_pool_post / (1 - target_pool_post)
    additional_pool_shares = max(0, target_pool_shares - pre_cap.get("existing_pool", 0))
    post = {
        "founders": pre_cap["founders"],
        "common_holders": pre_cap.get("common_holders", 0),
        "existing_preferred": pre_cap.get("existing_preferred", 0),
        "new_preferred": new_shares,
        "option_pool": pre_cap.get("existing_pool", 0) + additional_pool_shares,
    }
    post["total"] = sum(post.values())
    post["dilution_to_founders"] = 1 - post["founders"] / post["total"] * (pre_cap["total_shares"] / pre_cap["founders"])
    return post

pre = {"founders": 7_000_000, "common_holders": 500_000, "existing_preferred": 2_000_000,
       "existing_pool": 1_000_000, "total_shares": 10_500_000}
print(cap_table_post_round(pre, 10_000_000, 30_000_000, target_pool_post=0.12))
```

### Recipe 4 — Term-sheet diff vs NVCA model

```python
DEVIATIONS = {
    "liquidation_pref": {
        "market": "1x non-participating",
        "yellow": ["1x participating", "1.5x non-participating"],
        "red":    ["2x or higher", "full participating"]
    },
    "anti_dilution": {
        "market": "broad-based weighted-average",
        "yellow": ["narrow-based weighted-average"],
        "red":    ["full ratchet"]
    },
    "board": {
        "market": "founder + investor + independent (e.g. 2-2-1)",
        "yellow": ["investor-majority"],
        "red":    ["investor picks independent solely", "no founder seat"]
    },
    "acceleration": {
        "market": "double-trigger on CoC + involuntary termination",
        "yellow": ["single-trigger CoC only (Seed-ok; A+ unusual)"],
        "red":    ["no acceleration", "broad 'cause' definition"]
    },
    "no_shop": {
        "market": "30-45 days",
        "yellow": ["60 days"],
        "red":    ["90+ days", "open-ended"]
    },
    "redemption": {
        "market": "none (NVCA standard)",
        "yellow": ["redemption right after 5yr at cost"],
        "red":    ["redemption at premium", "redemption after 3yr"]
    }
}

def review_term(clause_name, observed_value):
    if clause_name not in DEVIATIONS:
        return ("UNKNOWN", "Not in NVCA review map")
    d = DEVIATIONS[clause_name]
    if observed_value == d["market"]:
        return ("GREEN", "Market")
    if observed_value in d["yellow"]:
        return ("YELLOW", "Negotiable deviation")
    if observed_value in d["red"]:
        return ("RED", "Material deviation — push back hard")
    return ("REVIEW", "Non-standard; review case-by-case")

print(review_term("liquidation_pref", "1x participating"))
```

### Recipe 5 — Generate review memo

```python
def review_memo(term_sheet_dict, target_dict=DEVIATIONS):
    lines = ["# Term Sheet Review — NVCA Oct 2025 Benchmark\n"]
    for clause, observed in term_sheet_dict.items():
        flag, comment = review_term(clause, observed)
        lines.append(f"## {clause}\n- Observed: {observed}\n- Flag: {flag}\n- Comment: {comment}\n")
    return "\n".join(lines)
```

### Recipe 6 — Tranched financing analysis (NEW Oct 2025)

```python
def tranched_round_analysis(total_commitment, tranches):
    """tranches: list of {label, amount, milestone, trigger_event}"""
    total = sum(t["amount"] for t in tranches)
    assert abs(total - total_commitment) < 1, "Tranches must sum to commitment"
    # Risk: if milestones missed, second tranche may not fund. Model dilution if not.
    out = []
    cumulative = 0
    for t in tranches:
        cumulative += t["amount"]
        out.append({
            **t,
            "cumulative_pct": cumulative / total_commitment,
            "founder_risk": "missing milestone → tranche withheld → dilutive bridge"
        })
    return out

tranches = [
    {"label": "Tranche 1", "amount": 6_000_000, "milestone": "Sign-off", "trigger_event": "Close"},
    {"label": "Tranche 2", "amount": 4_000_000, "milestone": "$3M ARR by 12mo", "trigger_event": "Hit ARR target"},
]
print(tranched_round_analysis(10_000_000, tranches))
```

### Recipe 7 — Multi-offer comparison table

```python
import pandas as pd

def compare_offers(offers):
    """offers: list of term-sheet dicts"""
    return pd.DataFrame(offers).T

print(compare_offers([
    {"offer": "A", "pre_money": 30_000_000, "raise": 10_000_000, "lp_mult": 1.0, "participating": False, "board": "2-2-1"},
    {"offer": "B", "pre_money": 32_000_000, "raise": 10_000_000, "lp_mult": 1.0, "participating": True,  "board": "2-3-0"},
    {"offer": "C", "pre_money": 28_000_000, "raise": 8_000_000,  "lp_mult": 1.0, "participating": False, "board": "2-1-2"},
]))
```

## Examples

### Example 1: Series A term sheet review

**Goal:** Generate review memo for incoming term sheet.

**Steps:**
1. Recipe 5 → review memo against NVCA Oct 2025.
2. Recipe 1 → run LP waterfall at 3 exit prices ($50M, $100M, $200M).
3. Recipe 3 → cap-table impact w/ pool top-up.
4. Recipe 2 → anti-dilution scenarios (down round at -25%).
5. Flag RED items first, YELLOW second, GREEN as "market."
6. Recommend 3-5 push-backs prioritized by founder impact.

**Result:** Memo with prioritized negotiation list.

### Example 2: Compare 3 offers

**Goal:** Pick best blended offer.

**Steps:**
1. Recipe 7 → side-by-side table.
2. Recipe 1 → LP waterfall at common exit values.
3. Recipe 3 → cap-table dilution per offer.
4. Compute per-offer founder ownership at hypothetical $200M exit.
5. Weight non-economic factors (board composition, signaling, value-add).

**Result:** Defensible offer recommendation.

## Edge cases / gotchas

- **"Market" varies by stage.** Series A bar differs from Series B. Use stage-specific benchmarks (Pillar Legal Q2 2025).
- **Tranched rounds (Oct 2025 update).** Milestone-based; if milestone slips, second tranche may walk. Model dilution risk.
- **Option pool top-up is pre-money dilution.** Founders pay; investors don't. Negotiate target size against actual hiring plan.
- **"Cause" definition.** Investor will push broad; founders should narrow to material breach + felony + extended absence.
- **Drag-along thresholds.** Standard: majority preferred + majority common. Lower thresholds (e.g. just majority preferred) = founder-unfavorable.
- **Founder activities (non-compete).** Some states (CA) make non-competes unenforceable. Confirm jurisdiction.
- **Information rights gating.** Annual audit at scale; quarterly + monthly mgmt accts standard. Don't agree to weekly.
- **Pay-to-play.** Forces existing investors to participate in down rounds or convert to common. Founder-favorable; rare in healthy markets.
- **Redemption rights.** NVCA standard excludes; some funds push (resist). Mandatory redemption = pseudo-debt.
- **Founder cliff post-Series A.** Many term sheets reset founder vesting to 4yr from close. Push back: credit time served.
- **Drag thresholds + common quorum.** Read both; sometimes hidden gotcha.
- **No-shop period.** 30-45 days standard; longer locks founder out of competing process.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions. For binding legal interpretation, engage qualified startup counsel (Cooley, Wilson Sonsini, Goodwin, Latham, Fenwick).**

## Sources

- NVCA Model Term Sheet (Oct 2025): https://nvca.org/wp-content/uploads/2019/06/NVCA-Model-Term-Sheet-1.doc
- Foley NVCA Oct 2025 breakdown: https://www.foley.com/insights/publications/2025/10/breaking-down-the-nvca-what-founders-and-vcs-need-to-know/
- Pillar Legal LP standards Q2 2025: https://www.pillarlegalpc.com/series-a-term-sheet-liquidation-preference/
- Cooley GO templates: https://www.cooleygo.com/documents/
- Y Combinator standard docs: https://www.ycombinator.com/documents
- WSGR term sheet primer: https://www.wsgr.com/en/insights/the-startup-and-vc-term-sheet-explained.html
- NVCA full docset: https://nvca.org/model-legal-documents/

## Related skills

- `fundraising-strategy-priced-safe-venture-debt-rbf` — round-type decision precedes this skill.
- `409a-valuation-negotiation` — LP stack drives OPM inputs.
- `capital-structure-debt-equity-mix-stage` — preferred stack impact.
- `investor-data-room-curation` — supports diligence prior to term sheet.
