<!--
Sources: FRED https://fred.stlouisfed.org/docs/api/fred/
         World Bank https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
         IMF https://www.imf.org/external/datamapper/api/help
         OECD SDMX-JSON https://data.oecd.org/api/
         Eurostat https://ec.europa.eu/eurostat/web/main/data/web-services
         BLS https://www.bls.gov/developers/
-->

# Authoritative time-series — FRED, World Bank, IMF, OECD, Eurostat, BLS

Six free, authoritative time-series databases that cover ~all macroeconomic, financial, demographic, and labor-market data you'd cite in a research deliverable. Always prefer these over secondary sources (news articles cite these; cite them directly).

## When to use this skill

- Macro inputs for TAM growth models (GDP, inflation, FX)
- Economic context for market research (interest rates, unemployment, consumer confidence)
- Cross-country comparison (World Bank `NY.GDP.MKTP.CD` for nominal GDP across countries)
- Long-history series (FRED goes back to early 1900s for some US series)
- Authoritative cite for any economic / demographic claim
- Labor-market analysis (BLS for US: wages, employment, JOLTS)
- Sector / industry-level data (Eurostat NACE codes, BLS NAICS codes)

## When NOT to use

- For company-specific financials → use `sec-edgar-market-sizing`
- For private-company data → use `crunchbase-market-research`
- For real-time market prices → these are not real-time feeds
- For very recent data (last 1-3 months) → some series lag a quarter or more

## Setup

```bash
# FRED — free key (instant from fredaccount.stlouisfed.org)
export FRED_API_KEY="..."
pip install fredapi

# World Bank — no key
pip install wbdata

# IMF Datamapper — no key
# OECD SDMX-JSON — no key
# Eurostat — no key
# BLS — free key for higher limits (https://data.bls.gov/registrationEngine/)
export BLS_API_KEY="..."
```

## FRED recipes

FRED has 816k+ economic series — the dominant resource for US macro and many international series.

### Recipe 1 — Single series

```python
from fredapi import Fred
fred = Fred(api_key=os.environ["FRED_API_KEY"])

gdp = fred.get_series("GDPC1")   # Real GDP, billions of chained 2017 dollars
cpi = fred.get_series("CPIAUCSL")  # CPI All Urban Consumers
ffr = fred.get_series("FEDFUNDS")  # Effective Federal Funds Rate
unemp = fred.get_series("UNRATE")  # Unemployment rate
```

Series IDs are searchable at https://fred.stlouisfed.org/.

### Recipe 2 — Multi-series merge

```python
import pandas as pd
df = pd.DataFrame({
    "GDP":   fred.get_series("GDPC1"),
    "CPI":   fred.get_series("CPIAUCSL"),
    "Unemp": fred.get_series("UNRATE"),
    "FedFunds": fred.get_series("FEDFUNDS"),
}).dropna()
```

### Recipe 3 — Series search by topic

```python
results = fred.search("housing starts", limit=20)
# Returns DataFrame with series IDs, titles, frequencies, last update
```

### Recipe 4 — Vintage data (point-in-time)

For historical-forecasting research you may need "what did the data say at time T" not the current revision:

```python
df_vintage = fred.get_series_first_release("GDPC1")
df_realtime = fred.get_series_all_releases("GDPC1")
```

## World Bank recipes

### Recipe 5 — Country-level indicator

```python
import wbdata, datetime as dt
data = wbdata.get_dataframe(
    {"NY.GDP.MKTP.CD": "gdp",                # GDP current USD
     "SP.POP.TOTL":    "population",
     "NY.GDP.PCAP.CD": "gdp_per_capita"},
    country=["USA","CHN","DEU","JPN","IND","BRA"],
    date=(dt.datetime(2010,1,1), dt.datetime(2025,1,1)),
)
```

Indicator IDs are searchable: `wbdata.search_indicators("inflation")`.

### Recipe 6 — All countries one indicator

```python
df = wbdata.get_dataframe({"NY.GDP.MKTP.CD": "gdp"}, date=dt.datetime(2024,1,1))
# Returns DataFrame indexed by country
```

## IMF recipes

### Recipe 7 — IMF Datamapper (no key)

```bash
# WEO GDP growth forecast for 2026
curl "https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH/USA/CHN/DEU?periods=2025,2026,2027"
```

The IMF DataMapper API exposes WEO (World Economic Outlook), FAD, and other databases. The indicator codes follow IMF conventions (`NGDP_RPCH` = real GDP growth, `PCPIPCH` = CPI inflation, `LUR` = unemployment).

## OECD SDMX-JSON recipes

### Recipe 8 — OECD time-series

```bash
# OECD CLI (Composite Leading Indicator) for major economies
curl "https://stats.oecd.org/sdmx-json/data/MEI_CLI/LOLITOAA.OECDE+USA+JPN+DEU+CHN.M/all?startTime=2024-Q1&endTime=2026-Q1"
```

The OECD SDMX-JSON API uses dataset codes (`MEI_CLI`) + dimension keys (`LOLITOAA.OECDE...`). The selector format is `INDICATOR.COUNTRY.FREQ` separated by `+` for multi-select.

OECD data browser: https://data.oecd.org/

## Eurostat recipes

### Recipe 9 — Eurostat (EU-level granular data)

```bash
curl "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/teicp000?lang=en&format=JSON"
# teicp000 = HICP - all-items annual rate of change
```

Eurostat datasets are coded by the table identifier. Browse at https://ec.europa.eu/eurostat/web/main/data/database.

## BLS recipes

### Recipe 10 — BLS time-series

```python
import requests, json
r = requests.post(
    "https://api.bls.gov/publicAPI/v2/timeseries/data/",
    headers={"Content-Type": "application/json"},
    data=json.dumps({
        "seriesid": ["LNS14000000"],  # Civilian unemployment rate
        "startyear": "2020", "endyear": "2026",
        "registrationkey": os.environ["BLS_API_KEY"],
    }),
)
print(r.json())
```

BLS series IDs follow conventions per program; full catalog at https://www.bls.gov/help/hlpforma.htm.

## Combining across sources

### Recipe 11 — Macro context table for a market deliverable

```python
df = pd.DataFrame({
    "US_GDP_growth": fred.get_series("A191RL1Q225SBEA").resample("Y").last(),  # real GDP %
    "US_CPI":        fred.get_series("CPIAUCSL").resample("Y").mean().pct_change(),
    "US_FedFunds":   fred.get_series("FEDFUNDS").resample("Y").mean(),
    "EU_GDP_growth": wbdata.get_dataframe({"NY.GDP.MKTP.KD.ZG":"v"}, country="EUU")["v"],
    "China_GDP_growth": wbdata.get_dataframe({"NY.GDP.MKTP.KD.ZG":"v"}, country="CHN")["v"],
}).tail(10)
```

Use this as the macro context table at the top of any market research deliverable.

## Edge cases

- **Frequency mismatch:** FRED returns native frequency (D/W/M/Q/A). When joining, resample to the lowest-common frequency before any cross-series math.
- **Revisions:** Most macro series are revised after first release. For backward-consistent analysis, use vintage data (FRED supports). For forward-looking deliverable, use latest revision.
- **Currency conversion:** GDP in USD (`MKTP.CD`) is in nominal current USD; for comparison use PPP (`MKTP.PP.CD`) or constant USD (`MKTP.KD`).
- **Country coverage:** World Bank has 200+ countries but uneven historical coverage. IMF / OECD cover their member states best.
- **Series discontinuation:** FRED retires series periodically (renames, methodology changes). Check the `notes` field on each series for revision history.
- **Series identifier conventions:** Memorize a small core (`GDPC1`, `CPIAUCSL`, `UNRATE`, `FEDFUNDS`, `DGS10`, `T10Y2Y`, `VIXCLS` for US; `NY.GDP.MKTP.CD`, `SP.POP.TOTL`, `FP.CPI.TOTL.ZG` for World Bank) and search the rest.
- **Polite-pool emails:** none of these enforce mailto, but it's polite.
- **Inflation adjustment:** when comparing values across years, deflate by CPI or use the chained-real series (`GDPC1` not `GDP`).

## Sources

- FRED API: https://fred.stlouisfed.org/docs/api/fred/
- FRED series search UI: https://fred.stlouisfed.org/
- fredapi Python: https://github.com/mortada/fredapi
- World Bank Indicators API: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
- wbdata: https://wbdata.readthedocs.io/
- IMF DataMapper API: https://www.imf.org/external/datamapper/api/help
- OECD SDMX-JSON: https://data.oecd.org/api/
- Eurostat REST API: https://ec.europa.eu/eurostat/web/main/data/web-services
- BLS Developers: https://www.bls.gov/developers/

## Related skills

- `sec-edgar-market-sizing` — company-specific complement to these macro series
- `kaggle-huggingface-datasets` — for non-authoritative but specific datasets
- `data-storytelling-plotly-altair` — visualize these series
