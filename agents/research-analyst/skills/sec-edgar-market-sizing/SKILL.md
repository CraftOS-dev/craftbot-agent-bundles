<!--
Source: https://www.sec.gov/edgar/sec-api-documentation
MCP: sec-edgar-mcp (already enabled in agent.yaml)
APIs: https://data.sec.gov/submissions/CIK{cik}.json
      https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json
      https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/Revenues.json
Rate limit: 10 rps with descriptive User-Agent header (no key)
-->

# SEC EDGAR XBRL — TAM / SAM / SOM from filings

Use SEC EDGAR's XBRL APIs to extract structured financial data from 10-K / 10-Q filings. Free, no API key, 10 rps with a polite `User-Agent` header. The single highest-leverage tool for market sizing: every public competitor's revenue, segments, geographies, costs, and forward guidance is here in machine-readable form.

## When to use this skill

- Market sizing (TAM / SAM / SOM) from public-company revenue + segment disclosures
- Competitive intelligence financial benchmarking (revenue, gross margin, R&D %, customer concentration)
- Industry growth rate calculation across N peer companies (5-year CAGR)
- Geographic / segment breakdown (which markets are growing, contracting?)
- Forward-guidance extraction (management's stated capex / revenue targets)
- Detecting accounting reclassifications (revenue line renames signal strategy shifts)
- Cross-checking analyst-report claims against primary filings

## When NOT to use

- Private company data → use Crunchbase / Similarweb instead
- Real-time stock prices → not in EDGAR; use a financial data vendor
- Non-US companies → only F-1 / 20-F filings (foreign private issuers); coverage is uneven
- Numerical data older than ~10 years → XBRL tagging started ~2009, sparse pre-2012

## Setup

```bash
# Polite User-Agent is REQUIRED — SEC blocks requests without one
export EDGAR_USER_AGENT="Research Analyst Agent name@example.com"

# All requests:
curl -A "$EDGAR_USER_AGENT" https://data.sec.gov/submissions/CIK0000320193.json
```

Or use `sec-edgar-mcp` (already enabled in `agent.yaml`).

## Core endpoints

| Endpoint | Returns | When to use |
|---|---|---|
| `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company={name}` | CIK lookup | Find the 10-digit CIK from company name |
| `https://data.sec.gov/submissions/CIK{cik10}.json` | Filing history + metadata | List all 10-K, 10-Q, 8-K filings |
| `https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json` | All XBRL facts | Bulk fetch every tagged value the company has ever reported |
| `https://data.sec.gov/api/xbrl/companyconcept/CIK{cik10}/us-gaap/{Concept}.json` | One concept over time | E.g., `Revenues`, `OperatingIncomeLoss`, `ResearchAndDevelopmentExpense` |
| `https://data.sec.gov/api/xbrl/frames/us-gaap/{Concept}/USD/CY{YYYY}Q{q}I.json` | All companies for one concept in one period | Cross-sectional industry comparison |

## Common recipes

### Recipe 1 — Find the CIK

```bash
# Browse-edgar full-text company name → CIK
curl -A "$EDGAR_USER_AGENT" \
  "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=Apple&type=10-K&dateb=&owner=include&count=10&output=atom"

# Apple → CIK 0000320193 (zero-padded to 10 digits)
```

### Recipe 2 — Pull entire company history (companyfacts)

```bash
curl -A "$EDGAR_USER_AGENT" \
  https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json \
  | jq '.facts."us-gaap".Revenues.units.USD[] | {form, fy, fp, end, val}'
```

The JSON structure:

```
{ "cik": 320193,
  "entityName": "Apple Inc.",
  "facts": {
    "us-gaap": {
      "Revenues": {
        "label": "Revenues",
        "units": {
          "USD": [
            {"form": "10-K", "fy": 2024, "fp": "FY", "end": "2024-09-28", "val": 391035000000, ...},
            ...
          ]
        }
      },
      ...
    },
    "dei": { ... }
  }
}
```

### Recipe 3 — Time series for one concept

```bash
curl -A "$EDGAR_USER_AGENT" \
  https://data.sec.gov/api/xbrl/companyconcept/CIK0000320193/us-gaap/Revenues.json \
  | jq '.units.USD | map(select(.form=="10-K" and .fp=="FY")) | sort_by(.end)'
```

### Recipe 4 — Cross-sectional industry comparison (frames)

Pull *every* US public company's revenue for a single fiscal period:

```bash
curl -A "$EDGAR_USER_AGENT" \
  "https://data.sec.gov/api/xbrl/frames/us-gaap/Revenues/USD/CY2024Q4I.json" \
  | jq '.data | sort_by(-.val) | .[0:50]'
```

Use to build a top-N industry leader table. Frame API note: instant (`I`) frames for balance-sheet items, duration (`D`) frames for income-statement items — check the docs for which concepts support which.

### Recipe 5 — TAM / SAM / SOM bottom-up build

```python
# Pseudocode — runs via cli-anything
import requests, pandas as pd

headers = {"User-Agent": os.environ["EDGAR_USER_AGENT"]}
peers = {
    "Apple":     "0000320193",
    "Microsoft": "0000789019",
    "Alphabet":  "0001652044",
    # ... 8-15 named peers in the segment
}

rows = []
for name, cik in peers.items():
    r = requests.get(f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/Revenues.json", headers=headers)
    for fact in r.json()["units"]["USD"]:
        if fact["form"] == "10-K" and fact["fp"] == "FY":
            rows.append({"company": name, "fy": fact["fy"], "rev_usd": fact["val"]})

df = pd.DataFrame(rows).pivot(index="fy", columns="company", values="rev_usd")
tam = df.sum(axis=1)                           # Approx TAM = sum of named peers
cagr_5y = (tam.iloc[-1] / tam.iloc[-6]) ** (1/5) - 1
# SAM = TAM × addressable-geo-or-segment-share
# SOM = SAM × realistic-capture-rate (typically 1-10% Y1, 10-30% Y3)
```

Caveat: this is **bottom-up named-peer TAM**, not analyst-report TAM. Note in deliverable that it excludes private players. Cross-check against IBISWorld / Statista (if accessible) or Crunchbase aggregate funding for the private-side estimate.

### Recipe 6 — Segment / geographic breakdown

Most 10-Ks tag segment revenue:

```bash
# Microsoft's Productivity & Business Processes segment revenue (custom tag)
curl -A "$EDGAR_USER_AGENT" \
  https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json \
  | jq '.facts."us-gaap" | keys | map(select(. | test("Segment"; "i")))'
```

For non-standard tags, look for `srt:RevenueFromExternalCustomersByGeographicAreasDomain` or custom company-namespace concepts.

### Recipe 7 — Forward-guidance extraction (from 10-K full text)

XBRL doesn't tag prose; for forward statements, fetch the 10-K HTML and grep for "guidance", "outlook", "fiscal 2025":

```bash
# Get most recent 10-K accession number
curl -A "$EDGAR_USER_AGENT" https://data.sec.gov/submissions/CIK0000320193.json \
  | jq '.filings.recent | [.form, .accessionNumber, .primaryDocument] | transpose | map(select(.[0]=="10-K"))[0]'

# Fetch the document, send the "Management's Discussion" section to Claude for extraction
```

## Concept name cheat sheet (us-gaap)

| Concept | Returns |
|---|---|
| `Revenues` | Total revenue |
| `RevenueFromContractWithCustomerExcludingAssessedTax` | ASC 606 revenue (post-2018) |
| `GrossProfit` | Gross profit |
| `OperatingIncomeLoss` | Operating income |
| `NetIncomeLoss` | Net income |
| `ResearchAndDevelopmentExpense` | R&D spend |
| `SellingGeneralAndAdministrativeExpense` | SG&A |
| `Assets` | Total assets (balance-sheet, use `I` frame) |
| `Liabilities` | Total liabilities |
| `StockholdersEquity` | Equity |
| `CashAndCashEquivalentsAtCarryingValue` | Cash balance |
| `LongTermDebt` | LT debt |
| `EmployeesNumberAtEndOfPeriod` (dei) | Employee count |

If a concept isn't returning data, the company may use a custom namespace tag — fall back to `companyfacts` and grep the keys.

## Edge cases

- **Fiscal year mismatch:** Apple's FY ends in late September; Microsoft's in late June. Compare on **calendar quarters** (`CY2024Q4I`) for cross-company benchmarking, or normalize to TTM (trailing twelve months).
- **Reclassifications:** Companies sometimes restate prior periods. The `fy` / `fp` tuple identifies the *reported* fiscal period; later filings may include restated values for the same period. Use the latest restated value.
- **Form 10-K/A amendments:** Treat amended filings as canonical over the original 10-K.
- **Currency:** Some foreign filers report in non-USD. The `units` key includes `USD`, `EUR`, etc. — pick the appropriate currency or convert via FRED FX time series.
- **Missing concept:** Smaller companies skip many us-gaap tags. Fall back to the textual 10-K and let Claude extract.
- **Polite-pool enforcement:** SEC will 403 / rate-throttle requests without a descriptive User-Agent. Always include name + email.
- **Bulk data:** For full-corpus analysis (every company × every period), download the bulk `companyfacts.zip` from https://www.sec.gov/Archives/edgar/daily-index/xbrl/ rather than hammering the API.

## Sources

- SEC EDGAR API documentation: https://www.sec.gov/edgar/sec-api-documentation
- XBRL frames documentation: https://www.sec.gov/structureddata/xbrl-data-frames
- Fair Access policy (User-Agent requirement): https://www.sec.gov/os/accessing-edgar-data
- us-gaap taxonomy browser: https://www.sec.gov/info/edgar/edgartaxonomies.shtml

## Related skills

- `crunchbase-market-research` — private-company complement
- `competitive-intelligence-tech-stack` — overlays SEC financials with tech / patent / pricing signals
- `authoritative-data-fred-worldbank` — for macro inputs (GDP, inflation) to TAM growth models
