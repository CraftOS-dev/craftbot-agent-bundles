<!--
Source: https://ilpa.org/best-practices/reporting/
Source: https://www.allvuesystems.com/lp-reporting/
Source: https://carta.com/learn/private-funds/lp-reporting/
Source: https://visible.vc/blog/lp-reporting-template/
Reference role.md: "LP reporting playbook"
Round 2 enrichment: full ILPA 3.0 quarterly LP report template + K-1 production workflow + LPAC meeting materials kit + Allvue/Carta LP/Affinity REST recipes.
-->

# Fund-of-funds + LP reporting (ILPA 3.0)

Drafts the quarterly LP report for fund GPs (VC / PE / fund-of-funds / family-office portfolios) per ILPA 3.0 standards. Covers capital calls + distributions + portfolio + NAV + IRR + MOIC + DPI + TVPI + management fees + carried interest. Annual K-1 / Schedule K-1 coordination with tax stack. Quarterly LPAC meeting materials.

## When to use

- Quarterly LP report drafting.
- Annual K-1 / Schedule K-1 production coordination.
- LPAC (Limited Partner Advisory Committee) meeting materials.
- Annual fund letter (GP narrative + portfolio + market view).
- Trigger phrases: "LP report", "LP letter", "ILPA report", "capital call letter", "K-1 coord", "LPAC materials", "annual fund letter".

NOT for: company-side investor update (use `monthly-investor-update-visible`); company-side board letter (use `quarterly-board-letter`); financial modeling of fund NAV/IRR (use `finance-agent`).

## Setup

```bash
# Allvue (preferred 2026 LP reporting platform)
export ALLVUE_API_KEY="<from Allvue Admin>"

# Carta LP Reporting (when on Carta)
export CARTA_LP_API_KEY="<from Carta Admin>"

# Affinity (CRM-led; relationship-driven)
export AFFINITY_API_KEY="<from Affinity Admin>"

# Visible.vc LP variant (alt)
export VISIBLE_API_KEY="<from Visible Settings>"
```

## ILPA 3.0 quarterly LP report sections

1. Letter from GP — performance + portfolio commentary + market view
2. Schedule of Investments — fair value + cost basis + multiple + IRR per position
3. Capital Account Statement per LP — contributions + distributions + NAV + unfunded commitment
4. IRR / TVPI / DPI / MOIC — fund-level
5. Realized + Unrealized — by vintage / sector / stage
6. Portfolio companies — 1-pager per top 10 holdings
7. Fund expenses — mgmt fees + carry + fund expenses
8. Capital calls + distributions schedule
9. Risk factors — LP-relevant
10. Disclosures — per ILPA template

## K-1 production

- Coordinate with tax / accounting on K-1 production
- LP-specific tax allocations
- Distribution + ECI / FDAP analysis

## LPAC meeting materials

- Quarterly (most funds) or semi-annual
- LP report + GP fund updates + investment pipeline + conflicts disclosures + budget

## Common recipes

```bash
# Allvue LP report pull
curl -H "Authorization: Bearer $ALLVUE_API_KEY" \
  "https://api.allvuesystems.com/v1/lp-reports?period=Q1-2026"

# Carta LP cap account
curl -H "Authorization: Bearer $CARTA_LP_API_KEY" \
  "https://api.carta.com/v1/lp-cap-accounts?fund_id=$FUND_ID"
```

## Examples

See `role.md` → "LP reporting playbook" for ILPA 3.0 report + K-1 coord + LPAC materials.

## Sources

- ILPA Reporting: https://ilpa.org/best-practices/reporting/
- Allvue LP Reporting: https://www.allvuesystems.com/lp-reporting/
- Carta LP Reporting: https://carta.com/learn/private-funds/lp-reporting/
- Visible.vc LP: https://visible.vc/blog/lp-reporting-template/
- See `role.md` → "LP reporting playbook"
