<!--
Source: https://www.sec.gov/files/rules/final/2023/33-11138.pdf
Source: https://www.cooley.com/news/insights/share-repurchase-programs-best-practices
Source: https://www.computershare.com/us/business/equity-services/ir-services
Source: https://carta.com/learn/cap-table/investor-relations/
Reference role.md: "Dividend / buyback / secondary playbook"
Round 2 enrichment: per-mechanic (dividend / buyback / secondary / tender) press release templates + 8-K body templates + 10b5-1 plan coord with counsel + transfer agent (Computershare/EQ) coord + Buffett-style capital allocation reaffirmation language.
-->

# Dividend / buyback / secondary / tender announcement comms

Drafts capital-return-mechanic comms — dividend initiation / increase, buyback authorization (10b5-1 plan), secondary offering (public co), tender offer (private co founder/employee secondary). Coordinates with `finance-agent` (capital allocation rationale + dilution math) and `legal-counsel` (10b5-1 plan + 8-K).

## When to use

- Dividend initiation / increase (public co; capital allocation reaffirmation).
- Buyback authorization (public co; 10b5-1 plan rule-based execution).
- Secondary offering (public co; prospectus supplement coord).
- Tender offer (private co; founder/employee secondary; ROFR/co-sale coord).
- Trigger phrases: "dividend announce", "buyback authorize", "10b5-1", "secondary offering", "tender offer", "capital return announce".

NOT for: capital allocation modeling (use `finance-agent`); routine 8-K (use `8k-event-reporting`); cap-table mechanics (use `monthly-investor-update-visible` for narrative; `finance-agent` for math).

## Setup

```bash
# Wire distribution
export BUSINESSWIRE_API_KEY="<from BW>"
export NOTIFIED_API_KEY="<from Notified>"

# Transfer agent (engagement-based)
# Computershare / EQ / Equiniti — record date + payment date + dividend disbursement

# Tools: docx for press release + 8-K body; xlsx for capital return math
```

## Dividend initiation / increase workflow

See `role.md` → "Dividend / buyback / secondary playbook" → "Dividend initiation / increase".

## Buyback authorization workflow

See `role.md` → "Dividend / buyback / secondary playbook" → "Buyback authorization".

## Secondary offering workflow

See `role.md` → "Dividend / buyback / secondary playbook" → "Secondary offering (public co)".

## Tender offer (private co) workflow

See `role.md` → "Dividend / buyback / secondary playbook" → "Founder/employee secondary (private co)".

## Common recipes

```bash
# Wire press release
curl -X POST -H "Authorization: Bearer $BUSINESSWIRE_API_KEY" \
  -d @capital_return_release.json \
  "https://api.businesswire.com/v1/releases"

# Form 4 / Form SR-related coord (for buyback Item 703 disclosure)
sec-edgar-mcp:fetch_filing --form=10-Q --section="Item 703"
```

## Examples

See `role.md` → "Dividend / buyback / secondary playbook" for per-mechanic workflows.

## Sources

- SEC Share Repurchase Rule: https://www.sec.gov/files/rules/final/2023/33-11138.pdf
- Cooley Share Repurchase: https://www.cooley.com/news/insights/share-repurchase-programs-best-practices
- Computershare IR Services: https://www.computershare.com/us/business/equity-services/ir-services
- Carta Cap Table IR: https://carta.com/learn/cap-table/investor-relations/
- See `role.md` → "Dividend / buyback / secondary playbook"
