<!--
Source: https://www.ey.com/en_us/services/strategy-transactions/joint-ventures-alliances
Source: https://jvalchemist.ankura.com/transactions/how-to-structure-a-joint-venture-the-five-essential-elements-of-jv-dealmaking/
Source: https://www.pwc.com/gx/en/services/deals/joint-ventures-and-alliances.html
Reference role.md: "Strategic partnership JV structuring playbook"
-->

# Strategic partnership / JV structuring — EY/Ankura 5-essential framework

JV / strategic alliance structuring using the Ankura JV Alchemist five essentials: (1) strategic rationale, (2) governance, (3) financing (capital calls, IRR waterfall, preferred return), (4) operating model, (5) exit. Equity-style JV: capital → preferred + common with waterfall. Commercial-style: revenue share, MFN, exclusivity, exit clauses. 2026 trend: alliance contagion across CEOs per EY-Parthenon.

## When to use

- Build vs buy vs partner decision lands on "partner."
- Strategic alliance with channel / OEM / co-development counterparty.
- Equity JV with strategic partner (e.g. 50/50 product co-development).
- Distribution / reseller agreement structuring with financial terms.
- Trigger phrases: "JV", "joint venture", "strategic partnership", "alliance", "co-development", "revenue share deal", "channel partnership", "MFN", "preferred return".

NOT for: full M&A (use `ma-target-screen-and-qoe`); build-vs-buy decision itself (corp dev framework).

## Setup

```bash
uvx --with pandas --with numpy python -c "import pandas, numpy"

# Engage:
# - Corp dev counsel (Cooley, Wilson Sonsini, Goodwin)
# - JV consulting (EY, PwC, Ankura)
```

## The 5-essential framework (Ankura)

```
ESSENTIAL 1 — STRATEGIC RATIONALE
  • What problem does the JV solve that solo execution cannot?
  • Why these counterparties? What does each bring?
  • What is the alternative (build / buy / license / status quo)?
  • Timeline + market window
  • Termination scenarios (success + failure)

ESSENTIAL 2 — GOVERNANCE
  • Board composition (parity, super-majority for key decisions)
  • Reserved matters (changes to scope, capital calls, IP licensing, exit)
  • CEO selection + reporting
  • Deadlock breaker (shotgun clause, buy-sell, mediator)
  • Reporting cadence + KPIs

ESSENTIAL 3 — FINANCING
  • Initial capital contributions (cash + IP + employee secondment)
  • Future capital calls (timing, trigger, dilution mechanism)
  • IRR waterfall (preferred return, catch-up, then split)
  • Distributions (timing, priority)
  • Loan vs equity contribution differentiation

ESSENTIAL 4 — OPERATING MODEL
  • Employee secondment vs hire
  • IP licensing (in / out)
  • Brand usage
  • Sales channel allocation (avoid channel conflict)
  • Customer ownership (joint vs. designated partner)
  • Cost-sharing methodology

ESSENTIAL 5 — EXIT
  • Right of first refusal / first offer (ROFR / ROFO)
  • Tag-along / drag-along
  • IPO + change-of-control mechanics
  • Buyout (put / call / shotgun)
  • Wind-down (asset distribution, employee transition)
  • Survivor obligations (non-compete, IP carve-outs)
```

## JV structure types

```
EQUITY JV (new entity formation)
  • 50/50 or 60/40 typical
  • Capital contributions = shares
  • Independent board
  • IP licensed in; new IP owned by JV
  • Tax: JV as separate entity (passthrough or corp)
  • Examples: chip co-development (Intel-Mobileye), e-com platform (TJX-Marmaxx)

COMMERCIAL ALLIANCE (no new entity)
  • Contract-based; no shared equity
  • Revenue share + cost share specifics
  • Each party retains own ops
  • MFN (most-favored-nation) clauses
  • Tax: bilateral revenue / expense
  • Examples: GTM partnership (Salesforce + AWS), reseller deal

CO-DEVELOPMENT ALLIANCE
  • Pool R&D resources; share output
  • Joint IP creation
  • Pre-agreed IP allocation
  • Royalty-bearing IP licensing post-development
  • Examples: pharma co-development (Pfizer-BioNTech)

CHANNEL / RESELLER
  • One party sells through other
  • Margin share (typical 15-40% to reseller)
  • Exclusivity + non-compete clauses
  • Examples: SaaS reseller programs
```

## Common recipes

### Recipe 1 — JV IRR waterfall

```python
def jv_waterfall(distribution_amount, partner_a_contrib, partner_b_contrib,
                  preferred_return_pct=0.08, catch_up=True, split_after_pref=(0.50, 0.50)):
    """Standard equity JV waterfall:
    1. Return of capital pro-rata
    2. Preferred return on capital
    3. Catch-up to GP (sponsor) for promote
    4. Split residual per pre-agreed share
    """
    total_contrib = partner_a_contrib + partner_b_contrib
    distrib = {}

    # Step 1: Return of capital
    if distribution_amount > 0:
        return_a = min(partner_a_contrib, distribution_amount * (partner_a_contrib / total_contrib))
        return_b = min(partner_b_contrib, distribution_amount * (partner_b_contrib / total_contrib))
        distrib["return_a"] = return_a
        distrib["return_b"] = return_b
        distribution_amount -= (return_a + return_b)

    # Step 2: Preferred return
    if distribution_amount > 0:
        pref_a = min(partner_a_contrib * preferred_return_pct, distribution_amount * 0.50)
        pref_b = min(partner_b_contrib * preferred_return_pct, distribution_amount * 0.50)
        distrib["pref_a"] = pref_a
        distrib["pref_b"] = pref_b
        distribution_amount -= (pref_a + pref_b)

    # Step 3: Residual split
    if distribution_amount > 0:
        distrib["residual_a"] = distribution_amount * split_after_pref[0]
        distrib["residual_b"] = distribution_amount * split_after_pref[1]

    return distrib

print(jv_waterfall(15_000_000, partner_a_contrib=4_000_000, partner_b_contrib=6_000_000))
```

### Recipe 2 — Build vs buy vs partner vs license matrix

```python
def matrix_scoring(option, time_to_market_months, total_cost_3yr, ownership_pct, strategic_differentiation):
    """Score by weight."""
    weights = {
        "time_to_market": 0.30,
        "total_cost": 0.25,
        "ownership": 0.25,
        "strategic_diff": 0.20
    }
    # Normalize (lower time/cost = better; higher ownership/diff = better)
    score = (
        weights["time_to_market"] * (1 - min(time_to_market_months / 36, 1)) +
        weights["total_cost"] * (1 - min(total_cost_3yr / 50_000_000, 1)) +
        weights["ownership"] * ownership_pct +
        weights["strategic_diff"] * (strategic_differentiation / 5)
    )
    return {"option": option, "score": round(score, 3)}

options = [
    {"option": "Build", "time": 18, "cost": 25_000_000, "ownership": 1.0, "diff": 5},
    {"option": "Buy", "time": 6, "cost": 35_000_000, "ownership": 1.0, "diff": 4},
    {"option": "Partner (JV)", "time": 9, "cost": 15_000_000, "ownership": 0.50, "diff": 3},
    {"option": "License", "time": 3, "cost": 8_000_000, "ownership": 0.0, "diff": 2},
]
for o in options:
    print(matrix_scoring(o["option"], o["time"], o["cost"], o["ownership"], o["diff"]))
```

### Recipe 3 — Capital call schedule

```python
def capital_call_schedule(total_commitment, partner_pct, call_milestones):
    """call_milestones: list of {month, pct_of_total}"""
    schedule = []
    for c in call_milestones:
        schedule.append({
            "month": c["month"],
            "call_amount": total_commitment * c["pct_of_total"] * partner_pct,
            "cumulative_pct": c.get("cumulative", 0)
        })
    return schedule

print(capital_call_schedule(
    total_commitment=20_000_000,
    partner_pct=0.40,
    call_milestones=[
        {"month": 0, "pct_of_total": 0.25},
        {"month": 6, "pct_of_total": 0.25},
        {"month": 12, "pct_of_total": 0.30},
        {"month": 18, "pct_of_total": 0.20},
    ]
))
```

### Recipe 4 — Revenue share computation

```python
def revenue_share(gross_revenue, hosting_cost, partner_a_share=0.60, partner_b_share=0.40):
    net_revenue = gross_revenue - hosting_cost
    return {
        "gross": gross_revenue,
        "hosting": hosting_cost,
        "net": net_revenue,
        "partner_a": net_revenue * partner_a_share,
        "partner_b": net_revenue * partner_b_share
    }

print(revenue_share(2_500_000, 280_000))
```

### Recipe 5 — Deadlock breaker mechanisms

```python
DEADLOCK_MECHANISMS = {
    "shotgun_clause": {
        "description": "Either party can offer to buy at price X; other must accept (sell at X) or buy (at X)",
        "use_when": "Both partners similar resources; trust each other to be reasonable",
        "risk": "Resource asymmetry → larger party always wins"
    },
    "buy_sell": {
        "description": "Specific party (initiator) sets price; other chooses buy or sell at that price",
        "use_when": "Want price-setter risk on initiator",
        "risk": "Can chill willingness to invoke"
    },
    "russian_roulette": {
        "description": "Both parties bid; lower bidder must sell at higher bid",
        "use_when": "Symmetric stakes",
        "risk": "Auction dynamic"
    },
    "neutral_mediation": {
        "description": "Pre-designated mediator (industry expert / former JV CEO) breaks tie",
        "use_when": "Operational disputes; need to keep relationship",
        "risk": "Mediator selection contentious post-fact"
    },
    "wind_down": {
        "description": "Pre-agreed wind-down + asset distribution",
        "use_when": "Strategic horizon ≤3yr; clean exit acceptable",
        "risk": "Sunk cost; loss of optionality"
    }
}
```

### Recipe 6 — IP allocation framework

```python
def ip_allocation_framework(background_ip_owners, joint_dev_ip, foreground_ip_rules):
    """Standard:
    - Background IP: each party retains; license in for JV use only
    - Joint development IP: jointly owned during JV; allocated on exit
    - Foreground IP: per pre-agreed rules (typically each party's domain)
    """
    return {
        "during_jv": {
            "background": "Each party retains; licenses to JV for limited purpose",
            "joint_dev": "Jointly owned; both parties may use within JV scope",
            "foreground": foreground_ip_rules
        },
        "on_exit": {
            "background": "Returns to each party",
            "joint_dev": "Buy-out OR shared license with non-compete + field-of-use restrictions",
            "foreground": "Per Foreground IP rules"
        }
    }
```

### Recipe 7 — Term sheet for commercial alliance

```markdown
# Strategic Alliance Term Sheet — Acme + PartnerCo

## Strategic Rationale
[Joint go-to-market for [segment]; combines Acme's [product] with PartnerCo's [reach]]

## Scope
- Territories: [list]
- Customer segments: [list]
- Duration: 3 years; auto-renew unless terminated
- Exclusivity: [Yes/No]; carve-outs: [list]

## Economic Terms
- Revenue share: [Acme X%, PartnerCo Y%]
- Joint marketing budget: [$X annually, split Z/W]
- Performance targets: [$X bookings Year 1; $Y Year 2; etc.]

## Operational Terms
- Joint go-to-market team: [X heads from each side]
- Branding: [co-branded / private label / partner-led]
- Customer ownership: [Acme owns / PartnerCo owns / joint]

## IP
- License: [Acme licenses [product] to PartnerCo on [terms]]
- Joint developments: [allocation rules]

## Governance
- Steering committee: [quarterly cadence; 2+2 reps]
- Operating committee: [monthly cadence]
- Conflict resolution: [escalation path; final: mediation]

## Termination
- For cause: [definitions]
- For convenience: [Y days notice; transitional support]
- Survival: [non-solicit, confidentiality, IP]
```

### Recipe 8 — Synergy quantification (NPV)

```python
def synergy_npv(annual_synergy, integration_cost, integration_years=3, wacc=0.12):
    """NPV of cumulative synergies net of integration cost."""
    pv = sum(annual_synergy / (1 + wacc) ** yr for yr in range(1, integration_years + 1))
    return {"pv_synergies": pv, "integration_cost": integration_cost, "net_pv": pv - integration_cost}

print(synergy_npv(annual_synergy=2_500_000, integration_cost=1_800_000))
```

### Recipe 9 — Pre-formation diligence checklist

```
Strategic fit:
  □ Product portfolio compatibility analysis
  □ Customer overlap (where is conflict?)
  □ Brand alignment

Financial:
  □ Partner financial health (recent statements, cap stack, debt covenants)
  □ Synergy model (Recipe 8)
  □ Tax implications of JV entity formation (use 'tax-strategy-qsbs-rd-credit-holdco')

Legal / IP:
  □ Background IP ownership clarified
  □ Field-of-use restrictions defined
  □ Joint dev IP allocation rules
  □ Trademark + domain handling

Governance:
  □ Decision rights matrix (RACI)
  □ Reserved matters list
  □ Deadlock mechanism
  □ Board composition

Operating model:
  □ Employee secondment policy
  □ Customer ownership rules
  □ Channel conflict resolution
  □ Reporting cadence

Exit:
  □ ROFR / ROFO triggers
  □ Buy-sell / shotgun mechanisms
  □ Wind-down procedures
  □ Survivor obligations
```

## Examples

### Example 1: Build vs Partner decision

**Goal:** Acme considering adding AI feature; build vs partner.

**Steps:**
1. Recipe 2 → matrix scoring; partner wins (faster time-to-market).
2. Recipe 9 → pre-formation diligence on partner.
3. Recipe 4 → revenue share modeling at expected volumes.
4. Recipe 7 → draft commercial alliance term sheet.
5. Recipe 8 → synergy NPV justification for board.

**Result:** Defensible partner-route decision.

### Example 2: 50/50 equity JV for international expansion

**Goal:** Acme + RegionalCo form 50/50 JV for APAC expansion.

**Steps:**
1. Recipe 1 → IRR waterfall; pref return on capital.
2. Recipe 3 → capital call schedule; $10M each over 18 months.
3. Recipe 5 → shotgun deadlock breaker.
4. Recipe 6 → IP allocation framework.
5. Recipe 9 → pre-formation diligence.
6. Recipe 7-style term sheet → equity JV variant.
7. Engage corp dev counsel (Cooley) for definitive docs.

**Result:** Operational JV; clear governance + exit.

## Edge cases / gotchas

- **JV failure rate 50-70%.** Most fail from misaligned strategic interest. Spend disproportionate time on Essential 1 (strategic rationale).
- **50/50 deadlock is the killer.** Pre-agreed deadlock breaker (Recipe 5) mandatory.
- **IP carve-outs are negotiated hardest.** Background vs joint dev vs foreground — get this in writing.
- **Channel conflict is the silent killer.** If JV sells to same customer as parent, customer ownership rules critical.
- **Tax structuring.** JV entity = corporate (sub-S, LLC) vs partnership. Affects tax + governance. Engage tax counsel.
- **Employee secondment.** Who pays salary; benefits continuity; non-solicit if JV terminates. Document.
- **Performance targets.** Build in measurable KPIs early; basis for termination for non-performance.
- **MFN clauses.** Most-favored-nation pricing protects partner from being undercut; complicates third-party deals.
- **Non-compete post-termination.** Standard 12-24 months; geographic + segment-specific.
- **Mutual termination for cause.** Define "cause" tightly (material breach + cure period).
- **Audit rights.** Each partner should have audit right on JV financials at least annually.
- **Branding rights.** If co-branded, who owns the co-brand? If JV terminates, brand goes where?

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions. JV / strategic partnership structuring requires licensed corp dev counsel + tax counsel.**

## Sources

- EY JVs and alliances: https://www.ey.com/en_us/services/strategy-transactions/joint-ventures-alliances
- Ankura JV Alchemist 5 essentials: https://jvalchemist.ankura.com/transactions/how-to-structure-a-joint-venture-the-five-essential-elements-of-jv-dealmaking/
- PwC JVs and alliances: https://www.pwc.com/gx/en/services/deals/joint-ventures-and-alliances.html
- McKinsey on alliances: https://www.mckinsey.com/business-functions/strategy-and-corporate-finance/our-insights
- HBR on JVs: https://hbr.org/2004/07/getting-real-about-strategic-alliances

## Related skills

- `capital-allocation-framework` — partner as one of 4 ladder priorities.
- `ma-target-screen-and-qoe` — alternative to JV.
- `tax-strategy-qsbs-rd-credit-holdco` — JV tax structuring.
- `international-entity-transfer-pricing` — cross-border JV.
- `term-sheet-nvca-grade-review` — for equity JV term sheets.
